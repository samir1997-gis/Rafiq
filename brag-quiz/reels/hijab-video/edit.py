#!/usr/bin/env python3
"""The edit of the owner's hijab video (30 Oct 2026, #307): his own cut (no silences to take out; "you don't need to edit any clips or
silences"), in three lengths; the pile-on in front (finish.sh); full-screen graphics (graphics.py) on every ayah and descriptive moment,
each ayah in Arabic, English and its reference; a few titles behind his head; sound effects at every graphic's beats, set against his own
voice (VP) and checked in the finished mix (check.py).

  python3 edit.py WORK vN chunks     write WORK/vN/chunks.json (the version's pieces of the take) and link clip.mp4
  python3 edit.py WORK vN            after the template's base and plan: fill in WORK/vN/config.json"""
import json, os, re, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); G = os.path.join(HERE, "out"); SFX = os.path.join(HERE, "..", "..", "sfx")
W, V = sys.argv[1], sys.argv[2]; D = os.path.join(W, V)
SEG = dict(A=(0, 11.22), B=(11.22, 18.78), C=(18.78, 29.30), D=(29.30, 41.64), E=(41.64, 48.87), F=(48.87, 56.26), G=(56.26, 63.41),
           H=(63.41, 73.78), I=(73.78, 84.60), J=(84.60, 91.42), K=(91.42, 104.58), L=(104.58, 114.72), L3=(105.16, 114.72))
VERS = {"v1": "A B C D E F G H I J K L", "v2": "A B C D G H I K L", "v3": "A C D H I L3"}   # v2: without Ṣād, Maryam and the Jahannam line; v3: the core
CH = [SEG[k] for k in VERS[V].split()]
if sys.argv[3:] == ["chunks"]:
    os.makedirs(D, exist_ok=True)
    if not os.path.exists(f"{D}/clip.mp4"): os.symlink(os.path.join(W, "src.mov"), f"{D}/clip.mp4")
    json.dump([list(c) for c in CH], open(f"{D}/chunks.json", "w")); print(V, round(sum(round((b - a) * 30) / 30 for a, b in CH), 1), "s"); sys.exit()

OFF, o = [], 0.0
for a, b in CH: OFF.append((a, b, o)); o += round((b - a) * 30) / 30
def vt(t):                                                    # a time in the take → in this version (None if that part is cut)
    for a, b, off in OFF:
        if a - 0.02 <= t <= b + 0.02: return round(off + max(0, t - a), 2)
C = json.load(open(f"{D}/config.json")); END = C["end"]
sys.path.insert(0, os.path.join(HERE, "..", "template")); from sfx_rules import info
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f"{D}/cut.wav", "-f", "s16le", "-"], capture_output=True).stdout, np.int16) / 32768
VP = float(np.percentile(20 * np.log10(np.sqrt(np.convolve(x ** 2, np.ones(800) / 800, "valid"))[::400] + 1e-9), 90))   # his words' loudest 50 ms
lvl = lambda f: float(re.findall(r"I:\s+(-?[\d.]+) LUFS", subprocess.run(["ffmpeg", "-i", f, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr)[-1])
VL = lvl(f"{D}/cut.wav"); AUDIO = []
def fx(name, t, db=0.0):                                      # a sound whose loudest 50 ms lands on take time t, db against his voice's peaks
    t = vt(t)
    if t is None: return
    f = next(os.path.join(SFX, d, name + ".wav") for d in ("soft", "ref", "owner", ".") if os.path.exists(os.path.join(SFX, d, name + ".wav")))
    pk_db, pk = info(f); AUDIO.append([f, round(max(0, t - pk), 3), round(10 ** ((VP + db - pk_db) / 20), 3)])
def bed(name, t0, t1, db):                                    # a texture under a graphic, db against his voice's loudness
    a, b = vt(t0), vt(t1)
    if a is None or b is None: return
    out = f"{D}/bed{len(AUDIO)}.wav"; d = max(0.6, b - a)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-stream_loop", "-1", "-i", os.path.join(SFX, "soft", name + ".wav"), "-t", f"{d:.2f}",
                    "-af", f"afade=t=in:d=0.3,afade=t=out:st={d - 0.4:.2f}:d=0.4", "-ar", "48000", "-ac", "2", out], check=True)
    AUDIO.append([out, a, round(10 ** ((VL + db - lvl(out)) / 20), 3)])

# the graphics: [their span in the take], and their sounds (take times)
from importlib.machinery import SourceFileLoader
T = SourceFileLoader("g", os.path.join(HERE, "graphics.py")).load_module().T
T = dict(T, sisters=(99.54, 104.58))                          # "our hijabi sisters are at the forefront of persecution": the pile-on again, its crowd
panels = []
for gid, (t0, t1) in T.items():
    s0, frm = vt(t0), 0.0
    if s0 is None:                                            # the graphic's start is cut in this version: begin where its piece starts
        a = next((a for a, b, _ in OFF if t0 < a < t1 - 1), None)
        if a is None: continue
        s0, frm = vt(a), a - t0
    s1 = vt(t1)
    if s1 is None: s1 = next(off + (b - a) for a, b, off in OFF if a <= t0 + frm < b)   # the end of the piece it starts in
    if s1 - s0 < 0.5: continue                                # only a sliver of it is left in this version
    src = os.path.join(G, gid + ".mp4") if gid != "sisters" else os.path.join(HERE, "..", "..", "out", "hijab", "hijab-pileon-anim.mp4")
    if gid == "sisters": frm += 8.6                           # the crowd and its bubbles, mid-build
    panels.append([round(s0, 2), round(min(s1, END), 2), "gfx", dict(src=src, **({"from": round(frm, 2)} if frm else {}), slams=[], hits=[])])
SOUNDS = [lambda: [fx("whoosh", 0.62, -10)] + [fx("tap", 0.8 + i * 0.4, -6) for i in range(6)],
          lambda: [fx("whoosh", 6.1, -10), fx("tick-lo", 8.44, -6), fx("scratch", 9.82, -8), fx("impact", 10.2, -2)],
          lambda: [fx("shimmer", 14.1, -10), fx("whoosh", 16.6, -8), fx("impact", 17.2, 0)],
          lambda: [fx("thump", t, -2) for t in (22.45, 22.95, 23.45)] + [fx("shimmer", 24.4, -10), fx("swoosh", 26.9, -6), fx("tap", 28.12, -6)],
          lambda: [fx("whoosh", 30.1, -10), fx("thump", 35.7, 0), fx("impact", 35.9, -4), bed("crackle", 40.3, 41.6, -14), fx("whoosh", 40.4, -10)],
          lambda: [fx("whoosh", 41.94, -10), bed("wind", 45.0, 48.8, -16), fx("thump", 46.6, -4)],
          lambda: [fx("whoosh", 49.28, -10), fx("swoosh", 52.86, -4), fx("tick-lo", 53.3, -6)],
          lambda: [fx("whoosh", 56.62, -10), fx("shimmer", 59.24, -8), bed("drone", 59.2, 63.4, -18), fx("tick-lo", 61.6, -6)],
          lambda: [fx("whoosh", 64.2, -10), fx("impact", 69.4, 0), fx("tick-lo", 70.6, -6), fx("impact", 72.86, 1)],
          lambda: [fx("thump", 79.8, -2)] + [fx("tap", t, -6) for t in (80.6, 81.56, 82.56)] + [fx("thump", 84.18 + k * 0.12, -4) for k in range(3)],
          lambda: [fx("shimmer", 85.1, -8), bed("crackle", 87.74, 91.4, -14), fx("whoosh", 90.36, -8)],
          lambda: [fx("impact", t, 1) for t in (97.36, 97.82, 98.54)] + [fx("thump", t, -2) for t in (97.36, 97.82, 98.54)],
          lambda: [fx("impact", 99.6, -4), bed("rumble", 99.6, 104.4, -16)],
          lambda: [fx("shimmer", 106.38, -8), fx("tick-lo", 108.0, -6)],
          lambda: [fx("shimmer", 109.8, -8), fx("impact", 113.6, -3)]]
for s in SOUNDS: s()

def title(t0, t1, small, big, size):
    a, b = vt(t0), vt(t1)
    if a is not None and b is not None: return [a, b, small, big, size]
titles = [x for x in (title(3.74, 5.9, "MOST PEOPLE", "DON'T KNOW", 260), title(11.36, 12.9, "WHAT ABOUT", "HIJAB?", 330),
                      title(74.02, 79.5, "NOT JUST A", "PIECE OF CLOTH", 180), title(91.42, 95.7, "IN THIS DAY AND AGE", "NOT EASY", 300)) if x]

FIX = {"hajibb": "ḥ-j-b", "ahraf": "al-Aʿrāf,", "saad": "Ṣād,", "ashurah": "ash-Shūrā,", "murkhiyamah": "Yawm al-Qiyāmah.", "jahannam": "Jahannam",
       "inshaallah": "in shā’ Allāh", "musa": "Mūsā,", "quran": "Qur’an"}
nz = lambda w: re.sub(r"[^a-z]", "", w.lower())
EM = set("opinion different cover bigger root shield paradise jahannam sun hides maryam musa men first gaze cloth scarf covering protection "
         "barrier evil easy banned persecution protect sisters qiyamah".split())
for c in C["caps"]:
    for w in c[2]:
        k = nz(w[0])
        if k == "al" and w[0].strip() == "Al": w[0] = ""
        elif k in FIX: w[0] = FIX[k]
        w[2] = k in EM
    c[2] = [w for w in c[2] if w[0]]
C["caps"] = [c for c in C["caps"] if c[2]]
C["title_top"] = 470; C["titles"] = sorted(titles); C["flicks"] = []; C["split"] = None; C["steps"] = []
PANELS = sorted(panels)
for p, q in zip(PANELS, PANELS[1:]): p[1] = min(p[1], q[0])
C["panels"] = PANELS
C["audio"] = [a for a in AUDIO if 0 <= a[1] < END]
busy = [(p[0], p[1]) for p in PANELS] + [(t[0], t[1]) for t in titles]
em = [w for c in C["caps"] for w in c[2] if w[2] and not any(a - .4 <= w[1] < b + .4 for a, b in busy)]
C["punch"] = [[w[1], w[1] + 0.4] for w in em][:6]
cuts = sorted({0, END} | {x for a, b in busy for x in (a, b)} | {off for _, _, off in OFF})
C["sections"] = [[a, b] for a, b in zip(cuts, cuts[1:]) if b - a > .3]
json.dump(C, open(f"{D}/config.json", "w"), indent=1, ensure_ascii=False)
json.dump([[round(t, 3) for _, t, _ in C["audio"]]], open(f"{D}/sfx-times.json", "w"))
print(V, "end", END, "| panels", [(p[0], p[1], os.path.basename(p[3]["src"])) for p in PANELS], "\n titles", titles, "\n sounds", len(C["audio"]))
