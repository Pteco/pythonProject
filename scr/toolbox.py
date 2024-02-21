from os.path import join
from numpy import ceil
from math import sqrt
import json
from kivy.core.audio import SoundLoader
from libPaths import Paths
from kivy.metrics import dp


def manager(act, data=None):

    file = join(Paths().data()['current'], 'scr_size.json')

    if act == 'read':
        with open(file, 'r') as outfile:
            data = json.load(outfile)
    if act == 'write':
        with open(file, 'w') as outfile:
            json.dump(data, outfile, ensure_ascii=False)
    return data


def scr_size():
    return manager('read')


def inv_mat(mt):
    i = []
    nn = -1
    for _ in mt:
        i.append(mt[nn])
        nn -= 1
    return i


def files2sound(files):
    sound = []
    duration = []
    for f in files:
        sound.append(SoundLoader.load(f))
        duration.append(sound[-1].length)
    return sound, duration


def file2sound(file):
    sound = SoundLoader.load(file)
    duration = sound.length
    return sound, duration


def xyt_sequence(var):
    sq, seq = [], []
    dx, dy = 0, 0
    if var['dist_x'] > 0:
        dx = var['dist_x'] - var['start_point'][0]

    if var['dist_y'] > 0:
        dy = var['dist_y'] - var['start_point'][1]

    p0 = var['start_point'].copy()
    for n in range(var['mat'][0]):
        for nn in range(var['mat'][1]):
            sq.append(p0.copy())
            sq[-1].extend(var['size'])
            p0[0] += dx
        p0[1] += dy
        p0[0] = var['start_point'].copy()[0]
    for q in sq:
        seq.append(convert_xyt(q))

    return seq


def hint(varin):
    varout = []
    n = 0
    for v in varin:
        varout.append(float('{:.6f}'.format(v / scr_size()[n])))
        n += 1
    return varout


def size_pos(coord):
    size, pos = [], []
    if coord:
        size = [dp(coord[2]), dp(coord[3])]
        pos = [int(dp(coord[0])),
               int(scr_size()[1] - (dp(coord[1]) + dp(coord[3])))]
    return size, pos


def degree(dct):
    x = dp(dct['cnt'][0]) - dp(dct['pos'][0])
    y = dp(dct['cnt'][1]) - dp(dct['pos'][1])

    radius = int(ceil(sqrt(x * x + y * y)))
    return radius


def convert_xyt(coord):
    var = {}
    if coord:
        s = [dp(coord[2]), dp(coord[3])]
        p = [dp(int(coord[0])),
             dp(int(scr_size()[1] - (coord[1] + coord[3])))]
        sh = [s[0] / scr_size()[0], s[1] / scr_size()[1]]
        ph = [p[0] / scr_size()[0], p[1] / scr_size()[1]]
        var['size'] = [int(sh[0] * scr_size()[0]),
                       int(sh[1] * scr_size()[1])]
        var['pos'] = [int(ph[0] * scr_size()[0]),
                      int(ph[1] * scr_size()[1])]
        var['size_hint'] = [float('{:.4f}'.format(sh[0])),
                            float('{:.4f}'.format(sh[1]))]
        var['pos_hint'] = [float('{:.4f}'.format(ph[0])),
                           float('{:.4f}'.format(ph[1]))]

    return cnt_xyt(var)


def cnt_xyt(xyt):
    cnt = [xyt['pos'][0] + (xyt['size'][0]/2),
           xyt['pos'][1] + (xyt['size'][1]/2)]
    ch = [cnt[0] / scr_size()[0],
          cnt[1] / scr_size()[1]]
    xyt['cnt_hint'] = [float('{:.4f}'.format(ch[0])),
                       float('{:.4f}'.format(ch[1]))]
    ct = [ch[0] * scr_size()[0],
          ch[1] * scr_size()[1]]
    xyt['cnt'] = [int(dp(ct[0])), int(dp(ct[1]))]
    return xyt


def name2sound(effectname):
    from libPaths import Paths
    f = join(Paths().assets()['aud_eft'], '{}.wav'.format(effectname))
    return SoundLoader.load(f)


def audinit():
    aud = name2sound('gup')
    aud.volume = 0
    aud.play()


def op_direction(idx: str):
    d = {
        'down': 'up',
        'up': 'down',
        'left': 'right',
        'right': 'left'
    }
    return d[idx]


scr_points = {
    'player': {
        '1': {
            'h1': ['left'],
            'h2': [],
            'v1': [],
            'v2': ['up']}},

    'pregame': {
        '1': {
            'h1': [],
            'h2': ['left'],
            'v1': ['down'],
            'v2': ['up']}},

    'pretask': {
        '1': {
            'h1': ['right'],
            'h2': ['left'],
            'v1': [],
            'v2': ['down']},
        '2': {
            'h1': ['left'],
            'h2': ['right'],
            'v1': [],
            'v2': ['down']}},

    'sqrtx': {
        '1': {
            'h1': ['right'],
            'h2': [],
            'v1': ['up'],
            'v2': []}},

    'rectmask': {
        '1': {
            'h1': ['left'],
            'h2': [],
            'v1': [],
            'v2': ['down']}},

    'rectav': {
        '1': {
            'h1': [],
            'h2': ['right'],
            'v1': [],
            'v2': ['down', 'up']}},
}


def paths_direction(start_scr, end_scr):
    spt = {
        'start': start_scr,
        'end': end_scr,
        'direction': '',
        'vector': '',
        'start_version': '',
        'end_version': ''}
    script = []

    sc = scr_points[start_scr]
    sn = scr_points[end_scr]

    for nc in sc:
        for k in sc[nc]:
            if sc[nc][k]:
                for nt in sn:
                    for kk in sn[nt]:
                        if sn[nt][kk]:
                            if k == kk:
                                for s in sn[nt][kk]:
                                    if op_direction(s) in sc[nc][k]:
                                        sp = spt.copy()
                                        sp['direction'] = s
                                        sp['vector'] = k
                                        sp['start_version'] = nc
                                        sp['end_version'] = nt
                                        script.append(sp)
                                        break
    return script


def sct_return():
    sct = {
        'direction': '',
        'destiny': ''}
    return sct
