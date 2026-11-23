import sys,json,math
sys.argv=["x"]
from sfxlib import *
TL=json.load(open("timeline.json")); T=TL["total"]; sc=TL["scenes"]; m=Mix(T); rng=m.rng
def W(i): s=sc[i]; e=sc[i+1]["start"] if i+1<len(sc) else T; return s["start"],e
for k in range(int(T/5)+2): m.sine(k*5,hz(31),5.6,.07,att=1.4,rel=1.4); m.sine(k*5,hz(31)*1.5,5.6,.03,att=1.4,rel=1.4); m.noise(k*5,5,.045,decay=0,lp=2000,att=1.2)  # viento helado
# campana tubular espaciada (original)
for j,(t,nn) in enumerate([(1.0,76),(5.5,69),(10.0,76),(18.0,72),(26.0,76),(34.0,69)]):
    if t<T-2: m.sine(t,hz(nn),3.5,.06,att=.01,decay=.7); m.sine(t,hz(nn)*2.76,2.0,.03,att=.01,decay=1.2)
a0,a1=W(2)
for k in range(int((a1-a0)/1.3)): m.noise(a0+k*1.3,1.0,.07,decay=2.5,hp=5)  # aire acondicionado
a0,a1=W(3)
for k in range(int((a1-a0)/1.5)): m.noise(a0+k*1.5+.1,.9,.09,decay=3.0,lp=2500,att=.3)  # respiracion
a0,a1=W(4)
for q in (1.2,2.8,4.2): m.noise(a0+q,.3,.18,decay=12,hp=3); m.sine(a0+q,hz(44),.25,.14,decay=10)
a0,a1=W(5); m.sine(a0+.8,hz(88),1.5,.07,att=.4,decay=1.5); m.sine(a0+.8,hz(94),1.5,.06,att=.4,decay=1.5)
whooshes(m,TL); m.save("music.wav",gain=1.3,T=T)
