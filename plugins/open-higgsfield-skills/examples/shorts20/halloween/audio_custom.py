import sys,json,math
sys.argv=["x"]
from sfxlib import *
TL=json.load(open("timeline.json")); T=TL["total"]; sc=TL["scenes"]; m=Mix(T); rng=m.rng
def W(i): s=sc[i]; e=sc[i+1]["start"] if i+1<len(sc) else T; return s["start"],e
# ostinato de piano inquieto 5/4 (original, inspirado solo en el tipo de compas)
notes=[57,60,64,57,60,64,57,60]
t=0.0; step=.28; k=0
while t<T-.3:
    nn=notes[k%len(notes)]-(12 if (k//16)%2 else 0)
    m.sine(t,hz(nn),.5,.07,att=.01,decay=7); m.sine(t,hz(nn+12),.4,.025,att=.01,decay=9)
    t+=step*(1.25 if k%5==4 else 1.0); k+=1
for k in range(int(T/6)+2): m.sine(k*6,hz(33),6.6,.06,att=1.6,rel=1.6); m.noise(k*6,6,.03,decay=0,lp=70,att=1.5)
a0,a1=W(1); m.noise(a0+.5,.08,.2,decay=30,hp=4); m.sine(a0+.5,hz(88),.1,.1,decay=18)   # claqueta
a0,a1=W(2); m.sine(a0+1.0,hz(88),.08,.1,decay=20); m.sine(a0+1.2,hz(95),.1,.1,decay=20)   # caja registradora
a0,a1=W(3)
for q in (.6,2.4,4.4): m.noise(a0+q,.35,.12,decay=8,hp=3); m.sine(a0+q,hz(50),.2,.1,decay=10)
a0,a1=W(4); m.sine(a0,hz(36),a1-a0,.1,att=1.0,decay=.2)
a0,a1=W(6)
for j,nn in enumerate([57,64,69,76]): m.sine(a0+2.0+j*.15,hz(nn),2.0,.07,att=.2,decay=1.0)
whooshes(m,TL); m.save("music.wav",gain=1.3,T=T)
