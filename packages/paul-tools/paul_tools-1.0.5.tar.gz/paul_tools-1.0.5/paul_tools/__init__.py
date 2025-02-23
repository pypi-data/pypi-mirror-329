__version__ = "1.0.0"


def logger_init(DEBUG: bool = False):
    from sys import stdout

    from loguru import logger

    logger.remove()
    logger.add(
        stdout, level=("DEBUG" if DEBUG else "INFO"), format="<level>{message}</level>"
    )
    return logger


logger = logger_init()
