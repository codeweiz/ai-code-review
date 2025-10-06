import unittest

from common.ai.llm.llm_client import LLMClient
from common.config import logger
from common.ioc.container import CommonContainer
from dependency_injector.wiring import Provide, inject


class TestLLMClient(unittest.IsolatedAsyncioTestCase):
    """测试 IOC 容器单例的 LLM 客户端"""

    @classmethod
    def setUpClass(cls):
        """初始化容器，wire 当前模块"""

        cls.container = CommonContainer()
        cls.container.wire(modules=[__name__])

    @inject
    def test_inject_llm1(self, llm: LLMClient = Provide[CommonContainer.llm_client]):
        self.assertIsInstance(llm, LLMClient)
        print(f"LLM id: {id(llm)}")

    @inject
    def test_inject_llm2(self, llm: LLMClient = Provide[CommonContainer.llm_client]):
        self.assertIsInstance(llm, LLMClient)
        print(f"LLM id: {id(llm)}")

    @inject
    async def test_inject_llm_chat(
        self, llm: LLMClient = Provide[CommonContainer.llm_client]
    ):
        res = await llm.client.ainvoke("你好，请问你叫什么名字？")
        logger.info(f"response from llm: {res.content}")
