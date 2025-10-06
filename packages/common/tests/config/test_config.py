import unittest

from common.config import appConfig, logger


class TestConfig(unittest.TestCase):
    """测试配置"""

    def test_llm_config(self):
        """测试 LLM 配置"""
        self.assertEqual(appConfig.llm.provider, "ollama")
        self.assertEqual(appConfig.llm.model_name, "deepseek-r1:32b")
        self.assertEqual(appConfig.llm.api_key, "")
        self.assertEqual(appConfig.llm.base_url, "http://192.168.220.15:11434")

    def test_datasource_config(self):
        """测试多数据源配置"""
        logger.info(appConfig.datasource.list_datasource())
        self.assertEqual(len(appConfig.datasource.list_datasource()), 2)

    def test_redis_config(self):
        """测试 redis 配置"""
        self.assertEqual(appConfig.redis.port, 6379)
