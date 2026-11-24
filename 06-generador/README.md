# Generador de personajes y Reels

Scripts con los que se dibujaron los personajes y se produjo el Reel 1. Sirven de base para los otros 9 guiones: se reutilizan los personajes de `chars.py` y se cambia la línea de tiempo.

| Archivo | Qué hace |
| --- | --- |
| `chars.py` | Dibuja a Prod, El Legacy, Vibe, El Ticket, El cliente y el cursor del dev como SVG. Cada personaje acepta parámetros (mirada, tamaño y inclinación de los ojos, parpadeo, boca, luz, sudor, calor). |
| `people.py` | Dibuja a Memo, Ruth y Caro como SVG con estados de ánimo, mirada y parpadeo. |
| `sheet_people.py` | Exporta un PNG por persona y la hoja de personas. |
| `sheet.py` | Exporta un PNG por personaje (fondo transparente) y la hoja general. |
| `reel1.py` | Línea de tiempo y animación del Reel 1; renderiza 600 fotogramas (1080x1920, 30 fps). |
| `audio1.py` | Sintetiza el sonido del Reel 1 (sin samples ni música de terceros). |

## Requisitos

Python 3 con Pillow y numpy, `rsvg-convert` (librsvg), `ffmpeg` y la fuente Inter (más DejaVu Sans Mono para el texto de terminal).

## Cómo se arma un Reel

1. Renderizar fotogramas: `python3 reel1.py`.
2. Generar el audio: `python3 audio1.py`.
3. Codificar: `ffmpeg -framerate 30 -i frames/f%04d.png -i audio_loud.wav -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart salida.mp4`.

Nota: las rutas de salida de los scripts apuntan al espacio de trabajo donde se crearon (`/mnt/user-data/outputs/...` y `/tmp/reel1/`); ajustarlas si se corren en otro equipo.

Para un Reel nuevo, copiar `reel1.py` como `reelNN.py`, cambiar los textos y los tiempos, y usar los personajes de `chars.py`.
