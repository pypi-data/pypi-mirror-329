import argparse
from .core.proxy_server import AcceleratorProxy
from .utils.config import load_config

def main():
    parser = argparse.ArgumentParser(description='Python Network Accelerator')
    parser.add_argument('-c', '--config', help='Config file path', default='config.yaml')
    parser.add_argument('--host', help='Bind host')
    parser.add_argument('-p', '--port', type=int, help='Listen port')
    args = parser.parse_args()

    config = load_config(args.config)
    if args.host:
        config['host'] = args.host
    if args.port:
        config['port'] = args.port

    proxy = AcceleratorProxy(config)
    proxy.start()

if __name__ == '__main__':
    main()