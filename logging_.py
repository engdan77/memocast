import logging
from __info__ import __pkg__


def get_logger():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')
    logger = logging.getLogger(__pkg__)
    return logger
