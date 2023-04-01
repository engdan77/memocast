import ui


class UrlRow(ui.View):
    def __init__(self, width=200, height=40, bg_color='white'):
        self.set_attrs(width=width, height=height, bg_color=bg_color)
        self.text = None
        self.url = None
        text = kwargs.get('text', 'none')
        self.add_button_and_label(text)

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
