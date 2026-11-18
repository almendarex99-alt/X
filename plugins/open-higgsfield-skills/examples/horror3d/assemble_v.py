import subprocess, sys
F="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
src=sys.argv[1] if len(sys.argv)>1 else "hvr"
def txt(s,a,b,size,y,col="white",box=False,extra=""):
    bx=":box=1:boxcolor=black@0.55:boxborderw=18" if box else ""
    return (f"drawtext=fontfile={F}:text='{s}':fontcolor={col}:fontsize={size}:x=(w-text_w)/2:y={y}"
            f":borderw=6:bordercolor=black{bx}:enable='between(t,{a},{b})'{extra}")
L=[]
# hook
L.append(txt("NUNCA mires",0,2.6,92,"h*0.12",box=False))
L.append(txt("el espejo de mamá...",0,2.6,72,"h*0.12+110",col="0xFF3B3B"))
# shorts captions
for a,b,s in[(8.4,10.4,"Aquí estoy,"),(8.4,10.4,"mi amor.")]: pass
L.append(txt("Aquí estoy,",8.4,10.4,78,"h*0.70"))
L.append(txt("mi amor.",8.4,10.4,78,"h*0.70+95"))
L.append(txt("Ya no tengas",12.0,14.0,78,"h*0.70"))
L.append(txt("miedo.",12.0,14.0,78,"h*0.70+95"))
L.append(txt("Yo nunca",15.2,17.4,84,"h*0.70",col="0xFF3B3B"))
L.append(txt("me fui.",15.2,17.4,84,"h*0.70+100",col="0xFF3B3B"))
L.append(txt("Mamá murió",20.2,22.5,90,"h*0.42",extra=":alpha='min(1,max(0,(t-20.3)/0.5))'"))
L.append(txt("hace un año.",20.2,22.5,90,"h*0.42+110",extra=":alpha='min(1,max(0,(t-20.3)/0.5))'"))
L.append(txt("¿Lo viste en el espejo?",21.0,22.5,56,"h*0.62",col="0xFF3B3B",extra=":alpha='min(1,max(0,(t-21.0)/0.4))'"))
vf=("scale=1080:1920:flags=lanczos,tpad=stop_mode=add:stop_duration=2.5:color=black,"
    "eq=contrast=1.08:saturation=0.92,vignette=PI/5,noise=alls=5:allf=t,"+",".join(L)+",format=yuv420p")
cmd=["ffmpeg","-y","-loglevel","error","-framerate","24","-i",f"{src}/f%04d.png","-i","horror_v.wav","-vf",vf,
     "-c:v","libx264","-crf","21","-preset","slow","-maxrate","8M","-bufsize","16M","-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart","el_espejo_shorts.mp4"]
subprocess.run(cmd,check=True)
