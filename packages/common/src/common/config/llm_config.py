from pydantic import BaseModel, Field

from .base import TOML_CONFIG


class LLMConfig(BaseModel):
    """LLM 配置"""

    provider: str = Field(
        default=TOML_CONFIG.get("llm", {}).get("provider", ""), description="LLM 提供商"
    )
    model_name: str = Field(
        default=TOML_CONFIG.get("llm", {}).get("model_name", ""),
        description="LLM 模型名称",
    )
    api_key: str = Field(
        default=TOML_CONFIG.get("llm", {}).get("api_key", ""), description="LLM API Key"
    )
    base_url: str = Field(
        default=TOML_CONFIG.get("llm", {}).get("base_url", ""),
        description="LLM API Base URL",
    )
    temperature: float = Field(
        default=TOML_CONFIG.get("llm", {}).get("temperature", 0.7),
        description="LLM 温度参数",
    )
