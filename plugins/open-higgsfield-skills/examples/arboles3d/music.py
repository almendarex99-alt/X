import numpy as np, wave
sr=44100; T=28; n=sr*T; t=np.arange(n)/sr
bpm=96; beat=60/bpm
chords=[[57,60,64],[53,57,60],[48,52,55],[55,59,62]]  # Am F C G
f=lambda m:440*2**((m-69)/12)
out=np.zeros(n)
for i in range(int(T/beat)):
    ch=chords[(i//4)%4]; s=int(i*beat*sr)
    m=ch[i%3]+12*(i%2); d=int(beat*sr*1.5); d=min(d,n-s)
    tt=np.arange(d)/sr; env=np.exp(-tt*5)
    out[s:s+d]+=0.25*env*(np.sin(2*np.pi*f(m)*tt)+0.3*np.sin(4*np.pi*f(m)*tt))
    if i%4==0:
        d2=min(int(beat*4*sr),n-s); tt=np.arange(d2)/sr
        for mm in ch: out[s:s+d2]+=0.07*np.sin(2*np.pi*f(mm-12)*tt)*np.minimum(1,tt*4)*np.minimum(1,(beat*4-tt)*4)
    if i%2==0:
        d3=min(int(0.12*sr),n-s); tt=np.arange(d3)/sr; out[s:s+d3]+=0.35*np.sin(2*np.pi*(90-300*tt)*tt)*np.exp(-tt*25)
out*=np.minimum(1,t/1.0)*np.minimum(1,(T-t)/1.5)
out=out/np.abs(out).max()*0.6
with wave.open("music.wav","wb") as w:
    w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((out*32767).astype(np.int16).tobytes())
