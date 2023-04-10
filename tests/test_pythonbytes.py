import pytest
import requests
from memocast.parsers.pythonbytes import PythonBytesParser


@pytest.fixture
def parser():
    html = requests.get('https://podcasts.google.com/feed/aHR0cHM6Ly9weXRob25ieXRlcy5mbS9lcGlzb2Rlcy9yc3M/episode/NTI2OTQ0YjEtNDhjZS00OTllLWE3YTAtZThiZWU2MzdlMTMy?sa=X&ved=0CAUQkfYCahcKEwigz5KCwJX-AhUAAAAAHQAAAAAQAQ').content
    return PythonBytesParser(html.decode())


@pytest.fixture
def episode_number(parser):
    return parser.get_current_episode_number()


@pytest.fixture
def linked_url(parser, episode_number):
    return parser.get_linked_url_podcast_source(episode_number)


def test_get_podcast_short_name(parser):
    short_name = parser.get_podcast_short_name()
    assert short_name == 'PythonBytes'


def test_get_current_episode_number(episode_number):
    assert episode_number == 329


def test_get_linked_url_podcast_source(linked_url):
    assert linked_url == 'https://pythonbytes.fm/329'


def test_parse(parser):
    links = parser.parse()
    assert len(links) == 24, 'Wrong number of URL retrieved'
    assert all(link.url.startswith(('http', 'mailto')) for link in links), "One of the URL not being valid"

