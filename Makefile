.PHONY: install install-dev clean lint format run-backend run-worker run-flower

# 安装依赖
install:
	uv sync

# 安装开发依赖
install-dev:
	uv sync
	uv sync --extra dev

# 清理项目
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# 代码检查
lint:
	uv run ruff check .
	uv run black --check .
	uv run isort --check .

# 代码格式化
format:
	uv run ruff check --fix .
	uv run black .
	uv run isort .

# 启动后端接口：单机多进程 --workers 4
run-backend:
	uv run uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

# 启动 Celery Worker，pool：默认 prefork，有问题就用 --pool=solo
run-worker:
	uv run celery -A api.celery.worker worker --loglevel=info --concurrency=4 --queues=migration,callback,celery --pool=solo -n $(or $(WORKER_NAME), worker-$(shell date +%s)-$(shell head -c 4 /dev/urandom | xxd -p)@%h)

# 启动 Flower 监控面板，访问 http://ip:5555
run-flower:
	uv run celery -A api.celery.app flower --port=5555 --address=0.0.0.0
