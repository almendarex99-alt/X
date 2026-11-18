#!/bin/bash
# Pone una voz de macOS (por defecto Jorge; prueba Alex, Paulina o Monica) sobre gta-short.mp4
# Uso:  ./poner-voz-mac.sh [voz]      Ejemplo: ./poner-voz-mac.sh Alex
# Requisitos: macOS (comando "say") y ffmpeg (brew install ffmpeg)
set -e
VOZ="${1:-Jorge}"; DIR="$(cd "$(dirname "$0")" && pwd)"; TMP="$(mktemp -d)"
SAY="${SAY_CMD:-say}"
# Segundo en que empieza cada escena y lo que dice
STARTS=(0 5.6 12.3 20.2 28.7 35.8 43.0)
LINES=(
"Hola. ¿Sabías que la saga GTA casi cumple treinta años? ¡Y todavía no se jubila!"
"En mil novecientos noventa y siete, todo se veía desde arriba. ¡Como cuando buscas tus llaves desde el techo!"
"En dos mil uno llegó el tres de, y las ciudades por fin tuvieron altura. ¡Y los jugadores, un montón de formas de perderse!"
"Vice City trajo los años ochenta, con luces de neón y camisas floridas. San Andreas trajo un estado entero. ¡Qué exagerados!"
"GTA cinco vendió más de doscientos millones de copias. ¡Casi tantas como calcetines perdidos en el mundo!"
"Y ahora viene GTA seis, con fecha anunciada para el diecinueve de noviembre de dos mil veintiséis. ¡Eso es mañana!"
"Suscríbete, y cuéntame cuál es tu favorito. ¡Hasta la próxima!")
IN=(); FILT=""
for i in "${!LINES[@]}"; do
  "$SAY" -v "$VOZ" -r 185 -o "$TMP/$i.aiff" "${LINES[$i]}"
  ms=$(python3 -c "print(int(${STARTS[$i]}*1000))")
  IN+=(-i "$TMP/$i.aiff"); FILT+="[$((i+1)):a]adelay=${ms}|${ms}[a$i];"
done
MIX=""; for i in "${!LINES[@]}"; do MIX+="[a$i]"; done
FILT+="${MIX}amix=inputs=${#LINES[@]}:normalize=0[v]"
ffmpeg -y -loglevel error -i "$DIR/gta-short.mp4" "${IN[@]}" -filter_complex "$FILT" \
  -map 0:v -map "[v]" -c:v copy -c:a aac -b:a 192k -t 48 "$DIR/gta-short-$VOZ.mp4"
echo "Listo: $DIR/gta-short-$VOZ.mp4"
