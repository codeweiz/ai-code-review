from pydantic import BaseModel, Field

from .base import TOML_CONFIG


class RedisConfig(BaseModel):
    """Redis 配置"""

    host: str = Field(
        default=TOML_CONFIG.get("redis", {}).get("host", "localhost"),
        description="Redis主机地址",
    )

    port: int = Field(
        default=TOML_CONFIG.get("redis", {}).get("port", 6379),
        description="Redis端口",
    )

    password: str = Field(
        default=TOML_CONFIG.get("redis", {}).get("password", ""),
        description="Redis密码",
    )

    db: int = Field(
        default=TOML_CONFIG.get("redis", {}).get("db", 0),
        description="Redis数据库编号",
    )

    max_connections: int = Field(
        default=TOML_CONFIG.get("redis", {}).get("max_connections", 10),
        description="连接池最大连接数",
    )

    socket_timeout: int = Field(
        default=TOML_CONFIG.get("redis", {}).get("socket_timeout", 5),
        description="Socket超时时间（秒）",
    )

    socket_connect_timeout: int = Field(
        default=TOML_CONFIG.get("redis", {}).get("socket_connect_timeout", 5),
        description="Socket连接超时时间（秒）",
    )

    @property
    def broker_url(self) -> str:
        """构建Celery Broker URL"""
        if self.password:
            return f"redis://:{self.password}@{self.host}:{self.port}/{self.db}"
        return f"redis://{self.host}:{self.port}/{self.db}"

    @property
    def result_backend_url(self) -> str:
        """构建Celery结果存储URL"""
        result_db = self.db + 1  # 使用不同的数据库存储结果
        if self.password:
            return f"redis://:{self.password}@{self.host}:{self.port}/{result_db}"
        return f"redis://{self.host}:{self.port}/{result_db}"
