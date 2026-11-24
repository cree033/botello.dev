"""Reel 1 · Viernes 5:58 pm (Prod). 1080x1920, 30 fps, 20 s."""
import math
import os
import random
import subprocess
import sys
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(__file__))
from chars import prod

W, H, FPS, DUR = 1080, 1920, 30, 20.0
N = int(FPS * DUR)
FRAMES = "/tmp/reel1/frames"

CMD = 'git commit -m "es un cambio chiquito"'
T_TYPE0, T_TYPE1 = 4.0, 7.0      # el dev escribe
T_ENTER = 7.5                    # empieza el pánico
T_CALM = 13.0                    # Prod mira a cámara
T_CUT = 17.0                     # corte a negro


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def rnd(i, salt):
    return random.Random(i * 7919 + salt).uniform(-1, 1)


def fade(t, a, b):
    """0 antes de a, 1 después de b."""
    return ease((t - a) / max(1e-6, b - a))


# ---- fase de la luz roja (parpadeo que se acelera) ----
_DT = 1 / 960
_PH = []
_p = 0.0
for _k in range(int(DUR / _DT) + 1):
    _t = _k * _DT
    if _t < T_ENTER:
        r = 1.0
    elif _t < 9.0:
        r = 1.0 + 3.5 * ease((_t - T_ENTER) / 1.5)
    elif _t < T_CALM:
        r = 4.5
    else:
        r = 0.0
    _p += r * _DT
    _PH.append(_p)


def phase(t):
    return _PH[min(len(_PH) - 1, int(t / _DT))]


def light(t):
    if t >= T_CUT:
        return 0.0
    if t >= T_CALM:
        return 1.0
    return 1.0 if (phase(t) % 1.0) < 0.5 else 0.22


def beep_times():
    out, last = [], 0
    for k, p in enumerate(_PH):
        t = k * _DT
        if t >= T_CALM:
            break
        if int(p) > last:
            last = int(p)
            out.append(t)
    return out


def panic(t):
    """0 → 1 al empezar el pánico, vuelve a 0 al calmarse."""
    up = fade(t, T_ENTER, T_ENTER + 1.5)
    down = 1 - fade(t, T_CALM, T_CALM + 0.4)
    return up * down


def blink(t):
    for t0 in (2.2, 5.9, 10.6, 14.8):
        if t0 <= t <= t0 + 0.18:
            x = (t - t0) / 0.18
            return 0.95 * (1 - abs(2 * x - 1))
    return 0.0


def wrap(text, n):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > n and cur:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    return lines


def subtitle(tag, lines, alpha, italic=False):
    if alpha <= 0.01:
        return ""
    n = len(lines)
    h = 66 + n * 72
    style = "italic" if italic else "normal"
    out = [f'<g opacity="{alpha:.3f}">',
           f'<rect x="70" y="1135" width="940" height="{h}" rx="28" fill="#000" opacity="0.62"/>',
           f'<text x="110" y="1181" font-family="Inter" font-weight="800" font-size="30" letter-spacing="4" fill="#ff6b6b">{tag}</text>']
    for k, ln in enumerate(lines):
        out.append(f'<text x="110" y="{1250 + k * 72}" font-family="Inter" font-weight="700" font-style="{style}" font-size="58" fill="#ffffff">{ln}</text>')
    out.append("</g>")
    return "".join(out)


def frame_svg(i):
    t = i / FPS
    pc = panic(t)

    # --- Prod ---
    amp = 12 * pc
    dx, dy, rot = amp * rnd(i, 1), amp * 0.5 * rnd(i, 2), amp * 0.12 * rnd(i, 3)
    bob = 4 * math.sin(t * 2.0) * (1 - pc)
    if t < 3.5:
        px, py = 0.0, 8.0
    elif t < T_CALM:
        px, py = 0.0, 16.0
    else:
        px, py = 0.0, 0.0
    px += 2.5 * pc * rnd(i, 4)
    py += 2.5 * pc * rnd(i, 5)
    eye_scale = 1.0 + 0.22 * pc + (0.1 if t >= T_CALM else 0.0) * (1 - pc)
    tilt = 8.0 + 9.0 * pc
    if t >= T_CALM:
        tilt = 3.0
    mouth = pc
    heat = pc
    sweat = 0.0
    if 9.0 <= t < T_CALM + 0.4:
        sweat = ((t - 9.0) / 1.4) % 1.0 or 0.01
    lv = light(t)
    prod_svg = prod(look=(px, py * 0.5), eye_scale=eye_scale, blink=blink(t), tilt=tilt, mouth=mouth, light=lv,
                    sweat=sweat, heat=heat, uid="p")

    # --- fondo con brillo rojo ---
    glow = 0.05 + 0.17 * pc * (0.6 + 0.4 * lv)
    if t >= T_CALM:
        glow = 0.07
    scene_a = 1 - fade(t, T_CUT, T_CUT + 0.3)

    # --- título ---
    title_a = fade(t, 0.0, 0.35)
    title = (f'<g opacity="{title_a:.3f}"><text x="540" y="318" font-family="Inter" font-weight="800" font-size="92" '
             f'text-anchor="middle" fill="#ffffff">Viernes, 5:58 pm.</text></g>')

    # --- subtítulos ---
    subs = ""
    a1 = fade(t, 0.8, 1.05) * (1 - fade(t, 3.2, 3.45))
    subs += subtitle("PROD", ["Dime que no vas a desplegar."], a1, italic=True)
    a2 = fade(t, 13.4, 13.65) * (1 - fade(t, 16.6, 16.9))
    subs += subtitle("PROD", ["Todos los desastres empiezan", "con “chiquito”."], a2)

    # --- terminal del dev ---
    term = ""
    ta = fade(t, 3.6, 3.9)
    if ta > 0:
        nchar = int(len(CMD) * clamp((t - T_TYPE0) / (T_TYPE1 - T_TYPE0)))
        typed = CMD[:nchar]
        cur_on = 1.0 if int(t * 2) % 2 == 0 or t < T_TYPE1 else 0.0
        border = "#2b3045" if t < T_ENTER else "#ff3b3b"
        cx = 132 + 21.7 * len(typed) + 4
        term = (f'<g opacity="{ta:.3f}">'
                f'<rect x="60" y="1372" width="960" height="140" rx="22" fill="#0e111a" stroke="{border}" stroke-width="3"/>'
                f'<text x="96" y="1436" font-family="DejaVu Sans Mono" font-size="36" fill="#39ff88">$ </text>'
                f'<text x="132" y="1436" font-family="DejaVu Sans Mono" font-size="36" fill="#e6e9f5" xml:space="preserve">{typed}</text>'
                f'<rect x="{cx:.1f}" y="1406" width="20" height="40" fill="#39ff88" opacity="{cur_on:.2f}"/>')
        if t >= T_ENTER:
            term += ('<text x="96" y="1490" font-family="DejaVu Sans Mono" font-size="32" fill="#ffb13c">› desplegando a producción…</text>')
        term += "</g>"

    # --- remate ---
    end_a = fade(t, 17.45, 17.85)
    end = (f'<g opacity="{end_a:.3f}">'
           f'<text x="540" y="880" font-family="Inter" font-weight="800" font-size="88" text-anchor="middle" fill="#ffffff">Lunes, 9:00 am:</text>'
           f'<text x="540" y="990" font-family="Inter" font-weight="800" font-size="88" text-anchor="middle" fill="#ff6b6b">ya estaba así.</text>'
           f'</g>')
    handle_a = fade(t, 18.3, 18.7)
    handle = f'<text x="540" y="1480" font-family="Inter" font-weight="600" font-size="36" text-anchor="middle" fill="#6f789c" opacity="{handle_a:.3f}">botello.dev</text>'

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs><radialGradient id="bgg" cx="540" cy="520" r="950" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#ff3b3b" stop-opacity="0.9"/><stop offset="1" stop-color="#ff3b3b" stop-opacity="0"/></radialGradient></defs>
<rect width="{W}" height="{H}" fill="#0b0d14"/>
<rect width="{W}" height="{H}" fill="url(#bgg)" opacity="{glow * scene_a:.3f}"/>
<g opacity="{scene_a:.3f}">
{title}
<g transform="translate(540 {750 + bob:.2f}) scale(1.35)"><g transform="translate({dx:.2f} {dy:.2f}) rotate({rot:.2f})">{prod_svg}</g></g>
{subs}
{term}
</g>
{end}
{handle}
</svg>'''


def render(i):
    path = f"{FRAMES}/f{i:04d}.png"
    subprocess.run(["rsvg-convert", "-w", str(W), "-h", str(H), "-o", path], input=frame_svg(i).encode("utf-8"), check=True)
    return i


if __name__ == "__main__":
    os.makedirs(FRAMES, exist_ok=True)
    only = [int(a) for a in sys.argv[1:]]
    if only:
        for i in only:
            render(i)
        print("frames", only)
    else:
        with Pool(2) as pool:
            for k, _ in enumerate(pool.imap_unordered(render, range(N), chunksize=10)):
                if k % 100 == 0:
                    print("rendered", k, flush=True)
        print("done", N)
