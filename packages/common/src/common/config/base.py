"""
基础配置加载模块
"""

from pathlib import Path

import toml
from common.util.path_utils import find_project_root

# 项目根目录
project_root = find_project_root() or Path.cwd()

# 加载配置文件
try:
    with open(project_root / ".config.toml") as f:
        TOML_CONFIG = toml.load(f)
except FileNotFoundError:
    TOML_CONFIG = {}
