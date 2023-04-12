from typing import Iterable
from .. import io_
from bs4 import BeautifulSoup
from memocast.logging_ import logger
from .. import protocols

from .baseclass import BasePodcastParser


class PythonBytesParser(BasePodcastParser):
    base_url = 'https://pythonbytes.fm'

    @staticmethod
    def get_podcast_short_name() -> str:
        return "PythonBytes"

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
        self.title = bs.find('div', class_='wv3SK').text
        return int(self.title.split(' ')[0].strip('#'))

    def get_all_urls_from_podcast_html(self, episode_source_html: str):
        bs = BeautifulSoup(episode_source_html, 'html.parser')
        urls = []
        for a in bs.find_all('a'):
            url = a.get('href')
            if url.startswith('/'):
                continue
            logger.debug(f'Found URL item {a}')
            try:
                description = a.text.strip('\n\t ')
            except AttributeError:
                logger.debug('Skipping to next ')
            else:
                urls.append(protocols.Url(url, description, self))
        return urls
