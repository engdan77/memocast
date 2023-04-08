import pytest
import requests
from podparse.parsers.realpython import RealPythonParser


@pytest.fixture
def parser():
    html = requests.get('https://podcasts.google.com/feed/aHR0cHM6Ly9yZWFscHl0aG9uLmNvbS9wb2RjYXN0cy9ycHAvZmVlZA/episode/NThjYTJiMjUtYjFjMS00YTBkLTgwMjYtOTc5YzlhZDA5Yjlh?sa=X&ved=0CAUQkfYCahgKEwigz5KCwJX-AhUAAAAAHQAAAAAQngg').content
    return RealPythonParser(html.decode())


@pytest.fixture
def episode_number(parser):
    return parser.get_current_episode_number()


@pytest.fixture
def linked_url(parser, episode_number):
    return parser.get_linked_url_podcast_source(episode_number)


def test_get_podcast_short_name(parser):
    short_name = parser.get_podcast_short_name()
    assert short_name == 'RealPython'


def test_get_current_episode_number(episode_number):
    assert episode_number == 152


def test_get_linked_url_podcast_source(linked_url):
    assert linked_url == 'https://realpython.com/podcasts/rpp/152'


def test_parse(parser):
    links = parser.parse()
    assert len(links) == 17, 'Wrong number of URL retrieved'
    assert all(link.url.startswith(('http', 'mailto')) for link in links), "One of the URL not being valid"

