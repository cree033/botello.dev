# Botello.Dev

Cuenta de Instagram de humor agrio para desarrolladores, contado por los objetos que viven dentro de un sistema: el servidor, el código heredado y la IA. El desarrollador es solo el testigo cansado.

- **Estado (2026-11-24):** pre-lanzamiento. Hoja de personajes v2 y nuevo elenco humano en Magnific (Memo, Nacho, Ruth) más servidores Prod y Staging rediseñados, Reel 1 v2 producido sin voz, Reel 2 producido con voz de IA mexicana y la serie "Ese viernes" planeada; faltan renombrar la cuenta a botello.dev y publicar.
- **Cuenta:** botello.dev (se renombra desde sil.ver.03 para conservar los 106 seguidores; renombrar es decisión confirmada del usuario y se hace desde la app de Instagram: Perfil > Editar perfil > Nombre de usuario).
- **Documento fuente:** https://claude.ai/artifact/Mh2hJhS6RpaR1sWseKd44y
- **Ritmo:** producir 2 Reels por semana en un bloque de unas 3 horas; publicar entre 1 y 3.

## Estructura de la carpeta

| Carpeta | Qué contiene |
| --- | --- |
| `00-perfil/` | Perfil y posicionamiento, diferenciación, voz y reglas, elenco |
| `01-produccion/` | Flujo de producción, calendario de las primeras 4 semanas, checklist de lanzamiento |
| `02-guiones/` | Un archivo por guion (`NN-slug.md`) |
| `03-medicion/` | Qué métricas mirar en Windsor.ai y cómo decidir |
| `04-publicaciones/` | Bitácora de todo lo que se publica (`bitacora.md`) |
| `05-assets/` | Hoja de personajes (PNG y SVG), exportes de Reels, portadas y subtítulos |
| `06-generador/` | Scripts que dibujan los personajes y producen los Reels |

## Cómo se usa esta carpeta

1. Cada pieza nueva empieza como archivo en `02-guiones/` con el estado `idea` y avanza a `guion`, `producido` y `publicado`.
2. Al publicar, se agrega una fila a `04-publicaciones/bitacora.md` con la fecha, el enlace y las métricas.
3. Los archivos finales (video exportado, imágenes, audio) van en `05-assets/`, en una subcarpeta con el número del guion.
4. Cada 2 o 3 semanas se revisan las métricas en Windsor.ai y se anotan en la bitácora antes de que salgan de la ventana de 30 días de la prueba.

## Regla de oro

Antes de publicar cada pieza: ¿la dice un objeto? ¿Podría haberla dicho cualquier serie de oficina? Si lo segundo es sí, se reescribe. Esta cuenta no usa personajes, guiones ni frases de Los Developers.
