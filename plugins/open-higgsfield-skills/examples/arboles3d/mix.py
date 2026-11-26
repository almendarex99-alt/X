import json,subprocess
tl=json.load(open("timeline.json"));s=tl["segments"]
fl=[];lab=[]
for i,x in enumerate(s):
    fl.append(f"[{i+1}:a]aresample=44100,adelay={int(x['start']*1000)}:all=1[v{i}]");lab.append(f"[v{i}]")
chain=";".join(fl)+";"+"".join(lab)+f"amix=inputs={len(s)}:normalize=0,highpass=f=60,equalizer=f=150:t=q:w=1:g=2,equalizer=f=3000:t=q:w=1.2:g=1.5,acompressor=threshold=-20dB:ratio=3:attack=8:release=120,asplit=2[vo][sc];[0:a]aresample=44100[bg];[bg][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400:makeup=1[duck];[duck]volume=0.45[d2];[d2][vo]amix=inputs=2:normalize=0,loudnorm=I=-15:TP=-1.5:LRA=7,alimiter=limit=0.95[aout]"
cmd=["ffmpeg","-y","-loglevel","error","-i","music.wav"]
for i in range(len(s)): cmd+=["-i",f"vo_{i}.wav"]
cmd+=["-filter_complex",chain,"-map","[aout]","-t",str(tl["total"]),"mix.m4a","-c:a","aac","-b:a","192k"]
subprocess.run(cmd,check=True)
