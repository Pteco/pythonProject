from scr.toolbox import convert_xyt, file2sound
from scr.utils import aud_eft_folder, sct_color
from scr.utils import compose_sbkg, scr_colors
from scr.map_color import ScrPaint, sda_colors
from scr.utils import scr_folder, btn_folder, spx_folder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from os import walk
from os.path import join, splitext


sct_atv = {}


def sct_obj():
    obj = {
        'xyt': {},
        'col': {},
        'file': ''}
    return obj


def btn_files(objs):
    fbtn = {}
    for obj in objs:
        if 'bt' in obj:
            if obj in ['btv']:
                fbtn[obj] = join(btn_folder, '{}.png'.format(obj))
            else:
                fbtn[obj] = {
                    'on': join(btn_folder, '{}_on.png'.format(obj)),
                    'off': join(btn_folder, '{}_off.png'.format(obj))}

    return fbtn


def txt_files(objs):
    ftxt = {}
    for _, _, arqs in walk(spx_folder):
        for arq in arqs:
            a = splitext(arq)[0]
            if a in objs:
                ftxt[a] = join(spx_folder, arq)
    return ftxt


def scr_files(objs):
    files = {}

    if txt_files(objs):
        i = txt_files(objs)
        for k in i:
            files[k] = i[k]

    if btn_files(objs):
        i = btn_files(objs)
        for k in i:
            files[k] = i[k]

    return files


def scr_manager(scr, objs, xyt):
    sct = {}
    n = 0
    for k in objs:
        sct[k] = sct_obj()
        sct[k]['xyt'] = convert_xyt(xyt[n])
        n += 1

    i = sda_colors(scr, sct)
    for k in objs:
        sct[k]['col'] = i[k]

    i = scr_files(objs)
    for k in i:
        sct[k]['file'] = i[k]

    sct['set'] = join(scr_folder, '{}.png'.format(scr))

    return sct


def pre_game():
    objs = ['bts', 'btr', 'bti']
    xyt = [
        [372, 165, 176, 176],
        [643, 53, 102, 102],
        [203, 353, 99, 99]
    ]
    sct = scr_manager('pregame', objs, xyt)
    return sct


def uni_sbkg(xy_col, col):
    sbk = {}
    n = 0
    for xy in xy_col:
        xt = convert_xyt(xy)
        sbk[str(n)] = sct_color()
        sbk[str(n)]['color'] = col
        sbk[str(n)]['size'] = xt['size']
        sbk[str(n)]['pos'] = xt['pos']
        n += 1
    return sbk


class Btn(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(Btn, self).__init__(**kwargs)


class Entry(FloatLayout):

    def __init__(self, **kwargs):
        super(Entry, self).__init__(**kwargs)
        self.entry = pre_game()
        self.config()

    def config(self):

        self.aud_btns, _ = file2sound(join(aud_eft_folder, 'pop.wav'))
        self.aud_start, _ = file2sound(join(aud_eft_folder, 'fantasia.wav'))

        scr = 'pregame'
        for c in compose_sbkg(scr, [[], scr_colors(scr)]):
            self.add_widget(ScrPaint(c))

        self.add_widget(ScrPaint(self.entry['bti']['col']))
        self.add_widget(Image(source=self.entry['set']))
