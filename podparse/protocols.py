from enum import Enum
from .dataclasses import dataclass
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from podparse.parsers.baseclass import BasePodcastParser


@dataclass
class Url:
    url: str
    description: str
    parser: "BasePodcastParser"


class DeviceType(str, Enum):
    ios = 'ios'
    other = 'other'
