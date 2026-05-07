import sys
import logging


def get_logger() -> logging.Logger:
    logger = logging.Logger(__name__, level=logging.INFO)
    formatter = logging.Formatter(
        fmt="[%(asctime)s | %(levelname)s]: %(message)s"
    )  # fmt: skip
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


log = get_logger()
