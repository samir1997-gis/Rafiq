#!/usr/bin/env python3
"""The Dajjāl edit's config (#316), after the template's base and plan: the graphics (brag-quiz/reels/scripts-gfx, re-timed onto his words
with WARP and rendered into WORK/gfx), titles behind his head for the lines without a graphic, sound effects on every beat set against his
own voice, and the captions' spellings. Times are written in the take (clip.mp4, from words.json) and moved into the cut through chunks.json.
Not used from the script's set: d_word (the intro has its own title), d_masih and d_dua (he didn't say those parts).

  python3 config.py WORK        (then reel.py WORK zoom / masks / layers / "mix keepvoice")
"""
import json, os, re, subprocess, sys
import numpy as np
W = sys.argv[1]; HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
GFX = os.path.join(ROOT, "brag-quiz/reels/scripts-gfx"); SFX = os.path.join(ROOT, "brag-quiz/sfx")
J = lambda f: json.load(open(os.path.join(W, f)))
OFF, o = [], 0.0
for a, b in J("chunks.json"): OFF.append((a, b, o)); o += round((b - a) * 30) / 30
def vt(t):                                    # a time in the take → in the cut (a time inside a removed pause moves to the next kept piece)
    for a, b, off in OFF:
        if t < a: return round(off, 2)
        if t <= b: return round(off + t - a, 2)
    return round(o, 2)
C = J("config.json"); END = C["end"]

# ---- the graphics: (gid, take start, take end, [(planned s in the clip, take time of the word it lands on)], its sounds [(name, take t, dB)])
G = [
 ("d_root", 43.9, 62.95, [(0.05, 44.26), (1.15, 45.4), (2.25, 46.56), (3.6, 58.74), (4.4, 61.2)],
  [("whoosh", 43.9, -10), ("tap", 44.26, 4), ("tap", 45.4, -4), ("tap", 46.56, 2), ("impact", 61.2, -2)]),
 ("d_camel", 111.3, 117.92, [(0.05, 111.35), (1.4, 114.8), (2.4, 117.0)],
  [("whoosh", 111.3, -10), ("swoosh", 114.8, -6), ("tick-lo", 117.0, -6)]),
 ("d_gild", 140.15, 144.3, [(0.3, 140.3), (1.6, 140.78), (2.6, 142.2)],
  [("whoosh", 140.15, -10), ("shimmer", 140.78, -6), ("thump", 142.2, -4)]),
 ("d_form", 169.7, 178.2, [(0.05, 169.75), (1.0, 170.55), (2.6, 176.6)],
  [("whoosh", 169.7, -10), ("tick-lo", 170.55, -6), ("tap", 176.6, -6)]),
 ("d_thirty", 228.35, 233.4, [(0.05, 228.44), (2.05, 231.3), (2.1, 231.5)],
  [("whoosh", 228.35, -10), ("impact", 231.5, -2)]),
 ("d_hadith", 241.5, 261.9, [(0.05, 241.6)], [("flip", 241.6, -6)]),
 ("d_one", 282.55, 290.95, [(0.3, 283.6), (0.9, 284.34), (1.6, 288.9)],
  [("whoosh", 282.55, -10), ("thump", 284.34, -2), ("impact", 288.9, -2)]),
 ("d_doors", 314.0, 327.85, [(0.05, 314.1), (0.3, 318.1), (0.5, 321.4), (1.2, 323.1), (1.8, 324.2), (2.4, 325.8)],
  [("whoosh", 314.0, -10), ("tap", 318.1, -6), ("tap", 321.4, -6), ("crack", 323.1, -2), ("crackle", 324.2, -8), ("thump", 325.8, -4)]),
 ("d_kafir", 413.9, 424.05, [(0.05, 414.0), (0.5, 417.46), (1.7, 419.58)],
  [("whoosh", 413.9, -10), ("shimmer", 417.46, -6), ("tap", 419.58, 6)]),
 ("d_kahf", 463.4, 469.3, [(0.05, 463.45), (0.5, 465.0), (1.9, 465.9), (2.2, 468.44)],
  [("whoosh", 463.4, -10), ("shimmer", 468.44, -6)]),
]
# the d_thirty count clicks, and the al-Kahf numbers' taps, every one heard (FORMATS: a sound on every count)
G[4][4].extend(("click", 228.44 + (231.3 - 228.44) * (1 - (1 - (k + 1) / 12) ** 2), -10) for k in range(12))
G[9][4].extend(("tap", 465.0 + k * 0.12 * (0.9 / 1.4), -4) for k in range(10))   # -4: at -10 they only just passed the check

# re-time and render the graphics into WORK/gfx (each clip's own beats moved onto the cut)
warp = {}
for gid, a, b, at, _ in G:
    s0 = vt(a); warp[gid] = {"at": [[p, round(vt(t) - s0, 2)] for p, t in at], "d": round(vt(b) - s0 + 0.15, 2)}
os.makedirs(os.path.join(W, "gfx"), exist_ok=True)
need = [g for g, *_ in G if not os.path.exists(os.path.join(W, "gfx", g + ".mp4")) or os.environ.get("REGFX")]
if need:
    env = dict(os.environ, WARP=json.dumps(warp), OUT=os.path.join(W, "gfx"))
    print(subprocess.run([sys.executable, os.path.join(GFX, "graphics.py"), *need], env=env, capture_output=True, text=True).stdout)
panels = [[vt(a), round(min(vt(b), END), 2), "gfx", dict(src=os.path.join(W, "gfx", gid + ".mp4"), slams=[], hits=[])] for gid, a, b, _, _ in G]

# ---- the sounds, each set against his own voice's loud moments (as the hijab edit)
sys.path.insert(0, os.path.join(ROOT, "brag-quiz/reels/template")); from sfx_rules import info
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(W, "cut.wav"), "-f", "s16le", "-"], capture_output=True).stdout, np.int16) / 32768
VP = float(np.percentile(20 * np.log10(np.sqrt(np.convolve(x ** 2, np.ones(800) / 800, "valid"))[::400] + 1e-9), 90))
AUDIO = []
for *_, sounds in G:
    for name, t, db in sounds:
        f = next(os.path.join(SFX, d, name + ".wav") for d in ("soft", "ref", ".") if os.path.exists(os.path.join(SFX, d, name + ".wav")))
        pk_db, pk = info(f); AUDIO.append([f, round(max(0, vt(t) - pk), 3), round(10 ** ((VP + db - pk_db) / 20), 3)])

# ---- titles behind his head, for the lines between the graphics: (take start, take end, small, big, size)
TT = [(179.6, 186.95, "A", "MASTER LIAR", 165), (203.7, 210.85, "COVERS THE TRUTH WITH", "SOMETHING SHINY", 125),
      (308.5, 313.6, "THE", "BIGGEST LIE", 200), (359.7, 368.3, "HE PAINTS", "HELL GOLD", 230),
      (409.65, 413.85, "ALLAH LEFT US", "CLUES", 330), (425.9, 432.2, "NOT READING.", "ĪMĀN.", 330), (470.1, 476.6, "SEND THIS TO", "SOMEONE", 260)]
titles = [[vt(a), vt(b), s, bg, z] for a, b, s, bg, z in TT]

# ---- captions: the transcript's spellings fixed (the template draws cutwords as they are)
def fix(ws):
    out = []
    for i, w in enumerate(ws):
        k = re.sub(r"[^a-z0-9]", "", w[0].lower())
        if k in ("alaihi", "alayhi", "wasallam", "wa", "salam") and out and out[-1][0].startswith("ﷺ"): continue
        if k in ("sallallahu", "saw"): w[0] = "ﷺ" + w[0][-1] if w[0][-1] in ",." else "ﷺ"
        elif re.fullmatch(r"(the)?(jal|gel|jahll|dejal|dajjal|dajjals|dejals|jal)s?", k): w[0] = re.sub(r"[A-Za-z\-]+", "dajjāl" + ("s" if k.endswith("ls") else ""), w[0], 1)
        elif k == "masiha" or k == "maseeh": w[0] = "al-Masīḥ"
        elif k == "al" and i + 1 < len(ws) and "mas" in ws[i + 1][0].lower(): continue
        elif k in ("kaif", "kef", "kahf"): w[0] = "al-Kahf"
        elif k == "kafir": w[0] = "kāfir"
        elif k == "dajjala": w[0] = "Dajala,"
        elif k == "pressure": w[0] = "precious."
        elif k == "fraud" and i + 1 < len(ws) and ws[i + 1][0].lower().startswith("someone"): w[0] = "fraudster."
        elif k == "at" and i + 2 < len(ws) and re.sub(r"[^a-z]", "", ws[i + 2][0].lower()) in ("jal", "gel"): w[0] = "a"
        elif k == "the" and out and out[-1][0] == "a": continue
        out.append(w)
    return out
EM = set("liar master dajjal root cover coat tar gold cheap precious shiny thousands thirty 30 greatest paradise fire jahannam kafir faith read ten protected".split())
for c in C["caps"]:
    c[2] = fix(c[2])
    for w in c[2]: w[2] = re.sub(r"[^a-z0-9āīūḥ]", "", w[0].lower()).replace("ā", "a") in EM
C["caps"] = [c for c in C["caps"] if c[2]]
C.update(title_top=470, titles=sorted(titles), flicks=[], split=None, steps=[], panels=sorted(panels), audio=[a for a in AUDIO if 0 <= a[1] < END])
for p, q in zip(C["panels"], C["panels"][1:]): p[1] = min(p[1], q[0])
busy = [(p[0], p[1]) for p in C["panels"]] + [(t[0], t[1]) for t in titles]
em = [w for c in C["caps"] for w in c[2] if w[2] and not any(a - .4 <= w[1] < b + .4 for a, b in busy)]
C["punch"] = [[w[1], w[1] + 0.4] for w in em][:7]
cuts = sorted({0, END} | {x for a, b in busy for x in (a, b)})
C["sections"] = [[a, b] for a, b in zip(cuts, cuts[1:]) if b - a > .3]
json.dump(C, open(os.path.join(W, "config.json"), "w"), indent=1, ensure_ascii=False)
json.dump([[round(t, 3) for _, t, _ in C["audio"]]], open(os.path.join(W, "sfx-times.json"), "w"))
print("end", END, "| panels", [(p[0], p[1], os.path.basename(p[3]["src"])) for p in C["panels"]], "\n titles", titles, "\n sounds", len(C["audio"]),
      "| punches", C["punch"])
