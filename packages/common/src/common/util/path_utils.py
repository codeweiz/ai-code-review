from pathlib import Path
from typing import Optional


def find_project_root(start_path: Optional[Path] = None) -> Optional[Path]:
    """
    查找项目根目录

    Args:
        start_path: 开始搜索的路径，默认为当前工作目录

    Returns:
        项目根目录路径，如果找不到返回 None
    """
    if start_path is None:
        start_path = Path.cwd()
    else:
        start_path = Path(start_path).resolve()

    current = start_path

    # 常见的项目根目录标志
    project_markers = [
        "Makefile",
        ".git",
    ]

    while current != current.parent:
        for marker in project_markers:
            if (current / marker).exists():
                return current
        current = current.parent

    return None
