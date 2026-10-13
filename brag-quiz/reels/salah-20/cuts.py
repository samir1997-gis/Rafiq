"""The owner's shorter cut (13 Oct 2026): lines taken out of the take, on top of the silence cut. Each edge snaps to the quietest
20 ms within a quarter-second, so no word is clipped. Writes chunks.json (keeps the silence-only cut as chunks-silence.json).
  python3 cuts.py /tmp/reel-salah        (after `reel.py <W> cut`, before `base`)"""
import json, os, shutil, subprocess, sys, numpy as np
W = sys.argv[1]
CUTS = [(1.10, 7.30),      # you pass away, you're buried,
        (41.30, 46.85),    # So I have a question to ask you and be honest with the answer.
        (49.30, 51.60),    # Are you?
        (53.75, 56.70),    # and you are struggling with khushu in your salah,   (13 Oct, second round)
        (74.30, 79.05),    # excluding the surahs you recite after al-Fatihah. Only 20.   (on screen instead, so the 56% stays accurate)
        (79.05, 91.05),    # Now, do you think learning 20 words is difficult? No, but those 20 words can have such a profound impact on your salah.
        (93.10, 94.10, 1), # you   ("from just performing actions"); exact: the snap found quiet inside the words here
        (95.27, 96.68, 1), # and not understanding what you're saying
        (98.74, 100.24),   # and have a conversation   ("to actually being able to connect with your Lord")
        (101.15, 108.05),  # and coming out of the salah feeling like you actually worshipped your Lord.
        (110.30, 111.75),  # probably yes.
        (118.70, 120.55),  # Not at all.  (the second)
        (132.08, 136.90),  # and make the intention to start learning the Arabic language, or at least
        (140.92, 142.28)]  # again and again, then
if not os.path.exists(os.path.join(W, "chunks-silence.json")): shutil.copy(os.path.join(W, "chunks.json"), os.path.join(W, "chunks-silence.json"))
ch = json.load(open(os.path.join(W, "chunks-silence.json")))
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(W, "audio.wav"), "-f", "s16le", "-ac", "1", "-ar", "16000", "-"],
                                 capture_output=True).stdout, np.int16).astype(float)
def quiet(t):                                             # the quietest 20 ms around t
    best, at = 1e18, t
    for c in np.arange(t - .25, t + .25, .01):
        a = int(c * 16000); e = np.mean(x[max(0, a - 160):a + 160] ** 2) if a > 0 else 0
        if e < best: best, at = e, c
    return round(float(at), 3)
cuts = [(a, b) if exact else (quiet(a), quiet(b)) for a, b, *exact in CUTS]   # a third value: set by hand from the level, no snapping
out = []
for a, b in ch:                                           # each kept piece, minus every cut that overlaps it
    segs = [[a, b]]
    for c0, c1 in cuts:
        segs = [s for g in segs for s in ([[g[0], min(g[1], c0)], [max(g[0], c1), g[1]]] if c0 < g[1] and c1 > g[0] else [g])]
    out += [s for s in segs if s[1] - s[0] > 0.05]
json.dump(out, open(os.path.join(W, "chunks.json"), "w"))
print(len(out), "pieces,", round(sum(round((b - a) * 30) / 30 for a, b in out), 1), "s; cuts at", cuts)
