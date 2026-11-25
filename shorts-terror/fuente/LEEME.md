# Motor de shorts de terror (VHS)

- `index.html?v=v7` carga `lib.js` (texto, grano, VHS, pasillo 3D) + el guion visual `v7.js` + `render.js`.
- Cada `vN.js` define `DUR`, la escena por segundo (`scene`), la portada (`COVER`, `COVER_T`) y las señales de sonido (`cue`).
- Voz: `vN_voz.json` con Piper es_ES-davefx-medium → `piper_tts.py`, `fit.py`, `place.py` (ver `pt-short/fuente/LEEME.md`), salida `vN_vtrack.wav`.
- `build.sh vN salida.mp4 portada.png`: renderiza 30 fps, sintetiza el sonido (`audio2.py`) y mezcla con los efectos a -16 LUFS y la voz a -19 LUFS.
- Necesita `node_modules` con @fontsource/anton, vt323, inter y Playwright.
