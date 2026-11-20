import sys,json,math
sys.argv=["x"]
from sfxlib import *
TL=json.load(open("timeline.json")); T=TL["total"]; sc=TL["scenes"]; m=Mix(T); rng=m.rng
def W(i): s=sc[i]; e=sc[i+1]["start"] if i+1<len(sc) else T; return s["start"],e
# ambiente de bosque: viento, grillos, crujidos
for k in range(int(T/3)+2): m.noise(k*3,3.3,.05,decay=0,lp=90,att=1.0)
for k in range(int(T*2)):
    if rng.random()<.45: t=k*.5; m.sine(t,3200+rng.random()*600,.05,.012,decay=30); m.sine(t+.08,3200+rng.random()*600,.05,.012,decay=30)
for k in range(int(T/4)+1): m.sine(k*4,hz(31),4.4,.07,att=1.2,rel=1.2)
def step(a,amp=.1): m.noise(a,.12,amp,decay=20,lp=12); m.sine(a,70,.1,amp*.8,decay=22,f2=45)
def snap(a): m.noise(a,.05,.2,decay=50,hp=3); m.sine(a,300,.06,.05,decay=40)
a0,a1=W(4)
for k in range(int((a1-a0)/.45)): step(a0+k*.45,.1)
for k in range(8): m.sine(a0+k*.8+.1,hz(81),.5,.06,decay=5); m.sine(a0+k*.8+.1,hz(88),.4,.03,decay=7)
a0,a1=W(1)
for k in range(30): m.noise(a0+.5+k*.25,.02,.05,decay=80,hp=3)
a0,a1=W(2)
for k in range(18): m.sine(a0+.4+k*.27,hz(70+(k*5)%12),.3,.04,decay=7)
# F: estatica creciente y latido
a0,a1=W(5)
n=int((a1-a0)*SR); u=np.arange(n)/SR; z=rng.standard_normal(n); z=z-np.convolve(z,np.ones(4)/4,mode="same"); m.add(a0,z*(u/(a1-a0))**2*.4*(.5+.5*np.sign(np.sin(u*53))),1.0)
for k in range(int((a1-a0)/.7)): m.sine(a0+k*.7,60,.16,.2,decay=14,f2=36)
a0,a1=W(6); 
for j,nn in enumerate([43,50,55]): m.sine(a0+.2+j*.2,hz(nn),3.0,.07,att=.4,decay=.9)
whooshes(m,TL); m.save("music.wav",gain=1.3,T=T)
