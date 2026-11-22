import sys,json,math
sys.argv=["x"]
from sfxlib import *
TL=json.load(open("timeline.json")); T=TL["total"]; sc=TL["scenes"]; m=Mix(T); rng=m.rng
def W(i): s=sc[i]; e=sc[i+1]["start"] if i+1<len(sc) else T; return s["start"],e
# zumbido de fluorescentes (120 Hz y armonicos) + tono de sala constante
for k in range(int(T/5)+2):
    for f,a in ((47,.05),(59,.03),(66,.015),(35,.03)): m.sine(k*5,hz(f),5.5,a,att=1.2,rel=1.2)
    m.noise(k*5,5,.03,decay=0,lp=900,att=1.2)
# parpadeo de balastro: chasquidos irregulares
t=1.4
while t<T-1:
    m.noise(t,.05,.16,decay=40,hp=6); m.sine(t,hz(95),.04,.05,decay=30); t+=2.0+rng.random()*3.5
# pasos amortiguados sobre moqueta en las escenas de caminata
for si,off in ((0,.6),(3,.4),(5,.5),(6,.8),(7,.5)):
    a0,a1=W(si); t=a0+off; sd=.52 if si!=5 else .6
    while t<a1-.3:
        m.noise(t,.12,.07,decay=22,lp=240); m.sine(t,hz(33),.12,.06,decay=18); t+=sd
# movil: toques y scroll
a0,a1=W(1)
for q in (.6,1.6,2.6,4.0,5.2): m.sine(a0+q,hz(100),.03,.05,decay=40); m.noise(a0+q,.04,.06,decay=50,hp=8)
# noclip: caida, chasquido y aterrizaje
a0,a1=W(2); m.noise(a0+2.9,.7,.2,decay=3,hp=5,att=.3); m.sine(a0+3.0,hz(96),.5,.1,decay=5,f2=hz(40)); m.noise(a0+3.05,.2,.25,decay=14,hp=10)
m.sine(a0+4.7,hz(31),.5,.3,decay=6); m.noise(a0+4.7,.25,.2,decay=14,lp=300)
# wiki: clics
a0,a1=W(4)
for q in (.8,2.6,4.4,6.0): m.noise(a0+q,.03,.08,decay=60,hp=8)
# metraje encontrado: ruido de cinta y latido grave
a0,a1=W(5); m.noise(a0,a1-a0,.045,decay=0,hp=7,att=.3)
q=a0+.4
while q<a1-.3: m.sine(q,hz(30),.2,.16,decay=9); m.sine(q+.22,hz(30),.2,.1,decay=9); q+=1.0
# sala enorme: crece un zumbido grave
a0,a1=W(6); m.sine(a0,hz(28),a1-a0,.08,att=2.5,rel=1.5)
# cierre: acorde frio
a0,a1=W(7)
for j,nn in enumerate([57,64,69,76]): m.sine(a0+.2+j*.15,hz(nn),2.6,.05,att=.4,decay=.8)
whooshes(m,TL); m.save("music.wav",gain=1.3,T=T)
