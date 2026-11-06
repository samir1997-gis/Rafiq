#!/usr/bin/env python3
"""h10-magazine, the story of a word #9 (#353), in the drawn format of h8-admiral and h9-mattress (#323, #340): the lines in
brag-quiz/voice/magazine-lines.json told with full-screen drawings over an old market's arched storehouses at dusk. Cinzel for the
titles, Amiri for the Arabic, every move on its word, eased (MOTION-STYLE.md):
  1 "Every magazine you've ever read is named after an Arabic word… and it has nothing to do with reading": MAGAZINE, a magazine
    drops onto the table, مَخازِن, a question mark
  2 مَخازِن (Rafiq) · "storehouses: where you keep the grain, the oil, the goods": a sack, a jar and a crate drop into the arches
  3 "Its root means to store away, to keep safe… put ma in front… the place where you keep things": خ ز ن, then مَخْزَن with its مَـ lit
  4 "Italian made it magazzino… French magasin… still a shop… in the 1580s… magazine: a storehouse": the word changes as it travels
  5 "how does a storehouse end up on a news stand? In 1731, a London monthly… The Gentleman's Magazine: a storehouse of articles"
  6 your turn: خ ز ن in Yūsuf 12:55, خَزائِنِ الْأَرْضِ: the armies / the roads / the storehouses? 3-2-1; the ayah (Rafiq); "STOREHOUSES!";
    and he saved the grain for seven hard years (12:47-48): seven sacks
  7 the ask: which English word should we trace back next? Then the cream end card.
Figures are faceless (owner, 27 Oct). Facts: Merriam-Webster "magazine" (Arabic makhzan, plural makhāzin, storehouse; French, then
English; 1731, The Gentleman's Magazine, "a storehouse" of articles); Wiktionary (Italian magazzino, Middle French magasin, root
khazana "to store"); Etymonline (English "warehouse", 1580s).

  python3 brag-quiz/reels/magazine/build.py    then  cd brag-quiz/reels/magazine/out/v && npx hyperframes render -o ../raw.mp4
"""
import json, os, re, shutil, subprocess
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
V6 = os.path.join(ROOT, "brag-output-v6/composition/assets"); VO = os.path.join(ROOT, "brag-quiz/voice/magazine")
INK, CREAM, GOLD, TEAL, RED, WOOD, NAVY = "#17262B", "#F6EBD3", "#F2C46B", "#2E7263", "#B4322A", "#8A5A2B", "#1D3557"
STONE, SHADE, ARCH = "#7a4a52", "#5c3442", "#2b1b2c"
dur = lambda f: float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))
mp3 = lambda n: os.path.join(VO, n + ".mp3")
SHOW = {"Makhaazin.": "Makhāzin.", "khazaa-in": "khazāʾin"}          # spelt for the voice, shown as written
def words(n):
    ws = json.load(open(os.path.join(VO, n + ".words.json")))
    return [(w[0], w[1], w[2] if len(w) > 2 else (ws[i + 1][1] if i + 1 < len(ws) else w[1] + 0.45)) for i, w in enumerate(ws)]
ORDER = [("h1", 0.3), ("makhazin", 0.35), ("b1", 0.25), ("b2", 0.45), ("b3", 0.5), ("b4", 0.5), ("t1", 0.55), ("ayah", 3.9), ("b5", 0.2), ("end", 0.8)]
ARABIC = ("makhazin", "ayah")
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

def sack(x, y, s, id="", c="#d9b26f"):   # a grain sack tied at the top, base at (x, y)
    return (f'<g transform="translate({x},{y}) scale({s})"><g id="{id}"><path d="M-70 0 C -96 -40 -84 -110 -40 -130 L 40 -130 C 84 -110 96 -40 70 0 Z" fill="{c}" stroke="{WOOD}" stroke-width="6"/>'
            f'<path d="M-40 -130 C -30 -160 30 -160 40 -130" fill="{c}" stroke="{WOOD}" stroke-width="6"/><path d="M-36 -128 L 36 -128" stroke="{RED}" stroke-width="9" stroke-linecap="round"/>'
            f'<path d="M-20 -150 L -30 -176 M 0 -152 L 0 -182 M 20 -150 L 30 -176" stroke="{GOLD}" stroke-width="6" stroke-linecap="round"/></g></g>')
def jar(x, y, s, id=""):                  # an oil jar
    return (f'<g transform="translate({x},{y}) scale({s})"><g id="{id}"><path d="M-30 0 C -90 -40 -90 -130 -36 -160 L -26 -190 L 26 -190 L 36 -160 C 90 -130 90 -40 30 0 Z" fill="#c8693f" stroke="{WOOD}" stroke-width="6"/>'
            f'<rect x="-34" y="-204" width="68" height="18" rx="6" fill="#c8693f" stroke="{WOOD}" stroke-width="5"/><path d="M-60 -96 C -20 -84 20 -84 60 -96" fill="none" stroke="{GOLD}" stroke-width="7"/></g></g>')
def crate(x, y, s, id=""):
    return (f'<g transform="translate({x},{y}) scale({s})"><g id="{id}"><rect x="-80" y="-130" width="160" height="130" rx="8" fill="#b9874f" stroke="{WOOD}" stroke-width="6"/>'
            f'<path d="M-80 -130 L 80 0 M 80 -130 L -80 0" stroke="{WOOD}" stroke-width="7"/><rect x="-80" y="-74" width="160" height="18" fill="#a5743f"/></g></g>')
def store(x, y, s, n=3, id=""):            # the storehouse: a stone front with n arched doors, base at (x, y)
    w = 300 * n
    g = f'<g transform="translate({x},{y}) scale({s})"><g id="{id}"><rect x="{-w / 2 - 30}" y="-420" width="{w + 60}" height="420" fill="{STONE}"/><rect x="{-w / 2 - 50}" y="-440" width="{w + 100}" height="34" rx="8" fill="{SHADE}"/>'
    for k in range(n):
        cx = -w / 2 + 150 + k * 300
        g += f'<path d="M{cx - 110} 0 L {cx - 110} -220 C {cx - 110} -350 {cx + 110} -350 {cx + 110} -220 L {cx + 110} 0 Z" fill="{ARCH}"/>'
        g += f'<path d="M{cx - 128} 0 L {cx - 128} -220 C {cx - 128} -372 {cx + 128} -372 {cx + 128} -220 L {cx + 128} 0" fill="none" stroke="{GOLD}" stroke-width="8" opacity=".55"/>'
    return g + '</g></g>'
def cover(x, y, s, c, title="MAGAZINE", id="", ts=44):   # a magazine cover, centre (x, y)
    lines = "".join(f'<rect x="-120" y="{150 + k * 22}" width="{240 - (k % 2) * 70}" height="10" rx="5" fill="#fff" opacity=".7"/>' for k in range(3))
    return (f'<g transform="translate({x},{y}) scale({s})"><g id="{id}"><rect x="-150" y="-210" width="300" height="420" rx="10" fill="{c}" stroke="{INK}" stroke-width="6"/>'
            + (f'<text x="0" y="-140" text-anchor="middle" font-family="CZ" font-size="{ts}" fill="{CREAM}">{title}</text>' if "|" not in title else
               f'<text x="0" y="-170" text-anchor="middle" font-family="CZ" font-size="{ts}" fill="{CREAM}">{title.split("|")[0]}</text>'
               f'<text x="0" y="-122" text-anchor="middle" font-family="CZ" font-size="{ts * 1.6:.0f}" fill="{GOLD}">{title.split("|")[1]}</text>')
            + f'<rect x="-120" y="-100" width="240" height="220" rx="8" fill="{CREAM}" opacity=".9"/><circle cx="0" cy="-20" r="56" fill="{GOLD}"/>'
            f'<path d="M-120 120 L -40 30 L 20 80 L 70 40 L 120 120 Z" fill="{TEAL}"/>{lines}</g></g>')
def table(y):
    return f'<rect x="80" y="{y}" width="920" height="34" rx="10" fill="{WOOD}"/><rect x="140" y="{y + 34}" width="34" height="200" fill="{WOOD}"/><rect x="906" y="{y + 34}" width="34" height="200" fill="{WOOD}"/>'
ARMY_I = (f'<svg width="70" height="70" viewBox="0 0 100 100"><path d="M20 90 L 50 10 L 80 90" fill="none" stroke="{WOOD}" stroke-width="6"/><path d="M50 10 L 42 30 L 58 30 Z" fill="#9aa5ab"/>'
          f'<path d="M50 40 C 26 40 22 64 26 84 L 74 84 C 78 64 74 40 50 40 Z" fill="{RED}" stroke="{WOOD}" stroke-width="5"/></svg>')
ROAD_I = (f'<svg width="70" height="70" viewBox="0 0 100 100"><path d="M30 96 C 30 60 74 60 70 36 C 66 16 50 10 46 4" fill="none" stroke="#9aa5ab" stroke-width="20" stroke-linecap="round"/>'
          f'<path d="M30 96 C 30 60 74 60 70 36 C 66 16 50 10 46 4" fill="none" stroke="{CREAM}" stroke-width="4" stroke-dasharray="8 8"/></svg>')
STORE_I = (f'<svg width="70" height="70" viewBox="0 0 100 100"><path d="M14 92 L 14 44 C 14 10 86 10 86 44 L 86 92 Z" fill="{STONE}" stroke="{WOOD}" stroke-width="5"/>'
           f'<ellipse cx="38" cy="78" rx="14" ry="14" fill="#d9b26f"/><ellipse cx="62" cy="78" rx="14" ry="14" fill="#d9b26f"/><ellipse cx="50" cy="58" rx="13" ry="13" fill="#d9b26f"/></svg>')

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
    target = lv(mp3("b5"))                                                   # Rafiq's Arabic level with Callum (the standard)
    for n in L:
        if n in ARABIC: subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp3(n), "-af", f"volume={target - lv(mp3(n)):.1f}dB,alimiter=limit=0.95", os.path.join(a, n + ".mp3")], check=True)
        else: shutil.copy(mp3(n), a)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-i", os.path.join(a, "drone.wav"), "-af",
                    f"atrim=0:{END},afade=t=in:d=0.6,afade=t=out:st={END - 0.4}:d=0.4", "-c:a", "libmp3lame", "-q:a", "3", os.path.join(a, "bed.mp3")], check=True)
    au = []
    def snd(name, t0, vol, d=None, track=None):
        d = d or dur(os.path.join(a, name))
        au.append(f'<audio id="s{len(au)}" src="assets/{name}" data-start="{max(0, t0):.3f}" data-duration="{d:.3f}" data-volume="{vol:.3f}" data-track-index="{track or 3 + len(au)}"></audio>')
    for n, t0 in L.items(): snd(f"{n}.mp3", t0, 1.0, track=None if n in ARABIC else 1)   # Rafiq's lines on their own tracks: the ayah's quiet tail runs under b5
    snd("bed.mp3", 0, 0.07, END, track=2)                                   # a low hum under it all
    js = []; T = js.append
    IN = lambda sel, t, y=40, d=0.5: T(f'tl.fromTo("{sel}", {{opacity:0, y:{y}}}, {{opacity:1, y:0, duration:{d}, ease:"power3.out"}}, {t:.2f});')
    POP = lambda sel, t, s=0.6: T(f'tl.fromTo("{sel}", {{opacity:0, scale:{s}}}, {{opacity:1, scale:1, duration:0.45, ease:"back.out(1.4)", transformOrigin:"50% 50%"}}, {t:.2f});')
    OUT = lambda sel, t: T(f'tl.to({sel}, {{opacity:0, y:-30, duration:0.3, ease:"power2.in"}}, {t:.2f});')
    def draw(sel, t, d=0.6): T(f'tl.fromTo("{sel}", {{strokeDashoffset:1}}, {{strokeDashoffset:0, duration:{d}, stagger:0.12, ease:"power2.inOut"}}, {t:.2f});')
    def pulse(sel, t, s=1.08): T(f'tl.fromTo("{sel}", {{scale:1}}, {{scale:{s}, duration:0.2, yoyo:true, repeat:1, ease:"power2.out", transformOrigin:"50% 50%", immediateRender:false}}, {t:.2f});')
    def drop(sel, t, r=20):     # falls in from above and lands with a bounce
        T(f'tl.fromTo("{sel}", {{opacity:0, y:-700, rotation:{r}}}, {{opacity:1, y:0, rotation:0, duration:0.6, ease:"bounce.out"}}, {t:.2f});')
    def count(sel, t, a0, b0, d, ticks=4):    # a number counting up, a tick as it goes
        T(f'tl.fromTo("{sel}", {{innerText:{a0}}}, {{innerText:{b0}, duration:{d}, snap:{{innerText:1}}, ease:"power2.out"}}, {t:.2f});')
        for k in range(ticks): snd("tick-lo.wav", t + d * (1 - (1 - (k + 1) / ticks) ** 2), 0.3)
    def scene(sel, t0, t1):
        if t0 > 0: T(f'tl.fromTo("{sel}", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.45, ease:"power3.out"}}, {t0:.2f});')
        if t1: T(f'tl.to("{sel}", {{opacity:0, y:-60, duration:0.35, ease:"power2.in"}}, {t1:.2f});'); snd("whoosh.wav", t1 - 0.05, 0.3)

    # the market lives the whole time: the sun sinks, the haze drifts, the lamps glow
    T(f'tl.fromTo("#sun", {{y:0}}, {{y:140, duration:{END:.2f}, ease:"sine.inOut"}}, 0);')
    T(f'tl.fromTo("#souk", {{x:0}}, {{x:-60, duration:{END:.2f}, ease:"sine.inOut"}}, 0);')
    T(f'tl.fromTo("#haze", {{x:0, opacity:0.5}}, {{x:120, opacity:0.9, duration:{END:.2f}, ease:"sine.inOut"}}, 0);')
    T(f'tl.fromTo(".lamp", {{opacity:0.5}}, {{opacity:1, duration:1.6, yoyo:true, repeat:{int(END / 1.6)}, ease:"sine.inOut"}}, 0);')

    # 1 · the hook: MAGAZINE; a magazine drops onto the table; an Arabic word; nothing to do with reading
    S2 = L["makhazin"] - 0.25
    mg = at("h1", "magazine"); drop("#mg1", mg - 0.2, -14); snd("thump.wav", mg + 0.3, 0.4)
    ab = at("h1", "arabic")
    POP("#tit", ab - 0.1, 0.7); snd("tap.wav", ab, 0.35)
    T(f'tl.fromTo("#ttl2", {{opacity:0, scale:1.6}}, {{opacity:1, scale:1, duration:0.45, ease:"back.out(1.4)"}}, {ab + 0.2:.2f});'); snd("impact.wav", ab + 0.2, 0.35, 1.2)
    rd = at("h1", "reading")
    POP("#qm", rd - 0.1, 0.4); snd("tick-lo.wav", rd, 0.45)
    scene("#s1", 0, S2 - 0.05)
    # 2 · مَخازِن: storehouses, for the grain, the oil, the goods
    scene("#s2", S2, L["b2"] - 0.35)
    POP("#mw", L["makhazin"] - 0.05, 0.7); snd("tick-lo.wav", L["makhazin"], 0.4)
    sh = at("b1", "storehouses")
    POP("#mm", sh - 0.05, 0.7); snd("tap.wav", sh, 0.35)
    for i, k in enumerate(("grain", "oil", "goods")):
        w0 = at("b1", k); drop(f"#it{i}", w0 - 0.3, (-1) ** i * 25); snd("thump.wav", w0 + 0.15, 0.4)
    # 3 · the root خ ز ن, to store away; مَـ: the place of; مَخْزَن, the place where you keep things
    S3 = L["b2"] - 0.1; scene("#s3", S3, L["b3"] - 0.35)
    rt = at("b2", "root")
    for i in range(3):
        T(f'tl.fromTo("#rl{i}", {{opacity:0, y:-200}}, {{opacity:1, y:0, duration:0.4, ease:"power3.out"}}, {rt - 0.15 + i * 0.14:.2f});'); snd("thump.wav", rt + i * 0.14, 0.3)
    st = at("b2", "store")
    POP("#rc", st - 0.05, 0.7); snd("tap.wav", st, 0.35)
    sf = at("b2", "safe")
    POP("#lock", sf - 0.05, 0.5); snd("click.wav", sf + 0.1, 0.6)
    ma = at("b2", "ma", exact=True)
    OUT('["#rtiles", "#rc", "#lock"]', ma - 0.35)
    POP("#pm", ma - 0.05, 0.6); snd("tap.wav", ma, 0.35)
    POP("#pmk", ma + 0.35, 0.7); snd("flip.wav", ma + 0.35, 0.35)
    pl = at("b2", "place")
    T(f'tl.to(".mpre", {{color:"{RED}", duration:0.3, ease:"power2.out"}}, {pl - 0.05:.2f});'); POP("#plc", pl - 0.05, 0.7); snd("shimmer.wav", pl, 0.3, 1.0)   # a red copy clipped to the مَـ (a kashida keeps Amiri from stacking مخ)
    th = at("b2", "things")
    POP("#plu", th - 0.1, 0.7); snd("tap.wav", th, 0.35)
    # 4 · magazzino → magasin (a shop) → 1580s → magazine: a storehouse
    S4 = L["b3"] - 0.1; scene("#s4", S4, L["b4"] - 0.35)
    for i, k in enumerate(("magazzino", "magasin")):
        w0 = at("b3", k, exact=True); POP(f"#wd{i}", w0 - 0.05, 0.7); snd("tap.wav", w0, 0.35)
        if i == 0: draw("#ar0", w0 + 0.6, 0.4)
    sp = at("b3", "shop"); POP("#shop", sp - 0.1, 0.7); snd("flip.wav", sp, 0.35)
    draw("#ar1", sp + 0.4, 0.4)
    yr = at("b3", "1580s"); POP("#yr", yr - 0.2, 0.7); count("#yrn", yr - 0.15, 1100, 1580, 0.7)
    mz = at("b3", "magazine", exact=True)
    IN("#wd2", mz - 0.15, 30); snd("shimmer.wav", mz, 0.35, 1.2); pulse("#wd2", mz + 0.45, 1.08)
    sh = at("b3", "storehouse"); POP("#sto", sh - 0.05, 0.7); snd("tap.wav", sh, 0.35)
    # 5 · the news stand; 1731; London; The Gentleman's Magazine: a storehouse of articles; the name stuck
    S5 = L["b4"] - 0.1; scene("#s5", S5, L["t1"] - 0.4)
    nw = at("b4", "news")
    for i in range(3): POP(f"#ns{i}", nw - 0.1 + i * 0.12, 0.6); snd("tap.wav", nw + i * 0.12, 0.3)
    y7 = at("b4", "1731"); POP("#y7", y7 - 0.2, 0.7); count("#y7n", y7 - 0.15, 1580, 1731, 0.9, 5)
    ld = at("b4", "london"); POP("#ldn", ld - 0.05, 0.7); snd("tap.wav", ld, 0.35)
    gm = at("b4", "gentleman")
    T(f'tl.to(["#ns0", "#ns2"], {{opacity:0, x:(i) => [-200, 200][i], duration:0.35, ease:"power2.in"}}, {gm - 0.4:.2f});')
    T(f'tl.to("#ns1", {{opacity:0, duration:0.25, ease:"power2.in"}}, {gm - 0.3:.2f});')
    T(f'tl.fromTo("#gmc", {{opacity:0, scale:0.5, rotation:-8}}, {{opacity:1, scale:1, rotation:0, duration:0.55, ease:"back.out(1.5)", transformOrigin:"50% 50%"}}, {gm - 0.1:.2f});'); snd("impact.wav", gm, 0.3, 1.0)
    ar = at("b4", "articles")
    T(f'tl.fromTo("#pages rect", {{opacity:0, x:(i) => [-420, 420, -380, 380][i], y:(i) => [-260, -200, 220, 260][i], rotation:(i) => [-30, 25, 20, -25][i]}}, {{opacity:1, x:0, y:0, rotation:0, duration:0.5, stagger:0.1, ease:"power3.out"}}, {ar - 0.4:.2f});')
    T(f'tl.to("#pages rect", {{opacity:0, duration:0.2, stagger:0.1, ease:"power2.in"}}, {ar + 0.3:.2f});')
    for k in range(4): snd("flip.wav", ar - 0.3 + k * 0.1, 0.2)
    sk = at("b4", "stuck"); POP("#stk", sk - 0.1, 0.5); pulse("#gmc", sk, 1.06); snd("thump.wav", sk, 0.45)
    # 6 · your turn: خ ز ن in Yūsuf 12:55: the armies / the roads / the storehouses? 3-2-1; the ayah; STOREHOUSES!
    S6 = L["t1"] - 0.1; scene("#s6", S6, L["end"] - 0.45)
    IN("#yt", L["t1"], 20)
    rt = at("t1", "root")
    for i in range(3):
        T(f'tl.fromTo("#tl{i}", {{opacity:0, y:-200}}, {{opacity:1, y:0, duration:0.4, ease:"power3.out"}}, {rt - 0.15 + i * 0.14:.2f});'); snd("thump.wav", rt + i * 0.14, 0.3)
    ys = at("t1", "yusuf")
    T(f'tl.to("#tiles", {{opacity:0, y:-30, duration:0.3, ease:"power2.in"}}, {ys - 0.3:.2f});')
    POP("#aya", ys - 0.1, 0.8); snd("flip.wav", ys, 0.4)
    kg = at("t1", "king"); IN("#ee0", kg - 0.1, 16)
    kz = at("t1", "khazaain"); T(f'tl.to("#hlw", {{color:"{RED}", duration:0.3, ease:"power2.out"}}, {kz - 0.05:.2f});'); pulse("#hlw", kz, 1.15); snd("tap.wav", kz, 0.4)
    for i, (k, last) in enumerate((("armies", False), ("roads", False), ("storehouses", True))):
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
    hit = at("b5", "storehouses")
    T(f'tl.to("#ops", {{opacity:0, y:30, duration:0.25, ease:"power2.in"}}, {hit - 0.25:.2f});')
    T(f'tl.fromTo("#slam", {{opacity:0, scale:1.8}}, {{opacity:1, scale:1, duration:0.45, ease:"back.out(1.7)"}}, {hit:.2f});')   # the one slam
    T(f'tl.fromTo("#cam", {{x:-14}}, {{x:14, duration:0.05, yoyo:true, repeat:7, ease:"sine.inOut", immediateRender:false}}, {hit + 0.05:.2f});')
    T(f'tl.set("#cam", {{x:0}}, {hit + 0.5:.2f});')
    snd("impact.wav", hit - 0.03, 0.75, 1.6)
    T(f'tl.fromTo("#burst i", {{opacity:1, x:0, y:0, scale:0.4}}, {{opacity:0, x:(i) => [-300, -170, 0, 170, 300, -90, 90][i], y:(i) => [-80, -200, -260, -200, -80, 150, 150][i], scale:1.3, duration:0.9, ease:"power2.out", immediateRender:false}}, {hit + 0.05:.2f});')
    pt = at("b5", "put")
    POP("#mean", pt - 0.1, 0.7); snd("tap.wav", pt, 0.4)
    gr = at("b5", "grain"); sv7 = at("b5", "seven")
    for k in range(7):
        T(f'tl.fromTo("#sk{k}", {{opacity:0, y:-260}}, {{opacity:1, y:0, duration:0.45, ease:"bounce.out"}}, {gr - 0.2 + k * 0.16:.2f});'); snd("thump.wav", gr + 0.2 + k * 0.16, 0.25)
    POP("#y7y", sv7 - 0.05, 0.7); count("#y7c", sv7 - 0.05, 1, 7, 0.6, 3)
    # 7 · the ask: which English word should we trace back next?
    S7 = L["end"] - 0.1; scene("#s7", S7, None)
    IN("#q", L["end"] + 0.1, 30)
    wd = at("end", "word"); IN("#stack", wd - 0.2, 60); snd("shimmer.wav", wd, 0.3, 1.2)
    cmt = at("end", "comment")
    POP("#url", cmt - 0.1, 0.8); snd("tap.wav", cmt, 0.4)
    T(f'tl.fromTo("#arr", {{opacity:0, y:0}}, {{opacity:1, y:18, duration:0.4, yoyo:true, repeat:3, ease:"sine.inOut"}}, {cmt:.2f});')

    # captions: the line being said, word by word, at the bottom
    caps = ""; k = 0
    for n in L:
        if n in ARABIC: continue
        ws = words(n); chunk = []
        for i, (w, s, e) in enumerate(ws):
            chunk.append((SHOW.get(w, w), s))
            if w[-1] in ",.:?!" or len(chunk) >= 6 or i + 1 == len(ws):
                nxt = L[n] + ws[i + 1][1] if i + 1 < len(ws) else L[n] + e + 0.4
                caps += f'<div class="cap" id="cp{k}">' + " ".join(f'<span id="cp{k}w{j}">{x}</span>' for j, (x, _) in enumerate(chunk)) + "</div>"
                T(f'tl.set("#cp{k}", {{opacity:1}}, {L[n] + chunk[0][1] - 0.02:.2f});')
                for j, (x, s0) in enumerate(chunk): T(f'tl.fromTo("#cp{k}w{j}", {{opacity:0, y:10}}, {{opacity:1, y:0, duration:0.2, ease:"power3.out"}}, {L[n] + s0:.2f});')
                T(f'tl.to("#cp{k}", {{opacity:0, duration:0.15, ease:"power2.in"}}, {nxt - 0.18:.2f});'); k += 1; chunk = []

    # the old market at dusk: arcades of storehouses, a dome and a minaret, lamps in the arches
    bld = ""
    for x, w, h in ((-60, 260, 300), (200, 220, 380), (420, 280, 260), (700, 220, 340), (920, 240, 300)):
        top = 1520 - h
        bld += f'<rect x="{x}" y="{top}" width="{w}" height="{h + 420}" fill="#4a2b3f"/><rect x="{x - 8}" y="{top - 14}" width="{w + 16}" height="18" fill="#3a2032"/>'
        bld += "".join(f'<path class="lamp" d="M{x + 40 + j * 90} {top + 150} L {x + 40 + j * 90} {top + 90} C {x + 40 + j * 90} {top + 50} {x + 100 + j * 90} {top + 50} {x + 100 + j * 90} {top + 90} L {x + 100 + j * 90} {top + 150} Z" fill="#f4c46e"/>'
                       for j in range(max(1, (w - 40) // 90)) if (j + x // 10) % 3 != 1)
    souk = (f'<g id="souk">{bld}<path d="M480 1262 C 480 1150 620 1150 620 1262 Z" fill="#4a2b3f"/><rect x="820" y="1040" width="34" height="200" fill="#4a2b3f"/>'
            f'<path d="M820 1040 L 837 996 L 854 1040 Z" fill="#4a2b3f"/></g>')
    sv = lambda inner: f'<svg class="full" viewBox="0 0 1080 1920">{inner}</svg>'
    arrow = lambda id, d: f'<path id="{id}" pathLength="1" d="{d}" fill="none" stroke="{GOLD}" stroke-width="7" stroke-linecap="round" stroke-dasharray="1" stroke-dashoffset="1"/>'
    tile = lambda id, ch, x, y, sz=190, fs=150: f'<div class="tile" id="{id}" style="left:{x}px;top:{y}px;width:{sz}px;height:{sz}px;line-height:{sz}px;font-size:{fs}px">{ch}</div>'
    burst = "".join(f'<i style="position:absolute;left:520px;top:960px;width:40px;height:40px;border-radius:50%;background:{c};opacity:0"></i>' for c in (GOLD, CREAM, RED, GOLD, CREAM, RED, GOLD))
    lock = (f'<svg width="150" height="170" viewBox="0 0 150 170"><path d="M40 80 L 40 50 C 40 10 110 10 110 50 L 110 80" fill="none" stroke="{CREAM}" stroke-width="16"/>'
            f'<rect x="15" y="75" width="120" height="90" rx="18" fill="{GOLD}" stroke="{WOOD}" stroke-width="6"/><circle cx="75" cy="112" r="12" fill="{WOOD}"/><rect x="69" y="116" width="12" height="28" rx="5" fill="{WOOD}"/></svg>')
    pages = "".join(f'<rect x="460" y="{820 + k * 10}" width="160" height="200" rx="6" fill="{CREAM}" stroke="{INK}" stroke-width="4" opacity="0"/>' for k in range(4))
    sacks7 = "".join(sack(150 + k * 130, 1330, 0.55, f"sk{k}") for k in range(7))
    css = f"""
@font-face {{ font-family:"CZ"; src:url("assets/cinzel-latin-700-normal.woff2"); }}
@font-face {{ font-family:"AM"; src:url("assets/amiri-arabic-700-normal.woff2"); }}
@font-face {{ font-family:"KA"; src:url("assets/karla-latin-700-normal.woff2"); }}
* {{ margin:0; box-sizing:border-box; }} html, body {{ width:1080px; height:1920px; overflow:hidden; background:#000; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; background:linear-gradient(#1f1838 0%, #4a2a52 34%, #9a4a58 62%, #d9824f 84%, #eaa45a 100%); font-family:KA; color:{CREAM}; }}
#cam {{ position:absolute; inset:0; }}
svg.full {{ position:absolute; left:0; top:0; width:1080px; height:1920px; overflow:visible; }}
.sc {{ position:absolute; inset:0; opacity:0; }} #s1 {{ opacity:1; }}
.t {{ position:absolute; left:0; right:0; text-align:center; opacity:0; }}
.cz {{ font-family:CZ; letter-spacing:.06em; color:{GOLD}; text-shadow:0 4px 0 {WOOD}, 0 10px 30px rgba(0,0,0,.5); }}
.am {{ font-family:AM; direction:rtl; color:{CREAM}; text-shadow:0 6px 0 {TEAL}, 0 14px 40px rgba(0,0,0,.45); line-height:1.3; }}
.pill {{ display:inline-flex; align-items:center; gap:14px; padding:8px 30px; border-radius:999px; background:rgba(30,18,40,.88); border:2px solid rgba(242,196,107,.6); font-family:KA; color:{CREAM}; }}
.cap {{ position:absolute; left:70px; right:70px; top:1600px; text-align:center; font-family:KA; font-size:50px; line-height:1.2; color:#fff; text-shadow:0 3px 0 rgba(0,0,0,.6), 0 0 18px rgba(0,0,0,.6); opacity:0; }}
.cap span {{ display:inline-block; opacity:0; }}
.card {{ position:absolute; left:60px; right:60px; padding:22px 26px 20px; border-radius:20px; background:#f3e3c0; color:{INK}; text-align:center; opacity:0;
  box-shadow:0 24px 50px rgba(0,0,0,.4), inset 0 0 0 6px #e3c993, inset 0 0 0 9px {TEAL}; }}
.card .aa {{ font-family:AM; direction:rtl; line-height:1.7; }}
.card .ee {{ font-family:CZ; font-size:30px; color:{TEAL}; margin-top:2px; }} .card small {{ display:block; font-size:28px; color:#6b5a44; margin-top:8px; }}
.hlw {{ display:inline-block; }}
.op {{ display:flex; align-items:center; gap:22px; width:640px; margin:18px auto 0; padding:12px 30px; border-radius:24px; background:rgba(246,235,211,.95); color:{INK}; font-family:CZ; font-size:46px; opacity:0; box-shadow:0 14px 30px rgba(0,0,0,.35); }}
.op svg {{ flex:none; }}
#cd {{ position:absolute; left:0; right:0; top:610px; text-align:center; font-family:CZ; font-size:130px; color:{GOLD}; opacity:0; text-shadow:0 6px 0 {WOOD}; }}
.tile {{ position:absolute; border-radius:30px; background:{CREAM}; color:{RED}; font-family:AM; text-align:center; opacity:0; box-shadow:0 14px 0 {WOOD}, 0 24px 40px rgba(0,0,0,.4); }}
.wd {{ position:absolute; left:0; right:0; text-align:center; opacity:0; }}
.wd span {{ display:inline-block; padding:10px 40px 6px; border-radius:24px; background:rgba(246,235,211,.96); color:{INK}; font-family:CZ; box-shadow:0 14px 30px rgba(0,0,0,.4); }}
.wd b {{ display:block; font-family:KA; font-size:28px; letter-spacing:.1em; color:{TEAL}; }}
.pair {{ position:absolute; left:0; right:0; text-align:center; opacity:0; }}
.pair .w {{ display:inline-block; font-family:AM; font-size:170px; line-height:1.25; direction:rtl; color:{CREAM}; text-shadow:0 6px 0 {TEAL}, 0 14px 40px rgba(0,0,0,.45); }}
.pair .w .mpre {{ color:{CREAM}; }}
#logo {{ position:absolute; top:62px; left:50%; transform:translateX(-50%); display:flex; justify-content:center; gap:12px; align-items:center; z-index:5; padding:6px 22px 6px 8px; border-radius:22px; background:rgba(30,18,40,.55); }}
#logo .tl {{ position:relative; width:58px; height:58px; border-radius:16px; background:{CREAM}; display:grid; place-items:center; }}
#logo .tl span {{ font-family:AM; font-size:38px; color:{INK}; margin-top:-6px; }} #logo .tl em {{ position:absolute; right:9px; top:8px; width:9px; height:9px; border-radius:50%; background:{RED}; }}
#logo b {{ font-family:AM; font-size:44px; color:{CREAM}; }}
"""
    body = f"""<div id="cam">
<svg class="full" viewBox="0 0 1080 1920"><g id="sun"><circle cx="300" cy="1060" r="190" fill="#ffd79a" opacity=".18"/><circle cx="300" cy="1060" r="120" fill="#ffcf7f"/></g>
 <g id="haze"><ellipse cx="300" cy="900" rx="420" ry="40" fill="#f6c9a0" opacity=".25"/><ellipse cx="820" cy="760" rx="360" ry="30" fill="#f6c9a0" opacity=".2"/></g>
 {souk}
</svg>
<div id="logo"><span class="tl"><span>ر</span><em></em></span><b>رَفِيق</b></div>
<div class="sc" id="s1">
 <div class="t cz" id="kick" style="top:180px;font-size:44px;opacity:1">THE STORY OF A WORD</div>
 <div class="t cz" id="ttl" style="top:250px;font-size:150px;opacity:1">MAGAZINE</div>
 <div class="t" id="tit" style="top:470px"><span class="pill" style="font-size:44px">an Arabic word</span></div>
 <div class="t am" id="ttl2" style="top:590px;font-size:180px;color:{GOLD}">مَخازِن</div>
 {sv(table(1450) + cover(540, 1236, 1.0, RED, "MAGAZINE", "mg1"))}
 <div class="t cz" id="qm" style="top:930px;left:740px;right:auto;width:200px;font-size:140px;color:{CREAM}">?</div>
</div>
<div class="sc" id="s2">
 <div class="t am" id="mw" style="top:170px;font-size:210px;color:{GOLD}">مَخازِن</div>
 <div class="t" id="mm" style="top:470px"><span class="pill" style="font-size:52px">makhāzin = <b style="color:{GOLD}">storehouses</b></span></div>
 {sv(store(540, 1520, 1.0) + sack(240, 1500, 1.0, "it0") + jar(540, 1500, 1.0, "it1") + crate(840, 1500, 1.0, "it2"))}
</div>
<div class="sc" id="s3">
 <div id="rtiles">{tile("rl0", "خ", 745, 230)}{tile("rl1", "ز", 445, 230)}{tile("rl2", "ن", 145, 230)}</div>
 <div class="t" id="rc" style="top:470px"><span class="pill" style="font-size:52px">the root = <b style="color:{GOLD}">to store away</b></span></div>
 <div class="t" id="lock" style="top:580px">{lock}</div>
 <div class="t" id="pm" style="top:180px"><span class="pill" style="font-size:52px"><b style="font-family:AM;font-size:70px;color:{GOLD}">مَـ</b> at the front</span></div>
 <div class="pair" id="pmk" style="top:330px"><div class="w" style="position:relative"><span>مَـخْزَن</span><span class="mpre" style="position:absolute;inset:0;clip-path:inset(0 0 0 67%)">مَـخْزَن</span></div></div>
 <div class="t" id="plc" style="top:580px"><span class="pill" style="font-size:48px">makhzan = <b style="color:{GOLD}">the place where you keep things</b></span></div>
 <div class="t" id="plu" style="top:690px"><span class="pill" style="font-size:42px">more than one: <b style="font-family:AM;font-size:60px;color:{GOLD}">مَخازِن</b></span></div>
 {sv(store(540, 1520, 0.85))}
</div>
<div class="sc" id="s4">
 <div class="wd" id="wd0" style="top:230px"><span style="font-size:76px"><b>ITALIAN</b>magazzino</span></div>
 {sv(arrow("ar0", "M540 450 L 540 520") + arrow("ar1", "M540 860 L 540 930"))}
 <div class="wd" id="wd1" style="top:540px"><span style="font-size:76px"><b>FRENCH</b>magasin</span></div>
 <div class="t" id="shop" style="top:760px"><span class="pill" style="font-size:42px">in France today: <b style="color:{GOLD}">a shop</b></span></div>
 <div class="t" id="yr" style="top:950px"><span class="pill" style="font-size:46px;font-family:CZ;color:{GOLD}"><span><span id="yrn">1580</span>s</span></span></div>
 <div class="wd" id="wd2" style="top:1050px"><span style="font-size:104px"><b>ENGLISH</b>MAGAZINE</span></div>
 <div class="t" id="sto" style="top:1330px"><span class="pill" style="font-size:46px">= <b style="color:{GOLD}">a storehouse</b></span></div>
</div>
<div class="sc" id="s5">
 <div class="t" id="y7" style="top:190px"><span class="pill" style="font-size:60px;font-family:CZ;color:{GOLD}" id="y7n">1731</span></div>
 <div class="t" id="ldn" style="top:320px"><span class="pill" style="font-size:44px">a <b style="color:{GOLD}">London</b> monthly</span></div>
 {sv(cover(250, 860, 0.8, TEAL, "NEWS", "ns0", 50) + cover(540, 860, 0.8, RED, "MONTHLY", "ns1", 40) + cover(830, 860, 0.8, NAVY, "WEEKLY", "ns2", 44)
     + cover(540, 900, 1.25, "#7a2d3a", "THE GENTLEMAN'S|MAGAZINE", "gmc", 26) + f'<g id="pages">{pages}</g>')}
 <div class="t" id="stk" style="top:1220px"><span class="pill" style="font-size:46px">a <b style="color:{GOLD}">storehouse</b> of articles</span></div>
</div>
<div class="sc" id="s6">
 <div class="t cz" id="yt" style="top:170px;font-size:76px">YOUR TURN</div>
 <div id="tiles">{tile("tl0", "خ", 745, 320)}{tile("tl1", "ز", 445, 320)}{tile("tl2", "ن", 145, 320)}</div>
 <div class="card" id="aya" style="top:280px"><div class="aa" style="font-size:56px">قالَ اجْعَلْنِي عَلى <span class="hlw" id="hlw">خَزائِنِ</span> الْأَرْضِ إِنِّي حَفِيظٌ عَلِيمٌ</div>
  <div style="position:relative;height:84px"><div class="ee" id="ee0" style="position:absolute;left:0;right:0;opacity:0">Put me in charge of the ___ of the land</div><div class="ee" id="ee1" style="position:absolute;left:0;right:0;opacity:0">Put me over the storehouses of the land:<br/>I am a knowing guardian</div></div>
  <small>the Qur’an · Yūsuf 12:55 · Yūsuf to the king</small></div>
 <div id="ops" style="position:absolute;left:0;right:0;top:800px"><div class="op" id="op0">{ARMY_I}<span>the armies</span></div><div class="op" id="op1">{ROAD_I}<span>the roads</span></div><div class="op" id="op2">{STORE_I}<span>the storehouses</span></div></div>
 <div id="cd">3</div>
 <div class="t cz" id="slam" style="top:800px;font-size:100px;line-height:1.1">STOREHOUSES!</div>
 <div class="t" id="mean" style="top:960px"><span class="pill" style="font-size:42px"><b style="font-family:AM;font-size:60px;color:{GOLD}">خَزائِن</b> storehouses</span></div>
 {sv(sacks7)}
 <div class="t" id="y7y" style="top:1380px"><span class="pill" style="font-size:44px"><b style="color:{GOLD}" id="y7c">7</b>&nbsp;hard years of grain, saved</span></div>
 <div id="burst">{burst}</div>
</div>
<div class="sc" id="s7">
 <div class="t" id="q" style="top:190px"><div class="cz" style="display:inline-block;padding:18px 40px 12px;border-radius:28px;background:rgba(30,18,40,.82);font-size:62px;line-height:1.25">WHICH WORD<br/>SHOULD WE TRACE NEXT?</div></div>
 {sv('<g id="stack" opacity="0" style="opacity:0">' + table(1450) + cover(400, 1230, 0.95, TEAL, "MAGAZINE", "", 40) + cover(680, 1236, 1.0, RED, "MAGAZINE") + '</g>')}
 <div class="t" id="url" style="top:700px"><span class="pill" style="font-size:50px;background:{TEAL}">rafiq-arabic.com</span></div>
 <div class="t" id="arr" style="top:560px;font-size:80px">👇</div>
</div>
</div>"""
    body = body[:-6] + caps + "</div>"
    open(os.path.join(out, "index.html"), "w").write(f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" /><title>magazine</title>
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
