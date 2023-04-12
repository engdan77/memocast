# Memocast

A small [iOS](https://en.wikipedia.org/wiki/IOS) application for e.g. iPhone that allow you to add links heard in podcasts into [reminders](https://en.wikipedia.org/wiki/Reminders_(Apple)).

## Motivation

Imagine that you just as I often do listening to a podcast such as [PythonBytes](https://podcasts.google.com/feed/aHR0cHM6Ly9weXRob25ieXRlcy5mbS9lcGlzb2Rlcy9yc3M/episode/NTI2OTQ0YjEtNDhjZS00OTllLWE3YTAtZThiZWU2MzdlMTMy?sa=X&ved=0CAwQz4EHahcKEwjgm5v-qov-AhUAAAAAHQAAAAAQCg) (a fantastic one) using [Google Podcast](https://podcasts.google.com/) while out walking and hear a talk about an interesting project or article you wish to read more about when time allow.
Thankfully the referenced links are added to the show notes of the talk, but it means you would need to look it up and add this into your own notes.

Wouldn't be nice if there was an easier way select which of those you found interesting and have them added to reminders on your phone while you'd still out walking without the need to lose too much focus on where you put your feets..?

... if you do recognise the same, then this small application might be what you're looking for.



## How does it work?





## Requirements and installation

To allow Python to run within your device you will need to first to install [Pythonista 3](https://apps.apple.com/us/app/pythonista-3/id1085978097) from app store that by the time writing this costs $9.99 which to my opinion is a very small price for such useful addition to your device.

Either click on this link or aim your camera at the below QR-code to have it downloaded to your device.



## How to develop additional podcast parser

All that is needed need to do is to create a new python file within the parsers package...

```
📦 memocast-project
┣ 📂 memocast
┃ ┣ 📜 ...
┃ ┗ 📂 parsers
┃   ┣ 📜 __init__.py
┃   ┣ 📜 baseclass.py
┃   ┣ 📜 pythonbytes.py
┃   ┗ 📜 otherpodcast.py  ✨🆕
```

... let's pretend we wish to add a new one named `otherpodcast.py` and within this we assure we create a new class and inherit from `BasePodCastParser` that will allow the application to dynamically use this new one as a plugin.

```python
# memocast/parsers/otherpodcast.py

from typing import Iterable
from bs4 import BeautifulSoup  # Most likely to be used for parsing HTML
from memocast.logging_ import logger  # Logging singleton
from .. import io_  # Module with e.g. convinient download_html(episode_url)
from .. import protocols  # Includes dataclass Url
from .baseclass import BasePodcastParser  # Inherit from this baseclass


class OtherParser(BasePodcastParser):
  	# This is the URL of which this podcast has its links available
    base_url = 'https://.....'  

    @staticmethod
    def get_podcast_short_name() -> str:
        return "OtherPodCast"  # This is used as part of the links shown in Reminders

   def get_current_episode_number(self) -> int:
    # This should return the episode number from Google Podcasts URL
    example_episode_number = 134
    return example_episodr_number
      
    def parse(self) -> Iterable[protocols.Url]:
      # This is the main method to do the work
      episode_source_html = io_.download('https://....')  # Example
      bs = BeautifulSoup(episode_source_html, 'html.parser')
        urls = [
          protocols.Url(url='http://foo.com', 'Project Foo', self)
          protocols.Url(url='http://bar.com', 'Project Bar', self)
        ]  # Obviously this should be dynamically created by your code
        return urls  # Return a list of URLs
```

By adding this module it will work as a plugin and allow the application to use this to attempt parsing.



## Software design

Essentially ...



### Class diagram for parsers

```mermaid
classDiagram
    BasePodcastParser <|-- PythonBytesParser
    BasePodcastParser <|-- OtherParser

class BasePodcastParser {
    <<abstract>>
    +try_all()
    }

class PythonBytesParser {
    + base_url
    + parse() : List[Url]
    - get_podcast_short_name() : str
    - get_current_episode_number() : int
    - get_linked_url_podcast_source(episode_number) : str
    }

class OtherParser {
    + base_url
    + parse() : List[Url]
    - get_podcast_short_name() : str
    - get_current_episode_number() : int
    - get_linked_url_podcast_source(episode_number) : str
    }

```

