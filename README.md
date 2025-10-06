# AI CODE REVIEW AI 代码审查工具

自动化 PR 代码质量审查工具，基于 LangChain + LangGraph + Deepseek LLM。

## 功能特点

- 监听 GitHub PR Webhook 事件
- 自动拉取 PR 的 diff、commit 信息
- 基于 LangChain + Deepseek LLM 进行代码质量分析
- 自动将分析结果评论到 PR
- 支持异步后台处理，主线程快速响应

## 技术栈

- **Web 框架**: FastAPI
- **LLM 集成**: LangChain + LangGraph
- **异步处理**: Celery + Redis
- **GitHub 交互**: GitHub REST API

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
