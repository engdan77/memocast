import random
from abc import ABC, abstractmethod
from .protocols import DeviceType
from .io_ import get_device_and_import_modules
from . import PODCAST_PREFIX


class BaseClipboard(ABC):
    def __init__(self):
        ...

    @abstractmethod
    def _get(self) -> str:
        """Get clipboard from system"""
        ...

    def get_and_verify(self, prefix_required=PODCAST_PREFIX) -> str:
        """Get from clipboard and verify it comes from Google podcasts"""
        url = self._get()
        return url if url.startswith(prefix_required) else None


class IosClipboard(BaseClipboard):
    def _get(self) -> str:
        import clipboard
        import appex
        url = clipboard.get()
        if not url:
            url = appex.get_url()
        return url


class MockClipboard(BaseClipboard):
    def _get(self) -> str:
        fake_urls = (
            "https://podcasts.google.com?feed=aHR0cHM6Ly90YWxrcHl0aG9uLmZtL2VwaXNvZGVzL3Jzcw%3D%3D&episode=ODA0Njk2OGQtY2I1OC00ZTVhLTlhOTQtZGE4NGU3ZGU2Y2Rj",
        )
        return random.choice(fake_urls)


class OtherClipboard(BaseClipboard):
    def _get(self) -> str:
        from tkinter import Tk
        return Tk().clipboard_get()


def get_clipboard_instance():
    """Get instance of clipboard manager based on device used"""
    device: DeviceType = get_device_and_import_modules()
    if device == DeviceType.ios:
        return IosClipboard()
    if device == DeviceType.other:
        return OtherClipboard()  # Will use clipboard instead
    assert False, "No valid device identified"
