from time import perf_counter
from typing import Any

from ..I18n import I18n
from .__init__ import Callable, functools, logger

i18n_obj = I18n(
    langJson={
        "en_us": {
            "file_lang": "en_us",
            "updata": "2024/09/25 17:56 UTC+0800",
            "getTime__Decorator__getTime__log": '"{}()" Execution time is {} seconds',
        },
        "zh_hk": {
            "file_lang": "zh_hk",
            "updata": "2024/09/25 18:12 UTC+0800",
            "getTime__Decorator__getTime__log": '"{}()" \u57f7\u884c\u6642\u9593\u70ba{} \u79d2',
        },
    }
)


def getTime(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time: float = perf_counter()
        result: Any = func(*args, **kwargs)
        end_time: float = perf_counter()

        logger.info(
            i18n_obj.locale(
                "getTime__Decorator__getTime__log",
                func.__name__,
                f"{end_time - start_time: .3f}",
            )
        )
        return result

    return wrapper
