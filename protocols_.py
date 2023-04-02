from enum import Enum

from dataclasses import dataclass
from parser_ import PodcastParser


@dataclass
class Url:
    url: str
    description: str
    parser: PodcastParser


class DeviceType(str, Enum):
    ios = 'ios'
    other = 'other'
