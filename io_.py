from enum import Enum
import requests


class DeviceType(str, Enum):
	ios = 'ios'
	other = 'other'


def prepare_device() -> DeviceType:
	"""import required packages and return type"""
	try:
		import clipboard as iosclipboard
	except ImportError:
		device = DeviceType.other
	else:
		device = DeviceType.ios
	return device


def download_html(url: str) -> str:
	"""Download URL"""
	r = requests.get(url)


