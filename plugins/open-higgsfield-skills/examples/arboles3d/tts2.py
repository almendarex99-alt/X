import sys, json, wave, glob
from piper import PiperVoice, SynthesisConfig
n=sys.argv[1]
v=PiperVoice.load(glob.glob("../voz/vits-piper-es_ES-davefx-medium/*.onnx")[0])
cfg=SynthesisConfig(noise_scale=0.75,noise_w_scale=0.9,length_scale=1.0)
t=0.5;out=[]
for i,x in enumerate(json.load(open(f"script_{n}.json"))):
    with wave.open(f"{n}_vo_{i}.wav","wb") as w: v.synthesize_wav(x["text"],w,syn_config=cfg)
    with wave.open(f"{n}_vo_{i}.wav") as w: d=w.getnframes()/w.getframerate()
    out.append({"text":x["text"],"start":round(t,3),"end":round(t+d,3),"dur":round(d,3)}); t+=d+0.35
json.dump({"segments":out,"total":round(t+0.6,2)},open(f"timeline_{n}.json","w"),ensure_ascii=False,indent=1)
print(n,[round(x["dur"],1) for x in out],"total",round(t+0.6,1))
