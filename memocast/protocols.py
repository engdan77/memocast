from enum import Enum
try:
    from dataclasses import dataclass
except ImportError:
    from .dataclasses_ import dataclass  # For earlier Python3


@dataclass
class Url:
    url: str
    description: str
    parser: "BasePodcastParser"


class DeviceType(str, Enum):
    ios = 'ios'
    other = 'other'
