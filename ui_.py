from io_ import get_device_and_import_modules
from enums import DeviceType
from abc import abstractmethod
from unittest import mock
if get_device_and_import_modules() == DeviceType.ios:
    import ui


def view_factory():
    """Factory function for Returning class of depending on which device used"""
    device = get_device_and_import_modules()
    if device.ios:
        return PythonistaView
    if device.other:
        return mock.Mock()


class BaseView:

    @abstractmethod
    def show(self):
        """Method expected for showing the UI"""
        ...


class PythonistaView(BaseView, ui.View):

    def __init__(self):
        w,h = ui.get_screen_size()
        self.ty = ui.Label()
        self.ty.text = 'Hello'
        self.ty.text_color = 'black'
        self.ty.font = ('<system>', 60)
        self.ty.frame = (0, 0, w, h*0.25)
        self.ty.bg_color = 'yellow'
        self.sv = ui.ScrollView()
        self.sv.width = w
        self.sv.height = h*0.25
        self.sv.content_size = (2*w, h*0.25)
        self.sv.add_subview(self.ty)
        self.add_subview(self.sv)

    def show(self):
        self.present('fullsreen')
