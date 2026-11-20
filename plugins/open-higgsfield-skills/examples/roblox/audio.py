import numpy as np, json, wave
SR=44100; TL=json.load(open("timeline.json")); S=[s["start"] for s in TL["scenes"]]+[TL["total"]]; T=TL["total"]
N=int((T+1)*SR); mus=np.zeros(N,np.float32); sfx=np.zeros(N,np.float32)
def add(buf,x,t0,g=1.0):
    i=int(t0*SR); x=x[:max(0,len(buf)-i)]; buf[i:i+len(x)]+=x*g
def env(n,a=.005,d=.15):
    t=np.arange(n)/SR; return np.minimum(t/a,1)*np.exp(-t/d)
def tone(f,dur,kind="mar",vel=1):
    n=int(dur*SR); t=np.arange(n)/SR
    if kind=="mar": y=np.sin(2*np.pi*f*t)+.35*np.sin(2*np.pi*f*4*t)*np.exp(-t*18)+.15*np.sin(2*np.pi*f*2*t); y*=env(n,.003,.16)
    elif kind=="bass": y=np.sin(2*np.pi*f*t)+.4*np.sin(2*np.pi*f*2*t); y*=env(n,.004,.22)
    elif kind=="pluck": y=(2*((f*t)%1)-1)*.5+np.sin(2*np.pi*f*t)*.5; y*=env(n,.002,.09)
    return (y*vel).astype(np.float32)
def noise(dur,seed=1): return np.random.RandomState(seed).randn(int(dur*SR)).astype(np.float32)
def midi(m): return 440*2**((m-69)/12)
BPM=118; b=60/BPM
# progresion Am - F - C - G (cada 2 compases) estilo detective divertido
prog=[(45,[57,60,64]),(41,[57,60,65]),(48,[55,60,64]),(43,[55,59,62])]
mel=[69,72,76,72,69,67,64,67, 65,69,72,69,65,64,60,64, 67,72,76,72,67,64,67,72, 71,67,62,67,71,74,71,67]
t=0; bar=0
while t<T+.5:
    root,ch=prog[(bar//2)%4]
    for k in range(4):
        tt=t+k*b
        add(mus,tone(midi(root),b*.9,"bass"),tt,.5) if k%2==0 else add(mus,tone(midi(root+12),b*.5,"bass"),tt+b*.5,.32)
        for j,m in enumerate(ch): add(mus,tone(midi(m),b*.35,"pluck"),tt+b*.5,.07)
        hh=noise(.04,int(tt*10)%50)*env(int(.04*SR),.0005,.01); add(mus,hh,tt,.08); add(mus,hh,tt+b*.5,.05)
    # melodia (marimba) en octavas desde s1
    if t>=S[0]+3:
        for k in range(8):
            m=mel[((bar%4)*8+k)%len(mel)]; add(mus,tone(midi(m-12+12*(0)),b*.5,"mar"),t+k*b/2,.16)
    # bombo
    for k in range(4):
        n=int(.18*SR); tt_=np.arange(n)/SR; kick=np.sin(2*np.pi*(55+90*np.exp(-tt_*28))*tt_)*np.exp(-tt_*12); add(mus,kick.astype(np.float32),t+k*b,.55)
    t+=4*b; bar+=1
# SFX
def whoosh(t0,dur=.35,g=.35):
    n=int(dur*SR); x=noise(dur,3); tt=np.arange(n)/SR
    # filtro simple barrido: media movil variable aproximada con mezcla de ruido pasa-bajo
    y=np.cumsum(x)*0.02; y-=np.convolve(y,np.ones(800)/800,'same'); y*=np.sin(np.pi*tt/dur)**2; y/=np.abs(y).max()+1e-6; add(sfx,y.astype(np.float32),t0,g)
def ding(t0,f=1568,g=.35): n=int(.7*SR); tt=np.arange(n)/SR; y=(np.sin(2*np.pi*f*tt)+.4*np.sin(2*np.pi*f*2.01*tt))*np.exp(-tt*6); add(sfx,y.astype(np.float32),t0,g)
def pop(t0,g=.6): n=int(.12*SR); tt=np.arange(n)/SR; y=np.sin(2*np.pi*(300+700*np.exp(-tt*40))*tt)*np.exp(-tt*35); add(sfx,y.astype(np.float32),t0,g)
def boing(t0,g=.45): n=int(.5*SR); tt=np.arange(n)/SR; y=np.sin(2*np.pi*(180+140*np.sin(2*np.pi*9*tt)*np.exp(-tt*5)+300*np.exp(-tt*6))*tt)*np.exp(-tt*5); add(sfx,y.astype(np.float32),t0,g)
def sting(t0,g=.4):
    for i,m in enumerate([57,57,57,52]): add(sfx,tone(midi(m),.28 if i<3 else .9,"bass"),t0+i*.2,g)
def trombone(t0,g=.4):
    for i,(f,d) in enumerate([(233,.45),(220,.45),(208,.45),(196,1.2)]):
        n=int(d*SR); tt=np.arange(n)/SR; fr=f*(1-.03*(i==3)*tt) ; y=(2*((fr*tt)%1)-1)*.4+np.sin(2*np.pi*fr*tt)*.5; y*=np.minimum(tt/.03,1)*np.minimum((d-tt)/.1,1)*(1+.1*np.sin(2*np.pi*5.5*tt)) ; add(sfx,y.astype(np.float32),t0+sum([.5,.5,.5][:i]),g)
def tada(t0,g=.4):
    for m in[60,64,67,72,76]: add(sfx,tone(midi(m),1.2,"mar"),t0+.0,g*.25)
def hiss(t0,dur=1.2,g=.12):
    x=noise(dur,5); x=x-np.convolve(x,np.ones(6)/6,'same'); x*=np.sin(np.pi*np.arange(len(x))/len(x)); add(sfx,x,t0,g)
for i in range(1,8): whoosh(S[i]-.25)
ding(1.0); pop(2.0); ding(S[1]+.4,1318,.25); boing(S[3]-.3); sting(S[3]+2.3); hiss(S[4]+.2,3.6)
ding(S[5]+.3,1568,.4); sting(S[5]+1.6,.35); trombone(S[6]+3.5); tada(S[7]+.2); pop(S[7]+.2)
mus/=max(1e-6,np.abs(mus).max()); mus*=.5
mix=mus+sfx*1.0; mix=np.tanh(mix*1.2)
pcm=(mix[:int((T+.3)*SR)]*30000).astype(np.int16)
with wave.open("music.wav","wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("ok",len(pcm)/SR)
