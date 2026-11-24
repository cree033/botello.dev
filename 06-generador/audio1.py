"""Diseño de sonido original (sintetizado) para el Reel 1. Sin samples ni música de terceros."""
import os
import sys
import wave

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import reel1 as R

SR = 44100
n = int(R.DUR * SR)
t = np.arange(n) / SR
out = np.zeros(n)
rng = np.random.default_rng(7)


def ease(x):
    x = np.clip(x, 0, 1)
    return x * x * (3 - 2 * x)


def add(sig, at):
    i = int(at * SR)
    j = min(n, i + len(sig))
    if i < n:
        out[i:j] += sig[: j - i]


def tone(freq, dur, amp, decay):
    x = np.arange(int(dur * SR)) / SR
    return amp * np.sin(2 * np.pi * freq * x) * np.exp(-x / decay)


def sweep(f0, f1, dur, amp, decay):
    x = np.arange(int(dur * SR)) / SR
    f = f0 + (f1 - f0) * (x / dur)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return amp * np.sin(ph) * np.exp(-x / decay)


def click(amp):
    x = np.arange(int(0.03 * SR)) / SR
    noise = np.diff(rng.uniform(-1, 1, len(x) + 1))
    return amp * noise * np.exp(-x / 0.006) + tone(170, 0.03, amp * 0.5, 0.008)


# --- zumbido grave que sube con la tensión ---
amp_env = np.where(t < R.T_ENTER, 0.05, 0.05 + 0.09 * ease((t - R.T_ENTER) / 3.5))
amp_env = np.where(t >= R.T_CALM, 0.025, amp_env)
amp_env = np.where(t >= R.T_CUT, 0.0, amp_env)
mult = 1 + 0.25 * ease((t - R.T_ENTER) / 5.5)
mult = np.where(t >= R.T_CALM, 1.0, mult)
ph = 2 * np.pi * np.cumsum(55 * mult) / SR
drone = 0.6 * np.sin(ph) + 0.4 * np.sin(1.5 * ph) + 0.2 * np.sin(1.012 * ph)
# corte seco al calmarse Prod
gate = np.where((t >= R.T_CALM) & (t < R.T_CALM + 0.03), 0.0, 1.0)
out += drone * amp_env * gate

# --- pitidos de la luz roja de Prod ---
for tb in R.beep_times():
    add(tone(880 if tb < R.T_ENTER else 1175, 0.07, 0.10, 0.02), tb)

# --- teclas mientras el dev escribe ---
for k in range(len(R.CMD)):
    add(click(0.13), R.T_TYPE0 + (R.T_TYPE1 - R.T_TYPE0) * (k + 1) / len(R.CMD))
add(click(0.26), R.T_ENTER - 0.1)  # enter

# --- latido de pánico ---
b = 8.0
while b < R.T_CALM:
    add(tone(60, 0.25, 0.22, 0.07), b)
    add(tone(55, 0.25, 0.14, 0.07), b + 0.14)
    b += 0.5

# --- apagón de Prod y golpe final ---
add(sweep(220, 40, 0.6, 0.22, 0.25), R.T_CALM)
add(sweep(110, 35, 0.8, 0.42, 0.28), R.T_CUT)
add(click(0.08), 17.45)

# --- master ---
out *= 0.62 / max(1e-9, np.max(np.abs(out)))
out *= np.clip((R.DUR - t) / 0.4, 0, 1)
pcm = (np.clip(out, -1, 1) * 32767).astype("<i2")
os.makedirs("/tmp/reel1", exist_ok=True)
with wave.open("/tmp/reel1/audio.wav", "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print("audio ok", len(pcm) / SR, "s")

# --- nivel para Reels: compresión suave + normalizar a -14 LUFS (sin esto queda a -24 LUFS y casi no se oye) ---
import subprocess
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "/tmp/reel1/audio.wav", "-af",
                "acompressor=threshold=-34dB:ratio=4:attack=5:release=150:makeup=4,loudnorm=I=-14:TP=-1.5:LRA=7",
                "-ar", "44100", "/tmp/reel1/audio_loud.wav"], check=True)
print("audio_loud ok: usar /tmp/reel1/audio_loud.wav al codificar")
