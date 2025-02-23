import os
import sys
from contextlib import contextmanager

from .__init__ import *

__all__ = ["noPrint"]


@contextmanager
def ContextManagersNoPrint():
    _original_stdout = sys.stdout
    sys.stdout = open(os.devnull, "w")

    yield _original_stdout

    sys.stdout.close()
    sys.stdout = _original_stdout


def noPrint(func: Callable):
    @functools.wraps(func)  # 保留原函數的元數據
    def wrapper(*args, **kwargs):
        with ContextManagersNoPrint():  # 使用上下文管理器禁用打印
            return func(*args, **kwargs)

    return wrapper
