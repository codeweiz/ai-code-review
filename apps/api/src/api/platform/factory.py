from typing import Dict, List, Type

from api.platform.base import GitPlatform
from common.config import logger


class GitPlatformFactory:
    """代码平台工厂"""

    _providers: Dict[str, Type[GitPlatform]] = {}
    _instances: Dict[str, GitPlatform] = {}

    @classmethod
    def register(cls, platform_name: str, platform_class: Type[GitPlatform]):
        """注册 Git 平台类型"""
        logger.info(f"注册 Git 平台类型：{platform_name}")
        cls._providers[platform_name.lower()] = platform_class

    @classmethod
    def create_instance(cls, platform_name: str) -> GitPlatform:
        """创建 Git 平台实例"""
        key = platform_name.lower()

        if key in cls._instances:
            return cls._instances[key]

        platform_class = cls._providers[key]
        instance = platform_class()
        cls._instances[key] = instance
        logger.info(f"创建 Git 平台实例：{platform_name}")
        return instance

    @classmethod
    def get_supported_platforms(cls) -> List[str]:
        """获取支持的 Git 平台"""

        return list(cls._providers.keys())

    @classmethod
    def is_supported(cls, platform_name: str) -> bool:
        """检查 Git 平台是否支持"""

        return platform_name.lower() in cls._providers


def get_git_platform(platform_name: str) -> GitPlatform:
    """根据 Git 平台名称获取 Git 平台"""

    return GitPlatformFactory.create_instance(platform_name)


def register_platform(platform_name: str):
    """Git 平台注册装饰器"""

    def decorator(platform_class: Type[GitPlatform]):
        GitPlatformFactory.register(platform_name, platform_class)
        return platform_class

    return decorator
