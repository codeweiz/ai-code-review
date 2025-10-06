import unittest

from common.config import logger
from common.ioc.container import CommonContainer
from common.semgrep.semgrep_client import SemgrepClient
from dependency_injector.wiring import Provide, inject


class TestSemgrepClient(unittest.TestCase):
    """测试 Semgrep 客户端"""

    @classmethod
    def setUpClass(cls):
        cls.container = CommonContainer()
        cls.container.wire(modules=[__name__])

    @inject
    def setUp(
        self, semgrep_client: SemgrepClient = Provide[CommonContainer.semgrep_client]
    ):
        """设置测试"""
        self.semgrep_client = semgrep_client

    def test_semgrep_client_scan(self):
        """测试 Semgrep 客户端扫描"""
        result = self.semgrep_client.scan(
            target={
                "main.py": "import os\nos.system(user_input)\na=1/0",
                "utils.py": "eval(code);;",
            },
            config="p/python",
        )
        logger.info(result)

        # 校验可以检测出 ; 的问题


if __name__ == "__main__":
    unittest.main()
