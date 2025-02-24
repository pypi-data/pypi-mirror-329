# -*- coding: utf-8 -*-
# @time: 2022/4/21 16:50
# @author: Dyz
# @file: time.py
# @software: PyCharm
import asyncio
from functools import wraps
from pathlib import Path
from time import gmtime, strftime, time


def get_args_file(*args, **kwargs):
    """从传入参数中找寻file相关的参数"""
    for file in args:
        if isinstance(file, Path):
            return file
    for key, val in kwargs.items():
        if isinstance(val, Path):
            return val


def _timer(func, start_time, *args, **kwargs):
    """计时与打印"""
    time_ = strftime("%H:%M:%S", gmtime(time() - start_time))
    if 'download' in str(func.__name__):
        file = get_args_file(*args, **kwargs)
        print(f'{file or str(func.__name__)} 耗时: {time_}')
    else:
        print(f'{func.__name__} 耗时: {time_}')


def timer(func):
    """ 计算时间装饰器 """
    if asyncio.iscoroutinefunction(func):
        # 用于装饰异步函数
        @wraps(func)
        async def aio_wrapper(*args, **kwargs):
            start_time = time()
            res = await func(*args, **kwargs)
            _timer(func, start_time, *args, **kwargs)
            return res

        return aio_wrapper

    else:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time()
            res = func(*args, **kwargs)
            _timer(func, start_time, *args, **kwargs)
            return res

        return wrapper
