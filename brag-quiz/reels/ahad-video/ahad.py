#!/usr/bin/env python3
"""The Aḥad videos (#315): four versions from two takes, with the template (brag-quiz/reels/template/reel.py).
  c1 = ahad1.mp4 (Drive 1ZPBbrOKcD_Hzqg1ayDYxH-3RHeYV5j36): on camera throughout; the "why aḥad, not wāḥid" part, hooks 2 and 3, the endings.
  c3 = ahad_alt_vers.mp4 (Drive 1fEHxjkvUDSFsAjpCJ3hQ2YJOH4s5IHMW): on camera until 65.83 s (hook 1, "1400 years ago", "deny Muḥammad"),
       then facing the window. Owner: never show the window footage. Those frames are blacked out when the take is joined, and full-screen
       graphics cover all of it (checked frame by frame in `config`) while his voice carries on.
Versions (owner, 5-6 Nov 2026): full (hook 1, sign-up ending), v90 (hook 2 "He was a slave…", comment ending), v60a (hook 3, the footsteps in
Jannah, told and come back to; comment ending), v60b (hook 4 "deny Muḥammad, believe in al-Lāt and al-ʿUzzā"; sign-up ending).
Each must tell the story, say he said aḥad, and what it means (tawḥīd), tied back to the story.

  python3 ahad.py VERSION WORK join     → WORK/clip.mp4 (the pieces joined), chunks.json (cuts in real silences, as dajjal-video/edit.py)
  python3 reel.py WORK base nologo; python3 reel.py WORK plan
  python3 ahad.py VERSION WORK config   → config.json: graphics (rendered into WORK/gfx), titles, sounds, captions; the window check
  python3 reel.py WORK zoom; python3 ahad.py VERSION WORK selfs; python3 reel.py WORK masks / layers / mix
"""
import json, os, re, subprocess, sys
import numpy as np
V, W, STEP = sys.argv[1:4]; os.makedirs(W, exist_ok=True)
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SRC = {"c1": "/tmp/reel-ahad/clip.mp4", "c3": "/tmp/reel-ahad3/clip.mp4"}
WIN = 65.80                                    # c3 faces the window from 65.833 s (the scene change, measured); a frame early, to be safe
BG = "0x14232a"                                # the graphics' background: what's under them where the window was

# ---- the pieces, in order: (take, from, to). Times are where words start (words.json); a word begun in a piece is kept whole.
P = {
 "full": [("c3", 0.0, 64.3),     # Under a burning rock … 1400 years ago … deny Muḥammad … one word in reply. And that word was aḥad.
          ("c3", 65.85, 89.6),   # [window] And why did Bilāl choose that word? … no room for any partnership: aḥad.
          ("c1", 69.2, 134.3),   # But why aḥad? Why not wāḥid? … al-Ikhlāṣ … it can also mean no one.
          ("c3", 137.1, 166.6),  # [window] That's the whole of tawḥīd in a single word … the very thing they were trying to make him deny.
          ("c1", 135.8, 212.1)], # Now let's go back to the story of Bilāl … the footsteps … sign up to rafiq-arabic.com.
 "v90": [("c1", 140.0, 150.1),   # He was a slave, on his back … the only word he could say was aḥad.
         ("c3", 14.6, 27.7),     # Now, let me take you back. 1400 years ago … his tyrant master Umayyah.
         ("c3", 43.4, 49.5),     # And they say to him: deny Muḥammad, believe in al-Lāt and al-ʿUzzā.
         ("c3", 51.3, 64.3),     # But this slave … Bilāl … one word in reply. And that word was aḥad.
         ("c3", 65.85, 89.6),    # [window] why aḥad … no room for any partnership: aḥad.
         ("c3", 137.1, 140.9),   # [window] That's the whole of tawḥīd in a single word.
         ("c3", 157.4, 166.6),   # [window] Bilāl wasn't just refusing their idols … make him deny.
         ("c3", 168.8, 181.9),   # [window] Next time you're reading al-Ikhlāṣ, say aḥad with as much conviction … as Bilāl did.
         ("c1", 223.3, 230.6)],  # … comment "Salah" down below and I'll send you a starter pack.
 "v60a": [("c1", 173.3, 180.7),  # The Prophet ﷺ told him: Yā Bilāl, I heard your footsteps in front of mine in Jannah.
          ("c3", 14.6, 27.7),    # Now, let me take you back …
          ("c3", 43.4, 49.5),    # deny Muḥammad …
          ("c3", 51.3, 64.3),    # … And that word was aḥad.
          ("c3", 137.1, 140.9),  # [window] That's the whole of tawḥīd in a single word.
          ("c3", 157.4, 166.6),  # [window] … the very thing they were trying to make him deny.
          ("c1", 154.7, 159.6),  # But out of everybody there, he was the only one who was free.
          ("c1", 176.1, 180.7),  # Yā Bilāl, I heard your footsteps in front of mine in Jannah.
          ("c1", 223.3, 230.6)], # comment "Salah" …
 "v60b": [("c3", 45.0, 49.5),    # Deny Muḥammad, believe in al-Lāt and al-ʿUzzā.
          ("c3", 51.3, 64.3),    # But this slave … Bilāl … And that word was aḥad.
          ("c3", 65.85, 89.6),   # [window] why aḥad … no room for any partnership: aḥad.
          ("c3", 137.1, 140.9),  # [window] tawḥīd in a single word.
          ("c3", 157.4, 166.6),  # [window] … make him deny.
          ("c1", 205.9, 212.1)], # And if you want to learn more about the words you say in your Salah, sign up to rafiq-arabic.com.
}[V]

if STEP == "join":
    os.chdir(W); os.makedirs("pieces", exist_ok=True); table, lst, o = [], [], 0.0
    for i, (src, a, b) in enumerate(P):
        s0 = max(0.0, a - 0.5); s1 = b + 0.9
        if src == "c3" and a < WIN: s1 = min(s1, WIN + 0.5)      # an on-camera piece may run a little into the window: blacked out below
        n = round((s1 - s0) * 30); d = n / 30; out = f"pieces/q{i:02d}.mp4"; lst.append(f"file '{out}'")
        w0 = WIN - s0 if src == "c3" else None                   # the window from here on, in this piece (None: never)
        black = f",drawbox=x=0:y=0:w=iw:h=ih:color={BG}:t=fill:enable='gte(t,{max(0, w0):.3f})'" if w0 is not None and w0 < d else ""
        if not os.path.exists(out):
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s0}", "-i", SRC[src], "-frames:v", str(n),
                            "-vf", f"scale=1404:2496:flags=lanczos,fps=30{black},format=yuv420p",
                            "-af", f"aresample=48000,atrim=duration={d:.6f},asetpts=PTS-STARTPTS,apad=whole_dur={d:.6f}",
                            "-c:v", "libx264", "-crf", "13", "-preset", "fast", "-c:a", "pcm_s16le", "-ac", "1", out.replace(".mp4", ".mov")], check=True)
            os.rename(out.replace(".mp4", ".mov"), out)
        table.append(dict(src=src, a=a, b=b, s0=s0, off=round(o, 4), d=d, win=(o + max(0, w0)) if black else None)); o += d
    open("pieces/list.txt", "w").write("\n".join(f"file 'q{i:02d}.mp4'" for i in range(len(P))))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "pieces/list.txt", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "clip.mp4"], check=True)
    json.dump(table, open("pieces.json", "w"), indent=1)
    # cuts in real silences, as dajjal-video/edit.py (speech over -46 dB in 10 ms steps; 0.08 s before a word, 0.20 s after; never at a word)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "clip.mp4", "-vn", "-ac", "1", "-ar", "16000", "audio.wav"], check=True)
    SP = [(t["off"] + t["a"] - t["s0"], t["off"] + t["b"] - t["s0"]) for t in table]
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", "audio.wav", "-f", "s16le", "-"], capture_output=True).stdout, np.int16) / 32768
    e = 20 * np.log10(np.sqrt(np.convolve(x ** 2, np.ones(160) / 160, "same"))[::160] + 1e-9)
    edges = [t["off"] for t in table[1:]]                     # a run never crosses a join of two pieces
    runs, cur = [], None
    for k, v in enumerate(np.append(e > -46, False)):
        if cur is not None and any(cur / 100 < j <= k / 100 for j in edges): runs.append((cur / 100, k / 100)); cur = None
        if v and cur is None: cur = k
        if not v and cur is not None:
            if runs and cur / 100 - runs[-1][1] < 0.06 and not any(runs[-1][1] <= j <= cur / 100 for j in edges): runs[-1] = (runs[-1][0], k / 100)
            else: runs.append((cur / 100, k / 100))
            cur = None
    runs = [r for r in runs if r[1] - r[0] >= 0.04]
    keep = [i for i, (s0, s1) in enumerate(runs) if any(a <= (s0 + s1) / 2 <= b or a <= s0 <= b for a, b in SP)]
    piece = lambda t: max(k for k, tb in enumerate(table) if tb["off"] <= t + 1e-6)
    groups = []
    for i in keep:
        gap = (runs[i - 1][1], runs[i][0]) if i else (0, 0)
        soft = 0 < gap[1] - gap[0] < 1.2 and (e[int(gap[0] * 100):int(gap[1] * 100)] > -52).sum() >= 8
        same = piece(runs[i][0]) == piece(runs[i - 1][0]) if i else False
        if groups and groups[-1][-1] == i - 1 and same and (gap[1] - gap[0] < 0.30 or soft): groups[-1].append(i)
        else: groups.append([i])
    chunks = []
    for g in groups:
        s0, s1 = runs[g[0]][0], runs[g[-1]][1]; k = piece(s0); lo, hi = table[k]["off"], table[k]["off"] + table[k]["d"]
        pre = runs[g[0] - 1][1] if g[0] and piece(runs[g[0] - 1][0]) == k else lo
        nxt = runs[g[-1] + 1][0] if g[-1] + 1 < len(runs) and piece(runs[g[-1] + 1][0]) == k else hi
        chunks.append((round(max(lo, s0 - min(0.08, (s0 - pre) / 2)), 3), round(min(hi, s1 + min(0.20, (nxt - s1) / 2)), 3)))
    json.dump(chunks, open("chunks.json", "w"))
    print(len(chunks), "pieces of speech,", round(sum(round((b - a) * 30) / 30 for a, b in chunks), 1), "s")
    sys.exit()

if STEP == "selfs":   # after reel.py zoom: the flicker's own clips, six moments of him on camera (the template takes fixed points of the reel,
    os.chdir(W); A = json.load(open("ahad.json"))       # which could land on the window)
    for k, t in enumerate(A["selfs"]):
        os.makedirs(f"broll/self{k}", exist_ok=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t}", "-i", "base.mov", "-t", "1", "-vf", f"{A['look'][k]},scale=960:1640:force_original_aspect_ratio=increase,crop=960:1640",
                        "-q:v", "3", f"broll/self{k}/%04d.jpg"], check=True)
    sys.exit()

# ================= config (after reel.py base + plan) =================
GFX = os.path.join(ROOT, "brag-quiz/reels/scripts-gfx"); SFX = os.path.join(ROOT, "brag-quiz/sfx")
Jf = lambda f: json.load(open(os.path.join(W, f)))
T = Jf("pieces.json"); OFF, o = [], 0.0
for a, b in Jf("chunks.json"): OFF.append((a, b, o)); o += round((b - a) * 30) / 30
def vj(t):                                     # a time in the joined clip → in the cut
    for a, b, off in OFF:
        if t < a: return round(off, 3)
        if t <= b: return round(off + t - a, 3)
    return round(o, 3)
vt = lambda i, t: vj(T[i]["off"] + t - T[i]["s0"])   # piece i's take time → the cut
C = Jf("config.json"); END = C["end"]

# graphics: gid → [(planned s in the clip, piece, take time of its word)], sounds [(name, beat, dB)]: the beat's index in the anchors
SND = {"a_word": [("shimmer", 0, -6)], "a_slam": [("impact", 0, -2), ("impact", 1, -2)], "a_scene": [("whoosh", 0, -10), ("thump", 1, -2)],
       "a_why": [("whoosh", 0, -10), ("tap", 1, -4), ("impact", 1, -4)], "a_deny": [("whoosh", 0, -10), ("impact", 1, -2), ("thump", 2, -4), ("impact", 3, -2)],
       "a_noroom": [("whoosh", 0, -10), ("crack", 1, -4), ("impact", 2, -2)], "a_tawhid": [("shimmer", 0, -6), ("impact", 1, -2)],
       "a_fear": [("whoosh", 0, -10), ("tap", 1, -4), ("impact", 2, -2)], "a_very": [("whoosh", 0, -10), ("crack", 1, -4), ("impact", 2, -2)],
       "a_say": [("flip", 0, -6), ("impact", 1, -2)], "a_count": [("whoosh", 0, -10), ("tap", 1, -4), ("tap", 2, -4), ("tap", 3, -4)],
       "a_ikhlas": [("flip", 0, -6), ("flip", 1, -6)], "a_free": [("whoosh", 0, -10), ("crack", 1, -4), ("impact", 2, -2)],
       "a_rock": [("whoosh", 0, -8), ("shimmer", 1, -6)], "a_kaba": [("whoosh", 0, -10), ("shimmer", 1, -6)], "a_jannah": [("shimmer", 0, -6), ("flip", 1, -6)]}
G = {   # (gid, piece, from, to, [(planned s, take time)])
 "full": [("a_slam", 0, 5.5, 8.9, [(0.05, 5.6), (1.0, 7.8)]),
          ("a_scene", 0, 28.2, 42.8, [(0.05, 28.3), (1.6, 40.1)]),
          ("a_word", 0, 62.0, 64.3, [(0.05, 62.0)]),
          ("a_why", 1, 65.85, 70.0, [(0.05, 65.9), (1.0, 68.5)]),
          ("a_deny", 1, 70.0, 83.0, [(0.05, 70.1), (0.8, 75.0), (1.8, 77.8), (3.2, 80.1)]),
          ("a_noroom", 1, 83.0, 90.5, [(0.05, 83.1), (1.4, 85.6), (3.0, 89.4)]),
          ("a_count", 2, 75.1, 80.8, [(0.05, 75.1), (0.6, 78.1), (1.0, 79.0), (1.4, 80.0)]),
          ("a_ikhlas", 2, 102.5, 124.0, [(0.05, 102.6), (2.0, 116.3)]),
          ("a_tawhid", 3, 137.0, 141.4, [(0.05, 136.95), (1.0, 139.1)]),
          ("a_scene", 3, 141.4, 153.2, [(0.05, 141.6), (1.6, 143.8)]),
          ("a_fear", 3, 153.2, 157.4, [(0.05, 153.4), (1.0, 155.4), (2.0, 156.5)]),
          ("a_very", 3, 157.4, 167.6, [(0.05, 157.6), (1.0, 159.6), (2.4, 162.2)]),
          ("a_free", 4, 154.7, 160.0, [(0.05, 154.7), (1.2, 156.4), (2.8, 159.1)]),
          ("a_rock", 4, 160.6, 164.1, [(0.6, 161.0), (1.4, 163.5)]),
          ("a_kaba", 4, 164.1, 172.7, [(0.05, 164.1), (0.9, 170.6)]),
          ("a_jannah", 4, 176.0, 181.2, [(0.05, 176.1), (0.3, 177.9)])],
 "v90": [("a_word", 3, 62.0, 64.3, [(0.05, 62.0)]),
         ("a_why", 4, 65.85, 70.0, [(0.05, 65.9), (1.0, 68.5)]),
         ("a_deny", 4, 70.0, 83.0, [(0.05, 70.1), (0.8, 75.0), (1.8, 77.8), (3.2, 80.1)]),
         ("a_noroom", 4, 83.0, 90.5, [(0.05, 83.1), (1.4, 85.6), (3.0, 89.4)]),
         ("a_tawhid", 5, 137.0, 141.4, [(0.05, 136.95), (1.0, 139.1)]),
         ("a_very", 6, 157.4, 167.6, [(0.05, 157.6), (1.0, 159.6), (2.4, 162.2)]),
         ("a_say", 7, 168.6, 182.6, [(0.05, 168.8), (2.0, 175.7)])],
 "v60a": [("a_jannah", 0, 177.1, 181.2, [(0.05, 177.2), (0.3, 177.9)]),
          ("a_word", 3, 62.0, 64.3, [(0.05, 62.0)]),
          ("a_tawhid", 4, 137.0, 141.4, [(0.05, 136.95), (1.0, 139.1)]),
          ("a_very", 5, 157.4, 167.6, [(0.05, 157.6), (1.0, 159.6), (2.4, 162.2)]),
          ("a_free", 6, 154.7, 160.0, [(0.05, 154.7), (1.2, 156.4), (2.8, 159.1)])],
 "v60b": [("a_word", 1, 62.0, 64.3, [(0.05, 62.0)]),
          ("a_why", 2, 65.85, 70.0, [(0.05, 65.9), (1.0, 68.5)]),
          ("a_deny", 2, 70.0, 83.0, [(0.05, 70.1), (0.8, 75.0), (1.8, 77.8), (3.2, 80.1)]),
          ("a_noroom", 2, 83.0, 90.5, [(0.05, 83.1), (1.4, 85.6), (3.0, 89.4)]),
          ("a_tawhid", 3, 137.0, 141.4, [(0.05, 136.95), (1.0, 139.1)]),
          ("a_very", 4, 157.4, 167.6, [(0.05, 157.6), (1.0, 159.6), (2.4, 162.2)])],
}[V]
# titles behind his head: (piece, from, to, small, big, size)
TT = {
 "full": [(0, 9.2, 13.8, "AN ENTIRE", "CREED", 300), (0, 16.6, 20.6, "1400 YEARS AGO", "MAKKAH", 280), (0, 21.7, 27.8, "A SLAVE FROM", "ABYSSINIA", 220),
          (0, 43.3, 49.6, "THEY SAID", "DENY MUḤAMMAD", 150), (0, 51.2, 61.0, "HIS NAME", "BILĀL", 330),
          (2, 69.1, 74.9, "WHY NOT", "WĀḤID?", 280), (2, 87.8, 97.5, "THE ONE WITH", "NO SECOND", 220), (2, 125.5, 134.5, "IT CAN ALSO MEAN", "NO ONE", 300),
          (4, 135.7, 151.0, "BACK TO", "BILĀL", 330), (4, 181.5, 196.8, "THE POWER OF", "AḤAD", 330), (4, 199.2, 205.4, "UNDERSTAND", "THE MEANING", 210),
          (4, 205.8, 212.6, "SIGN UP", "RAFIQ-ARABIC.COM", 120)],
 "v90": [(0, 147.5, 150.6, "THE ONLY WORD", "AḤAD", 330), (1, 16.6, 20.6, "1400 YEARS AGO", "MAKKAH", 280), (1, 21.7, 27.8, "A SLAVE FROM", "ABYSSINIA", 220),
         (2, 43.3, 49.6, "THEY SAID", "DENY MUḤAMMAD", 150), (3, 51.2, 61.0, "HIS NAME", "BILĀL", 330), (8, 223.2, 231.0, "COMMENT", "SALAH", 300)],
 "v60a": [(1, 16.6, 20.6, "1400 YEARS AGO", "MAKKAH", 280), (1, 21.7, 27.8, "A SLAVE FROM", "ABYSSINIA", 220), (2, 43.3, 49.6, "THEY SAID", "DENY MUḤAMMAD", 150),
          (3, 51.2, 61.0, "HIS NAME", "BILĀL", 330), (7, 176.0, 181.2, "FOOTSTEPS IN", "JANNAH", 300), (8, 223.2, 231.0, "COMMENT", "SALAH", 300)],
 "v60b": [(0, 44.9, 49.6, "THEY SAID", "DENY MUḤAMMAD", 150), (1, 51.2, 61.0, "HIS NAME", "BILĀL", 330), (5, 205.8, 212.6, "SIGN UP", "RAFIQ-ARABIC.COM", 120)],
}[V]
HOOK = {"full": "ONE WORD", "v90": "A SLAVE", "v60a": "YĀ BILĀL", "v60b": "DENY MUḤAMMAD"}[V]

# the graphics, re-timed onto his words and rendered into WORK/gfx (one clip per use: the same graphic can land on different words)
warp, panels, beats = {}, [], []
for n, (gid, i, a, b, at) in enumerate(G):
    s0, s1 = vt(i, a), vt(i, b); key = f"{gid}-{n}"
    warp[key] = {"at": [[p, round(vt(i, t) - s0, 2)] for p, t in at], "d": round(s1 - s0 + 0.3, 2)}
    panels.append([s0, s1, "gfx", dict(src=os.path.join(W, "gfx", key + ".mp4"), slams=[], hits=[])])
    beats.append((gid, [s0 + q for _, q in warp[key]["at"]]))
os.makedirs(os.path.join(W, "gfx"), exist_ok=True)
need = [k for k in warp if not os.path.exists(os.path.join(W, "gfx", k + ".mp4")) or os.environ.get("REGFX")]
if need:   # graphics.py renders by graphic id: render each use under its own name from a copy of the graphic's id
    for k in need:
        gid = k.rsplit("-", 1)[0]
        env = dict(os.environ, WARP=json.dumps({gid: warp[k]}), OUT=os.path.join(W, "gfx"))
        r = subprocess.run([sys.executable, os.path.join(GFX, "graphics.py"), gid], env=env, capture_output=True, text=True); print(r.stdout.strip(), r.stderr[-300:])
        os.replace(os.path.join(W, "gfx", gid + ".mp4"), os.path.join(W, "gfx", k + ".mp4"))

# the window: where it is in the cut, and the graphics run back to back over all of it (hard cuts between them, sliding in before, out after)
win = []
for tb in T:
    if tb["win"] is None: continue
    w0, w1 = tb["win"], tb["off"] + tb["d"]
    for a, b, off in OFF:
        if b > w0 and a < w1: win.append((round(off + max(a, w0) - a, 3), round(off + min(b, w1) - a, 3)))
panels.sort()
for p, q in zip(panels, panels[1:]):           # graphics less than 0.7 s apart: one runs into the next, a hard cut
    if q[0] - p[1] < 0.7: p[1] = q[0]; p[3]["cutout"] = True; q[3]["cutin"] = True
for w0, w1 in win:                             # stretch the graphics over each window stretch, with room for the slides
    inside = [p for p in panels if p[1] > w0 - 0.4 and p[0] < w1 + 0.4]
    assert inside, f"no graphic over the window at {w0}-{w1}"
    first, last = inside[0], inside[-1]
    if not first[3].get("cutin"): first[0] = min(first[0], round(w0 - 0.32, 3))
    if not last[3].get("cutout"): last[1] = max(last[1], round(w1 + 0.27, 3))
for p, q in zip(panels, panels[1:]):
    if q[0] < p[1]: p[1] = q[0]
    if q[0] - p[1] < 0.7: p[1] = q[0]; p[3]["cutout"] = True; q[3]["cutin"] = True
def covered(t):                                # fully covered at t: inside a panel, past its slide in and before its slide out
    for p0, p1, _, o in panels:
        if p0 <= t < p1 and (o.get("cutin") or t >= p0 + 0.3) and (o.get("cutout") or t < p1 - 0.25): return True
    return False
bad = [round(f / 30, 2) for w0, w1 in win for f in range(int(w0 * 30), int(np.ceil(w1 * 30)) + 1) if not covered(f / 30)]
assert not bad, f"window frames not covered: {bad[:10]}"
print("window in the cut:", win, "→ covered by", [(p[0], p[1]) for p in panels if any(p[1] > a and p[0] < b for a, b in win)])

# sounds, each set against his own voice (as dajjal-video/config.py)
sys.path.insert(0, os.path.join(ROOT, "brag-quiz/reels/template")); from sfx_rules import info
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(W, "cut.wav"), "-f", "s16le", "-"], capture_output=True).stdout, np.int16) / 32768
VP = float(np.percentile(20 * np.log10(np.sqrt(np.convolve(x ** 2, np.ones(800) / 800, "valid"))[::400] + 1e-9), 90))
AUDIO = []
for gid, bt in beats:
    for name, k, db in SND[gid]:
        if k >= len(bt): continue
        f = next(os.path.join(SFX, d, name + ".wav") for d in ("soft", "ref", ".") if os.path.exists(os.path.join(SFX, d, name + ".wav")))
        pk_db, pk = info(f); AUDIO.append([f, round(max(0, bt[k] - pk), 3), round(10 ** ((VP + db - pk_db) / 20), 3)])

titles = []
for i, a, b, sm, bg, z in TT:                  # a title never sits under a graphic: dropped if it starts in one, cut short before the next
    t0, t1 = vt(i, a), vt(i, b)
    if any(p[0] - 0.3 <= t0 < p[1] for p in panels): continue
    titles.append([t0, round(min([t1] + [p[0] for p in panels if p[0] > t0]), 3), sm, bg, z])
titles = sorted(titles)

def fix(ws):   # captions: the transcript's spellings
    out = []
    for i, w in enumerate(ws):
        k = re.sub(r"[^a-z0-9]", "", w[0].lower()); p = re.match(r"^\W*", w[0]).group(); s = re.search(r"\W*$", w[0]).group()
        if k in ("alaihi", "alayhi", "wasallam", "wa", "salam") and out and out[-1][0].startswith("ﷺ"): continue
        if k in ("sallallahu", "sallallahualaihiwasallam"): w[0] = "ﷺ" + s; out.append(w); continue
        rep = {"ahad": "aḥad", "wahid": "wāḥid", "tawhid": "tawḥīd", "tohid": "tawḥīd", "tawheed": "tawḥīd", "umayyya": "Umayyah", "umayyad": "Umayyah",
               "umayya": "Umayyah", "uzzah": "al-ʿUzzā", "uzza": "al-ʿUzzā", "iqlas": "al-Ikhlāṣ", "ikhlas": "al-Ikhlāṣ", "adan": "adhān", "aban": "adhān",
               "rafeeqarabic": "rafiq-arabic", "bilal": "Bilāl", "brought": "bought" if i + 1 < len(ws) and ws[i + 1][0].lower().startswith("him") else None,
               "khulhu": "Qul", "makkah": "Makkah", "jannah": "Jannah", "salah": "Salah"}.get(k)
        if k == "la" and i + 1 < len(ws) and ws[i + 1][0].startswith("'"): w[0] = p + "al-Lāt"; out.append(w); continue
        if k == "at" and out and out[-1][0].endswith("al-Lāt"): continue
        if k == "com" and out and out[-1][0].startswith("rafiq-arabic"): out[-1][0] += ".com" + s; continue
        if k == "ka" and i + 1 < len(ws) and "aba" in ws[i + 1][0]: w[0] = "Kaʿbah"; out.append(w); continue
        if k == "aba" and out and out[-1][0] == "Kaʿbah": continue
        if rep: w[0] = p + rep + s
        out.append(w)
    return out
EM = set("aḥad one word creed slave burning boulder rock deny bilāl free freedom tawḥīd partner partners partnership idols wāḥid second no conviction fear jannah footsteps power salah".split())
for c in C["caps"]:
    c[2] = fix(c[2])
    for w in c[2]: w[2] = re.sub(r"[^\wāīūḥ]", "", w[0].lower()) in EM
C["caps"] = [c for c in C["caps"] if c[2]]
C.update(title_top=470, titles=titles, flicks=[[0, 2.4, HOOK, 150 if len(HOOK) > 9 else 220]], split=None, steps=[], panels=panels,
         audio=[a for a in AUDIO if 0 <= a[1] < END])
busy = [(p[0], p[1]) for p in panels] + [(t[0], t[1]) for t in titles] + [(0, 2.4)]
em = [w for c in C["caps"] for w in c[2] if w[2] and not any(a - .4 <= w[1] < b + .4 for a, b in busy)]
C["punch"] = [[w[1], w[1] + 0.4] for w in em][::max(1, len(em) // 7)][:7]
cuts = sorted({0, END} | {x for a, b in busy for x in (a, b)})
C["sections"] = [[a, b] for a, b in zip(cuts, cuts[1:]) if b - a > .3]
# the flicker's own clips: six moments of him on camera (never the window: the template would take them at fixed points of the reel)
onc = [(a, b) for a, b in zip(cuts, cuts[1:]) if b - a > 1.5 and not any(b > p[0] and a < p[1] for p in panels)]
LOOK = ["crop=iw*.5:ih*.5:iw*.25:ih*.22", "hue=s=0,eq=contrast=1.35:brightness=-.03", "crop=iw*.7:ih*.7:iw*.15:ih*.12",
        "hue=s=0,crop=iw*.42:ih*.42:iw*.29:ih*.24", "crop=iw*.85:ih*.85:iw*.075:ih*.05", "hue=s=0,crop=iw*.6:ih*.6:iw*.2:ih*.15"]
json.dump(C, open(os.path.join(W, "config.json"), "w"), indent=1, ensure_ascii=False)
json.dump({"win": win, "selfs": [round(onc[int(k * len(onc) / 6)][0] + 0.3, 2) for k in range(6)], "look": LOOK}, open(os.path.join(W, "ahad.json"), "w"))
print("end", END, "| panels", [(p[0], p[1], os.path.basename(p[3]["src"]), "cut in" if p[3].get("cutin") else "", "cut out" if p[3].get("cutout") else "") for p in panels],
      "\n titles", titles, "\n sounds", len(C["audio"]), "| punches", C["punch"])
