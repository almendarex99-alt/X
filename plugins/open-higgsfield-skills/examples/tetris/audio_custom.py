import sys,json
sys.argv=["x"]
from sfxlib import *
import vid
TL=json.load(open("timeline.json")); T=TL["total"]; sc=TL["scenes"]; m=Mix(T)
# Korobeiniki (Tetris Type A), melodia folclorica rusa de dominio publico, en onda cuadrada tipo Game Boy
E5,B4,C5,D5,A4,F5,A5,G5=76,71,72,74,69,77,81,79
q=.4; e=.2
mel=[(E5,q),(B4,e),(C5,e),(D5,q),(C5,e),(B4,e),(A4,q),(A4,e),(C5,e),(E5,q),(D5,e),(C5,e),(B4,q+e),(C5,e),(D5,q),(E5,q),(C5,q),(A4,q),(A4,q*2),
     (D5,q+e),(F5,e),(A5,q),(G5,e),(F5,e),(E5,q+e),(C5,e),(E5,q),(D5,e),(C5,e),(B4,q),(B4,e),(C5,e),(D5,q),(E5,q),(C5,q),(A4,q),(A4,q*2)]
t=0.25; bass_root=[45,40,45,40]
while t<T+1:
    for n,d in mel:
        if t>T+1: break
        m.sq(t,hz(n),d*.92,.055,duty=.5,att=.005,rel=.04)
        m.sq(t,hz(n)*2.0,d*.5,.012,duty=.25)
        t+=d
t=0.25; k=0
while t<T+1:
    for i in range(8):
        r=[45,52,40,47,45,52,40,47][i]; m.sq(t,hz(r-12),.17,.05,duty=.25); m.sq(t+.2,hz(r-12+12),.12,.03,duty=.25); t+=.4
# efectos de juego sincronizados con la simulacion real
def events(P,t0,t1,off,scale=1.0):
    for p in P:
        tl=p["tl"]; u=(tl-off)/scale
        if 0<=u<t1-t0:
            a=t0+u
            m.sine(a,150,.12,.16,decay=18,f2=60)          # bloqueo de pieza
            m.noise(a,.05,.06,decay=60,lp=6)
            if p["full"]:
                n=len(p["full"])
                notes=[84,88,91,96] if n<4 else [72,76,79,84,88,91,96,100]
                for i,nn in enumerate(notes): m.sq(a+.05+i*.06,hz(nn),.09,.07,duty=.5,decay=6)
for idx,(simname,off) in {0:("SIM",0),5:("SIM",8),6:("SIMF",0),7:("SIM",6)}.items():
    s=sc[idx]; end=sc[idx+1]["start"] if idx+1<len(sc) else T
    events(getattr(vid,simname),s["start"],end,off)
# giro de pieza y whoosh
for p in vid.SIM[:12]:
    pass
whooshes(m,TL)
m.save("music.wav",gain=1.3,T=T)
