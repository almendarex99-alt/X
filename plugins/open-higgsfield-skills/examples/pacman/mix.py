import json,subprocess,wave,sys
pre=sys.argv[1]; out=sys.argv[2]
s=json.load(open("script.json")); fl=[];lab=[]
for i,x in enumerate(s):
    with wave.open(f"{pre}_{i}.wav") as w: d=w.getnframes()/w.getframerate()
    win=x["end"]-x["start"]; r=min(max(1.0,d/win),1.3)
    fl.append(f"[{i+1}:a]aresample=44100,atempo={r:.3f},adelay={int(x['start']*1000)}:all=1[v{i}]"); lab.append(f"[v{i}]"); print(i,round(d,2),"s ->",round(d/r,2),"ventana",round(win,1))
V="/root/.claude/uploads/6c82c91a-a910-5618-95bf-05abf2e310d3/35e2e21e-pacman_explicado_short.mp4"
chain=";".join(fl)+";"+"".join(lab)+f"amix=inputs={len(s)}:normalize=0,highpass=f=60,equalizer=f=150:t=q:w=1:g=2,equalizer=f=3000:t=q:w=1.2:g=1.5,acompressor=threshold=-20dB:ratio=3:attack=8:release=120,loudnorm=I=-15:TP=-1.5:LRA=7,asplit=2[vo][sc];[0:a]aresample=44100[bg];[bg][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400:makeup=1[duck];[duck]volume=0.55[d2];[d2][vo]amix=inputs=2:normalize=0,alimiter=limit=0.95[aout]"
cmd=["ffmpeg","-y","-loglevel","error","-i",V]
for i in range(len(s)): cmd+=["-i",f"{pre}_{i}.wav"]
cmd+=["-filter_complex",chain,"-map","0:v","-map","[aout]","-c:v","copy","-c:a","aac","-b:a","192k","-shortest",out]
subprocess.run(cmd,check=True)
