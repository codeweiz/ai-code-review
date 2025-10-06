from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, Optional, TypeVar

from pydantic import BaseModel


class BaseAgentState(BaseModel):
    """LangGraph 基础状态"""

    # 错误信息
    error: Optional[str] = None

    # 元数据
    metadata: Dict[str, Any] = {}

    # 当前步骤
    step: Optional[str] = None


StateT = TypeVar("StateT", bound=BaseAgentState)


class BaseNode(ABC, Generic[StateT]):
    """LangGraph 基础节点"""

    def __init__(self, name: Optional[str] = None):
        self.name = name or self.__class__.__name__

    @abstractmethod
    async def ainvoke(self, state: StateT) -> StateT:
        """异步执行节点"""
        pass
