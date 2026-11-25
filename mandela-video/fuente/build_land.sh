#!/bin/bash
# Video largo horizontal de Mandela. Uso: build_land.sh salida.mp4 miniatura.png
set -e; cd "$(dirname "$0")"; S=..
OUT=$1; COV=$2
node frames_land.js video mandela mandela_raw.mp4
node frames_land.js cover mandela "$COV"
python3 -I audio2.py mandela
DUR=$(python3 -c "import json;print(json.load(open('mandela/timeline.json'))['dur'])")
$S/kokoro/venv/bin/python -I $S/place.py mandela/place.json mandela/voz mandela_vtrack.wav $DUR | grep TARDE || true
ffmpeg -y -loglevel error -i mandela_vtrack.wav -af "highpass=f=80,equalizer=f=180:t=q:w=1:g=2,equalizer=f=3200:t=q:w=1.2:g=3,acompressor=threshold=-20dB:ratio=3:attack=5:release=80,aecho=0.8:0.7:45|75:0.10|0.06,loudnorm=I=-19:TP=-3:LRA=9" -ar 48000 -ac 2 mandela_vproc.wav
ffmpeg -y -loglevel error -i mandela_sfx.wav -af "loudnorm=I=-16:TP=-2:LRA=14" -ar 48000 mandela_sfxn.wav
ffmpeg -y -loglevel error -i mandela_raw.mp4 -i mandela_sfxn.wav -i mandela_vproc.wav -filter_complex "[1:a][2:a]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-14:TP=-2:LRA=11,alimiter=limit=0.5:level=false:attack=1:release=60,aresample=48000[a]" -map 0:v -map "[a]" -c:v libx264 -preset medium -b:v 2600k -maxrate 3600k -bufsize 7000k -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT"
echo "$(ffmpeg -hide_banner -i "$OUT" -af ebur128=peak=true -f null - 2>&1 | grep -E '^\s+(I|Peak):' | tail -2 | tr -s ' ' | tr '\n' ' ') $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT")"
