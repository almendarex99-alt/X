# coloca cada línea de voz en su tiempo (sin solaparse) y escribe una pista mono 48 kHz
import json,sys,numpy as np,soundfile as sf,subprocess,os
p,d,out,dur=sys.argv[1],sys.argv[2],sys.argv[3],float(sys.argv[4]);L=json.load(open(p));SR=48000
track=np.zeros(int(dur*SR));prev=0
for i,l in enumerate(L):
    w=os.path.join(d,f'{i:02d}.wav');r=w[:-4]+'_48.wav'
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',w,'-ar','48000','-ac','1',r],check=True)
    a,_=sf.read(r);st=max(l['t'],prev+.06);i0=int(st*SR);a=a[:len(track)-i0];track[i0:i0+len(a)]+=a;prev=st+len(a)/SR
    print(f"{i:2d} {st:6.2f}-{prev:6.2f}  ventana {l['t']}-{l['end']}  {'TARDE' if prev>l['end']+.25 else ''}")
sf.write(out,track,SR)
