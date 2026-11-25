#!/bin/bash
# Renderiza, sintetiza sonido y mezcla un short. Uso: build.sh v7 /ruta/salida.mp4 /ruta/portada.png
set -e
cd "$(dirname "$0")"
V=$1; OUT=$2; COV=$3
node frames.js video $V ${V}_raw.mp4
node frames.js cover $V "$COV"
python3 -I audio2.py $V
ffmpeg -y -loglevel error -i ${V}_vtrack.wav -af "highpass=f=80,equalizer=f=180:t=q:w=1:g=2,equalizer=f=3200:t=q:w=1.2:g=3,acompressor=threshold=-20dB:ratio=3:attack=5:release=80,aecho=0.8:0.7:45|75:0.10|0.06,loudnorm=I=-19:TP=-3:LRA=9" -ar 48000 -ac 2 ${V}_vproc.wav
ffmpeg -y -loglevel error -i ${V}_sfx.wav -af "loudnorm=I=-16:TP=-2:LRA=14" -ar 48000 ${V}_sfxn.wav
ffmpeg -y -loglevel error -i ${V}_raw.mp4 -i ${V}_sfxn.wav -i ${V}_vproc.wav -filter_complex "[1:a][2:a]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-13:TP=-2:LRA=11,alimiter=limit=0.6:level=false:attack=1:release=60,aresample=48000[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT"
echo "$V $(ffmpeg -hide_banner -i "$OUT" -af ebur128=peak=true -f null - 2>&1 | grep -E '^\s+(I|Peak):' | tail -2 | tr -s ' ' | tr '\n' ' ') $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT")"
