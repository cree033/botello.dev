import os, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
from people import PEOPLE, person
from chars import prod

OUT = "/mnt/user-data/outputs/Botello.Dev/05-assets/personajes"
os.makedirs(OUT, exist_ok=True)

def png(svg, png_, w=None, h=None):
    cmd = ["rsvg-convert", svg, "-o", png_]
    if w: cmd += ["-w", str(w)]
    if h: cmd += ["-h", str(h)]
    subprocess.run(cmd, check=True)

# archivos sueltos (fondo transparente)
for name, role, voice, draw, slug, accent in PEOPLE:
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-300 -300 600 600" width="600" height="600">{draw()}</svg>'
    open(f"{OUT}/{slug}.svg", "w", encoding="utf-8").write(s)
    png(f"{OUT}/{slug}.svg", f"{OUT}/{slug}.png", w=1024, h=1024)

# hoja de personas
W, H = 2400, 900
cells = []
for i, (name, role, voice, draw, slug, accent) in enumerate(PEOPLE):
    x0, y0 = 80 + i * 760, 230
    cells.append(f'''
<rect x="{x0}" y="{y0}" width="720" height="560" rx="30" fill="url(#card)" stroke="#262c45" stroke-width="2"/>
<rect x="{x0+40}" y="{y0}" width="640" height="4" rx="2" fill="{accent}" opacity="0.9"/>
<g transform="translate({x0+360} {y0+216}) scale(0.82)">{draw()}</g>
<circle cx="{x0+52}" cy="{y0+486}" r="7" fill="{accent}"/>
<text x="{x0+74}" y="{y0+497}" font-family="Inter" font-weight="700" font-size="44" fill="#ffffff">{name}</text>
<text x="{x0+50}" y="{y0+530}" font-family="Inter" font-weight="500" font-size="23" fill="#9aa3c7">{role}  ·  {voice}</text>''')
sheet = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b0d14"/><stop offset="1" stop-color="#121624"/></linearGradient>
<linearGradient id="card" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#171b2c"/><stop offset="1" stop-color="#10131f"/></linearGradient></defs>
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<text x="80" y="118" font-family="Inter" font-weight="800" font-size="70" fill="#ffffff">Botello.Dev</text>
<text x="80" y="178" font-family="Inter" font-weight="500" font-size="32" fill="#9aa3c7">Hoja de personas  ·  Los humanos que sufren a los objetos</text>
<text x="{W-80}" y="118" font-family="Inter" font-weight="600" font-size="26" text-anchor="end" fill="#6f789c">v2</text>
{''.join(cells)}
<text x="80" y="850" font-family="Inter" font-weight="500" font-size="26" fill="#6f789c">Las personas reaccionan; los objetos mandan  ·  máx. 1 persona + 1 objeto por pieza al inicio  ·  expresiones: neutral, cansado, preocupado, sorpresa, sonrisa, inexpresivo, socarrón</text>
</svg>'''
open(f"{OUT}/hoja-de-personas.svg", "w", encoding="utf-8").write(sheet)
png(f"{OUT}/hoja-de-personas.svg", f"{OUT}/hoja-de-personas.png")

# imagen de interacción: Memo frente a Prod
EV = "/mnt/user-data/outputs/Botello.Dev/05-assets/01-viernes-5-58"
scene = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" width="1600" height="900">
<defs><radialGradient id="g" cx="0.5" cy="0.4" r="0.8"><stop offset="0" stop-color="#2a1317"/><stop offset="1" stop-color="#0b0d14"/></radialGradient></defs>
<rect width="1600" height="900" fill="url(#g)"/>
<g transform="translate(470 440) scale(1.0)">{person("memo","worried",look=(10,0),uid="z1")}</g>
<g transform="translate(1180 460) scale(0.86)">{prod(look=(-12,0), eye_scale=1.22, tilt=17, mouth=1.0, heat=1.0, sweat=0.4, uid="z2")}</g>
<rect x="400" y="780" width="800" height="70" rx="14" fill="#0f1220" stroke="#e5484d" stroke-width="2"/>
<text x="430" y="824" font-family="DejaVu Sans Mono" font-size="26" fill="#e8ecff"><tspan fill="#39ff88">$</tspan> git push origin main <tspan fill="#ffb347">› desplegando a producción…</tspan></text>
<text x="80" y="90" font-family="Inter" font-weight="700" font-size="40" fill="#ffffff">Memo + Prod · prueba de interacción</text>
</svg>'''
open("/tmp/interaccion.svg", "w", encoding="utf-8").write(scene)
png("/tmp/interaccion.svg", "/tmp/interaccion.png")
print("ok")
