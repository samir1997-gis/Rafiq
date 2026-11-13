#!/usr/bin/env python3
"""f1-five, "5 words everyone should know" (owner, 13 Nov 2026): the five small words that are over 7,700 of the Qur'an's 78,245 words, counted
on the text (Tanzil; the word alone or with wa/fa in front, never with endings, so a floor): min 3,195 · lā 1,626 · fī 1,221 · alladhīna 984 ·
ʿalā 710 = 7,736. Motion graphics, light (cream and ink, gold): a lit Mushaf page of al-Baqarah fills the background, the camera drifting over
it; each word, as it comes, lights up everywhere on the page; its count runs up with a click on every step; a meter fills with its share of
the Qur'an. The g4 standard: Callum's hook with FIVE shouted and slammed, words one at a time, Rafiq says the Arabic, a 3-2-1 quiz on the
fifth, the comment ask heard in full, the fountain bed.

  python3 brag-quiz/reels/five/build.py   then  cd brag-quiz/reels/five/out/v && npx -y hyperframes@0.9.30 render -o ../raw.mp4
"""
import json, math, os, random, re, shutil, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
V6 = os.path.join(ROOT, "brag-output-v6/composition/assets"); VO = os.path.join(ROOT, "brag-quiz/voice/five")
FONTS, SFX = os.path.join(ROOT, "brag-quiz/fonts"), os.path.join(ROOT, "brag-quiz/sfx")
CREAM, PAPER, INK, GOLD, GOLD2, RED, TEAL = "#F1ECE0", "#f6f1e4", "#17262B", "#a8842c", "#E9B949", "#B4322A", "#2e7263"
HOOK = os.environ.get("HOOK", "h1")
dur = lambda f: float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))
OUT = os.path.join(HERE, "out", "v"); A = os.path.join(OUT, "assets")
STRIP = lambda w: re.sub("[ً-ْٰ۟ۡۥۦ]", "", w)

# the five: (key, Arabic, meaning, count, the line it's in, its source)
WORDS = [("min", "مِنْ", "from", 3195, "مِنْ شَرِّ مَا خَلَقَ", "“from the evil of what He created” · al-Falaq 113:2"),
         ("la", "لَا", "no · not", 1626, "لَا إِلَٰهَ إِلَّا اللَّهُ", "“there is no god but Allah” · the shahada"),
         ("fi", "فِي", "in", 1221, "يَدْخُلُونَ فِي دِينِ اللَّهِ", "“entering into the religion of Allah” · an-Naṣr 110:2"),
         ("alladhina", "الَّذِينَ", "those who", 984, "صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ", "“the path of those who You blessed” · al-Fātiḥah 1:7"),
         ("ala", "عَلَى", "over · on", 710, "إِنَّ اللَّهَ عَلَىٰ كُلِّ شَيْءٍ قَدِيرٌ", "“Allah has power over everything” · al-Baqarah 2:20")]
TOTAL = 78245
PLAIN = {"min": "من", "la": "لا", "fi": "في", "alladhina": "الذين", "ala": "على"}

def words(n):
    f = os.path.join(VO, n + ".words.json")
    if not os.path.exists(f):
        from faster_whisper import WhisperModel
        s, _ = WhisperModel("base.en", compute_type="int8").transcribe(os.path.join(VO, n + ".mp3"), word_timestamps=True)
        json.dump([[w.word.strip(), round(float(w.start), 2)] for x in s for w in x.words], open(f, "w"))
    out = []
    for w, t in (tuple(x[:2]) for x in json.load(open(f))):     # whisper splits "3,000" and "al-Falaq": join them back
        if out and (w[:1] in ",-" or (w[:1].isdigit() and out[-1][0][-1:].isdigit())): out[-1] = (out[-1][0] + w, out[-1][1])
        else: out.append((w, t))
    k = SPEED.get(n, 1.0)
    return [(w, round(t / k, 2)) for w, t in out]

SPEED = {"h1": 1.15, "h2": 1.15}                                  # the hook takes are slow (8.3 s): 15% faster, the pitch kept
# the lines in order, with the pause before each
SEQ = [(HOOK, 0.1), ("n1", 0.35), ("min", 0.1), ("d1", 0.15), ("n2", 0.45), ("la", 0.1), ("d2", 0.15), ("n3", 0.45), ("fi", 0.1), ("d3", 0.15),
       ("n4", 0.45), ("alladhina", 0.1), ("d4", 0.15), ("t1", 0.5), ("ala", 0.15), ("qadir", 0.25), ("t2", 0.25), ("a1", 3.4), ("end", 0.4)]
CAPS = {   # one token per spoken word ("+" glues it to the next); *gold
 "n1": "Number one.", "d1": "*From. Over 3,000 times. You say it in al-Falaq: from the evil of what He created.",
 "n2": "Number two.", "d2": "*No, or *not. Over 1,600 times. It starts the shahada: there is no god but Allah.",
 "n3": "Number three.", "d3": "*In. Over 1,200 times. Like in an-Naṣr: people entering into the religion of Allah.",
 "n4": "Number four.", "d4": "*Those *who. Nearly a thousand times. You say it in every salah: the path of those who You blessed.",
 "t1": "Your turn. Number five comes over 700 times.", "t2": "Does it mean *in, *from, or *over?",
 "a1": "*Over. Allah has power over everything.", "end": "How many did you know before this? Zero to five? Comment below!"}

def chunks(n, k):
    """caption chunks of about k tokens, broken after punctuation where possible"""
    toks = CAPS[n].split(); out, cur = [], 0
    for i, t in enumerate(toks):
        cur += 1
        if cur >= k or (cur >= 2 and t.rstrip("+")[-1:] in ".:?,!") or i == len(toks) - 1: out.append(cur); cur = 0
    return out

def build():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(A)
    for f in ("fredoka-latin-700-normal.woff2", "amiri-arabic-700-normal.woff2", "instrument-serif-latin-400-normal.woff2"): shutil.copy(os.path.join(FONTS, f), A)
    shutil.copy(os.path.join(V6, "lib/gsap.min.js"), A)
    for f in ("swoosh.wav", "short-swoosh.wav", "click.wav", "tap.wav"): shutil.copy(os.path.join(SFX, "ref", f), A)
    for f in ("shimmer.wav", "impact.wav", "flip.wav"): shutil.copy(os.path.join(SFX, "soft", f), A)
    for f in ("crash.wav", "boom.wav"): shutil.copy(os.path.join(SFX, f), A)
    for n, _ in SEQ:                                            # Callum and Rafiq level with each other (-19 LUFS); the mix goes to -16 after
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(VO, n + ".mp3"), "-af", f"atempo={SPEED.get(n, 1.0)},aresample=48000,loudnorm=I=-19:TP=-2:LRA=11,aresample=48000",
                        "-ar", "48000", os.path.join(A, n + ".wav")], check=True)
    W = {n: words(n) for n in list(CAPS) + [HOOK]}
    L, t = {}, 0.0
    for n, gap in SEQ:
        t += gap; L[n] = round(t, 2); t += dur(os.path.join(A, n + ".wav"))
    END = round(t + 1.3, 2)
    D = lambda n: dur(os.path.join(A, n + ".wav"))
    def at(n, key, k=0):
        return L[n] + [s for w, s in W[n] if key in w.lower()][k]

    au = []
    def snd(name, t0, vol, d=None, track=None):
        d = d or dur(os.path.join(A, name))
        au.append(f'<audio id="s{len(au)}" src="assets/{name}" data-start="{max(0, t0):.3f}" data-duration="{d:.3f}" data-volume="{vol:.3f}" data-track-index="{track or 4 + len(au)}"></audio>')
    for n, _ in SEQ: snd(n + ".wav", L[n], 1.0, track=1)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-i", os.path.join(V6, "sfx-gen/fountain.mp3"), "-af",
                    f"atrim=0:{END},afade=t=in:d=0.6,afade=t=out:st={END - 1.5}:d=1.5", "-c:a", "libmp3lame", "-q:a", "3", os.path.join(A, "bed.mp3")], check=True)
    snd("bed.mp3", 0, 0.1, END, track=2)
    js = []; T = js.append
    def fro(sel, a, b, t0, ir=False): T(f'tl.fromTo("{sel}", {a}, {b[:-1] + ("" if ir else ", immediateRender:false")}}}, {t0:.2f});')
    to = lambda sel, b, t0: T(f'tl.to("{sel}", {b}, {t0:.2f});')
    cam = lambda x, y, s, r, d, t0, ease="sine.inOut": T(f'tl.to(CAM, {{x:{x}, y:{y}, s:{s}, r:{r}, duration:{d}, ease:"{ease}", onUpdate:camSet}}, {t0:.2f});')
    def count(sel, n, t0, d=1.1, steps=12, vol=0.22):              # a number running up, eased out, a click on every step
        T(f'(() => {{ const o = {{v:0}}; tl.fromTo(o, {{v:0}}, {{v:{n}, duration:{d}, ease:"power2.out", immediateRender:false, onUpdate:() => {{ document.querySelector("{sel}").textContent = Math.round(o.v).toLocaleString("en-GB"); }}}}, {t0:.2f}); }})();')
        for k in range(steps):
            u = 1 - (1 - (k + 1) / steps) ** 0.5                     # the clicks bunch where the number moves fastest (power2.out)
            snd("click.wav", t0 + d * u, vol)
    def whip(t0):
        fro("#whip", "{opacity:0, x:-300}", "{opacity:1, x:300, duration:0.22, ease:\"power2.inOut\"}", t0 - 0.12)
        to("#whip", "{opacity:0, duration:0.1, ease:\"power2.in\"}", t0 + 0.1)
        snd("swoosh.wav", t0 - 0.2, 0.4)

    # ---- the hook: the line word by word; FIVE huge from frame 0, slamming on the shout; 7,736 counting up behind ----
    hw = W[HOOK]; five_i = next(i for i, (w, s) in enumerate(hw) if "five" in w.lower())
    toks = [re.sub(r"[^A-Za-z0-9',.\-]", "", w) for w, s in hw]
    seen = set(); fixed = []                                     # "seven thousand seven hundred" on screen as 7,700
    for w in toks:
        lw = w.lower().strip(",.")
        if lw in ("seven", "thousand", "hundred") or lw.replace(",", "").isdigit(): fixed.append("" if "num" in seen else "7,700"); seen.add("num")
        else: fixed.append(w)
    toks = fixed
    hl = "".join((f'<br><span class="hw five" id="hw{i}">FIVE</span><br>' if i == five_i else (f'<span class="hw" id="hw{i}">{w}</span> ' if w else "")) for i, w in enumerate(toks))
    FIVE = L[HOOK] + hw[five_i][1]
    for i, (w, s) in enumerate(hw):
        if i == five_i or not toks[i]: continue
        fro(f"#hw{i}", "{opacity:0, x:%d, filter:\"blur(8px)\"}" % (-50 if i % 2 else 50), "{opacity:1, x:0, filter:\"blur(0px)\", duration:0.22, ease:\"power3.out\"}", L[HOOK] + s)
    T(f'tl.set("#hw{five_i}", {{opacity:1, scale:2.6, y:520}}, 0);')
    fro(f"#hw{five_i}", "{scale:2.6}", "{scale:2.8, duration:%.2f, ease:\"sine.inOut\"}" % max(0.3, FIVE - 0.25), 0.01)
    fro(f"#hw{five_i}", "{scale:2.8, y:520}", "{scale:1, y:0, duration:0.2, ease:\"power4.in\"}", FIVE - 0.18)
    snd("crash.wav", FIVE, 0.75); snd("boom.wav", FIVE, 0.45)
    T(f'tl.to("#shake", {{keyframes:[{{x:-24, y:12}}, {{x:20, y:-16}}, {{x:-12, y:9}}, {{x:7, y:-5}}, {{x:0, y:0}}], duration:0.42, ease:"power1.out"}}, {FIVE + 0.02:.2f});')
    fro(f"#hw{five_i}", "{scaleY:0.78, scaleX:1.18}", "{scaleY:1, scaleX:1, duration:0.45, ease:\"elastic.out(1.2,0.4)\"}", FIVE + 0.02)
    fro(".ring", "{scale:0.2, opacity:0.9}", "{scale:3.2, opacity:0, duration:0.7, ease:\"power2.out\", stagger:0.08}", FIVE + 0.02)
    fro(".spark", "{x:0, y:0, opacity:1, scale:1}", "{x:(i, el) => +el.dataset.dx, y:(i, el) => +el.dataset.dy, opacity:0, scale:0.3, duration:0.6, ease:\"power3.out\"}", FIVE + 0.02)
    fro("#flash", "{opacity:0.7}", "{opacity:0, duration:0.35, ease:\"power2.out\"}", FIVE + 0.02)
    fro("#bigcount", "{opacity:0, scale:0.8}", "{opacity:1, scale:1, duration:0.4, ease:\"back.out(1.7)\"}", L[HOOK] + 0.05, ir=True)
    count("#bcn", 7736, L[HOOK] + 0.1, d=max(1.2, FIVE - L[HOOK] - 0.4), steps=16, vol=0.18)
    fro(".pw", "{color:\"rgba(23,38,43,.28)\"}", "{color:\"%s\", duration:0.5, ease:\"power2.out\", stagger:{each:0.004, from:\"random\"}}" % GOLD, FIVE + 0.05)  # every one of them on the page
    to(".pw", "{color:\"rgba(23,38,43,.28)\", duration:0.5, ease:\"power2.inOut\"}", L["n1"] - 0.4)
    T(f'tl.to("#hook, #bigcount", {{opacity:0, y:-40, duration:0.35, ease:"power2.in"}}, {L["n1"] - 0.35:.2f});')
    cam(560, 900, 1.06, -1.5, L["n1"], 0.0)

    # ---- the five ----
    share, cum = 0, 0
    pos = [(470, 720, 1.1, 1.2), (620, 1100, 1.12, -1.0), (480, 1400, 1.1, 1.4), (600, 820, 1.14, -1.2), (520, 1200, 1.1, 0.8)]
    for k, (key, ar, mean, n, line, src) in enumerate(WORDS):
        quiz = k == 4
        start = L["t1"] if quiz else L[f"n{k + 1}"]; said = L[key]
        nxt = L["end"] if quiz else (L[f"n{k + 2}"] if k < 3 else L["t1"])
        if k: whip(start)
        cam(*pos[k], 2.4, start - 0.3, "power2.inOut")
        fro(f"#num{k}", "{opacity:0, scale:1.6}", "{opacity:1, scale:1, duration:0.35, ease:\"back.out(2)\"}", start); snd("impact.wav", start, 0.3)
        fro(f"#card{k}", "{opacity:0, y:60, rotationX:-20}", "{opacity:1, y:0, rotationX:0, duration:0.5, ease:\"power3.out\"}", said - 0.25)
        fro(f"#card{k} .big", "{scale:0.6, filter:\"blur(14px)\"}", "{scale:1, filter:\"blur(0px)\", duration:0.45, ease:\"back.out(1.6)\"}", said - 0.2)
        snd("short-swoosh.wav", said - 0.25, 0.3)
        T(f'tl.to(".k-{key}", {{backgroundColor:"rgba(233,185,73,.55)", color:"{INK}", boxShadow:"0 0 18px rgba(233,185,73,.8)", duration:0.4, ease:"power2.out", stagger:{{each:0.03, from:"random"}}}}, {said + 0.1:.2f});')
        snd("shimmer.wav", said + 0.1, 0.3)
        T(f'tl.to(".k-{key}", {{backgroundColor:"rgba(233,185,73,.22)", boxShadow:"0 0 0px rgba(233,185,73,0)", duration:0.6, ease:"power2.inOut"}}, {nxt - 0.4:.2f});')
        if not quiz:
            d = f"d{k + 1}"
            fro(f"#card{k} .mean", "{opacity:0, y:16}", "{opacity:1, y:0, duration:0.35, ease:\"power3.out\"}", L[d])
            tc = L[d] + W[d][next(i for i, (w, s) in enumerate(W[d]) if w.lower().startswith(("over", "nearly")))][1]
            fro(f"#card{k} .cnt", "{opacity:0, scale:0.8}", "{opacity:1, scale:1, duration:0.3, ease:\"back.out(2)\"}", tc - 0.1)
            count(f"#c{k}", n, tc, d=1.2)
            key_w, nth = {"d1": ("from", 1), "d2": ("there", 0), "d3": ("people", 0), "d4": ("path", 0)}[d]   # the line starts here
            tl_line = L[d] + [s for w, s in W[d] if w.lower().startswith(key_w)][nth] - 0.15
        else:
            fro(f"#card{k} .cnt", "{opacity:0, scale:0.8}", "{opacity:1, scale:1, duration:0.3, ease:\"back.out(2)\"}", at("t1", "over") - 0.1)
            count(f"#c{k}", n, at("t1", "over"), d=1.2)
            tl_line = L["qadir"] - 0.1
        fro(f"#line{k}", "{opacity:0, y:40}", "{opacity:1, y:0, duration:0.45, ease:\"power3.out\"}", tl_line); snd("flip.wav", tl_line, 0.25)
        fro(f"#line{k} .hl", "{backgroundSize:\"0% 100%\"}", "{backgroundSize:\"100% 100%\", duration:0.45, ease:\"power2.out\"}", tl_line + 0.35)
        cum += n; share = 100 * cum / TOTAL
        reveal = L["a1"] - 0.1 if quiz else tl_line
        T(f'(() => {{ const o = {{v:{100 * (cum - n) / TOTAL:.2f}}}; tl.to(o, {{v:{share:.2f}, duration:0.9, ease:"power2.out", onUpdate:() => {{ document.getElementById("mpct").textContent = o.v.toFixed(1) + "%"; document.getElementById("mfill").style.width = (o.v * 9) + "%"; }}}}, {reveal + 0.3:.2f}); }})();')
        snd("tap.wav", reveal + 0.3, 0.3)
        T(f'tl.set("#dot{k}", {{backgroundColor:"{GOLD2}", borderColor:"{GOLD}"}}, {said:.2f});')
        if quiz:
            for j, opt in enumerate(("in", "from", "over")):
                tk = at("t2", opt)
                fro(f"#opt{j}", "{opacity:0, y:40, scale:0.85}", "{opacity:1, y:0, scale:1, duration:0.4, ease:\"back.out(1.8)\"}", tk - 0.08); snd("tap.wav", tk, 0.35)
            to("#meter", "{opacity:0, y:30, duration:0.3, ease:\"power2.in\"}", L["t2"] - 0.2)          # the options and the countdown take its place
            to("#meter", "{opacity:1, y:0, duration:0.4, ease:\"power3.out\"}", L["a1"] + 0.1)
            cd = L["t2"] + D("t2") + 0.2
            fro("#ring3", "{opacity:0, scale:0.6}", "{opacity:1, scale:1, duration:0.3, ease:\"back.out(2)\"}", cd - 0.1)
            fro("#ring3 .fg", "{strokeDashoffset:0}", "{strokeDashoffset:339, duration:3, ease:\"power1.inOut\"}", cd)
            for j in range(3):
                T(f'tl.set("#rnum", {{textContent:"{3 - j}"}}, {cd + j:.2f});'); snd("click.wav", cd + j, 0.6)
                fro("#rnum", "{scale:1.4}", "{scale:1, duration:0.4, ease:\"back.out(2)\"}", cd + j)
            rv = L["a1"] - 0.1
            to("#ring3", "{opacity:0, scale:1.4, duration:0.3, ease:\"power2.in\"}", rv - 0.15)
            to("#opt0, #opt1", "{opacity:0.3, scale:0.92, duration:0.35, ease:\"power2.out\"}", rv)
            fro("#opt2", "{scale:1}", "{scale:1.12, backgroundColor:\"%s\", color:\"%s\", duration:0.4, ease:\"back.out(2.2)\"}" % (GOLD2, INK), rv)
            fro("#card4 .mean", "{opacity:0, y:16}", "{opacity:1, y:0, duration:0.35, ease:\"power3.out\"}", rv)
            fro("#flash", "{opacity:0.5}", "{opacity:0, duration:0.4, ease:\"power2.out\"}", rv); snd("shimmer.wav", rv, 0.5); snd("impact.wav", rv, 0.4)
            to("#card4, #line4, #opts, #num4", "{opacity:0, y:-50, duration:0.4, ease:\"power2.in\"}", L["end"] - 0.35)
        else:
            to(f"#card{k}, #line{k}, #num{k}", "{opacity:0, y:-50, duration:0.35, ease:\"power2.in\"}", nxt - 0.3)

    # ---- end: the total, and the ask ----
    whip(L["end"])
    cam(540, 960, 0.92, 0, 3, L["end"] - 0.3, "power2.inOut")
    T(f'tl.to(".pw.k", {{backgroundColor:"rgba(233,185,73,.5)", duration:0.6, ease:"power2.out", stagger:{{each:0.01, from:"random"}}}}, {L["end"]:.2f});')
    fro("#endc", "{opacity:0, scale:0.85}", "{opacity:1, scale:1, duration:0.5, ease:\"back.out(1.8)\"}", L["end"] - 0.05)
    fro("#endc .opts2 span", "{opacity:0, y:30}", "{opacity:1, y:0, duration:0.35, ease:\"back.out(2)\", stagger:0.08}", at("end", "0") - 0.05)
    for j in range(6): snd("tap.wav", at("end", "0") - 0.05 + 0.08 * j, 0.2)
    T(f'tl.set("#endc", {{opacity:1}}, {END - 0.01:.2f});')

    # ---- captions: word by word, alternating sides, gold on the key words ----
    cap_html = ""
    for n, text in CAPS.items():
        tk, ws = text.split(), W[n]
        if len(tk) != len(ws): raise SystemExit(f"{n}: {len(tk)} caption tokens for {len(ws)} spoken words: {[w for w, _ in ws]}")
        i = 0
        for c, size in enumerate(chunks(n, 5)):
            cid = f"c{n}{c}"; spans = ""
            for j in range(i, i + size):
                t0 = tk[j]; glue = t0.endswith("+"); t0 = t0.rstrip("+"); gold = "*" in t0; t0 = t0.replace("*", "")
                spans += f'<span class="cw{" g" if gold else ""}" id="{cid}w{j - i}">{t0}</span>' + ("" if glue else " ")
            cap_html += f'<div class="cap" id="{cid}">{spans}</div>'
            st = L[n] + ws[i][1]; nx = L[n] + ws[i + size][1] if i + size < len(ws) else L[n] + D(n) + 0.2
            T(f'tl.set("#{cid}", {{opacity:1}}, {st - 0.02:.2f});')
            for j in range(size):
                fro(f"#{cid}w{j}", "{opacity:0, x:%d, filter:\"blur(6px)\"}" % (-40 if j % 2 else 40), "{opacity:1, x:0, filter:\"blur(0px)\", duration:0.2, ease:\"power3.out\"}", L[n] + ws[i + j][1])
            T(f'tl.to("#{cid}", {{opacity:0, duration:0.12, ease:"power2.in"}}, {nx - 0.06:.2f});')
            i += size

    # ---- the page: al-Baqarah 2:2-25, each of the five tagged where it stands ----
    text = open(os.path.join(HERE, "baqarah.txt")).read().split("\n", 1)[1].split()
    keyof = {v: k for k, v in PLAIN.items()}
    pw = ""
    for w in text:
        s = STRIP(w); k = keyof.get(s) or keyof.get(s[1:] if s[:1] in "وف" else "")
        pw += f'<span class="pw{" k k-" + k if k else ""}">{w}</span> '
    rnd = random.Random(3)
    sparks = "".join(f'<div class="spark" data-dx="{math.cos(a) * r:.0f}" data-dy="{math.sin(a) * r:.0f}" style="transform:rotate({math.degrees(a):.0f}deg)"></div>'
                     for a, r in ((j * math.tau / 16 + 0.2, 300 + (j % 3) * 90) for j in range(16)))
    cards = ""
    for k, (key, ar, mean, n, line, src) in enumerate(WORDS):
        word = PLAIN[key]
        hl_line = " ".join((f'<span class="hl">{x}</span>' if STRIP(x) == word else x) for x in line.split())
        cards += (f'<div class="num" id="num{k}">{"YOUR TURN" if k == 4 else f"Nº {k + 1}"}</div>'
                  f'<div class="card" id="card{k}"><div class="big">{ar}</div><div class="mean">{mean}</div>'
                  f'<div class="cnt"><b id="c{k}">0</b><small>times</small></div></div>'
                  f'<div class="line" id="line{k}"><div class="ar">{hl_line}</div><div class="src">{src}</div></div>')
    opts = "".join(f'<div class="opt" id="opt{j}">{o}</div>' for j, o in enumerate(("in", "from", "over")))
    dots = "".join(f'<i id="dot{k}"></i>' for k in range(5))
    css = f"""
@font-face {{ font-family:"FR"; src:url("assets/fredoka-latin-700-normal.woff2"); }}
@font-face {{ font-family:"AM"; src:url("assets/amiri-arabic-700-normal.woff2"); }}
@font-face {{ font-family:"IS"; src:url("assets/instrument-serif-latin-400-normal.woff2"); }}
* {{ margin:0; box-sizing:border-box; }} html, body {{ width:1080px; height:1920px; overflow:hidden; background:{CREAM}; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; background:{CREAM}; }}
#shake, #world {{ position:absolute; inset:0; }}
#page {{ position:absolute; left:-260px; top:-200px; width:1600px; height:2320px; transform-origin:0 0; padding:110px 120px; border-radius:20px;
  background:radial-gradient(ellipse at 40% 35%, #fbf7ec, {PAPER} 45%, #e9dfc8 100%); box-shadow:0 40px 120px rgba(23,38,43,.25), inset 0 0 120px rgba(168,132,44,.18); }}
#page::before {{ content:""; position:absolute; inset:40px; border:6px double rgba(168,132,44,.55); border-radius:12px; }}
#page::after {{ content:""; position:absolute; inset:62px; border:1.5px solid rgba(168,132,44,.35); border-radius:8px; }}
#txt {{ position:relative; font-family:AM; font-size:54px; line-height:2.05; direction:rtl; text-align:justify; color:rgba(23,38,43,.28); }}
.pw {{ border-radius:10px; padding:0 4px; }}
#grain {{ position:absolute; inset:-50px; opacity:.1; mix-blend-mode:multiply; pointer-events:none;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/></filter><rect width='300' height='300' filter='url(%23n)'/></svg>"); }}
#vig {{ position:absolute; inset:0; pointer-events:none; background:radial-gradient(ellipse at 50% 46%, rgba(241,236,224,0) 40%, rgba(241,236,224,.85) 100%); }}
#whip {{ position:absolute; top:0; bottom:0; left:340px; width:400px; opacity:0; background:linear-gradient(90deg, rgba(233,185,73,0), rgba(233,185,73,.45), rgba(233,185,73,0)); }}
#flash {{ position:absolute; inset:0; opacity:0; background:#fffaf0; }}
#hook {{ position:absolute; left:60px; right:60px; top:170px; text-align:center; }}
#hl {{ font-family:FR; font-size:80px; line-height:1.14; color:{INK}; }}
.hw {{ display:inline-block; opacity:0; }} .hw.five {{ opacity:1; color:{RED}; font-size:150px; letter-spacing:.07em; font-kerning:none; font-feature-settings:"kern" 0, "liga" 0; transform-origin:50% 50%;
  text-shadow:0 8px 0 #7a1d17, 0 14px 30px rgba(23,38,43,.35); }}
#bigcount {{ position:absolute; left:0; right:0; top:1150px; text-align:center; opacity:0; }}
#bigcount b {{ display:block; font-family:FR; font-size:190px; color:{GOLD}; text-shadow:0 6px 0 #7d621f, 0 16px 40px rgba(23,38,43,.25); }}
#bigcount small {{ font-family:FR; font-size:44px; letter-spacing:.12em; color:{INK}; opacity:.7; }}
.ring {{ position:absolute; left:440px; top:420px; width:200px; height:200px; border-radius:50%; border:10px solid {GOLD2}; opacity:0; }}
.spark {{ position:absolute; left:520px; top:510px; width:44px; height:8px; border-radius:4px; background:{GOLD2}; opacity:0; }}
.num {{ position:absolute; left:0; right:0; top:200px; text-align:center; font-family:FR; font-size:84px; color:{RED}; opacity:0; letter-spacing:.04em;
  text-shadow:0 6px 0 rgba(122,29,23,.35); }}
.card {{ position:absolute; left:110px; right:110px; top:340px; height:620px; border-radius:56px; text-align:center; opacity:0; perspective:900px;
  background:linear-gradient(170deg, rgba(255,253,247,.92), rgba(246,239,222,.9)); border:3px solid rgba(168,132,44,.5);
  box-shadow:0 50px 110px rgba(23,38,43,.28), inset 0 2px 0 #fff; backdrop-filter:blur(8px); }}
.card .big {{ font-family:AM; font-size:230px; line-height:1.3; margin-top:-6px; color:{INK}; text-shadow:0 10px 30px rgba(168,132,44,.35); }}
.card .mean {{ position:absolute; left:0; right:0; bottom:40px; font-family:FR; font-size:72px; color:{TEAL}; opacity:0; }}
.card .cnt {{ position:absolute; right:-40px; top:-50px; width:250px; height:250px; border-radius:50%; opacity:0; padding-top:50px;
  background:linear-gradient(160deg, #fbe3a1, {GOLD2} 55%, #b8891f); box-shadow:0 20px 50px rgba(23,38,43,.3), inset 0 3px 0 rgba(255,255,255,.6); }}
.card .cnt b {{ display:block; font-family:FR; font-size:74px; color:{INK}; }} .card .cnt small {{ font-family:FR; font-size:30px; color:{INK}; opacity:.75; letter-spacing:.1em; }}
.line {{ position:absolute; left:80px; right:80px; top:1010px; text-align:center; opacity:0; padding:30px 34px 28px; border-radius:40px;
  background:rgba(23,38,43,.9); box-shadow:0 30px 70px rgba(23,38,43,.35); }}
.line .ar {{ font-family:AM; font-size:76px; line-height:1.7; color:{CREAM}; direction:rtl; }}
.line .hl {{ color:{INK}; padding:0 10px; border-radius:14px; background-image:linear-gradient({GOLD2}, {GOLD2}); background-repeat:no-repeat; background-size:0% 100%; background-position:100% 0; }}
.line .src {{ font-family:IS; font-size:44px; color:rgba(241,236,224,.85); margin-top:4px; }}
#opts {{ position:absolute; left:0; right:0; top:1300px; display:flex; justify-content:center; gap:30px; }}
.opt {{ width:250px; padding:26px 0; border-radius:36px; text-align:center; font-family:FR; font-size:70px; color:{CREAM}; background:{TEAL}; opacity:0;
  box-shadow:0 20px 50px rgba(23,38,43,.3); }}
#ring3 {{ position:absolute; left:440px; top:1450px; width:200px; height:200px; opacity:0; }} #ring3 svg {{ position:absolute; inset:0; transform:rotate(-90deg); }}
#ring3 circle {{ fill:none; stroke-width:12; }} #ring3 .bg {{ stroke:rgba(23,38,43,.12); }} #ring3 .fg {{ stroke:{RED}; stroke-linecap:round; stroke-dasharray:339; }}
#rnum {{ position:absolute; inset:0; text-align:center; line-height:200px; font-family:FR; font-size:100px; color:{INK}; }}
#meter {{ position:absolute; left:90px; right:90px; top:1450px; padding:18px 26px 16px; border-radius:30px; background:rgba(246,241,228,.92); box-shadow:0 14px 40px rgba(23,38,43,.12); }}
#meter .lab {{ display:flex; justify-content:space-between; font-family:FR; font-size:36px; color:{INK}; }} #mpct {{ color:{RED}; font-size:52px; }}
#meter .bar {{ height:26px; border-radius:13px; background:rgba(23,38,43,.12); margin-top:12px; overflow:hidden; }}
#mfill {{ height:100%; width:0; border-radius:13px; background:linear-gradient(90deg, {GOLD}, {GOLD2}); box-shadow:0 0 20px rgba(233,185,73,.7); }}
#dots {{ display:flex; gap:16px; justify-content:center; margin-top:18px; }} #dots i {{ width:26px; height:26px; border-radius:50%; border:3px solid rgba(23,38,43,.3); }}
#endc {{ position:absolute; left:70px; right:70px; top:330px; text-align:center; opacity:0; }}
#endc .a {{ font-family:FR; font-size:96px; line-height:1.1; color:{INK}; }} #endc .a b {{ color:{RED}; }}
#endc .b {{ font-family:IS; font-size:64px; color:{TEAL}; margin-top:24px; }}
#endc .opts2 {{ display:flex; justify-content:center; gap:20px; margin-top:50px; }}
#endc .opts2 span {{ width:120px; height:120px; border-radius:30px; font-family:FR; font-size:70px; line-height:120px; color:{INK}; opacity:0;
  background:linear-gradient(160deg, #fbe3a1, {GOLD2}); box-shadow:0 14px 34px rgba(23,38,43,.3); }}
.cap {{ position:absolute; left:70px; right:70px; top:1660px; text-align:center; font-family:FR; font-size:62px; line-height:1.18; color:{INK}; opacity:0;
  text-shadow:0 0 18px {CREAM}, 0 0 8px {CREAM}; }}
.cw {{ display:inline-block; opacity:0; }} .cw.g {{ color:{RED}; }}
"""
    body = f"""
<div id="shake"><div id="world"><div id="page"><div id="txt">{pw}</div></div></div><div id="vig"></div>
<div id="hook"><div id="hl">{hl}</div></div>
<div id="bigcount"><b id="bcn">0</b><small>WORDS OF THE QUR'AN</small></div>
<div class="ring"></div><div class="ring"></div>{sparks}
{cards}
<div id="opts">{opts}</div>
<div id="ring3"><svg viewBox="0 0 200 200" width="200" height="200"><circle class="bg" cx="100" cy="100" r="54"/><circle class="fg" cx="100" cy="100" r="54"/></svg><div id="rnum">3</div></div>
<div id="meter"><div class="lab"><span>of every word in the Qur'an</span><b id="mpct">0.0%</b></div><div class="bar"><div id="mfill"></div></div><div id="dots">{dots}</div></div>
<div id="endc"><div class="a">5 tiny words.<br><b>7,736</b> times.</div><div class="b">How many did you already know?</div>
  <div class="opts2"><span>0</span><span>1</span><span>2</span><span>3</span><span>4</span><span>5</span></div></div>
{cap_html}
</div>
<div id="whip"></div><div id="flash"></div><div id="grain"></div>"""
    open(os.path.join(OUT, "index.html"), "w").write(f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" /><title>five</title>
<script src="assets/gsap.min.js"></script><style>{css}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{END}">
{body}
{chr(10).join(au)}
</div><script>
const tl = gsap.timeline({{ paused: true }});
const CAM = {{x:540, y:960, s:1.0, r:0}}, pg = document.getElementById("page");
function camSet() {{ pg.style.transform = `translate(${{540 + 260 - (CAM.x + 260) * CAM.s}}px, ${{960 + 200 - (CAM.y + 200) * CAM.s}}px) scale(${{CAM.s}}) rotate(${{CAM.r}}deg)`; }}
camSet();
{chr(10).join(js)}
window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;</script></body></html>
""")
    print("built", END, "s,", len(au), "sounds;", L)

if __name__ == "__main__":
    build()
