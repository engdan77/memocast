import re
from typing import Iterable, Optional
from .. import io_
from bs4 import BeautifulSoup
from memocast.logging_ import logger
from .. import protocols

from .baseclass import BasePodcastParser


class RealPythonParser(BasePodcastParser):
    base_url = 'https://realpython.com/podcasts/rpp'

    @staticmethod
    def get_podcast_short_name() -> str:
        return "RealPython"

    def parse(self) -> Iterable[protocols.Url]:
        """Parse and return iterable Urls"""
        logger.info('Start parsing')
        episode_number = self.get_current_episode_number()
        episode_url = self.get_linked_url_podcast_source(episode_number)
        episode_source_html = io_.download_html(episode_url)
        urls = self.get_all_urls_from_podcast_html(episode_source_html)
        return urls

    def get_linked_url_podcast_source(self, episode_number) -> str:
        """Get source URL based on episode in podcast page"""
        return f'{self.__class__.base_url}/{episode_number}'

    def get_current_episode_number(self) -> int:
        """Get episode number from html"""
        if self.episode_number:
            return self.episode_number
        bs = BeautifulSoup(self.podcast_html, 'html.parser')
        episode_number = re.match('.+_E(\d+)_.*', bs.find('a', class_='download-button').attrs['href']).group(1)
        title = bs.find('div', class_='section').find('h1').text.strip('#\n ')
        self.title = f'#{episode_number} {title}'
        return int(episode_number)

    def get_episode_number_amongst_all(self, description: str) -> Optional[int]:
        html = io_.download_html(self.base_url)
        bs = BeautifulSoup(html, 'html.parser')
        episode_number = None
        for e in bs.find_all('a'):
            if description in e.text:
                _, episode_number = e.text.split(':')[0].split()
        return int(episode_number)

    def get_all_urls_from_podcast_html(self, episode_source_html: str):
        bs = BeautifulSoup(episode_source_html, 'html.parser')
        urls = []
        for subject in ('Show Links:', 'Projects:', 'Additional Links:'):
            if not bs.find("p", string=subject):
                continue
            for link in bs.find("p", string=subject).fetchNextSiblings('ul')[0].find_all('a'):
                logger.debug(f'Found URL item {link}')
                description = link.text
                url = link.get('href')
                urls.append(protocols.Url(url, description, self))
        return urls
