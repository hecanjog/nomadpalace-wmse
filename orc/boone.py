from pippi import dsp
from pippi import tune
from pippic.settings import get_param as p
from pippic.settings import voice as vp
from pippic.settings import shared
import geodes as bot

shortname   = 'bo'
name        = 'boone'

def play(voice_id):
    tel = bot.getTel()

    freqs = tune.fromdegrees([ dsp.randchoose([1, 2, 3, 5, 6, 8]) for f in range(dsp.randint(2, 5)) ], root='c', octave=dsp.randint(1, 3), ratios=tune.just)

    out = ''

    for freq in freqs:
        waveform = dsp.randchoose(['tri', 'sine2pi'])
        length = dsp.randint(dsp.mstf(10), dsp.mstf(300))
        #length = dsp.mstf(150)
        pulsewidth = dsp.rand()

        mod = dsp.breakpoint([ dsp.rand() for b in range(int(round(tel['density'])) + 3) ], 512)
        window = dsp.breakpoint([0] + [ dsp.rand() for b in range(int(round(tel['harmonicity'] * 2)) + 3) ] + [0], 512)
        waveform = dsp.breakpoint([0] + [ dsp.rand(-1, 1) for b in range(int(round(tel['roughness'] * 3)) + 3) ] + [0], 512)

        modRange = 0.005
        modFreq = dsp.rand(0.0001, 5)

        volume = dsp.rand(0.2, 0.3)

        if dsp.rand(0, 100) > 50:
            t = dsp.pulsar(freq, length, pulsewidth, waveform, window, mod, modRange, modFreq, volume)
        else:
            t = dsp.tone(length, freq, waveform)

        #t = dsp.pulsar(freq, length, pulsewidth, waveform, window, mod, modRange, modFreq, volume)
        #t = dsp.tone(length, freq, waveform)

        t = dsp.pan(t, dsp.rand())
        t = dsp.alias(t)

        t = dsp.amp(t, dsp.rand(0.5, 5.0))

        t = dsp.pad(t, 0, dsp.randint(dsp.mstf(1), dsp.mstf(500)))
        #t = dsp.pad(t, 0, dsp.mstf(100))
        t = dsp.amp(t, dsp.rand(0.5, 0.75))

        #out += dsp.env(t, 'sine')
        out += t

    #out = dsp.env(t, 'sine')

    dsp.log('')
    dsp.log('boone')
    dsp.log('%s length: %.2f' % (voice_id, dsp.fts(dsp.flen(out))))
    bot.show_telemetry(tel)

    return out

