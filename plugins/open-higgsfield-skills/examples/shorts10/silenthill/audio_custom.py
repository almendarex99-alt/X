import sys,json,math
sys.argv=["x"]
from sfxlib import *
TL=json.load(open("timeline.json")); T=TL["total"]; sc=TL["scenes"]; m=Mix(T); rng=m.rng
def W(i): s=sc[i]; e=sc[i+1]["start"] if i+1<len(sc) else T; return s["start"],e
# ambiente industrial grave y metalico (inspirado, original)
for k in range(int(T/5)+2):
    m.sine(k*5,hz(28),5.6,.06,att=1.4,rel=1.4); m.sine(k*5,hz(28)*1.498,5.6,.03,att=1.4,rel=1.4)
    m.noise(k*5+2,2.4,.05,decay=0,lp=60,att=.8)
for k in range(int(T/1.2)):
    t=k*1.2+rng.random()*.3
    if rng.random()<.5: m.sine(t,hz(48+int(rng.random()*6)),.9,.03,decay=3.2); m.noise(t,.15,.04,decay=20,hp=5)
def static(a,d,amp,rise=False):
    n=int(d*SR); u=np.arange(n)/SR; z=rng.standard_normal(n); z=z-np.convolve(z,np.ones(6)/6,mode="same")
    e=(u/d)**1.2 if rise else np.exp(-u*3); m.add(a,z*e*amp*(.5+.5*np.sign(np.sin(u*37))),1.0)
a0,a1=W(2)
for k in range(16): m.sq(a0+.6+k*.3,hz(46+(k%5)),.06,.025,duty=.25,decay=14)
a0,a1=W(3); m.noise(a0+1.8,3.2,.08,decay=0,lp=80,att=1.8)
# F: la radio crepita mas cuanto mas cerca esta
a0,a1=W(5)
for k in range(14):
    t=a0+.3+k*.42; amp=.07+.35*(k/14.0)**1.4; static(t,.3,amp); 
m.sine(a0+4.0,hz(41),a1-a0-4.0,.2,att=1.2,f2=hz(36))
a0,a1=W(6)
for j,nn in enumerate([45,52,57]): m.sine(a0+.2+j*.15,hz(nn),3.0,.07,att=.4,decay=.9)
whooshes(m,TL); m.save("music.wav",gain=1.3,T=T)
