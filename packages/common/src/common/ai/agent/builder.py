from typing import Any, Awaitable, Callable, Dict, Generic, TypeVar, Union

from common.ai.agent.core import BaseAgentState
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph

StateT = TypeVar("StateT", bound=BaseAgentState)


class AgentBuilder(Generic[StateT]):
    """Agent构建器"""

    def __init__(self, state_class: type[StateT], trace_handler=None):
        self.workflow = StateGraph(state_class)
        self.nodes: Dict[str, Any] = {}
        self._entry_set = False
        self._trace_handler = trace_handler

    def add_node(
        self, name: str, node: Callable[[StateT], Union[StateT, Awaitable[StateT]]]
    ):
        """添加节点 - 支持函数或节点实例"""
        if name in self.nodes:
            raise ValueError(f"Node '{name}' already exists")

        self.workflow.add_node(name, node)
        self.nodes[name] = node
        return self

    def set_entry(self, name: str):
        """设置入口节点"""
        if name not in self.nodes:
            raise ValueError(f"Node '{name}' does not exist")

        self.workflow.set_entry_point(name)
        self._entry_set = True
        return self

    def connect(self, src: str, dest: Union[str, type]):
        """连接节点"""
        from langgraph.graph import END

        # 特殊处理 END
        if dest != END and isinstance(dest, str) and dest not in self.nodes:
            raise ValueError(f"Destination node '{dest}' does not exist")
        if src not in self.nodes:
            raise ValueError(f"Source node '{src}' does not exist")

        self.workflow.add_edge(src, dest)
        return self

    def add_conditional_edge(
        self, src: str, condition: Callable, mapping: Dict[str, str]
    ):
        """添加条件边"""
        if src not in self.nodes:
            raise ValueError(f"Source node '{src}' does not exist")

        # 验证映射中的目标节点
        from langgraph.graph import END

        for dest in mapping.values():
            if dest != END and dest not in self.nodes:
                raise ValueError(f"Mapping destination '{dest}' does not exist")

        self.workflow.add_conditional_edges(src, condition, mapping)
        return self

    def chain(self, *node_names: str):
        """链式连接多个节点"""
        if len(node_names) < 2:
            raise ValueError("Chain requires at least 2 nodes")

        for name in node_names:
            if name not in self.nodes:
                raise ValueError(f"Node '{name}' does not exist in chain")

        for i in range(len(node_names) - 1):
            self.connect(node_names[i], node_names[i + 1])
        return self

    def build(self) -> CompiledStateGraph:
        """构建图"""
        if not self._entry_set:
            raise ValueError(
                "Entry point not set. Use set_entry() to specify the starting node."
            )
        if not self.nodes:
            raise ValueError("No nodes added. Use add_node() to add at least one node.")

        return self.workflow.compile()

    def get_callbacks(self) -> list:
        """获取 callbacks 列表，用于运行时传入"""
        if self._trace_handler:
            return [self._trace_handler]
        return []
