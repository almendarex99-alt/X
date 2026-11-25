# Construye la línea de tiempo a partir de la duración real de cada frase
import json,wave,os,sys
d=os.path.dirname(os.path.abspath(__file__));L=json.load(open(os.path.join(d,'lines.json')))
t=4.0;out=[]
for i,l in enumerate(L):
    with wave.open(os.path.join(d,'voz',f'{i:02d}.wav')) as w: dur=w.getnframes()/w.getframerate()
    gap=max(.7,l['gap']*2.4)+(1.6 if l['scene'].startswith('chapter') else 0)
    t+=gap if i else 0
    out.append(dict(i=i,t=round(t,3),dur=round(dur,3),scene=l['scene'],label=l['label'],text=l['text']));t+=dur
for i,o in enumerate(out): o['end']=out[i+1]['t'] if i+1<len(out) else round(t+5,3)
DUR=round(t+5,2)
json.dump({'dur':DUR,'lines':out},open(os.path.join(d,'timeline.json'),'w'),ensure_ascii=False)
open(os.path.join(d,'..','mandela_tl.js'),'w').write('const TL='+json.dumps({'dur':DUR,'lines':out},ensure_ascii=False)+';')
# subtítulos .srt
def ts(x):h=int(x//3600);m=int(x%3600//60);s=x%60;return f'{h:02d}:{m:02d}:{int(s):02d},{int((s%1)*1000):03d}'
with open(os.path.join(d,'mandela.srt'),'w',encoding='utf8') as f:
    for k,o in enumerate(out,1):f.write(f"{k}\n{ts(o['t'])} --> {ts(o['t']+o['dur'])}\n{o['text']}\n\n")
print('DUR',DUR,'s =',round(DUR/60,2),'min')
