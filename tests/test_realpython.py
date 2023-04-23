from collections import namedtuple

import pytest
import requests
from memocast.parsers.realpython import RealPythonParser

from memocast.parsers.talkpython import TalkPythonToMeParser

test_case = namedtuple("test_case", "expected_count_links episode_number url")

test_params = (
    test_case(
        11,
        153,
        "https://podcasts.google.com/feed/aHR0cHM6Ly9yZWFscHl0aG9uLmNvbS9wb2RjYXN0cy9ycHAvZmVlZA/episode/YWU3MDAxNjgtNjQ5MC00YzZkLWJjNTMtOWVlMzNmMWI2YmI4?sa=X&ved=0CAUQkfYCahcKEwi45-Cslr3-AhUAAAAAHQAAAAAQPw",
    ),
    test_case(
        16,
        148,
        "https://podcasts.google.com/feed/aHR0cHM6Ly9yZWFscHl0aG9uLmNvbS9wb2RjYXN0cy9ycHAvZmVlZA/episode/NTBmZjQzZjItMTMzZC00NzE2LWIyYTgtOGFlYjQ0Y2JhMGFl?sa=X&ved=0CAUQkfYCahcKEwi45-Cslr3-AhUAAAAAHQAAAAAQPw",
    ),
)


@pytest.fixture(params=test_params)
def input_data(request):
    d = request.param
    html = requests.get(d.url).content
    return RealPythonParser(html.decode()), d.episode_number, d.expected_count_links


@pytest.fixture
def linked_url(input_data, episode_number):
    parser, *_ = input_data
    return parser.get_linked_url_podcast_source(episode_number)


def test_get_podcast_short_name(input_data):
    parser, *_ = input_data
    short_name = parser.get_podcast_short_name()
    assert short_name == "RealPython"


@pytest.mark.parametrize(
    "arg",
    [
        pytest.lazy_fixture("input_data"),
    ],
)
def test_parse(arg):
    parser, expected_episode_number, expected_count = arg
    links = parser.parse()
    assert len(links) == expected_count, "Wrong number of URL retrieved"
    assert all(
        link.url.startswith(("http", "mailto")) for link in links
    ), "One of the URL not being valid"
    assert (
        parser.get_current_episode_number() == expected_episode_number
    ), "Wrong episode number"
    assert parser.base_url == f"https://realpython.com/podcasts/rpp", "Wrong base URL"
