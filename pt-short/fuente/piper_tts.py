# uso: piper_tts.py lines.json outdir -> un wav por línea con Piper (es_ES-davefx-medium)
import json,sys,os,wave
from piper import PiperVoice
from piper.config import SynthesisConfig
M=os.path.join(os.path.dirname(os.path.abspath(__file__)),'piper','a','es_ES-davefx-medium.onnx')
v=PiperVoice.load(M)
L=json.load(open(sys.argv[1]));out=sys.argv[2];os.makedirs(out,exist_ok=True)
for i,l in enumerate(L):
    sp=l.get('speed',1.0)
    cfg=SynthesisConfig(length_scale=1.0/sp,noise_scale=0.6,noise_w_scale=0.8)
    p=os.path.join(out,f'{i:02d}.wav')
    with wave.open(p,'wb') as w: v.synthesize_wav(l['text'],w,syn_config=cfg)
    with wave.open(p) as w: print(i,w.getframerate(),round(w.getnframes()/w.getframerate(),2),l['text'][:60])
