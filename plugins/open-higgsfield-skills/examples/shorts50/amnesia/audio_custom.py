import sys,json,math
sys.argv=["x"]
from sfxlib import *
TL=json.load(open("timeline.json")); T=TL["total"]; sc=TL["scenes"]; m=Mix(T); rng=m.rng
def W(i): s=sc[i]; e=sc[i+1]["start"] if i+1<len(sc) else T; return s["start"],e
for k in range(int(T/6)+2): m.sine(k*6,hz(30),6.6,.07,att=1.6,rel=1.6); m.sine(k*6,hz(30)*1.06,6.6,.05,att=1.6,rel=1.6); m.noise(k*6,6,.04,decay=0,lp=90,att=1.5)
def drip(a): m.sine(a,hz(96),.18,.06,decay=18,f2=hz(88))
for k in range(int(T/2.4)): drip(k*2.4+rng.random())
def step(a,amp=.1): m.noise(a,.12,amp,decay=22,lp=10); m.sine(a,70,.1,amp*.8,decay=22,f2=45)
a0,a1=W(0)
for k in range(int((a1-a0)/.55)): step(a0+k*.55,.1)
a0,a1=W(2)
for k in range(8): m.noise(a0+.6+k*.7,.3,.05,decay=6,lp=30)   # respiracion contenida
a0,a1=W(3)
for k in range(int((a1-a0)/.8)): m.sine(a0+k*.8,60+k*0,.2,.18*(k/8.0+.4),decay=12,f2=36)    # latido que sube
a0,a1=W(4)
for k in range(14): m.sine(a0+.4+k*.4,hz(81+int(rng.random()*8)),.5,.03,att=.1,decay=2,f2=hz(78))   # susurros agudos
a0,a1=W(5)
for k in range(int((a1-a0)/.7)): step(a0+k*.7,.16); 
m.sine(a0+5.0,hz(36),1.2,.3,att=.4,decay=2.0); 
a0,a1=W(6)
for j,nn in enumerate([57,64,69]): m.sine(a0+.2+j*.2,hz(nn),3.0,.07,att=.4,decay=.9)
whooshes(m,TL); m.save("music.wav",gain=1.3,T=T)
