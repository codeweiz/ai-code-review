import os

from pydantic import BaseModel, Field

from .base import TOML_CONFIG
from .db_config import DataSourceDictConfig
from .langsmith_config import LangSmithConfig
from .llm_config import LLMConfig
from .redis_config import RedisConfig


class AppConfig(BaseModel):
    """
    应用配置
    """

    llm: LLMConfig = Field(default_factory=LLMConfig, description="大语言模型配置")
    datasource: DataSourceDictConfig = Field(
        default_factory=lambda: DataSourceDictConfig.from_toml_list(
            TOML_CONFIG.get("datasource", [])
        ),
        description="SQL数据源配置",
    )
    redis: RedisConfig = Field(default_factory=RedisConfig, description="Redis 配置")
    langsmith: LangSmithConfig = Field(
        default_factory=LangSmithConfig, description="LangGraph 调用追踪配置"
    )


# 全局配置实例
appConfig = AppConfig()

# 设置不需要 Auth 校验
os.environ["DANGEROUSLY_OMIT_AUTH"] = "true"

# 设置 LangSmith 环境变量
if appConfig.langsmith.tracing:
    os.environ["LANGCHAIN_TRACING"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = appConfig.langsmith.api_key
    os.environ["LANGCHAIN_PROJECT"] = appConfig.langsmith.project
