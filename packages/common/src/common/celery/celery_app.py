from typing import List, Optional

from celery import Celery
from common.config import appConfig, logger


def create_celery_app(
    app_name: str,
    task_modules: Optional[List[str]] = None,
    task_routes: Optional[dict] = None,
) -> Celery:
    """创建 Celery 应用"""

    app = Celery(app_name)

    # 配置
    app.conf.update(
        broker_url=appConfig.redis.broker_url,
        result_backend=appConfig.redis.result_backend_url,
        # 序列化
        task_serializer="json",
        result_serializer="json",
        accept_content=["json"],
        # 时区
        timezone="UTC",
        enable_utc=True,
        # 任务路由
        task_routes=task_routes or {},
        # Worker配置
        worker_prefetch_multiplier=4,
        worker_max_tasks_per_child=1000,
        # 超时配置
        task_soft_time_limit=3600,
        task_time_limit=3900,
        # 结果配置
        result_expires=86400,
        task_acks_late=True,
        task_reject_on_worker_lost=True,
        # 监控
        worker_send_task_events=True,
        task_send_sent_event=True,
    )

    # 自动发现任务
    if task_modules:
        app.autodiscover_tasks(task_modules)

    logger.info(f"Celery app '{app_name}' 创建成功")
    return app
