# uso: python3 prep.py  (en la carpeta del video): voz + timeline + musica
import json,wave,subprocess,sys,os
HERE=os.path.dirname(os.path.abspath(__file__))
subprocess.run([sys.executable,HERE+"/tts2.py","es_ES-davefx-medium","v"],check=True,stdout=subprocess.DEVNULL)
s=json.load(open("script.json")); t=0.35; sc=[]
for i,x in enumerate(s):
    with wave.open(f"v_{i}.wav") as w: d=w.getnframes()/w.getframerate()
    sc.append({"start":round(t if i else 0,2),"vstart":round(t,2),"dur":round(d,2),"text":x["text"]}); t+=d+0.42
total=round(t+0.3,2); json.dump({"scenes":sc,"total":total},open("timeline.json","w"),ensure_ascii=False,indent=1)
print("total",total,[x["start"] for x in sc])
if os.path.exists("audio_custom.py"):
    subprocess.run([sys.executable,"audio_custom.py"],check=True,env=dict(os.environ,PYTHONPATH=HERE))
else:
    subprocess.run([sys.executable,HERE+"/audio_mood.py"],check=True)
