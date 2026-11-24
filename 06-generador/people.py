"""Personas de Botello.Dev (estilo producto tech, mismas reglas que chars.py).

Busto centrado en (0, 0); cabeza en (0, -70). Cada persona acepta un estado de ánimo,
mirada y parpadeo para poder animarla igual que a los objetos.
"""
from chars import _blur, _floor, hexmix

SKIN = {"memo": "#c98d62", "ruth": "#8d5a3b", "caro": "#f0c3a0"}

# (ceja_izq_dy, ceja_der_dy, inclinación, apertura_ojo, boca)
MOODS = {
    "neutral": (0, 0, 0, 1.0, "flat"),
    "tired":   (4, 4, -3, 0.55, "flat"),
    "worried": (-6, -6, 9, 1.05, "wave"),
    "shock":   (-12, -12, 0, 1.35, "o"),
    "smile":   (-2, -2, 0, 0.9, "smile"),
    "deadpan": (2, 2, 0, 0.7, "flat"),
    "smug":    (-8, 2, 6, 0.85, "smirk"),
}


def _mouth(kind, col="#3a1d14"):
    if kind == "flat":
        return f'<path d="M-15 46 H15" stroke="{col}" stroke-width="5" stroke-linecap="round"/>'
    if kind == "wave":
        return f'<path d="M-18 48 Q-9 40 0 48 T18 48" stroke="{col}" stroke-width="5" stroke-linecap="round" fill="none"/>'
    if kind == "o":
        return f'<ellipse cx="0" cy="48" rx="9" ry="12" fill="#3a1218"/>'
    if kind == "smile":
        return f'<path d="M-18 42 Q0 60 18 42" stroke="{col}" stroke-width="5" stroke-linecap="round" fill="none"/>'
    if kind == "smirk":
        return f'<path d="M-14 48 Q4 52 18 40" stroke="{col}" stroke-width="5" stroke-linecap="round" fill="none"/>'
    return ""


def _face(who, mood, look, blink, uid, brow_col, glasses=False):
    bl, br, tilt, op, mouth = MOODS[mood]
    op = op * (1 - 0.92 * blink)
    lx, ly = look
    s = []
    for sx, bdy, sign in ((-30, bl, -1), (30, br, 1)):
        s.append(f'<ellipse cx="{sx}" cy="-4" rx="15" ry="{max(1.6, 13 * op):.1f}" fill="#fbf7f2"/>')
        pr = 6.4
        s.append(f'<circle cx="{sx + lx:.1f}" cy="{-4 + ly:.1f}" r="{pr}" fill="#1c1410" clip-path="url(#ec{uid}{sx})"/>')
        s.append(f'<defs><clipPath id="ec{uid}{sx}"><ellipse cx="{sx}" cy="-4" rx="15" ry="{max(1.6, 13 * op):.1f}"/></clipPath></defs>')
        s.append(f'<circle cx="{sx + lx + 2:.1f}" cy="{-6 + ly:.1f}" r="2" fill="#ffffff" clip-path="url(#ec{uid}{sx})"/>')
        by = -28 + bdy
        s.append(f'<path d="M{sx - 16} {by + sign * tilt * -0.5:.1f} L{sx + 16} {by + sign * tilt * 0.5:.1f}" stroke="{brow_col}" stroke-width="6" stroke-linecap="round"/>')
    s.append('<path d="M-3 12 Q0 20 6 18" stroke="#000" stroke-opacity="0.18" stroke-width="3" stroke-linecap="round" fill="none"/>')
    s.append(_mouth(mouth))
    if glasses:
        s.append('<g stroke="#1b1e2b" stroke-width="4.5" fill="#ffffff" fill-opacity="0.07">'
                 '<rect x="-52" y="-24" width="43" height="38" rx="14"/><rect x="9" y="-24" width="43" height="38" rx="14"/>'
                 '<path d="M-9 -8 H9" fill="none"/></g>')
    return "".join(s)


def _head(who, uid):
    sk = SKIN[who]
    dark = hexmix(sk, "#000000", 0.18)
    light = hexmix(sk, "#ffffff", 0.14)
    return (f'<defs><linearGradient id="sk{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{light}"/><stop offset="1" stop-color="{dark}"/></linearGradient></defs>'
            f'<rect x="-27" y="40" width="54" height="76" rx="18" fill="{dark}"/>'
            f'<ellipse cx="-78" cy="0" rx="14" ry="22" fill="{dark}"/><ellipse cx="78" cy="0" rx="14" ry="22" fill="{dark}"/>'
            f'<ellipse cx="0" cy="0" rx="78" ry="90" fill="url(#sk{uid})"/>')


def _body(fill_a, fill_b, uid):
    return (f'<defs><linearGradient id="bd{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{fill_a}"/><stop offset="1" stop-color="{fill_b}"/></linearGradient></defs>'
            f'<path d="M-205 262 C-205 138 -128 104 -46 94 L46 94 C128 104 205 138 205 262 Z" fill="url(#bd{uid})"/>'
            f'<path d="M-170 130 C-120 108 -70 100 -46 96" stroke="#ffffff" stroke-opacity="0.12" stroke-width="3" fill="none"/>')


def person(who, mood="neutral", look=(0.0, 0.0), blink=0.0, uid="m"):
    """who: 'memo' | 'ruth' | 'caro'"""
    parts = [f'<g transform="translate(0 10)">', _floor("h" + uid, cy=268, rx=200, ry=18)]
    if who == "memo":
        parts.append(_body("#2f7f88", "#1d4f58", uid))
        parts.append('<path d="M-70 98 C-60 150 60 150 70 98 L46 94 C30 120 -30 120 -46 94 Z" fill="#1b4a52"/>')
        parts.append('<path d="M-16 128 V196 M16 128 V196" stroke="#e8eef0" stroke-width="4" stroke-linecap="round"/>'
                     '<circle cx="-16" cy="200" r="5" fill="#e8eef0"/><circle cx="16" cy="200" r="5" fill="#e8eef0"/>')
        parts.append('<path d="M-60 128 Q0 190 60 128" stroke="#161a26" stroke-width="13" stroke-linecap="round" fill="none"/>'
                     '<rect x="-84" y="108" width="30" height="46" rx="13" fill="#161a26"/><rect x="54" y="108" width="30" height="46" rx="13" fill="#161a26"/>'
                     '<rect x="-79" y="116" width="8" height="30" rx="4" fill="#4cc9f0" opacity="0.9"/><rect x="71" y="116" width="8" height="30" rx="4" fill="#4cc9f0" opacity="0.9"/>')
        parts.append('<g transform="translate(0 -70)">')
        parts.append(_head("memo", uid))
        parts.append('<path d="M-84 -18 C-96 -112 -40 -146 12 -142 C74 -138 98 -92 84 -18 C74 -54 46 -70 4 -66 C-38 -62 -68 -48 -84 -18 Z" fill="#17120f"/>'
                     '<path d="M-52 -104 C-30 -126 10 -130 40 -118" stroke="#ffffff" stroke-opacity="0.16" stroke-width="5" stroke-linecap="round" fill="none"/>'
                     '<path d="M-44 52 Q0 72 44 52 Q36 70 0 72 Q-36 70 -44 52" fill="#17120f" opacity="0.28"/>')
        parts.append(_face("memo", mood, look, blink, uid, "#17120f"))
        parts.append('</g>')
    elif who == "ruth":
        parts.append(_body("#3d4466", "#252a42", uid))
        parts.append('<path d="M-46 94 L0 190 L46 94 Z" fill="#f3efe9"/>'
                     '<path d="M-46 94 L-6 206 L-96 170 Z M46 94 L6 206 L96 170 Z" fill="#2c3250"/>'
                     '<path d="M-46 94 L-6 206 M46 94 L6 206" stroke="#ffffff" stroke-opacity="0.18" stroke-width="3"/>')
        parts.append('<circle cx="62" cy="168" r="6" fill="#ff8fab"/>')
        parts.append('<g transform="translate(0 -70)">')
        parts.append('<circle cx="0" cy="-122" r="34" fill="#21140f"/><circle cx="0" cy="-122" r="34" fill="url(#hl%s)"/>' % uid)
        parts.append(f'<defs><radialGradient id="hl{uid}" cx="0.3" cy="0.3" r="0.8"><stop offset="0" stop-color="#ffffff" stop-opacity="0.18"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient></defs>')
        parts.append(_head("ruth", uid))
        parts.append('<path d="M-82 -10 C-96 -108 -44 -132 4 -130 C58 -130 98 -100 82 -10 C70 -58 36 -80 0 -78 C-38 -76 -68 -54 -82 -10 Z" fill="#21140f"/>'
                     '<path d="M-48 -100 C-24 -118 14 -120 44 -108" stroke="#ffffff" stroke-opacity="0.16" stroke-width="5" stroke-linecap="round" fill="none"/>')
        parts.append(_face("ruth", mood, look, blink, uid, "#21140f", glasses=True))
        parts.append('<circle cx="-80" cy="24" r="4.5" fill="#ff8fab"/>')
        parts.append('</g>')
    else:  # caro
        parts.append(_body("#3c8a63", "#25583e", uid))
        parts.append('<rect x="-38" y="92" width="76" height="40" rx="18" fill="#2f7351"/>')
        parts.append('<path d="M-30 128 L-14 214 M30 128 L14 214" stroke="#9be15d" stroke-width="7" stroke-linecap="round"/>'
                     '<rect x="-30" y="212" width="60" height="42" rx="7" fill="#f4f1e8" stroke="#cfc9b6" stroke-width="2"/>'
                     '<text x="0" y="242" font-family="Inter" font-weight="800" font-size="24" text-anchor="middle" fill="#25583e">QA</text>')
        parts.append('<g transform="translate(0 -70)">')
        parts.append('<path d="M-96 76 C-110 -60 -80 -128 0 -130 C80 -128 110 -60 96 76 C60 90 -60 90 -96 76 Z" fill="#8f3c22"/>')
        parts.append(_head("caro", uid))
        parts.append('<path d="M-84 -14 C-96 -100 -46 -134 6 -132 C60 -130 98 -96 86 -14 C70 -50 40 -58 8 -54 C-30 -50 -64 -40 -84 -14 Z" fill="#b04a2c"/>'
                     '<path d="M-70 -50 C-40 -74 10 -84 60 -64" stroke="#ffffff" stroke-opacity="0.18" stroke-width="5" stroke-linecap="round" fill="none"/>')
        parts.append(_face("caro", mood, look, blink, uid, "#7a2f19"))
        parts.append('</g>')
    parts.append("</g>")
    return "".join(parts)


# nombre, rol, voz, dibujo, slug, color de acento
PEOPLE = [
    ("Memo", "El dev que despliega los viernes", "Tranquilo; dice \"es rapidito\"", lambda: person("memo", "smile", uid="q1"), "memo", "#4cc9f0"),
    ("Ruth", "La tech lead", "Seca y cansada; solo dice lo necesario", lambda: person("ruth", "deadpan", uid="q2"), "ruth", "#ff8fab"),
    ("Caro", "QA", "Cálida, pero ya vio este bug antes", lambda: person("caro", "smug", uid="q3"), "caro", "#9be15d"),
]
