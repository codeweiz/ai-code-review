from pydantic import BaseModel, Field

from .base import TOML_CONFIG


class GiteeConfig(BaseModel):
    """Gitee 配置"""

    base_url: str = Field(
        default=TOML_CONFIG.get("gitee", {}).get("base_url", ""),
        description="Gitee 基础 URL",
    )
    token: str = Field(
        default=TOML_CONFIG.get("gitee", {}).get("token", ""),
        description="Gitee API 令牌",
    )
    webhook_secret: str = Field(
        default=TOML_CONFIG.get("gitee", {}).get("webhook_secret", ""),
        description="Webhook 密钥",
    )
