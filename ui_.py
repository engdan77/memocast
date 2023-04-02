from functools import partial
from typing import List

from io_ import get_device_and_import_modules
from abc import abstractmethod
from unittest import mock

from protocols import Url, DeviceType
from uiwidget import UrlRow

if get_device_and_import_modules() == DeviceType.ios:
    import ui


def view_factory():
    """Factory function for Returning class of depending on which device used"""
    device = get_device_and_import_modules()
    if device.ios:
        return PythonistaPodView
    if device.other:
        return mock.Mock()


class BasePodView:

    @classmethod
    @abstractmethod
    def show(cls, urls: List[Url]):
        """Method expected for showing the UI"""
        ...


class PythonistaPodView(BasePodView, ui.View):
    tm = 20  # top margin
    vgap = 10  # vertical gap between cells

    def __init__(self, *args, **kwargs):
        ui.View.__init__(self, *args, **kwargs)
        self.sv = None
        self.cells = []
        self.height_cache = self.tm
        self.make_view()

    def make_view(self):
        sv = ui.ScrollView(name='sv')
        sv.frame = self.bounds
        sv.flex = 'wh'
        self.add_subview(sv)
        self.sv = sv

    def add_cell(self, cell):
        self.cells.append(cell)
        cell.y = self.height_cache
        self.height_cache += (cell.height + self.vgap)
        self.sv.content_size = (0, self.height_cache)
        self.sv.add_subview(cell)

    def get_all_enabled(*args):
        """Get all enabled URLs from view"""
        podcast_view, button = args
        for sw in podcast_view.cells:
            if hasattr(sw, 'switch'):
                print(sw.switch.value)

    @classmethod
    def show(cls, urls: List[Url]):
        w = 600
        h = 800
        f = (0, 0, w, h)
        podcast_view = cls(frame=f, bg_color='white')

        for url in urls:
            cell = UrlRow(width=200, height=40, bg_color='white', url=url)
            podcast_view.add_cell(cell)

        btn = ui.Button(name='save', frame=(0, 0, 90, 64))
        btn.font = ('Arial Rounded MT Bold', 25)
        btn.title = 'Save'
        btn.border_width = .9
        btn.corner_radius = 3
        btn.background_color = 'blue'
        btn.tint_color = 'white'
        btn.action = partial(cls.get_all_enabled, podcast_view)

        button = ui.Button(title='Save')
        podcast_view.add_cell(btn)
        podcast_view.present('sheet')