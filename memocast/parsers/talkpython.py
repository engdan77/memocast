import re
from typing import Iterable
from .. import io_
from bs4 import BeautifulSoup
from memocast.logging_ import logger
from .. import protocols

from .baseclass import BasePodcastParser


class TalkPythonToMeParser(BasePodcastParser):
    base_url = 'https://talkpython.fm'

    @staticmethod
    def get_podcast_short_name() -> str:
        return "TalkPython"

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
        episode_number = next((m.group(1) for s in bs.find_all('span') if (m := re.match(r'^E(\d+)', s.text))), None)
        assert episode_number is not None, "Unable to find episode number"
        title = bs.find('h1', {'id': 'dialog_title'}).text
        self.title = f'#{episode_number} {title}'
        return int(episode_number)

    def get_all_urls_from_podcast_html(self, episode_source_html: str):
        urls = []
        raw_urls = {}
        bs = BeautifulSoup(episode_source_html, 'html.parser')
        all_links = [a for a in (li.find_all('a') for li in bs.find_all('li')) if
                     not next(iter(a), {'href': '/'}).get('href').startswith('/')]
        for sub_links in all_links:
            for sub_link in sub_links:
                title = sub_link.text
                url = sub_link.get('href')
                raw_urls[title] = url
        for description, url in raw_urls.items():
            urls.append(protocols.Url(url, description, self))
        return urls
