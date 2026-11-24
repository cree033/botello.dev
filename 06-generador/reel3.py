"""Reel 2 v2 '6:03 pm, una linea' - personajes con boca articulada (Magnific video_speak).
Reutiliza reel2.py (camara, overlays, final, audio) y reemplaza los planos de personaje
por los clips parlantes. Uso:
  python3 reel3.py frames [ids]   -> /tmp/reel3/f
  (el audio se mezcla con reel2.py audio -> /tmp/reel2/audio_raw.wav)
"""
import sys, os
import numpy as np
from PIL import Image
from multiprocessing import Pool
import reel2 as R

CLIPS = "/tmp/reel3/clips/"
OUT = "/tmp/reel3/f"
W, H, FPS, FINAL = R.W, R.H, R.FPS, R.FINAL

# (inicio, fin, imagen, tipo, camara, clip, inicio_de_clip)
# inicio_de_clip = (momento en que suena la voz) + onset_voz - onset_clip
SHOTS = [
    (0.0, 3.2, "memo-dev_master-v2.png", "p", "zoom", "memo1", 0.85),
    (3.2, 5.6, "nacho-scrum-manager_master-v2.png", "p", "sway", "nacho1", 3.29),
    (5.6, 7.4, "memo-dev_master-v2.png", "p", "zoom", "memo2", 5.76),
    (7.4, 9.5, "nacho-scrum-manager_master-v2.png", "p", "sway", "nacho2", 7.55),
    (9.5, 10.3, "prod-server-rack_master-v2.png", "s", "shake", None, 0),
    (10.3, 12.0, "memo-dev_master-v2.png", "p", "zoom", "memo3", 10.35),
    (12.0, 14.6, "nacho-scrum-manager_master-v2.png", "p", "sway", "nacho3", 12.31),
    (14.6, 17.0, "ruth-pmo_master-v2.png", "p", "push", "ruth1", 14.8),
]

_mask = {}
def mask_for(th, tw, kind):
    k = (th, tw, kind)
    if k in _mask: return _mask[k]
    m = np.ones((th, tw), np.float32); f = 70
    for i in range(f):
        a = i / f
        m[i, :] *= a; m[th - 1 - i, :] *= a
    _mask[k] = m[..., None]
    return _mask[k]

_cf = {}
def clip_frame(name, idx):
    key = (name, idx)
    if key not in _cf:
        _cf[key] = np.array(Image.open(f"{CLIPS}{name}/{idx:04d}.png").convert("RGB")).astype(np.float32)
        if len(_cf) > 60: _cf.pop(next(iter(_cf)))
    return _cf[key]

_nf = {}
def nframes(name):
    if name not in _nf: _nf[name] = len(os.listdir(CLIPS + name))
    return _nf[name]

def base_for(shot, t):
    s0, s1, img, kind, cam, clip, c0 = shot
    base = R.load(img, kind)
    if not clip: return base
    n = nframes(clip)
    idx = int(round((t - c0) * 25)) + 1
    idx = max(1, min(n, idx))
    still_h = None
    # misma geometria que R.load para kind "p"
    arr_src = clip_frame(clip, idx)
    tw = 1080
    th = int(Image.open(R.SRC + img).height * tw / Image.open(R.SRC + img).width)
    top = 380
    im = Image.fromarray(arr_src.astype(np.uint8)).resize((tw, th), Image.LANCZOS)
    arr = np.array(im).astype(np.float32)
    out = base.astype(np.float32)
    y1 = min(H, top + th)
    m = mask_for(th, tw, "p")[: y1 - top]
    sub = out[top:y1, (W - tw) // 2:(W - tw) // 2 + tw]
    out[top:y1, (W - tw) // 2:(W - tw) // 2 + tw] = sub * (1 - m) + arr[: y1 - top] * m
    return out.astype(np.uint8)

def frame(i):
    t = i / FPS
    if t >= FINAL:
        out = R.final_card(t)
    else:
        for s in SHOTS:
            if s[0] <= t < s[1]: break
        base = base_for(s, t)
        out = R.camera(base, t, s[0], s[1], s[4])
        out = R.vignette_red(out, t)
        k = (t - s[0]) / 0.18
        if 0 <= k < 1 and s[0] > 0:
            out = (out.astype(np.float32) * R.ease(k) + np.array(R.NAVY) * (1 - R.ease(k))).astype(np.uint8)
        if s[0] == 0:
            out = (out.astype(np.float32) * R.ease(t / 0.4)).astype(np.uint8)
        out = R.overlay(out, t)
    Image.fromarray(out).save(f"{OUT}/{i:05d}.png", compress_level=1)
    return i

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    n = int(R.DUR * FPS)
    idx = [int(a) for a in sys.argv[2:]] or list(range(n))
    with Pool(2) as p:
        for _ in p.imap_unordered(frame, idx, chunksize=8): pass
