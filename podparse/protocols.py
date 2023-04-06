from enum import Enum
from .dataclasses import dataclass


@dataclass
class Url:
    url: str
    description: str
    parser: "BasePodcastParser"


class DeviceType(str, Enum):
    ios = 'ios'
    other = 'other'
