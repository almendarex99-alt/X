# Línea de tiempo de un short a partir de la voz real. Uso: tl_build.py w1
import json,wave,os,sys
v=sys.argv[1];d=os.path.join(os.path.dirname(os.path.abspath(__file__)),'w',v)
L=json.load(open(os.path.join(d,'lines.json')));t=0.25;out=[]
for i,l in enumerate(L):
    with wave.open(os.path.join(d,'voz',f'{i:02d}.wav')) as w: dur=w.getnframes()/w.getframerate()
    if i: t+=0.45+(0.75 if l['fx']=='stinger' else 0)
    out.append(dict(i=i,t=round(t,3),dur=round(dur,3),**{k:l[k] for k in ('scene','text','cap1','cap2','fx')}));t+=dur
for i,o in enumerate(out): o['end']=out[i+1]['t'] if i+1<len(out) else round(t+2.6,3)
DUR=round(t+2.6,2);T={'dur':DUR,'lines':out}
open(os.path.join(d,'..','..',f'{v}_tl.js'),'w').write('const TL='+json.dumps(T,ensure_ascii=False)+';')
json.dump([{'t':o['t'],'end':o['end'],'text':o['text']} for o in out],open(os.path.join(d,'place.json'),'w'),ensure_ascii=False)
def ts(x):return f'{int(x//3600):02d}:{int(x%3600//60):02d}:{int(x%60):02d},{int((x%1)*1000):03d}'
with open(os.path.join(d,f'{v}.srt'),'w',encoding='utf8') as f:
    for k,o in enumerate(out,1):f.write(f"{k}\n{ts(o['t'])} --> {ts(o['t']+o['dur'])}\n{o['text']}\n\n")
print(v,'DUR',DUR)
