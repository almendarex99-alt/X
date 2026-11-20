import sys,json,math
sys.argv=["x"]
from sfxlib import *
TL=json.load(open("timeline.json")); T=TL["total"]; sc=TL["scenes"]; m=Mix(T); rng=m.rng
def W(i): s=sc[i]; e=sc[i+1]["start"] if i+1<len(sc) else T; return s["start"],e
# olas constantes
for k in range(int(T/2.4)+2): m.noise(k*2.4,3.0,.07,decay=0,lp=140,att=1.0)
# motivo de dos notas graves (original, inspirado en el suspense del tiburon): E - F, cada vez mas rapido
def motif(t0,t1):
    t=t0; gap=.9
    while t<t1:
        m.sine(t,hz(40),.35,.28,att=.01,decay=4); m.sine(t+gap*.5,hz(41),.35,.3,att=.01,decay=4)
        t+=gap; gap=max(.22,gap*.88)
for i in (0,4): a0,a1=W(i); motif(a0+.4,a1-.2)
a0,a1=W(6); motif(a0,a0+1.6)
# C: chirridos y chispas de las averias
a0,a1=W(2)
for k in range(14): m.noise(a0+.4+k*.45,.08,.1,decay=30,hp=3); m.sine(a0+.4+k*.45,hz(88+(k%3)*3),.1,.03,decay=14)
for k in range(3): m.sine(a0+1.0+k*1.9,hz(36),.6,.22,decay=3.2,f2=hz(30))
a0,a1=W(1)
for k in range(5): m.noise(a0+.6+k*1.2,.06,.14,decay=40,hp=3)   # claqueta
a0,a1=W(5)
for k in range(8): m.sine(a0+.5+k*.4,hz(55+k),.06,.03,decay=30)  # murmullos de sala
m.sine(a0+3.2,hz(41),1.2,.3,att=.04,decay=2); m.noise(a0+3.2,.3,.3,decay=8,lp=20)
whooshes(m,TL); m.save("music.wav",gain=1.3,T=T)
