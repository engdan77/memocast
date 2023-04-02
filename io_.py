from enum import Enum
import requests

from protocols_ import DeviceType


def get_device_and_import_modules() -> DeviceType:
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
	r = requests.get(url, verify=False)
	return r.content.decode()


