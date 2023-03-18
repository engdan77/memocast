from typing import Iterable
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

    def parse(self) -> Iterable[Url]:
        """Parse and return iterable Urls"""
        logger.info('Start parsing')
        bs = BeautifulSoup(self.html, 'html.parser')
        x.find('div', class_='wv3SK')
        return [Url('foo', 'bar')]


class TalkPythonToMeParser(PodcastParser):

    def parse(self) -> Iterable[Url]:
        """Parse and return iterable Urls"""
        ...
