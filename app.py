import requests.exceptions
import podparse as info
from podparse import io_
from podparse import clipboard_
import podparse.parsers.baseclass
from podparse.logging_ import logger
from podparse.shareios import get_share_url_from_ios
from podparse.ui_ import view_factory
from podparse.io_ import get_device_and_import_modules
from podparse.protocols import DeviceType


def parse_clipboard_url():
    """Function for parsing the clipboard URL"""
    url = get_share_url_from_ios()
    if not url:
        url = clipboard_.get_clipboard_instance().get_and_verify()
    logger.debug(f'Parsing {url}')
    html = io_.download_html(url)
    logger.debug(f'Downloaded HTML {len(html)} bytes')
    try:
        urls = podparse.parsers.baseclass.BasePodcastParser(html).try_all()
    except requests.exceptions.RequestException as e:
        logger.error(f'Error downloading source (forgot copy URL?): {e.args}')
        return
    assert get_device_and_import_modules() == DeviceType.ios, 'This is not an IOS device, exiting'
    podcast_view = view_factory()
    podcast_view().show(urls)


def main():
    logger.info(f'Starting {info.__pkg__} {info.__version__}')
    device = io_.get_device_and_import_modules()
    logger.info(f'Identified {device} device')
    try:
        parse_clipboard_url()
    except requests.exceptions.RequestException as e:
        logger.error(f'Unable to parse URL: {e.args}')

if __name__ == '__main__':
    main()
