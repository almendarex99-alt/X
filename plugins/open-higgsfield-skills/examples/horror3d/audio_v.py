import numpy as np, wave
SR=44100; D=22.5; n=int(SR*D); t=np.arange(n)/SR; rng=np.random.default_rng(1)
def env(a,b,att=.02,rel=.3):
    e=np.zeros(n); m=(t>=a)&(t<b); e[m]=1
    e=np.minimum(1,np.minimum((t-a)/att,(b-t)/rel)).clip(0,1)*m; return e
x=.18*np.sin(2*np.pi*43*t)+.14*np.sin(2*np.pi*46.5*t)+.06*np.sin(2*np.pi*86*t)*(1+np.sin(2*np.pi*.15*t))
x+=.03*rng.standard_normal(n)*(0.5+0.5*np.sin(2*np.pi*.1*t))*0.6
# heartbeat grows
hb=np.zeros(n)
for bt in np.arange(0.5,20,.9-.0):
    for off,amp in((0,1),(.27,.7)):
        s=bt+off; m=(t>=s)&(t<s+.25); hb[m]+=amp*np.exp(-18*(t[m]-s))*np.sin(2*np.pi*52*(t[m]-s))
x+=hb*(.15+.35*np.clip(t/20,0,1))
# flicker zaps
for a,b in[(1.2,1.35),(2.5,2.68),(3.6,3.74),(4.3,4.48),(4.9,5.12),(18.0,18.28),(19.2,19.75)]:
    z=env(a,b,.002,.05); x+=z*(.35*rng.standard_normal(n)*np.sin(2*np.pi*60*t)+.2*np.sin(2*np.pi*120*t))
# stingers
def boom(s,amp=.9,dur=1.8):
    m=(t>=s)&(t<s+dur); u=t[m]-s
    x[m]+=amp*np.exp(-2.2*u)*(np.sin(2*np.pi*(70-25*u)*u)+.4*rng.standard_normal(len(u))*np.exp(-9*u))
boom(5.0); boom(6.0,.5,1.2); boom(18.0,.8,2.0); boom(19.75,.9,2.2)
# footsteps (small) in hallway
for s in np.arange(0.4,4.4,.45):
    m=(t>=s)&(t<s+.12); x[m]+=.18*np.exp(-40*(t[m]-s))*np.sin(2*np.pi*95*(t[m]-s))
# running steps
for s in np.arange(5.4,7.2,.2):
    m=(t>=s)&(t<s+.08); x[m]+=.22*np.exp(-45*(t[m]-s))*np.sin(2*np.pi*110*(t[m]-s))
# rocking creak
cr=env(7.8,19,.5,.5)*(.025*np.sin(2*np.pi*(310+25*np.sin(2*np.pi*.7*t))*t))*(0.5+0.5*np.sin(2*np.pi*.7*t))
x+=cr
# silence before reveal, duck during end card
x*=np.where((t>=19.75)&(t<20.0),1,1)
x*=np.clip((D-t)/1.0,0,1)*np.clip(t/.5,0,1)
x=np.tanh(x*1.4)*.8
y=(x*32767).astype(np.int16); 
with wave.open("horror_v.wav","wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(y.tobytes())
