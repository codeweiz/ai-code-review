import logging.handlers
from pathlib import Path
from typing import Optional

from common.util.path_utils import find_project_root


# 设置 logging 环境
def setup_logging(
    log_level="INFO",
    log_file: Optional[str] = None,
    max_bytes=20 * 1024 * 1024,
    backup_count=10,
    console=True,
):
    # 查找项目根目录
    project_root = find_project_root() or Path.cwd()

    # 如果没有指定 log_file，默认放在项目根目录下 logs/app.log
    if log_file is None:
        log_file = project_root / "logs" / "app.log"
    else:
        log_file = Path(log_file)

    # 日志存储目录
    log_dir = log_file.parent
    if not log_dir.exists():
        log_dir.mkdir(parents=True, exist_ok=True)

    # 日志格式
    log_format = "[%(asctime)s] | %(levelname)s %(process)d %(threadName)s %(funcName)s:%(lineno)d | %(message)s"

    handlers = []

    # 文件转轮日志
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    file_handler.setFormatter(logging.Formatter(log_format))
    handlers.append(file_handler)

    # 控制台日志
    if console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(log_format))
        handlers.append(console_handler)

    logging.basicConfig(level=log_level, handlers=handlers, force=True)


# 自动执行初始化
setup_logging()

logger = logging.getLogger(__name__)
