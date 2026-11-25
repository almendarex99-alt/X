# Diseño de sonido sintetizado, sincronizado con cues.json (misma línea de tiempo que la imagen)
import json, numpy as np, wave, os
SR = 48000; DUR = 50.0; N = int(SR * DUR)
rng = np.random.default_rng(7)
here = os.path.dirname(os.path.abspath(__file__))
cues = json.load(open(os.path.join(here, 'cues.json')))
L = np.zeros(N); R = np.zeros(N)
t = np.arange(N) / SR

def bandpass(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    m = ((f >= lo) & (f <= hi)).astype(float)
    m = np.convolve(m, np.ones(41) / 41, 'same')
    return np.fft.irfft(X * m, len(x))

def add(sig, at, gain=1.0, pan=0.0):
    i = int(at * SR); sig = sig[: max(0, N - i)]
    if i < 0 or len(sig) == 0: return
    L[i:i + len(sig)] += sig * gain * (1 - max(pan, 0))
    R[i:i + len(sig)] += sig * gain * (1 + min(pan, 0))

def env(n, a, d):
    e = np.ones(n); na = max(1, int(a * SR)); e[:na] = np.linspace(0, 1, na)
    e *= np.exp(-np.arange(n) / SR / d); return e

# ---------- cama: drone + zumbido de fluorescente ----------
lfo = 0.75 + 0.25 * np.sin(2 * np.pi * 0.09 * t)
drone = (np.sin(2*np.pi*41.2*t) + .8*np.sin(2*np.pi*41.7*t) + .5*np.sin(2*np.pi*61.74*t+1) + .25*np.sin(2*np.pi*82.6*t)) * lfo
brown = np.cumsum(rng.normal(0, 1, N)); brown -= np.convolve(brown, np.ones(4801)/4801, 'same'); brown /= np.abs(brown).max()
air = bandpass(rng.normal(0, 1, N), 150, 900); air /= np.abs(air).max()
hum = (np.sign(np.sin(2*np.pi*120*t)) * .15 + np.sin(2*np.pi*240*t) * .1)
crack = np.zeros(N)
for k in range(int(DUR * 22)):
    h = (np.sin(k * 127.1 + 311.7) * 43758.5453) % 1
    if h > .93: i = int(k / 22 * SR); crack[i:i + 900] += rng.normal(0, 1, 900) * np.exp(-np.arange(900) / 200)
bed = drone * .16 + brown * .10 + air * .05 + hum * .02 + crack * .05
# la niebla de Silent Hills: pad grave que se abre
for c in cues:
    if c['type'] == 'fogpad':
        a, b = c['t'], c['end']; m = (t >= a) & (t < b); k = (t[m] - a) / (b - a)
        pad = (np.sin(2*np.pi*55*t[m]) + np.sin(2*np.pi*82.4*t[m]) + .6*np.sin(2*np.pi*110.3*t[m]) + .4*np.sin(2*np.pi*164.8*t[m])) * np.sin(np.pi * k) * .09
        bed[m] += pad
# silencio antes del susto y fundido para que el bucle empalme
gate = np.ones(N)
for c in cues:
    if c['type'] == 'silence':
        a, b = int(c['t'] * SR), int(c['end'] * SR); gate[a - 2400:a] = np.linspace(1, 0, 2400); gate[a:b] = 0
L += bed * gate; R += bed * gate * .96

# ---------- efectos ----------
def hit(big=True):
    n = int(SR * (1.6 if big else .9)); tt = np.arange(n) / SR
    f = 30 + (95 if big else 70) * np.exp(-tt * 7)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, .003, .55 if big else .3)
    s += rng.normal(0, 1, n) * np.exp(-tt * 40) * (.35 if big else .2)
    return np.tanh(s * 1.6)

def glitch():
    n = int(SR * .26); s = rng.normal(0, 1, n)
    s = np.round(s * 4) / 4; s *= (np.sin(2 * np.pi * 37 * np.arange(n) / SR) > 0)
    s += np.sin(2 * np.pi * 1400 * np.arange(n) / SR) * (np.arange(n) % 2400 < 1200) * .4
    return bandpass(s, 300, 7000) * np.linspace(1, 0, n)

def beep():
    n = int(SR * .32); tt = np.arange(n) / SR
    s = (np.sin(2*np.pi*660*tt) + np.sin(2*np.pi*663*tt)) * env(n, .005, .2)
    return bandpass(s + rng.normal(0, .2, n), 350, 3200)

def tick():
    n = int(SR * .02); return rng.normal(0, 1, n) * np.exp(-np.arange(n) / 80) * .6 + np.sin(2*np.pi*2400*np.arange(n)/SR) * np.exp(-np.arange(n)/120)

def loopcut():  # golpe de puerta + soplo
    n = int(SR * .9); tt = np.arange(n) / SR
    s = np.sin(2 * np.pi * (55 + 40 * np.exp(-tt * 20)) * tt) * env(n, .002, .18)
    s += bandpass(rng.normal(0, 1, n), 80, 1200) * np.sin(np.pi * np.clip(tt / .9, 0, 1)) * .25
    return s

def flash():  # chillido subliminal
    n = int(SR * .3); tt = np.arange(n) / SR
    s = np.sin(2 * np.pi * (2100 + 300 * np.sin(2 * np.pi * 31 * tt)) * tt) * np.sin(np.pi * tt / .3)
    return s * .5 + bandpass(rng.normal(0, 1, n), 2000, 8000) * np.sin(np.pi * tt / .3) * .3

def stinger():
    n = int(SR * 3.2); tt = np.arange(n) / SR; s = np.zeros(n)
    for f in (233.1, 246.9, 349.2, 370.0, 493.9, 698.5):  # cluster disonante
        ph = 2 * np.pi * f * tt; s += (2 * ((ph / (2 * np.pi)) % 1) - 1) * .16
    s = bandpass(s, 120, 6000) * env(n, .004, 1.1)
    s += rng.normal(0, 1, n) * np.exp(-tt * 6) * .5
    s += np.sin(2 * np.pi * np.cumsum(28 + 70 * np.exp(-tt * 5)) / SR) * env(n, .002, .9) * 1.2
    return np.tanh(s * 1.4)

def riser(d):
    n = int(SR * d); tt = np.arange(n) / SR; k = tt / d
    tone = np.sin(2 * np.pi * np.cumsum(180 + 900 * k ** 2) / SR) * k ** 2 * (0.6 + 0.4 * np.sin(2 * np.pi * (4 + 18 * k) * tt))
    noi = rng.normal(0, 1, n) * k ** 3
    return tone * .5 + bandpass(noi, 1500, 9000) * .6

def heartbeat(a, b, bpm0, bpm1):
    tt = a
    while tt < b:
        k = (tt - a) / (b - a); bpm = bpm0 + (bpm1 - bpm0) * k
        for off, g in ((0, 1), (.16, .7)):
            n = int(SR * .22); x = np.arange(n) / SR
            s = np.sin(2 * np.pi * (48 + 30 * np.exp(-x * 30)) * x) * env(n, .004, .07)
            add(s, tt + off, .9 * g * (.5 + .5 * k))
        tt += 60 / bpm

for c in cues:
    ty, at = c['type'], c['t']
    if ty == 'hit': add(hit(True), at, .9)
    elif ty == 'hit2': add(hit(False), at, .6)
    elif ty == 'glitch': add(glitch(), at, .35, pan=.3)
    elif ty == 'beep': add(beep(), at, .45, pan=-.25)
    elif ty == 'tick': add(tick(), at, .25, pan=.2)
    elif ty == 'loopcut': add(loopcut(), at, .7)
    elif ty == 'flash': add(flash(), at, .28, pan=-.4)
    elif ty == 'stinger': add(stinger(), at, 1.0)
    elif ty == 'riser': add(riser(c['end'] - at), at, .55)
    elif ty == 'heart': heartbeat(at, c['end'], c['bpm0'], c['bpm1'])
    elif ty == 'radio':
        n = int((c['end'] - at) * SR); x = np.arange(n) / SR
        st = bandpass(rng.normal(0, 1, n), 500, 4000) * (0.55 + 0.45 * np.sin(2 * np.pi * 0.7 * x) ** 2)
        st *= np.minimum(1, np.minimum(x / .3, (n / SR - x) / .3))
        add(st, at, .09, pan=-.25)
        # voz de radio ininteligible: formantes que balbucean
        v = np.zeros(n)
        for f0, w in ((130, 1), (260, .5), (390, .3)):
            v += np.sin(2 * np.pi * f0 * x * (1 + .03 * np.sin(2 * np.pi * 5 * x))) * w
        syll = (np.sin(2 * np.pi * 3.3 * x) > .2) * (np.sin(2 * np.pi * .9 * x + 1) > -.4)
        add(bandpass(v * syll, 400, 2600) * np.minimum(1, x / .5), at, .05, pan=-.25)

# reverb simple (eco de pasillo): sumas de retardos decrecientes
def verb(x):
    y = x.copy()
    for d, g in ((0.043, .35), (0.071, .28), (0.113, .22), (0.167, .16), (0.239, .11), (0.331, .07)):
        k = int(d * SR); y[k:] += x[:-k] * g
    return y
L, R = verb(L), verb(np.roll(R, 37))
# fundido de entrada/salida corto para el bucle
f = int(.25 * SR); fade = np.ones(N); fade[:f] = np.linspace(.6, 1, f); fade[-f:] = np.linspace(1, .6, f)
L *= fade; R *= fade
mx = max(np.abs(L).max(), np.abs(R).max()); L, R = L / mx * .89, R / mx * .89
pcm = (np.stack([L, R], 1) * 32767).astype(np.int16)
with wave.open(os.path.join(here, 'sfx.wav'), 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('ok', pcm.shape)
