from common.celery.celery_app import create_celery_app

# 任务路由配置
TASK_ROUTES = {
    "api.tasks.migration.*": {"queue": "migration"},
    "common.task.callback.*": {"queue": "callback"},
}

# Celery 实例
api_celery_app = create_celery_app(
    app_name="api_async_tasks",
    task_modules=[
        "api.tasks.migration",
        "common.task.callback",
    ],
    task_routes=TASK_ROUTES,
)
