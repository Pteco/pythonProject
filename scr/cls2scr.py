from scr.toolbox import name2sound
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image


class Btn(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(Btn, self).__init__(**kwargs)


class AudBtn(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(AudBtn, self).__init__(**kwargs)
        self.aud = name2sound('gup')
        self.aud.volume = .5

    def on_press(self):
        self.aud.play()
