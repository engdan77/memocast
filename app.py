from typing import List

import requests.exceptions
import memocast as info
from memocast import io_
from memocast import clipboard_
import memocast.parsers  # This to import all parsers as subclassed (allow those as plugins)
import memocast.parsers.baseclass
from memocast.logging_ import logger
from memocast.shareios import get_share_url_from_ios
from memocast.ui_ import view_factory
from memocast.io_ import get_device_and_import_modules
from memocast.protocols import DeviceType, Url

logger.setLevel("DEBUG")


def process_podcast():
    """Function for parsing the clipboard URL"""
    html = get_html_source()
    links = get_links(html)
    parsers_matching = get_duplicate_matched_parsers(links)
    logger.debug(f"Duplicate parsers: {parsers_matching}")
    assert (
        get_device_and_import_modules() == DeviceType.ios
    ), "This is not an IOS device, exiting"
    podcast_view = (
        view_factory()
    )  # Could potentially be extended in future for other that IOS
    pv = podcast_view()
    if len(parsers_matching) > 1:
        logger.warning(
            f"Found more than one parser, ask for which to use: {parsers_matching}"
        )
        correct_parser = pv.get_option(parsers_matching, "What parser to use?")
        logger.info(f"Selecting {correct_parser}")
        links = filter_parser(links, correct_parser)
    pv.show(links)


def filter_parser(links: List[Url], parser_name: str) -> List[Url]:
    """Based on filter name return new list of links"""
    return [_ for _ in links if _.parser.get_podcast_short_name() == parser_name]


def get_duplicate_matched_parsers(links: List[Url]):
    """Return names of parses that is found duplicate, to give option to select one"""
    return list({_.parser.get_podcast_short_name() for _ in links})


def get_links(html: str):
    """Main function to try all parsers on the HTML as argument"""
    try:
        links = memocast.parsers.baseclass.BasePodcastParser(html).try_all()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error downloading source (forgot copy URL?): {e.args}")
        raise SystemExit()
    return links


def get_html_source() -> str:
    """Get the HTML source based on URL from share or clipboard"""
    source_url = None
    try:
        source_url = get_share_url_from_ios()
    except ModuleNotFoundError:
        logger.info("Unable to get URL from share in IOS, using clipboard instead")
    if not source_url:
        source_url = clipboard_.get_clipboard_instance().get_and_verify()
    else:
        logger.info("Got URL from share in IOS")
    logger.debug(f"Parsing {source_url}")
    html = io_.download_html(source_url)
    logger.debug(f"Downloaded HTML {len(html)} bytes")
    return html


def main():
    logger.info(f"Starting {info.__pkg__} {info.__version__}")
    device = io_.get_device_and_import_modules()
    logger.info(f"Identified {device} device")
    try:
        process_podcast()
    except requests.exceptions.RequestException as e:
        logger.error(f"Unable to parse URL: {e.args}")


if __name__ == "__main__":
    main()
