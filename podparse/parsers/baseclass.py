from abc import abstractmethod
from typing import Iterable
from podparse import protocols
from ..logging_ import logger


class BasePodcastParser:

    def __init__(self, input_html: str):
        """Take HTML as input"""
        self.podcast_html = input_html
        self.title = None
        self.episode_number = None

    def try_all(self):
        links = []
        for subparserclass in self.__class__.__subclasses__():
            logger.debug(f'Attempt {subparserclass.get_podcast_short_name()} parser')
            try:
                subparser_urls = subparserclass(self.podcast_html).parse()
            except AttributeError as e:
                logger.warning(f'{subparserclass.__name__} unable to parse, needs to be Google Pod: {e.args}')
                continue
            logger.debug(f'Found {len(subparser_urls)} links')
            links.extend(subparser_urls)
        logger.debug(f'Found total {len(links)}')
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
