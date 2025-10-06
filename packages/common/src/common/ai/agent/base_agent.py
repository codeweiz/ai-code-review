from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type

from common.ai.agent.core import BaseAgentState
from common.ai.agent.factory import AgentFactory
from langgraph.graph.state import CompiledStateGraph


class BaseAgent(ABC):
    """Agent 基类"""

    def __init__(self, agent_factory: AgentFactory):
        self._agent = None
        self._agent_factory = agent_factory
        self._load()

    @abstractmethod
    def _load(self):
        """子类实现具体的 agent 构建逻辑"""
        pass

    @property
    def agent(self) -> CompiledStateGraph[Type[BaseAgentState]]:
        return self._agent

    async def ainvoke(
        self,
        state: Type[BaseAgentState],
        config: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """统一的 ainvoke 方法，自动添加 callbacks"""
        if config is None:
            config = {}

        if self._agent_factory._trace_handler:
            callbacks = config.get("callbacks", [])
            if self._agent_factory._trace_handler not in callbacks:
                callbacks.append(self._agent_factory._trace_handler)
            config["callbacks"] = callbacks

        return await self._agent.ainvoke(state, config=config)
