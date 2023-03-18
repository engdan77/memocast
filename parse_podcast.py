import __info__ as info
from clipboard_ import prepare_device
from logging_ import get_logger

logger = get_logger()


def main():
    logger.info(f'Starting {info.__pkg__} {info.__version__}')
    device = prepare_device()
    logger.info(f'Using {device}')


