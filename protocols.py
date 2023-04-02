from enum import Enum
from dataclasses import dataclass
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from parser_ import PodcastParser


@dataclass
class Url:
    url: str
    description: str
    parser: "PodcastParser"


class DeviceType(str, Enum):
    ios = 'ios'
    other = 'other'
