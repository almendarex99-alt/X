import json, subprocess, os, textwrap, re, glob, shutil
TL=json.load(open("timeline.json")); SC=TL["scenes"]; T=TL["total"]; FPS=24
F="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
# secuencia continua (rellena frames que falten con el anterior)
shutil.rmtree("seq",ignore_errors=True); os.makedirs("seq")
have=sorted(int(os.path.basename(p)[1:6]) for p in glob.glob("fr/f*.png")); n=int(T*FPS); hs=set(have); last=None
for f in range(n):
    if f in hs: last=f
    os.symlink(os.path.abspath(f"fr/f{last:05d}.png"),f"seq/{f:05d}.png")
os.makedirs("txt",exist_ok=True); L=[]; k=[0]
def add(text,a,b,size,y,col):
    k[0]+=1; p=f"txt/t{k[0]}.txt"; open(p,"w",encoding="utf-8").write(text)
    L.append(f"drawtext=fontfile={F}:textfile={p}:fontcolor={col}:fontsize={size}:x=(w-text_w)/2:y={y}:line_spacing=12:borderw=9:bordercolor=black:enable='gte(t,{a:.2f})*lt(t,{b:.2f})'")
KEY=["¿Quién se comió\nmi sándwich?","Sospechosa nº 1:\nLola","Sospechoso nº 2:\nMax","¡Acusación al\nprofe!","¡¿Yo?!","¡Pista!","Caso cerrado","¿Y tú?"]
for i,s in enumerate(SC):
    end=SC[i+1]["start"] if i+1<len(SC) else T
    add(KEY[i],s["start"]+.05 if i else .2,min(end-.05,s["start"]+3.2),78,"h*0.07","0xFFE23B" if i%2==0 else "white")
    words=s["text"].replace("…","...").split(); chunks=[];cur=""
    for w in words:
        if len(cur)+len(w)+1>30 and cur: chunks.append(cur); cur=w
        else: cur=(cur+" "+w).strip()
        if re.search(r"[.?!:]$",w) and len(cur)>14: chunks.append(cur); cur=""
    if cur: chunks.append(cur)
    SW={"a","un","una","de","del","la","el","los","las","lo","le","se","al","que","y","en","por","con","su","sus","mi","tu","es","era","no","me","yo"}
    for ci in range(len(chunks)-1):
        ws=chunks[ci].split()
        while len(ws)>2 and ws[-1].lower().strip(",.:?!¿¡") in SW: chunks[ci+1]=ws.pop()+" "+chunks[ci+1]
        chunks[ci]=" ".join(ws)
    tot=sum(len(c) for c in chunks); t0=s["start"]
    for c in chunks:
        d=s["dur"]*len(c)/tot; add("\n".join(textwrap.wrap(c,22)),t0,t0+d,72,"h*0.76","white"); t0+=d
vf=",".join(["scale=1080:1920:flags=lanczos","unsharp=5:5:0.6","eq=contrast=1.04:saturation=1.1","vignette=PI/6"]+L+["format=yuv420p"])
fl=[];lab=[]
for i,s in enumerate(SC): fl.append(f"[{i+1}:a]aresample=44100,adelay={int(s['start']*1000)}:all=1[v{i}]"); lab.append(f"[v{i}]")
chain=";".join(fl)+";"+"".join(lab)+f"amix=inputs={len(SC)}:normalize=0,highpass=f=60,equalizer=f=150:t=q:w=1:g=2,equalizer=f=3000:t=q:w=1.2:g=1.5,acompressor=threshold=-20dB:ratio=3:attack=8:release=120,loudnorm=I=-15:TP=-1.5:LRA=7,asplit=2[vo][sc];[{len(SC)+1}:a]aresample=44100[bg];[bg][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=500:makeup=1[duck];[duck]volume=0.8[d2];[d2][vo]amix=inputs=2:normalize=0,alimiter=limit=0.95[aout]"
cmd=["ffmpeg","-y","-loglevel","error","-framerate",str(FPS),"-i","seq/%05d.png"]
for i in range(len(SC)): cmd+=["-i",f"v_{i}.wav"]
cmd+=["-i","music.wav","-filter_complex",chain,"-vf",vf,"-map","0:v","-map","[aout]","-t",str(T),"-r","30","-c:v","libx264","-crf","20","-preset","medium","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-movflags","+faststart","roblox_sandwich_short.mp4"]
subprocess.run(cmd,check=True); print("listo")
