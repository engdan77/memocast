import random
from abc import ABC, abstractmethod
from .protocols import DeviceType
from .io_ import get_device_and_import_modules


class BaseClipboard(ABC):
	def __init__(self):
		...

	@abstractmethod
	def get(self) -> str:
		"""Get clipboard from system"""
		...


class IosClipboard(BaseClipboard):

	def get(self) -> str:
		import clipboard
		return clipboard.get()


class MockClipboard(BaseClipboard):

	def get(self) -> str:
		fake_urls = ('https://podcasts.google.com?feed=aHR0cHM6Ly90YWxrcHl0aG9uLmZtL2VwaXNvZGVzL3Jzcw%3D%3D&episode=ODA0Njk2OGQtY2I1OC00ZTVhLTlhOTQtZGE4NGU3ZGU2Y2Rj',)
		return random.choice(fake_urls)


def get_clipboard_instance():
	device: DeviceType = get_device_and_import_modules()
	if device == DeviceType.ios:
		return IosClipboard()
	if device == DeviceType.other:
		return MockClipboard()
	assert False, "No valid device identified"
