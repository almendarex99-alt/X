import sys,json,math
sys.argv=["x"]
from sfxlib import *
TL=json.load(open("timeline.json")); T=TL["total"]; sc=TL["scenes"]; m=Mix(T); rng=m.rng
def W(i): s=sc[i]; e=sc[i+1]["start"] if i+1<len(sc) else T; return s["start"],e
# ventilador y zumbido electrico constantes
for k in range(int(T/2)+2): m.noise(k*2,2.1,.045,decay=0,lp=40,att=.2)
for k in range(int(T/6)+2): m.sine(k*6,hz(31),6.4,.04,att=1.6,rel=1.6); m.sine(k*6,hz(31)*1.5,6.4,.02,att=1.6,rel=1.6)
# caja de musica (nana) en las escenas tiernas B y D
mel=[67,70,74,72,70,67,65,67,70,74,77,74,72,70]
for i in (1,3):
    a0,a1=W(i); t=a0+.2; j=0
    while t<a1-.3:
        n=mel[j%len(mel)]; m.sine(t,hz(n+12),1.4,.05,att=.005,rel=.2,decay=2.6); m.sine(t,hz(n+24),.8,.018,decay=5); t+=.42; j+=1
def bell(a): m.sine(a,hz(79),1.8,.12,decay=1.7); m.sine(a,hz(79)*2.01,1.2,.05,decay=2.6); m.sine(a,hz(55),1.5,.05,decay=2)
def slam(a): m.noise(a,.25,.4,decay=14,lp=14); m.sine(a,70,.4,.5,decay=7,f2=35); m.noise(a+.02,.08,.2,decay=40,hp=5)
def sting(a,amp=.5): 
    m.noise(a,.9,amp*.8,decay=4,hp=3); m.sine(a,500,.9,amp*.3,decay=3,f2=1800); m.sine(a,90,.9,amp*.5,decay=5,f2=30)
# A: gancho oscuro
a0,a1=W(0); m.sine(a0+1.2,60,2.0,.2,att=.8,rel=.6,f2=48)
# C: critica -> inquietante (zumbidos que se deforman)
a0,a1=W(2)
for k in range(4): m.sine(a0+.8+k*.9,hz(60+k*3),.5,.06,decay=4)
m.sine(a0+1,hz(52),a1-a0-1,.12,att=2.5,rel=1.2,f2=hz(46)); m.noise(a0+a1*0,0.1,0)
# E: puertas, energia y campanadas de las 6 AM
a0,a1=W(4); slam(a0+2.4); slam(a0+4.3); m.sine(a0+4.7,300,2.0,.1,att=.3,rel=.5,f2=90)
for k in range(3): bell(a1-1.5+k*.5)
# F: cortes de camara con estatica y golpes
a0,a1=W(5)
for k in range(4):
    a=a0+k*1.6; m.noise(a,.2,.3,decay=9,lp=2); m.sine(a,hz(40+k*3),1.0,.2,decay=3)
sting(a0+4.8,.7)
# G: viral
a0,a1=W(6)
for k in range(10): m.sine(a0+.3+k*.4,hz(76+(k%4)*2),.2,.04,decay=9)
whooshes(m,TL); m.save("music.wav",gain=1.35,T=T)
