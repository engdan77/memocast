import pytest
import requests
from collections import namedtuple

from memocast.parsers.talkpython import TalkPythonToMeParser


@pytest.fixture
def parser():
    html = requests.get('https://pca.st/episode/648d2a6b-ba67-48f0-9a77-177ef4d84fde').content
    return TalkPythonToMeParser(html.decode())


@pytest.fixture
def episode_number(parser):
    return parser.get_current_episode_number()


@pytest.fixture
def linked_url(parser, episode_number):
    return parser.get_linked_url_podcast_source(episode_number)


def test_get_podcast_short_name(parser):
    short_name = parser.get_podcast_short_name()
    assert short_name == "TalkPython"


def test_get_current_episode_number(episode_number):
    assert episode_number == 410


def test_get_linked_url_podcast_source(linked_url):
    assert linked_url == "https://talkpython.fm/410"


def test_parse(parser):
    links = parser.parse()
    assert len(links) == 22, "Wrong number of URL retrieved"
    assert all(
        link.url.startswith(("http", "mailto")) for link in links
    ), "One of the URL not being valid"
