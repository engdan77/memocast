from abc import abstractmethod
from typing import Iterable
from memocast import protocols
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
            class_shortname = subparserclass.get_podcast_short_name()
            logger.debug(f'Attempt use of {class_shortname} parser')
            try:
                subparser_urls = subparserclass(self.podcast_html).parse()
            except AttributeError as e:
                logger.warning(f'{subparserclass.__name__} unable to parse, needs to be Pocket Casts: {e.args}')
                continue
            except (ValueError, TypeError) as e:
                logger.warning(f'Unable to parse using {class_shortname}: {e.args}, SKIP TO NEXT PARSER')
                continue
            logger.debug(f'Found {len(list(subparser_urls))} links')
            links.extend(subparser_urls)
        links = [_ for _ in links if _.description]  # Removes unwanted blank descriptions
        logger.debug(f'Found total {len(links)} using {class_shortname}')
        return links

    def __repr__(self):
        return f'{self.__class__.__name__}'

    @abstractmethod
    def parse(self) -> Iterable[protocols.Url]:
        """Parse and return iterable Urls"""
        ...

    @abstractmethod
    def get_current_episode_number(self) -> int:
        """Get episode number from html"""
        ...

    @staticmethod
    @abstractmethod
    def get_podcast_short_name() -> str:
        """Return the short name of the podcast"""
        ...
