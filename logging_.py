import logging
from __info__ import __pkg__


class Logger(object):
    _logger = None

    def __new__(cls):
        """Create a singletone"""
        if not cls._logger:
            cls._logger = super().__new__(cls)
            logging.basicConfig(level=logging.DEBUG, format='%(asctime)s: %(message)s')
            cls._logger = logging.getLogger(__pkg__)
        return cls._logger


logger = Logger()