#!/usr/bin/env python3
"""h1-algebra in a new format (owner, 27 Oct 2026, #298: "more graphics, simpler script but more detailed… rather than just text, dynamic
graphics showing what's being described"). The story of #296 told with full-screen animated drawings on the series' pastel page, each move
on its word, short captions underneath:
  1 "…setting broken bones": an arm bone cracks · 2 الْجَبْر (Rafiq) "putting broken pieces back together": the halves slide back, the break
  glows gold, a bandage wraps it · 3 "twelve hundred years ago, in Baghdad, al-Khwārizmī wrote a book": the round city on the Tigris, the
  years counting, his book opening · 4-6 his own example drawn: a square x², ten of its sides (a 10-by-x strip) = 39; the strip splits into
  two fives on two sides; the missing corner 5 × 5 = 25 fills in; 39 + 25 = 64, its side 8, take away 5: x = 3 · 7 "al-jabr became algebra…
  a bone-setter… an algebrista": the Arabic word turns into the Latin, a bone-setter's sign swings · 8 "his name… algorithm": the name morphs
  · 9 your turn: وَاجْبُرْنِي on a prayer mat, three answers, 3-2-1 · 10 "and mend me": a cracked bowl mended with gold · 11 the ask.
Sources as #296 (al-jabr "reunion of broken parts", bone-setting: Wiktionary, American Heritage; x² + 10x = 39 is al-Khwārizmī's own
example, solved by completing the square; algebrista "bone-setter": Wiktionary; the duʿāʾ: al-Tirmidhī 284).

  python3 brag-quiz/reels/algebra/build.py    then  cd brag-quiz/reels/algebra/out/v && npx hyperframes render -o ../algebra-raw.mp4
"""
import json, os, re, shutil, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
V6 = os.path.join(ROOT, "brag-output-v6/composition/assets"); VO = os.path.join(ROOT, "brag-quiz/voice/algebra")
INK, CREAM, GOLD, RED, TEAL, BLUE, BONE = "#17262B", "#F6EFE2", "#E9B949", "#B4322A", "#2E7263", "#7FA7C9", "#FBF4E4"
dur = lambda f: float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))
mp3 = lambda n: os.path.join(VO, n + ".mp3")
def words(n):                                                             # [word, start, end]; the older lines (#296) have no ends
    ws = json.load(open(os.path.join(VO, n + ".words.json")))
    return [(w[0], w[1], w[2] if len(w) > 2 else (ws[i + 1][1] if i + 1 < len(ws) else w[1] + 0.45)) for i, w in enumerate(ws)]
ORDER = [("h1c", 0.3), ("jabr", 0.3), ("g2", 0.25), ("g3", 0.35), ("g4", 0.35), ("g5", 0.3), ("g6", 0.3), ("g7", 0.4), ("g8", 0.3),
         ("t1s", 0.4), ("wajburni", 0.25), ("t1b", 0.25), ("b6", 3.5), ("end", 0.5)]               # b6 waits for the 3-2-1
def spoken(n):                                                            # where the speech in a recording ends (ElevenLabs pads ~0.3 s)
    import numpy as np
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", mp3(n), "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout, np.int16) / 32768
    e = 20 * np.log10(np.sqrt(np.convolve(x ** 2, np.ones(160) / 160, "same")) + 1e-9)
    return np.where(e > -45)[0][-1] / 16000 + 0.05
L, t = {}, 0.0
for n, g in ORDER: t += g; L[n] = round(t, 2); t += spoken(n)
END = round(t + 0.8, 2)
def at(n, key, last=False, end=False):
    hits = [(s, e) for w, s, e in words(n) if key in re.sub(r"[^a-z0-9']", "", w.lower())]
    s, e = hits[-1] if last else hits[0]
    return round(L[n] + (e if end else s), 2)

def build():
    out = os.path.join(HERE, "out", "v"); a = os.path.join(out, "assets")
    if os.path.exists(out): shutil.rmtree(out)
    os.makedirs(a)
    for f in ("karla-latin-700-normal.woff2", "ibm-plex-sans-arabic-arabic-700-normal.woff2"): shutil.copy(os.path.join(V6, "fonts", f), a)
    for f in ("fredoka-latin-600-normal.woff2", "fredoka-latin-700-normal.woff2", "instrument-serif-latin-400-normal.woff2"): shutil.copy(os.path.join(ROOT, "brag-quiz/fonts", f), a)
    shutil.copy(os.path.join(V6, "lib/gsap.min.js"), a)
    for f in ("crack.wav", "shimmer.wav", "tick.wav", "tick-lo.wav", "thump.wav", "whoosh.wav", "flip.wav", "chalk.wav"): shutil.copy(os.path.join(ROOT, "brag-quiz/sfx/soft", f), a)
    for f in ("click.wav", "swoosh.wav", "tap.wav"): shutil.copy(os.path.join(ROOT, "brag-quiz/sfx/ref", f), a)
    lv = lambda f: float(re.findall(r"I:\s+(-?[\d.]+) LUFS", subprocess.run(["ffmpeg", "-i", f, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr)[-1])
    target = lv(mp3("g3"))                                                   # Rafiq's Arabic level with Callum (the standard)
    for n in L:
        if n in ("jabr", "wajburni"):
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp3(n), "-af", f"volume={target - lv(mp3(n)):.1f}dB,alimiter=limit=0.95", os.path.join(a, n + ".mp3")], check=True)
        else: shutil.copy(mp3(n), a)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-i", os.path.join(V6, "sfx-gen/fountain.mp3"), "-af",
                    f"volume=6dB,atrim=0:{END},afade=t=in:d=0.6,afade=t=out:st={END - 0.3}:d=0.3", "-c:a", "libmp3lame", "-q:a", "3", os.path.join(a, "bed.mp3")], check=True)
    au = []
    def snd(name, t0, vol, d=None, track=None):
        d = d or dur(os.path.join(a, name))
        au.append(f'<audio id="s{len(au)}" src="assets/{name}" data-start="{max(0, t0):.3f}" data-duration="{d:.3f}" data-volume="{vol:.3f}" data-track-index="{track or 3 + len(au)}"></audio>')
    for n, t0 in L.items(): snd(f"{n}.mp3", t0, 1.0, track=1)
    snd("bed.mp3", 0, 0.1, END, track=2)
    js = []; T = js.append
    IN = lambda sel, t, y=40, d=0.45: T(f'tl.fromTo("{sel}", {{opacity:0, y:{y}, scale:0.96}}, {{opacity:1, y:0, scale:1, duration:{d}, ease:"back.out(1.6)"}}, {t:.2f});')
    OUT = lambda sel, t: T(f'tl.to("{sel}", {{opacity:0, y:-40, duration:0.3, ease:"power2.in"}}, {t:.2f});')
    def draw(sel, t, d=0.6): T(f'tl.fromTo("{sel}", {{strokeDashoffset:1}}, {{strokeDashoffset:0, duration:{d}, ease:"power1.inOut"}}, {t:.2f});')
    def scene(sel, t0, t1):                                                  # a scene comes up and goes, with a soft whoosh
        if t0 > 0: T(f'tl.fromTo("{sel}", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.45, ease:"power3.out"}}, {t0:.2f});')   # the first is there on frame 0
        if t1: T(f'tl.to("{sel}", {{opacity:0, y:-60, duration:0.35, ease:"power2.in"}}, {t1:.2f});'); snd("whoosh.wav", t1 - 0.05, 0.35)
    def count(sel, a0, b0, t, d, fmt="v"):                                   # numbers count, a click on every step
        T(f'(() => {{ const o = {{v:{a0}}}, el = document.querySelector("{sel}"); tl.to(o, {{v:{b0}, duration:{d}, ease:"power2.out", onUpdate:() => el.textContent = Math.round(o.v).toLocaleString("en-GB")}}, {t:.2f}); }})();')
        for k in range(10): snd("click.wav", t + d * (1 - (1 - (k + 1) / 10) ** 2) * 0.95, 0.15)

    # 1 · "…broken bones": the bone cracks on "broken"
    S1 = 0.0
    br = at("h1c", "broken")
    draw("#crack", br - 0.05, 0.18); snd("crack.wav", br - 0.02, 0.8)
    T(f'tl.to("#boneL", {{x:-40, y:18, rotation:-10, duration:0.3, ease:"back.out(3)", svgOrigin:"540 980"}}, {br + 0.1:.2f});')
    T(f'tl.to("#boneR", {{x:40, y:18, rotation:10, duration:0.3, ease:"back.out(3)", svgOrigin:"540 980"}}, {br + 0.1:.2f});')
    T(f'tl.fromTo(".shard", {{opacity:0, x:0, y:0}}, {{opacity:1, x:(i) => [-60, 50, -20, 70][i], y:(i) => [-80, -60, 90, 70][i], duration:0.5, ease:"power2.out"}}, {br + 0.1:.2f});')
    IN("#t1b", at("h1c", "bones"), 20, 0.3)
    # 2 · الْجَبْر · "putting broken pieces back together": the halves slide back, the break glows gold, a bandage
    OUT("#t1, #t1b", L["jabr"] - 0.3)
    IN("#jabr", L["jabr"] - 0.05); snd("tick-lo.wav", L["jabr"], 0.4)
    bt = at("g2", "back")
    T(f'tl.to(["#boneL", "#boneR"], {{x:0, y:0, rotation:0, duration:0.6, ease:"power3.inOut", svgOrigin:"540 980"}}, {bt:.2f});')
    T(f'tl.to(".shard", {{opacity:0, x:0, y:0, duration:0.4}}, {bt:.2f});'); snd("thump.wav", bt + 0.55, 0.4)
    T(f'tl.to("#crack", {{stroke:"{GOLD}", strokeWidth:14, duration:0.4}}, {at("g2", "together"):.2f});'); snd("shimmer.wav", at("g2", "together"), 0.3, 1.2)
    T(f'tl.fromTo("#band", {{opacity:0, scaleY:0}}, {{opacity:1, scaleY:1, duration:0.35, ease:"back.out(2)", transformOrigin:"50% 50%"}}, {at("g2", "together") + 0.3:.2f});')
    IN("#t2", at("g2", "putting") - 0.1)
    scene("#s1", S1, L["g3"] - 0.35)
    # 3 · Baghdad, ~1,200 years ago: the Tigris, the round city, the years counting; his book opens
    S3 = L["g3"] - 0.1; scene("#s3", S3, L["g4"] - 0.35)
    count("#yrs", 0, 1200, at("g3", "1200") - 0.1, 1.0); IN("#yago", at("g3", "years"))
    draw("#tigris", at("g3", "baghdad") - 0.5, 0.8); draw("#city", at("g3", "baghdad") - 0.1, 0.7); IN("#bgl", at("g3", "baghdad") + 0.3, 20)
    T(f'tl.fromTo("#gates circle", {{scale:0}}, {{scale:1, duration:0.25, stagger:0.08, ease:"back.out(3)", transformOrigin:"50% 50%"}}, {at("g3", "baghdad") + 0.4:.2f});')
    IN("#khw", at("g3", "scholar"), 30); IN("#book", at("g3", "book") - 0.2, 60); snd("flip.wav", at("g3", "book"), 0.4)
    T(f'tl.fromTo("#bookR", {{rotationY:0}}, {{rotationY:-160, duration:0.6, ease:"power2.inOut", transformOrigin:"0% 50%"}}, {at("g3", "solving"):.2f});')
    # 4 · "a square, plus ten of its sides, makes thirty-nine"
    S4 = L["g4"] - 0.1; scene("#s4", S4, None)
    IN("#eq0", at("g4", "square") - 0.2, 20); draw("#sq", at("g4", "square") - 0.1, 0.6); IN("#sqx", at("g4", "square") + 0.4, 10)
    IN("#eq1", at("g4", "plus") - 0.1, 20); draw("#strip", at("g4", "ten") - 0.1, 0.6); IN("#stripl", at("g4", "sides"), 10)
    IN("#eq2", at("g4", "thirty") - 0.1, 20); snd("tick-lo.wav", at("g4", "thirty"), 0.4)
    # 5 · "split the ten into two fives, on two sides… a corner is missing: five by five, twenty-five"
    sp = at("g5", "split")
    T(f'tl.to("#strip, #stripl", {{opacity:0, duration:0.25}}, {sp + 0.2:.2f});')
    T(f'tl.fromTo("#fiveA", {{opacity:0, x:200, y:-300}}, {{opacity:1, x:0, y:0, duration:0.6, ease:"power3.out"}}, {at("g5", "two") :.2f});')
    T(f'tl.fromTo("#fiveB", {{opacity:0, x:-200, y:300}}, {{opacity:1, x:0, y:0, duration:0.6, ease:"power3.out"}}, {at("g5", "sides"):.2f});')
    snd("swoosh.wav", at("g5", "two"), 0.3); snd("swoosh.wav", at("g5", "sides"), 0.3); IN("#l5", at("g5", "two"), 10)
    T(f'tl.fromTo("#corner", {{opacity:0}}, {{opacity:1, duration:0.2, yoyo:true, repeat:3}}, {at("g5", "missing"):.2f});')
    IN("#cl", at("g5", "twenty") - 0.1, 10); snd("tick.wav", at("g5", "twenty"), 0.4)
    # 6 · "fill it in… 39 + 25 = 64… its side is eight… take away the five: three"
    fi = at("g6", "fill")
    T(f'tl.to("#corner", {{opacity:1, fill:"{GOLD}", duration:0.3}}, {fi:.2f});'); snd("thump.wav", fi + 0.1, 0.4)
    draw("#big", at("g6", "perfect") - 0.1, 0.6); snd("shimmer.wav", at("g6", "perfect"), 0.25, 1.2)
    T(f'tl.to("#eqrow", {{opacity:0, y:-30, duration:0.25}}, {at("g6", "39") - 0.3:.2f});')
    IN("#sum", at("g6", "39") - 0.1, 20); T(f'tl.set("#n64", {{textContent:"?"}}, {at("g6", "39") - 0.1:.2f});')
    count("#n64", 0, 64, at("g6", "64") - 0.1, 0.7)
    IN("#side8", at("g6", "8") - 0.1, 10); snd("tick-lo.wav", at("g6", "8"), 0.4)
    T(f'tl.to("#side8", {{opacity:0, duration:0.2}}, {at("g6", "take") - 0.1:.2f});'); IN("#side5", at("g6", "take"), 10)
    IN("#ans", at("g6", "3", last=True) - 0.1, 30); snd("tick-lo.wav", at("g6", "3", last=True), 0.6); snd("shimmer.wav", at("g6", "3", last=True), 0.35, 1.2)
    T(f'tl.to("#s4", {{opacity:0, y:-60, duration:0.35, ease:"power2.in"}}, {L["g7"] - 0.4:.2f});'); snd("whoosh.wav", L["g7"] - 0.45, 0.35)
    # 7 · "al-jabr became algebra… a bone-setter… an algebrista": the word changes on a manuscript; the sign swings
    S7 = L["g7"] - 0.1; scene("#s7", S7, L["g8"] - 0.35)
    IN("#ms", L["g7"] + 0.1, 40); snd("flip.wav", L["g7"] + 0.2, 0.3)
    al = at("g7", "algebra", last=True)
    T(f'tl.to("#msar", {{opacity:0, filter:"blur(8px)", duration:0.35}}, {al - 0.35:.2f});')
    T(f'tl.fromTo("#msla", {{opacity:0, clipPath:"inset(0% 100% 0% 0%)"}}, {{opacity:1, clipPath:"inset(0% 0% 0% 0%)", duration:0.6, ease:"power1.inOut"}}, {al - 0.2:.2f});'); snd("chalk.wav", al - 0.2, 0.3, 0.6)
    T(f'tl.fromTo("#sign", {{opacity:0, y:-200}}, {{opacity:1, y:0, duration:0.5, ease:"back.out(1.6)"}}, {at("g7", "spain") - 0.1:.2f});')
    T(f'tl.fromTo("#signb", {{rotation:-8}}, {{rotation:8, duration:0.7, yoyo:true, repeat:3, ease:"sine.inOut", svgOrigin:"540 1060"}}, {at("g7", "spain") + 0.3:.2f});')
    IN("#signt", at("g7", "algebrista") - 0.1, 10); snd("tick-lo.wav", at("g7", "algebrista"), 0.5)
    # 8 · "his own name, al-Khwārizmī, became… algorithm": the name morphs, step by step
    S8 = L["g8"] - 0.1; scene("#s8", S8, L["t1s"] - 0.4)
    IN("#n1", at("g8", "name") - 0.1); T(f'tl.to("#n1", {{opacity:0.25, scale:0.8, duration:0.3}}, {at("g8", "became") - 0.1:.2f});')
    IN("#n2", at("g8", "became") - 0.1, 30); snd("tap.wav", at("g8", "became"), 0.3)
    T(f'tl.to("#n2", {{opacity:0.25, scale:0.8, duration:0.3}}, {at("g8", "algorithm") - 0.25:.2f});')
    IN("#n3", at("g8", "algorithm") - 0.1, 30); snd("tick-lo.wav", at("g8", "algorithm"), 0.5)
    T(f'tl.fromTo(".code", {{opacity:0, x:-30}}, {{opacity:1, x:0, duration:0.3, stagger:0.12}}, {at("g8", "algorithm") + 0.4:.2f});')
    # 9 · your turn: وَاجْبُرْنِي on a prayer mat; three answers; 3-2-1
    S9 = L["t1s"] - 0.1; scene("#s9", S9, L["end"] - 0.4)
    IN("#mat", L["t1s"] + 0.1, 60); IN("#yt", L["t1s"], 20)
    IN("#wj", L["wajburni"] - 0.05, 20); snd("tick-lo.wav", L["wajburni"], 0.4)
    for i in range(3): IN(f"#op{i}", at("t1b", "mean") + 0.2 + i * 0.25, 20); snd("tap.wav", at("t1b", "mean") + 0.2 + i * 0.25, 0.25)
    c0 = round(L["t1b"] + spoken("t1b") + 0.25, 2)
    for k, nm in enumerate(("3", "2", "1")):
        T(f'tl.set("#cd", {{textContent:"{nm}", opacity:1}}, {c0 + k:.2f});'); T(f'tl.fromTo("#cd", {{scale:1.4}}, {{scale:1, duration:0.3, ease:"back.out(2)"}}, {c0 + k:.2f});')
        snd("click.wav", c0 + k, 0.5)
    T(f'tl.to("#cd", {{opacity:0, duration:0.2}}, {L["b6"] - 0.1:.2f});')
    T(f'tl.to("#op1", {{backgroundColor:"{GOLD}", scale:1.08, duration:0.25, ease:"back.out(2)"}}, {at("b6", "mend") - 0.05:.2f});'); snd("shimmer.wav", at("b6", "mend"), 0.4, 1.2)
    T(f'tl.to(["#op0", "#op2"], {{opacity:0.35, duration:0.3}}, {at("b6", "mend"):.2f});')
    # 10 · "set right whatever is broken in me": a cracked bowl, mended with gold
    T(f'tl.to("#mat", {{opacity:0, duration:0.3}}, {at("b6", "set") - 0.4:.2f});')
    IN("#bowl", at("b6", "set") - 0.3, 40)
    draw(".seam", at("b6", "broken") - 0.1, 0.9); snd("shimmer.wav", at("b6", "broken"), 0.3, 1.2)
    # 11 · the ask, heard in full
    S11 = L["end"] - 0.1; scene("#s11", S11, None)
    IN("#ask", L["end"], 30); IN("#url", at("end", "comment"), 20); snd("tick-lo.wav", at("end", "comment"), 0.5)
    T(f'tl.fromTo("#arr", {{y:0}}, {{y:18, duration:0.4, yoyo:true, repeat:5, ease:"sine.inOut"}}, {at("end", "comment"):.2f});')

    # captions: the line being said, word by word, small under the picture
    caps = ""; k = 0
    for n in L:
        if n in ("jabr", "wajburni"): continue
        ws = words(n); chunk = []
        for i, (w, s, e) in enumerate(ws):
            chunk.append((w, s))
            if w[-1] in ",.:?!" or len(chunk) >= 6 or i + 1 == len(ws):
                nxt = L[n] + ws[i + 1][1] if i + 1 < len(ws) else L[n] + e + 0.4
                caps += f'<div class="cap" id="cp{k}">' + " ".join(f'<span id="cp{k}w{j}">{x}</span>' for j, (x, _) in enumerate(chunk)) + "</div>"
                T(f'tl.set("#cp{k}", {{opacity:1}}, {L[n] + chunk[0][1] - 0.02:.2f});')
                for j, (x, s0) in enumerate(chunk): T(f'tl.fromTo("#cp{k}w{j}", {{opacity:0, y:10}}, {{opacity:1, y:0, duration:0.2}}, {L[n] + s0:.2f});')
                T(f'tl.to("#cp{k}", {{opacity:0, duration:0.15}}, {nxt - 0.05:.2f});'); k += 1; chunk = []

    blobs = "".join(f'<i class="blob" style="left:{x}px;top:{y}px;width:{r}px;height:{r}px;background:{c}"></i>' for x, y, r, c in
                    ((-200, -150, 700, "#f4d9c6"), (600, 200, 600, "#cfe5dc"), (-150, 1100, 650, "#f6e3b4"), (650, 1300, 600, "#e8d5e6")))
    sq = 'x="250" y="760" width="180" height="180"'                     # to scale: x = 3 → 180 px, so 5 → 300 px
    css = f"""
@font-face {{ font-family:"FR"; src:url("assets/fredoka-latin-600-normal.woff2"); font-weight:600; }}
@font-face {{ font-family:"FR"; src:url("assets/fredoka-latin-700-normal.woff2"); font-weight:700; }}
@font-face {{ font-family:"KA"; src:url("assets/karla-latin-700-normal.woff2"); font-weight:700; }}
@font-face {{ font-family:"SE"; src:url("assets/instrument-serif-latin-400-normal.woff2"); }}
@font-face {{ font-family:"AR"; src:url("assets/ibm-plex-sans-arabic-arabic-700-normal.woff2"); }}
* {{ margin:0; box-sizing:border-box; }} html, body {{ width:1080px; height:1920px; overflow:hidden; background:{CREAM}; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; background:{CREAM}; font-family:FR; color:{INK}; }}
.blob {{ position:absolute; border-radius:50%; filter:blur(60px); opacity:.75; }}
.sc {{ position:absolute; inset:0; opacity:0; }} #s1 {{ opacity:1; }}
svg.full {{ position:absolute; left:0; top:0; width:1080px; height:1920px; overflow:visible; }}
.ln {{ fill:none; stroke:{INK}; stroke-width:9; stroke-linecap:round; stroke-linejoin:round; stroke-dasharray:1; stroke-dashoffset:1; }}
.t {{ position:absolute; left:0; right:0; text-align:center; font-weight:700; opacity:0; }}
.ar {{ font-family:AR; direction:rtl; }}
.pill {{ display:inline-block; padding:10px 28px; border-radius:999px; background:#fff; box-shadow:0 10px 30px -14px rgba(23,38,43,.4); }}
.cap {{ position:absolute; left:80px; right:80px; top:1560px; text-align:center; font-family:KA; font-weight:700; font-size:50px; line-height:1.2; color:{INK}; opacity:0; }}
.cap span {{ display:inline-block; opacity:0; }}
#logo {{ position:absolute; top:70px; left:0; right:0; display:flex; justify-content:center; gap:12px; align-items:center; }}
#logo .tile {{ position:relative; width:58px; height:58px; border-radius:16px; background:{INK}; display:grid; place-items:center; }}
#logo .tile span {{ font-family:AR; font-size:36px; color:{CREAM}; margin-top:-4px; }} #logo .tile em {{ position:absolute; right:9px; top:8px; width:9px; height:9px; border-radius:50%; background:{RED}; }}
#logo b {{ font-family:AR; font-size:42px; }}
.op {{ display:block; width:620px; margin:18px auto 0; padding:22px; border-radius:26px; background:#fff; font-size:52px; text-align:center; box-shadow:0 12px 30px -16px rgba(23,38,43,.45); opacity:0; }}
#cd {{ position:absolute; left:0; right:0; top:1300px; text-align:center; font-size:130px; font-weight:700; color:{RED}; opacity:0; }}
"""
    body = f"""{blobs}
<div id="logo"><span class="tile"><span>ر</span><em></em></span><b>رَفِيق</b></div>
<div class="sc" id="s1">
 <div class="t" id="t1" style="top:250px;font-size:120px;color:{TEAL};opacity:1">algebra</div>
 <div class="t" id="t1b" style="top:400px;font-size:56px">= setting broken bones?</div>
 <div class="t ar" id="jabr" style="top:220px;font-size:230px;line-height:1.4;color:{RED}">الْجَبْر</div>
 <div class="t" id="t2" style="top:560px;font-size:56px"><span class="pill">putting broken pieces <b style="color:{TEAL}">back together</b></span></div>
 <svg class="full" viewBox="0 0 1080 1920" style="transform:scale(1.3);transform-origin:540px 980px">
  <g id="boneL"><path d="M300 940 C 240 880, 160 900, 170 960 C 120 980, 150 1060, 220 1040 C 250 1030, 280 1010, 300 1010 L 540 1010 L 528 990 L 552 975 L 532 955 L 540 940 Z" fill="{BONE}" stroke="{INK}" stroke-width="9" stroke-linejoin="round"/></g>
  <g id="boneR"><path d="M780 940 C 840 880, 920 900, 910 960 C 960 980, 930 1060, 860 1040 C 830 1030, 800 1010, 780 1010 L 540 1010 L 528 990 L 552 975 L 532 955 L 540 940 Z" fill="{BONE}" stroke="{INK}" stroke-width="9" stroke-linejoin="round"/></g>
  <path id="crack" class="ln" pathLength="1" d="M540 940 L 532 955 L 552 975 L 528 990 L 540 1010" style="stroke-width:7"/>
  {''.join(f'<path class="shard" d="M{x} {y} l14 -10 l8 16 z" fill="{BONE}" stroke="{INK}" stroke-width="4" opacity="0"/>' for x, y in ((535, 950), (545, 960), (538, 995), (548, 1000)))}
  <rect id="band" x="470" y="925" width="140" height="100" rx="18" fill="#ffffff" stroke="{TEAL}" stroke-width="7" opacity="0"/>
 </svg>
</div>
<div class="sc" id="s3">
 <div class="t" id="yago" style="top:200px;font-size:60px"><b id="yrs" style="font-size:150px;color:{RED}">0</b><br>years ago</div>
 <svg class="full" viewBox="0 0 1080 1920" style="transform:scale(1.25);transform-origin:560px 880px">
  <path id="tigris" class="ln" pathLength="1" d="M760 520 C 700 650, 820 760, 720 900 C 640 1010, 760 1120, 700 1260" style="stroke:{BLUE};stroke-width:30"/>
  <circle id="city" class="ln" pathLength="1" cx="520" cy="880" r="150" style="stroke-width:12"/>
  <g id="gates">{''.join(f'<circle cx="{520 + 150 * dx}" cy="{880 + 150 * dy}" r="20" fill="{GOLD}" stroke="{INK}" stroke-width="5"/>' for dx, dy in ((0.71, 0.71), (-0.71, 0.71), (0.71, -0.71), (-0.71, -0.71)))}</g>
  <circle cx="520" cy="880" r="34" fill="{TEAL}" stroke="{INK}" stroke-width="6"/>
 </svg>
 <div class="t" id="bgl" style="top:1090px;font-size:60px"><span class="pill">Baghdad</span></div>
 <div class="t" id="khw" style="top:1160px;font-size:52px;color:{TEAL}">al-Khwārizmī</div>
 <div id="book" style="position:absolute;left:330px;top:1260px;width:420px;height:270px;opacity:0;perspective:1200px">
  <div style="position:absolute;left:0;top:0;width:210px;height:270px;background:#fff;border:7px solid {INK};border-radius:14px 0 0 14px"></div>
  <div style="position:absolute;left:210px;top:0;width:210px;height:270px;background:#fff;border:7px solid {INK};border-radius:0 14px 14px 0;text-align:center;font-size:30px;padding-top:70px">x² + 10x<br>= 39</div>
  <div id="bookR" style="position:absolute;left:210px;top:0;width:210px;height:270px;background:{TEAL};border:7px solid {INK};border-radius:0 14px 14px 0;color:#fff;text-align:center;padding-top:60px;font-family:AR;font-size:60px;backface-visibility:hidden">الجبر</div>
 </div>
</div>
<div class="sc" id="s4">
 <div id="eqrow" class="t" style="top:240px;font-size:96px;opacity:1"><span id="eq0" style="opacity:0;display:inline-block">x²</span> <span id="eq1" style="opacity:0;display:inline-block">+ 10x</span> <span id="eq2" style="opacity:0;display:inline-block">= 39</span></div>
 <div id="sum" class="t" style="top:240px;font-size:84px">39 + 25 = <b id="n64" style="color:{RED}">?</b></div>
 <svg class="full" viewBox="0 0 1080 1920">
  <rect id="corner" x="430" y="940" width="300" height="300" fill="none" stroke="{RED}" stroke-width="7" stroke-dasharray="16 12" opacity="0"/>
  <rect id="fiveA" x="430" y="760" width="300" height="180" fill="#cfe5dc" stroke="{INK}" stroke-width="8" opacity="0"/>
  <rect id="fiveB" x="250" y="940" width="180" height="300" fill="#cfe5dc" stroke="{INK}" stroke-width="8" opacity="0"/>
  <rect id="sq" class="ln" pathLength="1" {sq} style="fill:#f6e3b4;fill-opacity:.9"/>
  <rect id="strip" class="ln" pathLength="1" x="250" y="1000" width="600" height="180" style="fill:#cfe5dc"/>
  <rect id="big" class="ln" pathLength="1" x="250" y="760" width="480" height="480" style="stroke:{RED};stroke-width:12"/>
 </svg>
 <div class="t" id="sqx" style="top:800px;left:250px;right:auto;width:180px;font-size:80px">x²</div>
 <div class="t" id="stripl" style="top:1200px;font-size:52px">10 × x &nbsp;(ten of its sides)</div>
 <div class="t" id="cl" style="top:1030px;left:430px;right:auto;width:300px;font-size:60px;color:{RED}">5 × 5<br>= 25</div>
 <div class="t" id="side8" style="top:1270px;font-size:60px">side = <b style="color:{RED}">8</b></div>
 <div class="t" id="side5" style="top:1270px;font-size:60px">8 − 5 = x</div>
 <div class="t" id="ans" style="top:1360px;font-size:150px;color:{TEAL}">x = 3</div>
 <div class="t" style="top:690px;left:250px;right:auto;width:180px;font-size:48px;opacity:1">x</div><div class="t" id="l5" style="top:690px;left:430px;right:auto;width:300px;font-size:48px">5</div>
</div>
<div class="sc" id="s7">
 <div id="ms" style="position:absolute;left:190px;top:330px;width:700px;height:520px;background:#efe0bd;border-radius:18px;box-shadow:0 30px 60px -30px rgba(23,38,43,.6);opacity:0">
  <div class="ar" id="msar" style="position:absolute;inset:0;display:grid;place-items:center;font-size:170px;color:{INK}">الجبر</div>
  <div id="msla" style="position:absolute;inset:0;display:grid;place-items:center;font-family:SE;font-style:italic;font-size:150px;color:{RED};opacity:0">algebra</div>
  <div style="position:absolute;left:30px;right:30px;bottom:30px;text-align:center;font-family:SE;font-style:italic;font-size:34px;color:#7a6a4a">Latin, 1100s</div></div>
 <svg class="full" viewBox="0 0 1080 1920" id="sign" style="opacity:0"><g id="signb">
  <line x1="540" y1="1000" x2="540" y2="1060" stroke="{INK}" stroke-width="8"/>
  <rect x="300" y="1060" width="480" height="230" rx="24" fill="#fff" stroke="{INK}" stroke-width="9"/>
  <path d="M430 1210 C 410 1190, 380 1200, 385 1222 C 365 1232, 380 1258, 405 1250 L 675 1250 C 700 1258, 715 1232, 695 1222 C 700 1200, 670 1190, 650 1210 Z" fill="{BONE}" stroke="{INK}" stroke-width="6"/></g></svg>
 <div class="t" id="signt" style="top:1090px;font-size:64px;color:{TEAL}">ALGEBRISTA</div>
</div>
<div class="sc" id="s8">
 <div class="t" id="n1" style="top:380px;font-size:100px;color:{TEAL}">al-Khwārizmī</div>
 <div class="t" id="n2" style="top:560px;font-size:100px">Algoritmi</div>
 <div class="t" id="n3" style="top:760px;font-size:120px;color:{RED}">algorithm</div>
 {''.join(f'<div class="t code" style="top:{1010 + i * 80}px;left:300px;right:auto;text-align:left;font-family:KA;font-size:44px;color:#5c6e70">{c}</div>' for i, c in enumerate(("step 1 →", "step 2 →", "step 3 → ✓")))}
</div>
<div class="sc" id="s9">
 <div class="t" id="yt" style="top:200px;font-size:64px;color:{TEAL}">Your turn</div>
 <svg class="full" viewBox="0 0 1080 1920" id="mat" style="opacity:0"><path d="M300 1500 L 300 900 C 300 760, 780 760, 780 900 L 780 1500 Z" fill="{TEAL}" stroke="{INK}" stroke-width="9"/>
  <path d="M360 1450 L 360 940 C 360 840, 720 840, 720 940 L 720 1450 Z" fill="none" stroke="{GOLD}" stroke-width="7"/></svg>
 <div class="t ar" id="wj" style="top:330px;font-size:170px;line-height:1.4;color:{RED}">وَاجْبُرْنِي</div>
 <div style="position:absolute;left:0;right:0;top:640px"><div class="op" id="op0">and forgive me</div><div class="op" id="op1">and mend me</div><div class="op" id="op2">and guide me</div></div>
 <div id="cd">3</div>
 <svg class="full" viewBox="0 0 1080 1920" id="bowl" style="opacity:0"><path d="M260 1100 C 280 1320, 800 1320, 820 1100 Z" fill="{BONE}" stroke="{INK}" stroke-width="9"/>
  <path class="ln seam" pathLength="1" d="M420 1100 L 450 1160 L 430 1210 L 470 1280" style="stroke:{GOLD};stroke-width:10"/>
  <path class="ln seam" pathLength="1" d="M680 1100 L 650 1170 L 690 1230" style="stroke:{GOLD};stroke-width:10"/></svg>
</div>
<div class="sc" id="s11">
 <div class="t" id="ask" style="top:420px;font-size:84px;line-height:1.2">What do you say<br>between the two<br>sujood?</div>
 <div class="t" id="url" style="top:900px;font-size:56px"><span class="pill" style="background:{TEAL};color:#fff">rafiq-arabic.com</span></div>
 <svg class="full" viewBox="0 0 1080 1920"><path id="arr" d="M540 1100 L 540 1260 M 480 1200 L 540 1265 L 600 1200" fill="none" stroke="{RED}" stroke-width="12" stroke-linecap="round"/></svg>
</div>
{caps}"""
    open(os.path.join(out, "index.html"), "w").write(f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" /><title>algebra</title>
<script src="assets/gsap.min.js"></script><style>{css}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{END}">
{body}
{chr(10).join(au)}
</div><script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;</script></body></html>
""")
    print("built", END, "s,", len(au), "sounds;", L)

if __name__ == "__main__":
    build()
