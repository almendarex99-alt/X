import numpy as np, wave
sr=44100; T=52.0; n=int(sr*T); out=np.zeros(n); rng=np.random.default_rng(3)
bpm=100; beat=60/bpm
def f(m): return 440*2**((m-69)/12)
def tone(freq,dur,nh=10,p=1.0,att=0.005,dec=6.0,det=0.0):
    k=int(dur*sr); t=np.arange(k)/sr; y=np.zeros(k)
    for h in range(1,nh+1):
        if freq*h>sr*0.45: break
        y+=np.sin(2*np.pi*freq*h*t+h)/h**p
        if det: y+=np.sin(2*np.pi*freq*(1+det)*h*t)/h**p
    env=np.minimum(1,t/att)*np.exp(-t*dec); return y*env
def put(buf,y,pos):
    i=int(pos*sr); j=min(n,i+len(y))
    if i<n: buf[i:j]+=y[:j-i]
chords=[(45,[57,60,64]),(41,[53,57,60]),(48,[55,60,64]),(43,[55,59,62])]   # Am F C G
bass=np.zeros(n);pad=np.zeros(n);arp=np.zeros(n);drums=np.zeros(n);kicks=[]
bars=int(T/(beat*4))+1
for b in range(bars):
    root,ch=chords[b%4];t0=b*beat*4
    for i in range(8):
        put(bass,tone(f(root+(12 if i%4==3 else 0)),beat*0.5,nh=9,p=1.0,att=0.004,dec=5.5),t0+i*beat*0.5)
    for m in ch:
        put(pad,tone(f(m),beat*4.1,nh=7,p=1.2,att=0.35,dec=0.25,det=0.004),t0)
    seq=[ch[0],ch[1],ch[2],ch[1]]
    for i in range(16):
        put(arp,tone(f(seq[i%4]+12),beat*0.4,nh=5,p=1.4,att=0.003,dec=11),t0+i*beat*0.25)
    for i in range(4):
        kicks.append(t0+i*beat)
        d=int(0.35*sr);tt=np.arange(d)/sr;fr=45+130*np.exp(-tt*28);ph=2*np.pi*np.cumsum(fr)/sr;put(drums,0.95*np.sin(ph)*np.exp(-tt*9),t0+i*beat)
        if i%2==1:
            d=int(0.25*sr);tt=np.arange(d)/sr;sn=(rng.standard_normal(d)*0.6+np.sin(2*np.pi*190*tt))*np.exp(-tt*16);put(drums,0.5*sn,t0+i*beat)
    for i in range(8):
        d=int(0.05*sr);tt=np.arange(d)/sr;hh=np.diff(rng.standard_normal(d+1))*np.exp(-tt*70);put(drums,0.22*hh*(1.4 if i%2 else 0.8),t0+i*beat*0.5)
# sidechain pad/bass on kicks
sc=np.ones(n)
for kt in kicks:
    i=int(kt*sr);d=int(0.28*sr);j=min(n,i+d)
    if i<n: sc[i:j]=np.minimum(sc[i:j],1-0.65*np.exp(-np.arange(j-i)/sr*9))
mix=0.55*bass*sc+0.18*pad*sc+0.16*arp+0.5*drums
t=np.arange(n)/sr
mix*=np.minimum(1,t/1.2)*np.minimum(1,(T-t)/2.0)
mix=mix/np.abs(mix).max()*0.7
with wave.open("music_neon.wav","wb") as w:
    w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((mix*32767).astype(np.int16).tobytes())
print("music ok")
