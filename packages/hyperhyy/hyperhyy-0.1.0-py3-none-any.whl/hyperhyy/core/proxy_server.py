from asyncio import QueueEmpty
import logging
from http.server import *
from .connection_pool import ConnectionPool
from .tls_handler import TLSHandler
import socket
from urllib.parse import *
import requests
from datetime import *
import threading
import re
from queue import *
import gzip
from io import BytesIO


class GzipCompressor:
    @staticmethod
    def compress(data: bytes, compression_level: int = 6) -> bytes:
        """压缩二进制数据"""
        buffer = BytesIO()
        with gzip.GzipFile(fileobj=buffer, mode='wb', compresslevel=compression_level) as f:
            f.write(data)
        return buffer.getvalue()

    @staticmethod
    def decompress(data: bytes) -> bytes:
        """解压缩数据"""
        with gzip.GzipFile(fileobj=BytesIO(data)) as f:
            return f.read()


class ConnectionPool:
    _instances = {}
    
    @classmethod
    def get_instance(cls, max_size=100):
        thread_id = threading.get_ident()
        if thread_id not in cls._instances:
            cls._instances[thread_id] = cls(max_size)
        return cls._instances[thread_id]

    def __init__(self, max_size):
        self.pool = Queue(max_size)
        self.max_size = max_size
        
    def get_session(self, host):
        try:
            return self.pool.get_nowait()
        except QueueEmpty:
            return requests.Session()
            
    def release_session(self, session):
        if self.pool.qsize() < self.max_size:
            self.pool.put(session)
        else:
            session.close()


class SecurityFilter:
    BAD_PATTERNS = [
        r'<script>.*?</script>',  # XSS检测
        r'\b(union|select|insert)\b',  # SQL注入检测
        r'\.\./'  # 路径遍历检测
    ]

    def check_request(self, handler):
        # 检查请求路径
        if any(re.search(pattern, handler.path) for pattern in self.BAD_PATTERNS):
            return False
        
        # 检查User-Agent
        user_agent = handler.headers.get('User-Agent', '')
        if 'curl' in user_agent.lower():
            handler.log('Blocked suspicious User-Agent')
            return False
        
        return True


class TieredCache:
    def __init__(self):
        self.memory_cache = {}
        self.disk_cache = {}
        self.lock = threading.Lock()

    def get(self, key):
        with self.lock:
            # 检查内存缓存
            entry = self.memory_cache.get(key)
            if entry and datetime.now() < entry['expire']:
                return entry['data']
            
            # 检查磁盘缓存
            entry = self.disk_cache.get(key)
            if entry and datetime.now() < entry['expire']:
                # 提升到内存缓存
                self.memory_cache[key] = entry
                return entry['data']
            
            return None

    def set(self, key, data, ttl=300):
        entry = {
            'data': data,
            'expire': datetime.now() + timedelta(seconds=ttl)
        }
        with self.lock:
            self.memory_cache[key] = entry
            if len(self.disk_cache) < 10000:  # 限制磁盘缓存大小
                self.disk_cache[key] = entry


class AcceleratorProxy:
    def __init__(self, config):
        self.config = config
        self.connection_pool = ConnectionPool(
            max_size=config.get('max_connections', 100)
        )
        self.logger = logging.getLogger(__name__)

    def start(self):
        server = ThreadingHTTPServer(
            (self.config['host'], self.config['port']),
            self._make_handler_class()
        )
        self.logger.info(f"Starting server on {self.config['host']}:{self.config['port']}")
        server.serve_forever()

    def _make_handler_class(self):
        config = self.config
        connection_pool = self.connection_pool

        class ProxyHandler(BaseHTTPRequestHandler):
            def do_CONNECT(self):
                """处理HTTPS CONNECT请求"""
                host, port = self.path.split(':')
                tls_handler = TLSHandler(config)
                
                try:
                    # 建立原始TCP连接
                    server_sock = socket.create_connection((host, port))
                    
                    # 发送连接成功响应
                    self.send_response(200, 'Connection Established')
                    self.end_headers()
                    
                    # 获取原始socket对象
                    client_sock = self.connection
                    
                    # 执行TLS拦截
                    tls_handler.intercept_tls(client_sock, server_sock)
                    
                except Exception as e:
                    self.send_error(500, f"TLS Handshake Failed: {str(e)}")
                finally:
                    server_sock.close()
            def do_GET(self):
                # 初始化关键组件
                cache = TieredCache()
                security = SecurityFilter()
                compressor = GzipCompressor()
                
                try:
                    # 1. 解析请求信息
                    url_parts = urlparse(self.path)
                    target_host = url_parts.hostname
                    target_port = url_parts.port or 80
                    full_url = self.path if self.path.startswith('http') else f'http://{self.path}'

                    # 2. 安全检测
                    if not security.check_request(self):
                        self.send_error(403, "Forbidden: Security check failed")
                        return

                    # 3. 缓存检查（仅缓存GET请求）
                    cache_key = f"{target_host}-{self.path}"
                    if cached_data := cache.get(cache_key):
                        self._send_cached_response(cached_data)
                        return

                    # 4. 获取连接池实例
                    conn_pool = ConnectionPool.get_instance()
                    session = conn_pool.get_session(target_host)

                    # 5. 构造转发请求头
                    headers = {
                        key: value 
                        for key, value in self.headers.items()
                        if key.lower() not in ['host', 'connection']
                    }
                    headers['Host'] = target_host

                    # 6. 转发请求
                    resp = session.get(
                        full_url,
                        headers=headers,
                        stream=True,
                        timeout=5
                    )

                    # 7. 读取响应内容
                    content = b""
                    for chunk in resp.iter_content(chunk_size=8192):
                        content += chunk

                    # 8. 压缩处理
                    accept_encoding = self.headers.get('Accept-Encoding', '')
                    if 'gzip' in accept_encoding and len(content) > 512:
                        compressed = compressor.compress(content)
                        content = compressed
                        resp.headers['Content-Encoding'] = 'gzip'
                        resp.headers['Content-Length'] = str(len(content))

                    # 9. 缓存响应（仅缓存成功响应）
                    if resp.status_code == 200:
                        cache.set(cache_key, {
                            'content': content,
                            'headers': dict(resp.headers),
                            'status': resp.status_code
                        }, ttl=300)

                    # 10. 返回响应给客户端
                    self.send_response(resp.status_code)
                    for key, value in resp.headers.items():
                        self.send_header(key, value)
                    self.end_headers()
                    self.wfile.write(content)

                except requests.exceptions.RequestException as e:
                    self.send_error(504, f"Gateway Timeout: {str(e)}")
                except Exception as e:
                    self.send_error(500, f"Internal Server Error: {str(e)}")
                finally:
                    # 释放连接回连接池
                    if 'session' in locals():
                        conn_pool.release_session(session)

            def log_message(self, format, *args):
                logging.info(format % args)

        return ProxyHandler