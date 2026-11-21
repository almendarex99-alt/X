import sys,json,math
sys.argv=["x"]
from sfxlib import *
TL=json.load(open("timeline.json")); T=TL["total"]; sc=TL["scenes"]; m=Mix(T); rng=m.rng
def W(i): s=sc[i]; e=sc[i+1]["start"] if i+1<len(sc) else T; return s["start"],e
# melodia chiptune original, alegre (do mayor), con bajo saltarin
mel=[(76,.2),(76,.2),(0,.2),(76,.2),(0,.2),(72,.2),(76,.4),(79,.4),(0,.4),(67,.4),(0,.4)]*0
phr=[72,76,79,76,72,67,72,76,79,84,79,76,72,74,77,81,77,74,69,74,77,81,84,81,77]
t=0.2; i=0
while t<T+1:
    n=phr[i%len(phr)]; m.sq(t,hz(n),.16,.05,duty=.25,decay=3); t+=.2; i+=1
t=0.2; j=0
while t<T+1:
    b=[48,48,55,55,53,53,55,55][j%8]; m.sq(t,hz(b-12),.16,.05,duty=.5); m.sq(t+.1,hz(b),.08,.03,duty=.25); t+=.4; j+=1
def coin(a): m.sq(a,hz(83),.06,.08,duty=.5); m.sq(a+.06,hz(88),.3,.08,duty=.5,decay=5)
def bloop(a,f=70): m.sq(a,hz(f),.08,.07,duty=.25,decay=12); m.sq(a+.08,hz(f+7),.14,.07,duty=.25,decay=8)
a0,a1=W(0)
for k in range(3): coin(a0+.6+k*1.3)
a0,a1=W(2)
for k in range(40): m.sq(a0+.3+k*.12,hz(60+k%12),.05,.03,duty=.5,decay=20)
m.sine(a0+4.5,hz(40),1.0,.2,decay=3,f2=hz(30))
a0,a1=W(3)
for k in range(4): bloop(a0+.4+k*1.0,60+k*3)
a0,a1=W(4)
for k in range(8): bloop(a0+.5+k*1.2,64+(k%2)*5)
a0,a1=W(6)
for j,nn in enumerate([72,76,79,84]): m.sq(a0+.2+j*.1,hz(nn),.3,.08,decay=3)
whooshes(m,TL); m.save("music.wav",gain=1.2,T=T)
