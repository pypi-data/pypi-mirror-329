# -*- coding:utf-8 -*-
"""
@Created on : 2024/10/8 23:01
@Author: XDTEAM
@Des: 异步请求重试机制
"""
import asyncio
import httpx
from typing import Callable, Generic, TypeVar, Awaitable, Optional

R = TypeVar('R')


class StateManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(StateManager, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        if not self.__initialized:
            self.__initialized = True

    async def update_key(self, current_params):
        #  TODO: 自己实现的关于更新参数的逻辑
        ...


class RequestResult(Generic[R]):
    """
    用来封装请求结果及其尝试次数。

    :param result: 请求的结果数据。
    :param attempts: 请求尝试的次数。
    """

    def __init__(self, result: Optional[R], attempts: int):
        self.result = result  # 请求结果
        self.attempts = attempts  # 尝试次数


class Retrier(Generic[R]):
    """
    用来管理重试逻辑。
    """

    def __init__(self, func: Callable[..., Awaitable[R]], max_attempts: int = 30, retry_delay: float = 1.0,
                 should_retry=None, update_handle=None, update_func=None):
        """
        用于包装需要重试的异步函数的装饰器。

        :param max_attempts: 最大重试次数，默认为30次。
        :param retry_delay: 每次重试之间的延迟时间，默认为1秒。
        :param should_retry: 用户定义的回调函数，用于决定是否需要重试。
        :param update_handle: 用户定义的回调函数，用于决定是否需要更新请求参数。
        :param update_func: 用户定义的异步回调函数，用于更新请求参数。
        """
        self.func = func
        self.max_attempts = max_attempts
        self.retry_delay = retry_delay
        self.attempts = 0
        self.should_retry = should_retry or (lambda response: response.status_code != 200)
        self.update_handle = update_handle or (lambda response: response.status_code == 422)
        self.update_func = update_func

    async def retry(self, **kwargs) -> RequestResult[R]:
        """
        执行请求，并根据重试条件决定是否继续重试。
        """
        while self.attempts < self.max_attempts:
            self.attempts += 1
            try:
                # 调用被装饰的函数并传递参数
                response = await self.func(**kwargs)

                # 如果需要更新参数，则执行更新操作
                if self.update_handle(response):
                    if self.update_func:
                        kwargs = await self.update_func(kwargs)

                # 检查是否需要重试
                if not self.should_retry(response):
                    # 如果不需要重试，则返回请求结果
                    return RequestResult(response.json(), self.attempts)

                # 等待指定的时间后重试
                await asyncio.sleep(self.retry_delay)

            except httpx.RequestError as e:
                print(f"An error occurred during request: {e}")
                if self.should_retry(e):
                    await asyncio.sleep(self.retry_delay)
                else:
                    break

        # 达到最大重试次数，返回None
        return RequestResult(None, self.attempts)


def retry_on_condition(max_attempts: int = 30, retry_delay: float = 1.0, should_retry=None, update_handle=None,
                       update_func=None):
    """
    用于包装需要重试的异步函数的装饰器。
    """

    def decorator(func: Callable[..., Awaitable[httpx.Response]]) -> Callable[..., Awaitable[RequestResult[R]]]:
        async def wrapper(**kwargs) -> RequestResult[R]:
            """
            实际的包装函数，负责启动重试逻辑，并返回结果。
            """
            retrier = Retrier(func, max_attempts=max_attempts, retry_delay=retry_delay, should_retry=should_retry,
                              update_handle=update_handle, update_func=update_func)
            return await retrier.retry(**kwargs)

        return wrapper

    return decorator