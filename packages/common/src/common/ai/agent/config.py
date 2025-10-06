from abc import ABC
from typing import Type

from common.ai.agent.core import BaseAgentState
from pydantic import BaseModel


class BaseAgentConfig(BaseModel, ABC):
    """Agent配置基类"""

    state_class: Type[BaseAgentState]


class BaseConnectionConfig(BaseModel):
    """连接配置"""

    from_node: str
    to_node: str
