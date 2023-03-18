from typing import Iterable

import io_
from dataclasses import dataclass
from abc import ABC
from bs4 import BeautifulSoup
from logging_ import logger


@dataclass
class Url:
    url: str
    description: str


class PodcastParser(ABC):
    def __init__(self, input_html: str):
        """Take HTML as input"""
        self.html = input_html
        self.title = None

    def parse(self) -> Iterable[Url]:
        """Parse and return iterable Urls"""
        ...

    def get_linked_podcast_source(self):
        """Get source URL based on episode in podcast page"""


class TalkPythonToMeParser(PodcastParser):

    def parse(self) -> Iterable[Url]:
        """Parse and return iterable Urls"""
        logger.info('Start parsing')
        bs = BeautifulSoup(self.html, 'html.parser')
        episode_number = self.get_episode_number()
        episode_url = self.get_linked_url_podcast_source(episode_number)
        episode_source_html = io_.download_html(episode_url)
        return [Url('foo', 'bar')]

    def get_urls_from_html(self) -> Iterable[Url]:
        """Get URLS from page"""
        return []

    def get_linked_url_podcast_source(self, episode_number) -> str:
        """Get source URL based on episode in podcast page"""
        return f'http://talkpython.fm/{episode_number}'

    def get_episode_number(self):
        """Get episode number from html"""
        bs = BeautifulSoup(self.html, 'html.parser')
        self.title = bs.find('div', class_='wv3SK').text
        return self.title.split(':')[0].strip('#')


