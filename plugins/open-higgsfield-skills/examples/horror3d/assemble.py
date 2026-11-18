import subprocess
F="/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
subs=[(8.4,10.4,"Aquí estoy, mi amor."),(12.0,14.0,"Ya no tengas miedo."),(15.2,17.4,"Yo nunca me fui.")]
dt=[]
for a,b,s in subs:
    dt.append(f"drawtext=fontfile={F}:text='{s}':fontcolor=white@0.92:fontsize=26:x=(w-text_w)/2:y=h-58:shadowcolor=black:shadowx=2:shadowy=2:enable='between(t,{a},{b})'")
dt.append(f"drawtext=fontfile={F}:text='Mamá murió hace un año.':fontcolor=white:fontsize=34:x=(w-text_w)/2:y=(h-text_h)/2:alpha='min(1,max(0,(t-20.3)/0.6))':enable='gte(t,20.2)'")
vf="tpad=stop_mode=add:stop_duration=2:color=black,eq=contrast=1.06:saturation=0.9,vignette=PI/5,noise=alls=6:allf=t,"+",".join(dt)+",format=yuv420p"
cmd=["ffmpeg","-y","-loglevel","error","-framerate","24","-i","hr/f%04d.png","-i","horror.wav","-vf",vf,"-c:v","libx264","-crf","17","-preset","slow","-c:a","aac","-b:a","192k","-shortest","el_espejo.mp4"]
subprocess.run(cmd,check=True)
