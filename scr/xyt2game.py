from os.path import join

from scr.toolbox import convert_xyt, degree, size_pos, \
    hint, xyt_sequence
from scr.utils import btn_folder, spx_folder, scr_folder
from scr.map_color import sct_color, uni_col

sct_atv = {}

colors_pk = {
    'violet': [58 / 255, 0, 84 / 255, 1],
    'dark_blue': [0, 29 / 255, 73 / 255, 1],
    'dark_violet': [51 / 255, 0, 74 / 255, 1],
    'aqua_blue': [2, 54, 112, 1],
    'green_blue': [0, 52 / 255, 73 / 255, 1]}


def mat_card(s, x, y):
    mat = []
    nt = 0
    for nn in y:
        mat.append([])
        for n in x:
            mat[nt].append([n, nn])
            mat[nt][-1].extend(s)
        nt += 1
    return mat


def sct_players(data):
    sct = sct_atv.copy()
    for n in [1, 2]:
        tk = {}
        sct['player{}'.format(n)] = {}
        for k in data['player{}'.format(n)]:
            tk[k] = {'size': data['player{}'.format(n)][k][0][2:],
                     'size_hint': [], 'pos': [], 'pos_hint': []}
            tk[k]['size_hint'] = hint(tk[k]['size'])

            for crd in data['player{}'.format(n)][k]:
                cv = convert_xyt(crd)
                tk[k]['pos'].append(cv['pos'])
                tk[k]['pos_hint'].append(cv['pos_hint'])

            if k == 'btn':
                tk[k]['pos_hint'] = tk[k]['pos_hint'][0]
                tk[k]['pos'] = []
            sct['player{}'.format(n)] = tk
    return sct


def xyt_cols(coord, col):
    sct = sct_color()
    sct['color'] = col
    sd = convert_xyt(coord)
    sct['size'] = sd['size']
    sct['pos'] = sd['pos']
    return sct


def gm_sbkg(col):
    sbkg = []
    xyt = [
        [0, 0, 262, 34],
        [0, 32, 22, 593],
        [0, 625, 920, 35],
        [322, 590, 271, 38],
        [899, 125, 21, 502]]

    for xy in xyt:
        sbkg.append(xyt_cols(xy, col))

    return sbkg


def xyt_tkn():
    st = [58, 58]
    tkn1 = []
    for t in [[137, 174], [59, 174], [59, 97]]:
        tkn1.append(t)
        tkn1[-1].extend(st)
    tkn2 = []
    for t in [[137, 470], [59, 470], [60, 547]]:
        tkn2.append(t)
        tkn2[-1].extend(st)
    return tkn1, tkn2


def xyt_simtkn():
    st = [43, 43]
    tkn1 = []
    for t in [[169, 160], [112, 160], [112, 103]]:
        tkn1.append(t)
        tkn1[-1].extend(st)
    tkn2 = []
    for t in [[169, 378], [112, 378], [112, 436]]:
        tkn2.append(t)
        tkn2[-1].extend(st)
    return tkn1, tkn2


def gm_color(cnd, coords, data=None):
    if data is None:
        data = []
    cx_col = [57, 1, 61, 1]
    data.append(xyt_cols(coords[0], cx_col))
    data.append(xyt_cols(coords[1], cx_col))
    tkn_col = [0, 29, 73, 1]

    if cnd == 'sim':
        tkn1, tkn2 = xyt_simtkn()
    else:
        tkn1, tkn2 = xyt_tkn()

    for tk in tkn1:
        data.append(xyt_cols(tk, tkn_col))
    for tk in tkn2:
        data.append(xyt_cols(tk, tkn_col))

    return data


def gm_files():
    files = {
        'set': join(scr_folder, 'game.png'),
        'dealer': join(spx_folder, 'dealer.png'),
        'btn_turn': {
            'on': join(btn_folder, 'btn_turn_on.png'),
            'off': join(btn_folder, 'btn_turn_off.png')},
        'btn_pass': {
            'on': join(btn_folder, 'btn_pass_on.png'),
            'eft': join(btn_folder, 'btn_pass_eft.png')},
        'btr': join(btn_folder, 'btr_on.png'),
        'tks': []}

    for n in range(12):
        files['tks'].append(
            join(spx_folder, 't{}.png'.format(n)))

    return files


def pop_up():
    psda = {
        'win': {
            'xyt': convert_xyt([277, 259, 360, 185]),
            'col': sct_color(),
            'file': join(spx_folder, 'pop_up.png')},
        'btn': {
            'sda': convert_xyt([508, 283, 95, 95]),
            'cont': convert_xyt([313, 283, 95, 95])}}
    cs, cp = size_pos([285, 271, 344, 165])
    psda['win']['col']['color'] = colors_pk['violet']
    psda['win']['col']['focus'] = 'bkg'
    psda['win']['col']['size'] = cs
    psda['win']['col']['pos'] = cp
    psda['win']['col']['form'] = 'rectangle'
    return psda


def game():
    """ matcard [  [ size ], [ X ], [ Y ] ]"""
    sct = sct_atv.copy()

    crd = mat_card([104, 104], [237, 352, 464, 578], [117, 479])
    btn = mat_card([67, 67], [778], [194, 443])
    tkn1, tkn2 = xyt_tkn()

    data = {
        'player1': {'card': crd[0], 'btn': btn[0], 'tkn': tkn1},
        'player2': {'card': crd[1], 'btn': btn[1], 'tkn': tkn2}}
    sct['xyt'] = sct_players(data)

    sct['xyt']['btn_pass'] = convert_xyt([663, 306, 85, 85])
    sct['xyt']['dealer'] = convert_xyt([53, 287, 130, 130])
    btr = [134, 18, 65, 65]
    sct['xyt']['btr'] = convert_xyt(btr)
    sct['xyt']['btr']['color'] = [1, 7, 123, 1]
    sct['xyt']['btr']['form'] = 'ellipse'
    sct['xyt']['btw'] = convert_xyt([399, 293, 122, 122])
    sct['xyt']['btw']['file'] = join(btn_folder, 'btn_click.png')

    sct['xyt']['release'] = convert_xyt([406, 298, 104, 104])
    sct['xyt']['release']['radius'] = degree(sct['xyt']['release'])
    vlim = convert_xyt([24, 36, 871, 584])
    sct['xyt']['lim'] = [
        vlim['pos'][0], vlim['pos'][1],
        vlim['size'][0], vlim['size'][1]]

    sct['pop_up'] = pop_up()
    sct['files'] = gm_files()
    sct['n_cards'] = 4
    sct['level'] = 0
    sct['colors'] = gm_color('', [[226, 103, 467, 129], [226, 467, 467, 129]])
    sct['sbkg'] = gm_sbkg([72, 2, 86, 1])

    return sct


sct_xyt_seq = {
    'start_point': [],
    'dist_x': 0,
    'dist_y': 0,
    'size': [],
    'mat': []}


def cardfilessim():
    cols = []
    f = 'b'
    for cn in [[0, 3, 1, 2], [3, 0, 2, 1]]:
        for c in cn:
            cols.append(join(spx_folder, '{}{}.png'.format(f, c)))
            if f == 'b':
                f = 'c'
            else:
                f = 'b'
    ct = []
    f = 'd'
    for cn in [[2, 1, 3, 0], [1, 2, 0, 3]]:
        for c in cn:
            ct.append(join(spx_folder, '{}{}.png'.format(f, c)))
            if f == 'd':
                f = 'a'
            else:
                f = 'd'
    cols.extend(ct)
    cols.append(join(spx_folder, 'y.png'))
    return cols


def game_sim():
    """ matcard [  [ size ], [ X ], [ Y ] ]"""

    crd = mat_card([75, 75], [242, 327, 410, 495], [120, 387])
    btn = mat_card([61, 61], [638], [176, 347])
    tkn1, tkn2 = xyt_simtkn()

    data = {
        'player1': {'card': crd[0], 'btn': btn[0], 'tkn': tkn1},
        'player2': {'card': crd[1], 'btn': btn[1], 'tkn': tkn2}}
    dts = sct_players(data)
    sct = {'player': [dts['player1'], dts['player2']], 'xyt': {}}

    sct['xyt']['btn_pass'] = convert_xyt([570, 255, 61, 61])
    sct['xyt']['dealer'] = convert_xyt([110, 235, 102, 102])
    sct['xyt']['release'] = convert_xyt([364, 254, 75, 75])
    sct['xyt']['release']['radius'] = degree(sct['xyt']['release'])
    sct['xyt']['btr'] = convert_xyt([787, 32, 47, 47])
    sct['xyt']['btr']['color'] = [1, 7, 123, 1]
    sct['xyt']['btr']['form'] = 'ellipse'

    fcs = sct_xyt_seq.copy()
    fcs['start_point'] = [96, 511]
    fcs['size'] = [57, 57]
    fcs['dist_x'] = 175
    fcs['dist_y'] = 587
    fcs['mat'] = [2, 8]
    fr = xyt_sequence(fcs)

    scoin = 70
    xc = 5
    coins = []
    for y in [50, 140, 230, 320, 410]:
        coins.append(convert_xyt([xc, y, scoin, scoin]))
    sd = 88
    xd = 777
    demo = []
    for y in [153, 262, 371, 480]:
        demo.append(convert_xyt([xd, y, sd, sd]))

    fc_card = []
    for c in ['color', 'form']:
        for n in range(4):
            fc_card.append([c, n])

    coord_inst = [
        [174, 176, 468, 254], [317, 330, 168, 168], [273, 251, 271, 186],
        [297, 107, 207, 207], [529, 194, 368, 226], [732, 182, 176, 290],
        [498, 212, 370, 151], [492, 198, 192, 192], [315, 476, 173, 107],
        [724, 276, 188, 211], [75, 476, 653, 160], [179, 521, 443, 119],
        [34, 511, 744, 124], [282, 521, 580, 124], [727, 161, 184, 290],
        [89, 498, 628, 161], [734, 184, 168, 211], [733, 188, 168, 211],
        [85, 504, 640, 151], [100, 519, 593, 126], [94, 503, 601, 152],
        [228, 214, 363, 154]]

    ct = [145 / 255, 98 / 255, 57 / 255, 1]

    forms = [
        'ellipse', 'ellipse', 'rectangle',
        'ellipse', 'ellipse', 'rectangle',
        'ellipse', 'ellipse', 'rectangle',
        'rectangle', 'rectangle', 'rectangle',
        'rectangle', 'rectangle', 'rectangle',
        'rectangle', 'rectangle', 'rectangle',
        'rectangle', 'rectangle', 'ellipse', 'rectangle']
    xyt_inst = []
    n = 0
    for crd in coord_inst:
        xyt_inst.append(convert_xyt(crd))
        xyt_inst[-1]['col'] = ct
        xyt_inst[-1]['file'] = join(spx_folder, 'inst{}.png'.format(n))
        xyt_inst[-1]['form'] = forms[n]
        n += 1

    sct['setting'] = {
        'formcolors': fr,
        'y': convert_xyt([771, 520, 101, 101]),
        'coins': coins,
        'demo': demo,
        'mix': convert_xyt([123, 247, 78, 78]),
        'instructions': xyt_inst,
        'manip_card': fc_card,
        'dist': [[3, 11, 8, 15], [0, 5, 16, 9]]}
    point = []
    point_size = [85, 104]
    point_positions = [[283, 266], [371, 266], [369, 266], [457, 266]]
    n = 0
    for ff in ['point_right.gif', 'point_left.gif']:
        for _ in range(2):
            pos = point_positions[n]
            pos.extend(point_size)
            point.append(convert_xyt(pos))
            point[-1]['file'] = join(spx_folder, ff)
            n += 1
    sct['setting']['point'] = point

    sct['btn_return'] = convert_xyt(coord_inst[-1])
    sct['btn_return']['file'] = join(spx_folder, 'gm_return.png')
    sct['btn_return']['col'] = uni_col(coord_inst[-1], [145, 98, 57, 1])
    sct['btn_return']['col']['form'] = 'ellipse'

    sct['files'] = gm_files()
    sct['files']['set'] = join(scr_folder, 'game_sims.png')
    sct['files']['tks'] = []
    for n in [0, 3, 4, 6, 12]:
        sct['files']['tks'].append(join(spx_folder, 't{}.png'.format(n)))
    sct['files']['card'] = cardfilessim()
    sct['files']['cnx'] = [join(spx_folder, 'cnx{}.png'.format(i)) for i in range(2)]
    sct['files']['point'] = [
        join(spx_folder, 'point_left.gif'), join(spx_folder, 'point_right.gif')
    ]
    sct['colors'] = gm_color('sim', [[236, 107, 344, 97], [236, 376, 344, 97]])
    sct['sbkg'] = gm_sbkg([72, 2, 86, 1])

    return sct
