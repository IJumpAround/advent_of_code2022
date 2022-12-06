import logging
import os
from pathlib import Path


def aoc_root() -> Path:
    return Path(__file__).parent.absolute()


logger = logging.getLogger(__name__)

level = os.environ.get('LOG_LEVEL') or logging.DEBUG
logger.setLevel(level)
handler = logging.StreamHandler()
handler.setLevel(level)
fmt = "%(levelname)s:%(name)s %(lineno)d: %(message)s"
handler.setFormatter(logging.Formatter(fmt))
logger.addHandler(handler)
