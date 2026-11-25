# Cómo regenerar el short

1. `npm install` (fuentes Anton, VT323 e Inter desde @fontsource) y Playwright con Chromium.
2. `node frames.js video raw.mp4`: renderiza los 1500 fotogramas (1080x1920, 30 fps) y escribe `cues.json`.
3. `python3 audio.py`: sintetiza el sonido a partir de `cues.json` (misma línea de tiempo que la imagen).
4. Mezcla:
   `ffmpeg -i raw.mp4 -i sfx.wav -map 0:v -map 1:a -c:v copy -af "loudnorm=I=-13:TP=-2:LRA=11,alimiter=limit=0.6:level=false:attack=1:release=60,aresample=48000" -c:a aac -b:a 192k -shortest -movflags +faststart pt-lisa-short.mp4`
5. Portada: `node frames.js cover portada.png`.

## Voz (español de España, Kokoro "em_alex")

- Modelo: `kokoro-q8-shards` (npm), une las 6 partes en `kokoro-q8.onnx`.
- Voces: `em_alex.pt`, `ef_dora.pt`, `em_santa.pt` de github.com/remsky/Kokoro-FastAPI (`api/src/voices/v1_0/`).
  `python mkvoices.py voices_raw voices_es.npz` lee los tensores sin ejecutar pickle.
- `pip install kokoro-onnx soundfile`, luego:
  `python tts.py voz.json voz` → `python fit.py voz.json voz` (ajusta velocidad) → `python tts.py voz.json voz` → `python place.py voz.json voz voz_track.wav 50`
- Mezcla (efectos por encima de la voz: efectos a -16 LUFS, voz a -19 LUFS):
  ```
  ffmpeg -i voz_track.wav -af "highpass=f=80,equalizer=f=180:t=q:w=1:g=2,equalizer=f=3200:t=q:w=1.2:g=3,acompressor=threshold=-20dB:ratio=3:attack=5:release=80,aecho=0.8:0.7:45|75:0.10|0.06,loudnorm=I=-19:TP=-3:LRA=9" -ar 48000 -ac 2 voz_proc.wav
  ffmpeg -i sfx.wav -af "loudnorm=I=-16:TP=-2:LRA=14" -ar 48000 sfx_n.wav
  ffmpeg -i raw.mp4 -i sfx_n.wav -i voz_proc.wav -filter_complex "[1:a][2:a]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-13:TP=-2:LRA=11,alimiter=limit=0.6:level=false:attack=1:release=60,aresample=48000[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart pt-lisa-short.mp4
  ```
