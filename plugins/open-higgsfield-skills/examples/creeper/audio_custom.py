import sys,json,math
sys.argv=["x"]
from sfxlib import *
TL=json.load(open("timeline.json")); T=TL["total"]; sc=TL["scenes"]; m=Mix(T)
rng=m.rng
# musica ambiental tipo piano suave (original): pentatonica, notas espaciadas con eco
PENT=[60,62,65,67,69,72,74,77]
t=0.3; i=0
while t<T:
    n=PENT[(i*3+(i//4))%8] - (12 if i%5==0 else 0)
    for k,(dly,amp) in enumerate([(0,.09),(.34,.04),(.68,.02)]):
        m.sine(t+dly,hz(n),1.8,amp,att=.01,rel=.5,decay=2.0); m.sine(t+dly,hz(n)*2,1.2,amp*.25,att=.01,rel=.3,decay=3.5)
    t+=rng.choice([.9,1.8,.9,2.7]); i+=1
for k in range(int(T/7)+1): m.sine(k*7,hz(36),7.6,.03,att=2,rel=2); m.sine(k*7,hz(43),7.6,.02,att=2,rel=2)
def idx_win(i): 
    s=sc[i]; e=sc[i+1]["start"] if i+1<len(sc) else T; return s["start"],e
def hiss(a,d,amp=.2,rise=True):
    n=int(d*SR); u=np.arange(n)/SR; z=rng.standard_normal(n)
    z=z-np.convolve(z,np.ones(8)/8,mode="same"); z=z-np.convolve(z,np.ones(3)/3,mode="same")*0.0
    e=(u/d) if rise else np.exp(-3*u)
    m.add(a,z*e,amp)
def step(a,amp=.12): m.noise(a,.09,amp,decay=30,lp=10); m.sine(a,90,.08,amp*.8,decay=30,f2=55)
def oink(a):
    for dly,f in((0,300),(.14,240)):
        m.sine(a+dly,f,.16,.1,att=.01,rel=.04,decay=5,f2=f*.65); m.sq(a+dly,f*.5,.14,.03,duty=.35,decay=6)
def click(a): m.noise(a,.03,.08,decay=90,hp=4)
# A: pasos en la hierba y siseo lejano
a0,a1=idx_win(0)
for k in range(int((a1-a0)/.42)): step(a0+k*.42,.07)
hiss(a0+(a1-a0)*.55,1.1,.07)
# B: teclas y oink del cerdo en el boceto
a0,a1=idx_win(1)
for k in range(40): click(a0+.4+k*(a1-a0-.8)/40+rng.random()*.05)
oink(a0+(a1-a0)*.7)
# C: sliders (blips que suben/bajan) y chasquido al encajar
a0,a1=idx_win(2); 
for k in range(24): m.sq(a0+1.0+k*.15,hz(60+k*1.0),.08,.04,duty=.25,decay=10)
m.sine(a1-1.2,hz(48),.4,.14,decay=6); m.noise(a1-1.2,.15,.08,decay=20,lp=4)
# D: duda: oink, nota interrogativa
a0,a1=idx_win(3); oink(a0+.6); 
for j,nn in enumerate([64,67,70]): m.sine(a0+1.4+j*.18,hz(nn),.3,.08,decay=4)
# E: pasos, siseo (mecha) y explosion
a0,a1=idx_win(4)
for k in range(8): step(a0+.3+k*.37,.1)
hiss(a0+3.0,1.0,.28)
b=a0+4.0
m.sine(b,90,1.4,.55,decay=3.2,f2=28); m.noise(b,1.2,.45,decay=3.5,lp=18); m.noise(b,.35,.35,decay=9,hp=5)
for k in range(10): m.sine(b+.25+k*.11,hz(60+k%5*2),.08,.04,decay=12); step(b+.5+k*.09+rng.random()*.1,.05)
# F: primer plano: siseos repetidos con latido grave
a0,a1=idx_win(5); 
for k in range(5): hiss(a0+.3+k*1.25,.9,.14); m.sine(a0+.3+k*1.25,48,.5,.1,decay=5)
# G: revelacion: campanitas ascendentes
a0,a1=idx_win(6)
for j,nn in enumerate([72,76,79,84,88]): m.sine(a0+.3+j*.14,hz(nn),.9,.08,decay=3.5); m.sine(a0+.3+j*.14,hz(nn)*2,.5,.03,decay=6)
whooshes(m,TL); m.save("music.wav",gain=1.3,T=T)
