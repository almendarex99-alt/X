# Reimplementación de la lógica de yt-viral (swipe.py no venía con la skill): múltiplo sobre la mediana del propio canal
import json,glob,statistics,sys
rows=[]
for f in sorted(glob.glob('c_*.json')):
    try:d=json.load(open(f))
    except Exception:continue
    if not isinstance(d,dict):continue
    tab=f.rsplit('_',1)[1][:-5];E=[e for e in d.get('entries',[]) if e.get('view_count')]
    if len(E)<4:print('omitido (menos de 4 videos):',f,file=sys.stderr);continue
    med=statistics.median(e['view_count'] for e in E)
    for e in E:rows.append(dict(ch=d.get('channel'),subs=d.get('channel_follower_count'),tab=tab,title=e.get('title'),views=e['view_count'],med=med,mult=e['view_count']/med,url=e.get('url'),dur=e.get('duration')))
json.dump(rows,open('rows.json','w'),ensure_ascii=False)
rows.sort(key=lambda r:-r['mult'])
for r in rows:
    if r['mult']>=2:print(f"{r['mult']:5.1f}x | {r['tab']:6} | {r['views']:>10,} (med {int(r['med']):,}) | {r['ch'][:16]:16} | {r['title'][:95]}")
