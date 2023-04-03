from typing import Iterable
import io_
from abc import abstractmethod
from bs4 import BeautifulSoup
from logging_ import logger
import protocols


class PodcastParser:

    def __init__(self, input_html: str):
        """Take HTML as input"""
        self.podcast_html = input_html
        self.title = None
        self.episode_number = None

    def try_all(self):
        links = []
        for subparserclass in self.__class__.__subclasses__():
            try:
                subparser_urls = subparserclass(self.podcast_html).parse()
            except AttributeError as e:
                logger.warning(f'{subparserclass.__name__} unable to parse, needs to be Google Pod: {e.args}')
                continue
            links.extend(subparser_urls)
        return links

    def __repr__(self):
        return f'{self.__class__.__name__}'

    @abstractmethod
    def parse(self) -> Iterable[protocols.Url]:
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

    @abstractmethod
    def get_podcast_short_name(self) -> str:
        """Return the a short name of the podcast"""
        ...


class TalkPythonToMeParser(PodcastParser):
    base_url = 'http://talkpython.fm'

    def get_podcast_short_name(self) -> str:
        return "TalkPython"

    def parse(self) -> Iterable[protocols.Url]:
        """Parse and return iterable Urls"""
        logger.info('Start parsing')
        episode_number = self.get_current_episode_number()
        episode_url = self.get_linked_url_podcast_source(episode_number)
        episode_source_html = io_.download_html(episode_url)
        urls = self.get_all_urls_from_podcast_html(episode_source_html)
        return urls

    def get_urls_from_html(self) -> Iterable[protocols.Url]:
        """Get URLS from page"""
        return []

    def get_linked_url_podcast_source(self, episode_number) -> str:
        """Get source URL based on episode in podcast page"""
        return f'{self.__class__.base_url}/{episode_number}'

    def get_current_episode_number(self) -> int:
        """Get episode number from html"""
        if self.episode_number:
            return self.episode_number
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
                urls.append(protocols.Url(url, description, self))
        return urls
