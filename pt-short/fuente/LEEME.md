# Cómo regenerar el short

1. `npm install` (fuentes Anton, VT323 e Inter desde @fontsource) y Playwright con Chromium.
2. `node frames.js video raw.mp4`: renderiza los 1500 fotogramas (1080x1920, 30 fps) y escribe `cues.json`.
3. `python3 audio.py`: sintetiza el sonido a partir de `cues.json` (misma línea de tiempo que la imagen).
4. Mezcla:
   `ffmpeg -i raw.mp4 -i sfx.wav -map 0:v -map 1:a -c:v copy -af "loudnorm=I=-13:TP=-2:LRA=11,alimiter=limit=0.6:level=false:attack=1:release=60,aresample=48000" -c:a aac -b:a 192k -shortest -movflags +faststart pt-lisa-short.mp4`
5. Portada: `node frames.js cover portada.png`.
