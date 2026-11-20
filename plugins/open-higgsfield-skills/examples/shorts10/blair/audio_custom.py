import sys,json,math
sys.argv=["x"]
from sfxlib import *
TL=json.load(open("timeline.json")); T=TL["total"]; sc=TL["scenes"]; m=Mix(T); rng=m.rng
def W(i): s=sc[i]; e=sc[i+1]["start"] if i+1<len(sc) else T; return s["start"],e
for k in range(int(T/3)+2): m.noise(k*3,3.3,.06,decay=0,lp=100,att=1.0)     # viento
for k in range(int(T*1.6)):
    if rng.random()<.5: t=k*.62; m.sine(t,3300+rng.random()*500,.05,.012,decay=30)
for k in range(int(T/5)+1): m.sine(k*5,hz(31),5.6,.06,att=1.4,rel=1.4)
def step(a,amp=.1): m.noise(a,.12,amp,decay=20,lp=12); m.sine(a,70,.1,amp*.8,decay=22,f2=45)
def twig(a): m.noise(a,.04,.2,decay=60,hp=3); m.sine(a,260,.05,.05,decay=40)
a0,a1=W(1)
for k in range(int((a1-a0)/.5)): step(a0+k*.5,.12)
for k in range(4): twig(a0+1.4+k*1.7)
a0,a1=W(0); twig(a0+2.2); m.sine(a0+2.5,hz(36),1.6,.15,att=.3,decay=1.6)
# camara: pitido de grabacion
for i in (0,1,2,7): a0,a1=W(i); m.sine(a0+.1,1200,.08,.04,decay=20)
a0,a1=W(3)
for k in range(6): m.noise(a0+.4+k*.55,.05,.1,decay=40,hp=3)   # carteles pegados
a0,a1=W(5)
for k in range(30): m.sine(a0+.6+k*.14,hz(60+int(k*.6)),.1,.04,decay=14)  # contador subiendo
m.sine(a0+4.5,hz(76),1.2,.1,decay=2); m.sine(a0+4.5,hz(83),1.0,.07,decay=2.4)
a0,a1=W(6)
for j,nn in enumerate([45,52,57]): m.sine(a0+.2+j*.2,hz(nn),3.0,.07,att=.4,decay=.9)
whooshes(m,TL); m.save("music.wav",gain=1.3,T=T)
