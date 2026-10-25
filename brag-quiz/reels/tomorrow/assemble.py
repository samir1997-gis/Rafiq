#!/usr/bin/env python3
"""The five versions of the tomorrow-people reel (SCRIPTS.md), assembled from the owner's one take before the reel template runs
(owner, 25 Oct 2026, #292). Each version is a list of stretches of the take; inside each, the voice is followed by its level
(10 ms steps) so no word is clipped, and pauses longer than 0.45 s close up to about 0.3 s. A "hold" is a stretch of him silent,
looped to a length: V3's recitation of al-Ḥijr 15:3 plays over it (behind the ayah screen). The template's own cut step is
skipped (chunks.json = the whole clip). Writes WORK/vN/clip.mp4 and WORK/vN/map.json ([out start, take start, length] per piece).

  python3 assemble.py WORK [vN ...]      (WORK has take.mp4 and a.wav: the take's 16 kHz mono audio)"""
import json, os, subprocess, sys
import numpy as np
W = sys.argv[1]; FPS = 30
REC = 15.2                                                  # al-Husary (Muallim) reciting 15:3: the words end at 14.91 s
V = {
 "v1": [(57.93, 93.1), (104.6, 124.4), (202.3, 230.4)],                     # 57.93: after a half-said "just-" (57.4)
 "v2": [(127.6, 148.2), (50.2, 53.6), (57.93, 76.6), (104.6, 124.4), (213.0, 230.4)],   # 50.2: he restarts "so who are…" (48.6)
 "v3": [(133.2, 148.2), (0.0, 30.4), ("hold", 30.6, REC), (35.2, 48.0), (213.0, 230.4)],
 "v4": [(151.0, 168.3), (169.7, 201.8), (104.6, 124.4), (213.0, 230.4)],
 "v5": [(77.3, 93.1), (57.93, 76.6), (127.6, 148.2), (185.5, 201.8), (213.0, 230.4)],
}
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f"{W}/a.wav", "-f", "s16le", "-"], capture_output=True).stdout, np.int16) / 32768
env = 20 * np.log10(np.sqrt(np.convolve(x ** 2, np.ones(320) / 320, "same"))[::160] + 1e-7)   # dB per 10 ms
room = np.percentile(env, 10); VOICE = room + 12

def pieces(a, b):
    """The spoken runs between a and b (s), each padded so soft starts and endings stay, pauses over 0.45 s closed to ~0.3 s."""
    on = env[int(a * 100):int(b * 100)] > VOICE; runs, i = [], 0
    while i < len(on):
        if on[i]:
            j = i
            while j < len(on) and on[j]: j += 1
            runs.append([i, j]); i = j
        else: i += 1
    merged = []
    for r in runs:
        if merged and r[0] - merged[-1][1] < 45: merged[-1][1] = r[1]
        else: merged.append(r)
    out = []
    for s, e in merged:
        if e - s < 6: continue                                # a click, not a word
        s0, e0 = a + s / 100 - .10, a + e / 100 + .16           # a breath before, the tail of the word after
        k = int(e0 * 100)                                       # follow the word's tail until it reaches the room's level
        while k < int(b * 100) and k < int(e0 * 100) + 30 and env[k] > room + 6: k += 1
        out.append([max(a, s0), min(b, max(e0, k / 100 + .04))])
    for p, q in zip(out, out[1:]):                              # never overlap; keep about 0.3 s between runs
        if q[0] - p[1] < 0: p[1] = q[0] = (p[1] + q[0]) / 2
    return out

for v, spans in V.items():
    if sys.argv[2:] and v not in sys.argv[2:]: continue
    d = os.path.join(W, v); os.makedirs(f"{d}/p", exist_ok=True); lst, mp, t = [], [], 0.0
    for sp in spans:
        if sp[0] == "hold": segs = [("hold", sp[1], sp[2])]
        else: segs = [("take", s, e - s) for s, e in pieces(*sp)]
        for kind, s, dur in segs:
            n = round(dur * FPS); dd = n / FPS; out = f"{d}/p/{len(lst):03d}.mov"
            if kind == "hold":                                  # his silent stretch, looped to the length
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s}", "-t", "4.4", "-i", f"{W}/take.mp4", "-c:v", "libx264", "-crf", "14", "-c:a", "pcm_s16le", f"{d}/hold.mov"], check=True)
                src = ["-stream_loop", "-1", "-i", f"{d}/hold.mov"]
            else: src = ["-ss", f"{s}", "-i", f"{W}/take.mp4"]
            subprocess.run(["ffmpeg", "-v", "error", "-y", *src, "-frames:v", str(n), "-vf", "scale=1440:2560:flags=lanczos,fps=30,format=yuv420p",
                            "-af", f"aresample=48000,atrim=duration={dd:.6f},asetpts=PTS-STARTPTS,apad,atrim=duration={dd:.6f},afade=t=in:d=0.012,afade=t=out:st={dd - 0.02:.4f}:d=0.02",
                            "-c:v", "libx264", "-crf", "14", "-preset", "fast", "-c:a", "pcm_s16le", "-ac", "2", out], check=True)
            lst.append(f"file '{out}'"); mp.append([round(t, 3), round(s, 3), round(dd, 3), kind]); t += dd
    open(f"{d}/p/list.txt", "w").write("\n".join(lst))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{d}/p/list.txt", "-c:v", "copy", "-c:a", "alac", f"{d}/clip.mp4"], check=True)
    json.dump(mp, open(f"{d}/map.json", "w")); json.dump([[0, round(t - .05, 3)]], open(f"{d}/chunks.json", "w"))
    print(v, round(t, 1), "s,", len(mp), "pieces")
