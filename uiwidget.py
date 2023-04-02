from io_ import get_device_and_import_modules
from protocols import DeviceType
if get_device_and_import_modules() == DeviceType.ios:
    import ui


class UrlRow(ui.View):
    def __init__(self, width=200, height=40, bg_color='white', url=None):
        self.set_attrs(width=width, height=height, bg_color=bg_color)
        self.url = url
        self.text = url.description
        self.add_button_and_label(self.text)

    def set_attrs(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)

    def add_button_and_label(self, text, url='none'):
        self.text = text
        self.url = url
        lb = ui.Label()
        lb.text = text
        lb.font = ('Arial Rounded MT Bold', 15)
        lb.size_to_fit()
        lb.center = self.center
        self.add_subview(lb)
        self.switch = ui.Switch()
        self.add_subview(self.switch)
