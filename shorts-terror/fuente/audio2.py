# Diseño de sonido sintetizado y sincronizado con <video>_cues.json. Uso: audio2.py v7
import json, sys, os, wave, numpy as np
here = os.path.dirname(os.path.abspath(__file__)); v = sys.argv[1]
D = json.load(open(os.path.join(here, f'{v}_cues.json'))); cues = D['cues']; DUR = float(D['dur'])
SR = 48000; N = int(SR * DUR); t = np.arange(N) / SR
rng = np.random.default_rng(11)
L = np.zeros(N); R = np.zeros(N)

def bandpass(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    m = np.convolve(((f >= lo) & (f <= hi)).astype(float), np.ones(41) / 41, 'same')
    return np.fft.irfft(X * m, len(x))
def add(sig, at, gain=1.0, pan=0.0):
    i = int(at * SR); sig = sig[: max(0, N - i)]
    if i < 0 or len(sig) == 0: return
    L[i:i + len(sig)] += sig * gain * (1 - max(pan, 0)); R[i:i + len(sig)] += sig * gain * (1 + min(pan, 0))
def env(n, a, d):
    e = np.ones(n); na = max(1, int(a * SR)); e[:na] = np.linspace(0, 1, na); return e * np.exp(-np.arange(n) / SR / d)
def seg(a, b): return (t >= a) & (t < b)

# ---------- cama ----------
gate = np.ones(N)
for c in cues:
    if c['type'] == 'silence':
        a, b = int(c['t'] * SR), int(c['end'] * SR); gate[max(0, a - 2400):a] = np.linspace(1, 0, min(2400, a)); gate[a:b] = 0
lfo = 0.75 + 0.25 * np.sin(2 * np.pi * 0.09 * t)
drone = (np.sin(2*np.pi*41.2*t) + .8*np.sin(2*np.pi*41.7*t) + .5*np.sin(2*np.pi*61.74*t+1) + .25*np.sin(2*np.pi*82.6*t)) * lfo
brown = np.cumsum(rng.normal(0, 1, N)); brown -= np.convolve(brown, np.ones(4801)/4801, 'same'); brown /= np.abs(brown).max()
bed = drone * .15 + brown * .09
kind = next((c['kind'] for c in cues if c['type'] == 'bed'), 'drone')
if kind == 'forest':
    wind = bandpass(rng.normal(0, 1, N), 200, 1400); wind /= np.abs(wind).max()
    bed += wind * (0.5 + 0.5 * np.sin(2*np.pi*0.07*t) ** 2) * .09
    for k in range(int(DUR / 3)):  # grillos lejanos
        at = k * 3 + rng.uniform(0, 2); n = int(SR * .6); x = np.arange(n) / SR
        add(np.sin(2*np.pi*4300*x) * (np.sin(2*np.pi*28*x) > .2) * np.sin(np.pi*x/.6) * .02, at, 1, pan=rng.uniform(-.8, .8))
elif kind == 'arcade':
    hum = np.sin(2*np.pi*60*t) * .03 + bandpass(rng.normal(0, 1, N), 300, 3000) * .012
    bed += hum
    notes = [220, 277, 330, 440, 330, 277]
    for k in range(int(DUR * 2)):  # pitidos de otras máquinas
        if rng.random() < .55:
            at = k / 2 + rng.uniform(0, .3); n = int(SR * .09); x = np.arange(n) / SR; f = notes[rng.integers(len(notes))] * rng.choice([1, 2])
            add(np.sign(np.sin(2*np.pi*f*x)) * env(n, .002, .05) * .025, at, 1, pan=rng.uniform(-.9, .9))
elif kind == 'tape':
    hiss = bandpass(rng.normal(0, 1, N), 2000, 12000); hiss /= np.abs(hiss).max()
    bed += hiss * .035 + np.sin(2*np.pi*50*t) * .015
    bed *= 1 + .04 * np.sin(2*np.pi*.6*t)
L += bed * gate; R += bed * gate * .96

# ---------- efectos ----------
def hit(big=True):
    n = int(SR * (1.6 if big else .9)); x = np.arange(n) / SR; f = 30 + (95 if big else 70) * np.exp(-x * 7)
    s = np.sin(2*np.pi*np.cumsum(f)/SR) * env(n, .003, .55 if big else .3) + rng.normal(0, 1, n) * np.exp(-x*40) * (.35 if big else .2)
    return np.tanh(s * 1.6)
def glitch():
    n = int(SR * .26); s = np.round(rng.normal(0, 1, n) * 4) / 4; s *= (np.sin(2*np.pi*37*np.arange(n)/SR) > 0)
    s += np.sin(2*np.pi*1400*np.arange(n)/SR) * (np.arange(n) % 2400 < 1200) * .4
    return bandpass(s, 300, 7000) * np.linspace(1, 0, n)
def stinger():
    n = int(SR * 3.2); x = np.arange(n) / SR; s = np.zeros(n)
    for f in (233.1, 246.9, 349.2, 370.0, 493.9, 698.5): s += (2 * ((f * x) % 1) - 1) * .16
    s = bandpass(s, 120, 6000) * env(n, .004, 1.1) + rng.normal(0, 1, n) * np.exp(-x*6) * .5
    s += np.sin(2*np.pi*np.cumsum(28 + 70*np.exp(-x*5))/SR) * env(n, .002, .9) * 1.2
    return np.tanh(s * 1.4)
def riser(d):
    n = int(SR * d); x = np.arange(n) / SR; k = x / d
    tone = np.sin(2*np.pi*np.cumsum(180 + 900*k**2)/SR) * k**2 * (0.6 + 0.4*np.sin(2*np.pi*(4 + 18*k)*x))
    return tone * .5 + bandpass(rng.normal(0, 1, n) * k**3, 1500, 9000) * .6
def stampfx():
    n = int(SR * .5); x = np.arange(n) / SR
    return np.tanh((np.sin(2*np.pi*(70 + 60*np.exp(-x*30))*x) * env(n, .001, .12) + bandpass(rng.normal(0, 1, n), 400, 5000) * np.exp(-x*60) * .8) * 2)
def heartbeat(a, b, bpm0, bpm1):
    tt = a
    while tt < b:
        k = (tt - a) / (b - a); bpm = bpm0 + (bpm1 - bpm0) * k
        for off, g in ((0, 1), (.16, .7)):
            n = int(SR * .22); x = np.arange(n) / SR
            add(np.sin(2*np.pi*(48 + 30*np.exp(-x*30))*x) * env(n, .004, .07), tt + off, .9 * g * (.5 + .5*k))
        tt += 60 / bpm
def flash():
    n = int(SR * .3); x = np.arange(n) / SR
    return np.sin(2*np.pi*(2100 + 300*np.sin(2*np.pi*31*x))*x) * np.sin(np.pi*x/.3) * .5
def tone_seg(a, b, fn, gain, pan=0):
    n = int((b - a) * SR); x = np.arange(n) / SR; s = fn(x, n)
    fade = np.minimum(1, np.minimum(x / .05, (n / SR - x) / .05)); add(s * fade, a, gain, pan)

for c in cues:
    ty, at = c['type'], c['t']; end = c.get('end', at)
    if ty == 'hit': add(hit(True), at, .9)
    elif ty == 'hit2': add(hit(False), at, .6)
    elif ty == 'glitch': add(glitch(), at, .35, pan=.3)
    elif ty == 'stinger': add(stinger(), at, 1.0)
    elif ty == 'riser': add(riser(end - at), at, .55)
    elif ty == 'heart': heartbeat(at, end, c['bpm0'], c['bpm1'])
    elif ty == 'flash': add(flash(), at, .28, pan=-.4)
    elif ty == 'stampfx': add(stampfx(), at, .8)
    elif ty == 'shutter':
        n = int(SR * .12); x = np.arange(n) / SR; add(bandpass(rng.normal(0, 1, n), 1500, 9000) * (np.exp(-x*90) + np.exp(-np.maximum(x-.06, 0)*90) * (x > .06)), at, .6)
    elif ty == 'chainsaw':
        tone_seg(at, end, lambda x, n: bandpass(np.tanh(np.sin(2*np.pi*np.cumsum(95 + 45*np.maximum(0, np.sin(2*np.pi*.7*x))**3)/SR) * 4) + rng.normal(0, .3, n), 80, 3000), .09, pan=.2)
    elif ty == 'roll':
        tone_seg(at, end, lambda x, n: bandpass(rng.normal(0, 1, n), 40, 300) * (0.6 + 0.4*np.sin(2*np.pi*3*x)) + np.sin(2*np.pi*(380 + 40*np.sin(2*np.pi*.5*x))*x) * (np.sin(2*np.pi*.33*x) > .97) * .4, .22)
    elif ty == 'coin':
        n = int(SR * .5); x = np.arange(n) / SR; s = (np.sin(2*np.pi*2400*x) + .6*np.sin(2*np.pi*3700*x)) * env(n, .001, .08)
        s += np.sin(2*np.pi*1800*np.maximum(x - .18, 0)) * env(n, .001, .1) * (x > .18) * .6; add(s, at, .35)
    elif ty == 'deleting':
        k = at
        while k < end: n = int(SR * .05); x = np.arange(n) / SR; add(np.sin(2*np.pi*1200*x) * env(n, .002, .02), k, .18); k += rng.uniform(.08, .2)
    elif ty == 'volume':
        for i in range(12):
            n = int(SR * .07); x = np.arange(n) / SR; add(np.sin(2*np.pi*880*x) * env(n, .002, .04), at + i * (end - at) / 12, .3 * (1 - i/12))
    elif ty == 'unplug':
        n = int(SR * .6); x = np.arange(n) / SR; add(np.tanh(np.sin(2*np.pi*(90 + 50*np.exp(-x*40))*x) * env(n, .001, .08) * 3) + np.sin(2*np.pi*440*x) * (x > .25) * env(n, .001, .5) * .4, at, .5)
    elif ty == 'crawl':
        k = at
        while k < end: n = int(SR * .012); add(bandpass(rng.normal(0, 1, n), 3000, 9000) * np.hanning(n), k, .2, pan=rng.uniform(-.9, .9)); k += rng.uniform(.01, .05)
    elif ty == 'bars':
        tone_seg(at, end, lambda x, n: np.sin(2*np.pi*1000*x), .12)
    elif ty == 'eas':
        tone_seg(at, end, lambda x, n: (np.sin(2*np.pi*853*x) + np.sin(2*np.pi*960*x)) * .5, .18)
    elif ty == 'staticb':
        tone_seg(at, end, lambda x, n: bandpass(rng.normal(0, 1, n), 800, 9000) * (0.6 + 0.4*np.sin(2*np.pi*.8*x)**2), .07)

def verb(x):
    y = x.copy()
    for d, g in ((0.043, .35), (0.071, .28), (0.113, .22), (0.167, .16), (0.239, .11), (0.331, .07)):
        k = int(d * SR); y[k:] += x[:-k] * g
    return y
L, R = verb(L), verb(np.roll(R, 37))
f = int(.25 * SR); fade = np.ones(N); fade[:f] = np.linspace(.6, 1, f); fade[-f:] = np.linspace(1, .6, f); L *= fade; R *= fade
mx = max(np.abs(L).max(), np.abs(R).max()); L, R = L / mx * .89, R / mx * .89
with wave.open(os.path.join(here, f'{v}_sfx.wav'), 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.stack([L, R], 1) * 32767).astype(np.int16).tobytes())
print(v, 'ok', DUR)
