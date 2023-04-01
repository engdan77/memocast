import logging

import requests.exceptions

import __info__ as info
import io_
import clipboard_
import parser_
from logging_ import logger
from ui_ import view_factory


def parse_clipboard_url():
    url = clipboard_.get_clipboard_instance().get()
    logger.debug(f'Parsing {url}')
    html = io_.download_html(url)
    logger.debug(f'Downloaded HTML {len(html)} bytes')
    try:
        links = parser_.PodcastParser(html).try_all()
    except requests.exceptions.RequestException as e:
        logger.error(f'Error downloading source (forgot copy URL?): {e.args}')
    logger.info(f'Found following links {links}')
    podcast_view = view_factory()
    podcast_view().show()


def main():
    logger.info(f'Starting {info.__pkg__} {info.__version__}')
    device = io_.get_device_and_import_modules()
    logger.info(f'Identified {device} device')
    parse_clipboard_url()


if __name__ == '__main__':
    main()
