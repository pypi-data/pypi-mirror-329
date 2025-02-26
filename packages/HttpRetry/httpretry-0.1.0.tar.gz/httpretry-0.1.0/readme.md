# 使用说明 - 异步请求重试机制

## 简介

本项目提供了一个异步请求重试机制，旨在处理网络请求中的失败情况。通过使用装饰器，可以轻松地为异步函数添加重试逻辑，以确保在请求失败时能够自动重试，直到达到最大重试次数或成功为止。

## 主要组件

1. **StateManager**: 单例模式的状态管理器，用于管理请求的状态。
2. **RequestResult**: 封装请求结果及其尝试次数的类。
3. **Retrier**: 管理重试逻辑的类，负责执行请求并根据条件决定是否重试。
4. **retry_on_condition**: 装饰器，用于包装需要重试的异步函数。

## 安装依赖

在使用本项目之前，请确保安装了以下依赖库：

```bash
pip install httpx loguru
```

## 使用示例

### 1. 定义异步请求函数

首先，定义一个异步函数，该函数将执行实际的网络请求。例如：

```python
import httpx

async def fetch_data(url: str) -> httpx.Response:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()  # 如果响应状态码不是200，将引发异常
        return response
```

### 2. 使用装饰器添加重试逻辑

使用 `retry_on_condition` 装饰器来包装你的异步请求函数，以添加重试逻辑。例如：

```python
@retry_on_condition(max_attempts=5, retry_delay=2.0)
async def fetch_with_retry(url: str) -> RequestResult[httpx.Response]:
    return await fetch_data(url)
```

### 3. 调用函数并处理结果

调用带有重试逻辑的函数，并处理返回的结果：

```python
import asyncio

async def main():
    url = "https://api.example.com/data"
    result = await fetch_with_retry(url)

    if result.result is not None:
        print("请求成功:", result.result)
    else:
        print(f"请求失败，尝试次数: {result.attempts}")

if __name__ == "__main__":
    asyncio.run(main())
```

## 参数说明

### `retry_on_condition` 装饰器参数

- `max_attempts`: 最大重试次数，默认为30次。
