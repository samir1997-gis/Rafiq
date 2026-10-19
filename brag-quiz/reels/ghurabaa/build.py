#!/usr/bin/env python3
"""The strangers video (owner, 19 Oct 2026; #269): the carousel as one big page the camera travels over (MOTION-STYLE.md, the moves of
reels/quran-count/build2.py), with the hook standard of FORMATS.md (Callum, the shouted word slammed with crash, shake, rings, flash).
Hook ISLAM IS SO STRANGE! → the hadith (Sahih Muslim 145) built word by word as Rafiq recites it → the camera zooms into لِلْغُرَباءِ while
the rest flies off → غُرَباء, one stranger غَرِيب → it breaks into its letters, the ي drops out: the root غ ر ب → down the page, the sun
sets: "to go away" → a whip to the family (الْمَغْرِب, غَرْب, غُرْبَة) → down: a stranger is far from home, Bukhari 6416 → the comment ask.
Voice: brag-quiz/voice/ghurabaa/*.mp3 (lines in brag-quiz/voice/ghurabaa-lines.json). English word timings from faster-whisper;
the Arabic words are spread over their line by length (whisper's Arabic timings drift).

  python3 brag-quiz/reels/ghurabaa/build.py        then  cd brag-quiz/reels/ghurabaa/out/v && npx hyperframes render -o ../ghurabaa.mp4
"""
import json, os, re, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
V6 = os.path.join(ROOT, "brag-output-v6/composition/assets"); GSAP = os.path.join(V6, "lib/gsap.min.js")
VOICE = os.path.join(ROOT, "brag-quiz/voice/ghurabaa"); HOOK = os.environ.get("HOOK", "ha")
INK, TEAL, GOLD, GOLD2, CREAM, RED = "#17262b", "#2e7263", "#a8842c", "#E9B949", "#f1ece0", "#b4322a"
dur = lambda p: float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).decode())
ORDER = [HOOK, "c1", "r1", "c2", "c3", "r2", "c4", "r3", "c5", "r4", "c6", "c7", "r5", "c8", "r6", "c9", "r7", "c10", "r8", "c11", "c12"]
GAP = {"c1": .2, "r1": .35, "c2": .3, "c3": .35, "r2": .15, "c4": .25, "r3": .1, "c5": .3, "r4": .15, "c6": .3, "c7": .35, "r5": .1, "c8": .35,
       "r6": .1, "c9": .35, "r7": .1, "c10": .45, "r8": .2, "c11": .25, "c12": .5}

def timings():
    cache = os.path.join(HERE, "out", "timings.json")
    T = json.load(open(cache)) if os.path.exists(cache) else {}
    todo = [f for f in ORDER if f not in T and not f.startswith("r")]
    if todo:
        from faster_whisper import WhisperModel
        m = WhisperModel("small", device="cpu", compute_type="int8")
        for f in todo:
            segs, _ = m.transcribe(os.path.join(VOICE, f + ".mp3"), word_timestamps=True, language="en")
            T[f] = [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]
        os.makedirs(os.path.dirname(cache), exist_ok=True); json.dump(T, open(cache, "w"), indent=1)
    return T

def build():
    T = timings(); out = os.path.join(HERE, "out", "v"); a = os.path.join(out, "assets")
    if os.path.exists(out): shutil.rmtree(out)
    os.makedirs(a)
    for f in ("ibm-plex-sans-arabic-arabic-700-normal.woff2", "karla-latin-500-normal.woff2", "karla-latin-700-normal.woff2"): shutil.copy(os.path.join(V6, "fonts", f), a)
    for f in ("instrument-serif-latin-400-normal.woff2", "fredoka-latin-700-normal.woff2"): shutil.copy(os.path.join(ROOT, "brag-quiz/fonts", f), a)
    shutil.copy(GSAP, a)
    for f in ("swoosh.wav", "short-swoosh.wav", "swoosh-low.wav", "tap.wav", "click.wav", "shutter.wav"): shutil.copy(os.path.join(ROOT, "brag-quiz/sfx/ref", f), a)
    shutil.copy(os.path.join(ROOT, "brag-quiz/sfx/crash.wav"), a); shutil.copy(os.path.join(ROOT, "brag-quiz/sfx/owner/n03.wav"), a)

    # the voice: every line levelled to the same loudness (Rafiq level with Callum), one after another
    at, D, t = {}, {}, 0.05
    for f in ORDER:
        t += GAP.get(f, 0); at[f] = round(t, 2)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(VOICE, f + ".mp3"), "-af", "loudnorm=I=-17:TP=-2:LRA=11", "-ar", "48000", os.path.join(a, f + ".wav")], check=True)
        D[f] = dur(os.path.join(a, f + ".wav")); t += D[f]
    END = round(t + 1.6, 2)
    def w(line, word, k=0, edge=0):
        hits = [x for x in T[line] if re.sub(r"[^\w]", "", x[0].lower()) == word.lower()]
        return round(at[line] + (hits[k][1 + edge] if len(hits) > k else 0), 2)
    def wi(line, i): x = T[line][min(i, len(T[line]) - 1)]; return round(at[line] + x[1], 2)
    lend = lambda f: round(at[f] + D[f], 2)
    def spread(line, words):                                    # Arabic: each word's start, by its length, over the line
        L = [len(re.sub(r"[ً-ْٰ،]", "", x)) + 1 for x in words]; s, o = sum(L), []
        span = D[line] - 0.25; acc = 0.1
        for x in L: o.append(round(at[line] + acc, 2)); acc += span * x / s
        return o

    au = [f'<audio id="{f}" src="assets/{f}.wav" data-start="{at[f]:.2f}" data-duration="{D[f]:.2f}" data-volume="1" data-track-index="{1 + i % 2}"></audio>' for i, f in enumerate(ORDER)]
    src = os.path.join(V6, "sfx-gen/fountain.mp3")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-i", src, "-filter_complex",   # looped: one copy is shorter than this video
                    f"[0]volume=6dB,atrim=0:{END + 0.5:.2f},afade=t=in:d=0.3,afade=t=out:st={END - 1.4:.2f}:d=1.4",
                    "-c:a", "libmp3lame", "-q:a", "3", os.path.join(a, "fountain.mp3")], check=True)
    au.append(f'<audio id="bed" src="assets/fountain.mp3" data-start="0" data-duration="{END:.2f}" data-volume="0.1" data-track-index="8"></audio>')
    sfx = []
    def fx(name, t0, vol=0.35, d=0.7): sfx.append(f'<audio id="fx{len(sfx)}" src="assets/{name}" data-start="{max(0, t0):.2f}" data-duration="{d}" data-volume="{vol}" data-track-index="{10 + len(sfx) % 5}"></audio>')

    js = []
    # the page: the scene centres on one tall page; the camera puts a page point at the screen's centre, at a scale
    PG = {"hook": (540, 960), "had": (540, 2880), "word": (540, 4800), "sun": (540, 6720), "fam": (1620, 6720), "end": (540, 8640)}
    def cam(scene, t0, d=0.8, s=1, ease="expo.inOut", snd="swoosh-low.wav"):
        x, y = PG[scene] if isinstance(scene, str) else scene
        js.append(f'tl.to("#world", {{x:{540 - x * s}, y:{960 - y * s}, scale:{s}, duration:{d}, ease:"{ease}"}}, {t0:.2f});')
        js.append(f'tl.fromTo(BL, {{v:0}}, {{v:1, duration:{d / 2}, ease:"power2.in", yoyo:true, repeat:1, onUpdate:blurUpd}}, {t0:.2f});')
        if snd: fx(snd, t0 + 0.05, 0.45)
    def pop(sel, t0, fromv="{opacity:0, scale:0.6, y:30}", d=0.45, ease="back.out(2)", click=False):
        js.append(f'tl.fromTo("{sel}", {fromv}, {{opacity:1, scale:1, y:0, x:0, rotation:0, filter:"blur(0px)", duration:{d}, ease:"{ease}"}}, {t0:.2f});')
        if click: fx("click.wav", t0, 0.25, 0.3)
    def zoomin(sel, t0): pop(sel, t0, '{opacity:0, scale:2.4, filter:"blur(22px)"}', 0.5, "expo.out")
    def swoop(sel, t0, side):                                   # in from the side, blurred, as each word is said
        pop(sel, t0, f'{{opacity:0, x:{side * 420}, scale:1.25, filter:"blur(14px)"}}', 0.36, "expo.out")
    def off(sel, t0, y=-420, x=0, d=0.45, snd=True):          # flies off the page
        js.append(f'tl.to("{sel}", {{y:{y}, x:{x}, opacity:0, filter:"blur(14px)", duration:{d}, ease:"power3.in", stagger:0.035}}, {t0:.2f});')
        if snd: fx("short-swoosh.wav", t0 + 0.1, 0.3)
    def glow(sel, t0, col):
        js.append(f'tl.to("{sel}", {{color:"{col}", textShadow:"0 0 34px {col}66", duration:0.25}}, {t0:.2f});')
        js.append(f'tl.fromTo("{sel}", {{scale:1}}, {{scale:1.14, duration:0.16, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}}, {t0:.2f});')
    def words_in(prefix, line, words, sides=True):              # an English line, word by word
        for i in range(len(words)): swoop(f"#{prefix}{i}", wi(line, i) - 0.06, -1 if i % 2 else 1)
    span = lambda prefix, words, cls="ew": " ".join(f'<span class="{cls}" id="{prefix}{i}">{x}</span>' for i, x in enumerate(words))

    # 1 · the hook (frame 0, the cover): Fredoka, STRANGE! huge, slams down on the voice; faint غَرِيب drifting behind
    H = T[HOOK]; hs = [x for x in H if "strange" in x[0].lower()]
    hit = round(at[HOOK] + (hs[0][1] if hs else 0.9) + 0.08, 2)
    hw = ["Islam", "is", "so"]
    for i in range(1, 3): swoop(f"#hk{i}", wi(HOOK, i) - 0.06, -1 if i % 2 else 1)
    fxr = '<i class="hring"></i><i class="hring r2"></i>' + "".join(f'<i class="hspark" style="transform:rotate({k}deg)"></i>' for k in range(0, 360, 36))
    js.append(f'tl.fromTo("#loud", {{scale:1.15, rotation:-5, x:20}}, {{scale:1, rotation:0, x:0, duration:{hit:.2f}, ease:"power4.in"}}, 0);')
    js.append(f'tl.to("#loud", {{keyframes:[{{scaleX:1.18, scaleY:0.78, duration:0.06}}, {{scaleX:0.94, scaleY:1.08, duration:0.08}}, {{scaleX:1, scaleY:1, duration:0.12}}]}}, {hit:.2f});')
    js.append(f'tl.fromTo("#loud .hring", {{scale:0.3, opacity:0.9}}, {{scale:3.4, opacity:0, duration:0.55, ease:"expo.out", stagger:0.07, immediateRender:false}}, {hit:.2f});')
    js.append(f'tl.fromTo("#loud .hspark", {{opacity:1, scaleX:0.2, x:60}}, {{opacity:0, scaleX:1.4, x:280, duration:0.4, ease:"expo.out", immediateRender:false}}, {hit:.2f});')
    js.append(f'tl.fromTo("#flash", {{opacity:0.85}}, {{opacity:0, duration:0.3, ease:"power2.out", immediateRender:false}}, {hit:.2f});')
    js.append(f'tl.to("#shake", {{keyframes:[{{x:-34, y:22, rotation:-1.4, duration:0.035}}, {{x:30, y:-18, rotation:1.2, duration:0.035}}, {{x:-22, y:14, rotation:-0.8, duration:0.04}}, '
              f'{{x:16, y:-10, rotation:0.6, duration:0.04}}, {{x:-8, y:6, rotation:-0.3, duration:0.05}}, {{x:0, y:0, rotation:0, duration:0.06}}]}}, {hit:.2f});')
    fx("crash.wav", hit - 0.02, 0.9, 1.5)
    js.append(f'tl.fromTo("#hookline", {{scale:1}}, {{scale:1.06, duration:{lend("c1"):.2f}, ease:"none"}}, 0);')
    js.append(f'tl.fromTo(".ghost", {{y:0}}, {{y:-160, duration:{lend("c1") + 0.5:.2f}, ease:"none", stagger:0.2}}, 0);')
    c1w = ["…and", "the", "Prophet", "(pbuh)", "told", "us", "it", "would", "be."]
    c1t = [wi("c1", 0), wi("c1", 1), wi("c1", 2), w("c1", "peace"), w("c1", "told"), w("c1", "us"), w("c1", "it"), w("c1", "would"), w("c1", "be")]
    for i, t0 in enumerate(c1t): swoop(f"#p{i}", t0 - 0.06, -1 if i % 2 else 1)
    # 2 · down the page: the hadith, word by word as Rafiq says it; the English builds under it with Callum
    off("#hookwrap", lend("c1") + 0.05, -700)
    cam("had", lend("c1") + 0.1)
    HA = ["بَدَأَ", "الإِسْلامُ", "غَرِيبًا،", "وَسَيَعُودُ", "كَما", "بَدَأَ", "غَرِيبًا،", "فَطُوبى", "لِلْغُرَباءِ"]
    for i, t0 in enumerate(spread("r1", HA)): zoomin(f"#a{i}", t0 - 0.05)
    for i in (2, 6, 8): glow(f"#a{i}", spread("r1", HA)[i] + 0.2, RED)
    EN = "Islam began as something strange, and it will return to being strange as it began, so glad tidings to the strangers.".split()
    words_in("e", "c2", EN); pop("#ref1", lend("c2") - 0.3, click=True)
    # 3 · "let's zoom in on that last word": everything else flies off, the camera dives into لِلْغُرَباءِ
    z0 = w("c3", "zoom") - 0.1
    off("#hadAr .aw:not(#a8)", z0, -500); off("#hadEn .ew, #ref1", z0 + 0.05, 500, snd=False)
    js.append(f'tl.to(CAMZ, {{p:1, duration:0.9, ease:"expo.inOut", onUpdate:zoomUpd}}, {z0 + 0.25:.2f});'); fx("swoosh.wav", z0 + 0.3, 0.5)
    js.append(f'tl.fromTo("#zflash", {{opacity:0}}, {{opacity:1, duration:0.25, ease:"power2.in"}}, {z0 + 0.9:.2f});')
    js.append(f'tl.set("#world", {{x:{540 - PG["word"][0]}, y:{960 - PG["word"][1]}, scale:1}}, {z0 + 1.15:.2f});')
    js.append(f'tl.to("#zflash", {{opacity:0, duration:0.35, ease:"power2.out"}}, {z0 + 1.15:.2f});')
    # 4 · غُرَباء = strangers; one stranger غَرِيب
    zoomin("#big", z0 + 1.1); fx("tap.wav", z0 + 1.2, 0.4, 0.3)
    pop("#tr2", at["r2"] + 0.3, "{opacity:0, y:20}")
    swoop("#strangers", w("c4", "strangers") - 0.08, 1); glow("#strangers", w("c4", "strangers") + 0.1, TEAL)
    pop("#one", w("c4", "one") - 0.05, "{opacity:0, y:40}", 0.4, "expo.out")
    zoomin("#g1", at["r3"] - 0.1); fx("tap.wav", at["r3"], 0.4, 0.3)
    # 5 · break it down: the big word leaves, غَرِيب moves up, splits into letters, the ي drops off, غ ر ب turn red
    off("#big, #tr2, #strangers, #oneLab", at["c5"] - 0.1, -600)
    js.append(f'tl.to("#gw", {{y:-560, scale:1.3, duration:0.6, ease:"expo.inOut"}}, {at["c5"]:.2f});')
    sp = w("c5", "root") - 0.1
    js.append(f'tl.to("#g1", {{opacity:0, duration:0.12}}, {sp:.2f}); tl.set("#letters", {{opacity:1}}, {sp:.2f});')
    js.append(f'tl.fromTo("#letters .lt", {{x:(i) => [-225, -75, 75, 225][i]}}, {{x:0, duration:0.55, ease:"back.out(1.6)"}}, {sp:.2f});'); fx("short-swoosh.wav", sp, 0.4)
    js.append(f'tl.to("#lY", {{y:520, rotation:40, opacity:0, duration:0.7, ease:"power2.in"}}, {w("c5", "three") - 0.1:.2f});'); fx("swoosh-low.wav", w("c5", "three"), 0.35)
    js.append(f'tl.to("#letters .lt", {{x:(i) => [-35, -75, 0, 35][i], duration:0.45, ease:"expo.out"}}, {w("c5", "three") + 0.35:.2f});')
    for k, t0 in enumerate(spread("r4", ["غَيْن،", "راء،", "باء"])):
        glow(["#lG", "#lR", "#lB"][k], t0, RED); fx("click.wav", t0, 0.3, 0.3)
    pop("#rootLab", at["r4"], "{opacity:0, y:20}")
    # 6 · down the page with the root: the sun sets behind the horizon, "to go away"
    cam("sun", at["c6"] - 0.15)
    js.append(f'tl.fromTo("#sunball", {{y:-380}}, {{y:330, duration:{D["c6"] + 0.6:.2f}, ease:"power1.in"}}, {at["c6"]:.2f});')
    js.append(f'tl.fromTo("#sky", {{opacity:0.25}}, {{opacity:1, duration:{D["c6"]:.2f}, ease:"none"}}, {at["c6"]:.2f});')
    swoop("#go", w("c6", "go") - 0.1, -1); glow("#go", w("c6", "away"), GOLD)
    pop("#sets", w("c6", "sun") - 0.1, "{opacity:0, y:30}", 0.4, "expo.out")
    # 7 · a whip to the family: each word card swings in from alternate sides as it's said
    cam("fam", at["c7"] - 0.25, 0.6, snd="swoosh.wav")
    pop("#famLab", at["c7"], "{opacity:0, y:-20}")
    for k, (r, wd) in enumerate((("r5", "maghrib"), ("r6", "gharb"), ("r7", "ghurba"))):
        c = ("c7", "c8", "c9")[k]; t0 = w(c, wd) - 0.15 if w(c, wd) > at[c] else at[c] + 0.3
        pop(f"#f{k}", t0, f'{{opacity:0, x:{-600 if k % 2 == 0 else 600}, rotation:{-6 if k % 2 == 0 else 6}, filter:"blur(12px)"}}', 0.5, "expo.out"); fx("swoosh.wav", t0, 0.3)
        glow(f"#f{k} .ar", at[r] + 0.05, RED); fx("tap.wav", at[r] + 0.05, 0.35, 0.3)
    # 8 · down: a stranger is someone far from home; Bukhari 6416; the comment ask
    off("#fam .card, #famLab", at["c10"] - 0.2, 0, 900)
    cam("end", at["c10"] - 0.05)
    swoop("#far", w("c10", "far") - 0.1, 1); glow("#far", w("c10", "home"), GOLD)
    off("#farWrap", w("c10", "said") - 0.25, -360, snd=True)
    pop("#bkLab", w("c10", "said") - 0.05, "{opacity:0, y:-20}")
    BK = ["كُنْ", "فِي", "الدُّنْيا", "كَأَنَّكَ", "غَرِيبٌ", "أَوْ", "عابِرُ", "سَبِيلٍ"]
    for i, t0 in enumerate(spread("r8", BK)): zoomin(f"#b{i}", t0 - 0.05)
    glow("#b4", spread("r8", BK)[4] + 0.2, RED)
    EN2 = "Be in this world as if you were a stranger, or a traveller.".split()
    words_in("k", "c11", EN2); pop("#ref2", lend("c11") - 0.3, click=True)
    off("#bukh .aw, #bukh .ew, #ref2", at["c12"] - 0.35, -500)
    zoomin("#ask", at["c12"] - 0.05); glow("#ask .acc", w("c12", "strangers"), GOLD2); fx("n03.wav", w("c12", "strangers"), 0.5, 1.5)
    js.append(f'tl.fromTo("#arrow", {{y:-20}}, {{y:20, duration:0.4, yoyo:true, repeat:{int((END - w("c12", "comment")) / 0.4)}, ease:"sine.inOut"}}, {w("c12", "comment"):.2f});')
    pop("#arrow", w("c12", "comment") - 0.1); pop("#send", lend("c12") + 0.1, "{opacity:0, y:30}", 0.4, "expo.out", True)
    js.append(f'tl.fromTo(".orb", {{rotation:0}}, {{rotation:50, duration:{END:.2f}, ease:"none"}}, 0);')

    ghost = "".join(f'<div class="ghost" style="left:{x}px;top:{y}px;font-size:{s}px;opacity:{o}">غَرِيب</div>'
                    for x, y, s, o in ((60, 220, 120, .07), (700, 360, 90, .06), (120, 1350, 150, .06), (640, 1560, 110, .07), (380, 1700, 80, .05)))
    body = f"""
<div id="shake"><div id="world">
 <section style="left:0;top:0"><div id="hookwrap">{ghost}
   <div id="hookline"><span class="hk" id="hk0">Islam</span> <span class="hk" id="hk1">is</span> <span class="hk" id="hk2">so</span><br><span id="loud">STRANGE!{fxr}</span></div>
   <div id="pline">{span("p", c1w, "pw")}</div></div></section>
 <section style="left:0;top:1920px"><div class="lab">THE PROPHET (PBUH) SAID</div>
   <div id="hadAr">{" ".join(f'<span class="aw" id="a{i}">{x}</span>' for i, x in enumerate(HA))}</div>
   <div id="hadEn">{span("e", EN)}</div><div class="ref" id="ref1">SAHIH MUSLIM 145</div></section>
 <section style="left:0;top:3840px"><div class="lab">THE WORD</div>
   <div id="big">غُرَباء</div><div class="tr" id="tr2">ghurabāʾ</div><div id="strangers">strangers</div>
   <div id="gw"><div id="oneLab"><span id="one">just one stranger</span></div><div id="g1">غَرِيب</div>
     <div id="letters"><span class="lt" id="lG">غ</span><span class="lt" id="lR">ر</span><span class="lt" id="lY">ي</span><span class="lt" id="lB">ب</span></div>
     <div id="rootLab">THE ROOT</div></div></section>
 <section style="left:0;top:5760px"><div id="sky"></div><div id="sunball"></div><div id="horizon"></div>
   <div id="rootTop">غ ر ب</div><div id="go">to go away</div><div id="sets">like the sun when it sets</div></section>
 <section style="left:1080px;top:5760px" id="fam"><div class="lab" id="famLab">THE SAME ROOT</div>
   <div class="card" id="f0"><span class="ar">الْمَغْرِب</span><span class="en">Maghrib<small>the sunset prayer</small></span></div>
   <div class="card" id="f1"><span class="ar">غَرْب</span><span class="en">gharb<small>the west</small></span></div>
   <div class="card" id="f2"><span class="ar">غُرْبَة</span><span class="en">ghurba<small>being far from home</small></span></div></section>
 <section style="left:0;top:7680px"><div id="farWrap"><div id="farBig">a stranger is someone</div><div id="far">far from home</div></div>
   <div id="bukh"><div class="lab" id="bkLab" style="top:420px;opacity:0">AND HE (PBUH) SAID</div>
     <div id="bkAr">{" ".join(f'<span class="aw" id="b{i}">{x}</span>' for i, x in enumerate(BK))}</div>
     <div id="bkEn">{span("k", EN2)}</div><div class="ref" id="ref2" style="top:1240px">SAHIH AL-BUKHARI 6416</div></div>
   <div id="ask">Are you one of<br>the <span class="acc">strangers?</span></div><div id="arrow">👇</div>
   <div id="send">Comment below · send this to someone who feels like a stranger 🤍</div></section>
</div></div>
<div class="orb" id="orbA"></div><div class="orb" id="orbB"></div><div id="flash"></div><div id="zflash"></div>"""
    css = f"""
@font-face {{ font-family:"Ar"; src:url("assets/ibm-plex-sans-arabic-arabic-700-normal.woff2"); font-weight:700; }}
@font-face {{ font-family:"Karla"; src:url("assets/karla-latin-500-normal.woff2"); font-weight:500; }}
@font-face {{ font-family:"Karla"; src:url("assets/karla-latin-700-normal.woff2"); font-weight:700; }}
@font-face {{ font-family:"InstrumentSerif"; src:url("assets/instrument-serif-latin-400-normal.woff2"); }}
@font-face {{ font-family:"Fredoka"; src:url("assets/fredoka-latin-700-normal.woff2"); font-weight:700; }}
body {{ margin:0; background:#000; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; background:{CREAM}; color:{INK}; font-family:"Karla";
  background-image:radial-gradient(circle at 50% 0%, rgba(168,132,44,.16) 0%, rgba(241,236,224,0) 55%); }}
#shake {{ position:absolute; inset:0; }}
#world {{ position:absolute; left:0; top:0; width:2160px; height:9600px; transform-origin:0 0; }}
section {{ position:absolute; width:1080px; height:1920px; }}
.lab {{ position:absolute; left:0; right:0; top:330px; text-align:center; font-family:"Karla"; font-weight:700; font-size:34px; letter-spacing:.22em; color:#5c6e70; }}
.arS {{ font-family:"Ar"; letter-spacing:0; }}
#hookwrap {{ position:absolute; inset:0; }}
.ghost {{ position:absolute; font-family:"Ar"; font-weight:700; color:{TEAL}; }}
#hookline {{ position:absolute; left:40px; right:40px; top:560px; text-align:center; font-family:"Fredoka"; font-weight:700; font-size:150px; line-height:1.0; letter-spacing:-.01em; }}
.hk {{ display:inline-block; }} #hk1, #hk2 {{ opacity:0; }}
#loud {{ position:relative; display:inline-block; font-size:168px; color:{RED}; margin-top:10px; }}
.hring {{ position:absolute; left:50%; top:50%; width:300px; height:300px; margin:-150px; border-radius:50%; border:14px solid {GOLD2}; opacity:0; }}
.hring.r2 {{ border-color:{RED}; border-width:8px; }}
.hspark {{ position:absolute; left:50%; top:50%; width:110px; height:12px; margin-top:-6px; border-radius:6px; background:{GOLD2}; transform-origin:0 50%; opacity:0; }}
#pline {{ position:absolute; left:90px; right:90px; top:1130px; text-align:center; font-family:"InstrumentSerif"; font-style:italic; font-size:68px; line-height:1.15; }}
.pw, .ew {{ display:inline-block; opacity:0; }} #p3 {{ font-size:.7em; }}
#hadAr {{ position:absolute; left:60px; right:60px; top:470px; text-align:center; direction:rtl; font-family:"Ar"; font-weight:700; font-size:92px; line-height:1.75; }}
.aw {{ display:inline-block; opacity:0; }}
#hadEn {{ position:absolute; left:90px; right:90px; top:1080px; text-align:center; font-family:"InstrumentSerif"; font-style:italic; font-size:60px; line-height:1.2; }}
.ref {{ position:absolute; left:0; right:0; top:1500px; text-align:center; font-weight:700; font-size:34px; letter-spacing:.16em; color:{TEAL}; opacity:0; }}
#big {{ position:absolute; left:0; right:0; top:520px; text-align:center; font-family:"Ar"; font-weight:700; font-size:330px; line-height:1.3; color:{RED}; opacity:0; }}
.tr {{ position:absolute; left:0; right:0; text-align:center; font-family:"Karla"; font-weight:500; font-size:40px; letter-spacing:.08em; color:#5c6e70; opacity:0; }}
#tr2 {{ top:1000px; }}
#strangers {{ position:absolute; left:0; right:0; top:1060px; text-align:center; font-family:"InstrumentSerif"; font-size:170px; line-height:1; letter-spacing:-.02em; opacity:0; }}
#gw {{ position:absolute; left:0; right:0; top:1300px; height:600px; }}
#oneLab {{ position:absolute; left:0; right:0; top:0; text-align:center; font-family:"InstrumentSerif"; font-style:italic; font-size:56px; color:#5c6e70; }} #one {{ display:inline-block; opacity:0; }}
#g1, #letters {{ position:absolute; left:0; right:0; top:90px; text-align:center; font-family:"Ar"; font-weight:700; font-size:180px; line-height:1.3; }}
#g1 {{ opacity:0; }} #letters {{ opacity:0; display:flex; justify-content:center; direction:rtl; }}
.lt {{ display:inline-block; width:150px; text-align:center; color:{INK}; }}
#rootLab {{ position:absolute; left:0; right:0; top:420px; text-align:center; font-weight:700; font-size:34px; letter-spacing:.22em; color:{RED}; opacity:0; }}
#sky {{ position:absolute; left:0; right:0; top:0; height:1240px; background:linear-gradient(#f6d7a8, #e9a86a 70%, #c8603b); opacity:.25; }}
#sunball {{ position:absolute; left:390px; top:820px; width:300px; height:300px; border-radius:50%; background:radial-gradient(circle, #ffe9a6, {GOLD2} 60%, #e07b39); box-shadow:0 0 120px 40px rgba(233,185,73,.5); }}
#horizon {{ position:absolute; left:0; right:0; top:1240px; height:680px; background:{CREAM}; border-top:6px solid {INK}; }}
#rootTop {{ position:absolute; left:0; right:0; top:260px; text-align:center; font-family:"Ar"; font-weight:700; font-size:170px; color:{RED}; letter-spacing:.14em; direction:rtl; }}
#go {{ position:absolute; left:0; right:0; top:1330px; text-align:center; font-family:"InstrumentSerif"; font-size:170px; line-height:1; letter-spacing:-.02em; opacity:0; }}
#sets {{ position:absolute; left:0; right:0; top:1540px; text-align:center; font-family:"InstrumentSerif"; font-style:italic; font-size:62px; color:#5c6e70; opacity:0; }}
.card {{ position:absolute; left:90px; right:90px; height:300px; border-radius:40px; background:#fff8ec; box-shadow:0 30px 60px -30px rgba(23,38,43,.45);
  display:flex; align-items:center; justify-content:space-between; padding:0 60px; opacity:0; }}
#f0 {{ top:520px; }} #f1 {{ top:880px; }} #f2 {{ top:1240px; }}
.card .ar {{ font-family:"Ar"; font-weight:700; font-size:120px; line-height:1.4; direction:rtl; display:inline-block; }}
.card .en {{ font-family:"InstrumentSerif"; font-size:76px; line-height:1; text-align:left; }} .card small {{ display:block; font-style:italic; font-size:44px; color:#5c6e70; margin-top:12px; }}
#famLab {{ opacity:0; }}
#farWrap {{ position:absolute; left:0; right:0; top:700px; text-align:center; }}
#farBig {{ font-family:"InstrumentSerif"; font-style:italic; font-size:72px; color:#5c6e70; }}
#far {{ display:inline-block; font-family:"InstrumentSerif"; font-size:170px; line-height:1.05; letter-spacing:-.02em; opacity:0; }}
#bkAr {{ position:absolute; left:60px; right:60px; top:560px; text-align:center; direction:rtl; font-family:"Ar"; font-weight:700; font-size:92px; line-height:1.75; }}
#bkEn {{ position:absolute; left:100px; right:100px; top:900px; text-align:center; font-family:"InstrumentSerif"; font-style:italic; font-size:66px; line-height:1.2; }}
#ask {{ position:absolute; left:40px; right:40px; top:520px; text-align:center; font-family:"Fredoka"; font-weight:700; font-size:130px; line-height:1.05; opacity:0; }}
#ask .acc {{ color:{RED}; display:inline-block; }}
#arrow {{ position:absolute; left:0; right:0; top:900px; text-align:center; font-size:150px; opacity:0; }}
#send {{ position:absolute; left:110px; right:110px; top:1130px; text-align:center; font-weight:700; font-size:44px; line-height:1.3; border:4px solid {INK}; border-radius:60px; padding:26px 30px; opacity:0; }}
.orb {{ position:absolute; width:520px; height:520px; border-radius:50%; border:70px solid rgba(46,114,99,.06); pointer-events:none; }}
#orbA {{ left:-260px; top:-200px; }} #orbB {{ right:-240px; bottom:-220px; border-color:rgba(168,132,44,.07); }}
#flash {{ position:absolute; inset:0; background:#fff8e6; opacity:0; pointer-events:none; }}
#zflash {{ position:absolute; inset:0; background:{CREAM}; opacity:0; pointer-events:none; }}
"""
    script = f"""
const BL = {{v:0}};
function blurUpd() {{ document.getElementById("world").style.filter = `blur(${{(this.targets()[0].v * 10).toFixed(1)}}px)`; }}
// the dive into لِلْغُرَباءِ: from the hadith page to the word, scale 1 → 4.5, measured once on load
const CAMZ = {{p:0}}; let ZP = null;
function zoomUpd() {{
  if (!ZP) {{ const W = document.getElementById("world"), r = document.getElementById("a8"), wr = W.getBoundingClientRect(), s = W.getBoundingClientRect().width / 2160;
    const rr = r.getBoundingClientRect(); ZP = {{x:(rr.left + rr.width / 2 - wr.left) / s, y:(rr.top + rr.height / 2 - wr.top) / s}}; }}
  const p = CAMZ.p, s = 1 + 3.5 * p, cx = {PG["had"][0]} + (ZP.x - {PG["had"][0]}) * p, cy = {PG["had"][1]} + (ZP.y - {PG["had"][1]}) * p;
  gsap.set("#world", {{x:540 - cx * s, y:960 - cy * s, scale:s}});
  document.getElementById("world").style.filter = `blur(${{(Math.sin(p * Math.PI) * 6).toFixed(1)}}px)`;
}}
"""
    open(os.path.join(out, "index.html"), "w").write(f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" /><title>ghurabaa</title>
<script src="assets/gsap.min.js"></script><style>{css}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{END:.2f}">
{body}
{chr(10).join(au + sfx)}
</div><script>{script}
const tl = gsap.timeline({{ paused: true }});
gsap.set("#world", {{x:0, y:0, scale:1}});
{chr(10).join(js)}
window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;</script></body></html>
""")
    json.dump({"at": at, "dur": D, "end": END}, open(os.path.join(HERE, "out", "plan.json"), "w"), indent=1)
    print(f"ghurabaa: {END:.1f}s · " + ", ".join(f"{k} {v:.2f}" for k, v in at.items()))

if __name__ == "__main__":
    build()
