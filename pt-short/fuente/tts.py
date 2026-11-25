# uso: tts.py lines.json outdir  -> genera un wav por línea con Kokoro (voz em_alex, español de España)
import json,sys,os,numpy as np,soundfile as sf
from kokoro_onnx import Kokoro
K=os.path.join(os.path.dirname(os.path.abspath(__file__)),'kokoro')
k=Kokoro(os.path.join(K,'kokoro-q8.onnx'),os.path.join(K,'voices_es.npz'))
lines=json.load(open(sys.argv[1]));out=sys.argv[2];os.makedirs(out,exist_ok=True)
voice=os.environ.get('VOICE','em_alex')
for i,l in enumerate(lines):
    a,sr=k.create(l['text'],voice=voice,speed=l.get('speed',1.0),lang='es')
    sf.write(os.path.join(out,f'{i:02d}.wav'),a,sr);print(i,sr,round(len(a)/sr,2),l['text'])
