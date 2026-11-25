# ajusta la velocidad de cada línea para que quepa en su ventana (máx. 1.2x) y vuelve a generar
import json,sys,soundfile as sf,os,subprocess
p,out=sys.argv[1],sys.argv[2];L=json.load(open(p))
for i,l in enumerate(L):
    d=sf.info(os.path.join(out,f'{i:02d}.wav')).duration;win=l['end']-l['t']
    l['speed']=round(min(1.2,max(1.0,l.get('speed',1.0)*d/win)),3) if d>win else l.get('speed',1.0)
    l['dur']=round(d,2)
json.dump(L,open(p,'w'),ensure_ascii=False,indent=0)
for l in L: print(l['t'],l['end'],l['dur'],l['speed'],l['text'][:50])
