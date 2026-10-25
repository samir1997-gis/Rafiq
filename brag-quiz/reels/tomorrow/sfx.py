#!/usr/bin/env python3
"""Sounds made for the tomorrow-people reel (owner, 25 Oct 2026: "make it more engaging with sound effects… when the door closes,
a loud door closing"), written to brag-quiz/sfx/soft/: doorslam (a heavy wooden door: thud, latch, room), impact (a deep cinematic
hit with a long tail), rumble (a low dark bed), wind (graveyard night air), crackle (fire, under the Jahannam ayah), flip (a paper
page turning), rip (a calendar page torn off).   python3 sfx.py"""
import os, wave
import numpy as np
from scipy.signal import butter, sosfilt
SR = 48000; OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "sfx", "soft"); rng = np.random.default_rng(11)
t_ = lambda d: np.arange(int(SR * d)) / SR
bp = lambda x, lo, hi, o=4: sosfilt(butter(o, [lo, hi], "band", fs=SR, output="sos"), x)
lp = lambda x, f, o=4: sosfilt(butter(o, f, "low", fs=SR, output="sos"), x)
def room(x, d=0.9, mix=0.35):                                      # a small hall: decaying noise convolved in
    ir = rng.standard_normal(int(SR * d)) * np.exp(-t_(d) * 6); ir = lp(ir, 5000)
    return x + mix * np.convolve(x, ir)[:len(x)] / np.abs(ir).sum() * 40
def save(n, x, pad=0.0):
    x = np.concatenate([x, np.zeros(int(SR * pad))]); x = x / (np.abs(x).max() + 1e-9) * 0.89
    w = wave.open(os.path.join(OUT, n + ".wav"), "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype(np.int16).tobytes()); w.close()
d = 1.6; t = t_(d)
thud = np.sin(2 * np.pi * (55 + 40 * np.exp(-t * 18)) * t) * np.exp(-t * 7)                 # the body of the door hitting the frame
wood = bp(rng.standard_normal(len(t)), 150, 1800) * np.exp(-t * 28)
latch = np.zeros(len(t)); i = int(SR * .045); latch[i:i + 900] = bp(rng.standard_normal(900), 2500, 7000) * np.exp(-np.arange(900) / 120)
save("doorslam", room(thud * 1.0 + wood * 0.7 + latch * 0.5, 1.2, 0.5))
d = 3.0; t = t_(d)
save("impact", room(np.sin(2 * np.pi * (42 + 70 * np.exp(-t * 9)) * t) * np.exp(-t * 2.2) + lp(rng.standard_normal(len(t)), 400) * np.exp(-t * 6) * .6, 2.0, .5))
d = 6.0; t = t_(d)
save("rumble", lp(rng.standard_normal(len(t)), 120, 2) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.23 * t)) * np.minimum(1, t / 1.0) * np.minimum(1, (d - t) / 1.0))
d = 8.0; t = t_(d)
gust = 0.5 + 0.5 * np.sin(2 * np.pi * 0.17 * t + 1) * np.sin(2 * np.pi * 0.05 * t)
save("wind", bp(rng.standard_normal(len(t)), 250, 1400, 2) * (0.3 + 0.7 * gust) * np.minimum(1, t / 1.2) * np.minimum(1, (d - t) / 1.2))
d = 8.0; t = t_(d); c = np.zeros(len(t))
for k in rng.integers(0, len(t) - 400, 260): c[k:k + 400] += bp(rng.standard_normal(400), 1500, 6000) * np.exp(-np.arange(400) / 60) * rng.uniform(.2, 1)
save("crackle", c + lp(rng.standard_normal(len(t)), 300) * 0.4 * np.minimum(1, t / 1.0) * np.minimum(1, (d - t) / 1.0))
d = 0.35; t = t_(d)
save("flip", bp(rng.standard_normal(len(t)), 900, 6000) * np.sin(np.pi * np.minimum(1, t / d)) ** 2 * (1 + 0.6 * np.sin(2 * np.pi * 34 * t)))
d = 0.6; t = t_(d); r = bp(rng.standard_normal(len(t)), 1200, 8000) * (rng.random(len(t)) < .35)
save("rip", r * np.minimum(1, t / 0.05) * np.exp(-np.maximum(0, t - .35) * 18) + bp(rng.standard_normal(len(t)), 300, 1500) * 0.3 * np.exp(-t * 6))
print("made: doorslam impact rumble wind crackle flip rip")
