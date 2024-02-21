from os.path import join
from numpy import zeros
from random import sample, random, randint

from scr.toolbox import file2sound
from scr.xyt2game import game
from scr.utils import spx_folder, aud_eft_folder,\
    compose_sbkg, scr_colors

from scr.map_color import ScrPaint

from kivy.animation import Animation
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.image import Image


def strategy(c1, cp1, cp2):
    st = ''
    s1 = []
    for i in cp1:
        if i:
            if i[0] == c1[0]:
                s1.append(i)
            if i[1:] == c1[1:]:
                s1.append(i)
    if s1:
        n = 0
        for s in s1:
            for ii in cp2:
                if ii:
                    if ii[0] == s[0]:
                        st = s1[n]
                    if ii[1:] == s[1:]:
                        st = s1[n]
            n += 1
    return st


class BtnChs(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(BtnChs, self).__init__(**kwargs)
        self.__end = 0

    def on_press(self):
        self.__end = 1

    def end(self):
        return self.__end

    def reset(self):
        self.__end = 0


class Btn(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(Btn, self).__init__(**kwargs)


class Gm(FloatLayout):
    btnsda = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Gm, self).__init__(**kwargs)
        self.touch = 'down'
        g = game()
        self.xyt_btr = g['xyt']['btr']
        self.file_btr = g['files']['btr']
        self.config()

    def game(self, _):
        if self.turn == 1:
            self.turn_machine()
        else:
            self.evt = Clock.schedule_interval(self._update_chs, 1 / 30)

    def pre_change_turn(self, _):
        if self.turn == 1:
            if [i for i in self.cards_current_p1 if i]:
                return self.change_turn(2)
            else:
                self.res_tkn(1)
        else:
            if [i for i in self.cards_current_p2 if i]:
                return self.change_turn(1)
            else:
                self.res_tkn(2)

    def change_turn(self, turn):
        def tr(_):
            if turn == 1:
                self.turn_p1.source = self.turn_files['on']
                self.turn_p2.source = self.turn_files['off']
                self.pass_btn.disabled = True

            else:
                self.turn_p2.source = self.turn_files['on']
                self.turn_p1.source = self.turn_files['off']
                self.pass_btn.disabled = False
                for tag in self.range_chs():
                    self.cards_im_p2[tag].disabled = False
            Clock.schedule_once(self.game, .5)

        self.aud_turn.play()
        self.turn = turn
        Clock.schedule_once(tr, .2)

    def start_turn(self, _):
        if random() > .75:
            return self.change_turn(1)
        else:
            return self.change_turn(2)

    def range_chs(self):
        rg = []
        n = 0
        for st in self.cards_current_p2:
            if st:
                rg.append(n)
            n += 1
        return rg

    def change_fnc(self, direction):
        self.fnc = direction
        for n in self.range_chs():
            if direction == 1:
                """ img2resp """
                self.cards_im_p2[n].disabled = False
            if direction == 0:
                """ resp2img """
                self.cards_im_p2[n].disabled = True

    def mont2release(self, _):
        def anim(_):
            Animation(
                pos=psrel,
                duration=.6).start(self.current_target[-1])

        psrel = self.pos_release()
        self.remove_widget(self.monte)

        self.current_data()

        self.add_widget(self.monte)
        self.aud_dist.play()
        self.pass_cum = 0
        Clock.schedule_once(anim, .2)
        if self.trial == 0:
            Clock.schedule_once(self.start_turn, 2)
            self.trial = 1
        else:
            self.pre_change_turn(0)

    def current_data(self):
        if self.card_mix:
            self.current_card = self.card_mix[-1]
            self.card_mix.pop()

            if self.current_card == 'x' or self.current_card == 'y':
                self.current_card = self.card_mix[-1]
                self.card_mix.pop()

            self.current_target.append(Image(
                source=join(spx_folder, '{}.png'.format(self.current_card)),
                size_hint=(None, None), size=self.size_monte.copy(), pos=self.pos_monte.copy()))
            self.add_widget(self.current_target[-1])
        else:
            self.card_mix = self.mix()

            self.current_data()

    def pre_start(self):
        Clock.schedule_once(self.dist_card, 2)
        Clock.schedule_once(self.mont2release, 6)

    def mix(self):
        mixcard = []
        if self.level == 0:
            for n in ['a', 'b', 'c', 'd']:
                for nn in range(4):
                    mixcard.append('{}{}'.format(n, nn))
            mixcard.append('y')
        if self.level == 1:
            for n in ['a', 'b', 'c', 'd']:
                for nn in range(12):
                    mixcard.append('{}{}'.format(n, nn))
            mixcard.append('x')
        return sample(mixcard, k=len(mixcard))

    def res_tkn(self, player):
        def disp_tks(_):
            self.add_widget(self.tks[-1])

        if self.tks_files:
            pass
        else:
            self.update_data('tks')
        c = randint(0, len(self.tks_files) - 1)
        file = self.tks_files[c]
        self.tks_files.pop(c)
        self.player_win = 'p{}'.format(player)

        if player == 1:
            sh = self.tks_xyt_p1['size_hint']
            ph = self.tks_xyt_p1['pos_hint'][self.tks_p1]
            self.tks_p1 += 1
            self.lim_tks = self.tks_p1
        else:
            sh = self.tks_xyt_p2['size_hint']
            ph = self.tks_xyt_p2['pos_hint'][self.tks_p2]
            self.tks_p2 += 1
            self.lim_tks = self.tks_p2

        self.tks.append(Image(source=file,
                              size_hint=sh,
                              pos_hint={'x': ph[0], 'y': ph[1]}))

        self.aud_win.volume = .6
        self.aud_win.play()
        Clock.schedule_once(disp_tks, .3)
        self.ntag = 0
        self.limtag = len(self.current_target)
        self.retc = Clock.schedule_interval(self.return_cards, .15)

    def return_cards(self, _):
        self.remove_widget(self.monte)
        dur = .3
        pos = self.pos_monte
        Animation(pos=[pos[0], pos[1]], duration=dur).start(self.current_target[self.ntag])
        self.ntag += 1
        self.add_widget(self.monte)
        if self.ntag >= self.limtag:
            self.retc.cancel()
            self.ntag = 0
            self.limtag = self.num_cards
            if self.player_win == 'p1':
                self.retc = Clock.schedule_interval(self.return_cards_p1, .15)
            if self.player_win == 'p2':
                self.retc = Clock.schedule_interval(self.return_cards_p2, .15)

    def return_cards_p1(self, _):
        self.remove_widget(self.monte)
        dur = .3
        pos = self.pos_monte
        Animation(pos=[pos[0], pos[1]], duration=dur).start(self.cards_im_p1[self.ntag])
        self.ntag += 1
        self.add_widget(self.monte)
        if self.ntag >= self.limtag:
            self.retc.cancel()
            self.ntag = 0
            self.limtag = self.num_cards
            if self.player_win == 'p1':
                self.retc = Clock.schedule_interval(self.return_cards_p2, .15)
            else:
                Clock.schedule_once(self.remove_cards, 2)

    def return_cards_p2(self, _):
        self.remove_widget(self.monte)
        dur = .3
        pos = self.pos_monte
        Animation(pos=[pos[0], pos[1]], duration=dur).start(self.cards_im_p2[self.ntag])
        self.ntag += 1
        self.add_widget(self.monte)
        if self.ntag >= self.limtag:
            self.retc.cancel()
            self.ntag = 0
            self.limtag = self.num_cards
            if self.player_win == 'p2':
                self.retc = Clock.schedule_interval(self.return_cards_p1, .15)
            else:
                Clock.schedule_once(self.remove_cards, 2)

    def remove_cards(self, _):
        for target in self.current_target:
            self.remove_widget(target)
        for card in self.cards_im_p2:
            self.remove_widget(card)
        for card in self.cards_im_p1:
            self.remove_widget(card)
        self.card_mix = self.mix()
        self.trial = 0
        if self.lim_tks >= 3:
            self.reset_in()
        else:
            self.pre_start()

    def reset_in(self):
        """ effecs popup>> 'de novo' / 'sair' """
        Clock.schedule_once(self.sda_popup, 2)

    def eft_return(self):
        ps = self.card_xyt_p2[self.tag]
        return Animation(pos=(ps[0], ps[1]), d=.6, t='in_out_quart').start(
            self.cards_im_p2[self.tag])

    def eft_join(self):
        eft = 'out_back'
        dur = .9
        if self.touch == 'move':
            dur = .3
            eft = 'in_out_quart'
        ps = self.pos_release()
        return Animation(pos=(ps[0], ps[1]), d=dur, t=eft).start(
            self.cards_im_p2[self.tag])

    def return_evt(self, _):
        self.evt = Clock.schedule_interval(self._update_chs, 1 / 30)

    def ok_result(self):
        self.reset_chs()
        self.eft_join()

        for tag in self.range_chs():
            self.cards_im_p2[tag].disabled = True
        self.evt.cancel()
        self.remove_widget(self.cards_im_p2[self.tag])
        self.current_card = self.cards_current_p2[self.tag]
        self.cards_current_p2[self.tag] = ''
        self.add_widget(self.cards_im_p2[self.tag])
        self.pass_btn.disabled = True
        if self.pass_cum >= 2:
            Clock.schedule_once(self.mont2release, 2)
        else:
            Clock.schedule_once(self.pre_change_turn, 2)

    def ok_chs(self):
        ok = 0
        if self.current_card[0] == self.cards_current_p2[self.tag][0]:
            self.pass_cum = 0
            ok = 1
        if self.current_card[1:] == self.cards_current_p2[self.tag][1:]:
            self.pass_cum = 0
            ok = 1
        if self.cards_current_p2[self.tag] == 'x' or \
                self.cards_current_p2[self.tag] == 'y':
            ok = 1
            if len([i for i in self.cards_current_p2 if i]) > 1:
                self.pass_cum = 2
        return ok

    def verify_chs(self):
        if self.ok_chs() > 0:
            self.ok_result()

    def _update_chs(self, _):
        self.tag = -1
        rg = self.range_chs()
        z = list(zeros(self.num_cards, dtype=int))
        for n in range(self.num_cards):
            if n in rg:
                if self.cards_im_p2[n].end() > 0:
                    self.cards_im_p2[n].reset()
                    z[n] = 1
        if 1 in z:
            self.tag = z.index(1)
            self.verify_chs()

    def reset_chs(self):
        tag = 0
        for _ in self.cards_im_p2:
            self.cards_im_p2[tag].reset()
            tag += 1
        return

    def eft_btn(self, _):
        self.pass_btn.source = self.pass_files['eft']
        if self.turn == 2:
            self.evt.cancel()

    def act_btn(self, _):
        self.pass_btn.disabled = True
        self.pass_btn.source = self.pass_files['on']
        self.pass_cum += 1

        if self.pass_cum >= 2:
            Clock.schedule_once(self.mont2release, 2)
        else:
            self.pre_change_turn(0)

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

    def act_chs(self, _):
        # self.change_fnc(0)
        pass

    def turn_machine(self):
        self.resp1 = -1
        val_resp = ''
        stg = strategy(self.current_card, self.cards_current_p1, self.cards_current_p2)
        if stg:
            self.resp1 = self.cards_current_p1.index(stg)
        else:
            okc, okf = [], []
            n = 0
            for i in self.cards_current_p1:
                if i:
                    if i[0] == self.current_card[0]:
                        okf.append(n)
                    if i[1:] == self.current_card[1:]:
                        okc.append(n)
                n += 1
            if okc or okf:
                if okc and okf:
                    if len(okc) > len(okf):
                        self.resp1 = okc[0]
                    if len(okc) < len(okf):
                        self.resp1 = okf[0]
                    if len(okc) == len(okf):
                        self.resp1 = okc[0]
                else:
                    if okc:
                        self.resp1 = okc[0]
                    if okf:
                        self.resp1 = okf[0]
            else:
                if 'x' in self.cards_current_p1:
                    val_resp = 'x'
                    self.resp1 = self.cards_current_p1.index('x')
                if 'y' in self.cards_current_p1:
                    val_resp = 'y'
                    self.resp1 = self.cards_current_p1.index('y')

        if self.resp1 >= 0:
            self.pass_cum = 0
            if val_resp == 'x' or val_resp == 'y':
                if len([i for i in self.cards_current_p1 if i]) > 1:
                    self.pass_cum = 2

            self.remove_widget(self.cards_im_p1[self.resp1])
            self.current_card = self.cards_current_p1[self.resp1]
            self.cards_current_p1[self.resp1] = ''
            self.add_widget(self.cards_im_p1[self.resp1])
            Clock.schedule_once(self.resp_p1, 3)
        else:
            self.simule_pass()

    def resp_p1(self, _):
        eft = 'out_back'
        posr = self.pos_release()
        Animation(pos=posr, d=.85, t=eft).start(self.cards_im_p1[self.resp1])
        if self.pass_cum >= 2:
            Clock.schedule_once(self.mont2release, .9)
        else:
            Clock.schedule_once(self.pre_change_turn, .9)

    def simule_pass(self):
        def eft(_):
            if self.ns == 0:
                self.pass_btn.source = self.pass_files['eft']
                self.ns = 1
            else:
                self.pass_btn.source = self.pass_files['on']
                self.ns = 0
            self.nc += 1
            if self.nc >= 8:
                self.simeft.cancel()
                self.pass_btn.source = self.pass_files['on']
                Clock.schedule_once(self.act_btn, .4)

        def time_eft(_):
            self.simeft = Clock.schedule_interval(eft, .2)
        self.ns = 0
        self.nc = 0
        Clock.schedule_once(time_eft, 2)

    def dist_card(self, _):
        self.stop = 0
        self.player_win = ''
        self.cum_cards = []
        self.cards_im_p1 = []
        self.remove_widget(self.monte)

        self.cards_current_p1 = []
        for n in range(self.num_cards):
            self.cards_current_p1.append(self.card_mix[-1])
            self.cards_im_p1.append(Image(
                source=join(spx_folder, '{}.png'.format(self.card_mix[-1])),
                size_hint=(None, None), size=self.size_monte, pos=self.pos_monte))
            self.add_widget(self.cards_im_p1[-1])
            self.card_mix.pop()

        self.cards_current_p2 = []
        self.cards_im_p2 = []
        for n in range(self.num_cards):
            self.cards_current_p2.append(self.card_mix[-1])

            self.cards_im_p2.append(BtnChs(
                source=join(spx_folder, '{}.png'.format(self.card_mix[-1])),
                size_hint=(None, None), size=self.size_monte, pos=self.pos_monte))

            self.cards_im_p2[-1].bind(on_release=self.act_chs)
            self.cards_im_p2[-1].disabled = True
            self.add_widget(self.cards_im_p2[-1])
            self.card_mix.pop()
        self.add_widget(self.monte)
        if random() > .5:
            Clock.schedule_once(self.pre_animd_c1, 1.1)
            Clock.schedule_once(self.pre_animd_c2, 2.5)
        else:
            Clock.schedule_once(self.pre_animd_c2, 1.1)
            Clock.schedule_once(self.pre_animd_c1, 2.5)

    def pre_animd_c1(self, _):
        self.aud_dist.play()
        Clock.schedule_once(self.animd_c1, .2)

    def animd_c1(self, _):
        dur = .8
        pos = self.card_xyt_p1['pos']
        for n in range(self.num_cards):
            Animation(
                pos=[pos[n][0], pos[n][1]],
                duration=dur).start(self.cards_im_p1[n])

    def pre_animd_c2(self, _):
        self.aud_dist.play()
        Clock.schedule_once(self.animd_c2, .2)

    def animd_c2(self, _):
        dur = .8
        pos = self.card_xyt_p2['pos']
        for n in range(self.num_cards):
            Animation(
                pos=[pos[n][0], pos[n][1]],
                duration=dur).start(self.cards_im_p2[n])

    def update_data(self, obj):
        setting = game()
        if obj == 'tks':
            ftk = setting['tks']
            self.tks_files = sample(ftk, k=len(ftk))

    def variables(self):
        self.stop = 0
        self.finalize = 0
        self.turn = 0
        self.trial = 0
        self.current_target = []
        self.card_mix = self.mix()
        self.tks_p1 = 0
        self.tks_p2 = 0
        self.distrand = 0

    def remove_setting(self):
        self.remove_widget(self.paint_files)
        self.remove_widget(self.turn_p1)
        self.remove_widget(self.turn_p2)
        self.remove_widget(self.tkn1_paint)
        self.remove_widget(self.tkn2_paint)
        self.remove_widget(self.pass_btn)
        self.remove_widget(self.monte)
        for bkg in self.bkg:
            self.remove_widget(bkg)

    def config(self):
        self.aud_dist, _ = file2sound(join(aud_eft_folder, 'transition.wav'))
        self.aud_turn, _ = file2sound(join(aud_eft_folder, 'ping.wav'))
        self.aud_win, _ = file2sound(join(aud_eft_folder, 'win.wav'))
        self.aud_win.volume = .7
        self.audw, _ = file2sound(join(aud_eft_folder, 'bin2.wav'))
        self.audw.volume = .3

        var_game = game()
        self.num_cards = var_game['n_cards']
        self.level = var_game['level']

        setting = var_game['xyt']
        self.popup = var_game['pop_up']
        el_files = var_game['files']
        self.variables()
        self.bw = setting['btw']

        ftk = el_files['tks']
        self.tks_files = sample(ftk, k=len(ftk))
        self.tks_xyt_p1 = setting['player1']['tkn']
        self.tks_xyt_p2 = setting['player2']['tkn']
        self.tks = []

        self.card_xyt_p1 = setting['player1']['card']
        self.card_xyt_p2 = setting['player2']['card']
        self.fnc = 0

        self.limt = setting['lim']
        self.release = setting['release']

        self.size_monte = self.card_xyt_p1['size']
        p = setting['dealer']['pos']
        self.pos_monte = [p[0] + 2, p[1] + 8]

        scr = 'game'
        for c in compose_sbkg(scr, [[], scr_colors(scr)]):
            self.add_widget(ScrPaint(c))

        for col in var_game['colors']:
            self.add_widget(ScrPaint(col))

        self.add_widget(ScrPaint(self.xyt_btr))

        self.add_widget(Image(source=var_game['files']['set']))

        self.turn_files = el_files['btn_turn']
        self.turn_p1 = Image(
            source=self.turn_files['off'],
            size_hint=setting['player1']['btn']['size_hint'],
            pos_hint={'x': setting['player1']['btn']['pos_hint'][0],
                      'y': setting['player1']['btn']['pos_hint'][1]})
        self.add_widget(self.turn_p1)
        self.turn_p2 = Image(
            source=self.turn_files['off'],
            size_hint=setting['player2']['btn']['size_hint'],
            pos_hint={'x': setting['player2']['btn']['pos_hint'][0],
                      'y': setting['player2']['btn']['pos_hint'][1]})
        self.add_widget(self.turn_p2)

        self.pass_files = el_files['btn_pass']
        self.pass_btn = Btn(
            source=self.pass_files['on'],
            size_hint=setting['btn_pass']['size_hint'],
            pos_hint={'x': setting['btn_pass']['pos_hint'][0],
                      'y': setting['btn_pass']['pos_hint'][1]})
        self.pass_btn.bind(on_press=self.eft_btn)
        self.pass_btn.bind(on_release=self.act_btn)
        self.pass_btn.disabled = True
        self.add_widget(self.pass_btn)

        self.monte = Image(
            source=el_files['dealer'],
            size_hint=setting['dealer']['size_hint'],
            pos_hint={'x': setting['dealer']['pos_hint'][0],
                      'y': setting['dealer']['pos_hint'][1]})
        self.add_widget(self.monte)

        self.welcome()

    def welcome(self):
        self.btw = Btn(source=self.bw['file'],
                       size_hint=self.bw['size_hint'],
                       pos_hint={'x': self.bw['pos_hint'][0],
                                 'y': self.bw['pos_hint'][1]})
        self.btw.bind(on_release=self.acw)
        self.add_widget(self.btw)

    def acw(self, _):
        self.audw.play()
        Animation(opacity=0, duration=.4).start(self.btw)
        Clock.schedule_once(self.rmw, .4)

    def rmw(self, _):
        self.remove_widget(self.btw)
        self.pre_start()

    def sda_popup(self, _):
        for t in self.tks:
            self.remove_widget(t)

        self.pop = Image(
            source=self.popup['win']['file'],
            size_hint=self.popup['win']['xyt']['size_hint'],
            pos_hint={'x': self.popup['win']['xyt']['pos_hint'][0],
                      'y': self.popup['win']['xyt']['pos_hint'][1]})
        self.btn_cont = Button(
            size_hint=self.popup['btn']['cont']['size_hint'],
            pos_hint={'x': self.popup['btn']['cont']['pos_hint'][0],
                      'y': self.popup['btn']['cont']['pos_hint'][1]},
            opacity=0)
        self.btn_cont.bind(on_press=self.act_cont)

        self.btnsda.disabled = False

        self.bkg_sda = ScrPaint(self.popup['win']['col'])

        self.add_widget(self.bkg_sda)
        self.add_widget(self.pop)
        self.add_widget(self.btn_cont)

    def act_cont(self, _):
        self.reset_out()
        self.pre_start()

    def act_sda(self):
        self.reset_out()

    def reset_out(self):
        self.remove_widget(self.bkg_sda)
        self.remove_widget(self.pop)
        self.remove_widget(self.btn_cont)
        self.variables()
