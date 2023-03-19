from typing import Iterable

import io_
from dataclasses import dataclass
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from logging_ import logger


@dataclass
class Url:
    url: str
    description: str


class PodcastParser(ABC):
    def __init__(self, input_html: str):
        """Take HTML as input"""
        self.podcast_html = input_html
        self.title = None

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
        bs = BeautifulSoup(self.podcast_html, 'html.parser')
        episode_number = self.get_current_episode_number()
        episode_url = self.get_linked_url_podcast_source(episode_number)
        episode_source_html = io_.download_html(episode_url)
        return [Url('foo', 'bar')]

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


