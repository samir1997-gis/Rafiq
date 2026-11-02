#!/usr/bin/env python3
"""h5-safari, the story of a word #5, in the drawn format of h3-lisan v2 and h4-khutbah v2 (#303, #310): the lines in
brag-quiz/voice/safari-lines.json told with full-screen drawings over a road across the savanna, from night to full morning,
because the root س ف ر means to uncover. Cinzel for the titles, Amiri for the Arabic, every move on its word, eased (MOTION-STYLE.md):
  1 "Safari comes from Arabic… what a journey reveals about you": SAFARI, سَفَر, a traveller walks in, the spotlight, YOU?
  2 سَفَر (Rafiq) · "a journey… Swahili… Arab traders… the coast… English, 1800s": a dhow sails the route ARABIC → SWAHILI → ENGLISH
  3 "the root means to uncover… like the dawn, uncovering the sky": س ف ر fall in, the clouds part, the dawn comes, al-Muddaththir 74:34
  4 "why is a journey called safar? … the dictionaries… faces… character" · "travel with someone…": Lisān al-ʿArab, two travellers, their tags
  5 your turn: ʿAbasa 80:38, travelling / covered / shining? 3-2-1; the ayah (Rafiq); "SHINING!", the sun all the way up
  6 the ask: two travellers walk into the sunrise, tag them, rafiq-arabic.com. Then the cream end card.
Figures are faceless (owner, 27 Oct).

  python3 brag-quiz/reels/safari/build.py    then  cd brag-quiz/reels/safari/out/v && npx hyperframes render -o ../raw.mp4
"""
import json, os, re, shutil, subprocess
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
V6 = os.path.join(ROOT, "brag-output-v6/composition/assets"); VO = os.path.join(ROOT, "brag-quiz/voice/safari")
INK, CREAM, GOLD, TEAL, RED, WOOD, SUN, SEA = "#17262B", "#F6EBD3", "#F2C46B", "#2E7263", "#B4322A", "#8A5A2B", "#FFB547", "#2B6F86"
DARK, FAR = "#0b1b20", "#173238"
dur = lambda f: float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))
mp3 = lambda n: os.path.join(VO, n + ".mp3")
def words(n):
    ws = json.load(open(os.path.join(VO, n + ".words.json")))
    return [(w[0], w[1], w[2] if len(w) > 2 else (ws[i + 1][1] if i + 1 < len(ws) else w[1] + 0.45)) for i, w in enumerate(ws)]
ORDER = [("h1", 0.3), ("safar", 0.35), ("b1", 0.25), ("b2", 0.45), ("b3", 0.5), ("b3b", 0.3), ("t1", 0.55), ("ayah", 3.9), ("b4", 0.2),
         ("end", 0.8)]                                                                     # the ayah waits for the 3-2-1
ARABIC = ("safar", "ayah")
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

def figure(x, y, s, c, cls="", pack=None, stick=False, id=""):   # a faceless traveller standing at (x, y), a pack on the back
    p = f'<rect x="16" y="-150" width="46" height="84" rx="14" fill="{pack}"/><path d="M20 -140 L 4 -120" stroke="{DARK}" stroke-width="5"/>' if pack else ""
    k = f'<path d="M-46 4 L -64 -168" stroke="{WOOD}" stroke-width="9" stroke-linecap="round"/>' if stick else ""
    return (f'<g transform="translate({x},{y}) scale({s})"><g id="{id}" class="{cls}">{p}{k}<path d="M-44 0 C -40 -80 -32 -126 0 -140 C 32 -126 40 -80 44 0 Z" fill="{c}"/>'
            f'<circle cx="0" cy="-160" r="26" fill="{c}"/></g></g>')
def acacia(x, y, s, c=DARK):
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M-6 0 L -4 -90 L -50 -140 M -4 -90 L 30 -150 M -2 -60 L 40 -110" stroke="{c}" stroke-width="12" stroke-linecap="round" fill="none"/>'
            f'<path d="M-150 -140 C -120 -190 120 -200 160 -150 C 120 -128 -110 -122 -150 -140 Z" fill="{c}"/><path d="M-60 -175 C -40 -205 70 -205 90 -176 Z" fill="{c}"/></g>')
def giraffe(x, y, s, c=DARK, id=""):
    return (f'<g transform="translate({x},{y}) scale({s})"><g id="{id}"><ellipse cx="0" cy="-130" rx="70" ry="34" fill="{c}"/>'
            f'<path d="M38 -150 L 62 -116 L 128 -292 L 104 -302 Z" fill="{c}"/><ellipse cx="128" cy="-300" rx="28" ry="13" transform="rotate(20 128 -300)" fill="{c}"/>'
            f'<path d="M110 -312 L 106 -334 M 122 -314 L 122 -336" stroke="{c}" stroke-width="6" stroke-linecap="round"/>'
            + "".join(f'<rect x="{lx}" y="-112" width="11" height="112" rx="5" fill="{c}"/>' for lx in (-52, -34, 30, 46))
            + f'<path d="M-68 -134 L -84 -84" stroke="{c}" stroke-width="5" stroke-linecap="round"/></g></g>')
def dhow(x, y, s, id=""):
    return (f'<g transform="translate({x},{y}) scale({s})"><g id="{id}"><path d="M8 -4 L 14 -170" stroke="{WOOD}" stroke-width="8"/>'
            f'<path d="M14 -170 L -96 -16 L 96 -26 Z" fill="{CREAM}" stroke="#d9cbae" stroke-width="4" stroke-linejoin="round"/>'
            f'<path d="M-110 -6 L 110 -6 L 84 34 L -84 34 Z" fill="{WOOD}" stroke="{GOLD}" stroke-width="5" stroke-linejoin="round"/></g></g>')
def sparkle(x, y, s, cls):
    return f'<path class="{cls}" transform="translate({x},{y}) scale({s})" d="M0 -30 C 4 -6 6 -4 30 0 C 6 4 4 6 0 30 C -4 6 -6 4 -30 0 C -6 -4 -4 -6 0 -30 Z" fill="#fff6dc"/>'
CASE = f'<svg width="70" height="70" viewBox="0 0 100 100"><rect x="12" y="30" width="76" height="56" rx="10" fill="{WOOD}"/><path d="M36 30 L 36 18 L 64 18 L 64 30" stroke="{WOOD}" stroke-width="8" fill="none"/><path d="M12 52 L 88 52" stroke="{GOLD}" stroke-width="5"/></svg>'
CLOUD = '<svg width="70" height="70" viewBox="0 0 100 100"><path d="M22 74 C 6 74 6 50 24 50 C 24 30 50 26 58 42 C 70 30 92 40 86 58 C 98 62 94 78 80 74 Z" fill="#8b9aa0"/></svg>'
SUNI = (f'<svg width="70" height="70" viewBox="0 0 100 100"><circle cx="50" cy="50" r="22" fill="{SUN}"/>'
        + "".join(f'<path d="M50 6 L 50 18" stroke="{SUN}" stroke-width="7" stroke-linecap="round" transform="rotate({a} 50 50)"/>' for a in range(0, 360, 45)) + '</svg>')

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
    OUT = lambda sel, t, y=-40: T(f'tl.to("{sel}", {{opacity:0, y:{y}, duration:0.3, ease:"power2.in"}}, {t:.2f});')
    def draw(sel, t, d=0.6): T(f'tl.fromTo("{sel}", {{strokeDashoffset:1}}, {{strokeDashoffset:0, duration:{d}, stagger:0.12, ease:"power2.inOut"}}, {t:.2f});')
    def pulse(sel, t, s=1.08): T(f'tl.fromTo("{sel}", {{scale:1}}, {{scale:{s}, duration:0.2, yoyo:true, repeat:1, ease:"power2.out", transformOrigin:"50% 50%", immediateRender:false}}, {t:.2f});')
    def walk(sel, t0, t1, step=0.32):                                     # a gentle walking bob between t0 and t1
        n = max(1, int((t1 - t0) / step / 2) * 2 - 1)
        T(f'tl.fromTo("{sel}", {{y:0}}, {{y:-10, duration:{step}, yoyo:true, repeat:{n}, stagger:{step / 2:.2f}, ease:"sine.inOut", immediateRender:false}}, {t0:.2f});')
    def scene(sel, t0, t1):
        if t0 > 0: T(f'tl.fromTo("{sel}", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.45, ease:"power3.out"}}, {t0:.2f});')
        if t1: T(f'tl.to("{sel}", {{opacity:0, y:-60, duration:0.35, ease:"power2.in"}}, {t1:.2f});'); snd("whoosh.wav", t1 - 0.05, 0.3)

    # the land lives the whole time: the stars drift, the far giraffe ambles, the grass sways
    T(f'tl.fromTo("#stars", {{x:0}}, {{x:-120, duration:{END:.2f}, ease:"sine.inOut"}}, 0);')
    T(f'tl.fromTo("#gir", {{x:0}}, {{x:420, duration:{END:.2f}, ease:"sine.inOut"}}, 0);')
    T(f'tl.fromTo(".grass", {{skewX:-6}}, {{skewX:6, duration:1.4, yoyo:true, repeat:{int(END / 1.4)}, stagger:0.2, ease:"sine.inOut", svgOrigin:"0 1920"}}, 0);')

    # 1 · the hook: SAFARI comes from Arabic
    ab = at("h1", "arabic")
    POP("#from", ab - 0.1, 0.7); snd("tap.wav", ab, 0.35)
    T(f'tl.fromTo("#ttl2", {{opacity:0, scale:1.6}}, {{opacity:1, scale:1, duration:0.45, ease:"back.out(1.4)"}}, {ab + 0.15:.2f});'); snd("impact.wav", ab + 0.15, 0.35, 1.2)
    jn = at("h1", "journey")
    T(f'tl.fromTo("#tr1", {{opacity:0, x:-420}}, {{opacity:1, x:0, duration:1.0, ease:"power2.out"}}, {jn - 0.5:.2f});'); snd("swoosh.wav", jn - 0.4, 0.3)
    walk("#tr1", jn - 0.5, jn + 0.6)
    rv0 = at("h1", "reveals")
    T(f'tl.fromTo("#spot1", {{opacity:0}}, {{opacity:0.22, duration:0.5, ease:"power2.out"}}, {rv0 - 0.1:.2f});'); snd("shimmer.wav", rv0, 0.35, 1.2)
    yu = at("h1", "you", last=True)
    POP("#you", yu - 0.1, 0.5); draw("#youarr", yu - 0.05, 0.4); snd("tick-lo.wav", yu, 0.45)
    S2 = L["safar"] - 0.25; scene("#s1", 0, S2 - 0.05)
    # 2 · سَفَر, a journey: ARABIC → SWAHILI → ENGLISH
    scene("#s2", S2, L["b2"] - 0.35)
    POP("#sw", L["safar"] - 0.05, 0.7); snd("tick-lo.wav", L["safar"], 0.4)
    POP("#sj", at("b1", "journey") - 0.05, 0.7); snd("tap.wav", at("b1", "journey"), 0.35)
    sh = at("b1", "swahili")
    POP("#st1", sh - 0.05, 0.6); snd("tap.wav", sh, 0.35)
    ar = at("b1", "arab")
    POP("#st0", ar - 0.1, 0.6); snd("tap.wav", ar, 0.35)
    T(f'tl.fromTo("#dh", {{opacity:0, scale:0.5}}, {{opacity:1, scale:1, duration:0.4, ease:"back.out(1.4)", transformOrigin:"50% 100%"}}, {ar + 0.15:.2f});')
    co = at("b1", "coast")
    T(f'tl.fromTo("#dh", {{x:0, y:0}}, {{x:-350, y:212, duration:1.3, ease:"power2.inOut", immediateRender:false}}, {co - 0.7:.2f});'); snd("swoosh.wav", co - 0.6, 0.35)
    T(f'tl.fromTo("#dh", {{rotation:-4}}, {{rotation:4, duration:0.3, yoyo:true, repeat:3, ease:"sine.inOut", transformOrigin:"50% 100%", immediateRender:false}}, {co - 0.7:.2f});')
    draw("#rt0", co - 0.7, 1.3)
    en = at("b1", "english")
    draw("#rt1", en - 0.3, 0.7); POP("#st2", en - 0.05, 0.6); snd("tap.wav", en, 0.35)
    yr = at("b1", "1800s")
    POP("#yr", yr - 0.05, 0.5); snd("tick-lo.wav", yr, 0.45)
    # 3 · the root: to uncover, like the dawn uncovering the sky
    S3 = L["b2"] - 0.1; scene("#s3", S3, L["b3"] - 0.35)
    rt = at("b2", "root")
    for i in range(3):
        T(f'tl.fromTo("#tl{i}", {{opacity:0, y:-260}}, {{opacity:1, y:0, duration:0.4, ease:"power3.out"}}, {rt - 0.2 + i * 0.16:.2f});'); snd("thump.wav", rt + i * 0.16, 0.3)
    POP("#unc", at("b2", "uncover") - 0.05, 0.7); snd("tap.wav", at("b2", "uncover"), 0.35)
    dw = at("b2", "dawn")
    T(f'tl.to("#sky1", {{opacity:1, duration:2.2, ease:"sine.inOut"}}, {dw - 0.2:.2f});')
    T(f'tl.to("#stars", {{opacity:0.15, duration:2.2, ease:"sine.inOut"}}, {dw - 0.2:.2f});')
    T(f'tl.fromTo("#sun", {{y:0}}, {{y:-200, duration:2.4, ease:"power2.out"}}, {dw - 0.1:.2f});'); snd("wind.wav", dw - 0.3, 0.25, 3.0); snd("shimmer.wav", dw, 0.35, 1.2)
    uc = at("b2", "uncovering")
    T(f'tl.to("#cl0", {{x:-520, duration:1.4, ease:"power2.out"}}, {uc - 0.2:.2f});'); T(f'tl.to("#cl1", {{x:520, duration:1.4, ease:"power2.out"}}, {uc - 0.2:.2f});')
    snd("whoosh.wav", uc - 0.1, 0.3)
    IN("#mud", at("b2", "sky") - 0.1, 30); snd("flip.wav", at("b2", "sky"), 0.35)
    # 4 · why a journey is safar: Lisān al-ʿArab; it uncovers faces and character
    S4 = L["b3"] - 0.1; scene("#s4", S4, L["t1"] - 0.4)
    IN("#why", at("b3", "why") - 0.1, 30)
    di = at("b3", "dictionaries")
    POP("#book", di - 0.1, 0.6); snd("flip.wav", di, 0.4)
    uv = at("b3", "uncovers")
    T(f'tl.fromTo("#pair", {{opacity:0, x:-360}}, {{opacity:1, x:0, duration:0.9, ease:"power2.out"}}, {uv - 0.5:.2f});')
    walk("#pair .w", uv - 0.5, L["t1"] - 0.5)
    fc = at("b3", "faces")
    T(f'tl.fromTo("#sweep", {{opacity:0, x:-700}}, {{opacity:0.3, x:700, duration:1.1, ease:"power2.inOut"}}, {fc - 0.35:.2f});'); snd("shimmer.wav", fc, 0.35, 1.2)
    ch = at("b3", "character")
    POP("#tg0", ch - 0.05, 0.5); snd("tick-lo.wav", ch, 0.4)
    POP("#tg1", ch + 0.35, 0.5); snd("tick-lo.wav", ch + 0.4, 0.4)
    T(f'tl.to("#pair", {{x:-70, duration:2.6, ease:"sine.inOut"}}, {at("b3b", "travel") - 0.2:.2f});')
    ra = at("b3b", "really")
    POP("#tg2", ra - 0.05, 0.5); snd("tap.wav", ra, 0.45)
    pulse("#tg2", at("b3b", "are") + 0.1, 1.1)
    # 5 · your turn: ʿAbasa 80:38, travelling / covered / shining? 3-2-1; the ayah; SHINING!
    S5 = L["t1"] - 0.1; scene("#s5", S5, L["end"] - 0.45)
    IN("#yt", L["t1"], 20)
    POP("#aya", at("t1", "abasa") - 0.1, 0.8); snd("flip.wav", at("t1", "abasa"), 0.4)
    fs = at("t1", "faces")
    IN("#ee0", fs - 0.1, 16); draw("#hl", fs, 0.5); snd("tap.wav", fs, 0.4)
    for i, k in enumerate(("travelling", "covered", "shining")):
        w0 = at("t1", k); POP(f"#op{i}", w0 - 0.05, 0.8); snd("tap.wav", w0, 0.3)
    c0 = round(L["t1"] + spoken("t1") + 0.3, 2)
    for k, nm in enumerate(("3", "2", "1")):
        T(f'tl.set("#cd", {{textContent:"{nm}", opacity:1}}, {c0 + k:.2f});'); T(f'tl.fromTo("#cd", {{scale:1.4}}, {{scale:1, duration:0.35, ease:"power3.out"}}, {c0 + k:.2f});')
        snd("click.wav", c0 + k, 1.0); snd("tick-lo.wav", c0 + k, 0.5)
    rv = c0 + 3
    T(f'tl.to("#cd", {{opacity:0, duration:0.2, ease:"power2.in"}}, {rv - 0.1:.2f});')
    T(f'tl.to("#op2", {{backgroundColor:"{GOLD}", scale:1.08, duration:0.3, ease:"back.out(1.4)"}}, {rv:.2f});'); snd("tick-lo.wav", rv, 0.45)
    T(f'tl.to(["#op0", "#op1"], {{opacity:0.3, duration:0.3, ease:"power2.in"}}, {rv:.2f});')
    T(f'tl.to("#ee0", {{opacity:0, duration:0.2, ease:"power2.in"}}, {L["ayah"] + 0.2:.2f});'); IN("#ee1", L["ayah"] + 0.4, 16)
    hit = at("b4", "shining")
    T(f'tl.to("#ops", {{opacity:0, y:30, duration:0.25, ease:"power2.in"}}, {hit - 0.25:.2f});')
    T(f'tl.fromTo("#slam", {{opacity:0, scale:1.8}}, {{opacity:1, scale:1, duration:0.45, ease:"back.out(1.7)"}}, {hit:.2f});')   # the one slam
    T(f'tl.fromTo("#cam", {{x:-14}}, {{x:14, duration:0.05, yoyo:true, repeat:7, ease:"sine.inOut", immediateRender:false}}, {hit + 0.05:.2f});')
    T(f'tl.set("#cam", {{x:0}}, {hit + 0.5:.2f});')
    snd("impact.wav", hit - 0.03, 0.75, 1.6)
    T(f'tl.fromTo("#burst i", {{opacity:1, x:0, y:0, scale:0.4}}, {{opacity:0, x:(i) => [-300, -170, 0, 170, 300, -90, 90][i], y:(i) => [-80, -200, -260, -200, -80, 150, 150][i], scale:1.3, duration:0.9, ease:"power2.out", immediateRender:false}}, {hit + 0.05:.2f});')
    T(f'tl.to("#sky2", {{opacity:1, duration:0.8, ease:"power2.out"}}, {hit:.2f});')
    T(f'tl.to("#sun", {{y:-430, duration:1.0, ease:"back.out(1.2)"}}, {hit:.2f});')
    T(f'tl.to("#rays", {{opacity:1, duration:0.6, ease:"power2.out"}}, {hit + 0.1:.2f});')
    T(f'tl.fromTo("#rays", {{rotation:0}}, {{rotation:40, duration:{END - hit:.2f}, ease:"sine.inOut", svgOrigin:"540 1440"}}, {hit:.2f});')
    uo = at("b4", "uncovered")
    for i in range(3): POP(f"#mt{i}", uo - 0.1 + i * 0.12, 0.5)
    snd("tap.wav", uo, 0.4)
    pulse("#sunc", at("b4", "dawn"), 1.12)
    # 6 · the ask: two travellers walk into the sunrise; tag them
    S6 = L["end"] - 0.1; scene("#s6", S6, None)
    IN("#q", L["end"] + 0.1, 30)
    walk("#pair2 .w", L["end"], END - 0.2)
    T(f'tl.fromTo("#pair2", {{y:0, scale:1}}, {{y:-60, scale:0.86, duration:{END - L["end"]:.2f}, ease:"sine.inOut", svgOrigin:"540 1460"}}, {L["end"]:.2f});')
    pe = at("end", "person")
    POP("#hrt", pe - 0.05, 0.4); snd("shimmer.wav", pe, 0.3, 1.2)
    tg = at("end", "tag")
    POP("#at", tg - 0.05, 0.5); snd("tick-lo.wav", tg, 0.5)
    cm = at("end", "comments")
    POP("#url", cm - 0.1, 0.8); snd("tap.wav", cm, 0.4)
    T(f'tl.fromTo("#arr", {{opacity:0, y:0}}, {{opacity:1, y:18, duration:0.4, yoyo:true, repeat:3, ease:"sine.inOut"}}, {cm:.2f});')

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
                    zip(rng.uniform(0, 1200, 90), rng.uniform(0, 1150, 90), rng.uniform(1, 3, 90), rng.uniform(0.25, 0.85, 90)))
    grass = "".join(f'<path class="grass" d="M{x} 1920 C {x - 6} 1880 {x + 4} 1850 {x + 10} {1830 - h}" stroke="{DARK}" stroke-width="7" stroke-linecap="round" fill="none"/>'
                    for x, h in zip(range(20, 1080, 46), rng.uniform(0, 50, 24)))
    land = (f'<path d="M-20 1450 C 160 1400 300 1420 440 1446 C 600 1470 760 1396 900 1410 C 990 1418 1050 1440 1100 1450 L 1100 1940 L -20 1940 Z" fill="{FAR}"/>'
            + giraffe(150, 1458, 0.62, FAR, "gir") + acacia(860, 1452, 0.7, FAR)
            + f'<path d="M-20 1530 C 200 1500 380 1520 540 1528 C 720 1536 900 1500 1100 1520 L 1100 1940 L -20 1940 Z" fill="{DARK}"/>'
            + f'<path d="M500 1528 C 520 1600 420 1700 300 1940 L 780 1940 C 660 1700 560 1600 580 1528 Z" fill="#c9a35e" opacity=".22"/>'
            + acacia(130, 1560, 1.25) + acacia(980, 1600, 1.0) + grass)
    sky0 = "linear-gradient(#0a141c 0%, #13232c 40%, #1b3a40 72%, #3b4a3e 100%)"
    sky1 = "linear-gradient(#22324a 0%, #6c5a7a 35%, #d98b6a 62%, #f2c46b 80%, #f6d9a0 100%)"
    sky2 = "linear-gradient(#2f6f86 0%, #5f9fb0 32%, #e8a86a 62%, #f2c46b 82%, #f6d9a0 100%)"
    rays = "".join(f'<path d="M540 1440 L {540 + 1400 * np.cos(np.radians(a - 4)):.0f} {1440 + 1400 * np.sin(np.radians(a - 4)):.0f} L {540 + 1400 * np.cos(np.radians(a + 4)):.0f} {1440 + 1400 * np.sin(np.radians(a + 4)):.0f} Z" fill="#fff3cf" opacity=".22"/>'
                   for a in range(180, 360, 18))
    clouds = (f'<path id="cl0" d="M120 1330 C 90 1270 180 1230 240 1260 C 270 1200 380 1200 410 1250 C 470 1230 560 1260 545 1330 Z" fill="#41505a"/>'
              f'<path id="cl1" d="M535 1330 C 520 1270 600 1240 650 1262 C 690 1200 800 1210 820 1258 C 880 1240 960 1280 940 1330 Z" fill="#3a4852"/>')
    arrow = lambda id, d, c=GOLD: f'<path id="{id}" pathLength="1" d="{d}" fill="none" stroke="{c}" stroke-width="7" stroke-linecap="round" stroke-dasharray="1" stroke-dashoffset="1"/>'
    dots = lambda id, d: f'<path id="{id}" pathLength="1" d="{d}" fill="none" stroke="{CREAM}" stroke-width="8" stroke-linecap="round" stroke-dasharray="1" stroke-dashoffset="1" opacity=".85"/>'
    sv = lambda inner: f'<svg class="full" viewBox="0 0 1080 1920">{inner}</svg>'
    sea = "".join(f'<path d="M{x} {y} q 30 -16 60 0 t 60 0" stroke="#9fd3e0" stroke-width="5" fill="none" opacity=".45" stroke-linecap="round"/>' for x, y in
                  ((560, 860), (820, 900), (420, 940), (700, 980), (520, 1060), (300, 1040), (760, 1080), (440, 1120)))
    book = (f'<svg width="420" height="250" viewBox="0 0 420 250"><path d="M210 40 C 150 10 70 10 20 30 L 20 220 C 70 200 150 200 210 230 Z" fill="#f3e3c0" stroke="{WOOD}" stroke-width="8" stroke-linejoin="round"/>'
            f'<path d="M210 40 C 270 10 350 10 400 30 L 400 220 C 350 200 270 200 210 230 Z" fill="#f3e3c0" stroke="{WOOD}" stroke-width="8" stroke-linejoin="round"/>'
            + "".join(f'<path d="M{x0} {y} L {x1} {y}" stroke="#b9a27a" stroke-width="6" stroke-linecap="round"/>' for y in (70, 100, 130, 160, 190) for x0, x1 in ((50, 180), (240, 370))) + '</svg>')
    tile = lambda id, ch, x, y, sz=190, fs=150: f'<div class="tile" id="{id}" style="left:{x}px;top:{y}px;width:{sz}px;height:{sz}px;line-height:{sz}px;font-size:{fs}px">{ch}</div>'
    burst = "".join(f'<i style="position:absolute;left:520px;top:960px;width:40px;height:40px;border-radius:50%;background:{c};opacity:0"></i>' for c in (GOLD, CREAM, RED, GOLD, CREAM, RED, GOLD))
    css = f"""
@font-face {{ font-family:"CZ"; src:url("assets/cinzel-latin-700-normal.woff2"); }}
@font-face {{ font-family:"AM"; src:url("assets/amiri-arabic-700-normal.woff2"); }}
@font-face {{ font-family:"KA"; src:url("assets/karla-latin-700-normal.woff2"); }}
* {{ margin:0; box-sizing:border-box; }} html, body {{ width:1080px; height:1920px; overflow:hidden; background:#000; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; background:{sky0}; font-family:KA; color:{CREAM}; }}
#cam {{ position:absolute; inset:0; }}
.sky {{ position:absolute; inset:0; opacity:0; }} #sky1 {{ background:{sky1}; }} #sky2 {{ background:{sky2}; }}
svg.full {{ position:absolute; left:0; top:0; width:1080px; height:1920px; overflow:visible; }}
.sc {{ position:absolute; inset:0; opacity:0; }} #s1 {{ opacity:1; }}
.t {{ position:absolute; left:0; right:0; text-align:center; opacity:0; }}
.cz {{ font-family:CZ; letter-spacing:.06em; color:{GOLD}; text-shadow:0 4px 0 {WOOD}, 0 10px 30px rgba(0,0,0,.5); }}
.am {{ font-family:AM; direction:rtl; color:{CREAM}; text-shadow:0 6px 0 {TEAL}, 0 14px 40px rgba(0,0,0,.45); line-height:1.3; }}
.pill {{ display:inline-flex; align-items:center; gap:14px; padding:8px 30px; border-radius:999px; background:rgba(23,38,43,.88); border:2px solid rgba(242,196,107,.6); font-family:KA; color:{CREAM}; }}
.cap {{ position:absolute; left:70px; right:70px; top:1580px; text-align:center; font-family:KA; font-size:50px; line-height:1.2; color:#fff; text-shadow:0 3px 0 rgba(0,0,0,.6), 0 0 18px rgba(0,0,0,.6); opacity:0; }}
.cap span {{ display:inline-block; opacity:0; }}
.card {{ position:absolute; left:70px; right:70px; padding:26px 30px 22px; border-radius:20px; background:#f3e3c0; color:{INK}; text-align:center; opacity:0;
  box-shadow:0 24px 50px rgba(0,0,0,.4), inset 0 0 0 6px #e3c993, inset 0 0 0 9px {TEAL}; }}
.card .aa {{ font-family:AM; direction:rtl; line-height:1.6; }}
.card .ee {{ font-family:CZ; font-size:36px; color:{TEAL}; margin-top:2px; }} .card small {{ display:block; font-size:28px; color:#6b5a44; margin-top:8px; }}
.hlw {{ position:relative; display:inline-block; }} .hlw svg {{ position:absolute; left:-40px; top:-6px; width:calc(100% + 80px); height:calc(100% + 12px); overflow:visible; }}
.op {{ display:flex; align-items:center; gap:22px; width:600px; margin:18px auto 0; padding:12px 30px; border-radius:24px; background:rgba(246,235,211,.95); color:{INK}; font-family:CZ; font-size:46px; opacity:0; box-shadow:0 14px 30px rgba(0,0,0,.35); }}
.op svg {{ flex:none; }}
#cd {{ position:absolute; left:0; right:0; top:560px; text-align:center; font-family:CZ; font-size:140px; color:{GOLD}; opacity:0; text-shadow:0 6px 0 {WOOD}; }}
.tile {{ position:absolute; border-radius:30px; background:{CREAM}; color:{RED}; font-family:AM; text-align:center; opacity:0; box-shadow:0 14px 0 {WOOD}, 0 24px 40px rgba(0,0,0,.4); }}
.stop {{ position:absolute; padding:14px 28px 10px; border-radius:22px; background:rgba(246,235,211,.96); color:{INK}; text-align:center; opacity:0; box-shadow:0 14px 30px rgba(0,0,0,.4); }}
.stop b {{ display:block; font-family:CZ; font-size:30px; letter-spacing:.08em; color:{TEAL}; }} .stop span {{ font-family:KA; font-size:54px; }} .stop .am2 {{ font-family:AM; font-size:64px; line-height:1.2; }}
.tag {{ position:absolute; padding:8px 24px; border-radius:16px; background:{CREAM}; color:{INK}; font-family:KA; font-size:40px; opacity:0; box-shadow:0 10px 24px rgba(0,0,0,.35); white-space:nowrap; }}
#logo {{ position:absolute; top:62px; left:50%; transform:translateX(-50%); display:flex; justify-content:center; gap:12px; align-items:center; z-index:5; padding:6px 22px 6px 8px; border-radius:22px; background:rgba(23,38,43,.55); }}
#logo .tl {{ position:relative; width:58px; height:58px; border-radius:16px; background:{CREAM}; display:grid; place-items:center; }}
#logo .tl span {{ font-family:AM; font-size:38px; color:{INK}; margin-top:-6px; }} #logo .tl em {{ position:absolute; right:9px; top:8px; width:9px; height:9px; border-radius:50%; background:{RED}; }}
#logo b {{ font-family:AM; font-size:44px; color:{CREAM}; }}
"""
    body = f"""<div id="cam">
<div class="sky" id="sky1"></div><div class="sky" id="sky2"></div>
<svg class="full" viewBox="0 0 1080 1920"><g id="stars">{stars}</g>
 <g id="rays" opacity="0">{rays}</g>
 <g id="sun"><circle cx="540" cy="1560" r="210" fill="{SUN}" opacity=".18"/><circle id="sunc" cx="540" cy="1560" r="120" fill="{SUN}"/></g>
 {clouds}{land}
</svg>
<div id="logo"><span class="tl"><span>ر</span><em></em></span><b>رَفِيق</b></div>
<div class="sc" id="s1">
 <div class="t cz" id="kick" style="top:180px;font-size:44px;opacity:1">THE STORY OF A WORD</div>
 <div class="t cz" id="ttl" style="top:250px;font-size:190px;opacity:1">SAFARI</div>
 <div class="t" id="from" style="top:500px"><span class="pill" style="font-size:44px">comes from Arabic</span></div>
 <div class="t am" id="ttl2" style="top:620px;font-size:220px;color:{GOLD}">سَفَر</div>
 {sv('<path id="spot1" d="M470 860 L 610 860 L 780 1450 L 300 1450 Z" fill="#fff3cf" opacity="0" style="opacity:0"/>' + figure(540, 1440, 1.5, CREAM, pack=TEAL, stick=True, id="tr1")
     + arrow("youarr", "M860 1010 C 820 1060 760 1100 680 1150"))}
 <div class="t cz" id="you" style="top:930px;left:640px;right:auto;width:420px;font-size:80px;color:{CREAM}">YOU?</div>
</div>
<div class="sc" id="s2">
 <div class="t am" id="sw" style="top:200px;font-size:210px;color:{GOLD}">سَفَر</div>
 <div class="t" id="sj" style="top:500px"><span class="pill" style="font-size:46px">safar = <b style="color:{GOLD}">a journey</b></span></div>
 {sv(sea + dots("rt0", "M700 880 C 640 960 540 1030 420 1050") + dots("rt1", "M300 1100 C 380 1170 520 1210 610 1230") + dhow(700, 880, 0.8, "dh"))}
 <div class="stop" id="st0" style="left:640px;top:600px"><b>ARABIC</b><div class="am2">سَفَر</div></div>
 <div class="stop" id="st1" style="left:60px;top:960px"><b>SWAHILI</b><span>safari</span></div>
 <div class="stop" id="st2" style="left:640px;top:1200px"><b>ENGLISH</b><span>safari</span></div>
 <div class="t" id="yr" style="top:1340px;left:200px;right:auto;width:440px"><span class="pill" style="font-size:44px;color:{GOLD}">1800s</span></div>
</div>
<div class="sc" id="s3">
 {tile("tl0", "س", 745, 220)}{tile("tl1", "ف", 445, 220)}{tile("tl2", "ر", 145, 220)}
 <div class="t" id="unc" style="top:470px"><span class="pill" style="font-size:52px">the root = <b style="color:{GOLD}">to uncover</b></span></div>
 <div class="card" id="mud" style="top:600px"><div class="aa" style="font-size:84px">وَالصُّبْحِ إِذا أَسْفَرَ</div><div class="ee">and the dawn, when it brightens</div><small>the Qur’an · al-Muddaththir 74:34</small></div>
</div>
<div class="sc" id="s4">
 <div class="t cz" id="why" style="top:180px;font-size:84px">WHY SAFAR?</div>
 <div class="t" id="book" style="top:310px">{book}<div style="margin-top:6px"><span class="pill" style="font-size:40px"><span style="font-family:AM;font-size:44px">لِسانُ الْعَرَب</span> · the old dictionaries</span></div></div>
 {sv('<ellipse id="sweep" cx="540" cy="1250" rx="160" ry="420" fill="#fff3cf" opacity="0" style="opacity:0"/>'
     + '<g id="pair" opacity="0" style="opacity:0">' + figure(400, 1440, 1.35, CREAM, cls="w", pack=TEAL, stick=True) + figure(690, 1440, 1.4, "#e7b07a", cls="w", pack=RED) + '</g>')}
 <div class="tag" id="tg0" style="left:200px;top:960px">patient ✓</div>
 <div class="tag" id="tg1" style="left:590px;top:900px">generous ✓</div>
 <div class="tag" id="tg2" style="left:120px;top:800px">grumpy before coffee 😅</div>
</div>
<div class="sc" id="s5">
 <div class="t cz" id="yt" style="top:170px;font-size:76px">YOUR TURN</div>
 <div class="card" id="aya" style="top:290px"><div class="aa" style="font-size:86px">وُجُوهٌ يَوْمَئِذٍ <span class="hlw">مُسْفِرَةٌ<svg viewBox="0 0 100 60" preserveAspectRatio="none"><ellipse id="hl" pathLength="1" cx="50" cy="32" rx="48" ry="27" fill="none" stroke="{RED}" stroke-width="3" stroke-dasharray="1" stroke-dashoffset="1" vector-effect="non-scaling-stroke" style="stroke-width:7px"/></svg></span></div>
  <div style="position:relative;height:50px"><div class="ee" id="ee0" style="position:absolute;left:0;right:0;opacity:0">Some faces, that Day, will be…?</div><div class="ee" id="ee1" style="position:absolute;left:0;right:0;opacity:0">Some faces, that Day, will be bright</div></div>
  <small>the Qur’an · ʿAbasa 80:38</small></div>
 <div id="ops" style="position:absolute;left:0;right:0;top:800px"><div class="op" id="op0">{CASE}<span>travelling</span></div><div class="op" id="op1">{CLOUD}<span>covered</span></div><div class="op" id="op2">{SUNI}<span>shining</span></div></div>
 <div id="cd">3</div>
 <div class="t cz" id="slam" style="top:820px;font-size:140px;line-height:1.1">SHINING!</div>
 {tile("mt0", "س", 650, 1040, 120, 90)}{tile("mt1", "ف", 480, 1040, 120, 90)}{tile("mt2", "ر", 310, 1040, 120, 90)}
 <div id="burst">{burst}</div>
</div>
<div class="sc" id="s6">
 <div class="t" id="q" style="top:180px"><div class="cz" style="display:inline-block;padding:18px 40px 12px;border-radius:28px;background:rgba(23,38,43,.82);font-size:70px;line-height:1.25">WHO WOULD YOU<br/>TRAVEL WITH?</div></div>
 {sv('<g id="pair2">' + figure(450, 1440, 1.25, CREAM, cls="w", pack=TEAL, stick=True) + figure(640, 1440, 1.3, "#e7b07a", cls="w", pack=RED) + '</g>'
     + '<path id="hrt" transform="translate(545,1080)" d="M0 30 C -60 -10 -40 -60 0 -32 C 40 -60 60 -10 0 30 Z" fill="' + RED + '" opacity="0" style="opacity:0"/>')}
 <div class="t" id="at" style="top:500px"><span class="pill" style="font-size:56px"><b style="color:{GOLD}">@</b> tag them</span></div>
 <div class="t" id="url" style="top:620px"><span class="pill" style="font-size:50px;background:{TEAL}">rafiq-arabic.com</span></div>
 <div class="t" id="arr" style="top:720px;font-size:80px">👇</div>
</div>
{caps}</div>"""
    open(os.path.join(out, "index.html"), "w").write(f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" /><title>safari</title>
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
