from enum import Enum


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