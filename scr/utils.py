from libPaths import Paths
from scr.toolbox import convert_xyt


btn_folder = Paths().assets()['buttons']
scr_folder = Paths().assets()['settings']
spx_folder = Paths().assets()['spx']
aud_eft_folder = Paths().assets()['aud_eft']

cod = 3


def sbkg_color():
    return [[63, 0, 96, 1], [0, 52, 73, 1],  [84, 4, 88, 1]]


def cxs_colors():
    cols = {
        '0': [145, 98, 57, 1],
        '1': [91, 42, 42, 1],
        '2': [2, 54, 112, 1],
        '3': [33, 110, 102, 1],
        '4': [64, 37, 156, 1],
        '5': [108, 112, 233, 1],
        '6': [171, 70, 158, 1],
        '7': [145, 98, 57, 1],
        'ref': ['laranja',
                'vermelho',
                'azul',
                'verde',
                'azul claro',
                'azul mais claro',
                'rosa',
                'laranja'],
    }
    return cols


def scr_colors(scr):

    cols = {
        'pregame': [
            [1, 2, 0], [2, 0, 1], [1, 0, 2],
            [0, 2, 1], [2, 1, 0], [0, 1, 2]],

        'game': [
            [1, 0], [2, 1], [1, 2],
            [0, 1], [2, 0], [0, 2]],

        'gamesim': [
            [1, 0], [2, 1], [1, 2],
            [0, 1], [2, 0], [0, 2]]}
    return cols[scr][cod]


def pregame():
    data = {
        'xyt': [
            [[0, 0, 839, 114], [0, 114, 111, 546], [461, 114, 379, 211],
             [634, 323, 124, 129], [111, 551, 150, 109]],
            [[843, 0, 77, 103], [886, 103, 34, 290], [759, 393, 161, 63],
             [636, 456, 284, 48], [635, 503, 214, 96]],
            [[112, 115, 345, 341], [113, 455, 520, 95], [263, 550, 370, 110],
             [633, 601, 287, 59], [852, 506, 68, 95]]],
        'cxs': [
            [[59, 49, 194, 65], [59, 114, 52, 169]],
            [[462, 254, 170, 198]],
            [[842, 106, 44, 220], [761, 326, 124, 66]]]}

    return data


def game():
    data = {
        'xyt': [
            [[0, 0, 262, 50], [0, 50, 32, 610],
             [32, 635, 888, 25], [325, 602, 267, 33], [878, 119, 42, 516]],
            [[262, 0, 658, 51], [32, 50, 888, 71], [32, 118, 844, 480],
             [32, 598, 292, 35], [595, 598, 281, 35]]],
        'cxs': []}

    return data


def gamesim():
    data = {
        'xyt': [
            [[0, 0, 262, 69],
             [0, 69, 93, 591],
             [93, 501, 827, 159],
             [309, 476, 198, 25], [717, 121, 203, 380]],

            [[263, 0, 657, 70], [92, 70, 828, 51],
             [92, 121, 624, 355], [92, 476, 216, 25],
             [507, 476, 209, 25]]],
        'cxs': []}

    return data


def scr_cxs(scr):
    cols = {
        'pregame': [2, 1, 3],
        'game': []}
    return cols[scr]


def rand_color():
    return 2


def convert_cod(_):
    pass


def sct_color() -> object:
    sct = {
        'color': [],
        'size': [],
        'pos': [],
        'form': 'rectangle'}
    return sct


def uni_sbkg(coord, color):
    sbkg = sct_color()
    sbkg['color'] = color
    st = convert_xyt(coord)
    sbkg['size'] = st['size']
    sbkg['pos'] = st['pos']
    return sbkg


def mk_sbkg(xyt, color):
    sbkg = []
    for xy in xyt:
        sbkg.append(uni_sbkg(xy, color))
    return sbkg


def compose_sbkg(scr, vcod):
    mth = eval(scr)
    xyt = mth()

    sbkg = []
    n = 0
    for xy in xyt['xyt']:

        sbkg.extend(mk_sbkg(xy, sbkg_color()[vcod[1][n]]))
        n += 1
    if xyt['cxs']:
        n = 0
        for xy in xyt['cxs']:
            sbkg.extend(mk_sbkg(xy, cxs_colors()[str(scr_cxs(scr)[n])]))
            n += 1

    return sbkg
