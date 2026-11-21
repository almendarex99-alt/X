import sys,json,math
sys.argv=["x"]
from sfxlib import *
TL=json.load(open("timeline.json")); T=TL["total"]; sc=TL["scenes"]; m=Mix(T); rng=m.rng
def W(i): s=sc[i]; e=sc[i+1]["start"] if i+1<len(sc) else T; return s["start"],e
for k in range(int(T/6)+2): m.sine(k*6,hz(27),6.6,.07,att=1.6,rel=1.6); m.sine(k*6,hz(27)*1.5,6.6,.035,att=1.6,rel=1.6); m.noise(k*6,6,.035,decay=0,lp=70,att=1.5)
def beep(a,f=88,amp=.1): m.sine(a,hz(f),.08,amp,decay=20); m.sine(a,hz(f+12),.06,amp*.5,decay=26)
def clank(a): m.noise(a,.08,.2,decay=30,hp=4); m.sine(a,hz(66),.3,.1,decay=8)
for k in range(int(T/2.0)): 
    if rng.random()<.55: clank(k*2.0+rng.random())
# detector de movimiento: pitido regular, cada vez mas rapido
for i,(a0,a1) in ((0,W(0)),(5,W(5))):
    t=a0+.3; gap=1.1 if i==0 else 1.0
    while t<a1-.2: beep(t); t+=gap; gap=max(.14 if i==5 else .5,gap*(.9 if i==5 else .97))
a0,a1=W(3)
for k in range(5): beep(a0+1.0+k*1.0,76+k*2,.06)
a0,a1=W(4)
for k in range(int((a1-a0)/.6)): m.noise(a0+k*.6,.1,.08,decay=20,lp=10); m.sine(a0+k*.6,hz(34),.12,.1,decay=16)
a0,a1=W(5); m.sine(a0+5.0,hz(38),1.2,.3,att=.3,decay=2.0); m.noise(a0+5.0,.6,.2,decay=6,hp=3)
a0,a1=W(6)
for j,nn in enumerate([57,64,69,76]): m.sine(a0+.2+j*.15,hz(nn),3.0,.07,att=.4,decay=.9)
whooshes(m,TL); m.save("music.wav",gain=1.3,T=T)
