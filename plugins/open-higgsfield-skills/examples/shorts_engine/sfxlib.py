import numpy as np, wave, json
SR=44100
class Mix:
    def __init__(s,T):
        s.n=int(SR*(T+.6)); s.x=np.zeros(s.n); s.t=np.arange(s.n)/SR; s.rng=np.random.default_rng(3)
    def add(s,a,sig,amp=1.0):
        i=int(a*SR)
        if i<0 or i>=s.n: return
        sig=sig[:max(0,s.n-i)]; s.x[i:i+len(sig)]+=sig*amp
    def sq(s,a,f,dur,amp=.1,duty=.5,att=.004,rel=.02,decay=0.0):
        n=int(dur*SR); u=np.arange(n)/SR; ph=(f*u)%1.0; w=np.where(ph<duty,1.0,-1.0)
        e=np.minimum(1,u/att)*np.minimum(1,(dur-u)/rel).clip(0,1)*np.exp(-decay*u); s.add(a,w*e,amp)
    def sine(s,a,f,dur,amp=.1,att=.004,rel=.03,decay=0.0,f2=None):
        n=int(dur*SR); u=np.arange(n)/SR; ff=f if f2 is None else f+(f2-f)*u/dur
        ph=2*np.pi*np.cumsum(ff)/SR if f2 is not None else 2*np.pi*f*u
        e=np.minimum(1,u/att)*np.minimum(1,(dur-u)/rel).clip(0,1)*np.exp(-decay*u); s.add(a,np.sin(ph)*e,amp)
    def noise(s,a,dur,amp=.1,decay=8.0,lp=0,hp=0,att=.003):
        n=int(dur*SR); u=np.arange(n)/SR; z=s.rng.standard_normal(n)
        if lp: z=np.convolve(z,np.ones(lp)/lp,mode="same")
        if hp: z=z-np.convolve(z,np.ones(hp)/hp,mode="same")
        e=np.minimum(1,u/att)*np.exp(-decay*u); s.add(a,z*e,amp)
    def save(s,path="music.wav",gain=1.5,fade_in=.6,T=None):
        x=s.x*np.clip(s.t/fade_in,0,1)
        if T: x*=np.clip((T+.35-s.t)/.8,0,1)
        x=np.tanh(x*gain)*.88
        with wave.open(path,"wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x*32767).astype(np.int16).tobytes())
def hz(n): return 440.0*2**((n-69)/12.0)
def whooshes(m,TL):
    for s in TL["scenes"][1:]:
        a=s["start"]-.15; m.noise(a,.5,.12,decay=3,lp=30)
