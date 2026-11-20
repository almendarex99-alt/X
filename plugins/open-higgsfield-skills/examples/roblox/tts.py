import json,wave,glob
from piper import PiperVoice, SynthesisConfig
v=PiperVoice.load(glob.glob("voz/*/*/*.onnx")[0])
cfg=SynthesisConfig(noise_scale=0.75,noise_w_scale=0.9,length_scale=1.0)
S=json.load(open("script.json")); t=0.3; sc=[]
for i,s in enumerate(S):
    with wave.open(f"v_{i}.wav","wb") as w: v.synthesize_wav(s["text"],w,syn_config=cfg)
    with wave.open(f"v_{i}.wav") as w: d=w.getnframes()/w.getframerate()
    sc.append({"start":round(t,2),"dur":round(d,2),"text":s["text"]}); print(i,round(t,2),round(d,2)); t+=d+0.28
json.dump({"scenes":sc,"total":round(t+0.5,2)},open("timeline.json","w"),ensure_ascii=False,indent=1); print("total",t+.5)
