#!/usr/bin/env python3
"""h4-khutbah in the new format (owner, 30 Oct 2026, #310: "edit it with interesting graphics"): the same lines
(brag-quiz/voice/khutbah-lines.json) told with full-screen drawings over a Friday city at dusk (domes and minarets, a crescent, lanterns),
Cinzel for the titles and Amiri for the Arabic, every move on its word, eased as MOTION-STYLE.md says:
  1 "The imam giving your Friday khutbah… and your fiancé…": the minbar and its imam, FRIDAY, the ring; "same name": =; "Arabic": خَطِيب
  2 خَطِيب (Rafiq) · "the one who gives the khutbah… and also, your fiancé": the preacher and the fiancé either side of the word
  3 "Both come from khataba: to address": خ ط ب fall in; the imam's voice reaches the rows; a suitor speaks to a family at their door
  4 خُطْبَة / خِطْبَة (Rafiq) · "one small mark": the lens; the ḍamma lit for the sermon, the kasra for the proposal
  5 your turn: al-Baqarah 2:235, sermon or proposal? the lens on the first letter, 3-2-1; the ayah (Rafiq), "A PROPOSAL!", the kasra lit
  6 the ask: the mosque at Jumuʿah, a paper plane to the rings, rafiq-arabic.com. Then the cream end card.
Figures are faceless (owner, 27 Oct).

  python3 brag-quiz/reels/khutbah/build.py    then  cd brag-quiz/reels/khutbah/out/v && npx hyperframes render -o ../raw.mp4
"""
import json, os, re, shutil, subprocess
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
V6 = os.path.join(ROOT, "brag-output-v6/composition/assets"); VO = os.path.join(ROOT, "brag-quiz/voice/khutbah")
INK, CREAM, GOLD, TEAL, RED, WOOD = "#17262B", "#F6EBD3", "#F2C46B", "#2E7263", "#B4322A", "#8A5A2B"
dur = lambda f: float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))
mp3 = lambda n: os.path.join(VO, n + ".mp3")
def words(n):
    ws = json.load(open(os.path.join(VO, n + ".words.json")))
    return [(w[0], w[1], w[2] if len(w) > 2 else (ws[i + 1][1] if i + 1 < len(ws) else w[1] + 0.45)) for i, w in enumerate(ws)]
ORDER = [("h1", 0.3), ("khatib", 0.35), ("b1", 0.25), ("b2", 0.45), ("b3", 0.5), ("khutba", 0.15), ("khitba", 0.3), ("b3b", 0.35),
         ("t1", 0.55), ("ayah", 3.9), ("b4", 0.2), ("end", 0.8)]                                   # the ayah waits for the 3-2-1
ARABIC = ("khatib", "khutba", "khitba", "ayah")
def spoken(n):
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", mp3(n), "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout, np.int16) / 32768
    e = 20 * np.log10(np.sqrt(np.convolve(x ** 2, np.ones(160) / 160, "same")) + 1e-9)
    return np.where(e > -45)[0][-1] / 16000 + 0.05
L, t = {}, 0.0
for n, g in ORDER: t += g; L[n] = round(t, 2); t += spoken(n)
END = round(t + 0.9, 2)
def at(n, key, last=False):
    hits = [s for w, s, e in words(n) if key in re.sub(r"[^a-z0-9']", "", w.lower().replace("é", "e"))]
    return round(L[n] + (hits[-1] if last else hits[0]), 2)

def figure(x, y, s, c, cls="", turban=None, arm=False):         # a faceless robed figure standing at (x, y)
    t = f'<circle cx="0" cy="-172" r="30" fill="{turban}"/>' if turban else ""
    a = f'<path class="arm" d="M18 -120 L 58 -150" stroke="{c}" stroke-width="16" stroke-linecap="round"/>' if arm else ""
    return (f'<g class="{cls}" transform="translate({x},{y}) scale({s})"><path d="M-44 0 C -40 -80 -32 -126 0 -140 C 32 -126 40 -80 44 0 Z" fill="{c}"/>'
            f'<circle cx="0" cy="-160" r="26" fill="{c}"/>{t}{a}</g>')
def minbar(x, y, s, id=""):                                   # the stepped pulpit, its little dome, and the imam on the top step
    return (f'<g id="{id}" transform="translate({x},{y}) scale({s})">'
            f'<path d="M0 300 L0 250 L45 250 L45 200 L90 200 L90 150 L135 150 L135 100 L180 100 L180 300 Z" fill="{WOOD}" stroke="{GOLD}" stroke-width="6" stroke-linejoin="round"/>'
            f'<path d="M180 300 L180 -10 M250 300 L250 -10" stroke="{GOLD}" stroke-width="8"/><rect x="180" y="100" width="70" height="200" fill="{WOOD}" stroke="{GOLD}" stroke-width="6"/>'
            f'<path d="M172 -10 L258 -10 C 258 -60 172 -60 172 -10 Z" fill="{GOLD}"/><path d="M215 -52 L215 -76" stroke="{GOLD}" stroke-width="5"/><circle cx="215" cy="-80" r="6" fill="{GOLD}"/>'
            + figure(215, 100, 0.62, CREAM, turban="#ffffff", arm=True) + '</g>')
def ring(x, y, s, id=""):
    return (f'<g id="{id}" transform="translate({x},{y}) scale({s})"><circle cx="0" cy="0" r="58" fill="none" stroke="{GOLD}" stroke-width="16"/>'
            f'<path d="M-30 -66 L -16 -96 L 16 -96 L 30 -66 L 0 -40 Z" fill="#dff3f0" stroke="#ffffff" stroke-width="4" stroke-linejoin="round"/>'
            f'<path d="M-16 -96 L 0 -66 L 16 -96 M -30 -66 L 30 -66" stroke="#9fd3cc" stroke-width="3" fill="none"/></g>')
def sparkle(x, y, s, cls):
    return f'<path class="{cls}" transform="translate({x},{y}) scale({s})" d="M0 -30 C 4 -6 6 -4 30 0 C 6 4 4 6 0 30 C -4 6 -6 4 -30 0 C -6 -4 -4 -6 0 -30 Z" fill="#fff6dc"/>'
LENS = (f'<svg width="260" height="260" viewBox="0 0 260 260"><circle cx="110" cy="110" r="88" fill="rgba(246,235,211,.15)" stroke="{GOLD}" stroke-width="16"/>'
        f'<path d="M176 176 L 244 244" stroke="{WOOD}" stroke-width="30" stroke-linecap="round"/><path d="M60 70 C 70 55 85 48 100 46" stroke="#fff" stroke-width="8" stroke-linecap="round" fill="none" opacity=".6"/></svg>')

def build():
    out = os.path.join(HERE, "out", "v"); a = os.path.join(out, "assets")
    if os.path.exists(out): shutil.rmtree(out)
    os.makedirs(a)
    for f in ("karla-latin-700-normal.woff2",): shutil.copy(os.path.join(V6, "fonts", f), a)
    for f in ("cinzel-latin-700-normal.woff2", "amiri-arabic-700-normal.woff2"): shutil.copy(os.path.join(ROOT, "brag-quiz/fonts", f), a)
    shutil.copy(os.path.join(V6, "lib/gsap.min.js"), a)
    for f in ("shimmer.wav", "tick-lo.wav", "thump.wav", "whoosh.wav", "impact.wav", "drone.wav", "flip.wav"): shutil.copy(os.path.join(ROOT, "brag-quiz/sfx/soft", f), a)
    for f in ("click.wav", "swoosh.wav", "tap.wav"): shutil.copy(os.path.join(ROOT, "brag-quiz/sfx/ref", f), a)
    lv = lambda f: float(re.findall(r"I:\s+(-?[\d.]+) LUFS", subprocess.run(["ffmpeg", "-i", f, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr)[-1])
    target = lv(mp3("b4"))                                                   # Rafiq's Arabic level with Callum (the standard)
    for n in L:
        if n in ARABIC: subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp3(n), "-af", f"volume={target - lv(mp3(n)):.1f}dB,alimiter=limit=0.95", os.path.join(a, n + ".mp3")], check=True)
        else: shutil.copy(mp3(n), a)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-i", os.path.join(a, "drone.wav"), "-af",
                    f"atrim=0:{END},afade=t=in:d=0.6,afade=t=out:st={END - 0.4}:d=0.4", "-c:a", "libmp3lame", "-q:a", "3", os.path.join(a, "bed.mp3")], check=True)
    au = []
    def snd(name, t0, vol, d=None, track=None):
        d = d or dur(os.path.join(a, name))
        au.append(f'<audio id="s{len(au)}" src="assets/{name}" data-start="{max(0, t0):.3f}" data-duration="{d:.3f}" data-volume="{vol:.3f}" data-track-index="{track or 3 + len(au)}"></audio>')
    for n, t0 in L.items(): snd(f"{n}.mp3", t0, 1.0, track=1)
    snd("bed.mp3", 0, 0.07, END, track=2)                                   # a low hum under it all
    js = []; T = js.append
    IN = lambda sel, t, y=40, d=0.5: T(f'tl.fromTo("{sel}", {{opacity:0, y:{y}}}, {{opacity:1, y:0, duration:{d}, ease:"power3.out"}}, {t:.2f});')
    POP = lambda sel, t, s=0.6: T(f'tl.fromTo("{sel}", {{opacity:0, scale:{s}}}, {{opacity:1, scale:1, duration:0.45, ease:"back.out(1.4)", transformOrigin:"50% 50%"}}, {t:.2f});')
    OUT = lambda sel, t, y=-40: T(f'tl.to("{sel}", {{opacity:0, y:{y}, duration:0.3, ease:"power2.in"}}, {t:.2f});')
    def draw(sel, t, d=0.6): T(f'tl.fromTo("{sel}", {{strokeDashoffset:1}}, {{strokeDashoffset:0, duration:{d}, stagger:0.12, ease:"power2.inOut"}}, {t:.2f});')
    def pulse(sel, t, s=1.08): T(f'tl.fromTo("{sel}", {{scale:1}}, {{scale:{s}, duration:0.2, yoyo:true, repeat:1, ease:"power2.out", transformOrigin:"50% 50%", immediateRender:false}}, {t:.2f});')
    def scene(sel, t0, t1):
        if t0 > 0: T(f'tl.fromTo("{sel}", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.45, ease:"power3.out"}}, {t0:.2f});')
        if t1: T(f'tl.to("{sel}", {{opacity:0, y:-60, duration:0.35, ease:"power2.in"}}, {t1:.2f});'); snd("whoosh.wav", t1 - 0.05, 0.3)

    # the city lives the whole time: the lanterns sway, the stars drift, the crescent rises a little
    T(f'tl.fromTo(".lan", {{rotation:-5}}, {{rotation:5, duration:1.6, yoyo:true, repeat:{int(END / 1.6)}, stagger:0.3, ease:"sine.inOut", svgOrigin:"0 0"}}, 0);')
    T(f'tl.fromTo("#stars", {{x:0}}, {{x:-120, duration:{END:.2f}, ease:"sine.inOut"}}, 0);')
    T(f'tl.fromTo("#moon", {{y:30}}, {{y:-30, duration:{END:.2f}, ease:"sine.inOut"}}, 0);')

    # 1 · the hook
    POP("#mb1", at("h1", "imam") - 0.1, 0.7); snd("thump.wav", at("h1", "imam"), 0.35)
    POP("#fri", at("h1", "friday") - 0.05, 0.7); snd("tap.wav", at("h1", "friday"), 0.35)
    draw("#s1 .wave", at("h1", "khutbah") - 0.1, 0.5)
    fi = at("h1", "fiance")
    POP("#rg1", fi - 0.1, 0.4); snd("shimmer.wav", fi, 0.35, 1.2)
    T(f'tl.fromTo("#s1 .spk", {{opacity:0, scale:0}}, {{opacity:1, scale:1, duration:0.4, stagger:0.1, ease:"back.out(1.4)", transformOrigin:"50% 50%"}}, {fi + 0.15:.2f});')
    sm = at("h1", "same")
    POP("#eq", sm - 0.05, 0.4); snd("tick-lo.wav", sm, 0.45)
    ab = at("h1", "arabic")
    T(f'tl.fromTo("#ttl", {{opacity:0, scale:1.6}}, {{opacity:1, scale:1, duration:0.45, ease:"back.out(1.4)"}}, {ab - 0.05:.2f});'); snd("impact.wav", ab, 0.4, 1.2)
    OUT("#kick", ab - 0.1)
    S2 = L["khatib"] - 0.25; scene("#s1", 0, S2 - 0.05)
    # 2 · خَطِيب: the preacher and the fiancé
    scene("#s2", S2, L["b2"] - 0.35)
    POP("#kw", L["khatib"] - 0.05, 0.7); snd("tick-lo.wav", L["khatib"], 0.4)
    IN("#kt", L["b1"], 20)
    kb = at("b1", "khutbah")
    draw("#ar0", kb - 0.25, 0.4); POP("#mb2", kb - 0.05, 0.6); POP("#lp0", kb + 0.2, 0.7); snd("thump.wav", kb, 0.35)
    fn = at("b1", "fiance")
    draw("#ar1", fn - 0.25, 0.4); POP("#rg2", fn - 0.05, 0.4); POP("#lp1", fn + 0.2, 0.7); snd("shimmer.wav", fn, 0.35, 1.2)
    T(f'tl.fromTo("#rg2", {{rotation:0}}, {{rotation:12, duration:0.12, yoyo:true, repeat:3, ease:"sine.inOut", immediateRender:false, svgOrigin:"0 0"}}, {fn + 0.45:.2f});')
    # 3 · خ ط ب: to address; the imam and the people, a suitor and a family
    S3 = L["b2"] - 0.1; scene("#s3", S3, L["b3"] - 0.35)
    kh = at("b2", "khataba")
    for i in range(3):
        T(f'tl.fromTo("#rt{i}", {{opacity:0, y:-260}}, {{opacity:1, y:0, duration:0.4, ease:"power3.out"}}, {kh - 0.25 + i * 0.16:.2f});'); snd("thump.wav", kh - 0.05 + i * 0.16, 0.3)
    POP("#addr", at("b2", "address") - 0.05, 0.7); snd("tap.wav", at("b2", "address"), 0.35)
    im = at("b2", "imam")
    IN("#band0", im - 0.15, 40)
    pe = at("b2", "people")
    draw("#band0 .wave", at("b2", "addresses") - 0.05, 0.6); snd("swoosh.wav", at("b2", "addresses"), 0.3)
    T(f'tl.fromTo("#band0 .sit", {{y:0}}, {{y:-14, duration:0.18, yoyo:true, repeat:1, stagger:0.05, ease:"power2.out", immediateRender:false}}, {pe:.2f});')
    POP("#bl0", pe + 0.1, 0.7)
    su = at("b2", "suitor")
    IN("#band1", su - 0.15, 40); snd("tap.wav", su, 0.35)
    ad2 = at("b2", "addresses", last=True)
    POP("#bub", ad2, 0.4); snd("tick-lo.wav", ad2, 0.4)
    fa = at("b2", "family")
    T(f'tl.fromTo("#band1 .fam", {{y:0}}, {{y:-14, duration:0.18, yoyo:true, repeat:1, stagger:0.06, ease:"power2.out", immediateRender:false}}, {fa:.2f});')
    POP("#bl1", fa + 0.1, 0.7)
    # 4 · خُطْبَة and خِطْبَة: one mark apart
    S4 = L["b3"] - 0.1; scene("#s4", S4, L["t1"] - 0.4)
    IN("#same", L["b3"] + 0.1, 20)
    POP("#w0", L["khutba"] - 0.05, 0.7); snd("tick-lo.wav", L["khutba"], 0.4)
    POP("#w1", L["khitba"] - 0.05, 0.7); snd("tick-lo.wav", L["khitba"], 0.4)
    OUT("#same", L["b3b"] - 0.1)
    mk = at("b3b", "mark")
    T(f'tl.fromTo("#lens", {{opacity:0, x:-500, y:300}}, {{opacity:1, x:0, y:0, duration:0.6, ease:"power3.out"}}, {mk - 0.3:.2f});'); snd("whoosh.wav", mk - 0.3, 0.3)
    T(f'tl.to("#lens", {{opacity:0, scale:0.6, duration:0.3, ease:"power2.in"}}, {at("b3b", "damma") - 0.3:.2f});')
    dm = at("b3b", "damma")
    draw("#c0", dm - 0.05, 0.4); snd("tap.wav", dm, 0.45)
    se = at("b3b", "sermon"); POP("#l0", se - 0.05, 0.7); snd("thump.wav", se, 0.3)
    ks = at("b3b", "kasra")
    draw("#c1", ks - 0.05, 0.4); snd("tap.wav", ks, 0.45)
    pr = at("b3b", "proposal"); POP("#l1", pr - 0.05, 0.7); snd("shimmer.wav", pr, 0.35, 1.2)
    # 5 · your turn: al-Baqarah 2:235; sermon or proposal? 3-2-1; the ayah; A PROPOSAL!
    S5 = L["t1"] - 0.1; scene("#s5", S5, L["end"] - 0.45)
    IN("#yt", L["t1"], 20)
    POP("#aya", at("t1", "baqarah") - 0.1, 0.8); snd("flip.wav", at("t1", "baqarah"), 0.4)
    sr = at("t1", "sermon")
    for i in range(2): POP(f"#op{i}", sr - 0.05 + i * 0.6, 0.8); snd("tap.wav", sr + i * 0.6, 0.3)
    lk = at("t1", "mark")
    T(f'tl.fromTo("#lens2", {{opacity:0, x:-400, y:200}}, {{opacity:1, x:0, y:0, duration:0.6, ease:"power3.out"}}, {lk - 0.3:.2f});'); snd("whoosh.wav", lk - 0.3, 0.3)
    pulse("#lens2", at("t1", "first"), 1.12)
    c0 = round(L["t1"] + spoken("t1") + 0.3, 2)
    for k, nm in enumerate(("3", "2", "1")):
        T(f'tl.set("#cd", {{textContent:"{nm}", opacity:1}}, {c0 + k:.2f});'); T(f'tl.fromTo("#cd", {{scale:1.4}}, {{scale:1, duration:0.35, ease:"power3.out"}}, {c0 + k:.2f});')
        snd("click.wav", c0 + k, 1.0); snd("tick-lo.wav", c0 + k, 0.5)
    rv = c0 + 3
    T(f'tl.to("#cd", {{opacity:0, duration:0.2, ease:"power2.in"}}, {rv - 0.1:.2f});')
    T(f'tl.to("#lens2", {{opacity:0, scale:0.6, duration:0.3, ease:"power2.in"}}, {rv - 0.1:.2f});')
    T(f'tl.to("#op1", {{backgroundColor:"{GOLD}", scale:1.08, duration:0.3, ease:"back.out(1.4)"}}, {rv:.2f});'); snd("tick-lo.wav", rv, 0.45)
    T(f'tl.to("#op0", {{opacity:0.3, duration:0.3, ease:"power2.in"}}, {rv:.2f});')
    IN("#aya .ee", L["ayah"] + 0.3, 16)
    hit = at("b4", "proposal")
    T(f'tl.to("#ops", {{opacity:0, y:30, duration:0.25, ease:"power2.in"}}, {hit - 0.25:.2f});')
    T(f'tl.fromTo("#slam", {{opacity:0, scale:1.8}}, {{opacity:1, scale:1, duration:0.45, ease:"back.out(1.7)"}}, {hit:.2f});')   # the one slam
    T(f'tl.fromTo("#cam", {{x:-14}}, {{x:14, duration:0.05, yoyo:true, repeat:7, ease:"sine.inOut", immediateRender:false}}, {hit + 0.05:.2f});')
    T(f'tl.set("#cam", {{x:0}}, {hit + 0.5:.2f});')
    snd("impact.wav", hit - 0.03, 0.75, 1.6)
    T(f'tl.fromTo("#burst i", {{opacity:1, x:0, y:0, scale:0.4}}, {{opacity:0, x:(i) => [-300, -170, 0, 170, 300, -90, 90][i], y:(i) => [-80, -200, -260, -200, -80, 150, 150][i], scale:1.3, duration:0.9, ease:"power2.out"}}, {hit + 0.05:.2f});')
    POP("#rg3", hit + 0.3, 0.4)
    ka = at("b4", "kasra"); draw("#c2", ka - 0.05, 0.4); snd("tap.wav", ka, 0.45)
    # 6 · the ask
    S6 = L["end"] - 0.1; scene("#s6", S6, None)
    draw("#mosque path", L["end"] + 0.05, 0.9); snd("shimmer.wav", L["end"], 0.3, 1.2)
    draw("#s6 .wave", at("end", "listen") + 0.1, 0.6)
    IN("#jm", at("end", "jumuah") - 0.1, 30); snd("tap.wav", at("end", "jumuah"), 0.35)
    sd = at("end", "send")
    POP("#rg4", at("end", "married") - 0.2, 0.5)
    T(f'tl.fromTo("#plane", {{opacity:0, x:-420, y:120, rotation:-10}}, {{opacity:1, x:0, y:0, rotation:0, duration:0.9, ease:"power2.inOut"}}, {sd:.2f});'); snd("swoosh.wav", sd + 0.1, 0.4)
    T(f'tl.to("#plane", {{opacity:0, scale:0.5, duration:0.3, ease:"power2.in"}}, {at("end", "married") + 0.2:.2f});')
    IN("#spot", at("end", "did") - 0.1, 30)
    POP("#url", at("end", "comment"), 0.8); snd("tick-lo.wav", at("end", "comment"), 0.5)
    T(f'tl.fromTo("#arr", {{opacity:0, y:0}}, {{opacity:1, y:18, duration:0.4, yoyo:true, repeat:3, ease:"sine.inOut"}}, {at("end", "comment"):.2f});')

    # captions: the line being said, word by word, at the bottom
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

    rng = np.random.default_rng(7)
    stars = "".join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#fff6dc" opacity="{o:.2f}"/>' for x, y, r, o in
                    zip(rng.uniform(0, 1200, 90), rng.uniform(0, 1100, 90), rng.uniform(1, 3, 90), rng.uniform(0.25, 0.85, 90)))
    def dome(x, w, h, base, c):
        return f'<path d="M{x - w} {base} C {x - w} {base - h} {x - w * 0.15} {base - h * 1.1} {x} {base - h * 1.35} C {x + w * 0.15} {base - h * 1.1} {x + w} {base - h} {x + w} {base} Z" fill="{c}"/>'
    def minaret(x, w, top, c):
        return (f'<rect x="{x - w}" y="{top}" width="{w * 2}" height="{1920 - top}" fill="{c}"/><rect x="{x - w - 10}" y="{top + 60}" width="{w * 2 + 20}" height="14" fill="{c}"/>'
                f'<path d="M{x - w} {top} L {x} {top - 70} L {x + w} {top} Z" fill="{c}"/>')
    city = ("".join(dome(x, w, h, 1560, "#10242a") for x, w, h in ((120, 110, 90), (420, 150, 120), (760, 120, 100), (1010, 100, 80)))
            + minaret(270, 22, 1240, "#10242a") + minaret(920, 18, 1290, "#10242a")
            + '<rect x="-20" y="1540" width="1120" height="400" fill="#10242a"/>'
            + "".join(dome(x, w, h, 1700, "#0b1b20") for x, w, h in ((260, 170, 130), (640, 210, 150), (980, 140, 110)))
            + minaret(470, 26, 1330, "#0b1b20") + '<rect x="-20" y="1690" width="1120" height="260" fill="#0b1b20"/>'
            + "".join(f'<rect x="{x}" y="{y}" width="14" height="22" rx="7" fill="{GOLD}" opacity=".55"/>' for x, y in ((390, 1600), (430, 1600), (600, 1740), (660, 1740), (720, 1740), (880, 1610))))
    lan = "".join(f'<g class="lan" transform="translate({x},0)"><path d="M0 0 L0 {h}" stroke="{GOLD}" stroke-width="3" opacity=".7"/>'
                  f'<g transform="translate(0,{h})"><path d="M-22 0 L 22 0 L 30 46 L 0 70 L -30 46 Z" fill="{GOLD}" opacity=".9"/><path d="M-14 8 L 14 8 L 18 42 L 0 56 L -18 42 Z" fill="#fff1c9"/>'
                  f'<circle cx="0" cy="34" r="54" fill="{GOLD}" opacity=".12"/></g></g>' for x, h in ((70, 120), (1010, 170)))
    seated = "".join(f'<g class="sit" transform="translate({x},{y})"><path d="M-34 40 C -34 0 34 0 34 40 Z" fill="{c}"/><circle cx="0" cy="-12" r="20" fill="{c}"/><circle cx="0" cy="-20" r="16" fill="#ffffff" opacity=".85"/></g>'
                     for x, y, c in [(560 + i * 100, 860, "#3f8a7a") for i in range(5)] + [(610 + i * 100, 960, TEAL) for i in range(4)])
    waves = lambda x, y, n, cls="wave": "".join(f'<path class="{cls}" pathLength="1" d="M{x + i * 40} {y - 50 - i * 22} C {x + 30 + i * 46} {y - 20 - i * 10} {x + 30 + i * 46} {y + 20 + i * 10} {x + i * 40} {y + 50 + i * 22}" fill="none" stroke="{GOLD}" stroke-width="7" stroke-linecap="round" stroke-dasharray="1" stroke-dashoffset="1"/>' for i in range(n))
    arrow = lambda id, d: f'<path id="{id}" pathLength="1" d="{d}" fill="none" stroke="{GOLD}" stroke-width="7" stroke-linecap="round" stroke-dasharray="1" stroke-dashoffset="1"/>'
    circ = lambda id, x, y, r: f'<svg style="position:absolute;left:{x - r - 10}px;top:{y - r - 10}px;overflow:visible" width="{2 * r + 20}" height="{2 * r + 20}"><circle id="{id}" pathLength="1" cx="{r + 10}" cy="{r + 10}" r="{r}" fill="none" stroke="{RED}" stroke-width="8" stroke-dasharray="1" stroke-dashoffset="1" transform="rotate(-90 {r + 10} {r + 10})"/></svg>'
    sv = lambda inner: f'<svg class="full" viewBox="0 0 1080 1920">{inner}</svg>'
    MB_ICON = f'<svg width="60" height="60" viewBox="-10 -90 280 400">{minbar(0, 0, 1)}</svg>'
    RG_ICON = f'<svg width="60" height="60" viewBox="-80 -110 160 190">{ring(0, 0, 1)}</svg>'
    burst = "".join(f'<i style="position:absolute;left:520px;top:1240px;width:40px;height:40px;border-radius:50%;background:{c};opacity:0"></i>' for c in (GOLD, CREAM, RED, GOLD, CREAM, RED, GOLD))
    css = f"""
@font-face {{ font-family:"CZ"; src:url("assets/cinzel-latin-700-normal.woff2"); }}
@font-face {{ font-family:"AM"; src:url("assets/amiri-arabic-700-normal.woff2"); }}
@font-face {{ font-family:"KA"; src:url("assets/karla-latin-700-normal.woff2"); }}
* {{ margin:0; box-sizing:border-box; }} html, body {{ width:1080px; height:1920px; overflow:hidden; background:#000; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; background:linear-gradient(#0e1a22 0%, #17262B 30%, #1d4a48 62%, #6a7a52 80%, #c9a35e 92%); font-family:KA; color:{CREAM}; }}
#cam {{ position:absolute; inset:0; }}
svg.full {{ position:absolute; left:0; top:0; width:1080px; height:1920px; overflow:visible; }}
.sc {{ position:absolute; inset:0; opacity:0; }} #s1 {{ opacity:1; }}
.t {{ position:absolute; left:0; right:0; text-align:center; opacity:0; }}
.cz {{ font-family:CZ; letter-spacing:.06em; color:{GOLD}; text-shadow:0 4px 0 {WOOD}, 0 10px 30px rgba(0,0,0,.5); }}
.am {{ font-family:AM; direction:rtl; color:{CREAM}; text-shadow:0 6px 0 {TEAL}, 0 14px 40px rgba(0,0,0,.45); line-height:1.3; }}
.pill {{ display:inline-flex; align-items:center; gap:14px; padding:8px 30px; border-radius:999px; background:rgba(23,38,43,.85); border:2px solid rgba(242,196,107,.6); font-family:KA; color:{CREAM}; }}
.cap {{ position:absolute; left:70px; right:70px; top:1580px; text-align:center; font-family:KA; font-size:50px; line-height:1.2; color:#fff; text-shadow:0 3px 0 rgba(0,0,0,.6), 0 0 18px rgba(0,0,0,.6); opacity:0; }}
.cap span {{ display:inline-block; opacity:0; }}
.card {{ position:absolute; left:90px; right:90px; padding:26px 30px 22px; border-radius:20px; background:#f3e3c0; color:{INK}; text-align:center; opacity:0;
  box-shadow:0 24px 50px rgba(0,0,0,.4), inset 0 0 0 6px #e3c993, inset 0 0 0 9px {TEAL}; }}
.card .aa {{ font-family:AM; font-size:96px; direction:rtl; line-height:1.6; }} 
.card .ee {{ font-family:CZ; font-size:38px; color:{TEAL}; margin-top:2px; opacity:0; }} .card small {{ display:block; font-size:28px; color:#6b5a44; margin-top:8px; }}
.op {{ display:flex; align-items:center; gap:22px; width:620px; margin:20px auto 0; padding:16px 30px; border-radius:24px; background:rgba(246,235,211,.95); color:{INK}; font-family:CZ; font-size:48px; opacity:0; box-shadow:0 14px 30px rgba(0,0,0,.35); }}
.op svg {{ flex:none; }}
#cd {{ position:absolute; left:0; right:0; top:1200px; text-align:center; font-family:CZ; font-size:150px; color:{GOLD}; opacity:0; text-shadow:0 6px 0 {WOOD}; }}
.tile {{ position:absolute; top:250px; width:190px; height:190px; border-radius:30px; background:{CREAM}; color:{RED}; font-family:AM; font-size:150px; line-height:190px; text-align:center; opacity:0; box-shadow:0 14px 0 {WOOD}, 0 24px 40px rgba(0,0,0,.4); }}
#logo {{ position:absolute; top:70px; left:0; right:0; display:flex; justify-content:center; gap:12px; align-items:center; z-index:5; }}
#logo .tl {{ position:relative; width:58px; height:58px; border-radius:16px; background:{CREAM}; display:grid; place-items:center; }}
#logo .tl span {{ font-family:AM; font-size:38px; color:{INK}; margin-top:-6px; }} #logo .tl em {{ position:absolute; right:9px; top:8px; width:9px; height:9px; border-radius:50%; background:{RED}; }}
#logo b {{ font-family:AM; font-size:44px; color:{CREAM}; }}
"""
    body = f"""<div id="cam">
<svg class="full" viewBox="0 0 1080 1920"><g id="stars">{stars}</g>
 <g id="moon"><circle cx="880" cy="300" r="62" fill="#f6ebd3"/><circle cx="905" cy="282" r="56" fill="#121f27"/></g>
 <circle cx="540" cy="1620" r="520" fill="{GOLD}" opacity=".08"/>{city}{lan}
</svg>
<div id="logo"><span class="tl"><span>ر</span><em></em></span><b>رَفِيق</b></div>
<div class="sc" id="s1">
 <div class="t cz" id="kick" style="top:200px;font-size:44px;opacity:1">THE STORY OF A WORD</div>
 <div class="t am" id="ttl" style="top:180px;font-size:230px;color:{GOLD}">خَطِيب</div>
 {sv(minbar(90, 760, 1.25, "mb1") + waves(430, 720, 3) + ring(800, 960, 1.6, "rg1") + sparkle(700, 820, 1, "spk") + sparkle(930, 790, 0.8, "spk") + sparkle(900, 1110, 0.7, "spk"))}
 <div class="t cz" id="fri" style="top:470px;left:60px;right:auto;width:420px;font-size:56px;color:{CREAM}">FRIDAY</div>
 <div class="t cz" id="eq" style="top:860px;font-size:190px;color:{GOLD}">=</div>
</div>
<div class="sc" id="s2">
 <div class="t am" id="kw" style="top:220px;font-size:260px;color:{GOLD}">خَطِيب</div>
 <div class="t" id="kt" style="top:640px"><span class="pill" style="font-size:46px">khaṭīb</span></div>
 {sv(arrow("ar0", "M440 720 C 360 760 300 800 290 860") + arrow("ar1", "M640 720 C 720 760 780 800 790 900") + minbar(110, 930, 1.0, "mb2") + ring(790, 1080, 1.5, "rg2"))}
 <div class="t" id="lp0" style="top:1290px;left:40px;right:auto;width:500px"><span class="pill" style="font-size:46px;color:{GOLD}">the preacher</span></div>
 <div class="t" id="lp1" style="top:1290px;left:540px;right:auto;width:500px"><span class="pill" style="font-size:46px;color:#ffb3a8">your fiancé</span></div>
</div>
<div class="sc" id="s3">
 <div class="tile" id="rt0" style="left:745px">خ</div><div class="tile" id="rt1" style="left:445px">ط</div><div class="tile" id="rt2" style="left:145px">ب</div>
 <div class="t" id="addr" style="top:480px"><span class="pill" style="font-size:50px">khaṭaba = <b style="color:{GOLD}">to address</b></span></div>
 <div class="t" id="band0" style="top:0;bottom:0">{sv(minbar(70, 700, 0.95) + waves(330, 820, 4) + seated)}
  <div class="t" id="bl0" style="top:1000px"><span class="pill" style="font-size:40px">the imam → <b style="color:{GOLD}">the people</b></span></div></div>
 <div class="t" id="band1" style="top:0;bottom:0">{sv(f'<g transform="translate(660,1180)"><rect x="0" y="0" width="220" height="300" rx="10" fill="#5a3a1e" stroke="{GOLD}" stroke-width="6"/><path d="M0 0 C 0 -110 220 -110 220 0" fill="#5a3a1e" stroke="{GOLD}" stroke-width="6"/><circle cx="185" cy="160" r="9" fill="{GOLD}"/></g>'
     + figure(250, 1480, 1.2, CREAM, arm=True) + '<g class="fam">' + figure(620, 1480, 1.15, "#e7b07a") + '</g><g class="fam">' + figure(760, 1480, 1.2, "#3f8a7a") + '</g><g class="fam">' + figure(900, 1480, 0.8, "#f2c46b") + '</g>')}
  <div id="bub" style="position:absolute;left:300px;top:1150px;padding:6px 26px;border-radius:30px;background:{CREAM};color:{INK};font-family:AM;font-size:56px;opacity:0;box-shadow:0 10px 24px rgba(0,0,0,.35)">السَّلامُ عَلَيْكُم</div>
  <div class="t" id="bl1" style="top:1500px"><span class="pill" style="font-size:40px">a suitor → <b style="color:#ffb3a8">a family</b></span></div></div>
</div>
<div class="sc" id="s4">
 <div class="t cz" id="same" style="top:170px;font-size:48px;color:{CREAM}">ALMOST THE SAME</div>
 <div class="t am" id="w0" style="top:330px;font-size:250px">خُطْبَة</div>
 <div class="t" id="l0" style="top:740px"><span class="pill" style="font-size:50px">{MB_ICON} a sermon</span></div>
 <div class="t am" id="w1" style="top:850px;font-size:250px">خِطْبَة</div>
 <div class="t" id="l1" style="top:1290px"><span class="pill" style="font-size:50px">{RG_ICON} a proposal</span></div>
 {circ("c0", 670, 302, 58)}{circ("c1", 660, 1158, 58)}
 <div id="lens" style="position:absolute;left:545px;top:1010px;opacity:0">{LENS}</div>
</div>
<div class="sc" id="s5">
 <div class="t cz" id="yt" style="top:200px;font-size:76px">YOUR TURN</div>
 <div class="card" id="aya" style="top:330px"><div class="aa">مِنْ خِطْبَةِ النِّساءِ</div><div class="ee">…a proposal to women</div><small>the Qur’an · al-Baqarah 2:235</small></div>
 {circ("c2", 622, 462, 42)}
 <div id="lens2" style="position:absolute;left:510px;top:335px;opacity:0">{LENS}</div>
 <div id="ops" style="position:absolute;left:0;right:0;top:820px"><div class="op" id="op0">{MB_ICON.replace('width="60" height="60"', 'width="70" height="70"')}<span>a sermon</span></div><div class="op" id="op1">{RG_ICON.replace('width="60" height="60"', 'width="70" height="70"')}<span>a proposal</span></div></div>
 <div id="cd">3</div>
 <div class="t cz" id="slam" style="top:850px;font-size:120px;line-height:1.1">A <span style="color:{CREAM}">PROPOSAL</span>!</div>
 {sv(ring(540, 1210, 1.5, "rg3"))}{burst}
</div>
<div class="sc" id="s6">
 {sv('<g id="mosque">' + "".join(f'<path pathLength="1" d="{d}" fill="none" stroke="{GOLD}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="1" stroke-dashoffset="1"/>' for d in (
     "M340 900 L 340 680 C 340 560 450 520 540 470 C 630 520 740 560 740 680 L 740 900", "M540 470 L 540 410 M 520 400 C 535 380 555 380 560 400", "M250 900 L 250 520 L 280 470 L 310 520 L 310 900",
     "M770 900 L 770 520 L 800 470 L 830 520 L 830 900", "M200 900 L 880 900", "M480 900 L 480 780 C 480 730 600 730 600 780 L 600 900")) + '</g>' + waves(880, 700, 3))}
 <div class="t cz" id="jm" style="top:240px;font-size:84px">JUMUʿAH</div>
 <div id="plane" style="position:absolute;left:250px;top:1000px;opacity:0"><svg width="150" height="120" viewBox="0 0 150 120"><path d="M5 60 L 145 5 L 110 115 L 70 78 Z" fill="{CREAM}"/><path d="M70 78 L 145 5 L 60 70 L 60 110 Z" fill="#d9cbae"/></svg></div>
 {sv(ring(690, 1110, 1.1, "rg4"))}
 <div class="t cz" id="spot" style="top:1240px;font-size:64px;color:{CREAM}">DID YOU SPOT IT?</div>
 <div class="t" id="url" style="top:1360px"><span class="pill" style="font-size:52px;background:{TEAL}">rafiq-arabic.com</span></div>
 <div class="t" id="arr" style="top:1450px;font-size:80px">👇</div>
</div>
{caps}</div>"""
    open(os.path.join(out, "index.html"), "w").write(f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" /><title>khutbah</title>
<script src="assets/gsap.min.js"></script><style>{css}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{END}">
{body}
{chr(10).join(au)}
</div><script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;</script></body></html>
""")
    print("built", END, "s,", len(au), "sounds;", {k: float(v) for k, v in L.items()})

if __name__ == "__main__":
    build()
