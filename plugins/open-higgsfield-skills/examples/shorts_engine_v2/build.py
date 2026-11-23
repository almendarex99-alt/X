# uso: python3 build.py <slug>   (voz + audio + render + montaje + portada + ficha)
import sys,os,json,subprocess,shutil
HERE=os.path.dirname(os.path.abspath(__file__)); slug=sys.argv[1]; D=os.path.join(HERE,slug); os.chdir(D)
env=dict(os.environ,PYTHONPATH=HERE)
M=json.load(open("meta.json"))
subprocess.run([sys.executable,HERE+"/prep.py"],check=True,env=env)
shutil.rmtree("fr",ignore_errors=True); os.makedirs("fr")
subprocess.run([sys.executable,"vid.py"],check=True,env=env)
subprocess.run([sys.executable,HERE+"/assemble_gen.py",slug+"_short.mp4"],check=True,env=env)
TL=json.load(open("timeline.json")); sc=TL["scenes"]
fi=int((sc[M["cover_scene"]]["start"]+M["cover_off"])*30)
F="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
l1,l2=M["thumb"]
subprocess.run(["ffmpeg","-y","-loglevel","error","-i",f"fr/f{fi:05d}.png","-vf",f"scale=1080:1920,eq=saturation=1.15:contrast=1.06,drawbox=x=0:y=0:w=1080:h=560:color=black@0.6:t=fill,drawtext=fontfile={F}:text='{l1}':fontcolor=white:fontsize={M.get('fs',150)}:x=(w-text_w)/2:y=80:borderw=12:bordercolor=black,drawtext=fontfile={F}:text='{l2}':fontcolor=0xFFD23B:fontsize={M.get('fs',150)}:x=(w-text_w)/2:y=290:borderw=12:bordercolor=black","-frames:v","1","-q:v","2","portada.jpg"],check=True)
shutil.rmtree("fr",ignore_errors=True)
open("youtube_short.txt","w").write(f"TÍTULO ({len(M['title'])} caracteres): {M['title']}\nPORTADA: {l1} {l2}\n\nDESCRIPCIÓN:\n{M['desc']}\n\n{M['tags_hash']}\n\nETIQUETAS: {M['tags']}\n\nVERIFICAR antes de publicar: {M['verify']}\n")
dst=os.path.join("/home/user/X/plugins/open-higgsfield-skills/examples/shorts30_v2",slug); os.makedirs(dst,exist_ok=True)
for f in (slug+"_short.mp4","portada.jpg","youtube_short.txt","vid.py","script.json","keys.json","meta.json","audio_custom.py"):
    if os.path.exists(f): shutil.copy(f,dst)
print("OK",slug)
