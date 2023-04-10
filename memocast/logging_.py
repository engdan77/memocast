import logging
from memocast import __pkg__
import builtins

class Logger(object):
    _logger = None

    def __new__(cls):
        """Create a singletone"""
        if not cls._logger:
            cls._logger = super().__new__(cls)
            logging.basicConfig(level=logging.DEBUG, format='>>> %(message)s\n')
            cls._logger = logging.getLogger(__pkg__)
        return cls._logger

    @classmethod
    def set_level(cls, loglevel='DEBUG'):
        cls._logger.setLevel(getattr(logging, loglevel))


logger = Logger()