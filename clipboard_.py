from enum import Enum, auto


class DeviceType(Enum, str):
	ios = auto()
	other = auto()


def prepare_device() -> DeviceType:
	"""import required packages and return type"""
	try:
		import clipboard as iosclipboard
	except ImportError:
		device = DeviceType.other
	else:
		device = DeviceType.ios
	return device
