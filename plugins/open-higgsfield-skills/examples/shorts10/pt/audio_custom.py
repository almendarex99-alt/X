import sys,json,math
sys.argv=["x"]
from sfxlib import *
TL=json.load(open("timeline.json")); T=TL["total"]; sc=TL["scenes"]; m=Mix(T); rng=m.rng
def W(i): s=sc[i]; e=sc[i+1]["start"] if i+1<len(sc) else T; return s["start"],e
for k in range(int(T/6)+2): m.sine(k*6,hz(33),6.6,.05,att=1.6,rel=1.6); m.noise(k*6,6,.03,decay=0,lp=50,att=1.5)
def static(a,d,amp):
    n=int(d*SR); u=np.arange(n)/SR; z=rng.standard_normal(n); z=z-np.convolve(z,np.ones(5)/5,mode="same"); m.add(a,z*np.exp(-u*5)*amp,1.0)
def step(a,amp=.12): m.noise(a,.1,amp,decay=26,lp=9); m.sine(a,90,.12,amp*.8,decay=22,f2=50)
# A/E: radio e indicacion de tienda (pitidos de interfaz)
a0,a1=W(0)
for j,nn in enumerate([76,79,83]): m.sine(a0+1.0+j*.12,hz(nn),.2,.05,decay=9)
m.sine(a0+2.2,hz(40),1.6,.18,att=.2,decay=1.8,f2=hz(34)); static(a0+2.0,.5,.3)
# C: pasos y bucle; cada vuelta mas grave y con estatica
a0,a1=W(2)
for k in range(int((a1-a0)/.5)): step(a0+k*.5,.11)
for lap in range(1,5): m.sine(a0+lap*1.8,hz(52-lap*3),1.2,.12,att=.1,decay=1.4); static(a0+lap*1.8,.3,.12*lap)
# D: revelacion
a0,a1=W(3)
for i in range(3): 
    t=a0+.5+i*1.2; m.sine(t,hz(60+i*4),.4,.08,decay=5); m.sine(t,hz(72+i*4),.3,.03,decay=7)
m.sine(a0+4.2,hz(43),2.0,.14,att=.4,decay=1.5); 
# E: campanada de cancelacion
a0,a1=W(4); 
m.sine(a0+2.6,hz(40),2.4,.4,decay=1.6); m.sine(a0+2.6,hz(40)*2.76,1.6,.14,decay=2.2); m.noise(a0+2.6,.12,.3,decay=28,lp=6)
# F: tono de acceso denegado
a0,a1=W(5); 
for j in range(2): m.sq(a0+2.2+j*.18,hz(52),.14,.06,duty=.5,decay=6)
a0,a1=W(6); 
for j,nn in enumerate([45,52,57]): m.sine(a0+.2+j*.2,hz(nn),3.4,.07,att=.5,decay=.8)
whooshes(m,TL); m.save("music.wav",gain=1.3,T=T)
