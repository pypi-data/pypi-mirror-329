import sys
from functools import cache

import loguru

_logger = None


@cache
def get_singleton_logger():
    global _logger
    if _logger is None:
        # logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

        _logger = loguru.logger

        _logger.remove()
        _logger.add(sys.stdout, level="INFO")


    return _logger


logger = get_singleton_logger()
