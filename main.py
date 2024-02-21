from os.path import dirname, join
from scr.toolbox import op_direction, audinit, \
    sct_return, manager
from scr.utils import rand_color
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.properties import NumericProperty, StringProperty, \
    BooleanProperty, ListProperty
from kivy.lang import Builder
from kivy.app import App
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.config import Config


Config.set('graphics', 'width', '920')
Config.set('graphics', 'height', '660')


class Screens(Screen):
    fullscreen = BooleanProperty(False)

    def add_widget(self, *args, **kwargs):
        if 'content' in self.ids:
            return self.ids.content.add_widget(*args, **kwargs)
        return super(Screens, self).add_widget(*args, **kwargs)


class GameApp(App):
    index = NumericProperty(-1)
    cur_screen = StringProperty()
    current_title = StringProperty()
    screen_names = ListProperty([])
    hierarchy = ListProperty([])
    direct = ListProperty([])

    def build(self):
        size = [dp(int(Config.get('graphics', 'width'))),
                dp(int(Config.get('graphics', 'height')))]
        self.size = size
        manager('write', size)
        # self.title = 'SplashGame'

        self.icon = 'assets/mr.ico'
        self.screens = {}
        self.available_screens = ['PreGame', 'Game', 'GameSims']

        self.screen_names = self.available_screens
        self.idx = ''
        self.lastidx = ''
        self.reverse = []
        self.back = {}

        rand_color()
        curdir = dirname(__file__)
        audinit()

        self.available_screens = [
            join(curdir, 'kvs', '{}.kv'.format(fn).lower())
            for fn in self.available_screens]

        self.go_screen(self.screen_names[0])

    def go_screen(self, idx, delay=0, dur=1.5, direction='left'):
        self.lastidx = self.idx

        self.idx = idx
        self.duration = dur
        self.direction = direction
        self.scr_direction()

        if self.idx not in self.reverse:
            self.return_direction([self.idx, self.direction])

        Clock.schedule_once(self.act, delay)

    def act(self, _):
        self.root.ids.sm.switch_to(self.load_screen(self.idx),
                                   transition=SlideTransition(),
                                   direction=self.direction,
                                   duration=self.duration)

    def go_hierarchy_previous(self):
        self.go_screen(
            self.back[self.direct[-1]]['destiny'],
            direction=self.back[self.direct[-1]]['direction'])

    def return_direction(self, dirt):
        self.back[dirt[0]] = sct_return()
        self.back[dirt[0]]['scr'] = dirt[0].lower()

        self.back[dirt[0]]['direction'] = op_direction(dirt[1])
        if self.direct:
            self.back[dirt[0]]['destiny'] = self.direct[-1]
        self.reverse.append(dirt[0])

    def scr_direction(self):
        if self.lastidx in ['Gamesims', 'Game']:
            self.unload_screen()

    def load_screen(self, idx):
        if idx in self.screens:
            return self.screens[idx]
        i = self.screen_names.index(idx)
        screen = Builder.load_file(self.available_screens[i])
        self.screens[idx] = screen

        return screen

    def unload_screens(self):
        curdir = dirname(__file__)
        for scr in self.screens:
            Builder.unload_file(join(curdir, 'scr', 'kvs', '{}.kv'.format(scr).lower()))
        self.screens = {}

    def unload_screen(self):
        curdir = dirname(__file__)
        Builder.unload_file(join(curdir, 'scr', 'kvs', '{}.kv'.format(self.lastidx).lower()))
        self.screens.pop(self.lastidx)

    def on_pause(self):
        return True

    def on_resume(self):
        pass


if __name__ == '__main__':
    GameApp().run()
