#!/usr/bin/env python3
"""Are the sound effects really in the finished video? (owner, 30 Oct 2026: "make sure the sound effects are actually in the video, unlike
other times where they've just been silent"). For every effect the edit placed (config.json "audio"), its loudest moment in the mixed
effects track (sfx.wav) against his voice's peaks, and, where it falls between his words, the finished video's level there against the
same moment with his voice alone. Fails loudly if any effect is missing.
  check.py WORK/vN PILE OUT.mp4"""
import json, subprocess, sys
import numpy as np
D, P, O = sys.argv[1], float(sys.argv[2]), sys.argv[3]
rd = lambda f: np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout, np.int16) / 32768
db = lambda x: 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)
C = json.load(open(f"{D}/config.json")); sfx, voice, fin = rd(f"{D}/sfx.wav"), rd(f"{D}/cut.wav"), rd(O)
vp = np.percentile([db(voice[i:i + 800]) for i in range(0, len(voice) - 800, 400)], 90)
rows, bad = [], 0
for f, t, v in C["audio"]:
    i = int(t * 16000); seg = sfx[i:i + 16000]
    pk = max(db(seg[j:j + 800]) for j in range(0, max(1, len(seg) - 800), 400)) if len(seg) > 800 else -99
    k = int((t + P) * 16000); quiet = db(voice[i:i + 4000]) < vp - 18           # between his words
    lift = db(fin[k:k + 4000]) - db(voice[i:i + 4000]) if quiet else None
    ok = pk > vp - 24 and (lift is None or lift > 3)
    bad += not ok; rows.append(f"{t:6.2f}s {f.split('/')[-1]:14s} peak {pk - vp:+5.1f} dB vs his voice" + (f", +{lift:4.1f} dB in the video" if lift is not None else "") + ("" if ok else "  ← TOO QUIET"))
print("\n".join(rows)); print(f"{len(rows)} effects, {bad} too quiet")
sys.exit(1 if bad else 0)
