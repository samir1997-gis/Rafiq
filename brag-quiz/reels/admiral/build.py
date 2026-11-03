#!/usr/bin/env python3
"""h8-admiral, the story of a word #7, in the drawn format of h5-safari and h6-zero (#317, #319): the lines in brag-quiz/voice/admiral-lines.json
told with full-screen drawings over a sea at dusk, ships drifting on the horizon. Cinzel for the titles, Amiri for the Arabic, every move on its
word, eased (MOTION-STYLE.md):
  1 "Every admiral in the navy has an Arabic title… they just don't know it": ADMIRAL, the admiral on his deck, أَمِير, a question mark
  2 أَمِير (Rafiq) · "a commander: the one who gives the orders": the admiral points, the signal flags go up
  3 "In Norman Sicily, in the 1100s… ran his fleet… amir of amirs": Sicily and Etna, the king, his commander, the fleet, أَمِيرُ الْأُمَراء
  4 "ammiratus… amiral… a D, from admire. Admiral.": the word changes as it travels; the D drops in
  5 your turn: أ م ر = to command; Yā-Sīn 36:82, أَمْرُهُ: ship / army / command? 3-2-1; the ayah (Rafiq); "COMMAND!", كُنْ فَيَكُونُ
  6 the ask: who's the real amir of your house? a crown drops onto mum. Then the cream end card.
Figures are faceless (owner, 27 Oct). Facts: Wiktionary and Wikipedia "admiral" (amīr; Roger II's "amir of amirs", George of Antioch,
Latinised ammiratus ammiratorum; the d from Latin admirari). The popular "amīr al-baḥr" origin is disputed, so the video doesn't claim it.

  python3 brag-quiz/reels/admiral/build.py    then  cd brag-quiz/reels/admiral/out/v && npx hyperframes render -o ../raw.mp4
"""
import json, os, re, shutil, subprocess
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
V6 = os.path.join(ROOT, "brag-output-v6/composition/assets"); VO = os.path.join(ROOT, "brag-quiz/voice/admiral")
INK, CREAM, GOLD, TEAL, RED, WOOD, NAVY = "#17262B", "#F6EBD3", "#F2C46B", "#2E7263", "#B4322A", "#8A5A2B", "#1D3557"
FAR, SEA = "#2a3550", "#0f3242"
dur = lambda f: float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))
mp3 = lambda n: os.path.join(VO, n + ".mp3")
def words(n):
    ws = json.load(open(os.path.join(VO, n + ".words.json")))
    return [(w[0], w[1], w[2] if len(w) > 2 else (ws[i + 1][1] if i + 1 < len(ws) else w[1] + 0.45)) for i, w in enumerate(ws)]
ORDER = [("h1", 0.3), ("amir", 0.35), ("b1", 0.25), ("b2", 0.45), ("b3", 0.5), ("t1", 0.55), ("ayah", 3.9), ("b4", 0.2), ("end", 0.8)]
ARABIC = ("amir", "ayah")
def spoken(n):
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", mp3(n), "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout, np.int16) / 32768
    e = 20 * np.log10(np.sqrt(np.convolve(x ** 2, np.ones(160) / 160, "same")) + 1e-9)
    return np.where(e > -45)[0][-1] / 16000 + 0.05
L, t = {}, 0.0
for n, g in ORDER: t += g; L[n] = round(t, 2); t += spoken(n)
END = round(t + 0.9, 2)
def at(n, key, last=False):
    hits = [s for w, s, e in words(n) if key in re.sub(r"[^a-z0-9']", "", w.lower())]
    return round(L[n] + (hits[-1] if last else hits[0]), 2)

def figure(x, y, s, c, id="", cls="", hat=None, hijab=None, arm=False, glass=False):   # faceless; the outer <g> places it, the inner one moves
    h = ""
    if hat: h = (f'<path d="M-46 -176 C -40 -214 40 -214 46 -176 C 30 -186 -30 -186 -46 -176 Z" fill="{INK}"/><path d="M-50 -176 C -20 -168 20 -168 50 -176" fill="none" stroke="{GOLD}" stroke-width="5"/>'
                 f'<circle cx="0" cy="-196" r="6" fill="{GOLD}"/>')
    if hijab: h = f'<path d="M0 -196 C -34 -196 -40 -160 -38 -140 C -40 -120 -34 -112 -30 -106 L 30 -106 C 34 -112 40 -120 38 -140 C 40 -160 34 -196 0 -196 Z" fill="{hijab}"/>'
    ep = f'<rect x="-46" y="-136" width="26" height="10" rx="4" fill="{GOLD}"/><rect x="20" y="-136" width="26" height="10" rx="4" fill="{GOLD}"/>' if hat else ""
    a = f'<path class="arm" d="M30 -110 L 86 -150" stroke="{c}" stroke-width="18" stroke-linecap="round"/>' if arm else ""
    g = (f'<path d="M30 -112 L 66 -126" stroke="{c}" stroke-width="18" stroke-linecap="round"/><rect x="60" y="-140" width="70" height="20" rx="6" fill="{GOLD}" stroke="{WOOD}" stroke-width="4" transform="rotate(-18 60 -130)"/>'
         if glass else "")
    return (f'<g transform="translate({x},{y}) scale({s})"><g id="{id}" class="{cls}"><path d="M-44 0 C -40 -80 -32 -126 0 -140 C 32 -126 40 -80 44 0 Z" fill="{c}"/>'
            f'<circle cx="0" cy="-160" r="26" fill="#C98E62"/>{h}{ep}{a}{g}</g></g>')
def ship(x, y, s, id="", sail=CREAM, flag=RED):
    return (f'<g transform="translate({x},{y}) scale({s})"><g id="{id}"><path d="M-6 -10 L -6 -250 M 90 -10 L 90 -190" stroke="{WOOD}" stroke-width="10"/>'
            f'<path d="M-6 -240 C 60 -200 60 -90 -6 -60 Z" fill="{sail}" stroke="#d9cbae" stroke-width="4"/><path d="M90 -180 C 140 -150 140 -80 90 -60 Z" fill="{sail}" stroke="#d9cbae" stroke-width="4"/>'
            f'<path d="M-6 -250 L 40 -238 L -6 -226 Z" fill="{flag}"/>'
            f'<path d="M-170 -20 L 190 -20 C 180 20 150 40 110 46 L -130 46 C -160 30 -170 10 -170 -20 Z" fill="{WOOD}" stroke="{GOLD}" stroke-width="5" stroke-linejoin="round"/>'
            + "".join(f'<circle cx="{cx}" cy="10" r="7" fill="{GOLD}"/>' for cx in (-100, -50, 0, 50, 100)) + '</g></g>')
def crown(x, y, s, id="", cls=""):
    return (f'<g transform="translate({x},{y}) scale({s})"><g id="{id}" class="{cls}"><path d="M-40 0 L -46 -50 L -22 -26 L 0 -60 L 22 -26 L 46 -50 L 40 0 Z" fill="{GOLD}" stroke="{WOOD}" stroke-width="5" stroke-linejoin="round"/>'
            f'<circle cx="0" cy="-64" r="7" fill="{RED}"/></g></g>')
SHIP_I = f'<svg width="70" height="70" viewBox="-200 -270 400 330">{ship(0, 0, 1)}</svg>'
ARMY_I = (f'<svg width="70" height="70" viewBox="0 0 100 100"><path d="M50 10 L 84 22 L 80 60 C 76 78 62 88 50 94 C 38 88 24 78 20 60 L 16 22 Z" fill="{TEAL}" stroke="{WOOD}" stroke-width="5"/>'
          f'<path d="M50 30 L 50 74 M 32 50 L 68 50" stroke="{CREAM}" stroke-width="7" stroke-linecap="round"/></svg>')
CMD_I = (f'<svg width="70" height="70" viewBox="0 0 100 100"><rect x="18" y="18" width="64" height="70" rx="8" fill="{CREAM}" stroke="{WOOD}" stroke-width="5"/>'
         f'<path d="M30 38 L 70 38 M 30 52 L 70 52 M 30 66 L 56 66" stroke="{WOOD}" stroke-width="5" stroke-linecap="round"/><circle cx="70" cy="76" r="12" fill="{RED}"/></svg>')

def build():
    out = os.path.join(HERE, "out", "v"); a = os.path.join(out, "assets")
    if os.path.exists(out): shutil.rmtree(out)
    os.makedirs(a)
    for f in ("karla-latin-700-normal.woff2",): shutil.copy(os.path.join(V6, "fonts", f), a)
    for f in ("cinzel-latin-700-normal.woff2", "amiri-arabic-700-normal.woff2"): shutil.copy(os.path.join(ROOT, "brag-quiz/fonts", f), a)
    shutil.copy(os.path.join(V6, "lib/gsap.min.js"), a)
    for f in ("shimmer.wav", "tick-lo.wav", "thump.wav", "whoosh.wav", "impact.wav", "drone.wav", "flip.wav", "wind.wav"): shutil.copy(os.path.join(ROOT, "brag-quiz/sfx/soft", f), a)
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
    def draw(sel, t, d=0.6): T(f'tl.fromTo("{sel}", {{strokeDashoffset:1}}, {{strokeDashoffset:0, duration:{d}, stagger:0.12, ease:"power2.inOut"}}, {t:.2f});')
    def pulse(sel, t, s=1.08): T(f'tl.fromTo("{sel}", {{scale:1}}, {{scale:{s}, duration:0.2, yoyo:true, repeat:1, ease:"power2.out", transformOrigin:"50% 50%", immediateRender:false}}, {t:.2f});')
    def rock(sel, t0, t1, deg=3, d=1.1):                                   # a ship rocking on the swell
        n = max(1, int((t1 - t0) / d / 2) * 2 - 1)
        T(f'tl.fromTo("{sel}", {{rotation:-{deg}}}, {{rotation:{deg}, duration:{d}, yoyo:true, repeat:{n}, ease:"sine.inOut", transformOrigin:"50% 100%", immediateRender:false}}, {t0:.2f});')
    def scene(sel, t0, t1):
        if t0 > 0: T(f'tl.fromTo("{sel}", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.45, ease:"power3.out"}}, {t0:.2f});')
        if t1: T(f'tl.to("{sel}", {{opacity:0, y:-60, duration:0.35, ease:"power2.in"}}, {t1:.2f});'); snd("whoosh.wav", t1 - 0.05, 0.3)

    # the sea lives the whole time: the waves roll, the far ships drift, the stars come out
    T(f'tl.fromTo("#waves", {{x:0}}, {{x:-240, duration:{END:.2f}, ease:"sine.inOut"}}, 0);')
    T(f'tl.fromTo("#farships", {{x:0}}, {{x:200, duration:{END:.2f}, ease:"sine.inOut"}}, 0);')
    T(f'tl.fromTo("#stars", {{opacity:0.2}}, {{opacity:0.9, duration:{END:.2f}, ease:"sine.inOut"}}, 0);')
    T(f'tl.fromTo("#sun", {{y:0}}, {{y:90, duration:{END:.2f}, ease:"sine.inOut"}}, 0);')

    # 1 · the hook: ADMIRAL on his deck; an Arabic title; they don't know it
    S2 = L["amir"] - 0.25
    rock("#sh1", 0, S2)
    ab = at("h1", "arabic")
    POP("#tit", ab - 0.1, 0.7); snd("tap.wav", ab, 0.35)
    T(f'tl.fromTo("#ttl2", {{opacity:0, scale:1.6}}, {{opacity:1, scale:1, duration:0.45, ease:"back.out(1.4)"}}, {ab + 0.2:.2f});'); snd("impact.wav", ab + 0.2, 0.35, 1.2)
    dk = at("h1", "don't")
    POP("#qm", dk - 0.1, 0.4); snd("tick-lo.wav", dk, 0.45)
    T(f'tl.fromTo("#adm1", {{rotation:0}}, {{rotation:-8, duration:0.3, yoyo:true, repeat:1, ease:"sine.inOut", transformOrigin:"50% 100%", immediateRender:false}}, {dk:.2f});')
    scene("#s1", 0, S2 - 0.05)
    # 2 · أَمِير: a commander, the one who gives the orders
    scene("#s2", S2, L["b2"] - 0.35)
    POP("#aw", L["amir"] - 0.05, 0.7); snd("tick-lo.wav", L["amir"], 0.4)
    cm = at("b1", "commander")
    POP("#ac", cm - 0.05, 0.7); snd("tap.wav", cm, 0.35)
    IN("#adm2", cm - 0.2, 60)
    od = at("b1", "orders")
    T(f'tl.fromTo("#adm2 .arm", {{rotation:30}}, {{rotation:0, duration:0.35, ease:"back.out(1.6)", svgOrigin:"30 -110"}}, {od - 0.2:.2f});')
    T(f'tl.fromTo("#flags path.f", {{opacity:0, y:-30}}, {{opacity:1, y:0, duration:0.3, stagger:0.08, ease:"back.out(1.6)"}}, {od - 0.1:.2f});'); draw("#flags .line", od - 0.2, 0.4)
    snd("swoosh.wav", od - 0.1, 0.35)
    # 3 · Norman Sicily, the 1100s: the king, his commander, the fleet, amir of amirs
    S3 = L["b2"] - 0.1; scene("#s3", S3, L["b3"] - 0.35)
    sc = at("b2", "sicily")
    POP("#sic", sc - 0.1, 0.7); IN("#isl", sc - 0.2, 60); snd("thump.wav", sc, 0.35)
    POP("#yr", at("b2", "1100s") - 0.05, 0.7); snd("tick-lo.wav", at("b2", "1100s"), 0.45)
    kg = at("b2", "king's")
    POP("#kg", kg - 0.1, 0.6); T(f'tl.fromTo("#kcr", {{opacity:0, y:-120}}, {{opacity:1, y:0, duration:0.45, ease:"bounce.out"}}, {kg:.2f});'); snd("tap.wav", kg, 0.35)
    cmd = at("b2", "commander")
    POP("#cmd", cmd - 0.1, 0.6); snd("tap.wav", cmd, 0.35)
    fl = at("b2", "fleet")
    T(f'tl.fromTo("#fleet g.sh", {{opacity:0, x:-500}}, {{opacity:1, x:0, duration:1.0, stagger:0.15, ease:"power2.out"}}, {fl - 0.4:.2f});'); snd("swoosh.wav", fl - 0.3, 0.4); snd("wind.wav", fl - 0.4, 0.2, 2.0)
    aa = at("b2", "amirs", last=True)
    T(f'tl.fromTo("#aoa", {{opacity:0, scale:1.5}}, {{opacity:1, scale:1, duration:0.45, ease:"back.out(1.6)"}}, {aa - 0.9:.2f});'); snd("impact.wav", aa - 0.9, 0.35, 1.2)
    # 4 · ammiratus → amiral → admiral: the D drops in
    S4 = L["b3"] - 0.1; scene("#s4", S4, L["t1"] - 0.4)
    for i, (k, lab) in enumerate((("ammiratus", "LATIN"), ("amiral", "FRENCH"))):
        w0 = at("b3", k); POP(f"#wd{i}", w0 - 0.05, 0.7); snd("tap.wav", w0, 0.35)
        draw(f"#ar{i}", w0 + 0.5, 0.4)
    IN("#wd2", at("b3", "english") - 0.1, 30); snd("tap.wav", at("b3", "english"), 0.35)
    dd = at("b3", "d")
    T(f'tl.fromTo("#dd", {{opacity:0, y:-260, rotation:-20}}, {{opacity:1, y:0, rotation:0, duration:0.55, ease:"bounce.out"}}, {dd - 0.1:.2f});'); snd("thump.wav", dd + 0.25, 0.45)
    POP("#adm", at("b3", "admire") - 0.05, 0.6); snd("tick-lo.wav", at("b3", "admire"), 0.4)
    pulse("#wd2", at("b3", "admiral", last=True), 1.1); snd("shimmer.wav", at("b3", "admiral", last=True), 0.35, 1.2)
    # 5 · your turn: أ م ر, to command; Yā-Sīn 36:82, ship / army / command? 3-2-1; the ayah; COMMAND!; كُنْ فَيَكُونُ
    S5 = L["t1"] - 0.1; scene("#s5", S5, L["end"] - 0.45)
    IN("#yt", L["t1"], 20)
    rt = at("t1", "root")
    for i in range(3):
        T(f'tl.fromTo("#tl{i}", {{opacity:0, y:-200}}, {{opacity:1, y:0, duration:0.4, ease:"power3.out"}}, {rt - 0.15 + i * 0.14:.2f});'); snd("thump.wav", rt + i * 0.14, 0.3)
    POP("#tc", at("t1", "command") - 0.05, 0.7); snd("tap.wav", at("t1", "command"), 0.35)
    ys = at("t1", "yaseen")
    T(f'tl.to(["#tiles", "#tc"], {{opacity:0, y:-30, duration:0.3, ease:"power2.in"}}, {ys - 0.3:.2f});')
    POP("#aya", ys - 0.1, 0.8); snd("flip.wav", ys, 0.4)
    ar_ = at("t1", "amruhu"); IN("#ee0", ar_ - 0.1, 16); draw("#hl", ar_, 0.5); snd("tap.wav", ar_, 0.4)
    for i, (k, last) in enumerate((("ship", False), ("army", False), ("command", True))):
        w0 = at("t1", k, last); POP(f"#op{i}", w0 - 0.05, 0.8); snd("tap.wav", w0, 0.3)
    c0 = round(L["t1"] + spoken("t1") + 0.3, 2)
    for k, nm in enumerate(("3", "2", "1")):
        T(f'tl.set("#cd", {{textContent:"{nm}", opacity:1}}, {c0 + k:.2f});'); T(f'tl.fromTo("#cd", {{scale:1.4}}, {{scale:1, duration:0.35, ease:"power3.out"}}, {c0 + k:.2f});')
        snd("click.wav", c0 + k, 1.0); snd("tick-lo.wav", c0 + k, 0.5)
    rv = c0 + 3
    T(f'tl.to("#cd", {{opacity:0, duration:0.2, ease:"power2.in"}}, {rv - 0.1:.2f});')
    T(f'tl.to("#op2", {{backgroundColor:"{GOLD}", scale:1.08, duration:0.3, ease:"back.out(1.4)"}}, {rv:.2f});'); snd("tick-lo.wav", rv, 0.45)
    T(f'tl.to(["#op0", "#op1"], {{opacity:0.3, duration:0.3, ease:"power2.in"}}, {rv:.2f});')
    T(f'tl.to("#ee0", {{opacity:0, duration:0.2, ease:"power2.in"}}, {L["ayah"] + 0.2:.2f});'); IN("#ee1", L["ayah"] + 0.4, 16)
    hit = at("b4", "command")
    T(f'tl.to("#ops", {{opacity:0, y:30, duration:0.25, ease:"power2.in"}}, {hit - 0.25:.2f});')
    T(f'tl.fromTo("#slam", {{opacity:0, scale:1.8}}, {{opacity:1, scale:1, duration:0.45, ease:"back.out(1.7)"}}, {hit:.2f});')   # the one slam
    T(f'tl.fromTo("#cam", {{x:-14}}, {{x:14, duration:0.05, yoyo:true, repeat:7, ease:"sine.inOut", immediateRender:false}}, {hit + 0.05:.2f});')
    T(f'tl.set("#cam", {{x:0}}, {hit + 0.5:.2f});')
    snd("impact.wav", hit - 0.03, 0.75, 1.6)
    T(f'tl.fromTo("#burst i", {{opacity:1, x:0, y:0, scale:0.4}}, {{opacity:0, x:(i) => [-300, -170, 0, 170, 300, -90, 90][i], y:(i) => [-80, -200, -260, -200, -80, 150, 150][i], scale:1.3, duration:0.9, ease:"power2.out", immediateRender:false}}, {hit + 0.05:.2f});')
    be = at("b4", "be")
    T(f'tl.fromTo("#kun", {{opacity:0, scale:0.4}}, {{opacity:1, scale:1, duration:0.5, ease:"back.out(1.8)"}}, {be - 0.05:.2f});'); snd("shimmer.wav", be, 0.4, 1.2)
    T(f'tl.fromTo("#glow", {{opacity:0, attr:{{r:100}}}}, {{opacity:0.6, attr:{{r:240}}, duration:0.8, ease:"power2.out"}}, {be:.2f});')
    POP("#fy", at("b4", "is", last=True) - 0.1, 0.7); snd("tap.wav", at("b4", "is", last=True), 0.4)
    # 6 · the ask: who's the real amir of your house? the crown drops onto mum
    S6 = L["end"] - 0.1; scene("#s6", S6, None)
    IN("#q", L["end"] + 0.1, 30)
    T(f'tl.fromTo("#fam g.p", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.4, stagger:0.1, ease:"back.out(1.4)"}}, {L["end"] + 0.2:.2f});')
    am = at("end", "amir")
    T(f'tl.fromTo("#mcr", {{opacity:0, y:-300}}, {{opacity:1, y:0, duration:0.6, ease:"bounce.out"}}, {am - 0.2:.2f});'); snd("thump.wav", am + 0.3, 0.4); snd("shimmer.wav", am + 0.3, 0.3, 1.2)
    cmt = at("end", "comment")
    POP("#url", cmt - 0.1, 0.8); snd("tap.wav", cmt, 0.4)
    T(f'tl.fromTo("#arr", {{opacity:0, y:0}}, {{opacity:1, y:18, duration:0.4, yoyo:true, repeat:3, ease:"sine.inOut"}}, {cmt:.2f});')

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

    rng = np.random.default_rng(9)
    stars = "".join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#fff6dc" opacity="{o:.2f}"/>' for x, y, r, o in
                    zip(rng.uniform(0, 1080, 70), rng.uniform(0, 900, 70), rng.uniform(1, 3, 70), rng.uniform(0.3, 0.9, 70)))
    waves = "".join(f'<path d="M{x} {y} q 40 -18 80 0 t 80 0" stroke="#7fb3c4" stroke-width="{w}" fill="none" opacity="{o}" stroke-linecap="round"/>'
                    for x, y, w, o in zip(rng.uniform(-100, 1300, 46), rng.uniform(1300, 1900, 46), rng.uniform(3, 6, 46), rng.uniform(0.2, 0.5, 46)))
    farships = "".join(f'<g transform="translate({x},1268) scale({s})"><path d="M-40 0 L 40 0 L 30 10 L -30 10 Z" fill="{FAR}"/><path d="M0 0 L 0 -60 M 0 -56 L 26 -10 L 0 -10 Z" stroke="{FAR}" stroke-width="5" fill="{FAR}"/></g>'
                       for x, s in ((150, 0.8), (430, 0.6), (820, 0.7)))
    sv = lambda inner: f'<svg class="full" viewBox="0 0 1080 1920">{inner}</svg>'
    arrow = lambda id, d: f'<path id="{id}" pathLength="1" d="{d}" fill="none" stroke="{GOLD}" stroke-width="7" stroke-linecap="round" stroke-dasharray="1" stroke-dashoffset="1"/>'
    tile = lambda id, ch, x, y, sz=190, fs=150: f'<div class="tile" id="{id}" style="left:{x}px;top:{y}px;width:{sz}px;height:{sz}px;line-height:{sz}px;font-size:{fs}px">{ch}</div>'
    burst = "".join(f'<i style="position:absolute;left:520px;top:960px;width:40px;height:40px;border-radius:50%;background:{c};opacity:0"></i>' for c in (GOLD, CREAM, RED, GOLD, CREAM, RED, GOLD))
    flags = ('<g id="flags"><path class="line" pathLength="1" d="M300 760 C 500 820 700 820 900 760" fill="none" stroke="' + CREAM + '" stroke-width="5" stroke-dasharray="1" stroke-dashoffset="1"/>'
             + "".join(f'<path class="f" d="M{x - 26} {y} L {x + 26} {y} L {x} {y + 56} Z" fill="{c}" opacity="0" style="opacity:0"/>' for x, y, c in
                       ((360, 782, RED), (440, 800, GOLD), (520, 808, TEAL), (600, 808, CREAM), (680, 800, RED), (760, 790, GOLD), (840, 774, TEAL))) + '</g>')
    island = (f'<g id="isl" opacity="0" style="opacity:0"><path d="M120 1250 C 200 1150 300 1120 380 1080 L 470 980 L 540 1060 C 640 1080 820 1120 960 1250 Z" fill="#3c5a43"/>'
              f'<path d="M430 1020 L 470 980 L 510 1020 C 490 1012 452 1012 430 1020 Z" fill="{CREAM}"/><path d="M470 970 C 460 930 490 920 480 880" fill="none" stroke="#c9ced6" stroke-width="10" stroke-linecap="round" opacity=".7"/></g>')
    fleet = '<g id="fleet">' + "".join(f'<g class="sh" opacity="0" style="opacity:0">{ship(x, y, s)}</g>' for x, y, s in ((260, 1440, 0.55), (560, 1480, 0.65), (860, 1430, 0.5))) + '</g>'
    css = f"""
@font-face {{ font-family:"CZ"; src:url("assets/cinzel-latin-700-normal.woff2"); }}
@font-face {{ font-family:"AM"; src:url("assets/amiri-arabic-700-normal.woff2"); }}
@font-face {{ font-family:"KA"; src:url("assets/karla-latin-700-normal.woff2"); }}
* {{ margin:0; box-sizing:border-box; }} html, body {{ width:1080px; height:1920px; overflow:hidden; background:#000; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; background:linear-gradient(#141a36 0%, #2b2f5c 35%, #6a4f73 58%, #d5866a 64.5%, {SEA} 65.5%, #0b2230 100%); font-family:KA; color:{CREAM}; }}
#cam {{ position:absolute; inset:0; }}
svg.full {{ position:absolute; left:0; top:0; width:1080px; height:1920px; overflow:visible; }}
.sc {{ position:absolute; inset:0; opacity:0; }} #s1 {{ opacity:1; }}
.t {{ position:absolute; left:0; right:0; text-align:center; opacity:0; }}
.cz {{ font-family:CZ; letter-spacing:.06em; color:{GOLD}; text-shadow:0 4px 0 {WOOD}, 0 10px 30px rgba(0,0,0,.5); }}
.am {{ font-family:AM; direction:rtl; color:{CREAM}; text-shadow:0 6px 0 {TEAL}, 0 14px 40px rgba(0,0,0,.45); line-height:1.3; }}
.pill {{ display:inline-flex; align-items:center; gap:14px; padding:8px 30px; border-radius:999px; background:rgba(14,20,44,.88); border:2px solid rgba(242,196,107,.6); font-family:KA; color:{CREAM}; }}
.cap {{ position:absolute; left:70px; right:70px; top:1580px; text-align:center; font-family:KA; font-size:50px; line-height:1.2; color:#fff; text-shadow:0 3px 0 rgba(0,0,0,.6), 0 0 18px rgba(0,0,0,.6); opacity:0; }}
.cap span {{ display:inline-block; opacity:0; }}
.card {{ position:absolute; left:60px; right:60px; padding:22px 26px 20px; border-radius:20px; background:#f3e3c0; color:{INK}; text-align:center; opacity:0;
  box-shadow:0 24px 50px rgba(0,0,0,.4), inset 0 0 0 6px #e3c993, inset 0 0 0 9px {TEAL}; }}
.card .aa {{ font-family:AM; direction:rtl; line-height:1.7; }}
.card .ee {{ font-family:CZ; font-size:32px; color:{TEAL}; margin-top:2px; }} .card small {{ display:block; font-size:28px; color:#6b5a44; margin-top:8px; }}
.hlw {{ position:relative; display:inline-block; }} .hlw svg {{ position:absolute; left:-40px; top:-4px; width:calc(100% + 60px); height:calc(100% + 8px); overflow:visible; }}
.op {{ display:flex; align-items:center; gap:22px; width:600px; margin:18px auto 0; padding:12px 30px; border-radius:24px; background:rgba(246,235,211,.95); color:{INK}; font-family:CZ; font-size:46px; opacity:0; box-shadow:0 14px 30px rgba(0,0,0,.35); }}
.op svg {{ flex:none; }}
#cd {{ position:absolute; left:0; right:0; top:610px; text-align:center; font-family:CZ; font-size:130px; color:{GOLD}; opacity:0; text-shadow:0 6px 0 {WOOD}; }}
.tile {{ position:absolute; border-radius:30px; background:{CREAM}; color:{RED}; font-family:AM; text-align:center; opacity:0; box-shadow:0 14px 0 {WOOD}, 0 24px 40px rgba(0,0,0,.4); }}
.wd {{ position:absolute; left:0; right:0; text-align:center; opacity:0; }}
.wd span {{ display:inline-block; padding:10px 40px 6px; border-radius:24px; background:rgba(246,235,211,.96); color:{INK}; font-family:CZ; box-shadow:0 14px 30px rgba(0,0,0,.4); }}
.wd b {{ display:block; font-family:KA; font-size:28px; letter-spacing:.1em; color:{TEAL}; }}
#logo {{ position:absolute; top:62px; left:50%; transform:translateX(-50%); display:flex; justify-content:center; gap:12px; align-items:center; z-index:5; padding:6px 22px 6px 8px; border-radius:22px; background:rgba(14,20,44,.55); }}
#logo .tl {{ position:relative; width:58px; height:58px; border-radius:16px; background:{CREAM}; display:grid; place-items:center; }}
#logo .tl span {{ font-family:AM; font-size:38px; color:{INK}; margin-top:-6px; }} #logo .tl em {{ position:absolute; right:9px; top:8px; width:9px; height:9px; border-radius:50%; background:{RED}; }}
#logo b {{ font-family:AM; font-size:44px; color:{CREAM}; }}
"""
    body = f"""<div id="cam">
<svg class="full" viewBox="0 0 1080 1920"><g id="stars">{stars}</g>
 <g id="sun"><circle cx="540" cy="1250" r="150" fill="#f0a062" opacity=".35"/><circle cx="540" cy="1250" r="90" fill="#f4b36e"/></g>
 <rect x="0" y="1258" width="1080" height="662" fill="url(#seag)"/><defs><linearGradient id="seag" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{SEA}"/><stop offset="1" stop-color="#0b2230"/></linearGradient></defs>
 <g id="farships">{farships}</g><g id="waves">{waves}</g>
</svg>
<div id="logo"><span class="tl"><span>ر</span><em></em></span><b>رَفِيق</b></div>
<div class="sc" id="s1">
 <div class="t cz" id="kick" style="top:180px;font-size:44px;opacity:1">THE STORY OF A WORD</div>
 <div class="t cz" id="ttl" style="top:250px;font-size:160px;opacity:1">ADMIRAL</div>
 <div class="t" id="tit" style="top:480px"><span class="pill" style="font-size:44px">an Arabic title</span></div>
 <div class="t am" id="ttl2" style="top:610px;font-size:180px;color:{GOLD}">أَمِير</div>
 {sv('<g id="sh1g">' + ship(540, 1380, 1.6, "sh1") + '</g>' + figure(540, 1348, 1.5, NAVY, "adm1", hat=True, glass=True))}
 <div class="t cz" id="qm" style="top:940px;left:640px;right:auto;width:200px;font-size:120px;color:{CREAM}">?</div>
</div>
<div class="sc" id="s2">
 <div class="t am" id="aw" style="top:180px;font-size:210px;color:{GOLD}">أَمِير</div>
 <div class="t" id="ac" style="top:480px"><span class="pill" style="font-size:50px">amīr = <b style="color:{GOLD}">a commander</b></span></div>
 {sv(flags + figure(540, 1440, 2.2, NAVY, "adm2", hat=True, arm=True) + f'<rect x="170" y="1430" width="740" height="74" rx="18" fill="{WOOD}" stroke="{GOLD}" stroke-width="6"/>' + ''.join(f'<rect x="{x}" y="1370" width="14" height="64" rx="6" fill="{WOOD}"/>' for x in (200, 330, 460, 610, 740, 870)) + f'<path d="M190 1372 L 890 1372" stroke="{WOOD}" stroke-width="12" stroke-linecap="round"/>')}
</div>
<div class="sc" id="s3">
 <div class="t" id="sic" style="top:180px"><span class="pill" style="font-size:52px">Norman <b style="color:{GOLD}">Sicily</b></span></div>
 <div class="t" id="yr" style="top:280px"><span class="pill" style="font-size:46px;font-family:CZ;color:{GOLD}">1100s</span></div>
 {sv(island + figure(300, 1200, 1.0, "#7a2d3a", "kg") + crown(300, 1016, 0.8, "kcr") + figure(780, 1200, 1.0, NAVY, "cmd", hat=True) + fleet)}
 <div class="t" id="aoa" style="top:420px"><div style="display:inline-block;padding:10px 40px 14px;border-radius:24px;background:rgba(246,235,211,.96);color:{INK};box-shadow:0 14px 30px rgba(0,0,0,.4)">
  <div style="font-family:AM;font-size:84px;line-height:1.4;direction:rtl">أَمِيرُ الْأُمَراء</div><div style="font-family:CZ;font-size:40px;color:{TEAL}">AMIR OF AMIRS</div></div></div>
</div>
<div class="sc" id="s4">
 <div class="wd" id="wd0" style="top:250px"><span style="font-size:76px"><b>LATIN</b>ammiratus</span></div>
 {sv(arrow("ar0", "M540 470 L 540 540") + arrow("ar1", "M540 760 L 540 830"))}
 <div class="wd" id="wd1" style="top:560px"><span style="font-size:76px"><b>FRENCH</b>amiral</span></div>
 <div class="wd" id="wd2" style="top:860px"><span style="font-size:110px"><b>ENGLISH</b>A<i id="dd" style="display:inline-block;font-style:normal;color:{RED}">D</i>MIRAL</span></div>
 <div class="t" id="adm" style="top:1130px"><span class="pill" style="font-size:44px">the D: from <b style="color:{GOLD}">“admire”</b></span></div>
</div>
<div class="sc" id="s5">
 <div class="t cz" id="yt" style="top:170px;font-size:76px">YOUR TURN</div>
 <div id="tiles">{tile("tl0", "أ", 745, 320)}{tile("tl1", "م", 445, 320)}{tile("tl2", "ر", 145, 320)}</div>
 <div class="t" id="tc" style="top:560px"><span class="pill" style="font-size:52px">the root = <b style="color:{GOLD}">to command</b></span></div>
 <div class="card" id="aya" style="top:280px"><div class="aa" style="font-size:62px">إِنَّما <span class="hlw">أَمْرُهُ<svg viewBox="0 0 100 60" preserveAspectRatio="none"><ellipse id="hl" pathLength="1" cx="50" cy="32" rx="48" ry="27" fill="none" stroke="{RED}" stroke-dasharray="1" stroke-dashoffset="1" vector-effect="non-scaling-stroke" style="stroke-width:7px"/></svg></span> إِذا أَرادَ شَيْئًا<br/>أَنْ يَقُولَ لَهُ كُنْ فَيَكُونُ</div>
  <div style="position:relative;height:46px"><div class="ee" id="ee0" style="position:absolute;left:0;right:0;opacity:0">His ___ is only to say: “Be!” and it is</div><div class="ee" id="ee1" style="position:absolute;left:0;right:0;opacity:0">His command is only to say: “Be!” and it is</div></div>
  <small>the Qur’an · Yā-Sīn 36:82</small></div>
 <div id="ops" style="position:absolute;left:0;right:0;top:800px"><div class="op" id="op0">{SHIP_I}<span>his ship</span></div><div class="op" id="op1">{ARMY_I}<span>his army</span></div><div class="op" id="op2">{CMD_I}<span>his command</span></div></div>
 <div id="cd">3</div>
 <div class="t cz" id="slam" style="top:740px;font-size:130px;line-height:1.1">COMMAND!</div>
 {sv(f'<circle id="glow" cx="540" cy="1180" r="200" fill="{GOLD}" opacity="0"/>')}
 <div class="t am" id="kun" style="top:990px;font-size:220px;color:{GOLD}">كُنْ</div>
 <div class="t" id="fy" style="top:1410px"><span class="pill" style="font-size:44px"><b style="font-family:AM;font-size:60px;color:{CREAM}">كُنْ فَيَكُونُ</b> “Be!” and it is</span></div>
 <div id="burst">{burst}</div>
</div>
<div class="sc" id="s6">
 <div class="t" id="q" style="top:180px"><div class="cz" style="display:inline-block;padding:18px 40px 12px;border-radius:28px;background:rgba(14,20,44,.82);font-size:64px;line-height:1.25">WHO’S THE REAL<br/>AMIR OF YOUR HOUSE?</div></div>
 {sv('<g id="fam">' + "".join(f'<g class="p" opacity="0" style="opacity:0">{figure(x, 1200, s, c, hijab=hj)}</g>' for x, s, c, hj in
     ((250, 1.3, "#3f8a7a", None), (450, 1.35, "#7a2d3a", "#2E7263"), (650, 0.95, "#e7b07a", None), (820, 0.85, GOLD, "#B4322A"))) + '</g>' + crown(450, 930, 1.0, "mcr"))}
 <div class="t" id="url" style="top:1300px"><span class="pill" style="font-size:50px;background:{TEAL}">rafiq-arabic.com</span></div>
 <div class="t" id="arr" style="top:1390px;font-size:80px">👇</div>
</div>
</div>"""
    body = body[:-6] + caps + "</div>"
    open(os.path.join(out, "index.html"), "w").write(f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" /><title>admiral</title>
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
