import sys,json,math
sys.argv=["x"]
from sfxlib import *
TL=json.load(open("timeline.json")); T=TL["total"]; sc=TL["scenes"]; m=Mix(T); rng=m.rng
def W(i): s=sc[i]; e=sc[i+1]["start"] if i+1<len(sc) else T; return s["start"],e
for k in range(int(T/6)+2): m.sine(k*6,hz(26),6.6,.08,att=1.6,rel=1.6); m.sine(k*6,hz(26)*1.5,6.6,.04,att=1.6,rel=1.6); m.noise(k*6,6,.03,decay=0,lp=70,att=1.5)
def clank(a): m.noise(a,.08,.2,decay=30,hp=4); m.sine(a,hz(70),.3,.12,decay=8)
for k in range(int(T/2.2)): 
    if rng.random()<.6: clank(k*2.2+rng.random())
def blip(a,f=84): m.sine(a,hz(f),.1,.05,decay=12); m.sine(a,hz(f+12),.08,.03,decay=16)
a0,a1=W(0)
for k in range(int((a1-a0)/.9)): m.sine(a0+k*.9,hz(48),.4,.12,decay=5,f2=hz(44))
a0,a1=W(3)
for k in range(int((a1-a0)/.7)): m.sine(a0+k*.7,60,.18,.2,decay=14,f2=36); 
a0,a1=W(4)
for k in range(6): blip(a0+1.6+k*.12,80+k*2)
a0,a1=W(5)
for k in range(int((a1-a0)/.5)): m.sine(a0+k*.5,hz(46+int(k*.4)),.3,.1,decay=4)
m.noise(a0+4.8,.8,.3,decay=4,hp=3); m.sine(a0+4.8,hz(40),1.0,.3,decay=3,f2=hz(30))
a0,a1=W(6)
for j,nn in enumerate([72,76,81,88]): m.sine(a0+.2+j*.15,hz(nn),2.4,.07,att=.2,decay=1.0)
whooshes(m,TL); m.save("music.wav",gain=1.3,T=T)
