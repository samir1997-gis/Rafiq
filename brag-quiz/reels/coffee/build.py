#!/usr/bin/env python3
"""h2-coffee in the new format (owner, 27 Oct 2026, #300: "do the same for the h2 coffee" as h1-algebra, #298): a simpler, more detailed
script (tools/typesafe-exp/coffee_v2_script.py, A) told with full-screen drawings on the series' pastel page, every move on its word:
  1 "…coffee used to mean… wine": the cup turns into a wine glass · 2 قَهْوَة (Rafiq) · "old Arabic dictionaries… takes away your appetite":
  a dictionary opens, a plate slides away · 3 "in the 1400s, Sufis in Yemen… coffee beans… awake… night prayers": a night window, the years
  counting, beans into a pot, an eye opening, a prayer mat · 4 "the old name: qahwa": the name moves from the glass to the cup · 5-6 the
  route on a doodle map, Yemen → Makkah → Cairo → Istanbul (kahve), a ship to the Dutch (koffie), English by 1582 (coffee) · 7 your turn:
  مَسْجِد, the place of sujood; مَقْهى? a coffee pot / a café / a coffee bean, 3-2-1; "A CAFE!" · 8 the ask: how do you take yours?
Easing as MOTION-STYLE.md (owner, 27 Oct 2026): entrances ease out, exits ease in, interface springs with a slight overshoot, nothing linear.
Sources as #296: qahwa "wine" in the old lexicographers, "because it takes away the appetite" (Hattox, Coffee and Coffeehouses, quoting
them); Yemeni Sufis in the 1400s drinking it for night devotions; Makkah and Cairo by about 1500, Istanbul's kahve; Dutch koffie, English
"coffee" first recorded 1582.

  python3 brag-quiz/reels/coffee/build.py    then  cd brag-quiz/reels/coffee/out/v && npx hyperframes render -o ../coffee-raw.mp4
"""
import json, os, re, shutil, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
V6 = os.path.join(ROOT, "brag-output-v6/composition/assets"); VO = os.path.join(ROOT, "brag-quiz/voice/coffee")
INK, CREAM, GOLD, RED, TEAL, BLUE, BROWN, NIGHT = "#17262B", "#F6EFE2", "#E9B949", "#B4322A", "#2E7263", "#7FA7C9", "#6B4226", "#1f3550"
dur = lambda f: float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))
mp3 = lambda n: os.path.join(VO, n + ".mp3")
def words(n):                                                             # [word, start, end]; the older lines (#296) have no ends
    ws = json.load(open(os.path.join(VO, n + ".words.json")))
    return [(w[0], w[1], w[2] if len(w) > 2 else (ws[i + 1][1] if i + 1 < len(ws) else w[1] + 0.45)) for i, w in enumerate(ws)]
ORDER = [("h1c", 0.3), ("qahwa", 0.3), ("k2", 0.25), ("k3", 0.35), ("k4", 0.3), ("k5", 0.35), ("k6", 0.35),
         ("t1", 1.3), ("maqha", 0.25), ("b6", 3.6), ("end", 0.5)]                                    # b6 waits for the 3-2-1
ARABIC = ("qahwa", "maqha")
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
    for f in ("shimmer.wav", "tick.wav", "tick-lo.wav", "thump.wav", "whoosh.wav", "flip.wav", "wind.wav"): shutil.copy(os.path.join(ROOT, "brag-quiz/sfx/soft", f), a)
    for f in ("click.wav", "swoosh.wav", "tap.wav"): shutil.copy(os.path.join(ROOT, "brag-quiz/sfx/ref", f), a)
    lv = lambda f: float(re.findall(r"I:\s+(-?[\d.]+) LUFS", subprocess.run(["ffmpeg", "-i", f, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr)[-1])
    target = lv(mp3("k3"))                                                   # Rafiq's Arabic level with Callum (the standard)
    for n in L:
        if n in ARABIC:
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
    # the easing rule (MOTION-STYLE.md): in = ease out, out = ease in, interface = spring with a slight overshoot, moves = in-out
    IN = lambda sel, t, y=40, d=0.5: T(f'tl.fromTo("{sel}", {{opacity:0, y:{y}}}, {{opacity:1, y:0, duration:{d}, ease:"power3.out"}}, {t:.2f});')
    POP = lambda sel, t, s=0.6: T(f'tl.fromTo("{sel}", {{opacity:0, scale:{s}}}, {{opacity:1, scale:1, duration:0.45, ease:"back.out(1.4)"}}, {t:.2f});')
    OUT = lambda sel, t, y=-40: T(f'tl.to("{sel}", {{opacity:0, y:{y}, duration:0.3, ease:"power2.in"}}, {t:.2f});')
    MOVE = lambda sel, t, d, **k: T(f'tl.to("{sel}", {{{", ".join(f"{x}:{v}" for x, v in k.items())}, duration:{d}, ease:"power2.inOut"}}, {t:.2f});')
    def draw(sel, t, d=0.6): T(f'tl.fromTo("{sel}", {{strokeDashoffset:1}}, {{strokeDashoffset:0, duration:{d}, ease:"power2.inOut"}}, {t:.2f});')
    def scene(sel, t0, t1):
        if t0 > 0: T(f'tl.fromTo("{sel}", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.45, ease:"power3.out"}}, {t0:.2f});')   # the first is there on frame 0
        if t1: T(f'tl.to("{sel}", {{opacity:0, y:-60, duration:0.35, ease:"power2.in"}}, {t1:.2f});'); snd("whoosh.wav", t1 - 0.05, 0.35)
    def count(sel, a0, b0, t, d, sep=True):                                  # numbers count, a click on every step
        f = 'Math.round(o.v).toLocaleString("en-GB")' if sep else "Math.round(o.v)"
        T(f'(() => {{ const o = {{v:{a0}}}, el = document.querySelector("{sel}"); tl.to(o, {{v:{b0}, duration:{d}, ease:"power2.out", onUpdate:() => el.textContent = {f}}}, {t:.2f}); }})();')
        for k in range(10): snd("click.wav", t + d * (1 - (1 - (k + 1) / 10) ** 2) * 0.95, 0.15)

    # 1 · "The Arabic word for coffee used to mean… wine": the steaming cup becomes a wine glass
    draw(".steam", 0.2, 1.0)
    T('tl.fromTo(".steam", {y:0}, {y:-14, duration:0.9, yoyo:true, repeat:3, ease:"sine.inOut"}, 0.2);')
    T(f'tl.fromTo("#k1w", {{scale:1}}, {{scale:1.12, duration:0.25, yoyo:true, repeat:1, ease:"power2.out"}}, {at("h1c", "coffee"):.2f});'); snd("tick-lo.wav", at("h1c", "coffee"), 0.4)
    wn = at("h1c", "wine")
    T(f'tl.to("#cup", {{opacity:0, scale:0.6, y:40, duration:0.25, ease:"power2.in", transformOrigin:"50% 80%"}}, {wn - 0.3:.2f});')
    POP("#glass", wn - 0.05, 0.4); snd("tap.wav", wn - 0.05, 0.5)
    T(f'tl.fromTo("#wineL", {{scaleY:0}}, {{scaleY:1, duration:0.5, ease:"power3.out", transformOrigin:"50% 100%"}}, {wn + 0.15:.2f});'); snd("shimmer.wav", wn + 0.1, 0.3, 1.2)
    IN("#k1b", wn, 20, 0.35)
    # 2 · قَهْوَة · "old Arabic dictionaries say it meant wine, because it takes away your appetite"
    S2 = L["qahwa"] - 0.25; scene("#s1", 0, S2 - 0.05); scene("#s2", S2, L["k3"] - 0.35)
    POP("#qw", L["qahwa"] - 0.05, 0.7); snd("tick-lo.wav", L["qahwa"], 0.4)
    IN("#dict", at("k2", "dictionaries") - 0.2, 60); snd("flip.wav", at("k2", "dictionaries"), 0.4)
    T(f'tl.fromTo("#dictR", {{rotationY:0}}, {{rotationY:-165, duration:0.6, ease:"power2.inOut", transformOrigin:"0% 50%"}}, {at("k2", "dictionaries") + 0.3:.2f});')
    POP("#dglass", at("k2", "wine") - 0.05); snd("tap.wav", at("k2", "wine"), 0.3)
    IN("#plate", at("k2", "because"), 40)
    T(f'tl.to("#plate", {{x:700, rotation:20, opacity:0, duration:0.55, ease:"power2.in"}}, {at("k2", "away"):.2f});'); snd("swoosh.wav", at("k2", "away"), 0.35)
    POP("#k2p", at("k2", "appetite") - 0.1)
    # 3 · "in the 1400s, Sufis in Yemen drank a dark brew made from coffee beans, to stay awake for their night prayers"
    S3 = L["k3"] - 0.1; scene("#s3", S3, L["k4"] - 0.35)
    POP("#win", L["k3"], 0.85); snd("tick-lo.wav", L["k3"], 0.3)
    yr = at("k3", "fourteen") if [w for w in words("k3") if "fourteen" in w[0].lower()] else at("k3", "14")
    count("#yrs", 1000, 1400, yr - 0.1, 0.8, sep=False); IN("#yrsl", yr - 0.1, 20)
    POP("#yemen", at("k3", "yemen") - 0.1); snd("tap.wav", at("k3", "yemen"), 0.3)
    T(f'tl.fromTo("#stars i", {{opacity:0, scale:0}}, {{opacity:1, scale:1, duration:0.3, stagger:0.06, ease:"back.out(1.4)"}}, {at("k3", "sufis") - 0.1:.2f});')
    IN("#pot", at("k3", "dark") - 0.2, 40)
    T(f'tl.fromTo(".bean", {{opacity:0, y:-160}}, {{opacity:1, y:0, duration:0.45, stagger:0.12, ease:"power3.out"}}, {at("k3", "beans") - 0.3:.2f});')
    for k in range(4): snd("tick.wav", at("k3", "beans") - 0.3 + k * 0.12 + 0.4, 0.3)
    T(f'tl.to(".bean", {{opacity:0, y:60, duration:0.3, stagger:0.08, ease:"power2.in"}}, {at("k3", "beans") + 0.6:.2f});')
    T(f'tl.fromTo("#brew", {{scaleY:0}}, {{scaleY:1, duration:0.6, ease:"power3.out", transformOrigin:"50% 100%"}}, {at("k3", "beans") + 0.7:.2f});')
    aw = at("k3", "awake")
    POP("#eye", aw - 0.3); T(f'tl.fromTo("#lid", {{scaleY:1}}, {{scaleY:0.05, duration:0.35, ease:"power3.out", transformOrigin:"50% 0%"}}, {aw:.2f});'); snd("tick-lo.wav", aw, 0.4)
    T(f'tl.fromTo("#moon", {{opacity:0, x:-60}}, {{opacity:1, x:0, duration:0.6, ease:"power3.out"}}, {at("k3", "night") - 0.1:.2f});')
    POP("#mat", at("k3", "prayers") - 0.1, 0.7); snd("shimmer.wav", at("k3", "prayers"), 0.25, 1.2)
    # 4 · "and they gave it the old name: qahwa": the name leaves the glass for the cup
    S4 = L["k4"] - 0.1; scene("#s4", S4, L["k5"] - 0.35)
    IN("#oglass", L["k4"] + 0.05, 40); IN("#ocup", L["k4"] + 0.25, 40); POP("#tag", at("k4", "old") - 0.1); snd("tap.wav", at("k4", "old"), 0.3)
    qa = at("k4", "qahwa")
    MOVE("#tag", qa - 0.35, 0.6, x=500, rotation=-6); snd("swoosh.wav", qa - 0.35, 0.3)
    T(f'tl.to("#oglass", {{opacity:0.25, duration:0.3, ease:"power2.in"}}, {qa:.2f});'); draw("#ox", qa + 0.1, 0.35)
    T(f'tl.fromTo("#ocup", {{scale:1}}, {{scale:1.08, duration:0.25, yoyo:true, repeat:1, ease:"power2.out"}}, {qa + 0.25:.2f});'); snd("tick-lo.wav", qa + 0.25, 0.4)
    # 5 · "from Yemen it travelled to Makkah and Cairo, then to Istanbul, where it became kahve": the route on a map
    S5 = L["k5"] - 0.1; scene("#s5", S5, L["t1"] - 0.4)
    T(f'tl.fromTo("#map", {{opacity:0}}, {{opacity:1, duration:0.5, ease:"power3.out"}}, {S5:.2f});')
    PINS = [("pY", "yemen"), ("pM", "makkah"), ("pC", "cairo"), ("pI", "istanbul")]
    for i, (p, w) in enumerate(PINS):
        tw = at("k5", w)
        if i: draw(f"#r{i}", tw - 0.45, 0.45)
        POP(f"#{p}", tw - 0.05, 0.3); snd("tap.wav", tw - 0.05, 0.35)
    POP("#kahve", at("k5", "kahve") - 0.1); snd("tick-lo.wav", at("k5", "kahve"), 0.5)
    # 6 · "ships carried it to Europe. The Dutch said koffie, and by 1582, English had a new word: coffee"
    sh = at("k6", "ships")
    MOVE("#mapcam", sh - 0.3, 0.8, y=380)                                     # the map slides down: Europe comes into view
    T(f'tl.fromTo("#shipi", {{opacity:0, scale:0.6}}, {{opacity:1, scale:1, duration:0.4, ease:"back.out(1.4)"}}, {sh:.2f});'); snd("wind.wav", sh, 0.25, 1.6)
    T(f'(() => {{ const p = document.querySelector("#r5"), L5 = p.getTotalLength(), o = {{v:0}}, s = document.querySelector("#ship");'
      f' tl.to(o, {{v:1, duration:1.6, ease:"power2.inOut", onUpdate:() => {{ const q = p.getPointAtLength(o.v * L5); s.setAttribute("transform", `translate(${{q.x}},${{q.y}})`); }}}}, {sh + 0.1:.2f}); }})();')
    draw("#r5", sh + 0.1, 1.6)
    POP("#pA", at("k6", "dutch") - 0.1, 0.3); POP("#koffie", at("k6", "koffie") - 0.1); snd("tap.wav", at("k6", "koffie"), 0.4)
    yk = [w for w in words("k6") if re.sub(r"[^0-9]", "", w[0])]
    y82 = round(L["k6"] + yk[0][1], 2) if yk else at("k6", "fifteen")
    draw("#r6", y82 - 0.3, 0.5); POP("#pL", y82 - 0.1, 0.3); IN("#y1582", y82 - 0.1, 20); count("#n1582", 1500, 1582, y82 - 0.1, 0.8, sep=False)
    cf = at("k6", "coffee", last=True)
    T(f'tl.fromTo("#coffee", {{opacity:0, scale:1.8}}, {{opacity:1, scale:1, duration:0.45, ease:"back.out(1.7)"}}, {cf - 0.05:.2f});')   # the one slam
    snd("thump.wav", cf + 0.15, 0.6); snd("shimmer.wav", cf + 0.1, 0.3, 1.2)
    # 7 · your turn: مَسْجِد, the place of sujood; مَقْهى? three answers, 3-2-1; "A CAFE!"
    S7 = L["t1"] - 0.1; scene("#s7", S7, L["end"] - 0.4)
    IN("#yt", L["t1"], 20)
    POP("#msj", at("t1", "masjid") - 0.1); snd("tick-lo.wav", at("t1", "masjid"), 0.4)
    T(f'tl.to("#msj .m", {{color:"{GOLD}", duration:0.3, ease:"power2.out"}}, {at("t1", "place") - 0.1:.2f});')
    IN("#msjl", at("t1", "sujood") - 0.2, 20)
    T(f'tl.to("#msjbox", {{opacity:0.3, scale:0.7, y:-90, duration:0.45, ease:"power2.inOut"}}, {L["maqha"] - 0.5:.2f});')
    POP("#mq", L["maqha"] - 0.05, 0.7); snd("tick-lo.wav", L["maqha"], 0.4)
    T(f'tl.to("#mq .m", {{color:"{GOLD}", duration:0.3, ease:"power2.out"}}, {L["maqha"] + 0.5:.2f});')
    o0 = round(L["maqha"] + spoken("maqha") + 0.1, 2)
    for i in range(3): POP(f"#op{i}", o0 + i * 0.25, 0.8); snd("tap.wav", o0 + i * 0.25, 0.25)
    c0 = round(o0 + 0.9, 2)
    for k, nm in enumerate(("3", "2", "1")):
        T(f'tl.set("#cd", {{textContent:"{nm}", opacity:1}}, {c0 + k:.2f});'); T(f'tl.fromTo("#cd", {{scale:1.4}}, {{scale:1, duration:0.35, ease:"power3.out"}}, {c0 + k:.2f});')
        snd("click.wav", c0 + k, 0.5)
    T(f'tl.to("#cd", {{opacity:0, duration:0.2, ease:"power2.in"}}, {L["b6"] - 0.15:.2f});')
    T(f'tl.to("#op1", {{backgroundColor:"{GOLD}", scale:1.08, duration:0.35, ease:"back.out(1.4)"}}, {L["b6"]:.2f});'); snd("shimmer.wav", L["b6"], 0.4, 1.2)
    T(f'tl.to(["#op0", "#op2"], {{opacity:0.35, duration:0.3, ease:"power2.in"}}, {L["b6"]:.2f});')
    T(f'tl.fromTo("#awn i", {{scaleY:0}}, {{scaleY:1, duration:0.35, stagger:0.06, ease:"back.out(1.4)", transformOrigin:"50% 0%"}}, {at("b6", "place") - 0.1:.2f});')
    # 8 · "so every coffee you order is a little bit of Arabic. How do you take yours? Comment below!"
    S8 = L["end"] - 0.1; scene("#s8", S8, None)
    IN("#ecup", L["end"] + 0.05, 50); POP("#etag", at("end", "arabic") - 0.1); snd("tick-lo.wav", at("end", "arabic"), 0.4)
    IN("#ask", at("end", "how") - 0.1, 30)
    for i in range(3): POP(f"#tk{i}", at("end", "yours") + i * 0.2, 0.8); snd("tap.wav", at("end", "yours") + i * 0.2, 0.25)
    POP("#url", at("end", "comment"), 0.8); snd("tick-lo.wav", at("end", "comment"), 0.5)
    T(f'tl.fromTo("#arr", {{y:0}}, {{y:18, duration:0.4, yoyo:true, repeat:5, ease:"sine.inOut"}}, {at("end", "comment"):.2f});')

    # captions: the line being said, word by word, small under the picture
    caps = ""; k = 0
    for n in L:
        if n in ARABIC: continue
        ws = words(n); chunk = []
        for i, (w, s, e) in enumerate(ws):
            chunk.append((w, s))
            if w[-1] in ",.:?!" or len(chunk) >= 6 or i + 1 == len(ws):
                nxt = L[n] + ws[i + 1][1] if i + 1 < len(ws) else L[n] + e + 0.4
                caps += f'<div class="cap" id="cp{k}">' + " ".join(f'<span id="cp{k}w{j}">{x}</span>' for j, (x, _) in enumerate(chunk)) + "</div>"
                T(f'tl.set("#cp{k}", {{opacity:1}}, {L[n] + chunk[0][1] - 0.02:.2f});')
                for j, (x, s0) in enumerate(chunk): T(f'tl.fromTo("#cp{k}w{j}", {{opacity:0, y:10}}, {{opacity:1, y:0, duration:0.2, ease:"power3.out"}}, {L[n] + s0:.2f});')
                T(f'tl.to("#cp{k}", {{opacity:0, duration:0.15, ease:"power2.in"}}, {nxt - 0.18:.2f});'); k += 1; chunk = []

    blobs = "".join(f'<i class="blob" style="left:{x}px;top:{y}px;width:{r}px;height:{r}px;background:{c}"></i>' for x, y, r, c in
                    ((-200, -150, 700, "#f4d9c6"), (600, 200, 600, "#cfe5dc"), (-150, 1100, 650, "#f6e3b4"), (650, 1300, 600, "#e8d5e6")))
    CUP = lambda: (f'<path d="M380 980 L 400 1200 C 405 1240, 435 1260, 470 1260 L 610 1260 C 645 1260, 675 1240, 680 1200 L 700 980 Z" fill="#fff" stroke="{INK}" stroke-width="10" stroke-linejoin="round"/>'
                   f'<path d="M700 1030 C 780 1030, 790 1140, 690 1160" fill="none" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>'
                   f'<path d="M392 1010 L 688 1010" stroke="{BROWN}" stroke-width="22"/><ellipse cx="540" cy="1290" rx="230" ry="26" fill="#fff" stroke="{INK}" stroke-width="9"/>')
    GLASS = lambda liq="": (f'<path d="M420 880 C 420 1060, 660 1060, 660 880 Z" fill="#fff" stroke="{INK}" stroke-width="10" stroke-linejoin="round"/>{liq}'
                            f'<path d="M540 1040 L 540 1220 M 450 1230 L 630 1230" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>')
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
.op {{ display:flex; align-items:center; justify-content:center; gap:20px; width:640px; margin:18px auto 0; padding:20px; border-radius:26px; background:#fff; font-size:52px; box-shadow:0 12px 30px -16px rgba(23,38,43,.45); opacity:0; }}
.op i {{ font-style:normal; font-size:56px; }}
#cd {{ position:absolute; left:0; right:0; top:1290px; text-align:center; font-size:130px; font-weight:700; color:{RED}; opacity:0; }}
.pin {{ opacity:0; }} .pin text {{ font-family:FR; font-weight:700; font-size:44px; fill:{INK}; }}
#stars i {{ position:absolute; width:12px; height:12px; border-radius:50%; background:#fff6d8; opacity:0; }}
#awn {{ position:absolute; left:360px; top:0; width:330px; height:46px; display:flex; }} #awn i {{ flex:1; height:46px; border-radius:0 0 18px 18px; }}
"""
    stars = "".join(f'<i style="left:{x}px;top:{y}px"></i>' for x, y in ((80, 60), (210, 120), (330, 50), (450, 140), (560, 70), (140, 210), (500, 230)))
    beans = "".join(f'<ellipse class="bean" cx="{x}" cy="1000" rx="20" ry="28" fill="{BROWN}" stroke="{INK}" stroke-width="5" opacity="0"/>' for x in (500, 545, 590, 540))
    PIN = lambda id, x, y, name, dx=30: (f'<g class="pin" id="{id}" style="transform-origin:{x}px {y}px"><circle cx="{x}" cy="{y}" r="22" fill="{RED}" stroke="{INK}" stroke-width="6"/>'
                                         f'<text x="{x + dx}" y="{y + 14}" text-anchor="{"start" if dx > 0 else "end"}">{name}</text></g>')
    body = f"""{blobs}
<div id="logo"><span class="tile"><span>ر</span><em></em></span><b>رَفِيق</b></div>
<div class="sc" id="s1">
 <div class="t" style="top:250px;font-size:72px;line-height:1.2;opacity:1">The Arabic word for<br><b id="k1w" style="display:inline-block;font-size:130px;color:{TEAL}">coffee</b><br>used to mean…</div>
 <div class="t" id="k1b" style="top:660px;font-size:120px;color:{RED}">wine?!</div>
 <svg class="full" viewBox="0 0 1080 1920">
  <g id="cup">{CUP()}<path class="ln steam" pathLength="1" d="M470 950 C 440 900, 500 870, 470 820" style="stroke-width:8;stroke:#9aa"/><path class="ln steam" pathLength="1" d="M560 950 C 530 900, 590 870, 560 820" style="stroke-width:8;stroke:#9aa"/><path class="ln steam" pathLength="1" d="M640 950 C 610 900, 670 870, 640 820" style="stroke-width:8;stroke:#9aa"/></g>
  <g id="glass" style="opacity:0;transform-origin:540px 1100px">{GLASS(f'<path id="wineL" d="M430 930 C 440 1040, 640 1040, 650 930 Z" fill="{RED}"/>')}</g>
 </svg>
</div>
<div class="sc" id="s2">
 <div class="t ar" id="qw" style="top:170px;font-size:220px;line-height:1.4;color:{RED}">قَهْوَة</div>
 <div id="dict" style="position:absolute;left:290px;top:620px;width:500px;height:330px;opacity:0;perspective:1200px">
  <div style="position:absolute;left:0;top:0;width:250px;height:330px;background:#fff;border:8px solid {INK};border-radius:16px 0 0 16px;padding:40px 26px">
   {''.join(f'<div style="height:10px;margin:18px 0;border-radius:5px;background:#c9c2b4;width:{w}%"></div>' for w in (90, 70, 85, 60, 80))}</div>
  <div style="position:absolute;left:250px;top:0;width:250px;height:330px;background:#fff;border:8px solid {INK};border-radius:0 16px 16px 0;text-align:center;padding-top:28px">
   <div class="ar" style="font-size:64px;color:{RED}">قَهْوَة</div>
   <svg id="dglass" viewBox="380 860 320 400" width="120" style="opacity:0;margin-top:6px">{GLASS(f'<path d="M430 930 C 440 1040, 640 1040, 650 930 Z" fill="{RED}"/>')}</svg></div>
  <div id="dictR" style="position:absolute;left:250px;top:0;width:250px;height:330px;background:{BROWN};border:8px solid {INK};border-radius:0 16px 16px 0;backface-visibility:hidden;color:{GOLD};font-family:SE;font-style:italic;font-size:44px;display:grid;place-items:center;text-align:center">Lisān<br>al-ʿArab</div>
 </div>
 <svg id="plate" class="full" viewBox="0 0 1080 1920" style="opacity:0"><ellipse cx="540" cy="1170" rx="230" ry="90" fill="#fff" stroke="{INK}" stroke-width="10"/><ellipse cx="540" cy="1160" rx="140" ry="48" fill="none" stroke="#c9c2b4" stroke-width="8"/>
  <path d="M500 1150 C 520 1120, 580 1120, 590 1150" fill="#e7a35a" stroke="{INK}" stroke-width="6"/><path d="M270 1080 L 270 1240 M 810 1080 L 810 1240" stroke="{INK}" stroke-width="12" stroke-linecap="round"/></svg>
 <div class="t" id="k2p" style="top:1320px;font-size:56px"><span class="pill">takes away your <b style="color:{RED}">appetite</b></span></div>
</div>
<div class="sc" id="s3">
 <div id="win" style="position:absolute;left:190px;top:240px;width:700px;height:620px;border-radius:350px 350px 30px 30px;background:{NIGHT};border:10px solid {INK};overflow:hidden;opacity:0">
  <div id="stars">{stars}</div>
  <svg id="moon" viewBox="0 0 100 100" width="130" style="position:absolute;right:90px;top:70px;opacity:0"><path d="M60 10 A 40 40 0 1 0 90 70 A 32 32 0 1 1 60 10 Z" fill="{GOLD}"/></svg>
  <div class="t" id="yrsl" style="top:250px;font-size:56px;color:#fff"><b id="yrs" style="font-size:140px;color:{GOLD}">1000</b>s</div>
  <div class="t" id="yemen" style="top:470px;font-size:52px"><span class="pill">Yemen</span></div>
  <svg id="mat" viewBox="0 0 200 300" width="200" style="position:absolute;right:40px;bottom:-10px;opacity:0"><path d="M20 300 L 20 90 C 20 20, 180 20, 180 90 L 180 300 Z" fill="{TEAL}" stroke="{INK}" stroke-width="8"/><path d="M45 290 L 45 100 C 45 50, 155 50, 155 100 L 155 290 Z" fill="none" stroke="{GOLD}" stroke-width="6"/></svg>
 </div>
 <svg class="full" viewBox="0 0 1080 1920">
  {beans}
  <g id="pot" style="opacity:0"><path d="M420 1060 C 400 1180, 420 1290, 470 1320 L 650 1320 C 700 1290, 720 1180, 680 1060 Z" fill="#fff" stroke="{INK}" stroke-width="10"/>
   <clipPath id="potc"><path d="M420 1060 C 400 1180, 420 1290, 470 1320 L 650 1320 C 700 1290, 720 1180, 680 1060 Z"/></clipPath>
   <g clip-path="url(#potc)"><rect id="brew" x="390" y="1120" width="320" height="210" fill="{BROWN}"/></g>
   <path d="M680 1100 C 760 1080, 790 1020, 820 990" fill="none" stroke="{INK}" stroke-width="10" stroke-linecap="round"/><path d="M430 1060 L 670 1060" stroke="{INK}" stroke-width="10"/></g>
  <g id="eye" style="opacity:0;transform-origin:860px 1200px"><path d="M770 1200 C 810 1150, 910 1150, 950 1200 C 910 1250, 810 1250, 770 1200 Z" fill="#fff" stroke="{INK}" stroke-width="8"/><circle cx="860" cy="1200" r="22" fill="{INK}"/>
   <path id="lid" d="M770 1200 C 810 1150, 910 1150, 950 1200 C 910 1250, 810 1250, 770 1200 Z" fill="{CREAM}" stroke="{INK}" stroke-width="8"/></g>
 </svg>
</div>
<div class="sc" id="s4">
 <svg class="full" viewBox="0 0 1080 1920">
  <g id="oglass" style="opacity:0" transform="translate(-260,0)">{GLASS(f'<path d="M430 930 C 440 1040, 640 1040, 650 930 Z" fill="{RED}"/>')}</g>
  <path id="ox" class="ln" pathLength="1" d="M180 870 L 380 1080 M 380 870 L 180 1080" style="stroke:{RED};stroke-width:14" transform="translate(0,0)"/>
  <g id="ocup" style="opacity:0;transform-origin:800px 1120px" transform="translate(260,-80)">{CUP()}</g>
 </svg>
 <div class="t" id="tag" style="top:560px;left:40px;right:auto;width:480px;font-size:80px;opacity:0"><span class="pill ar" style="color:{RED}">قَهْوَة</span></div>
</div>
<div class="sc" id="s5">
 <div id="mapcam" style="position:absolute;inset:0">
 <svg class="full" viewBox="0 0 1080 1920" id="map" style="opacity:0">
  <path d="M60 760 C 200 700, 420 720, 560 760 C 700 800, 820 760, 1000 800 L 1000 900 C 820 880, 660 930, 520 900 C 380 880, 200 900, 60 860 Z" fill="#cfe0ea" stroke="{BLUE}" stroke-width="6"/>
  <path d="M470 960 C 540 1080, 640 1240, 760 1420 L 800 1400 C 690 1220, 590 1060, 520 950 Z" fill="#cfe0ea" stroke="{BLUE}" stroke-width="6"/>
  <path d="M100 160 C 300 120, 400 260, 560 300 L 560 380 C 400 360, 260 420, 100 400 Z" fill="#cfe0ea" stroke="{BLUE}" stroke-width="6" transform="translate(0,-380)"/>
  <path id="r1" class="ln" pathLength="1" d="M800 1460 C 760 1360, 720 1300, 690 1250" style="stroke:{RED};stroke-dasharray:1;stroke-width:8"/>
  <path id="r2" class="ln" pathLength="1" d="M690 1250 C 620 1180, 520 1110, 450 1040" style="stroke:{RED};stroke-width:8"/>
  <path id="r3" class="ln" pathLength="1" d="M450 1040 C 520 920, 600 760, 680 660" style="stroke:{RED};stroke-width:8"/>
  <path id="r5" class="ln" pathLength="1" d="M680 660 C 560 800, 300 860, 160 760 C 80 600, 200 300, 360 0" style="stroke:{TEAL};stroke-width:8"/>
  <path id="r6" class="ln" pathLength="1" d="M360 0 C 300 -40, 240 -60, 170 -60" style="stroke:{TEAL};stroke-width:8"/>
  {PIN("pY", 800, 1460, "Yemen")}{PIN("pM", 690, 1250, "Makkah")}{PIN("pC", 450, 1040, "Cairo", -30)}{PIN("pI", 680, 660, "Istanbul")}
  {PIN("pA", 360, 0, "Amsterdam")}{PIN("pL", 170, -60, "London", 30)}
  <g id="ship"><g id="shipi" style="opacity:0"><path d="M-60 0 L 60 0 L 40 30 L -40 30 Z" fill="{BROWN}" stroke="{INK}" stroke-width="6"/><path d="M0 0 L 0 -80 L 50 -10 Z" fill="#fff" stroke="{INK}" stroke-width="6"/></g></g>
 </svg>
 <div class="t" id="kahve" style="top:560px;left:560px;right:auto;font-size:64px"><span class="pill" style="color:{RED}">kahve</span></div>
 <div class="t" id="koffie" style="top:-110px;left:420px;right:auto;font-size:64px"><span class="pill" style="color:{TEAL}">koffie</span></div>
 <div class="t" id="y1582" style="top:-250px;font-size:64px">by <b id="n1582" style="color:{RED}">1500</b></div>
 </div>
 <div class="t" id="coffee" style="top:1180px;font-size:150px;color:{TEAL}"><span class="pill" style="padding:0 50px">coffee</span></div>
</div>
<div class="sc" id="s7">
 <div class="t" id="yt" style="top:190px;font-size:64px;color:{TEAL}">Your turn</div>
 <div id="msjbox" style="position:absolute;left:0;right:0;top:300px">
  <div class="t ar" id="msj" style="position:relative;font-size:150px;line-height:1.4;color:{INK}"><span class="m">مَـ</span>سْجِد</div>
  <div class="t" id="msjl" style="position:relative;font-size:50px">the <b style="color:{GOLD}">place</b> of sujood</div></div>
 <div class="t ar" id="mq" style="top:420px;font-size:190px;line-height:1.4;color:{RED}"><span class="m">مَـ</span>قْهى</div>
 <div style="position:absolute;left:0;right:0;top:780px">
  <div class="op" id="op0"><i>🫖</i>a coffee pot</div>
  <div class="op" id="op1" style="position:relative"><div id="awn">{''.join(f'<i style="background:{c}"></i>' for c in (RED, "#fff", RED, "#fff", RED, "#fff"))}</div><i>☕</i>a café</div>
  <div class="op" id="op2"><i>🫘</i>a coffee bean</div></div>
 <div id="cd">3</div>
</div>
<div class="sc" id="s8">
 <div id="ecup" style="position:absolute;left:0;top:-420px;opacity:0"><svg class="full" viewBox="0 0 1080 1920">{CUP()}</svg></div>
 <div class="t" id="etag" style="top:430px;font-size:70px"><span class="pill ar" style="color:{RED}">قَهْوَة</span></div>
 <div class="t" id="ask" style="top:960px;font-size:84px;line-height:1.15">How do you<br>take yours?</div>
 <div style="position:absolute;left:0;right:0;top:1200px;display:flex;justify-content:center;gap:20px">
  {''.join(f'<span class="pill" id="tk{i}" style="font-size:46px;opacity:0">{x}</span>' for i, x in enumerate(("black", "with milk", "with sugar")))}</div>
 <div class="t" id="url" style="top:1340px;font-size:52px"><span class="pill" style="background:{TEAL};color:#fff">rafiq-arabic.com</span></div>
 <svg class="full" viewBox="0 0 1080 1920"><path id="arr" d="M540 1440 L 540 1520 M 495 1480 L 540 1525 L 585 1480" fill="none" stroke="{RED}" stroke-width="10" stroke-linecap="round" opacity="0"/></svg>
</div>
{caps}"""
    T(f'tl.fromTo("#arr", {{opacity:0}}, {{opacity:1, duration:0.3, ease:"power3.out"}}, {at("end", "comment"):.2f});')
    open(os.path.join(out, "index.html"), "w").write(f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" /><title>coffee</title>
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
