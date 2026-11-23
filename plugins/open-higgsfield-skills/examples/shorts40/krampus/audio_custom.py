import sys,json,math
sys.argv=["x"]
from sfxlib import *
TL=json.load(open("timeline.json")); T=TL["total"]; sc=TL["scenes"]; m=Mix(T); rng=m.rng
def W(i): s=sc[i]; e=sc[i+1]["start"] if i+1<len(sc) else T; return s["start"],e
# viento helado que sube y baja + tono grave
for k in range(int(T/4)+2):
    m.noise(k*4,4.6,.05+.03*math.sin(k*1.3),decay=0,lp=900,att=1.3); m.sine(k*4,hz(36),4.6,.05,att=1.3,rel=1.3); m.sine(k*4,hz(43),4.6,.025,att=1.3,rel=1.3)
def bells(a,n=6,gap=.07,amp=.035):
    for q in range(n): m.sine(a+q*gap+rng.random()*.03,hz(98+int(rng.random()*8)),.35,amp,att=.002,decay=10); m.sine(a+q*gap,hz(110+int(rng.random()*6)),.25,amp*.6,att=.002,decay=14)
def chain(a): 
    for q in range(7): m.noise(a+q*.045,.04,.1,decay=45,hp=8); m.sine(a+q*.045,hz(82+q%3),.04,.04,decay=40)
def step(a): m.noise(a,.09,.1,decay=26,lp=500); m.sine(a,hz(30),.1,.09,decay=18)
def churchbell(a): m.sine(a,hz(52),4.0,.09,att=.01,decay=.7); m.sine(a,hz(52)*2.76,2.2,.04,att=.01,decay=1.2); m.sine(a,hz(52)*5.4,1.0,.02,att=.01,decay=2.2)
churchbell(.8); churchbell(5.8)
# pasos en la nieve + cascabeles (escenas con Krampus andando)
for si in (0,3,7):
    a0,a1=W(si); t=a0+.5
    while t<a1-.3: step(t); bells(t+.12,4); t+=.62
for si in (0,2,3): 
    a0,a1=W(si)
    for q in range(int((a1-a0)/1.6)): chain(a0+1.0+q*1.6)
# desfile: muchos cascabeles, crepitar de antorchas y golpes de tambor
a0,a1=W(4); t=a0+.2
while t<a1-.2: bells(t,5,.05,.04); step(t+.05); m.noise(t+.3,.04,.12,decay=50,hp=6); m.sine(t,hz(33),.2,.15,decay=7); t+=.55
for q in range(int((a1-a0)/.12)): 
    if rng.random()<.5: m.noise(a0+q*.12,.03,.05,decay=60,hp=9)
# mapa y postales: papel y toques
a0,a1=W(1)
for q in (.8,2.6,4.4): m.noise(a0+q,.15,.08,decay=18,hp=5); m.sine(a0+q,hz(70),.08,.05,decay=20)
a0,a1=W(5)
for q in (.8,1.6,2.6,3.6): m.noise(a0+q,.12,.09,decay=22,hp=4)
# cine: proyector y golpe de susto
a0,a1=W(6); q=a0
while q<a1: m.noise(q,.02,.06,decay=70,hp=8); q+=.06
m.sine(a0+2.2,hz(31),.8,.25,decay=4); m.noise(a0+2.2,.3,.25,decay=10,lp=400)
# remate: campana lejana y acorde frio
a0,a1=W(7)
churchbell(a0+.3)
for j,nn in enumerate([57,64,69,76]): m.sine(a0+.5+j*.15,hz(nn),2.6,.05,att=.4,decay=.8)
whooshes(m,TL); m.save("music.wav",gain=1.3,T=T)
