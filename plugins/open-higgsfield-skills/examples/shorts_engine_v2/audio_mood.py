import numpy as np, wave, json, os
mood=os.environ.get("MOOD","pad")
SR=44100; TL=json.load(open("timeline.json")); T=TL["total"]; n=int(SR*(T+.5)); t=np.arange(n)/SR; rng=np.random.default_rng(11)
def tone(f,a,b,amp,att=.3,rel=.6,sq=False):
    m=np.zeros(n); i0,i1=int(a*SR),min(n,int(b*SR)); u=np.arange(i1-i0)/SR; L=b-a
    e=np.minimum(1,u/att)*np.minimum(1,(L-u)/rel).clip(0,1); w=np.sin(2*np.pi*f*u)
    if sq: w=np.sign(w)*.6+w*.4
    m[i0:i1]=amp*e*w; return m
x=np.zeros(n)
if mood=="chip":
    ch=[(110,165,220),(87.3,130.8,174.6),(130.8,196,261.6),(98,146.8,196)]
    k=0; tt=0
    while tt<T+1:
        for f in ch[k%4]: x+=tone(f,tt,tt+7.4,.03,.4,.8)
        tt+=7; k+=1
    notes=[440,523,659,784,659,523,440,392]
    for i,tb in enumerate(np.arange(0.3,T,.25)):
        f=notes[i%8]*(.75 if (i//16)%2 else 1)
        m=(t>=tb)&(t<tb+.2); u=t[m]-tb; w=np.sign(np.sin(2*np.pi*f*u)); x[m]+=.022*np.exp(-6*u)*w
    for i,tb in enumerate(np.arange(0.0,T,.5)):
        m=(t>=tb)&(t<tb+.12); u=t[m]-tb; x[m]+=.07*np.exp(-30*u)*np.sin(2*np.pi*(90-300*u)*u) if i%2==0 else .02*rng.standard_normal(m.sum())*np.exp(-40*u)
else:
    ch=[(55,82.4,110,130.8),(43.65,65.4,87.3,130.8),(65.4,98,130.8,164.8),(49,73.4,98,123.5)]
    k=0; tt=0
    while tt<T+1:
        for f in ch[k%4]: x+=tone(f,tt,tt+7.4,.05,1.2,1.5)+tone(f*2.003,tt,tt+7.4,.02,1.5,1.5)
        tt+=7; k+=1
    notes=[220,261.6,329.6,392,329.6,261.6]
    for i,tb in enumerate(np.arange(0.4,T,.5)):
        f=notes[i%6]*(0.75 if (i//12)%2 else 1)
        m=(t>=tb)&(t<tb+.35); u=t[m]-tb; x[m]+=.035*np.exp(-9*u)*np.sin(2*np.pi*f*u)
def whoosh(a,d=.5,amp=.22):
    m=(t>=a)&(t<a+d); u=(t[m]-a)/d; nz=rng.standard_normal(m.sum()); k=int(6+50*(1-u.mean()))
    x[m]+=amp*np.sin(np.pi*u)*np.convolve(nz,np.ones(k)/k,mode="same")
def boom(a,amp=.4):
    m=(t>=a)&(t<a+1.2); u=t[m]-a; x[m]+=amp*np.exp(-3.2*u)*np.sin(2*np.pi*(80-35*u)*u)
for s in TL["scenes"][1:]: whoosh(s["start"]-.15)
boom(0.0,.3); boom(TL["scenes"][6]["start"],.45)
x*=np.clip(t/1.0,0,1)*np.clip((T+.3-t)/1.0,0,1); x=np.tanh(x*1.5)*.85
with wave.open("music.wav","wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x*32767).astype(np.int16).tobytes())
