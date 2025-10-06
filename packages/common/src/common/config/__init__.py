"""
config 包初始化
"""

from .app_config import AppConfig, appConfig
from .log_config import logger, setup_logging

__all__ = ["AppConfig", "appConfig", "setup_logging", "logger"]
