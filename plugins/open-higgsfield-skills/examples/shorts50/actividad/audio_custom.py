import sys,json,math
sys.argv=["x"]
from sfxlib import *
TL=json.load(open("timeline.json")); T=TL["total"]; sc=TL["scenes"]; m=Mix(T); rng=m.rng
def W(i): s=sc[i]; e=sc[i+1]["start"] if i+1<len(sc) else T; return s["start"],e
# casi silencio: zumbido grave de habitacion, pisadas lejanas, un golpe
for k in range(int(T/7)+2): m.sine(k*7,hz(28),7.6,.06,att=1.8,rel=1.8); m.noise(k*7,7,.02,decay=0,lp=60,att=1.8)
for k in range(int(T/1.1)): m.sine(k*1.1,hz(52),.05,.04,decay=30)    # tic de camara
for t in (5.0,17.0,29.0): m.noise(t,.12,.2,decay=25,hp=4); m.sine(t,hz(40),.3,.13,decay=7)
a0,a1=W(2)
for k in range(6): m.noise(a0+1+k*.9,.1,.1,decay=28,hp=8)   # pasos
a0,a1=W(5)
for k in range(8): m.sine(a0+.8+k*.3,hz(95),.05,.06,decay=26)
a0,a1=W(6); m.sine(a0+1.0,hz(76),3.0,.04,att=1.0,decay=.5)
whooshes(m,TL); m.save("music.wav",gain=1.3,T=T)
