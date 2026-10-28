#!/usr/bin/env python3
"""h3-lisan in the new format (owner, 28 Oct 2026, #303: "fix H3 Lisan like we did yesterday, nicer graphics, nicer font"): the same lines
(brag-quiz/voice/lisan-lines.json) told with full-screen drawings on a cinematic dusk desert (layered dunes, a low sun, two moons, drifting
sand), Cinzel for the titles and Amiri for the Arabic, every move on its word, eased as MOTION-STYLE.md says:
  1 "Everyone in Dune chants Lisan al-Gaib…": robed figures on the ridge raise their fists; on "Arabic" the title turns into لِسانُ الْغَيْب
  2 لِسان (Rafiq) · "tongue… and language": a tongue, then speech bubbles in many scripts
  3 "The Qur'an says it came down in a clear Arabic lisan": light comes down onto an open mushaf; 26:195 with lisan lit
  4 your turn: the first page of al-Baqarah; الْغَيْب (Rafiq); the desert / the unseen / the future, 3-2-1; "the UNSEEN!": the worm bursts out of
    the sand; "everything hidden from our eyes": a sandstorm veils it; 2:3; غ = gh
  5 لِسانُ الْغَيْب (Rafiq) · "the tongue of the unseen"
  6 "Herbert didn't invent it…": a book, 1965 rolls back to 1390, Shiraz draws in, Hafez, Lisān al-Ghayb
  7 the ask: Muad'Dib or Usul? Then the cream end card.
No clip from the film, no Dune logo or the film's font (as #303). Figures are faceless (owner, 27 Oct).

  python3 brag-quiz/reels/lisan/build.py    then  cd brag-quiz/reels/lisan/out/v && npx hyperframes render -o ../lisan-raw.mp4
"""
import json, os, re, shutil, subprocess
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
V6 = os.path.join(ROOT, "brag-output-v6/composition/assets"); VO = os.path.join(ROOT, "brag-quiz/voice/lisan")
INK, CREAM, GOLD, SAND, RUST, TEAL, RED = "#17262B", "#F6EBD3", "#F2C46B", "#E7B07A", "#8A3B16", "#2E7263", "#B4322A"
dur = lambda f: float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))
mp3 = lambda n: os.path.join(VO, n + ".mp3")
def words(n):
    ws = json.load(open(os.path.join(VO, n + ".words.json")))
    return [(w[0], w[1], w[2] if len(w) > 2 else (ws[i + 1][1] if i + 1 < len(ws) else w[1] + 0.45)) for i, w in enumerate(ws)]
ORDER = [("h1", 0.3), ("lisan", 0.35), ("b1", 0.3), ("b1b", 0.4), ("t1", 0.55), ("ghayb", 0.25), ("t1b", 0.3), ("b2t", 3.6),
         ("lisanghayb", 0.7), ("b3t", 0.3), ("b4", 0.6), ("end", 0.7)]                                 # b2t waits for the 3-2-1
ARABIC = ("lisan", "ghayb", "lisanghayb")
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

def build():
    out = os.path.join(HERE, "out", "v"); a = os.path.join(out, "assets")
    if os.path.exists(out): shutil.rmtree(out)
    os.makedirs(a)
    for f in ("karla-latin-700-normal.woff2",): shutil.copy(os.path.join(V6, "fonts", f), a)
    for f in ("cinzel-latin-700-normal.woff2", "amiri-arabic-700-normal.woff2"): shutil.copy(os.path.join(ROOT, "brag-quiz/fonts", f), a)
    shutil.copy(os.path.join(V6, "lib/gsap.min.js"), a)
    for f in ("shimmer.wav", "tick-lo.wav", "thump.wav", "whoosh.wav", "flip.wav", "impact.wav", "rumble.wav", "wind.wav"): shutil.copy(os.path.join(ROOT, "brag-quiz/sfx/soft", f), a)
    for f in ("click.wav", "swoosh.wav", "tap.wav"): shutil.copy(os.path.join(ROOT, "brag-quiz/sfx/ref", f), a)
    lv = lambda f: float(re.findall(r"I:\s+(-?[\d.]+) LUFS", subprocess.run(["ffmpeg", "-i", f, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr)[-1])
    target = lv(mp3("b4"))                                                   # Rafiq's Arabic level with Callum (the standard)
    for n in L:
        if n in ARABIC: subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp3(n), "-af", f"volume={target - lv(mp3(n)):.1f}dB,alimiter=limit=0.95", os.path.join(a, n + ".mp3")], check=True)
        else: shutil.copy(mp3(n), a)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-i", os.path.join(a, "wind.wav"), "-af",
                    f"atrim=0:{END},afade=t=in:d=0.6,afade=t=out:st={END - 0.4}:d=0.4", "-c:a", "libmp3lame", "-q:a", "3", os.path.join(a, "bed.mp3")], check=True)
    au = []
    def snd(name, t0, vol, d=None, track=None):
        d = d or dur(os.path.join(a, name))
        au.append(f'<audio id="s{len(au)}" src="assets/{name}" data-start="{max(0, t0):.3f}" data-duration="{d:.3f}" data-volume="{vol:.3f}" data-track-index="{track or 3 + len(au)}"></audio>')
    for n, t0 in L.items(): snd(f"{n}.mp3", t0, 1.0, track=1)
    snd("bed.mp3", 0, 0.12, END, track=2)                                   # the desert wind under it all
    js = []; T = js.append
    IN = lambda sel, t, y=40, d=0.5: T(f'tl.fromTo("{sel}", {{opacity:0, y:{y}}}, {{opacity:1, y:0, duration:{d}, ease:"power3.out"}}, {t:.2f});')
    POP = lambda sel, t, s=0.6: T(f'tl.fromTo("{sel}", {{opacity:0, scale:{s}}}, {{opacity:1, scale:1, duration:0.45, ease:"back.out(1.4)"}}, {t:.2f});')
    OUT = lambda sel, t, y=-40: T(f'tl.to("{sel}", {{opacity:0, y:{y}, duration:0.3, ease:"power2.in"}}, {t:.2f});')
    def draw(sel, t, d=0.6): T(f'tl.fromTo("{sel}", {{strokeDashoffset:1}}, {{strokeDashoffset:0, duration:{d}, ease:"power2.inOut"}}, {t:.2f});')
    def scene(sel, t0, t1):
        if t0 > 0: T(f'tl.fromTo("{sel}", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.45, ease:"power3.out"}}, {t0:.2f});')
        if t1: T(f'tl.to("{sel}", {{opacity:0, y:-60, duration:0.35, ease:"power2.in"}}, {t1:.2f});'); snd("whoosh.wav", t1 - 0.05, 0.3)
    def count(sel, a0, b0, t, d):
        T(f'(() => {{ const o = {{v:{a0}}}, el = document.querySelector("{sel}"); tl.to(o, {{v:{b0}, duration:{d}, ease:"power2.out", onUpdate:() => el.textContent = Math.round(o.v)}}, {t:.2f}); }})();')
        for k in range(12): snd("click.wav", t + d * (1 - (1 - (k + 1) / 12) ** 2) * 0.95, 0.15)

    # the desert lives the whole time: the sand drifts, the moons rise a little
    T(f'tl.fromTo("#grains", {{x:0}}, {{x:-260, duration:{END:.2f}, ease:"sine.inOut"}}, 0);')
    T(f'tl.fromTo("#moons", {{y:30}}, {{y:-30, duration:{END:.2f}, ease:"sine.inOut"}}, 0);')
    T(f'tl.fromTo("#dune1", {{x:0}}, {{x:-60, duration:{END:.2f}, ease:"sine.inOut"}}, 0);')

    # 1 · the hook: the chanting figures, the title turns Arabic on "Arabic"
    ch = at("h1", "chants")
    T(f'tl.fromTo(".arm", {{rotation:0}}, {{rotation:-60, duration:0.22, yoyo:true, repeat:5, stagger:0.04, ease:"power2.out", svgOrigin:"0 0", immediateRender:false}}, {ch:.2f});')
    snd("thump.wav", ch + 0.15, 0.25); snd("thump.wav", ch + 0.6, 0.25)
    T(f'tl.fromTo("#ttl", {{scale:1}}, {{scale:1.06, duration:0.25, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}}, {at("h1", "lisan"):.2f});'); snd("whoosh.wav", at("h1", "lisan") - 0.1, 0.4)
    ab = at("h1", "arabic")
    T(f'tl.to("#ttl", {{opacity:0, y:-30, duration:0.25, ease:"power2.in"}}, {ab - 0.15:.2f});')
    POP("#ttlar", ab, 0.7); snd("shimmer.wav", ab, 0.3, 1.2)
    IN("#qmark", ab + 0.4, 20)
    S2 = L["lisan"] - 0.2; scene("#s1", 0, S2 - 0.05)
    # 2 · لِسان: "tongue… and language"
    scene("#s2", S2, L["b1b"] - 0.35)
    POP("#lw", L["lisan"] - 0.05, 0.7); snd("tick-lo.wav", L["lisan"], 0.4)
    POP("#tongue", at("b1", "tongue") - 0.1, 0.5); snd("tap.wav", at("b1", "tongue"), 0.4)
    T(f'tl.fromTo("#tongue .tg", {{scaleY:0.2}}, {{scaleY:1, duration:0.35, ease:"back.out(1.4)", transformOrigin:"50% 0%"}}, {at("b1", "tongue"):.2f});')
    lg = at("b1", "language")
    for i in range(5): POP(f"#sb{i}", lg - 0.05 + i * 0.1, 0.4); snd("tap.wav", lg + i * 0.1, 0.25)
    # 3 · "The Qur'an says it came down in a clear Arabic lisan: a clear Arabic tongue"
    S3 = L["b1b"] - 0.1; scene("#s3", S3, L["t1"] - 0.4)
    T(f'tl.fromTo("#beam", {{scaleY:0, opacity:0}}, {{scaleY:1, opacity:1, duration:0.7, ease:"power3.out", transformOrigin:"50% 0%"}}, {at("b1b", "came"):.2f});'); snd("shimmer.wav", at("b1b", "came"), 0.35, 1.2)
    IN("#mus", at("b1b", "qur") - 0.2, 60)
    T(f'tl.fromTo("#musR", {{rotationY:0}}, {{rotationY:-165, duration:0.7, ease:"power2.inOut", transformOrigin:"0% 50%"}}, {at("b1b", "says"):.2f});'); snd("flip.wav", at("b1b", "says"), 0.4)
    IN("#aya1", at("b1b", "clear") - 0.1, 30)
    T(f'tl.to("#aya1 .hl", {{backgroundColor:"rgba(242,196,107,.55)", duration:0.3, ease:"power2.out"}}, {at("b1b", "lisan"):.2f});'); snd("tick-lo.wav", at("b1b", "lisan"), 0.4)
    # 4 · your turn: the first page of al-Baqarah; الْغَيْب; three answers, 3-2-1; the UNSEEN: the worm; the sandstorm; 2:3
    S4 = L["t1"] - 0.1; scene("#s4", S4, L["lisanghayb"] - 0.45)
    IN("#yt", L["t1"], 20)
    POP("#page", at("t1", "page") - 0.1, 0.8); snd("flip.wav", at("t1", "page"), 0.35)
    T(f'tl.to("#page", {{opacity:0, scale:0.6, y:-120, duration:0.35, ease:"power2.in"}}, {L["ghayb"] - 0.35:.2f});')
    POP("#gw", L["ghayb"] - 0.05, 0.7); snd("tick-lo.wav", L["ghayb"], 0.4)
    o0 = round(L["t1b"] + spoken("t1b") + 0.05, 2)
    for i in range(3): POP(f"#op{i}", L["t1b"] + 0.1 + i * 0.2, 0.8); snd("tap.wav", L["t1b"] + 0.1 + i * 0.2, 0.25)
    c0 = o0 + 0.3
    for k, nm in enumerate(("3", "2", "1")):
        T(f'tl.set("#cd", {{textContent:"{nm}", opacity:1}}, {c0 + k:.2f});'); T(f'tl.fromTo("#cd", {{scale:1.4}}, {{scale:1, duration:0.35, ease:"power3.out"}}, {c0 + k:.2f});')
        snd("click.wav", c0 + k, 0.5)
    T(f'tl.to("#cd", {{opacity:0, duration:0.2, ease:"power2.in"}}, {L["b2t"] - 0.1:.2f});')
    un = at("b2t", "unseen")
    T(f'tl.to("#op1", {{backgroundColor:"{GOLD}", scale:1.08, duration:0.3, ease:"back.out(1.4)"}}, {L["b2t"]:.2f});')
    T(f'tl.to(["#op0", "#op2"], {{opacity:0.3, duration:0.3, ease:"power2.in"}}, {L["b2t"]:.2f});')
    T(f'tl.to("#ops, #gw", {{opacity:0, y:-40, duration:0.3, ease:"power2.in"}}, {un + 0.5:.2f});')
    T(f'tl.set("#worm", {{opacity:1}}, {un - 0.1:.2f});')
    T(f'tl.fromTo("#worm", {{y:700}}, {{y:0, duration:0.55, ease:"power3.out", immediateRender:false}}, {un - 0.1:.2f});')
    OUT("#yt", un - 0.1)            # the worm bursts out of the sand
    T(f'tl.fromTo("#burst i", {{opacity:1, x:0, y:0, scale:0.4}}, {{opacity:0, x:(i) => [-260, -140, 0, 150, 270, -60, 80][i], y:(i) => [-160, -260, -300, -250, -150, -200, -220][i], scale:1.4, duration:0.9, ease:"power2.out"}}, {un:.2f});')
    T(f'tl.fromTo("#cam", {{x:-14}}, {{x:14, duration:0.05, yoyo:true, repeat:9, ease:"sine.inOut", immediateRender:false}}, {un:.2f});')
    T(f'tl.set("#cam", {{x:0}}, {un + 0.55:.2f});')
    snd("impact.wav", un - 0.05, 0.8, 1.6); snd("rumble.wav", un - 0.2, 0.5, 1.5)
    T(f'tl.fromTo("#unseen", {{opacity:0, scale:1.8}}, {{opacity:1, scale:1, duration:0.45, ease:"back.out(1.7)"}}, {un:.2f});')   # the one slam
    hd = at("b2t", "hidden")
    T(f'tl.fromTo("#storm", {{opacity:0, x:900}}, {{opacity:1, x:0, duration:0.8, ease:"power2.inOut"}}, {hd - 0.3:.2f});'); snd("wind.wav", hd - 0.3, 0.5, 1.6)
    T(f'tl.to("#worm", {{opacity:0, duration:0.6, ease:"power2.in"}}, {hd + 0.2:.2f});')
    IN("#aya2", at("b2t", "eyes") + 0.3, 30); POP("#gh", at("b2t", "eyes") + 1.3, 0.7); snd("tap.wav", at("b2t", "eyes") + 1.3, 0.3)
    # 5 · لِسانُ الْغَيْب: "the tongue of the unseen"
    S5 = L["lisanghayb"] - 0.25; scene("#s5", S5, L["b4"] - 0.45)
    T(f'tl.fromTo("#storm", {{opacity:1}}, {{opacity:0, duration:0.4, ease:"power2.in", immediateRender:false}}, {S5:.2f});')
    POP("#lgw", L["lisanghayb"] - 0.05, 0.7); snd("tick-lo.wav", L["lisanghayb"], 0.4)
    IN("#lg0", L["lisanghayb"] + 0.2, 20); IN("#lg1", L["lisanghayb"] + 0.9, 20)
    tg = at("b3t", "tongue")
    T(f'tl.fromTo("#tou", {{opacity:0, scale:1.5}}, {{opacity:1, scale:1, duration:0.45, ease:"back.out(1.4)"}}, {tg - 0.05:.2f});'); snd("shimmer.wav", tg, 0.35, 1.2)
    T(f'tl.to("#tou em", {{color:"{GOLD}", duration:0.3, ease:"power2.out"}}, {at("b3t", "unseen"):.2f});')
    # 6 · "Herbert didn't invent it… five hundred years before Dune… Hafez… Lisan al-Ghayb"
    S6 = L["b4"] - 0.1; scene("#s6", S6, L["end"] - 0.45)
    IN("#dbook", at("b4", "herbert") - 0.1, 50); snd("tap.wav", at("b4", "herbert"), 0.3)
    T(f'tl.fromTo("#dbook", {{rotation:0}}, {{rotation:-6, duration:0.08, yoyo:true, repeat:3, ease:"power2.inOut", immediateRender:false}}, {at("b4", "invent"):.2f});')
    fv = at("b4", "five")
    IN("#yr", fv - 0.2, 20); count("#yrn", 1965, 1390, fv, 1.6)
    T(f'tl.to("#dbook", {{opacity:0.25, scale:0.8, x:-260, duration:0.5, ease:"power2.inOut"}}, {fv:.2f});')
    draw(".shz", at("b4", "persian") - 0.2, 0.9); snd("whoosh.wav", at("b4", "persian") - 0.2, 0.3)
    T(f'tl.fromTo(".cyp", {{scaleY:0}}, {{scaleY:1, duration:0.4, stagger:0.08, ease:"back.out(1.4)", transformOrigin:"50% 100%"}}, {at("b4", "persian") + 0.3:.2f});')
    POP("#hafez", at("b4", "hafez") - 0.1, 0.7); snd("tick-lo.wav", at("b4", "hafez"), 0.4)
    T(f'tl.fromTo("#rose", {{opacity:0, scale:0, rotation:-40}}, {{opacity:1, scale:1, rotation:0, duration:0.5, ease:"back.out(1.4)"}}, {at("b4", "hafez") + 0.3:.2f});')
    POP("#hlg", at("b4", "lisan", last=True) - 0.1, 0.6); snd("shimmer.wav", at("b4", "lisan", last=True), 0.35, 1.2)
    # 7 · the ask
    S7 = L["end"] - 0.1; scene("#s7", S7, None)
    IN("#ask", L["end"] + 0.05, 30)
    POP("#vm", at("end", "muad") - 0.1, 0.6); snd("tap.wav", at("end", "muad"), 0.4)
    POP("#vu", at("end", "usul") - 0.1, 0.6); snd("tap.wav", at("end", "usul"), 0.4)
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

    rng = np.random.default_rng(4)
    grains = "".join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#fbe2bd" opacity="{o:.2f}"/>' for x, y, r, o in
                     zip(rng.uniform(0, 1400, 140), rng.uniform(700, 1900, 140), rng.uniform(1.5, 4, 140), rng.uniform(0.2, 0.6, 140)))
    stars = "".join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#fff6dc" opacity="{o:.2f}"/>' for x, y, r, o in
                    zip(rng.uniform(0, 1080, 60), rng.uniform(0, 600, 60), rng.uniform(1, 3, 60), rng.uniform(0.3, 0.9, 60)))
    robe = lambda x, s, c: (f'<g transform="translate({x},1010) scale({s})"><path d="M-40 0 C -36 -80 -30 -120 0 -150 C 30 -120 36 -80 40 0 Z" fill="{c}"/>'
                            f'<path d="M-24 -150 C -24 -196 24 -196 24 -150 C 24 -130 -24 -130 -24 -150 Z" fill="{c}"/>'
                            f'<g class="arm" transform="translate(14,-120)"><path d="M0 0 L 34 -10" stroke="{c}" stroke-width="16" stroke-linecap="round"/><circle cx="36" cy="-11" r="10" fill="{c}"/></g></g>')
    crowd = "".join(robe(x, s, c) for x, s, c in ((160, 0.9, "#3b1e12"), (300, 1.0, "#2e170e"), (430, 0.85, "#3b1e12"), (650, 0.9, "#2e170e"), (780, 1.05, "#3b1e12"), (920, 0.85, "#2e170e")))
    def card(id, ar, en, ref, top, hl=None):
        if hl: ar = ar.replace(hl, f'<span class="hl">{hl}</span>', 1)
        return f'<div class="card" id="{id}" style="top:{top}px"><div class="aa">{ar}</div><div class="ee">{en}</div><small>{ref}</small></div>'
    css = f"""
@font-face {{ font-family:"CZ"; src:url("assets/cinzel-latin-700-normal.woff2"); }}
@font-face {{ font-family:"AM"; src:url("assets/amiri-arabic-700-normal.woff2"); }}
@font-face {{ font-family:"KA"; src:url("assets/karla-latin-700-normal.woff2"); }}
* {{ margin:0; box-sizing:border-box; }} html, body {{ width:1080px; height:1920px; overflow:hidden; background:#000; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; background:linear-gradient(#1b1d3a 0%, #4a2f55 30%, #b4573a 55%, #f0a35e 68%, #f7c98b 74%); font-family:KA; color:{CREAM}; }}
#cam {{ position:absolute; inset:0; }}
svg.full {{ position:absolute; left:0; top:0; width:1080px; height:1920px; overflow:visible; }}
.sc {{ position:absolute; inset:0; opacity:0; }} #s1 {{ opacity:1; }}
.t {{ position:absolute; left:0; right:0; text-align:center; opacity:0; }}
.cz {{ font-family:CZ; letter-spacing:.06em; color:{GOLD}; text-shadow:0 4px 0 {RUST}, 0 10px 30px rgba(0,0,0,.5); }}
.am {{ font-family:AM; direction:rtl; color:{CREAM}; text-shadow:0 6px 0 {RUST}, 0 14px 40px rgba(0,0,0,.45); line-height:1.3; }}
.pill {{ display:inline-block; padding:8px 30px; border-radius:999px; background:rgba(23,38,43,.78); border:2px solid rgba(242,196,107,.6); font-family:KA; color:{CREAM}; }}
.cap {{ position:absolute; left:70px; right:70px; top:1580px; text-align:center; font-family:KA; font-size:50px; line-height:1.2; color:#fff; text-shadow:0 3px 0 rgba(0,0,0,.55), 0 0 18px rgba(0,0,0,.5); opacity:0; }}
.cap span {{ display:inline-block; opacity:0; }}
.card {{ position:absolute; left:110px; right:110px; padding:28px 30px 24px; border-radius:20px; background:#f3e3c0; color:{INK}; text-align:center; opacity:0;
  box-shadow:0 24px 50px rgba(0,0,0,.4), inset 0 0 0 6px #e3c993, inset 0 0 0 9px {RUST}; }}
.card .aa {{ font-family:AM; font-size:78px; direction:rtl; line-height:1.5; }} .card .hl {{ border-radius:12px; padding:0 8px; }}
.card .ee {{ font-family:CZ; font-size:38px; color:{RUST}; margin-top:4px; }} .card small {{ display:block; font-size:26px; color:#6b5a44; margin-top:8px; }}
.op {{ display:flex; align-items:center; gap:22px; width:640px; margin:18px auto 0; padding:18px 30px; border-radius:24px; background:rgba(246,235,211,.95); color:{INK}; font-family:CZ; font-size:46px; opacity:0; box-shadow:0 14px 30px rgba(0,0,0,.35); }}
.op svg {{ flex:none; }}
#cd {{ position:absolute; left:0; right:0; top:1290px; text-align:center; font-family:CZ; font-size:140px; color:{GOLD}; opacity:0; text-shadow:0 6px 0 {RUST}; }}
.sb {{ position:absolute; padding:10px 28px; border-radius:30px; background:{CREAM}; color:{INK}; font-size:56px; opacity:0; box-shadow:0 10px 24px rgba(0,0,0,.35); }}
#logo {{ position:absolute; top:70px; left:0; right:0; display:flex; justify-content:center; gap:12px; align-items:center; z-index:5; }}
#logo .tile {{ position:relative; width:58px; height:58px; border-radius:16px; background:{CREAM}; display:grid; place-items:center; }}
#logo .tile span {{ font-family:AM; font-size:38px; color:{INK}; margin-top:-6px; }} #logo .tile em {{ position:absolute; right:9px; top:8px; width:9px; height:9px; border-radius:50%; background:{RED}; }}
#logo b {{ font-family:AM; font-size:44px; color:{CREAM}; }}
"""
    ICON = {"desert": f'<svg width="70" height="50" viewBox="0 0 70 50"><path d="M0 50 C 15 20 30 20 40 35 C 50 25 60 25 70 40 L 70 50 Z" fill="{SAND}" stroke="{RUST}" stroke-width="3"/><circle cx="52" cy="14" r="9" fill="{GOLD}"/></svg>',
            "unseen": f'<svg width="70" height="50" viewBox="0 0 70 50"><path d="M5 5 L 65 5 L 65 12 C 50 20 50 40 65 48 L 5 48 C 20 40 20 20 5 12 Z" fill="#6b4a8a" stroke="{INK}" stroke-width="3"/><path d="M35 8 L 35 48" stroke="{INK}" stroke-width="3"/></svg>',
            "future": f'<svg width="70" height="50" viewBox="0 0 70 50"><path d="M20 3 L 50 3 L 50 8 C 50 20 38 22 38 25 C 38 28 50 30 50 42 L 50 47 L 20 47 L 20 42 C 20 30 32 28 32 25 C 32 22 20 20 20 8 Z" fill="{CREAM}" stroke="{INK}" stroke-width="3"/><path d="M26 44 L 44 44 L 35 34 Z" fill="{SAND}"/></svg>'}
    ops = "".join(f'<div class="op" id="op{i}">{ICON[k]}<span>the {k}</span></div>' for i, k in enumerate(("desert", "unseen", "future")))
    sbs = "".join(f'<div class="sb" id="sb{i}" style="left:{x}px;top:{y}px;{st}">{w}</div>' for i, (w, x, y, st) in enumerate(
        (("ع", 170, 1000, "font-family:AM"), ("Aa", 760, 990, "font-family:CZ"), ("你好", 120, 1200, ""), ("Bonjour", 680, 1210, "font-family:CZ;font-size:44px"), ("سَلام", 420, 1330, "font-family:AM"))))
    worm = (f'<g id="worm" style="opacity:0"><path d="M300 1500 C 290 1200 360 1000 540 960 C 720 1000 790 1200 780 1500 Z" fill="#7a4a2a"/>'
            + "".join(f'<path d="M{310 + i * 6} {1460 - i * 90} C 420 {1420 - i * 90}, 660 {1420 - i * 90}, {770 - i * 6} {1460 - i * 90}" fill="none" stroke="#5a341c" stroke-width="8"/>' for i in range(5))
            + f'<ellipse cx="540" cy="1010" rx="190" ry="70" fill="#2a120a"/>'
            + "".join(f'<path d="M{540 + 170 * np.cos(np.radians(a)):.0f} {1010 + 60 * np.sin(np.radians(a)):.0f} L {540 + 120 * np.cos(np.radians(a)):.0f} {1010 + 40 * np.sin(np.radians(a)):.0f}" stroke="#f6ebd3" stroke-width="10" stroke-linecap="round"/>' for a in range(0, 360, 20))
            + '</g>')
    burst = "".join('<i style="position:absolute;left:520px;top:1000px;width:40px;height:40px;border-radius:50%;background:#e7b07a;opacity:0"></i>' for _ in range(7))
    body = f"""<div id="cam">
<svg class="full" viewBox="0 0 1080 1920">{stars}
 <g id="moons"><circle cx="985" cy="175" r="48" fill="#f3ead8" opacity=".92"/><circle cx="968" cy="165" r="48" fill="#4a2f55" opacity=".25"/><circle cx="905" cy="250" r="17" fill="#f3ead8" opacity=".8"/></g>
 <circle cx="300" cy="1060" r="190" fill="#ffd9a0" opacity=".55"/><circle cx="300" cy="1060" r="130" fill="#ffe7bf" opacity=".8"/>
 <path id="dune1" d="M-100 1080 C 150 980 360 1040 560 1000 C 760 960 900 1010 1200 980 L 1200 1920 L -100 1920 Z" fill="#c97b45"/>
 <path d="M-100 1230 C 200 1140 420 1240 680 1180 C 880 1140 1000 1190 1200 1160 L 1200 1920 L -100 1920 Z" fill="#b5652f"/>
 <path d="M-100 1420 C 260 1330 520 1440 760 1380 C 920 1340 1040 1380 1200 1360 L 1200 1920 L -100 1920 Z" fill="#9a5226"/>
 <g id="grains">{grains}</g>
</svg>
<div id="logo"><span class="tile"><span>ر</span><em></em></span><b>رَفِيق</b></div>
<div class="sc" id="s1">
 <div class="t cz" id="ttl" style="top:270px;font-size:118px;opacity:1">LISAN<br>AL-GAIB</div>
 <div class="t am" id="ttlar" style="top:250px;font-size:170px;color:{GOLD}">لِسانُ الْغَيْب</div>
 <div class="t cz" id="qmark" style="top:560px;font-size:64px;color:{CREAM}">…in Arabic?</div>
 <svg class="full" viewBox="0 0 1080 1920">{crowd}</svg>
</div>
<div class="sc" id="s2">
 <div class="t am" id="lw" style="top:240px;font-size:250px">لِسان</div>
 <div class="t" id="tongue" style="top:690px"><svg width="300" height="230" viewBox="0 0 300 230"><path d="M30 40 C 80 10 220 10 270 40 C 230 70 70 70 30 40 Z" fill="#7a2c22"/>
  <g class="tg"><path d="M95 52 C 95 200 205 200 205 52 Z" fill="#e5737a" stroke="#7a2c22" stroke-width="6"/><path d="M150 70 L 150 150" stroke="#b9464f" stroke-width="6" stroke-linecap="round"/></g></svg>
  <div><span class="pill" style="font-size:48px">tongue</span></div></div>
 {sbs}<div class="t" id="sbl" style="top:1450px;opacity:1"></div>
</div>
<div class="sc" id="s3">
 <div id="beam" style="position:absolute;left:340px;top:0;width:400px;height:1000px;background:linear-gradient(rgba(255,240,200,0), rgba(255,240,200,.55));clip-path:polygon(40% 0, 60% 0, 100% 100%, 0 100%);opacity:0"></div>
 <div id="mus" style="position:absolute;left:330px;top:640px;width:420px;height:300px;opacity:0;perspective:1200px">
  <div style="position:absolute;left:0;top:0;width:210px;height:300px;background:#f8efd9;border:6px solid {RUST};border-radius:14px 0 0 14px;padding:40px 22px">{''.join(f'<div style="height:9px;margin:18px 0;border-radius:5px;background:#cdb991"></div>' for _ in range(6))}</div>
  <div style="position:absolute;left:210px;top:0;width:210px;height:300px;background:#f8efd9;border:6px solid {RUST};border-radius:0 14px 14px 0;padding:40px 22px">{''.join(f'<div style="height:9px;margin:18px 0;border-radius:5px;background:#cdb991"></div>' for _ in range(6))}</div>
  <div id="musR" style="position:absolute;left:210px;top:0;width:210px;height:300px;background:{TEAL};border:6px solid {GOLD};border-radius:0 14px 14px 0;backface-visibility:hidden;display:grid;place-items:center"><svg width="120" height="120" viewBox="0 0 120 120"><path d="M60 6 L 74 46 L 114 46 L 82 70 L 94 110 L 60 86 L 26 110 L 38 70 L 6 46 L 46 46 Z" fill="none" stroke="{GOLD}" stroke-width="5"/></svg></div></div>
 {card("aya1", "بِلِسانٍ عَرَبِيٍّ مُبِينٍ", "in a clear Arabic tongue", "the Qur’an · ash-Shuʿarāʾ 26:195", 1000, "بِلِسانٍ")}
</div>
<div class="sc" id="s4">
 <div class="t cz" id="yt" style="top:200px;font-size:72px">YOUR TURN</div>
 <div class="t" id="page" style="top:330px"><svg width="440" height="600" viewBox="0 0 440 600"><rect x="10" y="10" width="420" height="580" rx="18" fill="#f8efd9" stroke="{RUST}" stroke-width="8"/>
  <rect x="40" y="40" width="360" height="90" rx="40" fill="{TEAL}" stroke="{GOLD}" stroke-width="5"/><text x="220" y="102" text-anchor="middle" font-family="AM" font-size="52" fill="{GOLD}">سُورَةُ الْبَقَرَة</text>
  {''.join(f'<rect x="50" y="{170 + i * 45}" width="340" height="12" rx="6" fill="#cdb991"/>' for i in range(9))}</svg>
  <div><span class="pill" style="font-size:40px">al-Baqarah · page one</span></div></div>
 <div class="t am" id="gw" style="top:300px;font-size:220px">الْغَيْب</div>
 <div id="ops" style="position:absolute;left:0;right:0;top:720px">{ops}</div>
 <div id="cd">3</div>
 <svg class="full" viewBox="0 0 1080 1920">{worm}</svg>{burst}
 <div class="t cz" id="unseen" style="top:520px;font-size:120px">THE UNSEEN</div>
 <div id="storm" style="position:absolute;left:-200px;top:600px;width:1480px;height:1100px;opacity:0;background:radial-gradient(ellipse at 50% 50%, rgba(231,176,122,.95), rgba(201,123,69,.8) 60%, rgba(201,123,69,0) 75%);filter:blur(30px)"></div>
 {card("aya2", "الَّذِينَ يُؤْمِنُونَ بِالْغَيْبِ", "those who believe in the unseen", "the Qur’an · al-Baqarah 2:3", 820)}
 <div class="t" id="gh" style="top:1240px"><span class="pill" style="font-size:46px"><b class="am" style="font-size:60px;color:{GOLD};text-shadow:none">غ</b> = gh, not g</span></div>
</div>
<div class="sc" id="s5">
 <div class="t am" id="lgw" style="top:300px;font-size:180px">لِسانُ الْغَيْب</div>
 <div class="t" id="lg0" style="top:640px;left:560px;right:auto;width:420px"><span class="pill" style="font-size:44px">tongue</span></div>
 <div class="t" id="lg1" style="top:640px;left:100px;right:auto;width:420px"><span class="pill" style="font-size:44px">the unseen</span></div>
 <div class="t cz" id="tou" style="top:820px;font-size:92px;line-height:1.2;color:{CREAM}">THE TONGUE<br>OF <em style="font-style:normal">THE UNSEEN</em></div>
</div>
<div class="sc" id="s6">
 <div id="dbook" style="position:absolute;left:390px;top:330px;width:300px;height:400px;border-radius:10px 22px 22px 10px;background:linear-gradient(#d39a5c,#a8642f);border:6px solid #5a2e14;opacity:0;box-shadow:0 20px 40px rgba(0,0,0,.4)">
  <div style="position:absolute;left:0;right:0;top:60px;text-align:center;font-family:CZ;font-size:44px;color:#3a1a0a">A NOVEL</div>
  <div style="position:absolute;left:0;right:0;bottom:50px;text-align:center;font-family:CZ;font-size:56px;color:#3a1a0a">1965</div></div>
 <div class="t cz" id="yr" style="top:230px;font-size:64px;color:{CREAM}">THE YEAR<br><b id="yrn" style="font-size:150px;color:{GOLD}">1965</b></div>
 <svg class="full" viewBox="0 0 1080 1920">
  <path class="shz" pathLength="1" d="M180 1060 L 180 900 L 300 900 L 300 1060 M 240 900 C 240 830 200 820 240 760 C 280 820 240 830 240 900" fill="none" stroke="{CREAM}" stroke-width="8" stroke-dasharray="1" stroke-dashoffset="1"/>
  <path class="shz" pathLength="1" d="M400 1060 L 400 860 C 400 720 680 720 680 860 L 680 1060 M 540 740 L 540 680" fill="none" stroke="{CREAM}" stroke-width="9" stroke-dasharray="1" stroke-dashoffset="1"/>
  <path class="shz" pathLength="1" d="M780 1060 L 780 820 L 820 780 L 860 820 L 860 1060" fill="none" stroke="{CREAM}" stroke-width="8" stroke-dasharray="1" stroke-dashoffset="1"/>
  {''.join(f'<path class="cyp" d="M{x} 1060 C {x - 22} 1000 {x - 14} 940 {x} 880 C {x + 14} 940 {x + 22} 1000 {x} 1060 Z" fill="#2c4a33"/>' for x in (130, 350, 730, 930))}
  <g id="rose" transform="translate(540,1180)"><circle r="34" fill="{RED}"/><path d="M-18 -6 C -6 -26 18 -18 14 2 C 10 18 -14 16 -10 0" fill="none" stroke="#7a1c16" stroke-width="5"/><path d="M0 34 L 0 110" stroke="#2c4a33" stroke-width="8"/></g>
 </svg>
 <div class="t" id="hafez" style="top:1310px"><span class="pill" style="font-size:50px">Hafez of Shiraz · d. 1390</span></div>
 <div class="t am" id="hlg" style="top:1390px;font-size:110px;color:{GOLD}">لِسانُ الْغَيْب</div>
</div>
<div class="sc" id="s7">
 <div class="t cz" id="ask" style="top:250px;font-size:80px;line-height:1.15;color:{CREAM}">WHICH DUNE<br>WORD NEXT?</div>
 <div class="t" id="vm" style="top:560px;left:90px;right:auto;width:420px"><div class="card" style="position:relative;left:0;right:0;opacity:1"><div class="aa">مُؤَدِّب</div><div class="ee">MUAD’DIB</div></div></div>
 <div class="t" id="vu" style="top:560px;left:570px;right:auto;width:420px"><div class="card" style="position:relative;left:0;right:0;opacity:1"><div class="aa">أُصُول</div><div class="ee">USUL</div></div></div>
 <div class="t" id="url" style="top:1020px"><span class="pill" style="font-size:52px;background:{TEAL}">rafiq-arabic.com</span></div>
 <div class="t" id="arr" style="top:1130px;font-size:90px">👇</div>
</div>
{caps}</div>"""
    open(os.path.join(out, "index.html"), "w").write(f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" /><title>lisan</title>
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
