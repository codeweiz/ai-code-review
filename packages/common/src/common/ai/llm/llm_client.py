from common.config import appConfig
from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel


class LLMClient:
    """LLM 客户端"""

    def __init__(self, trace_handler=None):
        self._client = None
        self._trace_handler = trace_handler
        self._load()

    def _load(self, **kwargs):
        callbacks = []
        if self._trace_handler:
            callbacks.append(self._trace_handler)

        self._client = init_chat_model(
            model_provider=appConfig.llm.provider,
            model=appConfig.llm.model_name,
            api_key=appConfig.llm.api_key,
            base_url=appConfig.llm.base_url,
            temperature=appConfig.llm.temperature,
            callbacks=callbacks,
            **kwargs,
        )

    @property
    def client(self) -> BaseChatModel:
        return self._client
