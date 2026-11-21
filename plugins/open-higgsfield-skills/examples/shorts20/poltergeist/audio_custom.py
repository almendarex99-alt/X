import sys,json,math
sys.argv=["x"]
from sfxlib import *
TL=json.load(open("timeline.json")); T=TL["total"]; sc=TL["scenes"]; m=Mix(T); rng=m.rng
def W(i): s=sc[i]; e=sc[i+1]["start"] if i+1<len(sc) else T; return s["start"],e
for k in range(int(T/6)+2): m.sine(k*6,hz(32),6.6,.07,att=1.6,rel=1.6); m.noise(k*6,6,.03,decay=0,lp=80,att=1.5)
# nana de caja de musica (original, inquietante)
mel=[76,79,83,81,79,76,74,71]
t=1.0; k=0
while t<T-1:
    nn=mel[k%8]; m.sine(t,hz(nn),.4,.06,att=.01,decay=7); m.sine(t,hz(nn)*2,.3,.02,att=.01,decay=10)
    t+=.55; k+=1
a0,a1=W(2)
for k in range(5): m.noise(a0+.6+k*.7,.5,.14,decay=6,lp=500); m.sine(a0+.6+k*.7,hz(40),.3,.1,decay=8)
a0,a1=W(3)
for k in range(8): m.sine(a0+1.0+k*.4,hz(95),.05,.08,decay=26)   # monedas
a0,a1=W(4)
for k in range(10): m.noise(a0+.5+k*.45,.08,.12,decay=30,hp=6)    # huesos
a0,a1=W(6); m.noise(a0,a1-a0,.1,decay=0,hp=6,att=.1)  # estatica
whooshes(m,TL); m.save("music.wav",gain=1.3,T=T)
