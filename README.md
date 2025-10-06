# AI CODE REVIEW AI 代码审查工具

## 安装和设置

### 1. 安装 UV

如果还没有安装 UV，请先安装：

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 或者使用 pip
pip install uv
```

### 2. 安装项目依赖

在项目根目录运行：

```bash
# 安装所有工作空间的依赖
make install-dev
```

## 运行测试

### 运行所有测试

```bash
# 运行所有模块的测试
make test
```

### 代码格式化和检查

```bash
# 格式化代码
make format

# 类型检查
make lint
```
