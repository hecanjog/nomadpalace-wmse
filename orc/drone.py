from pippi import dsp
from pippi import tune
from pippic.settings import get_param as p
from pippic.settings import voice as vp
from pippic.settings import shared
import blue as bot

shortname   = 'dr'
name        = 'drone'

def play(voice_id):
    tel = bot.getTel()

    degrees = [ dsp.randchoose([1, 2, 3, 4, 5, 6, 7, 8]) for f in range(dsp.randint(2, 6)) ]

    octave = dsp.randint(1, 5)

    freqs = tune.fromdegrees(degrees, root='c', octave=octave, ratios=tune.just)

    out = ''

    for freq in freqs:
        length = dsp.randint(dsp.stf(4), dsp.stf(12))

        pulsewidth = dsp.rand(0.5, 1)

        mod = dsp.breakpoint([ dsp.rand(0, 1) for b in range(4) ], 512)
        window = dsp.breakpoint([0] + [ dsp.rand(0, 1) for b in range(4) ] + [0], 512)
        waveform = dsp.breakpoint([0] + [ dsp.rand(-1, 1) for b in range(4) ] + [0], 512)

        modRange = 0.01
        modFreq = dsp.rand(0.0001, 5)

        volume = dsp.rand(0.6, 1)

        t = dsp.pulsar(freq, length, pulsewidth, waveform, window, mod, modRange, modFreq, volume)

        t = dsp.pan(t, dsp.rand())

        t = dsp.amp(t, dsp.rand(0.5, 1.0))

        t = dsp.env(t, 'sine')

        out += t


    dsp.log('')
    dsp.log('drone')
    dsp.log('%s length: %.2f' % (voice_id, dsp.fts(dsp.flen(out))))
    bot.show_telemetry(tel)

    return out

