#!/bin/bash
# Añade el cierre del canal al final de un video. Uso: append.sh entrada.mp4 v|h [bitrate]
set -e; D="$(cd "$(dirname "$0")" && pwd)"; IN=$1; M=$2; BR=${3:-}
read W H < <(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "$IN" | tr ',' ' ')
TMP="${IN%.mp4}.tmp.mp4"; VQ="-crf 20"; [ -n "$BR" ] && VQ="-b:v $BR -maxrate 3600k -bufsize 7000k"
ffmpeg -y -loglevel error -i "$IN" -i "$D/endcard_$M.mp4" -filter_complex "[0:v]fps=30,scale=$W:$H,setsar=1,format=yuv420p[a];[1:v]fps=30,scale=$W:$H,setsar=1,format=yuv420p[b];[0:a]aresample=48000,aformat=channel_layouts=stereo[aa];[1:a]aresample=48000,aformat=channel_layouts=stereo[bb];[a][aa][b][bb]concat=n=2:v=1:a=1[v][au]" -map "[v]" -map "[au]" -c:v libx264 -preset medium $VQ -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart "$TMP"
mv "$TMP" "$IN"; echo "$(basename "$IN") $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN")s $(du -m "$IN" | cut -f1)MB"
