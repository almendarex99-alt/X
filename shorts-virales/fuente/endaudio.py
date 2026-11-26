import numpy as np,wave
SR=48000;D=4.6;N=int(SR*D);t=np.arange(N)/SR;rng=np.random.default_rng(3);x=np.zeros(N)
def add(s,at,g=1.0):
    i=int(at*SR);s=s[:N-i];x[i:i+len(s)]+=s*g
def env(n,a,d):e=np.ones(n);na=max(1,int(a*SR));e[:na]=np.linspace(0,1,na);return e*np.exp(-np.arange(n)/SR/d)
x+=(np.sin(2*np.pi*55*t)+.6*np.sin(2*np.pi*82.4*t))*.08*np.minimum(1,t/.4)*np.minimum(1,(D-t)/.4)
n=int(SR*.6);w=np.cumsum(rng.normal(0,1,n));w=w-np.convolve(w,np.ones(200)/200,'same');add(w/np.abs(w).max()*np.sin(np.pi*np.arange(n)/n),0,.5)
for i in range(3):
    n=int(SR*.15);s=np.sin(2*np.pi*(500+i*120)*np.arange(n)/SR*(1+np.arange(n)/n))*env(n,.002,.05);add(s,1.0+i*.25,.4)
n=int(SR*.05);add(rng.normal(0,1,n)*np.exp(-np.arange(n)/200),2.5,.6)
n=int(SR*1.2);s=(np.sin(2*np.pi*1318*np.arange(n)/SR)+.5*np.sin(2*np.pi*1975*np.arange(n)/SR))*env(n,.002,.35);add(s,2.6,.3)
x=x/np.abs(x).max()*.7;pcm=(np.stack([x,x],1)*32767).astype(np.int16)
with wave.open('endcard.wav','wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(SR);f.writeframes(pcm.tobytes())
