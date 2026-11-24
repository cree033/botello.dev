"""Personajes de Botello.Dev (v2, estilo producto tech). Grupos SVG centrados en (0, 0).

Sistema visual: superficies con degradado y luz desde arriba a la izquierda, bordes finos,
sombra de piso suave y un solo color de acento por personaje. Las caras viven en pantallas.
"""


def hexmix(a, b, k):
    k = max(0.0, min(1.0, k))
    ca = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    cb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(round(ca[j] + (cb[j] - ca[j]) * k) for j in range(3))


def _blur(fid, sd):
    return f'<filter id="{fid}" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="{sd}"/></filter>'


def _floor(uid, cx=0, cy=214, rx=190, ry=24):
    return (f'<defs><radialGradient id="fl{uid}"><stop offset="0" stop-color="#000" stop-opacity="0.55"/>'
            f'<stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient></defs>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#fl{uid})"/>')


# ----------------------------------------------------------------------------
# PROD · servidor de producción. La cara es el display frontal.
# ----------------------------------------------------------------------------
def prod(look=(0.0, 0.0), eye_scale=1.0, blink=0.0, tilt=9.0, mouth=0.0, light=1.0, sweat=0.0, heat=0.0, uid="p"):
    eye = hexmix("#d7f2ff", "#ffb347", heat)
    dsp = hexmix("#173a55", "#52300f", heat)
    ew, eh = 44 * eye_scale, 62 * eye_scale * (1 - 0.92 * blink)
    lx, ly = look
    s = [f'''
<defs>
 <linearGradient id="bd{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#555d7b"/><stop offset="0.5" stop-color="#3a4058"/><stop offset="1" stop-color="#262b3d"/></linearGradient>
 <radialGradient id="ds{uid}" cx="0.5" cy="0.45" r="0.8"><stop offset="0" stop-color="{dsp}"/><stop offset="1" stop-color="#090b12"/></radialGradient>
 <radialGradient id="gl{uid}"><stop offset="0" stop-color="#ff3b3b" stop-opacity="0.95"/><stop offset="1" stop-color="#ff3b3b" stop-opacity="0"/></radialGradient>
 <linearGradient id="dm{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff8a80"/><stop offset="1" stop-color="#c91f1f"/></linearGradient>
 {_blur("bl" + uid, 7)}
</defs>''', _floor("p" + uid)]
    s.append(f'''
<rect x="-100" y="196" width="52" height="20" rx="6" fill="#1a1e2d"/>
<rect x="48" y="196" width="52" height="20" rx="6" fill="#1a1e2d"/>
<rect x="-126" y="-168" width="282" height="372" rx="24" fill="#191d2b"/>
<rect x="-140" y="-180" width="280" height="370" rx="24" fill="url(#bd{uid})" stroke="#6b7392" stroke-width="2"/>
<path d="M-118 -178 H118" stroke="#ffffff" stroke-opacity="0.22" stroke-width="2"/>
<circle cx="0" cy="-200" r="92" fill="url(#gl{uid})" opacity="{0.9 * light:.3f}"/>
<rect x="-28" y="-194" width="56" height="16" rx="6" fill="#1c2132" stroke="#4a5272" stroke-width="2"/>
<path d="M-22 -194 A22 22 0 0 1 22 -194 Z" fill="url(#dm{uid})" opacity="{0.35 + 0.65 * light:.3f}"/>
<path d="M-13 -203 Q-8 -212 3 -212" stroke="#ffffff" stroke-opacity="0.6" stroke-width="3" stroke-linecap="round" fill="none"/>
<rect x="-112" y="-146" width="224" height="160" rx="18" fill="#0a0c14" stroke="#1f2538" stroke-width="3"/>
<rect x="-106" y="-140" width="212" height="148" rx="14" fill="url(#ds{uid})"/>
<rect x="-106" y="-140" width="212" height="46" rx="14" fill="#ffffff" opacity="0.045"/>''')
    for sx, sign in ((-48, -1), (48, 1)):
        cx, cy = sx + lx, -76 + ly
        hl = max(3.0, min(eh * 0.3, 10.0))
        s.append(f'''
<g transform="translate({cx:.1f} {cy:.1f}) rotate({sign * tilt:.1f})">
 <rect x="{-ew / 2:.1f}" y="{-eh / 2:.1f}" width="{ew:.1f}" height="{eh:.1f}" rx="{min(ew, eh) * 0.36:.1f}" fill="{eye}" filter="url(#bl{uid})" opacity="0.65"/>
 <rect x="{-ew / 2:.1f}" y="{-eh / 2:.1f}" width="{ew:.1f}" height="{eh:.1f}" rx="{min(ew, eh) * 0.36:.1f}" fill="{eye}"/>
 <rect x="{-ew / 2 + 7:.1f}" y="{-eh / 2 + 6:.1f}" width="{ew * 0.32:.1f}" height="{hl:.1f}" rx="4" fill="#ffffff" opacity="0.55"/>
</g>''')
    a = 7 * mouth
    if mouth < 0.03:
        mp = "M-36 -20 L36 -20"
    else:
        mp = f"M-40 -22 L-26 {-22 + a:.1f} L-12 {-22 - a:.1f} L2 {-22 + a:.1f} L16 {-22 - a:.1f} L30 {-22 + a:.1f} L40 -22"
    s.append(f'<path d="{mp}" stroke="{eye}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" fill="none" opacity="0.9"/>')
    s.append(f'''
<path d="M-108 46 H108 M-108 66 H108 M-108 86 H108" stroke="#151927" stroke-width="7" stroke-linecap="round" stroke-dasharray="12 8"/>
<rect x="-112" y="118" width="104" height="48" rx="10" fill="#1f2436" stroke="#343b55" stroke-width="2"/>
<rect x="8" y="118" width="104" height="48" rx="10" fill="#1f2436" stroke="#343b55" stroke-width="2"/>
<path d="M-80 142 H-30 M30 142 H80" stroke="#4a5272" stroke-width="4" stroke-linecap="round"/>
<circle cx="-96" cy="142" r="4.5" fill="#3cff8a"/>
<circle cx="96" cy="142" r="4.5" fill="#ffb13c"/>''')
    if sweat > 0:
        s.append(f'''
<g transform="translate(124 {-140 + sweat * 80:.1f})" opacity="{min(1.0, sweat * 4):.2f}">
 <path d="M0 -15 C9 -2 11 6 0 11 C-11 6 -9 -2 0 -15 Z" fill="#8fd8ff"/>
</g>''')
    return "".join(s)


# ----------------------------------------------------------------------------
# EL LEGACY · stored procedure de 2009: monitor CRT beige, amarillento, con cables colgando.
# ----------------------------------------------------------------------------
def legacy(blink=0.0, uid="l"):
    g = "#5dff9a"
    scan = "".join(f"M-96 {y} H96 " for y in range(-116, 34, 5))
    frac = 0.52 + 0.42 * blink
    ew, eh, cy = 30.0, 38.0, -66.0
    s = [f'''
<defs>
 <linearGradient id="bg{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ddd0ad"/><stop offset="1" stop-color="#b3a37b"/></linearGradient>
 <radialGradient id="ag{uid}" cx="0.5" cy="0.5" r="0.75"><stop offset="0.55" stop-color="#7a5a1c" stop-opacity="0"/><stop offset="1" stop-color="#7a5a1c" stop-opacity="0.38"/></radialGradient>
 <radialGradient id="sc{uid}" cx="0.5" cy="0.45" r="0.7"><stop offset="0" stop-color="#14402a"/><stop offset="1" stop-color="#06100b"/></radialGradient>
 <clipPath id="cs{uid}"><rect x="-96" y="-116" width="192" height="148" rx="20"/></clipPath>
 {_blur("bl" + uid, 5)}
</defs>''', _floor("l" + uid, cy=262, rx=170, ry=22)]
    s.append(f'''
<rect x="-90" y="150" width="180" height="30" rx="8" fill="#a99b74"/>
<rect x="-122" y="178" width="244" height="16" rx="10" fill="#8f8160"/>
<rect x="-140" y="-165" width="280" height="320" rx="30" fill="url(#bg{uid})" stroke="#8c7f5d" stroke-width="3"/>
<rect x="-140" y="-165" width="280" height="320" rx="30" fill="url(#ag{uid})"/>
<path d="M-118 -163 H118" stroke="#ffffff" stroke-opacity="0.45" stroke-width="2"/>
<rect x="-112" y="-132" width="224" height="180" rx="28" fill="#9d8f6b"/>
<rect x="-108" y="-128" width="216" height="172" rx="26" fill="#1b1a14"/>
<rect x="-96" y="-116" width="192" height="148" rx="20" fill="url(#sc{uid})"/>
<g clip-path="url(#cs{uid})">
 <path d="{scan}" stroke="#000000" stroke-opacity="0.24" stroke-width="2"/>
 <rect x="-96" y="-116" width="192" height="50" fill="#ffffff" opacity="0.035"/>''')
    for sx in (-42, 42):
        top = cy - eh / 2
        cut = eh * frac
        s.append(f'''
 <rect x="{sx - ew / 2}" y="{top + cut:.1f}" width="{ew}" height="{eh - cut:.1f}" rx="7" fill="{g}" filter="url(#bl{uid})" opacity="0.7"/>
 <rect x="{sx - ew / 2}" y="{top + cut:.1f}" width="{ew}" height="{eh - cut:.1f}" rx="7" fill="{g}"/>
 <path d="M{sx - 17} {cy + 26} Q{sx} {cy + 34} {sx + 17} {cy + 26}" stroke="{g}" stroke-opacity="0.3" stroke-width="3" fill="none" stroke-linecap="round"/>''')
    s.append(f'''
 <text x="-82" y="22" font-family="DejaVu Sans Mono" font-size="17" fill="{g}" opacity="0.85">&gt;_ sp_2009</text>
</g>
<g transform="rotate(-4 -64 102)">
 <rect x="-118" y="76" width="108" height="52" rx="3" fill="#e8d98a" stroke="#b8a64a" stroke-width="1.5"/>
 <text x="-64" y="100" font-family="DejaVu Sans Mono" font-weight="bold" font-size="17" text-anchor="middle" fill="#3b3217">sp_2009</text>
 <text x="-64" y="118" font-family="DejaVu Sans Mono" font-weight="bold" font-size="13" text-anchor="middle" fill="#8a2f1f">NO TOCAR</text>
</g>
<rect x="20" y="82" width="92" height="10" rx="4" fill="#4a432f"/>
<circle cx="38" cy="118" r="10" fill="#8c7f5d" stroke="#6f6448" stroke-width="2"/>
<circle cx="68" cy="118" r="10" fill="#8c7f5d" stroke="#6f6448" stroke-width="2"/>
<circle cx="100" cy="118" r="4.5" fill="#ffb13c"/>
<path d="M-138 -138 L-108 -163 M-138 -116 L-82 -163 M-138 -92 L-52 -163 M-124 -150 Q-114 -128 -92 -118 M-132 -118 Q-116 -104 -102 -94" stroke="#ffffff" stroke-opacity="0.32" stroke-width="1.6" fill="none"/>''')
    cables = [("#23262f", -72, -2), ("#b8453b", -46, 14), ("#3b78b8", -22, 0), ("#d9a62e", 4, 18), ("#23262f", 28, 4), ("#3d9a6a", 52, 16), ("#b8453b", 74, 0)]
    for color, x, k in cables:
        ey = 238 + k
        s.append(f'<path d="M{x} 152 C{x + 16} 188 {x - 16} 214 {x + 5} {ey}" stroke="{color}" stroke-width="11" stroke-linecap="round" fill="none"/>'
                 f'<rect x="{x - 3}" y="{ey - 2}" width="16" height="20" rx="3" fill="#161821" stroke="#3a3e4d" stroke-width="1.5"/>')
    return "".join(s)


# ----------------------------------------------------------------------------
# VIBE · la IA: burbuja de cristal con degradado violeta-rosa.
# ----------------------------------------------------------------------------
def vibe(blink=0.0, uid="v"):
    ry = 24 * (1 - 0.92 * blink)
    return f'''
<defs>
 <linearGradient id="vb{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8b6bff"/><stop offset="1" stop-color="#ff7ac8"/></linearGradient>
 <linearGradient id="vf{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2f2560"/><stop offset="1" stop-color="#191539"/></linearGradient>
 <linearGradient id="ve{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#cdbfff"/></linearGradient>
 {_blur("bl" + uid, 9)}
</defs>
{_floor("v" + uid, cy=196, rx=150, ry=18)}
<rect x="-150" y="-120" width="300" height="210" rx="74" fill="url(#vb{uid})" filter="url(#bl{uid})" opacity="0.55"/>
<path d="M-90 80 L-126 164 L-24 92 Z" fill="url(#vf{uid})" stroke="url(#vb{uid})" stroke-width="4" stroke-linejoin="round"/>
<rect x="-150" y="-120" width="300" height="210" rx="74" fill="url(#vf{uid})" stroke="url(#vb{uid})" stroke-width="4"/>
<path d="M-112 -86 Q0 -126 112 -86" stroke="#ffffff" stroke-opacity="0.16" stroke-width="6" stroke-linecap="round" fill="none"/>
<ellipse cx="-52" cy="-18" rx="14" ry="{ry:.2f}" fill="url(#ve{uid})"/>
<ellipse cx="52" cy="-18" rx="14" ry="{ry:.2f}" fill="url(#ve{uid})"/>
<path d="M-46 38 Q0 68 46 38" stroke="url(#vb{uid})" stroke-width="8" stroke-linecap="round" fill="none"/>
<g transform="translate(114 -108)"><path d="M0 -20 L5 -5 L20 0 L5 5 L0 20 L-5 5 L-20 0 L-5 -5 Z" fill="#ffffff"/></g>
<g transform="translate(-122 -98) scale(0.55)"><path d="M0 -20 L5 -5 L20 0 L5 5 L0 20 L-5 5 L-20 0 L-5 -5 Z" fill="#ffffff" opacity="0.7"/></g>
'''


# ----------------------------------------------------------------------------
# EL TICKET · tarjeta de tarea con estilo de gestor de proyectos.
# ----------------------------------------------------------------------------
def ticket(pct=0.9, uid="t"):
    w = 160 * pct
    return f'''
<defs><clipPath id="tc{uid}"><rect x="-115" y="-155" width="230" height="310" rx="20"/></clipPath></defs>
{_floor("t" + uid, cy=178, rx=140, ry=16)}
<rect x="-109" y="-145" width="230" height="310" rx="20" fill="#000000" opacity="0.28"/>
<rect x="-115" y="-155" width="230" height="310" rx="20" fill="#f4f1e8" stroke="#d8d2bf" stroke-width="2"/>
<g clip-path="url(#tc{uid})"><rect x="-115" y="-155" width="230" height="14" fill="#f2a93b"/></g>
<rect x="-99" y="-128" width="84" height="30" rx="15" fill="#1f2436"/>
<text x="-57" y="-107" font-family="Inter" font-weight="700" font-size="17" text-anchor="middle" fill="#ffffff">#4521</text>
<path d="M66 -102 L78 -114 L90 -102 M66 -92 L78 -104 L90 -92" stroke="#d8453a" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
<circle cx="-34" cy="-44" r="8" fill="#1f2436"/><circle cx="34" cy="-44" r="8" fill="#1f2436"/>
<circle cx="-31" cy="-47" r="2.6" fill="#ffffff"/><circle cx="37" cy="-47" r="2.6" fill="#ffffff"/>
<path d="M-22 -8 H22" stroke="#1f2436" stroke-width="5" stroke-linecap="round"/>
<rect x="-99" y="26" width="170" height="9" rx="4.5" fill="#d6d0bc"/>
<rect x="-99" y="46" width="120" height="9" rx="4.5" fill="#d6d0bc"/>
<rect x="-99" y="72" width="108" height="26" rx="13" fill="#e1ecff"/>
<text x="-45" y="90" font-family="Inter" font-weight="600" font-size="14" text-anchor="middle" fill="#2457c5">En progreso</text>
<rect x="-99" y="112" width="160" height="14" rx="7" fill="#e4dfcd"/>
<rect x="-99" y="112" width="{w:.1f}" height="14" rx="7" fill="#2f9e6a"/>
<text x="99" y="125" font-family="Inter" font-weight="700" font-size="15" text-anchor="end" fill="#3b3a33">{int(pct * 100)} %</text>
'''


# ----------------------------------------------------------------------------
# EL CLIENTE · silueta sin cara, con luz de borde.
# ----------------------------------------------------------------------------
def cliente(uid="c"):
    return f'''
<defs>
 <linearGradient id="sh{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2a3050"/><stop offset="0.55" stop-color="#0d0f19"/><stop offset="1" stop-color="#05060a"/></linearGradient>
 <linearGradient id="rm{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#a3acdc"/><stop offset="0.5" stop-color="#3d4468"/><stop offset="1" stop-color="#1a1e30"/></linearGradient>
</defs>
{_floor("c" + uid, cy=206, rx=200, ry=18)}
<path d="M-170 196 C-170 84 -90 42 0 42 C90 42 170 84 170 196 Z" fill="url(#sh{uid})" stroke="url(#rm{uid})" stroke-width="3"/>
<circle cx="0" cy="-96" r="74" fill="url(#sh{uid})" stroke="url(#rm{uid})" stroke-width="3"/>
<path d="M-46 46 L0 124 L46 46 Z" fill="#c9cde0" opacity="0.88"/>
<path d="M-46 46 L-4 136 L-82 98 Z M46 46 L4 136 L82 98 Z" fill="#0b0d16" opacity="0.9"/>
<path d="M-11 78 L11 78 L17 152 L0 180 L-17 152 Z" fill="#8f2d3a"/>
<rect x="-12" y="68" width="24" height="16" rx="5" fill="#a63a49"/>
'''


# ----------------------------------------------------------------------------
# EL DEV · solo un cursor parpadeante.
# ----------------------------------------------------------------------------
def cursor_dev(on=1.0, uid="d"):
    return f'''
<defs>{_blur("bl" + uid, 12)}</defs>
<path d="M-126 -38 L-78 0 L-126 38" stroke="#39ff88" stroke-width="13" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
<rect x="-34" y="-56" width="68" height="112" rx="10" fill="#39ff88" filter="url(#bl{uid})" opacity="{0.55 * on:.2f}"/>
<rect x="-34" y="-56" width="68" height="112" rx="10" fill="#39ff88" opacity="{on:.2f}"/>
'''


# nombre, rol, voz, dibujo, slug, color de acento
CAST = [
    ("Prod", "El servidor de producción", "Voz aguda y nerviosa", lambda: prod(uid="s1"), "prod", "#ff6b6b"),
    ("El Legacy", "Stored procedure de 2009", "Voz grave, de abuelo", lambda: legacy(blink=0.0, uid="s2"), "el-legacy", "#5dff9a"),
    ("Vibe", "La IA asistente", "Siempre segura, casi siempre mal", lambda: vibe(uid="s3"), "vibe", "#a78bfa"),
    ("El Ticket", "Tarjeta de tarea", "Su barra nunca termina", lambda: ticket(uid="s4"), "el-ticket", "#f2a93b"),
    ("El cliente", "Silueta con voz", "Pide cosas enormes", lambda: cliente(uid="s5"), "el-cliente", "#8892b8"),
    ("El dev", "El testigo cansado", "Solo un cursor parpadeante", lambda: cursor_dev(uid="s6"), "el-dev-cursor", "#39ff88"),
]
