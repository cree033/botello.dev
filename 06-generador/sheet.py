import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import CAST

OUT = "/mnt/user-data/outputs/Botello.Dev/05-assets/personajes"
os.makedirs(OUT, exist_ok=True)

# escala y desplazamiento vertical por personaje dentro de su tarjeta
FIT = {
    "prod": (0.8, 18),
    "el-legacy": (0.84, -40),
    "vibe": (1.05, -15),
    "el-ticket": (1.0, -8),
    "el-cliente": (0.95, -15),
    "el-dev-cursor": (1.5, 0),
}


def svg_to_png(svg_path, png_path, width=None, height=None):
    cmd = ["rsvg-convert", svg_path, "-o", png_path]
    if width:
        cmd += ["-w", str(width)]
    if height:
        cmd += ["-h", str(height)]
    subprocess.run(cmd, check=True)


# 1) Un archivo por personaje, fondo transparente (para CapCut u otro editor)
for name, role, voice, draw, slug, accent in CAST:
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-300 -300 600 600" width="600" height="600">{draw()}</svg>'
    sp = f"{OUT}/{slug}.svg"
    open(sp, "w", encoding="utf-8").write(svg)
    svg_to_png(sp, f"{OUT}/{slug}.png", width=1024, height=1024)

# 2) Hoja general
W, H = 2400, 1500
cells = []
col_x = [80, 840, 1600]
row_y = [240, 840]
for i, (name, role, voice, draw, slug, accent) in enumerate(CAST):
    x0, y0 = col_x[i % 3], row_y[i // 3]
    cx, cy = x0 + 360, y0 + 238
    k, dy = FIT[slug]
    cells.append(f'''
<rect x="{x0}" y="{y0}" width="720" height="560" rx="30" fill="url(#card)" stroke="#262c45" stroke-width="2"/>
<rect x="{x0 + 40}" y="{y0}" width="640" height="4" rx="2" fill="{accent}" opacity="0.9"/>
<g transform="translate({cx} {cy + dy}) scale({k})">{draw()}</g>
<circle cx="{x0 + 52}" cy="{y0 + 486}" r="7" fill="{accent}"/>
<text x="{x0 + 74}" y="{y0 + 497}" font-family="Inter" font-weight="700" font-size="44" fill="#ffffff">{name}</text>
<text x="{x0 + 50}" y="{y0 + 530}" font-family="Inter" font-weight="500" font-size="23" fill="#9aa3c7">{role}  ·  {voice}</text>
''')

sheet = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>
 <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b0d14"/><stop offset="1" stop-color="#121624"/></linearGradient>
 <linearGradient id="card" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#171b2c"/><stop offset="1" stop-color="#10131f"/></linearGradient>
</defs>
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<text x="80" y="118" font-family="Inter" font-weight="800" font-size="70" fill="#ffffff">Botello.Dev</text>
<text x="80" y="178" font-family="Inter" font-weight="500" font-size="32" fill="#9aa3c7">Hoja de personajes  ·  Humor agrio para devs, contado por objetos</text>
<text x="{W - 80}" y="118" font-family="Inter" font-weight="600" font-size="26" text-anchor="end" fill="#6f789c">v2</text>
{''.join(cells)}
<text x="80" y="1452" font-family="Inter" font-weight="500" font-size="26" fill="#6f789c">Máx. 2 personajes por pieza  ·  fondo oscuro liso  ·  movimiento mínimo  ·  un color de acento por personaje</text>
</svg>'''
open(f"{OUT}/hoja-de-personajes.svg", "w", encoding="utf-8").write(sheet)
svg_to_png(f"{OUT}/hoja-de-personajes.svg", f"{OUT}/hoja-de-personajes.png")
print("ok", len(os.listdir(OUT)), "archivos")
