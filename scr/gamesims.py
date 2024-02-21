from random import sample, random, randint
from os.path import basename, splitext
from scr.xyt2game import game_sim
from scr.utils import compose_sbkg, scr_colors
from scr.map_color import ScrPaint
from os.path import join

from scr.utils import aud_eft_folder
from scr.toolbox import file2sound

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Ellipse, Color, RoundedRectangle

from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior


class Btn(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(Btn, self).__init__(**kwargs)


class Inst(ButtonBehavior, Image):
    duration = .6
    duration_rm = .45

    def __init__(self, inst, **kwargs):
        super(Inst, self).__init__(**kwargs)
        self._n = 0
        self.inst = inst
        self.init_in()

    def on_release(self):
        self.disp()

    def wdg(self):
        self.canvas.before.clear()
        if self.inst[self._n]['col']:
            with self.canvas.before:
                Color(*self.inst[self._n]['col'])
                if self.inst[self._n]['form'] == 'ellipse':
                    Ellipse(size=self.inst[self._n]['size'],
                            pos=self.inst[self._n]['pos'])
                else:
                    RoundedRectangle(size=self.inst[self._n]['size'],
                                     pos=self.inst[self._n]['pos'])

        self.source = self.inst[self._n]['file']
        self.size_hint = self.inst[self._n]['size_hint']
        self.pos_hint = {'x': self.inst[self._n]['pos_hint'][0],
                         'y': self.inst[self._n]['pos_hint'][1]}
        Animation(opacity=1, duration=self.duration).start(self)
        self._n += 1

    def disp(self):
        Animation(opacity=0, duration=self.duration_rm).start(self)
        Clock.schedule_once(self.rmcanvas, self.duration_rm)

    def rmcanvas(self, _):

        self.wdg()

    @property
    def n(self):
        return self._n

    def init_in(self):
        self.opacity = 0
        self.wdg()


class GameSims(FloatLayout):
    disbtn = BooleanProperty(True)
    btr = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(GameSims, self).__init__(**kwargs)
        self.game = game_sim()
        self.config()

    def act_inst(self, _):
        self.meta_sims = 0
        nt = self.instructions.n
        self.instructions.disabled = True

        if nt == 1:
            Clock.schedule_once(self.eft_formcolors, 1.5)
        if nt == 2:
            self.nft = 0
            self.a = 0
            self.b = 3
            Clock.schedule_interval(self.continue_eft, 3)
            self.nst += 1

        if nt == 3:
            self.nft = 4
            self.a = 4
            self.b = 7
            Clock.schedule_interval(self.continue_eft, 4)
            self.nst += 1

        if nt == 4:
            Clock.schedule_once(self.jocker_in, 1)
            self.nst += 1

        if nt == 5:
            self.jocker_eft()
            self.nst += 1

        if nt == 6:
            Clock.schedule_once(self.dist_in, 1.8)
            self.nst += 1

        if nt == 7:
            self.kfc_in()
            self.nst += 1

        if nt == 8:
            self.return_inst(0)
            self.nst += 1

        if nt == 9:
            self.player = 2
            Clock.schedule_once(self.turn_in, 3.4)
            self.nst += 1

        if nt == 10:
            self.return_inst(0)
            self.nst += 1

        if nt == 11:
            self.point_idx = [1, 3]
            Clock.schedule_once(self.point_in, .4)
            self.nst += 1

        if nt == 12:
            self.point_idx = [2]
            Clock.schedule_once(self.point_in, .4)
            self.nst += 1

        if nt == 13:
            self.player = 2
            self.chs_idx = 3
            Clock.schedule_once(self.chs_in, 3.8)
            self.nst += 1

        if nt == 14:
            self.player = 1
            Clock.schedule_once(self.turn_in, 4.4)
            self.chs_idx = 1
            Clock.schedule_once(self.chs_in, 6.8)
            self.nst += 1

        if nt == 15:
            self.player = 2
            Clock.schedule_once(self.turn_in, 1.8)
            self.nst += 1

        if nt == 16:
            self.meta_sims = 1
            self.meta_idx = [[2, 1], [1, 0]]
            self.xyt_eft = []
            for n in [0, 1]:
                self.xyt_eft.append(self.game['player'][n]['card']['pos'][n])

            self.mt = 2
            self.nst += 1
            self.sms(0)

        if nt == 17:

            self.meta_sims = 1
            self.meta_idx = [[2], [0]]
            self.mt = 1
            self.nst += 1
            self.return_sms()

        if nt == 18:
            self.nst += 1
            Clock.schedule_once(self.bps, 6)

        if nt == 19:
            self.meta_sims = 1
            self.meta_idx = [[2, 1], [1, 0]]
            self.xyt_eft = []
            for n in [0, 1]:
                self.xyt_eft.append(self.game['player'][n]['card']['pos'][n])
            self.mt = 2
            self.nst += 1
            self.sms(0)
            Clock.schedule_once(self.coin_in, 2)

        if nt == 20:
            self.player = 2
            self.chs_idx = 2
            Clock.schedule_once(self.chs_in, 1.8)
            Clock.schedule_once(self.coin_eft, 4.2)
            Clock.schedule_once(self.return_end, 6.3)

            self.nst += 1
        if nt == 21:
            self.remove_widget(self.btr)
            self.disbtn = False
            self.add_widget(self.btr)

    def return_end(self, _):
        self.nd = 0
        self.aud_win.play()
        self.remove_widget(self.monte)
        self.add_widget(self.monte)
        Clock.schedule_interval(self.ret_end, .18)

    def ret_end(self, _):
        Animation(pos=self.game['xyt']['dealer']['pos']).start(self.end[self.nd])
        self.nd += 1
        if self.nd >= len(self.end):
            return False

    def coin_eft(self, _):
        Animation(pos=self.game['player'][1]['tkn']['pos'][0],
                  size=self.game['player'][1]['tkn']['size'],
                  duration=1.25).start(self.imcoin[0])

    def coin_in(self, _):
        for coin in self.imcoin:
            self.add_widget(coin)
            Animation(opacity=1).start(coin)

    def bps(self, _):
        self.nbt = 0
        self.vbt = 0
        Clock.schedule_interval(self.bps_eft, .3)

    def bps_eft(self, _):
        if self.vbt == 0:
            self.pass_btn.source = self.pass_files['eft']
            self.vbt = 1
        else:
            self.pass_btn.source = self.pass_files['on']
            self.vbt = 0
        self.nbt += 1
        if self.nbt > 16:
            self.pass_btn.source = self.pass_files['on']
            self.player = 2
            Clock.schedule_once(self.turn_in, .1)

            return False

    def return_sms(self):
        Animation(pos=self.xyt_eft[0],
                  duration=1.2, t='out_back').start(self.imdist[0][0])
        Clock.schedule_once(self.rets, 1.4)

    def rets(self, _):
        Animation(pos=self.xyt_eft[1],
                  duration=1.2, t='out_back').start(self.imdist[1][1])
        self.xyt_eft = [self.game['player'][1]['card']['pos'][0]]
        Clock.schedule_once(self.sms, .4)

    def sms(self, _):
        self.m = 0
        Clock.schedule_interval(self.chs_in, 3.1)

    def chs_in(self, _):
        if self.meta_sims > 0:
            if self.m < len(self.meta_idx[0]):
                self.player = self.meta_idx[0][self.m]
                self.chs_idx = self.meta_idx[1][self.m]
            else:
                return False
        self.remove_widget(self.imdist[self.player - 1][self.chs_idx])
        self.add_widget(self.imdist[self.player - 1][self.chs_idx])
        Animation(pos=self.pos_release(),
                  size=self.release['size'],
                  duration=1.4,
                  t='out_back').start(self.imdist[self.player - 1][self.chs_idx])
        if self.meta_sims == 0:
            Clock.schedule_once(self.return_inst, 1.4)
        else:
            Clock.schedule_once(self.turn_in, 1.8)

    def turn_in(self, _):
        self.aud_turn.play()
        Clock.schedule_once(self.turn_eft, .6)

    def turn_eft(self, _):
        if self.meta_sims > 0:
            if self.meta_idx[0][self.m] == 1:
                self.turn_p1.source = self.turn_files['off']
                self.turn_p2.source = self.turn_files['on']
            else:
                self.turn_p1.source = self.turn_files['on']
                self.turn_p2.source = self.turn_files['off']
        else:
            if self.player == 1:
                self.turn_p1.source = self.turn_files['on']
                self.turn_p2.source = self.turn_files['off']
            else:
                self.turn_p1.source = self.turn_files['off']
                self.turn_p2.source = self.turn_files['on']

        if self.meta_sims > 0:
            self.m += 1
            if self.m >= len(self.meta_idx[0]):
                self.return_inst(0)
        else:
            self.return_inst(0)

    def point_in(self, _):
        self.point_delay = 53 * .08
        self.pt = 0
        self.ptd = 0
        Clock.schedule_interval(self.point_eft, self.point_delay+.2)

    def point_eft(self, _):
        self.add_widget(self.point[self.point_idx[self.pt]])
        self.point[self.point_idx[self.pt]].anim_delay = .08
        Clock.schedule_once(self.point_out, self.point_delay)
        self.pt += 1
        if self.pt >= len(self.point_idx):
            Clock.schedule_once(self.return_inst, self.point_delay)
            return False

    def point_out(self, _):
        self.remove_widget(self.point[self.point_idx[self.ptd]])
        self.ptd += 1

    def kfc_in(self):
        self.mix.source = self.game['files']['card'][7]
        self.remove_widget(self.monte)
        self.add_widget(self.mix)
        self.add_widget(self.monte)
        self.end.append(self.mix)
        Clock.schedule_once(self.kfc_eft, 1)

    def kfc_eft(self, _):
        self.aud_dist.play()
        Animation(pos=self.pos_release(),
                  size=self.release['size'],
                  duration=1.2, t='out_back').start(self.mix)
        Clock.schedule_once(self.return_inst, 1.2)

    def dist_in(self, _):
        self.mdt = 0
        Clock.schedule_interval(self.dist_eft, 2)

    def dist_eft(self, _):
        self.aud_dist.play()
        self.remove_widget(self.monte)
        for n in range(4):
            self.add_widget(self.imdist[self.mdt][n])
            Animation(pos=self.game['player'][self.mdt]['card']['pos'][n],
                      duration=.8).start(self.imdist[self.mdt][n])
            self.end.append(self.imdist[self.mdt][n])

        self.add_widget(self.monte)
        self.mdt += 1
        if self.mdt >= 2:
            Clock.schedule_once(self.return_inst, .8)
            return False

    def jocker_in(self, _):
        self.add_widget(self.jocker)
        Clock.schedule_once(self.return_inst, .2)

    def jocker_eft(self):
        Animation(pos=self.game['setting']['y']['pos'],
                  size=self.game['setting']['y']['size'],
                  duration=1.2, t='in_quart').start(self.jocker)
        Clock.schedule_once(self.mix_in, 3.8)

    def mix_in(self, _):
        self.mixfiles = []
        self.mxf = sample(range(len(self.game['files']['card'])),
                          k=len(self.game['files']['card']))
        for n in self.mxf:
            self.mixfiles.append(self.game['files']['card'][n])
        self.mix.source = self.mixfiles[0]
        self.monte.opacity = .3
        self.add_widget(self.mix)
        self.mx = 0
        Clock.schedule_interval(self.mix_eft, .36)

    def mix_eft(self, _):
        self.aud_mx.play()
        self.mix.source = self.mixfiles[self.mx]
        if self.mxf[self.mx] == 16:
            self.remove_widget(self.jocker)
        else:
            self.remove_widget(self.ids[self.ref_card()[self.mxf[self.mx]]])

        self.mx += 1

        if self.mx >= len(self.mixfiles):
            self.monte.opacity = 1
            self.remove_widget(self.mix)
            Clock.schedule_once(self.return_inst, 1.2)
            return False

    def return_inst(self, _):
        self.instructions.disabled = False

    def continue_eft(self, _):
        dur = 1.2
        d1 = self.game['setting']['demo'].copy()
        n = 0
        for cod in self.cod_card(self.game['setting']['manip_card'][self.nft]):
            Animation(pos=[d1[n]['pos'][0], d1[n]['pos'][1]],
                      size=d1[n]['size'],
                      duration=dur).start(self.ids[self.ref_card()[cod]])
            n += 1

        if self.nft > self.a:
            d2 = self.game['setting']['formcolors'].copy()
            for cod in self.cod_card(self.game['setting']['manip_card'][self.nft-1]):
                Animation(pos=[d2[cod]['pos'][0], d2[cod]['pos'][1]],
                          size=d2[cod]['size'],
                          duration=dur).start(self.ids[self.ref_card()[cod]])
        self.nft += 1
        if self.nft >= self.b:
            Clock.schedule_once(self.end_eft, 4)
            return False

    def end_eft(self, _):
        dur = 1.2
        d2 = self.game['setting']['formcolors'].copy()
        for cod in self.cod_card(self.game['setting']['manip_card'][self.nft-1]):
            Animation(pos=[d2[cod]['pos'][0], d2[cod]['pos'][1]],
                      size=d2[cod]['size'],
                      duration=dur).start(self.ids[self.ref_card()[cod]])
        Clock.schedule_once(self.return_inst, 1.2)

    def cod_card(self, dt):
        fc = self.ref_card()
        if dt[0] == 'color':
            cod = [i for i in range(len(fc)) if int(fc[i][1]) == dt[1]]
        else:
            cod = [i for i in range(len(fc)) if fc[i][0] == ['a', 'b', 'c', 'd'][dt[1]]]

        return cod

    def ref_card(self):
        fc = []
        for f in self.game['files']['card'][:-1]:
            fc.append(splitext(basename(f))[0])
        return fc

    def pos_release(self):
        p = self.release['pos'].copy()
        incx = randint(0, 12)
        incy = randint(0, 12)
        if random() > .5:
            incx *= -1
        if random() < .5:
            incy *= -1
        p[0] += incx
        p[1] += incy
        pos = [int(p[0]), int(p[1])]

        return pos

    def config(self):
        self.end = []

        self.aud_dist, _ = file2sound(join(aud_eft_folder, 'transition.wav'))
        self.aud_turn, _ = file2sound(join(aud_eft_folder, 'ping.wav'))
        self.aud_win, _ = file2sound(join(aud_eft_folder, 'win.wav'))
        self.aud_mx, _ = file2sound(join(aud_eft_folder, 'gup.wav'))

        f = ['belltree', 'bertrof2', 'brass']
        self.aud_fc1, _ = file2sound(join(aud_eft_folder, '{}.wav'.format(f[0])))
        self.aud_win.volume = .5
        self.aud_fc1.volume = .3

        scr = 'gamesim'
        for c in compose_sbkg(scr, [[], scr_colors(scr)]):
            self.add_widget(ScrPaint(c))

        for col in self.game['colors']:
            self.add_widget(ScrPaint(col))

        self.add_widget(ScrPaint(self.game['xyt']['btr']))

        self.release = self.game['xyt']['release']

        self.add_widget(Image(source=self.game['files']['set']))
        self.turn_files = self.game['files']['btn_turn']
        self.turn_p1 = Image(
            source=self.turn_files['off'],
            size_hint=self.game['player'][0]['btn']['size_hint'],
            pos_hint={'x': self.game['player'][0]['btn']['pos_hint'][0],
                      'y': self.game['player'][0]['btn']['pos_hint'][1]})
        self.add_widget(self.turn_p1)
        self.turn_p2 = Image(
            source=self.turn_files['off'],
            size_hint=self.game['player'][1]['btn']['size_hint'],
            pos_hint={'x': self.game['player'][1]['btn']['pos_hint'][0],
                      'y': self.game['player'][1]['btn']['pos_hint'][1]})
        self.add_widget(self.turn_p2)

        self.pass_files = self.game['files']['btn_pass']
        self.pass_btn = Btn(
            source=self.pass_files['on'],
            size_hint=self.game['xyt']['btn_pass']['size_hint'],
            pos_hint={'x': self.game['xyt']['btn_pass']['pos_hint'][0],
                      'y': self.game['xyt']['btn_pass']['pos_hint'][1]})
        self.pass_btn.disabled = True
        self.add_widget(self.pass_btn)

        self.monte = Image(
            source=self.game['files']['dealer'],
            size_hint=self.game['xyt']['dealer']['size_hint'],
            pos_hint={'x': self.game['xyt']['dealer']['pos_hint'][0],
                      'y': self.game['xyt']['dealer']['pos_hint'][1]})
        self.add_widget(self.monte)
        self.mix = Image(
            size_hint=[None, None],
            size=self.game['setting']['mix']['size'],
            pos=self.game['setting']['mix']['pos'])
        self.jocker = Image(
            source=self.game['files']['card'][-1],
            size_hint=[None, None],
            size=self.game['setting']['demo'][-2]['size'],
            pos=[self.game['setting']['demo'][-2]['pos'][0]+5,
                 self.game['setting']['demo'][-2]['pos'][1]])

        self.point = []
        for n in range(4):
            point = Image(
                source=self.game['setting']['point'][n]['file'],
                size_hint=[None, None],
                size=self.game['setting']['point'][n]['size'],
                pos=self.game['setting']['point'][n]['pos'],
                anim_loop=1, anim_delay=-1)
            self.point.append(point)
        self.imcoin = []
        n = 0
        for xyt in self.game['setting']['coins']:
            self.imcoin.append(Image(source=self.game['files']['tks'][n],
                               size_hint=[None, None], size=xyt['size'],
                               pos=xyt['pos'], opacity=0))
            n += 1

        self.imdist = []
        for nn in self.game['setting']['dist']:
            imdist = []
            for nd in nn:
                imdist.append(Image(
                    source=self.game['files']['card'][nd],
                    size_hint=[None, None],
                    size=self.game['setting']['mix']['size'],
                    pos=self.game['setting']['mix']['pos']))
            self.imdist.append(imdist)
        Clock.schedule_once(self.start_inst, 3)

    def start_inst(self, _):
        self.instructions = Inst(self.game['setting']['instructions'])
        self.instructions.bind(on_release=self.act_inst)
        self.nst = 0
        self.add_widget(self.instructions)

    def eft_formcolors(self, _):
        self.aud_fc1.play()
        self.fcn = 0
        Clock.schedule_once(self.pre_form, .6)

    def pre_form(self, _):
        Clock.schedule_interval(self.formcolors, .08)

    def formcolors(self, _):
        fc = self.game['setting']['formcolors'].copy()
        im = Image(
            source=self.game['files']['card'][self.fcn],
            size_hint=[None, None],
            size=fc[self.fcn]['size'],
            pos=fc[self.fcn]['pos'])
        im.keep_ratio = True
        im.allow_stretch = True
        self.add_widget(im)
        self.ids[self.ref_card()[self.fcn]] = im
        self.fcn += 1
        if self.fcn >= len(self.game['files']['card']) - 1:
            Clock.schedule_once(self.return_inst, .2)
            return False


if __name__ == '__main__':
    from kivy.app import App
    from kivy.config import Config

    Config.set('graphics', 'width', '920')
    Config.set('graphics', 'height', '660')

    class Gs(App):
        def build(self):
            return GameSims()

    Gs().run()
