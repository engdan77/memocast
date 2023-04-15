from .io_ import get_device_and_import_modules
from .protocols import DeviceType
from unittest import mock
if get_device_and_import_modules() == DeviceType.ios:
    import ui
else:
    ui = mock.Mock()


class UrlRow(ui.View):
    def __init__(self, width=200, height=40, bg_color='white', url=None):
        """This is the widget responsible for generating row based in link"""
        self.set_attrs(width=width, height=height, bg_color=bg_color)
        self.url = url
        self.text = url.description
        self.add_button_and_label(self.text)

    def __str__(self):
        return f'{self.url}'

    def set_attrs(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)

    def add_button_and_label(self, text):
        self.text = text
        lb = ui.Label()
        lb.text = text
        lb.x = 100
        lb.font = ('Arial Rounded MT Bold', 15)
        lb.size_to_fit()
        self.add_subview(lb)
        self.switch = ui.Switch()
        self.add_subview(self.switch)
