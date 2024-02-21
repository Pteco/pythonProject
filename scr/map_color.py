from scr.toolbox import convert_xyt
from kivy.graphics import Rectangle, Ellipse, Color, RoundedRectangle
from kivy.uix.widget import Widget


class ScrPaint(Widget):
    def __init__(self, col, **kwargs):
        super(ScrPaint, self).__init__(**kwargs)
        cor = []
        for c in range(3):
            cor.append(col['color'][c] / 255)

        with self.canvas.before:
                Color(*cor)
                if col['form'] == 'rectangle':
                    Rectangle(size=col['size'],
                              pos=col['pos'])
                if col['form'] == 'ellipse':
                    Ellipse(size=col['size'],
                            pos=col['pos'])

                if col['form'] == 'roundrect':
                    RoundedRectangle(size=col['size'],
                                     pos=col['pos'])


def sct_color() -> object:
    sct = {
        'color': [],
        'size': [],
        'pos': [],
        'form': 'rectangle'}
    return sct


def uni_col(coord, color):
    col = sct_color()
    col['color'] = color
    st = convert_xyt(coord)
    col['size'] = st['size']
    col['pos'] = st['pos']
    return col


sct_col = {
    'task': sct_color(),
    'smp': sct_color(),
    'chs': {},
    'sref': sct_color()}


sct_cols = {
    'bkg': {},
    'tkn': {
        'tks': [],
        'sch': []},
    'col': {}}


pallete = {
    '0': [14, 78, 89, 1], '1': [14, 78, 89, 1], '2': [64, 37, 153, 1],
    '4': [119, 0, 147, 1], '5': [145, 98, 57, 1], '6': [2, 54, 112, 1],
    '7': [57, 1, 61, 1], '8': [188, 157, 147, 1], '9': [147, 89, 31, 1],
    '10': [14, 78, 89, 1], '11': [79, 52, 154, 1], '12': [78, 11, 81, 1]}


def set_color(coord, color, form=''):
    sc = sct_color()
    if color:
        c = convert_xyt(coord)
        sc['color'] = color
        sc['size'] = c['size']
        sc['pos'] = c['pos']
        if form:
            sc['form'] = form
    return sc


def btn_colors(key):
    btn = {
        'btr': [78, 11, 81, 1],
        'btk': [2, 54, 112, 1],
        'btv': [0, 52, 73, 1],
        'bti': [2, 54, 112, 1],
        'prt': [29, 79, 118, 1],
        'sref': [29, 79, 118, 1]}
    return btn[key]


# Screen Colors
# config = [212, 192, 182, 1]
c1 = [109, 72, 39, 1]
c2 = [37, 84, 109, 1]


def scr_cols(scr):

    var_cols = {
        'init': {
            'title': pallete[str(6)],
            'brev': pallete[str(8)],
            'opt': pallete[str(11)],
            'config': pallete[str(11)]},
        'brev': {
            'grd': pallete[str(6)],
            'manual': [147, 89, 31, 1],
            'scy': [14, 78, 89, 1],
            'btr': btn_colors('btr')},
        'scy': {
            'btr': btn_colors('btr')},
        'grd': {
            'btr': btn_colors('btr')},
        'manual': {
            'btr': btn_colors('btr')},
        'opt': {
            'login': pallete[str(6)],
            'play': pallete[str(6)],
            'btr': btn_colors('btr')},
        'login': {
            'key': pallete[str(6)],
            'input': [1, 1, 1, 1],
            'ops': [],
            'btr': btn_colors('btr'),
            'btk': btn_colors('btk'),
            'btv': btn_colors('btv')},
        'pregame': {
            'bts': [],
            'btr': btn_colors('btr'),
            'bti': [145, 98, 57, 1]},
        'pretask': {
            'initask': [],
            'bti': [145, 98, 57, 1],
            'btr': [108, 112, 233, 1]
        }}

    return var_cols[scr]


def sda_colors(scr, sct):
    col = {}
    obj_cols = scr_cols(scr)
    for k in sct:
        col[k] = sct_color()
        col[k]['color'] = obj_cols[k]
        xy = sct[k]['xyt']
        col[k]['size'] = xy['size']
        col[k]['pos'] = xy['pos']

    if scr == 'init':
        for k in ['opt', 'brev', 'config']:
            col[k]['form'] = 'ellipse'

    if scr == 'brev':
        for k in col:
            col[k]['form'] = 'ellipse'

    if scr == 'login':
        for k in ['btr', 'btk', 'btv']:
            col[k]['form'] = 'ellipse'

    if 'btr' in col:
        col['btr']['form'] = 'ellipse'

    if 'bti' in col:
        col['bti']['form'] = 'ellipse'

    return col
