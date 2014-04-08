from pippi import dsp
from pippi import tune
from pippic.settings import get_param as p
from pippic.settings import voice as vp
from pippic.settings import shared
import blue as bot

shortname   = 'sh'
name        = 'shimmer'

def play(voice_id):
    tel = bot.getTel()

    degrees = [ dsp.randchoose([1, 2, 3, 4, 5, 6, 7, 8]) for f in range(dsp.randint(2, 6)) ]

    octave = dsp.randint(1, 4)

    freqs = tune.fromdegrees(degrees, root='c', octave=octave, ratios=tune.just)

    out = ''

    freq = dsp.randchoose(freqs)
    volume = dsp.rand(0.5, 0.8)
    length = dsp.randint(dsp.mstf(20), dsp.mstf(30))

    for p in range(dsp.randint(20, 100)):

        pulsewidth = dsp.rand(0.5, 1)

        mod = dsp.breakpoint([ dsp.rand(0, 1) for b in range(4) ], 512)
        window = dsp.breakpoint([0] + [ dsp.rand(0, 1) for b in range(10) ] + [0], 512)
        waveform = dsp.breakpoint([0] + [ dsp.rand(-1, 1) for b in range(20) ] + [0], 512)

        modRange = 0.01
        modFreq = dsp.rand(0.0001, 5)

        t = dsp.pulsar(freq, length, pulsewidth, waveform, window, mod, modRange, modFreq, volume)

        t = dsp.pad(t, 0, length * 3)

        t = dsp.env(t, 'sine')

        out += t

    out = dsp.env(out, 'sine')
    out = dsp.pan(out, dsp.rand(0, 1))

    dsp.log('')
    dsp.log('drone')
    dsp.log('%s length: %.2f' % (voice_id, dsp.fts(dsp.flen(out))))
    bot.show_telemetry(tel)

    return out

