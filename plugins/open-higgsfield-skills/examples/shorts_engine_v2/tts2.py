import sys, json, wave, glob
from piper import PiperVoice
try:
    from piper import SynthesisConfig
except Exception: SynthesisConfig=None
voice=sys.argv[1]; out=sys.argv[2]
import os
VOZ=os.environ.get("VOZ_DIR","/tmp/claude-0/-home-user-X/6c82c91a-a910-5618-95bf-05abf2e310d3/scratchpad/pac/voz")
onnx=glob.glob(f"{VOZ}/x_vits-piper-{voice}/*/*.onnx")[0]
v=PiperVoice.load(onnx)
cfg=SynthesisConfig(noise_scale=0.75,noise_w_scale=0.9,length_scale=1.0) if SynthesisConfig else None
for i,s in enumerate(json.load(open("script.json"))):
    with wave.open(f"{out}_{i}.wav","wb") as w:
        v.synthesize_wav(s.get("say",s["text"]),w,syn_config=cfg) if cfg else v.synthesize_wav(s.get("say",s["text"]),w)
    with wave.open(f"{out}_{i}.wav") as w: d=w.getnframes()/w.getframerate()
    print(i,round(d,2),"s")
