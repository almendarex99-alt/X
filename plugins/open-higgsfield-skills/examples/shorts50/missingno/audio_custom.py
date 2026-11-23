import sys,json,math
sys.argv=["x"]
from sfxlib import *
TL=json.load(open("timeline.json")); T=TL["total"]; sc=TL["scenes"]; m=Mix(T); rng=m.rng
def W(i): s=sc[i]; e=sc[i+1]["start"] if i+1<len(sc) else T; return s["start"],e
# fondo: melodia de aventura original, onda cuadrada tipo Game Boy, ritmo suave
phr=[69,72,76,72,69,64,67,71,74,71,67,62,64,67,71,76,74,71,67,64]
t=0.3; i=0
while t<T+1: m.sq(t,hz(phr[i%len(phr)]),.22,.04,duty=.5,decay=3); t+=.3; i+=1
t=0.3; j=0
while t<T+1: m.sq(t,hz([45,45,43,43,41,41,43,43][j%8]-12),.28,.05,duty=.25); t+=.6; j+=1
def glitch(a,d=.4):
    n=int(d*SR); u=np.arange(n)/SR; f=np.where((np.floor(u*60)%3)==0,rng.random(n)*1800+200,200); ph=2*np.pi*np.cumsum(f)/SR
    m.add(a,np.sign(np.sin(ph))*np.exp(-u*3)*.14,1.0)
a0,a1=W(0); glitch(a0+.4,.8)
a0,a1=W(2)
for k in range(3): m.sq(a0+.8+k*1.5,hz(72+k*2),.12,.07,duty=.5,decay=5)
a0,a1=W(3); glitch(a0+1.2,.7)
a0,a1=W(4)
for k in range(10): glitch(a0+.4+k*.5,.2)
a0,a1=W(5)
for k in range(40): m.sq(a0+1.0+k*.075,hz(60+int(k*.7)),.04,.05,duty=.5,decay=25)
for j,nn in enumerate([72,76,79,84]): m.sq(a0+4.3+j*.08,hz(nn),.25,.08,decay=4)
a0,a1=W(6)
for k in range(8): m.sq(a0+.5+k*.6,hz(67+(k%3)*2),.1,.04,duty=.25,decay=10)
whooshes(m,TL); m.save("music.wav",gain=1.2,T=T)
