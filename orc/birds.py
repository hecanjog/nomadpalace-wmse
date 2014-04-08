from pippi import dsp
from pippi import tune
from pippic.settings import get_param as p
from pippic.settings import voice as vp
from pippic.settings import shared
import orange as bot

shortname   = 'bi'
name        = 'birds'

def play(voice_id):
    tel = bot.getTel()

    b = dsp.read('sounds/birds.wav').data

    b = dsp.split(b, dsp.randint(100, 1000))

    b = b[:dsp.randint(len(b) / 10, len(b))]

    blen = len(b)

    pans = dsp.breakpoint([ dsp.rand() for i in range(dsp.randint(10, 100)) ], blen)
    speeds = dsp.breakpoint([ dsp.rand(0.25, 1.5) for i in range(dsp.randint(10, 100)) ], blen)
    amps = dsp.breakpoint([ dsp.rand(0.05, 1.5) for i in range(dsp.randint(10, 100)) ], blen)

    b = [ dsp.pan(b[i], pans[i]) for i in range(blen) ]
    b = [ dsp.transpose(b[i], speeds[i]) for i in range(blen) ]
    b = [ dsp.amp(b[i], amps[i]) for i in range(blen) ]

    b = dsp.packet_shuffle(b, dsp.randint(4, 30))

    for i, bb in enumerate(b):
        if dsp.rand(0, 100) > 60:
            b[i] = bb * dsp.randint(2, 10)

    out = ''.join(b)

    dsp.log('')
    dsp.log('birds')
    dsp.log(blen)
    dsp.log('%s length: %.2f' % (voice_id, dsp.fts(dsp.flen(out))))
    bot.show_telemetry(tel)

    return out

