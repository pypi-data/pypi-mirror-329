# VinehooLLM

A Python package for interacting with OpenAI-compatible Language Models (LLMs) with function/tool calling capabilities.

[English](#english) | [中文](#中文)

<a name="english"></a>
## English

### Overview
VinehooLLM is a Python client library that provides a simple interface for interacting with OpenAI-compatible Language Models. It supports modern features like function/tool calling and is designed to be easy to use while maintaining flexibility.

### Features
- OpenAI-compatible API support
- Function/tool calling capabilities
- Type-safe implementation using Pydantic models
- Automatic function execution handling
- Customizable API endpoints
- Comprehensive error handling

### Installation
```bash
pip install vinehoollm
```

### Publishing to PyPI
To publish the package to PyPI, follow these steps:

1. Install build and twine:
```bash
pip install build twine
```

2. Update version in `setup.py` or `pyproject.toml`

3. Build the package:
```bash
python -m build  # This modern command replaces the legacy "python setup.py sdist bdist_wheel"
```

4. Upload to PyPI:
```bash
# Test PyPI (recommended for testing)
python -m twine upload --repository testpypi dist/*

# Official PyPI
python -m twine upload dist/*
```

### Quick Start
```python
from vinehoollm.client import VinehooLLM, ChatMessage

# Initialize the client
client = VinehooLLM(
    api_key="your-api-key",
    model="gpt-4o-mini"  # or any other compatible model
)

# Simple chat completion
messages = [
    ChatMessage(role="user", content="Hello, how are you?")
]
response = client.chat(messages)
print(response.text)

# Using function/tool calling
def calculator(a: int, b: int, operation: str) -> float:
    if operation == "add":
        return a + b
    elif operation == "multiply":
        return a * b
    # ... other operations

# Define the tool
calculator_tool = {
    "type": "function",
    "function": {
        "name": "calculator",
        "description": "Perform basic arithmetic operations",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "integer"},
                "b": {"type": "integer"},
                "operation": {
                    "type": "string",
                    "enum": ["add", "subtract", "multiply", "divide"]
                }
            },
            "required": ["a", "b", "operation"]
        }
    }
}

# Initialize client with tool
client_with_tools = VinehooLLM(
    api_key="your-api-key",
    model="gpt-4o-mini",
    tools=[calculator_tool],
    tool_handlers={"calculator": calculator}
)
```

<a name="chinese"></a>
## 中文

### 项目概述
VinehooLLM 是一个用于与 OpenAI 兼容的语言模型进行交互的 Python 客户端库。它支持函数/工具调用等现代特性，设计简单易用，同时保持灵活性。

### 特性
- 支持 OpenAI 兼容的 API
- 支持函数/工具调用功能
- 使用 Pydantic 模型实现类型安全
- 自动处理函数执行
- 可自定义 API 端点
- 全面的错误处理

### 安装
```bash
pip install vinehoollm
```

### 发布到 PyPI
按照以下步骤将包发布到 PyPI：

1. 安装 build 和 twine：
```bash
pip install build twine
```

2. 更新 `setup.py` 或 `pyproject.toml` 中的版本号

3. 构建包：
```bash
python -m build
```

4. 上传到 PyPI：
```bash
# 测试版 PyPI（建议先测试）
python -m twine upload --repository testpypi dist/*

# 正式版 PyPI
python -m twine upload dist/*
```

### 快速开始
```python
from vinehoollm.client import VinehooLLM, ChatMessage

# 初始化客户端
client = VinehooLLM(
    api_key="你的API密钥",
    model="gpt-4o-mini"  # 或其他兼容的模型
)

# 简单的聊天完成
messages = [
    ChatMessage(role="user", content="你好，最近如何？")
]
response = client.chat(messages)
print(response.text)

# 使用函数/工具调用
def calculator(a: int, b: int, operation: str) -> float:
    if operation == "add":
        return a + b
    elif operation == "multiply":
        return a * b
    # ... 其他操作

# 定义工具
calculator_tool = {
    "type": "function",
    "function": {
        "name": "calculator",
        "description": "执行基本的算术运算",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "integer"},
                "b": {"type": "integer"},
                "operation": {
                    "type": "string",
                    "enum": ["add", "subtract", "multiply", "divide"]
                }
            },
            "required": ["a", "b", "operation"]
        }
    }
}

# 使用工具初始化客户端
client_with_tools = VinehooLLM(
    api_key="你的API密钥",
    model="gpt-4o-mini",
    tools=[calculator_tool],
    tool_handlers={"calculator": calculator}
)
```