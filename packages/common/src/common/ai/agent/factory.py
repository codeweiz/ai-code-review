from typing import List, Type

from common.ai.agent.builder import AgentBuilder
from common.ai.agent.core import BaseAgentState, BaseNode
from langchain_core.callbacks import BaseCallbackHandler
from langgraph.graph import END
from langgraph.graph.state import CompiledStateGraph


class AgentFactory:
    """Agent工厂类"""

    def __init__(self, trace_handler: BaseCallbackHandler = None):
        self._trace_handler = trace_handler

    def create_chain(
        self,
        state_class: Type[BaseAgentState],
        nodes: List[BaseNode],
    ) -> CompiledStateGraph:
        """创建简单的链式Agent"""

        if not nodes:
            raise ValueError("At least one node is required")

        builder = AgentBuilder(state_class, trace_handler=self._trace_handler)

        # 添加所有节点
        for i, node in enumerate(nodes):
            node_name = f"node_{i}" if not hasattr(node, "name") else node.name
            builder.add_node(node_name, node.ainvoke)

        # 设置入口节点
        first_node_name = "node_0" if not hasattr(nodes[0], "name") else nodes[0].name
        builder.set_entry(first_node_name)

        # 链式连接
        for i in range(len(nodes) - 1):
            from_name = f"node_{i}" if not hasattr(nodes[i], "name") else nodes[i].name
            to_name = (
                f"node_{i + 1}"
                if not hasattr(nodes[i + 1], "name")
                else nodes[i + 1].name
            )
            builder.connect(from_name, to_name)

        # 连接到END
        last_node_name = (
            f"node_{len(nodes) - 1}"
            if not hasattr(nodes[-1], "name")
            else nodes[-1].name
        )
        builder.connect(last_node_name, END)

        return builder.build()
