import sys,json,math
sys.argv=["x"]
from sfxlib import *
import vid
TL=json.load(open("timeline.json")); T=TL["total"]; sc=TL["scenes"]; m=Mix(T)
BASS=[55.0,51.9,49.0,46.2]   # marcha descendente de 4 notas (referencia sonora del arcade original)
# ambiente muy suave
for k in range(int(T/6)+2): m.sine(k*6,hz(33),6.2,.025,att=1.5,rel=1.5)
def window(idx,fn_t,vol=1.0,ticks=True,shots=True):
    s=sc[idx]; end=sc[idx+1]["start"] if idx+1<len(sc) else T; dur=end-s["start"]
    prev=None; note=0; lastn=None; pbprev=None
    for i in range(int(dur*30)):
        u=i/30.0; ts=fn_t(u); sn=vid.snap(ts); a=s["start"]+u
        if ticks:
            if prev is not None and sn["frame"]!=prev:
                f=BASS[note%4]; note+=1
                m.sine(a,f,.11,.2*vol,att=.002,rel=.04,decay=6); m.sq(a,f*2,.07,.05*vol,duty=.25,decay=12)
            prev=sn["frame"]
        if shots:
            if sn["pb"] is not None and pbprev is None: m.sine(a,1400,.16,.09*vol,decay=10,f2=250); 
            pbprev=sn["pb"]
            if lastn is not None and sn["n"]<lastn: m.noise(a,.28,.18*vol,decay=11,lp=14); m.sine(a,120,.22,.12*vol,decay=9,f2=40)
            lastn=sn["n"]
window(0,lambda u:u)
window(1,lambda u:u*1.2+10,.35)
# C: la marcha sigue el ritmo del procesador (menos invasores -> intervalos mas cortos)
s=sc[2]; end=sc[3]["start"]; a=s["start"]; note=0
while a<end:
    u=a-s["start"]; n=max(3,int(55-u*7.2)); iv=0.018+0.0165*n
    f=BASS[note%4]; note+=1
    m.sine(a,f,min(.11,iv*.9),.16,att=.002,rel=.03,decay=6); a+=max(.03,iv*1.0)
    if note%4==0 and u<4: pass
# D: tono que sube con la velocidad real (cronologia acelerada)
s=sc[3]; end=sc[4]["start"]; dur=end-s["start"]
for i in range(int(dur*30)):
    u=i/30.0; t0=min(77.0,u*10.5); sn=vid.snap(t0); f=110+ (1/sn["interval"])*22
    m.sine(s["start"]+u,f,.05,.05,att=.005,rel=.02)
window(5,lambda u:max(0,(next((i/30.0 for i,sn in enumerate(vid.SIM) if i>300 and sn["n"]==55),80.0))-5.6+u),1.2)
# latido de miedo en F
s=sc[5]; end=sc[6]["start"]; a=s["start"]
while a<end:
    m.sine(a,60,.18,.2,decay=14,f2=35); m.sine(a+.22,55,.14,.16,decay=16,f2=35); a+=3.14/3.2*1.0
# G: OVNI con trino y revelacion
s=sc[6]; end=sc[7]["start"]
for i in range(int((end-s["start"])*60)):
    u=i/60.0; ux=(u*80)%700-80
    if 0<ux<540: m.sine(s["start"]+u,880+260*math.sin(u*38),.02,.03,att=.002,rel=.01)
for j,nn in enumerate([72,76,79,84]): m.sq(s["start"]+.4+j*.1,hz(nn),.18,.06,decay=4)
window(7,lambda u:u+30,.9)
whooshes(m,TL); m.save("music.wav",gain=1.4,T=T)
