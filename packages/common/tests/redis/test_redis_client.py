import unittest

from common.ioc.container import CommonContainer
from common.redis.redis_client import RedisClient
from dependency_injector.wiring import Provide, inject


class TestRedisClient(unittest.TestCase):
    """测试 Redis 客户端"""

    @classmethod
    def setUpClass(cls):
        cls.container = CommonContainer()
        cls.container.wire(modules=[__name__])

    @inject
    def setUp(self, redis_client: RedisClient = Provide[CommonContainer.redis_client]):
        """设置测试"""
        self.redis_client = redis_client.client

    def test_redis_connection(self):
        """测试 Redis 连接"""
        # 测试基本连接
        result = self.redis_client.ping()
        self.assertTrue(result)

    def test_redis_set_get(self):
        """测试 Redis 设置和获取"""
        key = "test_key"
        value = "test_value"

        # 设置值
        self.redis_client.set(key, value)

        # 获取值
        retrieved_value = self.redis_client.get(key)
        self.assertEqual(retrieved_value.decode("utf-8"), value)

        # 清理
        self.redis_client.delete(key)

    def test_redis_exists(self):
        """测试 Redis 键存在检查"""
        key = "test_exists_key"
        value = "test_value"

        # 键不存在
        self.assertFalse(self.redis_client.exists(key))

        # 设置键
        self.redis_client.set(key, value)

        # 键存在
        self.assertTrue(self.redis_client.exists(key))

        # 清理
        self.redis_client.delete(key)

    def test_redis_expire(self):
        """测试 Redis 键过期"""
        key = "test_expire_key"
        value = "test_value"

        # 设置带过期时间的键
        self.redis_client.setex(key, 1, value)  # 1秒过期

        # 立即检查应该存在
        self.assertTrue(self.redis_client.exists(key))

        # 检查TTL
        ttl = self.redis_client.ttl(key)
        self.assertGreater(ttl, 0)
        self.assertLessEqual(ttl, 1)

    def test_redis_delete(self):
        """测试 Redis 键删除"""
        key = "test_delete_key"
        value = "test_value"

        # 设置键
        self.redis_client.set(key, value)
        self.assertTrue(self.redis_client.exists(key))

        # 删除键
        deleted_count = self.redis_client.delete(key)
        self.assertEqual(deleted_count, 1)
        self.assertFalse(self.redis_client.exists(key))

    def tearDown(self):
        """清理测试"""
        # 清理所有测试键
        test_keys = [
            "test_key",
            "test_exists_key",
            "test_expire_key",
            "test_delete_key",
        ]
        for key in test_keys:
            self.redis_client.delete(key)


if __name__ == "__main__":
    unittest.main()
