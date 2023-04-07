import pytest
import requests
from podparse.parsers.talkpython import TalkPythonToMeParser


@pytest.fixture
def parser():
    html = requests.get('https://podcasts.google.com/feed/aHR0cHM6Ly90YWxrcHl0aG9uLmZtL2VwaXNvZGVzL3Jzcw/episode/MjkxNDM0NjktYjQzZC00Mjk4LWFjNTMtZjhmMWE3OTIxMzdk?sa=X&ved=0CAwQz4EHahcKEwiQh9C4k5f-AhUAAAAAHQAAAAAQCg').content
    return TalkPythonToMeParser(html.decode())


@pytest.fixture
def episode_number(parser):
    return parser.get_current_episode_number()


@pytest.fixture
def linked_url(parser, episode_number):
    return parser.get_linked_url_podcast_source(episode_number)


def test_get_podcast_short_name(parser):
    short_name = parser.get_podcast_short_name()
    assert short_name == 'TalkPython'


def test_get_current_episode_number(episode_number):
    assert episode_number == 410


def test_get_linked_url_podcast_source(linked_url):
    assert linked_url == 'https://talkpython.fm/410'


def test_parse(parser):
    links = parser.parse()
    assert len(links) == 17, 'Wrong number of URL retrieved'
    assert all(link.url.startswith(('http', 'mailto')) for link in links), "One of the URL not being valid"

