import json, subprocess, os, textwrap, re
TL=json.load(open("timeline.json")); SC=TL["scenes"]; T=TL["total"]
F="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
os.makedirs("txt",exist_ok=True); L=[]; n=[0]
def add(text,a,b,size,y,col,extra=""):
    n[0]+=1; p=f"txt/t{n[0]}.txt"; open(p,"w",encoding="utf-8").write(text)
    L.append(f"drawtext=fontfile={F}:textfile={p}:fontcolor={col}:fontsize={size}:x=(w-text_w)/2:y={y}:line_spacing=12:borderw=8:bordercolor=black:enable='gte(t,{a:.2f})*lt(t,{b:.2f})'{extra}")
KEY=["¿Mario no se\nllamaba Mario?","1981 · Donkey Kong","Gorra y bigote:\nla razón real","El giro: el casero","¡Lo llamaron Mario!","1983: de carpintero\na fontanero","Nombre de leyenda","Comenta tu favorito"]
for i,s in enumerate(SC):
    end=SC[i+1]["start"] if i+1<len(SC) else T
    add(KEY[i],s["start"]+.1 if i else .15,end-.05,84 if i!=0 else 88,"h*0.07","0xFFE23B" if i%2==0 else "white")
    # subtitulos: trozos por frases
    words=s["text"].replace("…","...").split(); chunks=[];cur=""
    for w in words:
        if len(cur)+len(w)+1>38 and cur: chunks.append(cur); cur=w
        else: cur=(cur+" "+w).strip()
        if re.search(r"[.?!:]$",w) and len(cur)>18: chunks.append(cur); cur=""
    if cur: chunks.append(cur)
    SW={"a","un","una","de","del","la","el","los","las","lo","le","se","al","que","y","en","por","con","su","sus","mi","tu","es","era","no"}
    for ci in range(len(chunks)-1):
        ws=chunks[ci].split()
        while len(ws)>2 and ws[-1].lower().strip(",.:?!¿¡") in SW:
            chunks[ci+1]=ws.pop()+" "+chunks[ci+1]
        chunks[ci]=" ".join(ws)
    tot=sum(len(c) for c in chunks); t0=s["vstart"]
    for c in chunks:
        d=s["dur"]*len(c)/tot; c2="\n".join(textwrap.wrap(c,24)); add(c2,t0,t0+d,66,"h*0.79","white"); t0+=d
vf=",".join(["eq=contrast=1.05:saturation=1.08","vignette=PI/6"]+L+["format=yuv420p"])
# audio
fl=[]; lab=[]
for i,s in enumerate(SC):
    fl.append(f"[{i+1}:a]aresample=44100,adelay={int(s['vstart']*1000)}:all=1[v{i}]"); lab.append(f"[v{i}]")
chain=";".join(fl)+";"+"".join(lab)+f"amix=inputs={len(SC)}:normalize=0,highpass=f=60,equalizer=f=150:t=q:w=1:g=2,equalizer=f=3000:t=q:w=1.2:g=1.5,acompressor=threshold=-20dB:ratio=3:attack=8:release=120,loudnorm=I=-15:TP=-1.5:LRA=7,asplit=2[vo][sc];[{len(SC)+1}:a]aresample=44100[bg];[bg][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=500:makeup=1[duck];[duck]volume=0.9[d2];[d2][vo]amix=inputs=2:normalize=0,alimiter=limit=0.95[aout]"
cmd=["ffmpeg","-y","-loglevel","error","-framerate","30","-i","fr/f%05d.png"]
for i in range(len(SC)): cmd+=["-i",f"v_{i}.wav"]
cmd+=["-i","music.wav","-filter_complex",chain,"-vf",vf,"-map","0:v","-map","[aout]","-t",str(T),"-c:v","libx264","-crf","23","-preset","medium","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-movflags","+faststart","mario_nombre_short.mp4"]
subprocess.run(cmd,check=True)
