#!/usr/bin/env python3
"""h9-mattress, the story of a word #8 (#340), in the drawn format of h5-safari and h8-admiral (#317, #323): the lines in
brag-quiz/voice/mattress-lines.json told with full-screen drawings over a town's rooftops at night, under the moon. Cinzel for the
titles, Amiri for the Arabic, every move on its word, eased (MOTION-STYLE.md):
  1 "Every night, you fall asleep on an Arabic word… and you don't even know it": MATTRESS, a mattress on a rooftop, the sleeper
    flops onto it, مَطْرَح, a question mark
  2 مَطْرَح (Rafiq) · "something thrown down: a cushion you throw on the floor, to sit or sleep on": cushions drop onto the floor
  3 "Its root means to throw… the same ma as masjid: the place of… the place you throw yourself down": ط ر ح, مَسْجِد and مَطْرَح
    side by side with their مَـ lit, then the sleeper flops down again
  4 "Sicily passed it to Italian as materasso… French… materas… by the 1300s… a mattress": the word changes as it travels
  5 your turn: ط ر ح in Yūsuf 12:9, اطْرَحُوهُ: hide him / sell him / throw him? 3-2-1; the ayah (Rafiq); "THROW!"
  6 the ask: what do you say before you sleep? the sleeper under the moon. Then the cream end card.
Figures are faceless (owner, 27 Oct). Facts: Wiktionary "mattress", "materasso" (Arabic مَطْرَح "place where something is thrown",
from طَرَحَ "to throw"); Etymonline (Old French materas, Italian materasso, Arabic al-maṭraḥ "the cushion, the thing thrown down";
English c. 1290); the Arabic word passed through Sicily (OED, via Wiktionary). The popular Crusader story isn't sourced, so it isn't told.

  python3 brag-quiz/reels/mattress/build.py    then  cd brag-quiz/reels/mattress/out/v && npx hyperframes render -o ../raw.mp4
"""
import json, os, re, shutil, subprocess
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
V6 = os.path.join(ROOT, "brag-output-v6/composition/assets"); VO = os.path.join(ROOT, "brag-quiz/voice/mattress")
INK, CREAM, GOLD, TEAL, RED, WOOD, NAVY = "#17262B", "#F6EBD3", "#F2C46B", "#2E7263", "#B4322A", "#8A5A2B", "#1D3557"
ROOF, WALL = "#2a2d52", "#3b3f6e"
dur = lambda f: float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))
mp3 = lambda n: os.path.join(VO, n + ".mp3")
def words(n):
    ws = json.load(open(os.path.join(VO, n + ".words.json")))
    return [(w[0], w[1], w[2] if len(w) > 2 else (ws[i + 1][1] if i + 1 < len(ws) else w[1] + 0.45)) for i, w in enumerate(ws)]
ORDER = [("h1", 0.3), ("matrah", 0.35), ("b1", 0.25), ("b2", 0.45), ("b3", 0.5), ("t1", 0.55), ("ayah", 3.9), ("b4", 0.2), ("end", 0.8)]
ARABIC = ("matrah", "ayah")
def spoken(n):
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", mp3(n), "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout, np.int16) / 32768
    e = 20 * np.log10(np.sqrt(np.convolve(x ** 2, np.ones(160) / 160, "same")) + 1e-9)
    return np.where(e > -45)[0][-1] / 16000 + 0.05
L, t = {}, 0.0
for n, g in ORDER: t += g; L[n] = round(t, 2); t += spoken(n)
END = round(t + 0.9, 2)
def at(n, key, last=False, exact=False):   # when the word containing key is said (exact: the whole word)
    clean = lambda w: re.sub(r"[^a-z0-9']", "", w.lower())
    hits = [s for w, s, e in words(n) if (clean(w) == key if exact else key in clean(w))]
    return round(L[n] + (hits[-1] if last else hits[0]), 2)

def figure(x, y, s, c, id="", cls="", hijab=None):   # faceless; the outer <g> places it, the inner one moves
    h = f'<path d="M0 -196 C -34 -196 -40 -160 -38 -140 C -40 -120 -34 -112 -30 -106 L 30 -106 C 34 -112 40 -120 38 -140 C 40 -160 34 -196 0 -196 Z" fill="{hijab}"/>' if hijab else ""
    return (f'<g transform="translate({x},{y}) scale({s})"><g id="{id}" class="{cls}"><path d="M-44 0 C -40 -80 -32 -126 0 -140 C 32 -126 40 -80 44 0 Z" fill="{c}"/>'
            f'<circle cx="0" cy="-160" r="26" fill="#C98E62"/>{h}</g></g>')
def mattress(x, y, s, id=""):   # a striped floor mattress with a pillow, seen from the front
    stripes = "".join(f'<path d="M{-230 + k * 46} -70 L {-230 + k * 46} 0" stroke="{TEAL}" stroke-width="10" opacity=".55"/>' for k in range(11))
    return (f'<g transform="translate({x},{y}) scale({s})"><g id="{id}"><rect x="-250" y="-74" width="500" height="80" rx="26" fill="{CREAM}" stroke="{WOOD}" stroke-width="6"/>{stripes}'
            f'<path d="M-250 -30 L 250 -30" stroke="#d9cbae" stroke-width="5"/>'
            f'<rect x="-226" y="-118" width="150" height="56" rx="26" fill="#fbf4e4" stroke="{WOOD}" stroke-width="5"/></g></g>')
def sleeper(x, y, s, id="", c=NAVY):   # someone lying on their back under a blanket, faceless
    return (f'<g transform="translate({x},{y}) scale({s})"><g id="{id}"><circle cx="-150" cy="-106" r="30" fill="#C98E62"/>'
            f'<path d="M-118 -78 C -60 -130 150 -128 210 -86 C 226 -76 224 -60 206 -58 L -114 -58 C -130 -60 -132 -70 -118 -78 Z" fill="{c}"/>'
            f'<path d="M-60 -98 C 20 -112 120 -110 190 -92" fill="none" stroke="{GOLD}" stroke-width="6" stroke-linecap="round" opacity=".8"/></g></g>')
def cushion(x, y, s, c, id=""):
    return (f'<g transform="translate({x},{y}) scale({s})"><g id="{id}"><path d="M-110 -10 C -120 -70 120 -70 110 -10 C 120 50 -120 50 -110 -10 Z" fill="{c}" stroke="{WOOD}" stroke-width="6"/>'
            f'<circle cx="0" cy="-10" r="10" fill="{GOLD}" stroke="{WOOD}" stroke-width="4"/>'
            + "".join(f'<path d="M{a} {b} l {dx} {dy}" stroke="{GOLD}" stroke-width="6" stroke-linecap="round"/>' for a, b, dx, dy in ((-110, -10, -22, -10), (110, -10, 22, -10), (-110, -10, -22, 10), (110, -10, 22, 10)))
            + '</g></g>')
def mosque(x, y, s, id=""):
    return (f'<g transform="translate({x},{y}) scale({s})"><g id="{id}"><rect x="-90" y="-90" width="180" height="90" fill="{CREAM}" stroke="{WOOD}" stroke-width="5"/>'
            f'<path d="M-60 -90 C -60 -170 60 -170 60 -90 Z" fill="{GOLD}" stroke="{WOOD}" stroke-width="5"/><rect x="104" y="-170" width="26" height="170" fill="{CREAM}" stroke="{WOOD}" stroke-width="5"/>'
            f'<path d="M104 -170 L 117 -200 L 130 -170 Z" fill="{GOLD}" stroke="{WOOD}" stroke-width="4"/><path d="M-18 0 L -18 -40 C -18 -62 18 -62 18 -40 L 18 0 Z" fill="{TEAL}"/></g></g>')
HIDE_I = (f'<svg width="70" height="70" viewBox="0 0 100 100"><path d="M10 84 C 6 50 30 30 50 34 C 70 22 96 44 90 84 Z" fill="{TEAL}" stroke="{WOOD}" stroke-width="5"/>'
          f'<circle cx="34" cy="56" r="6" fill="#4f9a86"/><circle cx="62" cy="50" r="7" fill="#4f9a86"/><circle cx="70" cy="70" r="5" fill="#4f9a86"/></svg>')
SELL_I = (f'<svg width="70" height="70" viewBox="0 0 100 100">' + "".join(f'<ellipse cx="50" cy="{y}" rx="30" ry="10" fill="{GOLD}" stroke="{WOOD}" stroke-width="4"/>' for y in (78, 64, 50, 36)) + '</svg>')
THROW_I = (f'<svg width="70" height="70" viewBox="0 0 100 100"><path d="M14 80 C 30 20 70 14 88 40" fill="none" stroke="{RED}" stroke-width="7" stroke-linecap="round" stroke-dasharray="2 12"/>'
           f'<path d="M78 30 L 92 44 L 74 48 Z" fill="{RED}"/><circle cx="16" cy="80" r="10" fill="{WOOD}"/></svg>')

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
    for n, t0 in L.items(): snd(f"{n}.mp3", t0, 1.0, track=None if n in ARABIC else 1)   # Rafiq's lines on their own tracks: the ayah's quiet tail runs under b4
    snd("bed.mp3", 0, 0.07, END, track=2)                                   # a low hum under it all
    js = []; T = js.append
    IN = lambda sel, t, y=40, d=0.5: T(f'tl.fromTo("{sel}", {{opacity:0, y:{y}}}, {{opacity:1, y:0, duration:{d}, ease:"power3.out"}}, {t:.2f});')
    POP = lambda sel, t, s=0.6: T(f'tl.fromTo("{sel}", {{opacity:0, scale:{s}}}, {{opacity:1, scale:1, duration:0.45, ease:"back.out(1.4)", transformOrigin:"50% 50%"}}, {t:.2f});')
    def draw(sel, t, d=0.6): T(f'tl.fromTo("{sel}", {{strokeDashoffset:1}}, {{strokeDashoffset:0, duration:{d}, stagger:0.12, ease:"power2.inOut"}}, {t:.2f});')
    def pulse(sel, t, s=1.08): T(f'tl.fromTo("{sel}", {{scale:1}}, {{scale:{s}, duration:0.2, yoyo:true, repeat:1, ease:"power2.out", transformOrigin:"50% 50%", immediateRender:false}}, {t:.2f});')
    def flop(sel, t):            # standing → tips over onto the mattress: eases in as it falls, then a small settle
        T(f'tl.fromTo("{sel}", {{rotation:0}}, {{rotation:-90, duration:0.45, ease:"power2.in", transformOrigin:"50% 100%", immediateRender:false}}, {t:.2f});')
        T(f'tl.fromTo("{sel}", {{y:0}}, {{y:-14, duration:0.18, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}}, {t + 0.45:.2f});')
    def zzz(sel, t):
        T(f'tl.fromTo("{sel} text", {{opacity:0, y:20}}, {{opacity:1, y:-40, duration:0.9, stagger:0.25, ease:"power2.out", immediateRender:false}}, {t:.2f});')
    def scene(sel, t0, t1):
        if t0 > 0: T(f'tl.fromTo("{sel}", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.45, ease:"power3.out"}}, {t0:.2f});')
        if t1: T(f'tl.to("{sel}", {{opacity:0, y:-60, duration:0.35, ease:"power2.in"}}, {t1:.2f});'); snd("whoosh.wav", t1 - 0.05, 0.3)

    # the night lives the whole time: the stars twinkle, the moon drifts, the lanterns glow
    T(f'tl.fromTo("#stars", {{opacity:0.35}}, {{opacity:0.95, duration:{END / 2:.2f}, yoyo:true, repeat:1, ease:"sine.inOut"}}, 0);')
    T(f'tl.fromTo("#moon", {{x:0, y:0}}, {{x:30, y:16, duration:{END:.2f}, ease:"sine.inOut"}}, 0);')
    T(f'tl.fromTo("#town", {{x:0}}, {{x:-60, duration:{END:.2f}, ease:"sine.inOut"}}, 0);')
    T(f'tl.fromTo(".lamp", {{opacity:0.5}}, {{opacity:1, duration:1.6, yoyo:true, repeat:{int(END / 1.6)}, ease:"sine.inOut"}}, 0);')

    # 1 · the hook: MATTRESS on a rooftop; the sleeper flops onto it; an Arabic word; you don't know it
    S2 = L["matrah"] - 0.25
    fa = at("h1", "asleep"); flop("#p1", fa - 0.35); snd("thump.wav", fa + 0.1, 0.45); zzz("#z1", fa + 0.3)
    ab = at("h1", "arabic")
    POP("#tit", ab - 0.1, 0.7); snd("tap.wav", ab, 0.35)
    T(f'tl.fromTo("#ttl2", {{opacity:0, scale:1.6}}, {{opacity:1, scale:1, duration:0.45, ease:"back.out(1.4)"}}, {ab + 0.2:.2f});'); snd("impact.wav", ab + 0.2, 0.35, 1.2)
    dk = at("h1", "don't")
    POP("#qm", dk - 0.1, 0.4); snd("tick-lo.wav", dk, 0.45)
    scene("#s1", 0, S2 - 0.05)
    # 2 · مَطْرَح: something thrown down, a cushion you throw on the floor
    scene("#s2", S2, L["b2"] - 0.35)
    POP("#mw", L["matrah"] - 0.05, 0.7); snd("tick-lo.wav", L["matrah"], 0.4)
    th = at("b1", "thrown")
    POP("#mm", th - 0.05, 0.7); snd("tap.wav", th, 0.35)
    for i, k in enumerate(("cushion", "floor", "sleep")):
        w0 = at("b1", k)
        T(f'tl.fromTo("#cu{i}", {{opacity:0, y:-700, rotation:{(-1) ** i * 25}}}, {{opacity:1, y:0, rotation:0, duration:0.6, ease:"bounce.out"}}, {w0 - 0.3:.2f});'); snd("thump.wav", w0 + 0.15, 0.4)
    # 3 · the root ط ر ح, to throw; مَـ as in مَسْجِد: the place of; the place you throw yourself down
    S3 = L["b2"] - 0.1; scene("#s3", S3, L["b3"] - 0.35)
    rt = at("b2", "root")
    for i in range(3):
        T(f'tl.fromTo("#rl{i}", {{opacity:0, y:-200}}, {{opacity:1, y:0, duration:0.4, ease:"power3.out"}}, {rt - 0.15 + i * 0.14:.2f});'); snd("thump.wav", rt + i * 0.14, 0.3)
    POP("#rc", at("b2", "throw") - 0.05, 0.7); snd("tap.wav", at("b2", "throw"), 0.35)
    ma = at("b2", "ma", exact=True)
    T(f'tl.to(["#rtiles", "#rc"], {{opacity:0, y:-30, duration:0.3, ease:"power2.in"}}, {ma - 0.35:.2f});')
    POP("#pm", ma - 0.05, 0.6); snd("tap.wav", ma, 0.35)
    mj = at("b2", "masjid")
    POP("#pmas", mj - 0.1, 0.7); IN("#msq", mj - 0.2, 40); snd("flip.wav", mj, 0.35)
    pl = at("b2", "place")
    T(f'tl.to(".mpre", {{color:"{RED}", duration:0.3, ease:"power2.out"}}, {pl - 0.05:.2f});'); POP("#plc", pl - 0.05, 0.7); snd("shimmer.wav", pl, 0.3, 1.0)   # colour only: the letters stay joined
    yd = at("b2", "yourself")
    POP("#pmat", yd - 0.6, 0.7); snd("flip.wav", yd - 0.6, 0.35)
    flop("#p3", yd); snd("thump.wav", yd + 0.45, 0.45)
    # 4 · Sicily → materasso → materas → 1300s → mattress
    S4 = L["b3"] - 0.1; scene("#s4", S4, L["t1"] - 0.4)
    POP("#sic", at("b3", "sicily") - 0.1, 0.7); snd("thump.wav", at("b3", "sicily"), 0.35)
    for i, k in enumerate(("materasso", "materas")):
        w0 = at("b3", k, exact=True); POP(f"#wd{i}", w0 - 0.05, 0.7); snd("tap.wav", w0, 0.35)
        draw(f"#ar{i}", w0 + 0.5, 0.4)
    POP("#yr", at("b3", "1300s") - 0.05, 0.7); snd("tick-lo.wav", at("b3", "1300s"), 0.45)
    mt = at("b3", "mattress", last=True)
    IN("#wd2", mt - 0.15, 30); snd("shimmer.wav", mt, 0.35, 1.2); pulse("#wd2", mt + 0.45, 1.08)
    # 5 · your turn: ط ر ح in Yūsuf 12:9: hide / sell / throw? 3-2-1; the ayah; THROW!
    S5 = L["t1"] - 0.1; scene("#s5", S5, L["end"] - 0.45)
    IN("#yt", L["t1"], 20)
    rt = at("t1", "root")
    for i in range(3):
        T(f'tl.fromTo("#tl{i}", {{opacity:0, y:-200}}, {{opacity:1, y:0, duration:0.4, ease:"power3.out"}}, {rt - 0.15 + i * 0.14:.2f});'); snd("thump.wav", rt + i * 0.14, 0.3)
    ys = at("t1", "yusuf")
    T(f'tl.to("#tiles", {{opacity:0, y:-30, duration:0.3, ease:"power2.in"}}, {ys - 0.3:.2f});')
    POP("#aya", ys - 0.1, 0.8); snd("flip.wav", ys, 0.4)
    it = at("t1", "itrahoohu"); IN("#ee0", it - 0.1, 16); draw("#hl", it, 0.5); snd("tap.wav", it, 0.4)
    for i, (k, last) in enumerate((("hide", False), ("sell", False), ("throw", True))):
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
    hit = at("b4", "throw")
    T(f'tl.to("#ops", {{opacity:0, y:30, duration:0.25, ease:"power2.in"}}, {hit - 0.25:.2f});')
    T(f'tl.fromTo("#slam", {{opacity:0, scale:1.8}}, {{opacity:1, scale:1, duration:0.45, ease:"back.out(1.7)"}}, {hit:.2f});')   # the one slam
    T(f'tl.fromTo("#cam", {{x:-14}}, {{x:14, duration:0.05, yoyo:true, repeat:7, ease:"sine.inOut", immediateRender:false}}, {hit + 0.05:.2f});')
    T(f'tl.set("#cam", {{x:0}}, {hit + 0.5:.2f});')
    snd("impact.wav", hit - 0.03, 0.75, 1.6)
    T(f'tl.fromTo("#burst i", {{opacity:1, x:0, y:0, scale:0.4}}, {{opacity:0, x:(i) => [-300, -170, 0, 170, 300, -90, 90][i], y:(i) => [-80, -200, -260, -200, -80, 150, 150][i], scale:1.3, duration:0.9, ease:"power2.out", immediateRender:false}}, {hit + 0.05:.2f});')
    kl = at("b4", "kill")
    POP("#mean", kl - 0.1, 0.7); snd("tap.wav", kl, 0.4)
    # 6 · the ask: what do you say before you sleep? the sleeper under the moon
    S6 = L["end"] - 0.1; scene("#s6", S6, None)
    IN("#q", L["end"] + 0.1, 30)
    sl = at("end", "sleep")
    IN("#bed6", L["end"] + 0.2, 60); zzz("#z6", sl); snd("shimmer.wav", sl, 0.3, 1.2)
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

    rng = np.random.default_rng(11)
    stars = "".join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#fff6dc" opacity="{o:.2f}"/>' for x, y, r, o in
                    zip(rng.uniform(0, 1080, 90), rng.uniform(0, 1150, 90), rng.uniform(1, 3, 90), rng.uniform(0.3, 0.9, 90)))
    houses = ""
    for x, w, h in ((-60, 220, 300), (150, 180, 380), (320, 240, 260), (560, 200, 340), (750, 230, 290), (960, 220, 360)):
        top = 1520 - h
        houses += f'<rect x="{x}" y="{top}" width="{w}" height="{h + 420}" fill="{WALL}"/><rect x="{x - 8}" y="{top - 14}" width="{w + 16}" height="18" fill="{ROOF}"/>'
        houses += "".join(f'<rect class="lamp" x="{x + 30 + j * 70}" y="{top + 60 + r * 90}" width="34" height="46" rx="16" fill="#f4c46e"/>'
                          for r in range(2) for j in range(max(1, (w - 40) // 70)) if (r + j + x // 10) % 3 != 1)
    town = (f'<g id="town">{houses}<path d="M600 1180 C 600 1080 720 1080 720 1180 Z" fill="{WALL}"/><rect x="740" y="1000" width="30" height="190" fill="{WALL}"/>'
            f'<path d="M740 1000 L 755 960 L 770 1000 Z" fill="{WALL}"/></g>')
    sv = lambda inner: f'<svg class="full" viewBox="0 0 1080 1920">{inner}</svg>'
    arrow = lambda id, d: f'<path id="{id}" pathLength="1" d="{d}" fill="none" stroke="{GOLD}" stroke-width="7" stroke-linecap="round" stroke-dasharray="1" stroke-dashoffset="1"/>'
    tile = lambda id, ch, x, y, sz=190, fs=150: f'<div class="tile" id="{id}" style="left:{x}px;top:{y}px;width:{sz}px;height:{sz}px;line-height:{sz}px;font-size:{fs}px">{ch}</div>'
    zz = lambda id, x, y: f'<g id="{id}">' + "".join(f'<text x="{x + k * 40}" y="{y - k * 46}" font-family="CZ" font-size="{50 + k * 14}" fill="{CREAM}" opacity="0">z</text>' for k in range(3)) + '</g>'
    burst = "".join(f'<i style="position:absolute;left:520px;top:960px;width:40px;height:40px;border-radius:50%;background:{c};opacity:0"></i>' for c in (GOLD, CREAM, RED, GOLD, CREAM, RED, GOLD))
    roof = f'<rect x="60" y="1500" width="960" height="40" rx="10" fill="{ROOF}"/><rect x="60" y="1480" width="960" height="26" rx="8" fill="#4a4f86"/>'
    css = f"""
@font-face {{ font-family:"CZ"; src:url("assets/cinzel-latin-700-normal.woff2"); }}
@font-face {{ font-family:"AM"; src:url("assets/amiri-arabic-700-normal.woff2"); }}
@font-face {{ font-family:"KA"; src:url("assets/karla-latin-700-normal.woff2"); }}
* {{ margin:0; box-sizing:border-box; }} html, body {{ width:1080px; height:1920px; overflow:hidden; background:#000; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; background:linear-gradient(#0e1230 0%, #1d2250 40%, #343a72 70%, #4a4f86 100%); font-family:KA; color:{CREAM}; }}
#cam {{ position:absolute; inset:0; }}
svg.full {{ position:absolute; left:0; top:0; width:1080px; height:1920px; overflow:visible; }}
.sc {{ position:absolute; inset:0; opacity:0; }} #s1 {{ opacity:1; }}
.t {{ position:absolute; left:0; right:0; text-align:center; opacity:0; }}
.cz {{ font-family:CZ; letter-spacing:.06em; color:{GOLD}; text-shadow:0 4px 0 {WOOD}, 0 10px 30px rgba(0,0,0,.5); }}
.am {{ font-family:AM; direction:rtl; color:{CREAM}; text-shadow:0 6px 0 {TEAL}, 0 14px 40px rgba(0,0,0,.45); line-height:1.3; }}
.pill {{ display:inline-flex; align-items:center; gap:14px; padding:8px 30px; border-radius:999px; background:rgba(14,20,44,.88); border:2px solid rgba(242,196,107,.6); font-family:KA; color:{CREAM}; }}
.cap {{ position:absolute; left:70px; right:70px; top:1600px; text-align:center; font-family:KA; font-size:50px; line-height:1.2; color:#fff; text-shadow:0 3px 0 rgba(0,0,0,.6), 0 0 18px rgba(0,0,0,.6); opacity:0; }}
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
.pair {{ position:absolute; width:420px; text-align:center; opacity:0; }}
.pair .w {{ display:inline-block; font-family:AM; font-size:124px; line-height:1.25; direction:rtl; color:{CREAM}; text-shadow:0 6px 0 {TEAL}, 0 14px 40px rgba(0,0,0,.45); }}
.pair .w .mpre {{ color:{CREAM}; }}
.pair .g {{ font-family:KA; font-size:36px; line-height:1.2; color:{GOLD}; margin-top:26px; }}
#logo {{ position:absolute; top:62px; left:50%; transform:translateX(-50%); display:flex; justify-content:center; gap:12px; align-items:center; z-index:5; padding:6px 22px 6px 8px; border-radius:22px; background:rgba(14,20,44,.55); }}
#logo .tl {{ position:relative; width:58px; height:58px; border-radius:16px; background:{CREAM}; display:grid; place-items:center; }}
#logo .tl span {{ font-family:AM; font-size:38px; color:{INK}; margin-top:-6px; }} #logo .tl em {{ position:absolute; right:9px; top:8px; width:9px; height:9px; border-radius:50%; background:{RED}; }}
#logo b {{ font-family:AM; font-size:44px; color:{CREAM}; }}
"""
    body = f"""<div id="cam">
<svg class="full" viewBox="0 0 1080 1920"><g id="stars">{stars}</g>
 <g id="moon"><circle cx="112" cy="152" r="88" fill="#f6e7b8" opacity=".12"/><circle cx="112" cy="152" r="54" fill="#f6e7b8"/><circle cx="134" cy="138" r="48" fill="#141a40"/></g>
 {town}
</svg>
<div id="logo"><span class="tl"><span>ر</span><em></em></span><b>رَفِيق</b></div>
<div class="sc" id="s1">
 <div class="t cz" id="kick" style="top:180px;font-size:44px;opacity:1">THE STORY OF A WORD</div>
 <div class="t cz" id="ttl" style="top:250px;font-size:150px;opacity:1">MATTRESS</div>
 <div class="t" id="tit" style="top:470px"><span class="pill" style="font-size:44px">an Arabic word</span></div>
 <div class="t am" id="ttl2" style="top:590px;font-size:180px;color:{GOLD}">مَطْرَح</div>
 {sv(roof + mattress(540, 1478, 1.25) + figure(640, 1400, 1.3, NAVY, "p1") + zz("z1", 720, 1270))}
 <div class="t cz" id="qm" style="top:940px;left:700px;right:auto;width:200px;font-size:120px;color:{CREAM}">?</div>
</div>
<div class="sc" id="s2">
 <div class="t am" id="mw" style="top:170px;font-size:210px;color:{GOLD}">مَطْرَح</div>
 <div class="t" id="mm" style="top:470px"><span class="pill" style="font-size:48px">maṭraḥ = <b style="color:{GOLD}">something thrown down</b></span></div>
 {sv(roof + cushion(320, 1440, 1.0, RED, "cu0") + cushion(560, 1440, 1.0, TEAL, "cu1") + cushion(790, 1440, 1.0, GOLD, "cu2"))}
</div>
<div class="sc" id="s3">
 <div id="rtiles">{tile("rl0", "ط", 745, 230)}{tile("rl1", "ر", 445, 230)}{tile("rl2", "ح", 145, 230)}</div>
 <div class="t" id="rc" style="top:470px"><span class="pill" style="font-size:52px">the root = <b style="color:{GOLD}">to throw</b></span></div>
 <div class="t" id="pm" style="top:180px"><span class="pill" style="font-size:52px"><b style="font-family:AM;font-size:70px;color:{GOLD}">مَـ</b> at the front</span></div>
 <div class="pair" id="pmas" style="left:560px;top:350px"><div class="w"><span class="mpre">مَ&zwj;</span>&zwj;سْجِد</div><div class="g">the place of sujood</div></div>
 <div class="pair" id="pmat" style="left:100px;top:350px"><div class="w"><span class="mpre">مَ&zwj;</span>&zwj;طْرَح</div><div class="g">the place you throw yourself down</div></div>
 <div class="t" id="plc" style="top:720px"><span class="pill" style="font-size:52px">مَـ = <b style="color:{GOLD}">the place of</b></span></div>
 {sv('<g id="msq" opacity="0" style="opacity:0">' + mosque(770, 1060, 0.9) + '</g>' + roof + mattress(540, 1478, 1.25) + figure(640, 1400, 1.3, "#7a2d3a", "p3"))}
</div>
<div class="sc" id="s4">
 <div class="t" id="sic" style="top:190px"><span class="pill" style="font-size:52px">via <b style="color:{GOLD}">Sicily</b></span></div>
 <div class="wd" id="wd0" style="top:300px"><span style="font-size:76px"><b>ITALIAN</b>materasso</span></div>
 {sv(arrow("ar0", "M540 520 L 540 590") + arrow("ar1", "M540 810 L 540 880"))}
 <div class="wd" id="wd1" style="top:610px"><span style="font-size:76px"><b>FRENCH</b>materas</span></div>
 <div class="t" id="yr" style="top:905px"><span class="pill" style="font-size:46px;font-family:CZ;color:{GOLD}">1300s</span></div>
 <div class="wd" id="wd2" style="top:990px"><span style="font-size:104px"><b>ENGLISH</b>MATTRESS</span></div>
</div>
<div class="sc" id="s5">
 <div class="t cz" id="yt" style="top:170px;font-size:76px">YOUR TURN</div>
 <div id="tiles">{tile("tl0", "ط", 745, 320)}{tile("tl1", "ر", 445, 320)}{tile("tl2", "ح", 145, 320)}</div>
 <div class="card" id="aya" style="top:280px"><div class="aa" style="font-size:66px">اقْتُلُوا يُوسُفَ أَوِ <span class="hlw">اطْرَحُوهُ<svg viewBox="0 0 100 60" preserveAspectRatio="none"><ellipse id="hl" pathLength="1" cx="50" cy="32" rx="48" ry="27" fill="none" stroke="{RED}" stroke-dasharray="1" stroke-dashoffset="1" vector-effect="non-scaling-stroke" style="stroke-width:7px"/></svg></span> أَرْضًا</div>
  <div style="position:relative;height:46px"><div class="ee" id="ee0" style="position:absolute;left:0;right:0;opacity:0">Kill Yūsuf, or ___ to some land</div><div class="ee" id="ee1" style="position:absolute;left:0;right:0;opacity:0">Kill Yūsuf, or throw him out to some land</div></div>
  <small>the Qur’an · Yūsuf 12:9 · his brothers’ plan</small></div>
 <div id="ops" style="position:absolute;left:0;right:0;top:800px"><div class="op" id="op0">{HIDE_I}<span>hide him</span></div><div class="op" id="op1">{SELL_I}<span>sell him</span></div><div class="op" id="op2">{THROW_I}<span>throw him</span></div></div>
 <div id="cd">3</div>
 <div class="t cz" id="slam" style="top:790px;font-size:150px;line-height:1.1">THROW!</div>
 <div class="t" id="mean" style="top:1010px"><span class="pill" style="font-size:42px"><b style="font-family:AM;font-size:60px;color:{GOLD}">اطْرَحُوهُ</b> throw him out</span></div>
 <div id="burst">{burst}</div>
</div>
<div class="sc" id="s6">
 <div class="t" id="q" style="top:190px"><div class="cz" style="display:inline-block;padding:18px 40px 12px;border-radius:28px;background:rgba(14,20,44,.82);font-size:62px;line-height:1.25">WHAT DO YOU SAY<br/>BEFORE YOU SLEEP?</div></div>
 {sv('<g id="bed6" opacity="0" style="opacity:0">' + roof + mattress(540, 1478, 1.25) + sleeper(560, 1404, 1.0) + '</g>' + zz("z6", 470, 1250))}
 <div class="t" id="url" style="top:700px"><span class="pill" style="font-size:50px;background:{TEAL}">rafiq-arabic.com</span></div>
 <div class="t" id="arr" style="top:560px;font-size:80px">👇</div>
</div>
</div>"""
    body = body[:-6] + caps + "</div>"
    open(os.path.join(out, "index.html"), "w").write(f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" /><title>mattress</title>
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
