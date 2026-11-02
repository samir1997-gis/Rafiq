#!/usr/bin/env python3
"""h6-zero, the story of a word #6, in the drawn format of h5-safari (#317): the lines in brag-quiz/voice/zero-lines.json told with
full-screen drawings over Baghdad at night, numbers drifting in the sky. Cinzel for the titles, Amiri for the Arabic, every move on its word,
eased (MOTION-STYLE.md):
  1 "Zero comes from an Arabic word… and so does the word for a secret code": ZERO, a giant 0, صِفْر, a padlock
  2 صِفْر (Rafiq) · "empty… Indian numbers reached Baghdad… the sign for nothing": an empty box, ١ to ٩ and the empty place ٠
  3 "In 1202, Fibonacci took it to Italy as zephirum… zefiro… zero": Baghdad → Pisa, the words shrinking down to ZERO
  4 "a second road: cifra… cipher… zero, any number, a secret code": the fork in the road, 0 → 1 2 3 → the padlock
  5 your turn: ص ف ر, al-Baqarah 2:69, empty / zero / yellow? 3-2-1; the ayah (Rafiq); "YELLOW!", a yellow cow, صِفْر vs صَفْراء
  6 the ask: your favourite number? zero doesn't count. Then the cream end card.

  python3 brag-quiz/reels/zero/build.py    then  cd brag-quiz/reels/zero/out/v && npx hyperframes render -o ../raw.mp4
"""
import json, os, re, shutil, subprocess
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
V6 = os.path.join(ROOT, "brag-output-v6/composition/assets"); VO = os.path.join(ROOT, "brag-quiz/voice/zero")
INK, CREAM, GOLD, TEAL, RED, WOOD, YEL = "#17262B", "#F6EBD3", "#F2C46B", "#2E7263", "#B4322A", "#8A5A2B", "#FFD23F"
CITY, CITY2 = "#141a3a", "#0c1028"
dur = lambda f: float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))
mp3 = lambda n: os.path.join(VO, n + ".mp3")
def words(n):
    ws = json.load(open(os.path.join(VO, n + ".words.json")))
    return [(w[0], w[1], w[2] if len(w) > 2 else (ws[i + 1][1] if i + 1 < len(ws) else w[1] + 0.45)) for i, w in enumerate(ws)]
ORDER = [("h1", 0.3), ("sifr", 0.35), ("b1", 0.25), ("b2", 0.45), ("b3", 0.5), ("t1", 0.55), ("ayah", 3.9), ("b4", 0.2), ("end", 0.8)]
ARABIC = ("sifr", "ayah")
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

def padlock(x, y, s, id=""):                                   # a padlock with a combination dial; the outer <g> places it, the inner one moves
    return (f'<g transform="translate({x},{y}) scale({s})"><g id="{id}"><path d="M-60 -60 L -60 -120 C -60 -200 60 -200 60 -120 L 60 -60" fill="none" stroke="#c9ced6" stroke-width="26"/>'
            f'<rect x="-100" y="-70" width="200" height="170" rx="26" fill="{GOLD}" stroke="{WOOD}" stroke-width="8"/>'
            f'<g class="dial"><circle cx="0" cy="15" r="52" fill="{CREAM}" stroke="{WOOD}" stroke-width="6"/>'
            + "".join(f'<path d="M0 -30 L 0 -22" stroke="{INK}" stroke-width="5" transform="translate(0,15) rotate({a})"/>' for a in range(0, 360, 36))
            + f'<text x="0" y="40" text-anchor="middle" font-family="CZ" font-size="60" fill="{INK}">0</text></g></g></g>')
def cow(x, y, s, id=""):                                       # a faceless cow, bright yellow
    c = YEL
    return (f'<g transform="translate({x},{y}) scale({s})"><g id="{id}">'
            + "".join(f'<rect x="{lx}" y="-60" width="26" height="80" rx="10" fill="{c}" stroke="{WOOD}" stroke-width="6"/>' for lx in (-100, -60, 50, 86))
            + f'<path d="M-130 -70 C -130 -150 120 -160 130 -80 C 134 -40 110 -30 0 -30 C -110 -30 -130 -40 -130 -70 Z" fill="{c}" stroke="{WOOD}" stroke-width="7"/>'
            f'<path d="M-130 -100 C -160 -90 -170 -60 -160 -30" fill="none" stroke="{WOOD}" stroke-width="7" stroke-linecap="round"/>'
            f'<ellipse cx="166" cy="-118" rx="50" ry="40" fill="{c}" stroke="{WOOD}" stroke-width="7"/>'
            f'<path d="M140 -150 C 128 -186 150 -196 156 -170 M 192 -150 C 204 -186 182 -196 176 -170" fill="none" stroke="{CREAM}" stroke-width="10" stroke-linecap="round"/>'
            f'<ellipse cx="118" cy="-140" rx="22" ry="11" fill="{c}" stroke="{WOOD}" stroke-width="6" transform="rotate(-25 118 -140)"/>'
            f'<ellipse cx="186" cy="-94" rx="26" ry="16" fill="#f4b183" stroke="{WOOD}" stroke-width="5"/></g></g>')
EMPTY = f'<svg width="70" height="70" viewBox="0 0 100 100"><rect x="14" y="24" width="72" height="60" rx="8" fill="none" stroke="{WOOD}" stroke-width="8" stroke-dasharray="12 9"/></svg>'
ZERO_I = f'<svg width="70" height="70" viewBox="0 0 100 100"><ellipse cx="50" cy="52" rx="26" ry="36" fill="none" stroke="{TEAL}" stroke-width="12"/></svg>'
YEL_I = f'<svg width="70" height="70" viewBox="0 0 100 100"><circle cx="50" cy="52" r="34" fill="{YEL}" stroke="{WOOD}" stroke-width="6"/></svg>'

def build():
    out = os.path.join(HERE, "out", "v"); a = os.path.join(out, "assets")
    if os.path.exists(out): shutil.rmtree(out)
    os.makedirs(a)
    for f in ("karla-latin-700-normal.woff2",): shutil.copy(os.path.join(V6, "fonts", f), a)
    for f in ("cinzel-latin-700-normal.woff2", "amiri-arabic-700-normal.woff2"): shutil.copy(os.path.join(ROOT, "brag-quiz/fonts", f), a)
    shutil.copy(os.path.join(V6, "lib/gsap.min.js"), a)
    for f in ("shimmer.wav", "tick-lo.wav", "thump.wav", "whoosh.wav", "impact.wav", "drone.wav", "flip.wav", "type.wav"): shutil.copy(os.path.join(ROOT, "brag-quiz/sfx/soft", f), a)
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
    def scene(sel, t0, t1):
        if t0 > 0: T(f'tl.fromTo("{sel}", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.45, ease:"power3.out"}}, {t0:.2f});')
        if t1: T(f'tl.to("{sel}", {{opacity:0, y:-60, duration:0.35, ease:"power2.in"}}, {t1:.2f});'); snd("whoosh.wav", t1 - 0.05, 0.3)

    # the sky lives the whole time: the stars drift, the numbers float up, the moon rises a little
    T(f'tl.fromTo("#stars", {{x:0}}, {{x:-120, duration:{END:.2f}, ease:"sine.inOut"}}, 0);')
    T(f'tl.fromTo("#nums", {{y:0}}, {{y:-260, duration:{END:.2f}, ease:"sine.inOut"}}, 0);')

    # 1 · the hook: ZERO, the giant 0; from Arabic; the secret code
    T(f'tl.fromTo("#big0", {{rotation:-8}}, {{rotation:8, duration:1.2, yoyo:true, repeat:3, ease:"sine.inOut", transformOrigin:"50% 50%"}}, 0);')
    ab = at("h1", "arabic")
    POP("#from", ab - 0.1, 0.7); snd("tap.wav", ab, 0.35)
    T(f'tl.fromTo("#ttl2", {{opacity:0, scale:1.6}}, {{opacity:1, scale:1, duration:0.45, ease:"back.out(1.4)"}}, {ab + 0.2:.2f});'); snd("impact.wav", ab + 0.2, 0.35, 1.2)
    sc = at("h1", "secret")
    T(f'tl.to("#big0", {{opacity:0, scale:0.5, duration:0.35, ease:"power2.in", transformOrigin:"50% 50%"}}, {sc - 0.4:.2f});')
    POP("#lk1", sc - 0.1, 0.4); snd("thump.wav", sc, 0.4)
    T(f'tl.fromTo("#lk1 .dial", {{rotation:0}}, {{rotation:-200, duration:1.0, ease:"power2.inOut", transformOrigin:"50% 50%"}}, {sc + 0.2:.2f});'); snd("type.wav", sc + 0.2, 0.3, 0.9)
    IN("#code", at("h1", "code") + 0.1, 20)
    S2 = L["sifr"] - 0.25; scene("#s1", 0, S2 - 0.05)
    # 2 · صِفْر: empty; Indian numbers reach Baghdad; the sign for nothing
    scene("#s2", S2, L["b2"] - 0.35)
    POP("#sw", L["sifr"] - 0.05, 0.7); snd("tick-lo.wav", L["sifr"], 0.4)
    em = at("b1", "empty")
    POP("#se", em - 0.05, 0.7); POP("#box", em + 0.1, 0.6); snd("tap.wav", em, 0.35)
    ind = at("b1", "indian")
    T(f'tl.to("#box", {{opacity:0, scale:0.7, duration:0.3, ease:"power2.in", transformOrigin:"50% 50%"}}, {ind - 0.3:.2f});')
    T(f'tl.fromTo("#digits span", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.35, stagger:0.09, ease:"back.out(1.6)"}}, {ind:.2f});'); snd("type.wav", ind, 0.3, 1.0)
    bg = at("b1", "baghdad")
    T(f'tl.to(".win", {{opacity:1, duration:0.5, stagger:0.05, ease:"power2.out"}}, {bg - 0.1:.2f});'); POP("#bgd", bg - 0.05, 0.7); snd("shimmer.wav", bg, 0.3, 1.2)
    no = at("b1", "nothing")
    POP("#slot", no - 0.1, 0.5); snd("tick-lo.wav", no, 0.45)
    POP("#slotl", at("b1", "sifr", last=True) - 0.05, 0.7); snd("tap.wav", at("b1", "sifr", last=True), 0.35)
    # 3 · 1202: Fibonacci, Baghdad → Pisa; zephirum → zefiro → ZERO
    S3 = L["b2"] - 0.1; scene("#s3", S3, L["b3"] - 0.35)
    POP("#yr", at("b2", "1202") - 0.05, 0.6); snd("tick-lo.wav", at("b2", "1202"), 0.45)
    fb = at("b2", "fibonacci")
    POP("#pt0", fb - 0.1, 0.6); draw("#route", fb + 0.1, 1.0); snd("swoosh.wav", fb + 0.1, 0.35)
    POP("#pt1", at("b2", "italy") - 0.05, 0.6); snd("tap.wav", at("b2", "italy"), 0.35)
    for i, k in enumerate(("zephirum", "zefiro")):
        w0 = at("b2", k); POP(f"#w{i}", w0 - 0.05, 0.7); snd("tap.wav", w0, 0.35)
        draw(f"#ar{i}", w0 + 0.4, 0.4)
    zr = at("b2", "zero")
    T(f'tl.fromTo("#w2", {{opacity:0, scale:1.6}}, {{opacity:1, scale:1, duration:0.45, ease:"back.out(1.6)"}}, {zr - 0.05:.2f});'); snd("impact.wav", zr, 0.35, 1.2)
    # 4 · the second road: cifra → cipher; zero → any number → a secret code
    S4 = L["b3"] - 0.1; scene("#s4", S4, L["t1"] - 0.4)
    draw("#fork path", L["b3"] + 0.1, 0.9)
    POP("#rd", at("b3", "second") - 0.05, 0.7); snd("tap.wav", at("b3", "second"), 0.35)
    POP("#cf", at("b3", "cifra") - 0.05, 0.7); snd("tap.wav", at("b3", "cifra"), 0.35)
    POP("#cp", at("b3", "cipher") - 0.05, 0.7); snd("tick-lo.wav", at("b3", "cipher"), 0.45)
    for i, (k, last) in enumerate((("zero", False), ("number", False), ("code", False))):
        w0 = at("b3", k, last); POP(f"#m{i}", w0 - 0.1, 0.6); snd("tap.wav", w0, 0.35)
    T(f'tl.fromTo("#lk2 .dial", {{rotation:0}}, {{rotation:240, duration:1.0, ease:"power2.inOut", transformOrigin:"50% 50%"}}, {at("b3", "code") + 0.2:.2f});'); snd("type.wav", at("b3", "code") + 0.2, 0.3, 0.9)
    # 5 · your turn: ص ف ر in al-Baqarah 2:69; empty / zero / yellow? 3-2-1; the ayah; YELLOW!
    S5 = L["t1"] - 0.1; scene("#s5", S5, L["end"] - 0.45)
    IN("#yt", L["t1"], 20)
    tl3 = at("t1", "three")
    for i in range(3):
        T(f'tl.fromTo("#tl{i}", {{opacity:0, y:-200}}, {{opacity:1, y:0, duration:0.4, ease:"power3.out"}}, {tl3 - 0.15 + i * 0.14:.2f});'); snd("thump.wav", tl3 + i * 0.14, 0.3)
    T(f'tl.to("#tiles", {{opacity:0, y:-30, duration:0.3, ease:"power2.in"}}, {at("t1", "albaqarah") - 0.3:.2f});')
    POP("#aya", at("t1", "albaqarah") - 0.1, 0.8); snd("flip.wav", at("t1", "albaqarah"), 0.4)
    cw = at("t1", "cow"); IN("#ee0", cw - 0.1, 16); draw("#hl", cw, 0.5); snd("tap.wav", cw, 0.4)
    for i, k in enumerate(("empty", "zero", "yellow")):
        w0 = at("t1", k); POP(f"#op{i}", w0 - 0.05, 0.8); snd("tap.wav", w0, 0.3)
    c0 = round(L["t1"] + spoken("t1") + 0.3, 2)
    for k, nm in enumerate(("3", "2", "1")):
        T(f'tl.set("#cd", {{textContent:"{nm}", opacity:1}}, {c0 + k:.2f});'); T(f'tl.fromTo("#cd", {{scale:1.4}}, {{scale:1, duration:0.35, ease:"power3.out"}}, {c0 + k:.2f});')
        snd("click.wav", c0 + k, 1.0); snd("tick-lo.wav", c0 + k, 0.5)
    rv = c0 + 3
    T(f'tl.to("#cd", {{opacity:0, duration:0.2, ease:"power2.in"}}, {rv - 0.1:.2f});')
    T(f'tl.to("#op2", {{backgroundColor:"{YEL}", scale:1.08, duration:0.3, ease:"back.out(1.4)"}}, {rv:.2f});'); snd("tick-lo.wav", rv, 0.45)
    T(f'tl.to(["#op0", "#op1"], {{opacity:0.3, duration:0.3, ease:"power2.in"}}, {rv:.2f});')
    T(f'tl.to("#ee0", {{opacity:0, duration:0.2, ease:"power2.in"}}, {L["ayah"] + 0.2:.2f});'); IN("#ee1", L["ayah"] + 0.4, 16)
    hit = at("b4", "yellow")
    T(f'tl.to("#ops", {{opacity:0, y:30, duration:0.25, ease:"power2.in"}}, {hit - 0.25:.2f});')
    T(f'tl.fromTo("#slam", {{opacity:0, scale:1.8}}, {{opacity:1, scale:1, duration:0.45, ease:"back.out(1.7)"}}, {hit:.2f});')   # the one slam
    T(f'tl.fromTo("#cam", {{x:-14}}, {{x:14, duration:0.05, yoyo:true, repeat:7, ease:"sine.inOut", immediateRender:false}}, {hit + 0.05:.2f});')
    T(f'tl.set("#cam", {{x:0}}, {hit + 0.5:.2f});')
    snd("impact.wav", hit - 0.03, 0.75, 1.6)
    T(f'tl.fromTo("#wash", {{opacity:0}}, {{opacity:0.55, duration:0.15, yoyo:true, repeat:1, ease:"power2.out"}}, {hit:.2f});')
    T(f'tl.fromTo("#burst i", {{opacity:1, x:0, y:0, scale:0.4}}, {{opacity:0, x:(i) => [-300, -170, 0, 170, 300, -90, 90][i], y:(i) => [-80, -200, -260, -200, -80, 150, 150][i], scale:1.3, duration:0.9, ease:"power2.out", immediateRender:false}}, {hit + 0.05:.2f});')
    bc = at("b4", "cow")
    T(f'tl.fromTo("#cw", {{opacity:0, x:-500}}, {{opacity:1, x:0, duration:0.8, ease:"power3.out"}}, {at("b4", "bright") - 0.3:.2f});'); snd("swoosh.wav", at("b4", "bright") - 0.2, 0.35)
    T(f'tl.fromTo("#cw", {{y:0}}, {{y:-14, duration:0.2, yoyo:true, repeat:3, ease:"sine.inOut", immediateRender:false}}, {bc:.2f});')
    sl = at("b4", "letters")
    POP("#pr0", sl - 0.2, 0.6); snd("tap.wav", sl - 0.15, 0.35)
    POP("#pr1", at("b4", "different") - 0.1, 0.6); snd("tick-lo.wav", at("b4", "different"), 0.45)
    # 6 · the ask: your favourite number; zero doesn't count
    S6 = L["end"] - 0.1; scene("#s6", S6, None)
    IN("#q", L["end"] + 0.1, 30)
    T(f'tl.fromTo("#fav span", {{opacity:0, y:50}}, {{opacity:1, y:0, duration:0.4, stagger:0.08, ease:"back.out(1.6)"}}, {at("end", "number") - 0.2:.2f});'); snd("type.wav", at("end", "number") - 0.1, 0.3, 0.8)
    T(f'tl.fromTo("#fav span", {{y:0}}, {{y:-16, duration:0.3, yoyo:true, repeat:5, stagger:0.06, ease:"sine.inOut", immediateRender:false}}, {at("end", "number") + 0.4:.2f});')
    cm = at("end", "comment")
    POP("#url", cm - 0.1, 0.8); snd("tap.wav", cm, 0.4)
    T(f'tl.fromTo("#arr", {{opacity:0, y:0}}, {{opacity:1, y:18, duration:0.4, yoyo:true, repeat:3, ease:"sine.inOut"}}, {cm:.2f});')
    zc = at("end", "zero")
    POP("#z0", zc - 0.1, 0.5); draw("#zx path", at("end", "count") - 0.1, 0.35); snd("tick-lo.wav", at("end", "count"), 0.5)

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

    rng = np.random.default_rng(5)
    stars = "".join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#fff6dc" opacity="{o:.2f}"/>' for x, y, r, o in
                    zip(rng.uniform(0, 1200, 90), rng.uniform(0, 1250, 90), rng.uniform(1, 3, 90), rng.uniform(0.25, 0.85, 90)))
    glyphs = "0123456789٠١٢٣٤٥٦٧٨٩"
    nums = "".join(f'<text x="{x:.0f}" y="{y:.0f}" font-family="{"AM" if c in "٠١٢٣٤٥٦٧٨٩" else "CZ"}" font-size="{sz:.0f}" fill="{GOLD}" opacity="{o:.2f}" text-anchor="middle">{c}</text>'
                   for x, y, sz, o, c in zip(rng.uniform(40, 1040, 26), rng.uniform(200, 1700, 26), rng.uniform(40, 90, 26), rng.uniform(0.07, 0.16, 26), rng.choice(list(glyphs), 26)))
    def dome(x, w, h, base, c):
        return f'<path d="M{x - w} {base} C {x - w} {base - h} {x - w * 0.15} {base - h * 1.1} {x} {base - h * 1.35} C {x + w * 0.15} {base - h * 1.1} {x + w} {base - h} {x + w} {base} Z" fill="{c}"/>'
    def minaret(x, w, top, c):
        return (f'<rect x="{x - w}" y="{top}" width="{w * 2}" height="{1920 - top}" fill="{c}"/><rect x="{x - w - 10}" y="{top + 60}" width="{w * 2 + 20}" height="14" fill="{c}"/>'
                f'<path d="M{x - w} {top} L {x} {top - 70} L {x + w} {top} Z" fill="{c}"/>')
    city = ("".join(dome(x, w, h, 1560, CITY) for x, w, h in ((120, 110, 90), (420, 150, 120), (760, 120, 100), (1010, 100, 80)))
            + minaret(270, 22, 1240, CITY) + minaret(920, 18, 1290, CITY) + f'<rect x="-20" y="1540" width="1120" height="400" fill="{CITY}"/>'
            + "".join(f'<rect class="win" x="{x}" y="{y}" width="16" height="26" rx="8" fill="{GOLD}" opacity=".25"/>' for x, y in ((380, 1580), (430, 1580), (740, 1590), (790, 1590), (100, 1600), (1000, 1600)))
            + "".join(dome(x, w, h, 1700, CITY2) for x, w, h in ((260, 170, 130), (640, 210, 150), (980, 140, 110)))
            + minaret(470, 26, 1330, CITY2) + f'<rect x="-20" y="1690" width="1120" height="260" fill="{CITY2}"/>'
            + "".join(f'<rect class="win" x="{x}" y="{y}" width="14" height="22" rx="7" fill="{GOLD}" opacity=".25"/>' for x, y in ((600, 1740), (660, 1740), (720, 1740), (230, 1750), (290, 1750))))
    arrow = lambda id, d, c=GOLD: f'<path id="{id}" pathLength="1" d="{d}" fill="none" stroke="{c}" stroke-width="7" stroke-linecap="round" stroke-dasharray="1" stroke-dashoffset="1"/>'
    dots = lambda id, d: f'<path id="{id}" pathLength="1" d="{d}" fill="none" stroke="{CREAM}" stroke-width="8" stroke-linecap="round" stroke-dasharray="1" stroke-dashoffset="1" opacity=".85"/>'
    sv = lambda inner: f'<svg class="full" viewBox="0 0 1080 1920">{inner}</svg>'
    tile = lambda id, ch, x, y, sz=190, fs=150: f'<div class="tile" id="{id}" style="left:{x}px;top:{y}px;width:{sz}px;height:{sz}px;line-height:{sz}px;font-size:{fs}px">{ch}</div>'
    burst = "".join(f'<i style="position:absolute;left:520px;top:960px;width:40px;height:40px;border-radius:50%;background:{c};opacity:0"></i>' for c in (GOLD, CREAM, RED, YEL, CREAM, RED, YEL))
    css = f"""
@font-face {{ font-family:"CZ"; src:url("assets/cinzel-latin-700-normal.woff2"); }}
@font-face {{ font-family:"AM"; src:url("assets/amiri-arabic-700-normal.woff2"); }}
@font-face {{ font-family:"KA"; src:url("assets/karla-latin-700-normal.woff2"); }}
* {{ margin:0; box-sizing:border-box; }} html, body {{ width:1080px; height:1920px; overflow:hidden; background:#000; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; background:linear-gradient(#0b0f26 0%, #151c45 40%, #26306a 75%, #3d3f78 100%); font-family:KA; color:{CREAM}; }}
#cam {{ position:absolute; inset:0; }}
#wash {{ position:absolute; inset:0; background:{YEL}; opacity:0; }}
svg.full {{ position:absolute; left:0; top:0; width:1080px; height:1920px; overflow:visible; }}
.sc {{ position:absolute; inset:0; opacity:0; }} #s1 {{ opacity:1; }}
.t {{ position:absolute; left:0; right:0; text-align:center; opacity:0; }}
.cz {{ font-family:CZ; letter-spacing:.06em; color:{GOLD}; text-shadow:0 4px 0 {WOOD}, 0 10px 30px rgba(0,0,0,.5); }}
.am {{ font-family:AM; direction:rtl; color:{CREAM}; text-shadow:0 6px 0 {TEAL}, 0 14px 40px rgba(0,0,0,.45); line-height:1.3; }}
.pill {{ display:inline-flex; align-items:center; gap:14px; padding:8px 30px; border-radius:999px; background:rgba(14,18,44,.88); border:2px solid rgba(242,196,107,.6); font-family:KA; color:{CREAM}; }}
.cap {{ position:absolute; left:70px; right:70px; top:1580px; text-align:center; font-family:KA; font-size:50px; line-height:1.2; color:#fff; text-shadow:0 3px 0 rgba(0,0,0,.6), 0 0 18px rgba(0,0,0,.6); opacity:0; }}
.cap span {{ display:inline-block; opacity:0; }}
.card {{ position:absolute; left:70px; right:70px; padding:26px 30px 22px; border-radius:20px; background:#f3e3c0; color:{INK}; text-align:center; opacity:0;
  box-shadow:0 24px 50px rgba(0,0,0,.4), inset 0 0 0 6px #e3c993, inset 0 0 0 9px {TEAL}; }}
.card .aa {{ font-family:AM; direction:rtl; line-height:1.6; }}
.card .ee {{ font-family:CZ; font-size:36px; color:{TEAL}; margin-top:2px; }} .card small {{ display:block; font-size:28px; color:#6b5a44; margin-top:8px; }}
.hlw {{ position:relative; display:inline-block; }} .hlw svg {{ position:absolute; left:-75px; top:-6px; width:calc(100% + 80px); height:calc(100% + 12px); overflow:visible; }}
.op {{ display:flex; align-items:center; gap:22px; width:600px; margin:18px auto 0; padding:12px 30px; border-radius:24px; background:rgba(246,235,211,.95); color:{INK}; font-family:CZ; font-size:46px; opacity:0; box-shadow:0 14px 30px rgba(0,0,0,.35); }}
.op svg {{ flex:none; }}
#cd {{ position:absolute; left:0; right:0; top:560px; text-align:center; font-family:CZ; font-size:140px; color:{GOLD}; opacity:0; text-shadow:0 6px 0 {WOOD}; }}
.tile {{ position:absolute; border-radius:30px; background:{CREAM}; color:{RED}; font-family:AM; text-align:center; opacity:0; box-shadow:0 14px 0 {WOOD}, 0 24px 40px rgba(0,0,0,.4); }}
.wd {{ position:absolute; left:0; right:0; text-align:center; opacity:0; }}
.wd span {{ display:inline-block; padding:10px 40px; border-radius:24px; background:rgba(246,235,211,.96); color:{INK}; font-family:CZ; box-shadow:0 14px 30px rgba(0,0,0,.4); }}
.stop {{ position:absolute; padding:12px 28px 10px; border-radius:22px; background:rgba(246,235,211,.96); color:{INK}; text-align:center; opacity:0; box-shadow:0 14px 30px rgba(0,0,0,.4); }}
.stop b {{ display:block; font-family:CZ; font-size:30px; letter-spacing:.08em; color:{TEAL}; }} .stop span {{ font-family:KA; font-size:46px; }}
#digits {{ position:absolute; left:0; right:0; top:720px; text-align:center; direction:rtl; font-family:AM; font-size:96px; color:{CREAM}; }}
#digits span {{ display:inline-block; width:92px; opacity:0; text-shadow:0 5px 0 {TEAL}; }}
#fav {{ position:absolute; left:0; right:0; top:560px; text-align:center; font-family:CZ; font-size:110px; color:{CREAM}; }}
#fav span {{ display:inline-block; margin:0 14px; opacity:0; text-shadow:0 6px 0 {TEAL}; }}
#logo {{ position:absolute; top:62px; left:50%; transform:translateX(-50%); display:flex; justify-content:center; gap:12px; align-items:center; z-index:5; padding:6px 22px 6px 8px; border-radius:22px; background:rgba(14,18,44,.55); }}
#logo .tl {{ position:relative; width:58px; height:58px; border-radius:16px; background:{CREAM}; display:grid; place-items:center; }}
#logo .tl span {{ font-family:AM; font-size:38px; color:{INK}; margin-top:-6px; }} #logo .tl em {{ position:absolute; right:9px; top:8px; width:9px; height:9px; border-radius:50%; background:{RED}; }}
#logo b {{ font-family:AM; font-size:44px; color:{CREAM}; }}
"""
    digit_row = "".join(f"<span>{d}</span>" for d in "١٢٣٤٥٦٧٨٩")
    body = f"""<div id="cam">
<svg class="full" viewBox="0 0 1080 1920"><g id="stars">{stars}</g><g id="nums" data-layout-ignore aria-hidden="true">{nums}</g>
 {city}
</svg>
<div id="wash"></div>
<div id="logo"><span class="tl"><span>ر</span><em></em></span><b>رَفِيق</b></div>
<div class="sc" id="s1">
 <div class="t cz" id="kick" style="top:180px;font-size:44px;opacity:1">THE STORY OF A WORD</div>
 <div class="t cz" id="ttl" style="top:250px;font-size:200px;opacity:1">ZERO</div>
 {sv(f'<g id="big0"><ellipse cx="540" cy="1190" rx="200" ry="260" fill="none" stroke="{GOLD}" stroke-width="52" opacity=".9"/><ellipse cx="540" cy="1190" rx="200" ry="260" fill="none" stroke="{CREAM}" stroke-width="10" opacity=".5"/></g>' + padlock(540, 1300, 1.4, "lk1"))}
 <div class="t" id="from" style="top:510px"><span class="pill" style="font-size:44px">comes from Arabic</span></div>
 <div class="t am" id="ttl2" style="top:630px;font-size:200px;color:{GOLD}">صِفْر</div>
 <div class="t" id="code" style="top:1460px"><span class="pill" style="font-size:46px">…and <b style="color:{GOLD}">a secret code</b></span></div>
</div>
<div class="sc" id="s2">
 <div class="t am" id="sw" style="top:200px;font-size:210px;color:{GOLD}">صِفْر</div>
 <div class="t" id="se" style="top:500px"><span class="pill" style="font-size:50px">ṣifr = <b style="color:{GOLD}">empty</b></span></div>
 {sv(f'<g id="box" opacity="0" style="opacity:0"><rect x="380" y="720" width="320" height="260" rx="20" fill="none" stroke="{CREAM}" stroke-width="12" stroke-dasharray="40 26"/></g>')}
 <div id="digits">{digit_row}</div>
 <div class="t" id="bgd" style="top:880px"><span class="pill" style="font-size:44px">Baghdad</span></div>
 <div id="slot" style="position:absolute;left:440px;top:1000px;width:200px;height:220px;border-radius:26px;border:8px dashed {GOLD};opacity:0;text-align:center;font-family:AM;font-size:150px;line-height:200px;color:{GOLD}">٠</div>
 <div class="t" id="slotl" style="top:1250px"><span class="pill" style="font-size:46px">the sign for nothing = <b style="color:{GOLD}">صِفْر</b></span></div>
</div>
<div class="sc" id="s3">
 <div class="t" id="yr" style="top:190px"><span class="pill" style="font-size:60px;color:{GOLD}">1202</span></div>
 {sv(dots("route", "M860 470 C 700 380 420 380 230 470") + arrow("ar0", "M540 870 L 540 930") + arrow("ar1", "M540 1090 L 540 1150"))}
 <div class="stop" id="pt0" style="left:740px;top:440px"><b>BAGHDAD</b><span>ṣifr</span></div>
 <div class="stop" id="pt1" style="left:100px;top:440px"><b>PISA</b><span>Fibonacci</span></div>
 <div class="wd" id="w0" style="top:760px"><span style="font-size:76px">zephirum</span></div>
 <div class="wd" id="w1" style="top:960px"><span style="font-size:66px">zefiro</span></div>
 <div class="t cz" id="w2" style="top:1150px;font-size:170px">ZERO</div>
</div>
<div class="sc" id="s4">
 {sv('<g id="fork">' + "".join(f'<path pathLength="1" d="{d}" fill="none" stroke="{GOLD}" stroke-width="14" stroke-linecap="round" stroke-dasharray="1" stroke-dashoffset="1"/>' for d in (
     "M540 1500 L 540 1150", "M540 1150 C 540 1000 300 950 250 800", "M540 1150 C 540 1000 780 950 830 800")) + '</g>' + padlock(820, 1310, 0.9, "lk2"))}
 <div class="t" id="rd" style="top:180px"><span class="pill" style="font-size:52px">a <b style="color:{GOLD}">second road</b></span></div>
 <div class="stop" id="cf" style="left:110px;top:640px"><b>LATIN</b><span>cifra</span></div>
 <div class="stop" id="cp" style="left:680px;top:640px"><b>ENGLISH</b><span>cipher</span></div>
 <div class="t" id="m0" style="top:330px;left:60px;right:auto;width:320px"><span class="pill" style="font-size:60px;font-family:CZ">0</span></div>
 <div class="t" id="m1" style="top:330px;left:380px;right:auto;width:320px"><span class="pill" style="font-size:60px;font-family:CZ">1 2 3</span></div>
 <div class="t" id="m2" style="top:330px;left:700px;right:auto;width:320px"><span class="pill" style="font-size:44px">a secret code</span></div>
</div>
<div class="sc" id="s5">
 <div class="t cz" id="yt" style="top:170px;font-size:76px">YOUR TURN</div>
 <div id="tiles">{tile("tl0", "ص", 745, 330)}{tile("tl1", "ف", 445, 330)}{tile("tl2", "ر", 145, 330)}</div>
 <div class="card" id="aya" style="top:290px"><div class="aa" style="font-size:80px">بَقَرَةٌ <span class="hlw">صَفْراءُ<svg viewBox="0 0 100 60" preserveAspectRatio="none"><ellipse id="hl" pathLength="1" cx="50" cy="32" rx="48" ry="27" fill="none" stroke="{RED}" stroke-dasharray="1" stroke-dashoffset="1" vector-effect="non-scaling-stroke" style="stroke-width:7px"/></svg></span> فاقِعٌ لَوْنُها</div>
  <div style="position:relative;height:50px"><div class="ee" id="ee0" style="position:absolute;left:0;right:0;opacity:0">a ___ cow, bright in colour</div><div class="ee" id="ee1" style="position:absolute;left:0;right:0;opacity:0">a yellow cow, bright in colour</div></div>
  <small>the Qur’an · al-Baqarah 2:69</small></div>
 <div id="ops" style="position:absolute;left:0;right:0;top:800px"><div class="op" id="op0">{EMPTY}<span>empty</span></div><div class="op" id="op1">{ZERO_I}<span>zero</span></div><div class="op" id="op2">{YEL_I}<span>yellow</span></div></div>
 <div id="cd">3</div>
 <div class="t cz" id="slam" style="top:760px;font-size:150px;line-height:1.1;color:{YEL}">YELLOW!</div>
 {sv(cow(470, 1390, 1.3, "cw"))}
 <div class="t" id="pr0" style="top:960px;left:40px;right:auto;width:500px"><span class="pill" style="font-size:42px"><b style="font-family:AM;font-size:56px;color:{CREAM}">صِفْر</b> empty</span></div>
 <div class="t" id="pr1" style="top:960px;left:540px;right:auto;width:500px"><span class="pill" style="font-size:42px"><b style="font-family:AM;font-size:56px;color:{YEL}">صَفْراء</b> yellow</span></div>
 <div id="burst">{burst}</div>
</div>
<div class="sc" id="s6">
 <div class="t" id="q" style="top:180px"><div class="cz" style="display:inline-block;padding:18px 40px 12px;border-radius:28px;background:rgba(14,18,44,.82);font-size:70px;line-height:1.25">YOUR FAVOURITE<br/>NUMBER?</div></div>
 <div id="fav"><span>7</span><span>3</span><span>9</span><span>1</span><span>5</span></div>
 <div class="t" id="url" style="top:760px"><span class="pill" style="font-size:50px;background:{TEAL}">rafiq-arabic.com</span></div>
 <div class="t" id="arr" style="top:850px;font-size:80px">👇</div>
 {sv(f'<g id="z0" opacity="0" style="opacity:0"><ellipse cx="540" cy="1200" rx="110" ry="150" fill="none" stroke="{GOLD}" stroke-width="34"/></g><g id="zx">'
     + "".join(f'<path pathLength="1" d="{d}" fill="none" stroke="{RED}" stroke-width="26" stroke-linecap="round" stroke-dasharray="1" stroke-dashoffset="1"/>' for d in ("M400 1050 L 680 1350", "M680 1050 L 400 1350")) + '</g>')}
</div>
{caps}</div>"""
    open(os.path.join(out, "index.html"), "w").write(f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" /><title>zero</title>
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
