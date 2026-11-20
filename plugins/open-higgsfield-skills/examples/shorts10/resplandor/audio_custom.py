import sys,json,math
sys.argv=["x"]
from sfxlib import *
TL=json.load(open("timeline.json")); T=TL["total"]; sc=TL["scenes"]; m=Mix(T); rng=m.rng
def W(i): s=sc[i]; e=sc[i+1]["start"] if i+1<len(sc) else T; return s["start"],e
# cuerdas graves y disonantes (original), tension lenta
for k in range(int(T/6)+2):
    m.sine(k*6,hz(29),6.6,.07,att=1.8,rel=1.8); m.sine(k*6,hz(29)*1.06,6.6,.05,att=1.8,rel=1.8); m.sine(k*6+2,hz(58)*1.5,3.6,.025,att=1.2,rel=1.2)
def clap(a): m.noise(a,.05,.22,decay=60,hp=3); m.sine(a,300,.06,.06,decay=40)
def thump(a): m.sine(a,70,.3,.3,decay=9,f2=38); m.noise(a,.08,.14,decay=30,lp=8)
def step(a,amp=.1): m.noise(a,.1,amp,decay=24,lp=9); m.sine(a,100,.1,amp*.8,decay=22,f2=55)
# A y D: cada toma suena como una claqueta, y se acelera
for i,dur in((0,3.6),(3,6.0)):
    a0,a1=W(i); t=a0+.2; gap=.45
    while t<a0+dur+.4: clap(t); t+=gap; gap=max(.06,gap*.93)
a0,a1=W(3)
for k in range(int((a1-a0)/.55)): step(a0+k*.55,.07)
for k in range(5): thump(a0+1.0+k*1.3)
a0,a1=W(1)
for k in range(5): clap(a0+.6+k*1.3)
a0,a1=W(2)
for k in range(60): m.noise(a0+k*(5.0/60)+.1,.03,.12,decay=60,hp=3)
# E: sello y campanilla del record
a0,a1=W(4); thump(a0+.6); 
for j,nn in enumerate([76,81,85,88]): m.sine(a0+1.0+j*.1,hz(nn),1.6,.07,decay=2.2)
a0,a1=W(5)
for k in range(int((a1-a0)/.5)): m.sine(a0+k*.5,hz(60),.05,.03,decay=40)   # tic del reloj acelerado
a0,a1=W(6); m.noise(a0,a1-a0,.05,decay=0,lp=140,att=1.0)
for j,nn in enumerate([45,52,57]): m.sine(a0+.2+j*.2,hz(nn),3.0,.07,att=.4,decay=.9)
whooshes(m,TL); m.save("music.wav",gain=1.3,T=T)
