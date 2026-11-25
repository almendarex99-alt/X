import json,wave,subprocess,glob,os,re,textwrap
from piper import PiperVoice, SynthesisConfig
VOZ=os.environ["VOZ_DIR"]; onnx=glob.glob(f"{VOZ}/x_vits-piper-es_ES-davefx-medium/*/*.onnx")[0]
v=PiperVoice.load(onnx); cfg=SynthesisConfig(noise_scale=0.75,noise_w_scale=0.9,length_scale=1.1)
S=json.load(open("script.json")); t=0.6; sc=[]
for i,s in enumerate(S):
    with wave.open(f"v_{i}.wav","wb") as w: v.synthesize_wav(s.get("say",s["text"]),w,syn_config=cfg)
    with wave.open(f"v_{i}.wav") as w: d=w.getnframes()/w.getframerate()
    sc.append(dict(start=t,dur=d,text=s["text"])); t+=d+(0.9 if i in(3,5,6) else 0.6)
T=round(t+0.8,2); print("duración",T)
F="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; os.makedirs("txt",exist_ok=True); L=[]; n=0
for s in sc:
    words=s["text"].split(); chunks=[];cur=""
    for w in words:
        if len(cur)+len(w)+1>30 and cur: chunks.append(cur); cur=w
        else: cur=(cur+" "+w).strip()
    if cur: chunks.append(cur)
    tot=sum(len(c) for c in chunks); t0=s["start"]
    for c in chunks:
        d=s["dur"]*len(c)/tot; n+=1; open(f"txt/t{n}.txt","w").write("\n".join(textwrap.wrap(c,20)))
        L.append(f"drawtext=fontfile={F}:textfile=txt/t{n}.txt:fontcolor=white:fontsize=84:x=(w-text_w)/2:y=(h-text_h)/2:line_spacing=14:borderw=8:bordercolor=black:enable='gte(t,{t0:.2f})*lt(t,{t0+d:.2f})'"); t0+=d
fl=[f"[{i}:a]aresample=44100,adelay={int(s['start']*1000)}:all=1[v{i}]" for i,s in enumerate(sc)]
chain=";".join(fl)+";"+"".join(f"[v{i}]" for i in range(len(sc)))+f"amix=inputs={len(sc)}:normalize=0,highpass=f=60,equalizer=f=150:t=q:w=1:g=3,equalizer=f=3000:t=q:w=1.2:g=1.5,acompressor=threshold=-20dB:ratio=3:attack=8:release=120,aecho=0.8:0.55:70|140:0.22|0.12,loudnorm=I=-15:TP=-1.5:LRA=7[aout]"
ins=[]; 
for i in range(len(sc)): ins+=["-i",f"v_{i}.wav"]
def render(out,vf):
    subprocess.run(["ffmpeg","-y","-loglevel","error"]+ins+["-f","lavfi","-i",f"color=c=black:s=1080x1920:r=30:d={T}","-filter_complex",chain+f";[{len(sc)}:v]{vf}[vout]","-map","[vout]","-map","[aout]","-t",str(T),"-c:v","libx264","-crf","23","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-movflags","+faststart",out],check=True)
render("solo_voz_subtitulado.mp4",",".join(L+["format=yuv420p"])); render("solo_voz_negro.mp4","format=yuv420p")
