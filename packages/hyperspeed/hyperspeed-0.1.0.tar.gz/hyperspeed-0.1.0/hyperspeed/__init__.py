# hyperspeed/__init__.py
__version__ = "0.1.0"
__author__ = "Huang Yiyi 363766697@qq.com"

# 导出核心类
from .core.proxy_server import AcceleratorProxy
from .cli import main

# 导出工具类
from .utils.logger import logger
from .utils.config import load_config

__all__ = [
    'AcceleratorProxy',
    'main',
    'logger',
    'load_config'
]