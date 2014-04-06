from pippi import dsp
from pippi import tune
from pippic.settings import get_param as p
from pippic.settings import voice as vp
from pippic.settings import shared
import orange as bot

shortname   = 'bo'
name        = 'boone'

def play(voice_id):
    tel = bot.getTel()

    degrees = [ dsp.randchoose([1, 2, 3, 5, 6, 8]) for f in range(dsp.randint(2, 100)) ]
    degrees = [ dsp.randchoose([1, 5, 6, 7, 8]) for f in range(dsp.randint(2, 10)) ]

    octave = dsp.randint(2, 3)
    octave = 1

    freqs = tune.fromdegrees(degrees, root='c', octave=octave, ratios=tune.just)

    out = ''

    for freq in freqs:
        waveform = dsp.randchoose(['tri', 'sine2pi'])

        length = dsp.randint(dsp.mstf(5), dsp.mstf(60))
        length = dsp.mstf(1500)
        length = dsp.mstf(2500)

        pulsewidth = dsp.rand(0.01, 1)

        mod = dsp.breakpoint([ dsp.rand() for b in range(int(round(tel['density'])) + 3) ], 512)
        window = dsp.breakpoint([0] + [ dsp.rand() for b in range(int(round(tel['harmonicity'] * 2)) + 3) ] + [0], 512)
        waveform = dsp.breakpoint([0] + [ dsp.rand(-1, 1) for b in range(int(round(tel['roughness'] * 3)) + 3) ] + [0], 512)

        modRange = 0.05
        modFreq = dsp.rand(0.0001, 5)

        #volume = dsp.rand(0.2, 0.3) * (tel['density'] / 10.0)
        volume = dsp.rand(0.2, 0.8)

        t = dsp.pulsar(freq, length, pulsewidth, waveform, window, mod, modRange, modFreq, volume)
        #t = dsp.tone(length, freq, waveform)

        t = dsp.pan(t, dsp.rand())

        t = dsp.alias(t)

        t = dsp.amp(t, dsp.rand(0.5, 1.0))

        #t = dsp.pad(t, 0, dsp.randint(dsp.mstf(1), dsp.mstf(150)))

        t = dsp.amp(t, dsp.rand(0.5, 0.95))

        #t = dsp.env(t, 'sine')
        t = dsp.env(t, 'phasor')

        #t = dsp.pine(t, dsp.flen(t) * 4, freq)

        out += t


    dsp.log('')
    dsp.log('boone')
    dsp.log('%s length: %.2f' % (voice_id, dsp.fts(dsp.flen(out))))
    bot.show_telemetry(tel)

    return out

