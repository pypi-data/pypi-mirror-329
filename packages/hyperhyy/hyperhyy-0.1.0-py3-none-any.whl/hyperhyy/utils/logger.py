# utils/logger.py
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name: str = "accelerator", 
                log_level: int = logging.INFO,
                log_file: str = "accelerator.log") -> logging.Logger:
    """
    配置日志系统
    :param name: 日志器名称
    :param log_level: 日志级别
    :param log_file: 日志文件路径
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # 防止重复添加handler
    if logger.handlers:
        return logger

    # 控制台输出格式
    console_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # 文件输出格式
    file_format = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(module)s:%(funcName)s:%(lineno)d - %(message)s"
    )

    # 控制台handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_format)
    
    # 文件handler（自动轮转）
    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(file_format)

    # 添加处理器
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

# 初始化全局日志器
logger = setup_logger()