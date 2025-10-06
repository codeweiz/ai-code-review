from pydantic import BaseModel, Field

from .base import TOML_CONFIG


class GithubConfig(BaseModel):
    """GitHub 配置"""

    base_url: str = Field(
        default=TOML_CONFIG.get("github", {}).get("base_url", ""),
        description="GitHub 基础 URL",
    )
    token: str = Field(
        default=TOML_CONFIG.get("github", {}).get("token", ""),
        description="GitHub API 令牌",
    )
    webhook_secret: str = Field(
        default=TOML_CONFIG.get("github", {}).get("webhook_secret", ""),
        description="Webhook 密钥",
    )
