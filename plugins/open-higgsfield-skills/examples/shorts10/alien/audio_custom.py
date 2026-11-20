import sys,json,math
sys.argv=["x"]
from sfxlib import *
TL=json.load(open("timeline.json")); T=TL["total"]; sc=TL["scenes"]; m=Mix(T); rng=m.rng
def W(i): s=sc[i]; e=sc[i+1]["start"] if i+1<len(sc) else T; return s["start"],e
# nave: zumbido de motores y pitidos electronicos
for k in range(int(T/5)+2): m.sine(k*5,hz(27),5.6,.08,att=1.4,rel=1.4); m.sine(k*5,hz(27)*1.5,5.6,.04,att=1.4,rel=1.4); m.noise(k*5,5,.035,decay=0,lp=50,att=1.2)
for k in range(int(T/1.7)):
    t=k*1.7+rng.random(); m.sq(t,hz(88+int(rng.random()*8)),.07,.022,duty=.25,decay=14)
a0,a1=W(1)
for k in range(5): m.noise(a0+.6+k*1.3,.06,.14,decay=40,hp=3)
a0,a1=W(3)
for k in range(24): m.sq(a0+.4+k*.16,hz(70+int(k*1.3)),.05,.03,duty=.25,decay=16)   # presion subiendo
m.sine(a0+.3,hz(46),4.2,.1,att=.5,rel=.4,f2=hz(70))
# E: explosion de sangre falsa: golpe seco + chorro
a0,a1=W(4); b=a0+1.4
m.sine(b,80,.9,.5,decay=3.6,f2=34); m.noise(b,.9,.4,decay=3.4,lp=10); m.noise(b,.25,.3,decay=14,hp=4)
for k in range(8): m.noise(b+.3+k*.06,.1,.12,decay=24,lp=4)
m.sine(b+.2,hz(88),1.6,.08,decay=1.6,f2=hz(60))
a0,a1=W(5)
for k in range(6): m.sine(a0+.3+k*.35,hz(70+k),.2,.05,decay=7)
a0,a1=W(6)
for j,nn in enumerate([52,59,64,71]): m.sine(a0+.2+j*.12,hz(nn),3.0,.07,att=.3,decay=1.0)
whooshes(m,TL); m.save("music.wav",gain=1.3,T=T)
