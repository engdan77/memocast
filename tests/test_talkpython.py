import pytest
import requests

from memocast.parsers.talkpython import TalkPythonToMeParser


@pytest.mark.parametrize(
    "episode_url, expected_short_name, expected_episode_number, expected_linked_url, expected_link_count",
    [
        (
            "https://pca.st/episode/648d2a6b-ba67-48f0-9a77-177ef4d84fde",
            "TalkPython",
            410,
            "https://talkpython.fm/410",
            20,
        ),
    ],
)
def test_talkpython_episode(
    episode_url, expected_short_name, expected_episode_number, expected_linked_url, expected_link_count
):
    html = requests.get(episode_url).content.decode()
    parser = TalkPythonToMeParser(html)

    assert parser.get_podcast_short_name() == expected_short_name
    assert parser.get_current_episode_number() == expected_episode_number
    assert parser.get_linked_url_podcast_source(expected_episode_number) == expected_linked_url

    links = parser.parse()
    assert len(links) == expected_link_count, "Wrong number of URL retrieved"
    assert all(link.url.startswith(("http", "mailto")) for link in links), "One of the URL not being valid"
