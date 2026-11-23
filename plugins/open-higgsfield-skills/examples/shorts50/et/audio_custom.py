import sys,json,math
sys.argv=["x"]
from sfxlib import *
TL=json.load(open("timeline.json")); T=TL["total"]; sc=TL["scenes"]; m=Mix(T); rng=m.rng
def W(i): s=sc[i]; e=sc[i+1]["start"] if i+1<len(sc) else T; return s["start"],e
for k in range(int(T/6)+2): m.sine(k*6,hz(34),6.6,.05,att=1.6,rel=1.6); m.noise(k*6,6,.03,decay=0,lp=70,att=1.5)
for k in range(int(T/.45)): 
    if rng.random()<.5: m.sq(k*.45,hz(60+int(rng.random()*10)),.06,.025,duty=.5,decay=10)     # pitidos de consola retro
def rumble(a,d,amp=.1): m.noise(a,d,amp,decay=0,lp=120,att=.3); m.sine(a,hz(30),d,.08,att=.3,rel=.3)
a0,a1=W(0); rumble(a0+.2,a1-a0-.4,.1)
a0,a1=W(2)
for k in range(5): m.sine(a0+k,hz(64),.12,.05,decay=12)
for k in range(5): m.sq(a0+.8+k*1.0,hz(76),.1,.05,decay=8)
a0,a1=W(3)
for k in range(5): m.sine(a0+1.2+k*.7,hz(60-k*3),.4,.07,decay=4,f2=hz(50-k*3))
a0,a1=W(4); rumble(a0+.2,a1-a0-.4,.14)
for k in range(10): m.noise(a0+.5+k*.55,.18,.2,decay=14,lp=30)
a0,a1=W(5); rumble(a0+.2,a1-a0-.4,.1)
for k in range(8): m.noise(a0+.6+k*.7,.22,.1,decay=14,hp=3)
a0,a1=W(6)
for j,nn in enumerate([60,64,67,72]): m.sine(a0+.2+j*.15,hz(nn),2.6,.07,att=.2,decay=1.0)
whooshes(m,TL); m.save("music.wav",gain=1.3,T=T)
