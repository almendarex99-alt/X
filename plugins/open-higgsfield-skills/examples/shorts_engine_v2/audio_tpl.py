import sys,json,math
sys.argv=["x"]
from sfxlib import *
def make(root=33,motif=(57,60,64,60),step=.5,mamp=.05,pad=.06,hiss=.03,ev=None,mrange=None,octv=0,bright=0.0):
    TL=json.load(open("timeline.json")); T=TL["total"]; sc=TL["scenes"]; m=Mix(T); rng=m.rng
    def W(i): s=sc[i]; e=sc[i+1]["start"] if i+1<len(sc) else T; return s["start"],e
    for k in range(int(T/6)+2):
        m.sine(k*6,hz(root),6.6,pad,att=1.6,rel=1.6); m.sine(k*6,hz(root)*1.5,6.6,pad*.5,att=1.6,rel=1.6); m.noise(k*6,6,hiss,decay=0,lp=70,att=1.5)
    t=1.0; k=0
    while t<T-.5:
        nn=motif[k%len(motif)]+octv; m.sine(t,hz(nn),step*.9,mamp,att=.01,decay=6); m.sine(t,hz(nn+12),step*.7,mamp*.35,att=.01,decay=8)
        if bright: m.sine(t,hz(nn+19),step*.4,mamp*bright,att=.005,decay=12)
        t+=step; k+=1
    for (si,off,kind) in (ev or []):
        a0,a1=W(si); a=a0+off
        if a>=T-.3: continue
        if kind=="hit": m.noise(a,.3,.2,decay=10,hp=3); m.sine(a,hz(root+12),.35,.16,decay=7)
        elif kind=="tick": m.sine(a,hz(90),.05,.09,decay=26)
        elif kind=="coin": m.sine(a,hz(88),.07,.1,decay=18); m.sine(a+.08,hz(95),.12,.1,decay=16)
        elif kind=="noise": m.noise(a,.5,.12,decay=5,hp=4)
        elif kind=="bell": m.sine(a,hz(76),3.0,.07,att=.01,decay=.8); m.sine(a,hz(76)*2.76,1.6,.03,att=.01,decay=1.4)
        elif kind=="zap": m.sine(a,hz(96),.25,.09,decay=8,f2=hz(60)); m.noise(a,.15,.1,decay=14,hp=8)
        elif kind=="thud": m.sine(a,hz(root+5),.4,.22,decay=7); m.noise(a,.15,.12,decay=18,lp=200)
        elif kind=="click": m.noise(a,.03,.2,decay=60,hp=8)
        elif kind=="whoosh": m.noise(a,.6,.1,decay=4,hp=5,att=.3)
    a0,a1=W(6)
    for j,nn in enumerate([motif[0]+12,motif[1]+12,motif[2]+12,motif[0]+24]): m.sine(a0+.4+j*.15,hz(nn),2.2,.06,att=.3,decay=1.0)
    whooshes(m,TL); m.save("music.wav",gain=1.3,T=T)
