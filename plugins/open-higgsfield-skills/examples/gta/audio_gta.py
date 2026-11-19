import numpy as np, wave, json
SR=44100; TL=json.load(open("timeline.json")); T=TL["total"]; n=int(SR*(T+.5)); t=np.arange(n)/SR; rng=np.random.default_rng(7)
def tone(f,a,b,amp,att=.3,rel=.6):
    m=np.zeros(n); i0,i1=int(a*SR),min(n,int(b*SR)); u=np.arange(i1-i0)/SR; L=(b-a)
    e=np.minimum(1,u/att)*np.minimum(1,(L-u)/rel).clip(0,1); m[i0:i1]=amp*e*np.sin(2*np.pi*f*u)
    return m
x=np.zeros(n)
# pad misterioso: Am - F - C - G (cada ~7 s)
ch=[(55,82.4,110,130.8),(43.65,65.4,87.3,130.8),(65.4,98,130.8,164.8),(49,73.4,98,123.5)]
k=0; tt=0
while tt<T+1:
    for f in ch[k%4]: x+=tone(f,tt,tt+7.4,.05,1.2,1.5)+tone(f*2.003,tt,tt+7.4,.02,1.5,1.5)
    tt+=7; k+=1
# pulso suave (arpegio) con ritmo
notes=[220,261.6,329.6,392,329.6,261.6]
for i,tb in enumerate(np.arange(0.4,T,.5)):
    f=notes[i%6]*(0.75 if (i//12)%2 else 1)
    m=(t>=tb)&(t<tb+.35); u=t[m]-tb; x[m]+=.035*np.exp(-9*u)*np.sin(2*np.pi*f*u)
# sfx
def whoosh(a,d=.5,amp=.25):
    m=(t>=a)&(t<a+d); u=(t[m]-a)/d; nz=rng.standard_normal(m.sum()); 
    y=np.convolve(nz,np.ones(int(6+60*(1-u.mean())))/ (6+60*(1-u.mean())),mode="same"); x[m]+=amp*np.sin(np.pi*u)*y
def boom(a,amp=.5):
    m=(t>=a)&(t<a+1.4); u=t[m]-a; x[m]+=amp*np.exp(-3*u)*np.sin(2*np.pi*(80-35*u)*u)
def glitch(a,d=.5):
    m=(t>=a)&(t<a+d); u=t[m]-a; x[m]+=.12*rng.standard_normal(m.sum())*(rng.random(m.sum())>.6)*np.exp(-3*u)
glitch(0.0,.5); boom(0.0,.35)
for s in TL["scenes"][1:]: whoosh(s["start"]-.15)
boom(TL["scenes"][4]["start"]+1.5,.3)       # giro de roles
boom(TL["scenes"][6]["start"],.5)           # el error lo salvó
glitch(T-1.0,1.0)
x*=np.clip(t/1.0,0,1)*np.clip((T+.3-t)/1.0,0,1)
x=np.tanh(x*1.5)*.85
with wave.open("music.wav","wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x*32767).astype(np.int16).tobytes())
