from pydantic import BaseModel, Field

from .base import TOML_CONFIG


class LangSmithConfig(BaseModel):
    """
    LangSmith 配置
    """

    tracing: bool = Field(
        default=TOML_CONFIG.get("langsmith", {}).get("tracing", False),
        description="LangSmith Tracing",
    )
    project: str = Field(
        default=TOML_CONFIG.get("langsmith", {}).get("project", "default"),
        description="LangSmith Project",
    )
    api_key: str = Field(
        default=TOML_CONFIG.get("langsmith", {}).get("api_key", ""),
        description="LangSmith API Key",
    )
