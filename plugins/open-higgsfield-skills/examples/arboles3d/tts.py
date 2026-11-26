import json, wave, glob
from piper import PiperVoice, SynthesisConfig
onnx=glob.glob("../voz/vits-piper-es_ES-davefx-medium/*.onnx")[0]
v=PiperVoice.load(onnx)
cfg=SynthesisConfig(noise_scale=0.75,noise_w_scale=0.9,length_scale=1.0)
s=json.load(open("script.json")); t=0.5; out=[]
for i,x in enumerate(s):
    with wave.open(f"vo_{i}.wav","wb") as w: v.synthesize_wav(x["text"],w,syn_config=cfg)
    with wave.open(f"vo_{i}.wav") as w: d=w.getnframes()/w.getframerate()
    out.append({"text":x["text"],"start":round(t,3),"end":round(t+d,3),"dur":round(d,3)})
    t+=d+0.35
json.dump({"segments":out,"total":round(t+0.6,2)},open("timeline.json","w"),ensure_ascii=False,indent=1)
print(json.dumps(out,ensure_ascii=False)); print("total",t+0.6)
