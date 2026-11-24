---
pieza: Reel 2 - 6:03 pm, una línea
archivo: reel-02_v1_voz-ia.mp4
duracion: 21 s (1080x1920, 30 fps, -15.7 LUFS)
estado: listo para revisar y publicar
serie: Ese viernes (ep. 2)
---

# Reel 2: guion de voz y publicación

## Voces (IA, español de México, ElevenLabs v3 vía Magnific)

| Personaje | Voz | Líneas |
| --- | --- | --- |
| Memo | Ignacio Valverde (joven, cálido, juguetón) | "Es solo una línea." / "Es una línea." / "Nada importante." |
| Nacho | Roberto Pérez (adulto, acento de la CDMX, cansado) | "¿Tests?" / "¿Y esa línea... qué hacía?" / "...Aprobado." |
| Ruth | Araceli Mendoza (seca, directa) | "¿Ya salió?" |

Los clips sueltos están en `audio/`. Prod no habla: solo latido y baliza.

## Plano a plano

| Tiempo | Imagen | Texto en pantalla |
| --- | --- | --- |
| 0:00 a 0:03 | Memo con la laptop | "Viernes, 6:03 pm." |
| 0:03 a 0:06 | Nacho sudando, tres gafetes | "¿Tests?" |
| 0:06 a 0:07 | Memo | "Es una línea." |
| 0:07 a 0:10 | Prod tiembla con la baliza roja; tarjeta del cambio | `- WHERE id = @id` |
| 0:10 a 0:12 | Memo | "Nada importante." |
| 0:12 a 0:15 | Nacho resignado, sello verde | "...Aprobado." |
| 0:15 a 0:17 | Ruth con la tableta | "¿Ya salió?" |
| 0:17 a 0:21 | Tarjeta negra | "6:04 pm. Aprobado por 1 persona (que también es QA y PMO). Leído por 0." |

Todo el texto queda en la zona segura de Instagram (nada en los últimos 380 px).

## Caption propuesto

Aprobado por 1 persona (que también es QA y PMO). Leído por 0.
Mándaselo a quien aprueba pull requests sin abrirlos.

Voces e ilustraciones hechas con IA.

#desarrolladores #programacion #devhumor #humortech #softwaredeveloper

## Antes de publicar

- Activar la etiqueta "Contenido generado con IA" de Instagram si aparece al subir el Reel.
- Portada: `portada.png` (cuadro de 9 s). Cambiarla si se prefiere el cuadro de Nacho.
- Publicar después de renombrar la cuenta a botello.dev (pasos en el README raíz).

---

## v2 con boca articulada (24 nov 2026)

- Archivo: `reel-02_v2_habla.mp4` (21 s, 1080x1920, -15.7 LUFS). Misma voz IA, ahora los personajes mueven la boca, gesticulan y parpadean.
- Clips parlantes en `clips-parlantes/` (Magnific `video_speak`, modelo `veed-fabric-1.0-fast`; `omnihuman` salió en negro con estos dibujos). Costo: ~700-1,750 créditos por clip según duración.
- Prod (servidor) sigue con temblor y latido; no habla.
- Generador: `06-generador/reel3.py` (usa reel2.py) → `python3 reel3.py frames`, luego `reel2.py audio` y ffmpeg.
- Cambio de edición: Nacho aparece en pantalla para "¿Y esa línea... qué hacía?" y Prod entra al final del plano (9.5-10.3 s).
- Sigue vigente: avisar IA en la descripción y activar la etiqueta de contenido IA de Instagram. Perfil ya renombrado a botello.dev.
