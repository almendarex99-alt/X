# Prompt maestro para todos mis videos (copiar y pegar)

> Pega este texto al empezar cualquier sesión y, al final, añade solo el tema. Ejemplo: `TEMA: la máscara de Halloween`.

---

Actúa como guionista, director de arte y editor de YouTube Shorts. Haz el vídeo del TEMA que te indico al final, con **la misma calidad y detalle que los vídeos "Backrooms" y "shorts30_v2"**. Usa el motor del repositorio (`plugins/open-higgsfield-skills/examples/shorts_engine_v2/`) y las plantillas de `shorts30_v2/<tema>/vid.py`.

## 1. Formato (obligatorio)
- Vertical 1080×1920, 30 fps, **menos de 58 s**, subtítulos grandes abajo y título clave arriba en cada escena.
- Español. Voz de hombre de España, Piper `es_ES-davefx-medium` (campo `say` con respelado fonético para nombres extranjeros). Música y efectos **originales**, sin derechos de autor. Mezcla: voz con EQ y compresión, música con sidechain, loudnorm −15 LUFS.
- No lo subas a YouTube (no tengo acceso a mi cuenta): entrégame los archivos.

## 2. Guion (retención alta)
- 8 segmentos, 115–150 palabras: **gancho en forma de pregunta** → contexto (año/autor) → 3 de desarrollo → revelación → detalle final → cierre que enlaza con el gancho (bucle) + **pregunta para comentar y "suscríbete"**.
- Frases cortas, un dato nuevo cada 5 s, cambio visual en cada segmento.
- **Fiel a los hechos.** Si un dato es anécdota o no está 100 % confirmado, dilo en el guion ("se cuenta", "según contó"). Entrega una lista **VERIFICAR** por vídeo. Sin gore ni imágenes truculentas.
- Los títulos clave (`keys.json`) deben coincidir **uno a uno** con lo que se narra en cada segmento.

## 3. Calidad visual (lo que más me importa)
**Cada escena debe parecerse a la realidad de lo que se cuenta**, no a un dibujo plano:
- **Espacios reales en 3D** (`liminal.py`, motor de rayos con numpy): perspectiva real, texturas procedurales (papel pintado, moqueta, hormigón, metal), iluminación con caída y parpadeo, niebla, ruido de cámara, desenfoque de lente. Pasillos, salas, túneles, casas: con puertas, zócalos, techo, sombras y profundidad.
- **Personajes con anatomía correcta** (`rig.py`): cuello unido al torso, cabeza con orejas, **pelo detrás y delante de la cabeza (y por detrás del cuello si es largo)**, brazos con hombro-codo-muñeca, **manos con 5 dedos de dos falanges** que agarran de verdad lo que sostienen, piernas con rodilla y pie. Nada flotando, nada desconectado.
- **Animales y criaturas** (`creatures.py`): patas de dos segmentos, cola articulada, mandíbula móvil, ojos, dientes, garras.
- **Mucho movimiento**: todos caminan, respiran, parpadean y gesticulan; la cámara avanza, se acerca o gira en cada escena; hay partículas, humo, luces o sombras que se mueven. Nada estático más de 1 s.
- **Detalle**: objetos del tema bien dibujados (cámaras, carátulas, pantallas, libros, máscaras, monitores) con sombras y brillos, rótulos legibles y paleta coherente con la época del tema. Si hay una pantalla (móvil, monitor, cámara VHS) muéstrala con su interfaz real: texto, fecha, REC, líneas de barrido.
- Si conozco la obra original, respeta **colores, formas y época**. Si no puedes ser fiel sin material de referencia, **pídeme capturas** en lugar de inventar y dime honestamente que son recreaciones tuyas.
- Evita choques de texto: el título superior ocupa y≈67-200 y los subtítulos y≈758-840 (lienzo 540×960); no pongas rótulos ahí.

## 4. Sonido con detalle
- Ambiente propio del tema (zumbido de fluorescentes, viento, cinta VHS, sala con eco…), pasos y foley sincronizados con la acción, golpes en los giros, un remate de cierre. Nunca una música continua genérica.

## 5. Control de calidad antes de entregar
1. Genera una hoja de contactos con un cuadro de cada escena y revísala: manos con dedos, pelo y cuello unidos, nada cortado por el borde, texto legible, sin solapes.
2. Comprueba la duración (<58 s) y que los títulos clave coinciden con los segmentos.
3. Corrige y vuelve a renderizar lo que falle (borra solo los archivos temporales).
4. Haz commit y push a la rama de trabajo; no crees pull requests salvo que te lo pida.

## 6. Entrega
Para **cada** vídeo envíame: el **MP4**, la **portada.jpg**, y la **ficha** con: título (≤ 60 caracteres), descripción con pregunta final, hashtags, etiquetas y la lista **VERIFICAR**. Ve enviándome cada MP4 en cuanto termine su render. Al final, resume en pocas líneas qué limitaciones tiene el resultado (lo que es recreación propia y qué referencias mejorarían la fidelidad).

**TEMA:** <escribe aquí el tema o los temas>

---

### Variantes rápidas
- **Una tanda de 10:** añade `Haz 10 vídeos distintos sobre: videojuegos, juegos de terror, cortos de terror y sucesos o curiosidades de películas.`
- **Rehacer uno:** `Rehaz el vídeo de <tema> con el máximo detalle y realismo, igual que Backrooms.`
- **Más realismo en un vídeo concreto:** `Pasa <tema> al motor 3D (liminal.py) y sustituye las escenas planas por escenas reales con texturas, iluminación y cámara en movimiento.`
