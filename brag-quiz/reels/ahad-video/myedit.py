#!/usr/bin/env python3
"""The Aḥad video from the owner's own edit (#315, 7 Nov 2026): myedit_ahad.mp4 in RAW (Drive 1bTyNgEkU0TozywZQ0tHX7PSDvRAQwy9q), his
cut kept exactly as it is (nothing shortened, no silences cut), with:
  - "14,000 years ago" swapped for "1400 years ago" from his other take (ahad_alt_vers.mp4, 14.37-17.97 s), done when WORK/clip.mp4 was made;
  - the window footage (65.90-97.10 s and 106.73-119.13 s) never shown: full-screen graphics over all of it, checked frame by frame;
  - no flicker at the start;
  - the camera: slow, smooth pushes centred on his face, a step deeper on each big word (eased over 0.9 s, never a jerk), a long
    slow pull back when it gets too close, and any reset only while a graphic covers him (owner: "a smooth zoom into me as centre");
  - sound: impacts and booms on the big words, echoes on them, and on the opening "aḥad, aḥad" a slowed, deeper copy with bass
    and a long reverb under his voice, over a low hum (owner: "impacts on emphasis, echoes, slow reverb").

  python3 reel.py WORK base nologo; python3 reel.py WORK plan      (chunks.json: the whole clip, one piece)
  python3 myedit.py WORK config        → config.json, gfx/, fx/ (the voice layers)
  python3 myedit.py WORK zoom          → base.mov (instead of reel.py zoom)
  python3 reel.py WORK masks; python3 reel.py WORK layers; python3 reel.py WORK mix
"""
import json, os, re, subprocess, sys
import numpy as np
W, STEP = sys.argv[1:3]; HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
GFX = os.path.join(ROOT, "brag-quiz/reels/scripts-gfx"); SFX = os.path.join(ROOT, "brag-quiz/sfx")
Jf = lambda f: json.load(open(os.path.join(W, f)))
sh = lambda *a: subprocess.run(list(a), check=True)
WIN = Jf("win.json")                                 # the window frames, measured by colour (blue wall vs the brown room)
C = Jf("config.json"); END = C["end"]

# his words: where each really starts (speech over -40 dB, from a little before the transcript's time)
x16 = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(W, "cut.wav"), "-f", "s16le", "-"], capture_output=True).stdout, np.int16) / 32768
ENV = 20 * np.log10(np.sqrt(np.convolve(x16 ** 2, np.ones(160) / 160, "same"))[::160] + 1e-9)
def on(t):                                     # the quietest moment just before the transcript's time, then the first sound after it
    a0 = int(max(0, t - 0.35) * 100); k = a0 + int(np.argmin(ENV[a0:int((t + 0.15) * 100)]))
    while k < min(len(ENV) - 1, int((t + 0.25) * 100)) and ENV[k] < -40: k += 1
    return round(k / 100, 2)

# ---- graphics: (gid, from, to, [(planned s, word time)]); the ones over the window run back to back
G = [("a_scene", 30.7, 37.9, [(0.05, 30.8), (1.6, 34.5)]),
     ("a_deny", 65.6, 77.6, [(0.05, 66.2), (0.8, 70.24), (1.8, 73.06), (3.2, 75.34)]),
     ("a_noroom", 77.6, 87.0, [(0.05, 78.44), (1.4, 80.86), (3.0, 84.55)]),
     ("a_none", 87.0, 91.5, [(0.05, 87.12), (0.9, 89.3), (1.6, 90.2), (2.3, 91.1)]),
     ("a_alone", 91.5, 97.5, [(0.05, 91.6), (0.8, 93.94), (2.0, 96.26)]),
     ("a_qul", 99.9, 106.6, [(0.05, 100.0), (0.8, 100.42)]),
     ("a_tawhid", 106.6, 110.6, [(0.05, 106.86), (1.0, 108.5)]),
     ("a_very", 110.6, 119.5, [(0.05, 110.74), (1.0, 111.72), (2.4, 114.28)]),
     ("a_kaba", 122.4, 126.9, [(0.05, 122.48), (0.9, 124.84)]),
     ("a_jannah", 130.6, 135.0, [(0.05, 130.72), (0.3, 131.54)])]
SND = {"a_scene": [("whoosh", 0, -8), ("thump", 1, 0)], "a_deny": [("whoosh", 0, -8), ("impact", 1, 0), ("thump", 2, -2), ("impact", 3, 0)],
       "a_noroom": [("whoosh", 0, -8), ("crack", 1, -2), ("boom", 2, -1)], "a_none": [("impact", 1, -2), ("impact", 2, -2), ("boom", 3, -1)],
       "a_alone": [("shimmer", 0, -6), ("impact", 2, 0)], "a_qul": [("flip", 1, -4)], "a_tawhid": [("shimmer", 0, -6), ("boom", 1, 0)],
       "a_very": [("crack", 1, -2), ("impact", 2, 0)], "a_kaba": [("whoosh", 0, -8), ("shimmer", 1, -4)], "a_jannah": [("shimmer", 0, -4), ("whoosh", 1, -8)]}
# titles behind his head
TT = [(3.5, 6.6, "ONLY", "ONE WORD", 230), (6.6, 8.85, "", "AḤAD", 380), (11.0, 15.6, "1400 YEARS AGO", "MAKKAH", 280), (16.1, 22.4, "A SLAVE FROM", "ABYSSINIA", 220),
      (38.0, 44.6, "THEY SAID", "DENY MUḤAMMAD", 150), (45.8, 56.6, "HIS NAME", "BILĀL", 330), (56.7, 60.4, "ONE WORD", "AḤAD", 380),
      (60.5, 65.5, "WHY NOT", "WĀḤID?", 280), (127.0, 130.5, "", "YĀ BILĀL", 300), (135.2, 146.4, "THE POWER OF", "AḤAD", 380), (150.4, END, "COMMENT", "SALAH", 300)]
# the big words: (word time, impact sounds [(name, dB)], voice layer: deep / echo / reverb / None, zoom step)
BIG = [(1.12, [("thump", -2)], None, 0.03), (3.66, [("thump", -4)], None, 0.035),
       (6.70, [("boom", 0), ("impact", 0)], "deep", 0.12), (8.13, [("boom", 2), ("impact", 2)], "deep", 0.12),   # (measured: the transcript has them ~1 s early)
       (11.14, [("impact", -2)], None, 0.06), (16.82, [("thump", -2)], None, 0.06), (29.58, [("thump", -4)], None, 0.05),
       (39.90, [("impact", 0)], "echo", 0.1), (50.82, [("impact", -1)], "echo", 0.1), (54.70, [("thump", -4)], None, 0.05),
       (58.48, [("boom", 0), ("impact", 0)], "echo", 0.1), (59.58, [("impact", 1)], "echo", 0.08), (61.00, [("thump", -3)], None, 0.06),
       (62.78, [("thump", -3)], None, 0.06), (84.55, [], "echo", 0), (108.5, [], "echo", 0), (118.58, [("impact", -1)], "echo", 0),
       (129.86, [("impact", 0)], "echo", 0.1), (134.16, [], "reverb", 0), (135.9, [("boom", -1), ("impact", -2)], "echo", 0.1),
       (137.22, [("thump", -3)], None, 0.05), (143.74, [("thump", -4)], None, 0), (145.66, [("boom", 0), ("impact", 0)], "reverb", 0.12),
       (150.64, [("impact", -2)], None, 0.08)]

if STEP == "config":
    # graphics, re-timed onto his words, one clip per use
    warp, panels, beats = {}, [], []
    for n, (gid, a, b, at) in enumerate(G):
        key = f"{gid}-{n}"; at = [(p, on(t)) for p, t in at]
        warp[key] = {"at": [[p, round(t - a, 2)] for p, t in at], "d": round(b - a + 0.4, 2)}
        panels.append([a, b, "gfx", dict(src=os.path.join(W, "gfx", key + ".mp4"), slams=[], hits=[])]); beats.append((gid, [t for _, t in at]))
    os.makedirs(os.path.join(W, "gfx"), exist_ok=True)
    for k in warp:
        if os.path.exists(os.path.join(W, "gfx", k + ".mp4")) and not os.environ.get("REGFX"): continue
        gid = k.rsplit("-", 1)[0]
        r = subprocess.run([sys.executable, os.path.join(GFX, "graphics.py"), gid], env=dict(os.environ, WARP=json.dumps({gid: warp[k]}), OUT=os.path.join(W, "gfx")),
                           capture_output=True, text=True); print(r.stdout.strip(), r.stderr[-300:])
        os.replace(os.path.join(W, "gfx", gid + ".mp4"), os.path.join(W, "gfx", k + ".mp4"))
    # the window covered: graphics back to back over it (hard cuts), sliding in before it and out after it
    panels.sort()
    for p, q in zip(panels, panels[1:]):
        if q[0] - p[1] < 0.7: p[1] = q[0]; p[3]["cutout"] = True; q[3]["cutin"] = True
    for w0, w1 in WIN:
        inside = [p for p in panels if p[1] > w0 - 0.4 and p[0] < w1 + 0.4]; assert inside, (w0, w1)
        if not inside[0][3].get("cutin"): inside[0][0] = min(inside[0][0], round(w0 - 0.35, 3))
        if not inside[-1][3].get("cutout"): inside[-1][1] = max(inside[-1][1], round(w1 + 0.32, 3))
    for p, q in zip(panels, panels[1:]):
        if q[0] < p[1]: p[1] = q[0]
        if q[0] - p[1] < 0.7: p[1] = q[0]; p[3]["cutout"] = True; q[3]["cutin"] = True
    def covered(t):
        return any(p0 <= t < p1 and (o.get("cutin") or t >= p0 + 0.3) and (o.get("cutout") or t < p1 - 0.25) for p0, p1, _, o in panels)
    bad = [round(f / 30, 2) for w0, w1 in WIN for f in range(int(w0 * 30), int(np.ceil(w1 * 30)) + 1) if not covered(f / 30)]
    assert not bad, f"window frames not covered: {bad[:10]}"
    print("window", WIN, "covered by", [(p[0], p[1], os.path.basename(p[3]["src"])) for p in panels])

    # the voice layers: the word copied, treated, and laid under his own (at his voice's level after the mix's gain)
    os.makedirs(os.path.join(W, "fx"), exist_ok=True)
    if not os.path.exists(os.path.join(W, "fx", "voice48.wav")):
        sh("ffmpeg", "-v", "error", "-y", "-i", os.path.join(W, "cut.mov"), "-vn", "-ac", "1", "-ar", "48000", os.path.join(W, "fx", "voice48.wav"))
    CLEAN = "highpass=f=80,lowpass=f=13000,afftdn=nr=18:nf=-66:tn=1,agate=threshold=0.003:ratio=2.5:range=0.15:attack=6:release=220,acompressor=threshold=-28dB:ratio=2:attack=12:release=220"
    m = subprocess.run(["ffmpeg", "-i", os.path.join(W, "fx", "voice48.wav"), "-af", CLEAN + ",ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    GAIN = -14.5 - float(re.findall(r"I:\s+(-?[\d.]+) LUFS", m)[-1])             # what reel.py mix gives his voice
    FX = {"deep": ("asetrate=48000*0.78,aresample=48000,bass=g=9:f=110,lowpass=f=5000,"
                   "aecho=0.8:0.88:70|140|260|420|650:0.55|0.45|0.35|0.25|0.18,afade=t=out:st=1.6:d=1.4", 4, 3.2, 0.0),
          "echo": ("asplit=3[a][b][c];[a]adelay=230,volume=0.42[a2];[b]adelay=460,volume=0.24[b2];[c]adelay=690,volume=0.12[c2];"
                   "[a2][b2][c2]amix=inputs=3:normalize=0,highpass=f=220,lowpass=f=6500,aecho=0.8:0.6:60|110:0.3|0.2", 7, 1.8, 0.0),
          "reverb": ("asetrate=48000*0.9,aresample=48000,bass=g=5:f=120,aecho=0.8:0.9:40|73|110|170|260|400|560:0.5|0.45|0.4|0.35|0.3|0.25|0.18,"
                     "lowpass=f=5000,afade=t=out:st=1.4:d=1.6", 2, 3.0, 0.0)}
    AUDIO = []
    for t, _, kind, _ in BIG:
        if not kind: continue
        s = on(t); f = os.path.join(W, "fx", f"{kind}-{s:.2f}.wav"); chain, db, dur, _ = FX[kind]
        e = next((w["e"] for w in Jf("cutwords.json") if abs(w["s"] - t) < 0.3), s + 0.6)          # the word alone, not the next one
        n = max(0.35, e - s + 0.12)
        sh("ffmpeg", "-v", "error", "-y", "-ss", f"{s - 0.03}", "-t", f"{n}", "-i", os.path.join(W, "fx", "voice48.wav"), "-filter_complex",
           f"[0:a]{CLEAN},afade=t=out:st={n - 0.06:.3f}:d=0.06,apad=pad_dur={dur},{chain}", "-ar", "48000", "-ac", "1", f)
        AUDIO.append([f, round(s - 0.03, 3), round(10 ** ((GAIN + db) / 20), 3)])
    # the sounds: impacts on the big words, each graphic's beats, a low hum under the opening
    sys.path.insert(0, os.path.join(ROOT, "brag-quiz/reels/template")); from sfx_rules import info
    VP = float(np.percentile(20 * np.log10(np.sqrt(np.convolve(x16 ** 2, np.ones(800) / 800, "valid"))[::400] + 1e-9), 90))
    def snd(name, t, db):
        f = next(p for p in (os.path.join(SFX, d, name + ".wav") for d in ("soft", "ref", ".")) if os.path.exists(p))
        db -= 3 if name == "boom" else 0                                      # the booms a touch under the impacts
        pk_db, pk = info(f); AUDIO.append([f, round(max(0, t - pk), 3), round(10 ** ((VP + db - pk_db) / 20) * 10 ** (GAIN / 20), 3)])
    for t, hits, _, _ in BIG:
        for name, db in hits: snd(name, on(t), db)
    for gid, bt in beats:
        for name, k, db in SND[gid]:
            if k < len(bt): snd(name, bt[k], db)
    hum = os.path.join(W, "fx", "hum.wav")
    sh("ffmpeg", "-v", "error", "-y", "-stream_loop", "3", "-i", os.path.join(SFX, "soft", "darkhum.wav"), "-t", "9.5", "-af",
       "afade=t=in:d=1.2,afade=t=out:st=7.6:d=1.9,aresample=48000", "-ac", "1", hum)
    AUDIO.append([hum, 0.0, round(10 ** ((VP - 14 - info(hum)[0]) / 20) * 10 ** (GAIN / 20), 3)])

    titles = []
    for a, b, sm, bg, z in TT:                 # never under a graphic
        if any(p[0] - 0.3 <= a < p[1] for p in panels): continue
        titles.append([a, round(min([b] + [p[0] for p in panels if p[0] > a]), 3), sm, bg, z])

    def fix(ws):
        out = []
        for i, w in enumerate(ws):
            k = re.sub(r"[^a-z0-9]", "", w[0].lower()); p = re.match(r"^\W*", w[0]).group(); s = re.search(r"\W*$", w[0]).group()
            if k in ("alaihi", "alayhi", "wasallam", "wa", "salam") and out and out[-1][0].startswith("ﷺ"): continue
            if k in ("sallallahu",): w[0] = "ﷺ" + s; out.append(w); continue
            rep = {"ahad": "aḥad", "wahid": "wāḥid", "tawheed": "tawḥīd", "umeya": "Umayyah", "umayyya": "Umayyah", "uzzah": "al-ʿUzzā", "laat": "al-Lāt",
                   "ikhlas": "al-Ikhlāṣ", "adhan": "adhān", "kaaba": "Kaʿbah", "bilal": "Bilāl", "qulhu": "Qul huwa", "radeelahu": "raḍiya Allāhu", "anh": "ʿanhu",
                   "jannah": "Jannah"}.get(k)
            if k == "la" and i + 1 < len(ws) and ws[i + 1][0].startswith("'"): w[0] = p + "al-Lāt"; out.append(w); continue
            if k == "at" and out and out[-1][0].endswith("al-Lāt"): continue
            if rep: w[0] = p + rep + s
            out.append(w)
        return out
    BIGT = [round(on(t), 1) for t, *_ in BIG]
    for c in C["caps"]:
        c[2] = fix(c[2])
        for w in c[2]: w[2] = any(abs(w[1] - t) < 0.25 for t in BIGT)      # the gold pop only on the big words
    C["caps"] = [c for c in C["caps"] if c[2]]
    for c in C["caps"]:                          # the opening "aḥad, aḥad": the transcript has them ~1 s early
        for w in c[2]:
            if 5.5 < w[1] < 6.0: w[1] = 6.70
            elif 7.6 < w[1] < 7.9: w[1] = 8.13
        if 5.5 < c[0] < 6.0: c[0] = 6.68
        elif 7.6 < c[0] < 7.9: c[0] = 8.11
    C.update(title_top=470, titles=titles, flicks=[], split=None, steps=[], punch=[], panels=panels, audio=[a for a in AUDIO if 0 <= a[1] < END])
    cuts = sorted({0, END} | {v for p in panels for v in p[:2]} | {v for t in titles for v in t[:2]})
    C["sections"] = [[a, b] for a, b in zip(cuts, cuts[1:]) if b - a > .3]
    json.dump(C, open(os.path.join(W, "config.json"), "w"), indent=1, ensure_ascii=False)
    print("titles", [(t[0], t[1], t[3]) for t in titles], "\nsounds", len(AUDIO), "gain", round(GAIN, 1))

elif STEP == "zoom":    # the camera: smooth, centred on his face, deeper on each big word, resets only under a graphic
    P = C["panels"]
    def hidden(t): return any(p0 + 0.32 <= t < p1 - 0.27 for p0, p1, *_ in P)
    K = [(0.0, 1.0)]; z = 1.0; last = 0.0
    events = sorted([(on(t), step) for t, _, _, step in BIG if step > 0])
    for p0, p1, *_ in P:                       # a reset to 1.0 halfway through each graphic (when it fully covers him),
        events.append((round((p0 + p1) / 2, 2), "reset"))      # and a gentle push in as the camera comes back to him
        if p1 < END - 1 and not any(q[0] <= p1 + 0.1 < q[1] for q in P): events.append((round(p1 + 0.1, 2), 0.035))
    for t, step in sorted(events, key=lambda e: e[0]):
        if step == "reset":
            if not hidden(t) or z == 1.0: continue
            K += [(t, z), (t + 1 / 30, 1.0)]; z = 1.0; last = t; continue
        if hidden(t): continue
        t0 = max(t - 0.2, K[-1][0] + 0.05)
        z0 = min(z + 0.012 * (t0 - K[-1][0]), z + 0.04)                     # a slow drift in between
        if z0 + step * 1.4 > 1.56:                                            # too close: a long, slow pull back in the quiet before the word
            if t0 - K[-1][0] < 1.9: continue                                 # (no room: hold, never pull back on the word itself)
            K += [(t0 - 1.7, round(z0, 3)), (t0 - 0.1, 1.08)]; z0 = 1.08
        z1 = z0 + step * 1.4                                                 # more dramatic: each big word a clear step in, eased over 0.9 s
        K += [(t0, round(z0, 3)), (t0 + 0.9, round(z1, 3))]; z = z1
    K.append((END, min(z + 0.012 * (END - K[-1][0]), z + 0.06)))
    K = [k for i, k in enumerate(K) if i == 0 or k[0] > K[i - 1][0]]
    sm = lambda u: f"({u})*({u})*(3-2*({u}))"
    Z = f"{K[0][1]}" + "".join(f"+{b[1] - a[1]:.4f}*{sm(f'clip((t-{a[0]:.3f})/{max(b[0] - a[0], 1 / 60):.3f},0,1)')}" for a, b in zip(K, K[1:]) if b[1] != a[1])
    # centred on his face, frame by frame (owner, 7 Nov: "keep me centred as you zoom"; anchoring one fixed point let him drift to the
    # edge): his face found every 3rd frame (OpenCV), wrong finds dropped, the track smoothed over 1.5 s so the camera follows gently
    import cv2
    fp = os.path.join(W, "faces.json")
    SW, SH = map(int, subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height", "-of", "csv=p=0",
                                      os.path.join(W, "cut.mov")], capture_output=True, text=True).stdout.strip().split(","))
    if not os.path.exists(fp):
        w, h = SW // 4, SH // 4; out = []
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", os.path.join(W, "cut.mov"), "-vf", f"select='not(mod(n\\,3))',scale={w}:{h}", "-vsync", "0",
                              "-f", "rawvideo", "-pix_fmt", "gray", "-"], stdout=subprocess.PIPE)
        cas = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml"); i = 0
        while len(b := p.stdout.read(w * h)) == w * h:
            fs = cas.detectMultiScale(np.frombuffer(b, np.uint8).reshape(h, w), 1.1, 5, minSize=(30, 30))
            if len(fs): x, y, fw, fh = max(fs, key=lambda r: r[2] * r[3]); out.append([i * 3, (x + fw / 2) / w, (y + fh / 2) / h])
            i += 1
        json.dump(out, open(fp, "w"))
    F = np.array(json.load(open(fp))); my = np.median(F[:, 2])
    F = F[(abs(F[:, 2] - my) < 0.06) & (abs(F[:, 1] - np.median(F[:, 1])) < 0.12)]          # his face, not his hands or the wall
    N = round(END * 30); fr = np.arange(N)
    fx, fy = np.interp(fr, F[:, 0], F[:, 1]), np.interp(fr, F[:, 0], F[:, 2])
    ker = np.ones(45) / 45; pad = lambda a: np.pad(a, 22, mode="edge")
    fx, fy = np.convolve(pad(fx), ker, "valid")[:N], np.convolve(pad(fy), ker, "valid")[:N]
    TY = 0.36                                   # where his face sits on screen, from the top
    def zat(t):
        z = K[0][1]
        for a, b in zip(K, K[1:]):
            u = min(1, max(0, (t - a[0]) / max(b[0] - a[0], 1 / 60))); z += (b[1] - a[1]) * u * u * (3 - 2 * u)
        return z
    open(os.path.join(W, "zoom.txt"), "w").write(json.dumps(K))
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", os.path.join(W, "cut.mov"), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1080x1920", "-r", "30", "-i", "-",
                            "-i", os.path.join(W, "cut.mov"), "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "15", "-preset", "medium",
                            "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", "-shortest", os.path.join(W, "base.mov")], stdin=subprocess.PIPE)
    off = []
    for n in range(N):
        b = dec.stdout.read(SW * SH * 3)
        if len(b) < SW * SH * 3: break
        z = zat(n / 30); cw, ch = SW / z, SH / z
        x0 = min(max(fx[n] * SW - cw / 2, 0), SW - cw); y0 = min(max(fy[n] * SH - TY * ch, 0), SH - ch)
        M = np.float32([[1080 / cw, 0, -x0 * 1080 / cw], [0, 1920 / ch, -y0 * 1920 / ch]])
        img = cv2.warpAffine(np.frombuffer(b, np.uint8).reshape(SH, SW, 3), M, (1080, 1920), flags=cv2.INTER_LANCZOS4 if z > 1.001 else cv2.INTER_AREA)
        enc.stdin.write(img.tobytes()); off.append(round((fx[n] * SW - x0) / cw, 3))
    enc.stdin.close(); enc.wait(); dec.stdout.close()
    print(len(K), "zoom keys, max", max(k[1] for k in K), "| his face across the screen: from", min(off), "to", max(off), "(0.5 = centre)")
