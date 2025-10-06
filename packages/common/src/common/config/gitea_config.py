from pydantic import BaseModel, Field

from .base import TOML_CONFIG


class GiteaConfig(BaseModel):
    """Gitea 配置"""

    base_url: str = Field(
        default=TOML_CONFIG.get("gitea", {}).get("base_url", ""),
        description="Gitea 基础 URL",
    )
    token: str = Field(
        default=TOML_CONFIG.get("gitea", {}).get("token", ""),
        description="Gitea API 令牌",
    )
    webhook_secret: str = Field(
        default=TOML_CONFIG.get("gitea", {}).get("webhook_secret", ""),
        description="Webhook 密钥",
    )
