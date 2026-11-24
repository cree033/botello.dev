"""Reel 2 '6:03 pm, una linea' - motion comic con los masters de Magnific.
Uso: python3 reel2.py frames   (renderiza frames a /tmp/reel2/f)
     python3 reel2.py audio    (mezcla /tmp/reel2/audio.wav)
"""
import sys, os, math, wave, random
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
from multiprocessing import Pool

W, H, FPS, DUR = 1080, 1920, 30, 21.0
NAVY = (16, 19, 31)
SRC = "/mnt/user-data/outputs/Botello.Dev/05-assets/personajes/magnific/"
OUT = "/tmp/reel2/f"
VOX = "/tmp/reel2/a/"

F = "/usr/share/fonts/truetype/dejavu/"
def font(n, s): return ImageFont.truetype(F + n, s)
BOLD, MONO, REG = "DejaVuSans-Bold.ttf", "DejaVuSansMono-Bold.ttf", "DejaVuSans.ttf"

# (inicio, fin, imagen, tipo, camara)
SHOTS = [
    (0.0, 3.2, "memo-dev_master-v2.png", "p", "zoom"),
    (3.2, 5.6, "nacho-scrum-manager_master-v2.png", "p", "sway"),
    (5.6, 7.4, "memo-dev_master-v2.png", "p", "zoom"),
    (7.4, 10.3, "prod-server-rack_master-v2.png", "s", "shake"),
    (10.3, 12.0, "memo-dev_master-v2.png", "p", "zoom"),
    (12.0, 14.6, "nacho-scrum-manager_master-v2.png", "p", "sway"),
    (14.6, 17.0, "ruth-pmo_master-v2.png", "p", "push"),
]
FINAL = 17.0

# (inicio, fin, texto, quien)
SUBS = [
    (0.9, 2.3, "Es solo una línea.", "Memo"),
    (3.4, 4.1, "¿Tests?", "Nacho"),
    (5.8, 7.0, "Es una línea.", "Memo"),
    (7.6, 10.3, "¿Y esa línea... qué hacía?", "Nacho"),
    (10.4, 11.8, "Nada importante.", "Memo"),
    (12.4, 14.0, "...Aprobado.", "Nacho"),
    (14.9, 16.0, "¿Ya salió?", "Ruth"),
]
ACCENT = {"Memo": (76, 201, 240), "Nacho": (242, 169, 59), "Ruth": (255, 143, 171)}

_cache = {}
def load(name, kind):
    key = (name, kind)
    if key in _cache: return _cache[key]
    im = Image.open(SRC + name).convert("RGB")
    if kind == "p":
        tw = 1080; th = int(im.height * tw / im.width); top = 380
    else:
        tw = 1080; th = 1080; top = 330
    im = im.resize((tw, th), Image.LANCZOS)
    arr = np.array(im).astype(np.float32)
    bg = np.median(arr[:20, :, :].reshape(-1, 3), axis=0)
    canvas = np.empty((H, W, 3), np.float32)
    ys = np.linspace(0, 1, H)[:, None, None]
    canvas[:] = bg * (1 - 0.35 * ys) + np.array(NAVY) * 0.35 * ys
    x0 = (W - tw) // 2
    mask = np.ones((th, tw), np.float32)
    f = 70
    for i in range(f):
        a = i / f
        mask[i, :] *= a; mask[th - 1 - i, :] *= a
        mask[:, i] *= a if kind == "s" else 1
        mask[:, tw - 1 - i] *= a if kind == "s" else 1
    y1 = min(H, top + th)
    sub = canvas[top:y1, x0:x0 + tw]
    m = mask[: y1 - top, :tw][..., None]
    canvas[top:y1, x0:x0 + tw] = sub * (1 - m) + arr[: y1 - top] * m
    _cache[key] = canvas.astype(np.uint8)
    return _cache[key]

def ease(x): x = max(0, min(1, x)); return x * x * (3 - 2 * x)

def camera(img, t, t0, t1, mode):
    p = (t - t0) / (t1 - t0)
    cx, cy, s = W / 2, H / 2, 1.0
    if mode == "zoom": s = 1.0 + 0.07 * ease(p)
    elif mode == "sway":
        s = 1.02 + 0.04 * ease(p); cx += 10 * math.sin(t * 2.6); cy += 6 * math.sin(t * 3.4)
    elif mode == "push": s = 1.12 - 0.08 * ease(p * 1.6)
    elif mode == "shake":
        k = 4 + 10 * ease(p)
        rnd = random.Random(int(t * FPS))
        cx += rnd.uniform(-k, k); cy += rnd.uniform(-k, k)
        beat = max(0.0, math.sin(t * 2 * math.pi * 1.7)) ** 6
        s = 1.04 + 0.05 * beat + 0.03 * p
    M = cv2.getRotationMatrix2D((W / 2, H / 2), 0, s)
    M[0, 2] += cx - W / 2; M[1, 2] += cy - H / 2
    return cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

def text_center(d, y, txt, fnt, fill, stroke=0, sf=(0, 0, 0)):
    w = d.textlength(txt, font=fnt)
    d.text(((W - w) / 2, y), txt, font=fnt, fill=fill, stroke_width=stroke, stroke_fill=sf)

def overlay(img, t):
    pil = Image.fromarray(img).convert("RGBA")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    # hora arriba
    if t < FINAL:
        a = 255
        if t < 3.2:
            fa = ease(t / 0.5)
            d.rounded_rectangle((170, 235, 910, 355), 28, fill=(10, 13, 22, int(190 * fa)))
            text_center(d, 258, "Viernes, 6:03 pm.", font(BOLD, 64), (255, 255, 255, int(255 * fa)))
        elif 7.4 <= t < 10.3:
            d.rounded_rectangle((90, 235, 990, 375), 26, fill=(10, 13, 22, 235), outline=(255, 107, 107, 255), width=3)
            d.text((130, 252), "1 archivo · 1 línea", font=font(REG, 30), fill=(150, 160, 190, 255))
            d.text((130, 298), "-  WHERE id = @id", font=font(MONO, 48), fill=(255, 107, 107, 255))
        else:
            d.rounded_rectangle((380, 245, 700, 320), 20, fill=(10, 13, 22, 170))
            text_center(d, 255, "6:03 pm", font(BOLD, 46), (230, 235, 250, 255))
    # subtitulos
    for s0, s1, txt, who in SUBS:
        if s0 <= t < s1 + 0.25:
            fa = ease((t - s0) / 0.12) * (1 - ease((t - s1) / 0.25))
            fnt = font(BOLD, 62)
            w = d.textlength(txt, font=fnt)
            y = 1440
            d.rounded_rectangle(((W - w) / 2 - 36, y - 24, (W + w) / 2 + 36, y + 96), 30, fill=(8, 10, 18, int(215 * fa)))
            d.text((W / 2 - w / 2, y), txt, font=fnt, fill=(255, 255, 255, int(255 * fa)))
            c = ACCENT[who]
            lab = font(BOLD, 30); lw = d.textlength(who.upper(), font=lab)
            d.rounded_rectangle(((W - lw) / 2 - 18, y - 84, (W + lw) / 2 + 18, y - 32), 16, fill=c + (int(255 * fa),))
            d.text(((W - lw) / 2, y - 79), who.upper(), font=lab, fill=(12, 14, 22, int(255 * fa)))
    # sello aprobado
    if 13.8 <= t < 14.6:
        p = ease((t - 13.8) / 0.2)
        r = int(110 * (0.6 + 0.4 * p))
        cx, cy = 820, 560
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(40, 200, 110, int(235 * p)))
        fn = font(BOLD, int(130 * p) + 10)
        w = d.textlength("✔", font=fn)
        d.text((cx - w / 2, cy - 78 * p - 8), "✔", font=fn, fill=(255, 255, 255, int(255 * p)))
    pil = Image.alpha_composite(pil, ov).convert("RGB")
    return np.array(pil)

def vignette_red(img, t):
    if 7.4 <= t < 10.3:
        beat = max(0.0, math.sin(t * 2 * math.pi * 1.7)) ** 4
        h, w = img.shape[:2]
        yy, xx = np.mgrid[0:h, 0:w]
        r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
        a = np.clip((r - 0.55) / 0.9, 0, 1) * (0.25 + 0.35 * beat)
        img = img.astype(np.float32)
        img[..., 0] = img[..., 0] * (1 - a) + 255 * a
        img[..., 1] *= (1 - a); img[..., 2] *= (1 - a)
        return np.clip(img, 0, 255).astype(np.uint8)
    return img

def final_card(t):
    img = np.empty((H, W, 3), np.uint8); img[:] = NAVY
    pil = Image.fromarray(img).convert("RGBA")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    u = t - FINAL
    def line(t0, y, txt, fnt, col):
        a = ease((u - t0) / 0.3)
        text_center(d, y + (1 - a) * 20, txt, fnt, col[:3] + (int(255 * a),))
    line(0.1, 620, "6:04 pm.", font(BOLD, 86), (230, 235, 250, 255))
    line(0.9, 790, "Aprobado por 1 persona.", font(BOLD, 62), (255, 255, 255, 255))
    line(1.6, 880, "(que también es QA y PMO)", font(REG, 40), (242, 169, 59, 255))
    line(2.4, 1010, "Leído por 0.", font(BOLD, 86), (255, 107, 107, 255))
    line(3.2, 1290, "botello.dev", font(MONO, 48), (57, 255, 136, 255))
    return np.array(Image.alpha_composite(pil, ov).convert("RGB"))

def frame(i):
    t = i / FPS
    if t >= FINAL:
        out = final_card(t)
    else:
        for s in SHOTS:
            if s[0] <= t < s[1]: break
        base = load(s[2], s[3])
        out = camera(base, t, s[0], s[1], s[4])
        out = vignette_red(out, t)
        # fundido de 0.18 s al inicio de cada plano
        k = (t - s[0]) / 0.18
        if 0 <= k < 1 and s[0] > 0:
            out = (out.astype(np.float32) * ease(k) + np.array(NAVY) * (1 - ease(k))).astype(np.uint8)
        if s[0] == 0:
            out = (out.astype(np.float32) * ease(t / 0.4)).astype(np.uint8)
        out = overlay(out, t)
    Image.fromarray(out).save(f"{OUT}/{i:05d}.png", compress_level=1)
    return i

def readwav(n):
    w = wave.open(VOX + n + ".wav")
    return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768

def audio():
    sr = 44100
    N = int(DUR * sr); mix = np.zeros(N, np.float32)
    t = np.arange(N) / sr
    rng = np.random.default_rng(3)
    # zumbido de oficina
    hum = 0.012 * np.sin(2 * np.pi * 60 * t) + 0.006 * np.sin(2 * np.pi * 120 * t)
    noise = rng.normal(0, 1, N).astype(np.float32)
    k = np.ones(400) / 400
    air = np.convolve(noise, k, mode="same") * 0.05
    mix += (hum + air) * np.where(t < FINAL, 1.0, 0.0)
    # latido de Prod 7.4 a 10.3
    for bt in np.arange(7.4, 10.3, 1 / 1.7):
        for off, g in ((0, 1.0), (0.18, 0.6)):
            s = int((bt + off) * sr); L = int(0.16 * sr)
            if s + L < N:
                tt = np.arange(L) / sr
                mix[s:s + L] += g * 0.5 * np.sin(2 * np.pi * (70 - 120 * tt) * tt) * np.exp(-tt * 22)
    # teclas
    for tk in (3.0, 3.07, 5.5):
        s = int(tk * sr); L = int(0.05 * sr)
        mix[s:s + L] += rng.normal(0, 1, L) * np.exp(-np.arange(L) / (0.008 * sr)) * 0.12
    # clic de aprobado 13.8
    s = int(13.8 * sr); L = int(0.14 * sr); tt = np.arange(L) / sr
    mix[s:s + L] += 0.35 * np.sin(2 * np.pi * 1200 * tt) * np.exp(-tt * 40) + 0.2 * np.sin(2 * np.pi * 1800 * tt) * np.exp(-tt * 60)
    # golpe final 17.0 y 19.4 (Leido por 0)
    for hit, g in ((FINAL + 0.1, 0.6), (FINAL + 2.4, 0.9)):
        s = int(hit * sr); L = int(0.9 * sr); tt = np.arange(L) / sr
        mix[s:s + L] += g * np.sin(2 * np.pi * (55 - 20 * tt) * tt) * np.exp(-tt * 5)
    # voces
    for name, at in (("voz_memo1", 0.9), ("voz_nacho1", 3.4), ("voz_memo2", 5.8), ("voz_nacho2", 7.6),
                     ("voz_memo3", 10.4), ("voz_nacho3", 12.4), ("voz_ruth1", 14.9)):
        v = readwav(name); s = int(at * sr)
        mix[s:s + len(v)] += v * 1.0
    mix = np.clip(mix, -1, 1)
    out = (mix * 32767).astype(np.int16)
    w = wave.open("/tmp/reel2/audio_raw.wav", "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes(out.tobytes()); w.close()

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    if sys.argv[1] == "frames":
        n = int(DUR * FPS)
        idx = [int(a) for a in sys.argv[2:]] or list(range(n))
        with Pool(2) as p:
            for _ in p.imap_unordered(frame, idx, chunksize=8): pass
    else:
        audio()
