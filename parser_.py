from typing import Iterable

import io_
from dataclasses import dataclass
from abc import abstractmethod
from bs4 import BeautifulSoup
from logging_ import logger


class PodcastParser:
    def __init__(self, input_html: str):
        """Take HTML as input"""
        self.podcast_html = input_html
        self.title = None

    def try_all(self):
        links = []
        for subparserclass in self.__class__.__subclasses__():
            try:
                subparser_urls = subparserclass(self.podcast_html).parse()
            except AttributeError as e:
                logger.warning(f'{subparserclass.__name__} unable to parse, needs to be Google Pod: {e.args}')
                continue
            links.extend(subparser_urls)
        logger.debug(links)

    @abstractmethod
    def parse(self) -> Iterable[Url]:
        """Parse and return iterable Urls"""
        ...

    @abstractmethod
    def get_linked_url_podcast_source(self, episode_number) -> str:
        """Get source URL based on episode in podcast page"""
        ...

    @abstractmethod
    def get_current_episode_number(self) -> int:
        """Get episode number from html"""
        ...



class TalkPythonToMeParser(PodcastParser):
    base_url = 'http://talkpython.fm'

    def parse(self) -> Iterable[Url]:
        """Parse and return iterable Urls"""
        logger.info('Start parsing')
        episode_number = self.get_current_episode_number()
        episode_url = self.get_linked_url_podcast_source(episode_number)
        episode_source_html = io_.download_html(episode_url)
        urls = self.get_all_urls_from_podcast_html(episode_source_html)
        return urls

    def get_urls_from_html(self) -> Iterable[Url]:
        """Get URLS from page"""
        return []

    def get_linked_url_podcast_source(self, episode_number) -> str:
        """Get source URL based on episode in podcast page"""
        return f'{self.__class__.base_url}/{episode_number}'

    def get_current_episode_number(self) -> int:
        """Get episode number from html"""
        bs = BeautifulSoup(self.podcast_html, 'html.parser')
        self.title = bs.find('div', class_='wv3SK').text
        return int(self.title.split(':')[0].strip('#'))

    def get_all_urls_from_podcast_html(self, episode_source_html: str):
        bs = BeautifulSoup(episode_source_html, 'html.parser')
        urls = []
        for bold_item in bs.find_all('b'):
            logger.debug(f'Parsing {bold_item}')
            description = bold_item.text
            try:
                url = bold_item.nextSibling.nextSibling.get('href')
            except AttributeError:
                logger.debug('Skipping to next ')
            else:
                urls.append(Url(url, description, self))
        return urls


@dataclass
class Url:
    url: str
    description: str
    parser: PodcastParser
