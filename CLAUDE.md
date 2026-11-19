# Preferencias de video del usuario

## Voz en off (por defecto, siempre)
- Idioma: español. Voz: **hombre, español de España**, modelo Piper `es_ES-davefx-medium` (grave, ~120 Hz).
- Descarga del modelo (HuggingFace está bloqueado en los entornos en la nube; este espejo sí funciona):
  `https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-es_ES-davefx-medium.tar.bz2`
- Usar `pip install piper-tts` y el script `plugins/open-higgsfield-skills/examples/pacman/tts2.py` (parámetros: noise_scale 0.75, noise_w_scale 0.9).
- Mezcla: ver `plugins/open-higgsfield-skills/examples/pacman/mix.py` (voz procesada con EQ y compresión, música bajada con sidechain, loudnorm -15 LUFS).
- No usar la voz femenina `es_MX-claude-high` ni la masculina mexicana `es_MX-ald-medium` salvo que el usuario lo pida.

## Formato
- Videos para YouTube Shorts: vertical 1080x1920, menos de 60 s, subtítulos grandes.
- El usuario sube los videos él mismo (esta sesión no tiene acceso a su cuenta de YouTube).
