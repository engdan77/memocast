from functools import partial
from typing import List, Union, Callable
from .logging_ import logger

from .io_ import get_device_and_import_modules
from abc import abstractmethod
from unittest import mock

from .protocols import Url, DeviceType
from .uiwidget import UrlRow
from .reminder_ import add_reminder_from_url

if get_device_and_import_modules() == DeviceType.ios:
    import ui
    import console
else:
    class FakeClass:
        ...
    ui = mock.Mock()
    ui.View = FakeClass


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

    def add_urls_to_reminder(self, urls: List[Url]):
        """The view is responsible to use this method that will add URLs to ios reminder"""
        print(urls)
        for url in urls:
            logger.info(f'Adding to reminder: {url}')
            add_reminder_from_url(url)

    @abstractmethod
    def get_option(self, options: List[str], title='') -> Union[str, None]:
        """UI for displaying options (buttons) to be selected"""
        ...


class PythonistaPodView(BasePodView, ui.View):
    tm = 20  # top margin
    vgap = 10  # vertical gap between cells
    ui = None

    def __init__(self, *args, **kwargs):
        ui.View.__init__(self, *args, **kwargs)
        self.sv = None
        self.cells = []
        self.height_cache = self.tm
        self.make_view()
        self.__class__.ui = self

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

    def get_all_enabled(self, button):
        """Get all enabled URLs from view"""
        enabled_urls = []
        for sw in self.cells:
            if hasattr(sw, 'switch') and sw.switch is not None:
                if sw.switch.value is True:
                    enabled_urls.append(sw.url)
        self.add_urls_to_reminder(enabled_urls)
        self.close()

    @classmethod
    def exit_app(cls, *args):
        cls.ui.close()
        raise SystemExit('Exiting application')

    @classmethod
    def show(cls, urls: List[Url]):
        w = 600
        h = 800
        f = (0, 0, w, h)
        podcast_view = cls(frame=f, bg_color='white')

        for url in urls:
            cell = UrlRow(width=1024, height=40, bg_color='white', url=url)
            podcast_view.add_cell(cell)

        save_btn = cls.create_button(callback=partial(cls.get_all_enabled, podcast_view), label='Save')
        exit_btn = cls.create_button(callback=cls.exit_app, label='Exit')
        podcast_view.add_cell(save_btn)
        podcast_view.add_cell(exit_btn)
        podcast_view.present('fullscreen')

    @classmethod
    def create_button(cls, callback: Callable, label: str):
        button = ui.Button(name='save', frame=(0, 0, 90, 64))
        button.font = ('Arial Rounded MT Bold', 25)
        button.title = label
        button.border_width = .9
        button.corner_radius = 3
        button.background_color = 'blue'
        button.tint_color = 'white'
        button.action = callback
        return button

    def get_option(self, options: List[str], title: str = '') -> Union[str, None]:
        option_index = console.alert('', title, *options, hide_cancel_button=False)
        return options[option_index - 1]
