import sys,json,math
sys.argv=["x"]
from sfxlib import *
TL=json.load(open("timeline.json")); T=TL["total"]; sc=TL["scenes"]; m=Mix(T); rng=m.rng
def W(i): s=sc[i]; e=sc[i+1]["start"] if i+1<len(sc) else T; return s["start"],e
for k in range(int(T/7)+2):
    m.sine(k*7,hz(38),7.6,.05,att=2,rel=2); m.sine(k*7,hz(45),7.6,.03,att=2,rel=2)
# piano frio y espaciado (sala segura) 
notes=[69,72,76,74,72,69,67,72]
t=1.0; j=0
while t<T:
    n=notes[j%8]; m.sine(t,hz(n),1.6,.07,att=.01,rel=.4,decay=2.2); m.sine(t,hz(n)*2,.9,.025,decay=4); t+=1.5 if j%4 else 2.4; j+=1
def creak(a,d=2.4,f0=140,f1=300,amp=.12):
    n=int(d*SR); u=np.arange(n)/SR; f=f0+(f1-f0)*(u/d)**1.6+14*np.sin(u*40)
    ph=2*np.pi*np.cumsum(f)/SR; sig=np.sign(np.sin(ph))*.5+np.sin(ph)*.5
    e=np.minimum(1,u/.15)*np.minimum(1,(d-u)/.3).clip(0,1); m.add(a,sig*e,amp)
def thud(a): m.sine(a,80,.4,.3,decay=8,f2=40); m.noise(a,.1,.15,decay=30,lp=8)
# D: puerta que se abre lentamente (crujido largo) mientras "carga"
a0,a1=W(3); creak(a0+1.0,a1-a0-1.4,120,260,.14)
for k in range(6): m.sq(a0+1.2+k*.7,hz(72+k),.05,.025,duty=.25,decay=20)
# E: latido y puerta
a0,a1=W(4); 
for k in range(int((a1-a0)/.62)): thud(a0+k*.62); m.sine(a0+k*.62+.2,60,.14,.18,decay=14,f2=35)
creak(a0+.6,3.2,110,230,.16); m.sine(a0+3.4,hz(40),1.4,.3,att=.3,decay=2.2); m.noise(a0+3.4,.8,.3,decay=5,hp=4)
# C: pitidos de carga de memoria (sube la presion)
a0,a1=W(2)
for k in range(24): m.sq(a0+.5+k*.28,hz(60+(k%8)),.07,.03,duty=.25,decay=12)
m.sine(a0+3.0,hz(50),a1-a0-3.0,.1,att=.3,f2=hz(70))
# F: sello de marca (golpe seco)
a0,a1=W(5); m.noise(a0+1.5,.12,.3,decay=28,lp=6); thud(a0+1.5)
# G: revelacion: acorde que abre
a0,a1=W(6)
for j,nn in enumerate([57,64,69,72]): m.sine(a0+.2+j*.1,hz(nn),2.4,.07,att=.05,decay=1.6)
whooshes(m,TL); m.save("music.wav",gain=1.3,T=T)
