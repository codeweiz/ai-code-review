from api.celery.app import api_celery_app
from api.ioc.container import ApiContainer
from celery.signals import worker_process_init
from common.config import logger, setup_logging
from dependency_injector import providers


@worker_process_init.connect
def init_worker(**kwargs):
    """Worker 进程初始化时重新配置日志"""
    setup_logging()
    logger.info("Worker 进程日志配置完成")


# 初始化 DI 容器
container = ApiContainer()
container.wire(
    modules=[
    ]
)


# 预热 IOC 单例
def preload_singletons(container):
    for provider in container.traverse():
        if isinstance(provider, providers.Singleton):
            try:
                provider()
            except Exception as e:
                target = getattr(provider.provides, "__name__", str(provider.provides))
                print(f"单例 {target} 预热失败: {e}")


preload_singletons(container)

if __name__ == "__main__":
    logger.info("启动 API Celery Worker...")
    api_celery_app.start()
