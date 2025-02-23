from time import sleep
from typing import Any

from ..I18n import I18n
from ..Tools import color, typeToColor
from .__init__ import *

__all__ = ["retry"]

i18n_obj = I18n(
    langJson={
        "en_us": {
            "file_lang": "en_us",
            "updata": "2024/09/25 17:56 UTC+0800",
            "retry__Decorator__retry__ValueErrorText": "retries not < 1 or delay not <= 0",
            "retry__Decorator__retry__run": "run({}): {}()",
            "retry__Decorator__retry__errFail": 'Error: {},"{}()"Failed after {} retries.',
            "retry__Decorator__retry__err": "Error: {} -> Retrying...",
        },
        "zh_hk": {
            "file_lang": "zh_hk",
            "updata": "2024/09/25 18:12 UTC+0800",
            "retry__Decorator__retry__ValueErrorText": "重試次數不 < 1 或延遲不 <= 0",
            "retry__Decorator__retry__run": "\u904b\u884c({}): {}()",
            "retry__Decorator__retry__errFail": '\u932f\u8aa4\uff1a{},"{}()"\u91cd\u8a66 {} \u6b21\u5f8c\u5931\u6557\u3002',
            "retry__Decorator__retry__err": "\u932f\u8aa4\uff1a{} -> \u6b63\u5728\u91cd\u8a66({})...",
        },
    }
)


def retry(retries: int = 3, delay: float = 1) -> Callable:
    if retries < 1 or delay <= 0:
        raise ValueError(i18n_obj.locale("retry__Decorator__retry__ValueErrorText"))

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            for i in range(1, retries + 1):
                try:
                    logger.info(
                        i18n_obj.locale(
                            "retry__Decorator__retry__run", i, func.__name__
                        )
                    )
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == retries:
                        logger.warning(
                            *color(
                                i18n_obj.locale(
                                    "retry__Decorator__retry__errFail",
                                    repr(e),
                                    func.__name__,
                                    retries,
                                ),
                                color=typeToColor("err"),
                            )
                        )
                        raise e
                    else:
                        logger.warning(
                            *color(
                                i18n_obj.locale(
                                    "retry__Decorator__retry__err", repr(e), i
                                ),
                                color=typeToColor("warn"),
                            )
                        )
                        sleep(delay)

        return wrapper

    return decorator
