import sys,json,math
sys.argv=["x"]
from sfxlib import *
TL=json.load(open("timeline.json")); T=TL["total"]; sc=TL["scenes"]; m=Mix(T); rng=m.rng
def W(i): s=sc[i]; e=sc[i+1]["start"] if i+1<len(sc) else T; return s["start"],e
# ducha constante
for k in range(int(T/1.0)+1): m.noise(k*1.0,1.1,.06,decay=0,lp=4,att=.05)
# violines estridentes originales (glissandos agudos y rasposos) inspirados en la tension del cine clasico
def screech(a,d=.5,f0=1600,f1=2400,amp=.14):
    n=int(d*SR); u=np.arange(n)/SR; f=f0+(f1-f0)*np.sin(u/d*math.pi*1.2); ph=2*np.pi*np.cumsum(f)/SR
    sig=np.sign(np.sin(ph))*.4+np.sin(ph)*.6+.2*np.sin(ph*2.03)
    e=np.minimum(1,u/.01)*np.exp(-u*3); m.add(a,sig*e,amp)
a0,a1=W(4)
for k in range(8): screech(a0+.6+k*.55,.5,1500+k*110,2300-k*60,.13)
a0,a1=W(5); screech(a0+.2,.8,1800,2600,.1)
a0,a1=W(6)
for k in range(5): screech(a0+.3+k*.18,.4,1700+k*160,2600,.15)
m.sine(a0+.2,hz(36),2.0,.3,decay=2)
a0,a1=W(2)
for k in range(10): m.noise(a0+.6+k*.3,.18,.08,decay=12,lp=10); m.sine(a0+.6+k*.3,hz(48+k),.12,.04,decay=18)  # goteo espeso
a0,a1=W(3)
for k in range(45): m.noise(a0+k*(5.0/45)+.1,.015,.12,decay=90,hp=3)  # cortes de montaje (clics)
a0,a1=W(1)
for k in range(5): m.noise(a0+.6+k*1.3,.06,.14,decay=40,hp=3)
for k in range(int(T/6)+2): m.sine(k*6,hz(30),6.4,.05,att=1.6,rel=1.6)
# cuchilladas de cuerda: notas cortas muy agudas que suben de semitono
a0,a1=W(6)
for k in range(8): screech(a0+1.6+k*.16,.12,2200+k*140,2600+k*140,.16)
whooshes(m,TL); m.save("music.wav",gain=1.3,T=T)
