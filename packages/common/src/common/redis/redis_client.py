import redis
from common.config import appConfig


class RedisClient:
    """Redis 客户端"""

    def __init__(self):
        self._client = None
        self._load()

    def _load(self):
        self._client = redis.Redis(
            host=appConfig.redis.host,
            port=appConfig.redis.port,
            password=appConfig.redis.password if appConfig.redis.password else None,
            db=appConfig.redis.db,
            max_connections=appConfig.redis.max_connections,
            socket_timeout=appConfig.redis.socket_timeout,
            socket_connect_timeout=appConfig.redis.socket_connect_timeout,
            decode_responses=False,
        )

    @property
    def client(self) -> redis.Redis:
        """获取 Redis 客户端"""

        return self._client
