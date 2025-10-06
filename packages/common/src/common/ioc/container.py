from common.ai.llm.llm_client import LLMClient
from common.orm.session_factory import DatabaseSessionFactory
from common.redis.redis_client import RedisClient
from common.util.thread_pool_service import ThreadPoolService
from dependency_injector import containers, providers


class CommonContainer(containers.DeclarativeContainer):
    """管理公共包的单例"""

    # 大语言模型客户端
    llm_client = providers.Singleton(LLMClient)

    # 数据库连接工厂
    db_session_factory = providers.Singleton(DatabaseSessionFactory)

    # Redis 客户端
    redis_client = providers.Singleton(RedisClient)

    # 线程池服务
    thread_pool_service = providers.Singleton(ThreadPoolService)
