#!/usr/bin/env python3
"""q1-quran-count v2 (owner, 12 Oct 2026): the same numbers as build.py, in Rafiq's colours, with a voiceover and the motion
style of the owner's reference reel: everything lands on the word that's said. One tall page the camera scrolls down
(the page moves up), sideways whips with motion blur between beats, words that blur-zoom in, keywords in teal or gold
with a soft glow, a gold underline that draws itself, counters that pop, filled and outlined pills that stack, a hand-drawn
circle round the key phrase, a highlighter sweep, a typewriter line that whips to the answer. The 6,236 verses are dots
filling an eight-pointed star (the ۞ printed in the Quran), growing from the centre in the Quran's order.

Voice: brag-quiz/voice/quran-count/v1..v11.mp3 (ElevenLabs, Rafiq voice; lines in brag-quiz/voice/quran-count-lines.json).
Word timings come from the audio itself (faster-whisper), cached in out/timings.json.

  python3 brag-quiz/reels/quran-count/build2.py      then in brag-quiz/reels/quran-count/out/q1-quran-count-v2:
  npx hyperframes render -o ../q1-quran-count-v2.mp4  and level it to -16 LUFS (loudnorm)
"""
import json, math, os, re, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import count, TEN, V6, GSAP, HERE, ROOT          # the same counts and top-10 words as v1

ID = "q1-quran-count-v2"
VOICE = os.path.join(ROOT, "brag-quiz/voice/quran-count")
LINES = json.load(open(os.path.join(ROOT, "brag-quiz/voice/quran-count-lines.json")))
GAP = {"v2": 0.35, "v3": 0.55, "v4": 0.3, "v5": 0.25, "v6": 0.45, "v7": 0.05, "v8": 0.6, "v9": 0.4, "v10": 0.5, "v11": 0.5}
INK, TEAL, GOLD, GOLD2, CREAM, RED = "#17262b", "#2e7263", "#a8842c", "#E9B949", "#f1ece0", "#b4322a"
dur = lambda p: float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).decode())

def timings():
    """Each line's words with their start/end inside the line, from faster-whisper; cached."""
    cache = os.path.join(HERE, "out", "timings.json")
    if os.path.exists(cache): return json.load(open(cache))
    from faster_whisper import WhisperModel
    m = WhisperModel("small", device="cpu", compute_type="int8"); out = {}
    for ln in LINES:
        segs, _ = m.transcribe(os.path.join(VOICE, ln["file"] + ".mp3"), word_timestamps=True, language="en")
        out[ln["file"]] = [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]
    os.makedirs(os.path.dirname(cache), exist_ok=True); json.dump(out, open(cache, "w"), indent=1)
    return out

def star_points(n):
    """n points, centre outwards (phyllotaxis), inside an eight-pointed star: two squares, one turned 45 degrees."""
    S = 300.0                                                   # half-side of each square; the star's tips reach S*sqrt(2)
    inside = lambda x, y: (abs(x) <= S and abs(y) <= S) or (abs(x + y) <= S * math.sqrt(2) and abs(x - y) <= S * math.sqrt(2))
    lo, hi = 1.0, 20.0
    for _ in range(40):                                         # the spacing that fits exactly n points in the star
        c = (lo + hi) / 2; k = 0; pts = []
        while True:
            r = c * math.sqrt(k + 0.5); a = k * 2.399963
            if r > S * math.sqrt(2) + c: break
            x, y = r * math.cos(a), r * math.sin(a)
            if inside(x, y): pts.append((round(x, 1), round(y, 1)))
            k += 1
        if len(pts) >= n: lo = c
        else: hi = c
    return pts[:n], c

def build():
    N = count(); T = timings()
    out = os.path.join(HERE, "out", ID); a = os.path.join(out, "assets")
    if os.path.exists(out): shutil.rmtree(out)
    os.makedirs(a)
    for f in ("ibm-plex-sans-arabic-arabic-700-normal.woff2", "karla-latin-500-normal.woff2", "karla-latin-700-normal.woff2"):
        shutil.copy(os.path.join(V6, "fonts", f), a)
    shutil.copy(os.path.join(ROOT, "brag-quiz/fonts/instrument-serif-latin-400-normal.woff2"), a); shutil.copy(GSAP, a)
    for f in ("swoosh.wav", "short-swoosh.wav", "swoosh-low.wav", "tap.wav", "click.wav"): shutil.copy(os.path.join(ROOT, "brag-quiz/sfx/ref", f), a)

    # the voice, one line after another
    at, t = {}, 0.15
    for ln in LINES:
        f = ln["file"]; t += GAP.get(f, 0); at[f] = t
        shutil.copy(os.path.join(VOICE, f + ".mp3"), a); t += dur(os.path.join(VOICE, f + ".mp3"))
    END = t + 2.2
    def w(line, word, k=0, edge=0):
        """When `word` (the k-th match) is said in `line`; edge 1 = when it ends. Falls back to the line's start."""
        hits = [x for x in T[line] if re.sub(r"[^\w]", "", x[0].lower()) == word.lower()]
        return round(at[line] + (hits[k][1 + edge] if len(hits) > k else 0), 2)
    def wi(line, i, edge=0):                                    # the i-th word of the line
        x = T[line][min(i, len(T[line]) - 1)]; return round(at[line] + x[1 + edge], 2)
    def lend(line): return round(at[line] + dur(os.path.join(VOICE, line + ".mp3")), 2)

    au = [f'<audio id="{ln["file"]}" src="assets/{ln["file"]}.mp3" data-start="{at[ln["file"]]:.2f}" data-duration="{dur(os.path.join(VOICE, ln["file"] + ".mp3")):.2f}" data-volume="1" data-track-index="{1 + i % 2}"></audio>'
          for i, ln in enumerate(LINES)]
    src = os.path.join(V6, "sfx-gen/fountain.mp3")             # the fountain under it all, as Comp does (build_teach.py)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-i", src, "-filter_complex",
                    f"[0][1]acrossfade=d=2:c1=tri:c2=tri,volume=6dB,atrim=0:{END + 0.5:.2f},afade=t=in:d=0.6,afade=t=out:st={END - 1.4:.2f}:d=1.4",
                    "-c:a", "libmp3lame", "-q:a", "3", os.path.join(a, "fountain.mp3")], check=True)
    au.append(f'<audio id="bed" src="assets/fountain.mp3" data-start="0" data-duration="{END:.2f}" data-volume="0.1" data-track-index="8"></audio>')
    sfx = []
    def fx(name, t0, vol=0.35, d=0.6): sfx.append(f'<audio id="fx{len(sfx)}" src="assets/{name}" data-start="{max(0, t0):.2f}" data-duration="{d}" data-volume="{vol}" data-track-index="{10 + len(sfx) % 4}"></audio>')

    # ---- the page: scenes at fixed places on one tall page; the camera moves between them ----
    PG = {"s1": (0, 0), "s2": (1080, 0), "s3": (0, 1920), "s8": (0, 3840), "s10": (0, 5760), "s10b": (1080, 5760)}
    js = []
    def cam(scene, t0, d=0.75, ease="expo.inOut"):
        x, y = PG[scene]
        js.append(f'tl.to("#world", {{x:{-x}, y:{-y}, duration:{d}, ease:"{ease}"}}, {t0:.2f});')
        js.append(f'tl.fromTo("#blur", {{v:0}}, {{v:1, duration:{d / 2}, ease:"power2.in", yoyo:true, repeat:1, onUpdate:blurUpd}}, {t0:.2f});')
        fx("swoosh.wav" if x else "swoosh-low.wav", t0 + 0.05, 0.4)
    def pop(sel, t0, fromv="{opacity:0, scale:0.6, y:30}", d=0.45, ease="back.out(2)"):
        js.append(f'tl.fromTo("{sel}", {fromv}, {{opacity:1, scale:1, y:0, x:0, filter:"blur(0px)", duration:{d}, ease:"{ease}"}}, {t0:.2f});')
    def zoomin(sel, t0):                                        # the reference's blur-zoom entry
        pop(sel, t0, '{opacity:0, scale:2.6, filter:"blur(24px)"}', 0.5, "expo.out")
    def glow(sel, t0, col):
        js.append(f'tl.to("{sel}", {{color:"{col}", textShadow:"0 0 34px {col}55", duration:0.25}}, {t0:.2f});')
        js.append(f'tl.fromTo("{sel}", {{scale:1}}, {{scale:1.12, duration:0.16, yoyo:true, repeat:1, ease:"power2.out"}}, {t0:.2f});')
    def counter(sel, to, t0, d=0.9, fmt='Math.round(o.v).toLocaleString("en-GB")'):
        js.append(f'(() => {{ const o = {{v:0}}; tl.to(o, {{v:{to}, duration:{d}, ease:"power2.out", onUpdate:() => {{ document.querySelector("{sel}").textContent = {fmt}; }}}}, {t0:.2f}); }})();')
    def draw(sel, t0, d=0.6):                                   # an SVG stroke drawing itself
        js.append(f'tl.fromTo("{sel}", {{strokeDashoffset:1}}, {{strokeDashoffset:0, duration:{d}, ease:"power2.inOut"}}, {t0:.2f});')

    # s1, the hook: on screen from frame 0 (it's the cover); each word lifts as it's said, "Quran" turns teal
    hook = ["Think", "understanding", "the", "Quran", "is", "too", "hard?"]
    s1 = "".join(f'<span class="hw" id="h{i}">{x}</span> ' for i, x in enumerate(hook))
    for i, x in enumerate(hook):
        js.append(f'tl.fromTo("#h{i}", {{y:0}}, {{y:-14, duration:0.14, yoyo:true, repeat:1, ease:"power2.out"}}, {wi("v1", i):.2f});')
    glow("#h3", wi("v1", 3), TEAL); glow("#h6", wi("v1", 6), RED)
    # s2: whip right, "We counted every word of it." word by word, a gold line draws under "every word"
    cam("s2", at["v2"] - 0.35)
    s2w = ["We", "counted", "every", "word", "of", "it."]
    for i in range(len(s2w)): zoomin(f"#c{i}", wi("v2", i) - 0.05)
    s2h = " ".join(f'<span id="c{i}" class="cw">{x}</span>' for i, x in enumerate(s2w[:2])) + \
          ' <span class="uw"><span id="c2" class="cw">every</span> <span id="c3" class="cw">word</span><svg id="under" viewBox="0 0 600 40" preserveAspectRatio="none"><path d="M8 26 C 150 6, 300 34, 592 14" pathLength="1"/></svg></span> ' + \
          " ".join(f'<span id="c{i}" class="cw">{x}</span>' for i, x in enumerate(s2w) if i > 3)
    draw("#under path", wi("v2", 2), 0.5)
    # s3: the page moves up to the star; it grows from the centre as the verses are counted
    cam("s3", at["v3"] - 0.45)
    pop("#n3", at["v3"]); counter("#n3 b", N["verses"], at["v3"], 1.6); pop("#n3 i", w("v3", "verses") - 0.05)
    js.append(f'tl.to(G, {{grow:1, duration:{lend("v3") - at["v3"] + 0.2:.2f}, ease:"power1.inOut"}}, {at["v3"]:.2f});')
    fx("short-swoosh.wav", at["v3"], 0.3)
    # s4/s5: the words counted; then the different ones, as two pills
    js.append(f'tl.to("#n3", {{opacity:0, y:-40, duration:0.3}}, {at["v4"] - 0.3:.2f});')
    pop("#n4", at["v4"]); counter("#n4 b", N["words"], at["v4"], 1.2); pop("#n4 i", w("v4", "words") - 0.05)
    js.append(f'tl.to("#n4", {{opacity:0, y:-40, duration:0.3}}, {at["v5"] - 0.2:.2f});')
    pop("#p5 .lead", at["v5"] - 0.05); pop("#p5a", w("v5", "4") - 0.1, "{opacity:0, x:-260}", 0.5, "expo.out"); counter("#p5a b", N["lemmas"], w("v5", "4"), 0.8)
    pop("#p5b", w("v5", "different"), "{opacity:0, x:260}", 0.5, "expo.out"); fx("click.wav", w("v5", "different"), 0.4, 0.3)
    js.append(f'tl.to(["#p5 .lead", "#p5a", "#p5b"], {{opacity:0, y:-40, duration:0.3, stagger:0.04}}, {at["v6"] - 0.3:.2f});')
    # s6/s7: 100 pops in gold; the star turns gold by how much of each verse is top-100 words; "more than half" circled
    pop("#n6", at["v6"]); zoomin("#n6 b", w("v6", "hundred") - 0.1); fx("tap.wav", w("v6", "hundred"), 0.45, 0.3)
    js.append(f'tl.to(G, {{gold:1, duration:2.0, ease:"power1.inOut"}}, {w("v7", "more") - 0.2:.2f});')
    js.append(f'tl.to("#n6", {{opacity:0, y:-40, duration:0.25}}, {at["v7"] - 0.1:.2f});')
    pop("#n7", at["v7"] + 0.15); counter("#n7 b", round(N["top100"]), w("v7", "more"), 1.6, 'Math.round(o.v) + "%"')
    draw("#ring path", w("v7", "half") - 0.1, 0.7); glow("#n7 .half", w("v7", "half"), GOLD)
    # s8: the page moves up; the top 10 stack as pills, filled and outlined in turn, the first three as they're said
    cam("s8", at["v8"] - 0.5)
    pop("#t8", at["v8"])
    pt = [wi("v8", 2), wi("v8", 3), wi("v8", 4)]
    for k in range(10):
        t0 = pt[k] - 0.05 if k < 3 else lend("v8") + 0.05 + 0.13 * (k - 3)
        pop(f"#k{k}", t0, f"{{opacity:0, x:{-240 if k % 2 == 0 else 240}}}", 0.45, "expo.out"); fx("click.wav", t0, 0.25, 0.3)
    # s9: "a quarter" with a highlighter sweep
    pop("#t9", at["v9"] - 0.05)
    js.append(f'tl.fromTo("#t9 .hl", {{scaleX:0}}, {{scaleX:1, duration:0.45, ease:"power3.out"}}, {w("v9", "quarter") - 0.15:.2f});')
    # s10: down the page; a typewriter line, then a whip to the answer, circled
    cam("s10", at["v10"] - 0.5)
    tw = "So start with"
    js.append(f'(() => {{ const o = {{n:0}}; tl.to(o, {{n:{len(tw)}, duration:{max(0.4, w("v10", "with", 0, 1) - at["v10"]):.2f}, ease:"none", '
              f'onUpdate:() => {{ document.querySelector("#tw").textContent = "{tw}".slice(0, Math.round(o.n)); }}}}, {at["v10"]:.2f}); }})();')
    cam("s10b", w("v10", "a") - 0.1, 0.5)
    zoomin("#a10", w("v10", "hundred") - 0.1); draw("#ring2 path", w("v10", "words"), 0.6)
    # s11 (same place): the site and the free week, high on the screen; the share ask
    js.append(f'tl.to("#a10wrap", {{y:-420, duration:0.6, ease:"expo.inOut"}}, {at["v11"] - 0.35:.2f});')
    pop("#site", at["v11"]); fx("tap.wav", at["v11"], 0.4, 0.3)
    pop("#free", w("v11", "free") - 0.05 if any(x[0].lower().startswith("free") for x in T["v11"]) else at["v11"] + 1.2)
    pop("#send", lend("v11") + 0.2); pop("#src", lend("v11") + 0.4, "{opacity:0}")
    # the soft rings drifting in the corners, as in the reference, the whole way through
    js.append(f'tl.fromTo(".orb", {{rotation:0}}, {{rotation:40, duration:{END:.2f}, ease:"none"}}, 0);')
    js.append(f'tl.fromTo("#orbA", {{x:-40, y:-30}}, {{x:30, y:40, duration:{END:.2f}, ease:"sine.inOut"}}, 0);')
    js.append(f'tl.fromTo("#orbB", {{x:30, y:20}}, {{x:-40, y:-50, duration:{END:.2f}, ease:"sine.inOut"}}, 0);')

    pts, c = star_points(N["verses"])
    ten = "".join(f'<div class="pill {"fill" if k % 2 == 0 else "line"}" id="k{k}"><span class="ar" lang="ar">{ar}</span><span class="en">{en}</span></div>'
                  for k, (ar, en, _) in enumerate(N["ten"]))
    S1, S2, S3, S8, S10, S10b = (f'left:{PG[s][0]}px; top:{PG[s][1]}px' for s in ("s1", "s2", "s3", "s8", "s10", "s10b"))
    body = f"""
<div id="world">
 <section style="{S1}"><div class="big hook">{s1}</div></section>
 <section style="{S2}"><div class="big" id="s2t">{s2h}</div></section>
 <section style="{S3}">
   <div class="num" id="n3"><b>0</b> <i>verses</i></div>
   <div class="num" id="n4"><b>0</b> <i>words</i></div>
   <div id="p5"><span class="lead">But only</span><div class="row"><div class="pill fill xl" id="p5a"><b>0</b></div><div class="pill line xl" id="p5b">different ones</div></div></div>
   <div class="num" id="n6"><span class="sm">And just</span><b class="gold">100</b><i>of them</i></div>
   <div class="num" id="n7"><b class="gold">0%</b><span class="half">more than half<svg id="ring" viewBox="0 0 520 150" preserveAspectRatio="none"><path d="M60 80 C 40 20, 470 10, 500 70 C 520 130, 120 150, 40 100 C 20 85, 60 40, 140 30" pathLength="1"/></svg></span><i>of the Quran</i></div>
   <canvas id="star" width="1080" height="1080"></canvas>
 </section>
 <section style="{S8}"><div class="title" id="t8">Words like…</div><div id="pills">{ten}</div>
   <div class="title" id="t9">The top 10 alone: <span class="hlw"><span class="hl"></span><span>a quarter</span></span><br><i>of every page.</i></div></section>
 <section style="{S10}"><div class="big"><span id="tw"></span><span class="caret">|</span></div></section>
 <section style="{S10b}"><div id="a10wrap"><div class="big" id="a10">100 <i>words.</i><svg id="ring2" viewBox="0 0 520 220" preserveAspectRatio="none"><path d="M70 120 C 40 40, 470 20, 500 100 C 520 190, 110 210, 40 140 C 20 120, 70 60, 160 45" pathLength="1"/></svg></div></div>
   <div id="site"><span class="tile"><span lang="ar">ر</span><em></em></span>rafiq-arabic.com</div>
   <div id="free">Free for a week · no card needed</div>
   <div id="send">Send this to someone learning the Quran 🤍</div>
   <div id="src">Counted from the Quranic Arabic Corpus (corpus.quran.com). “Different words” = dictionary forms.</div></section>
</div>
<div class="orb" id="orbA"></div><div class="orb" id="orbB"></div>"""
    css = f"""
@font-face {{ font-family:"Ar"; src:url("assets/ibm-plex-sans-arabic-arabic-700-normal.woff2"); font-weight:700; }}
@font-face {{ font-family:"Karla"; src:url("assets/karla-latin-500-normal.woff2"); font-weight:500; }}
@font-face {{ font-family:"Karla"; src:url("assets/karla-latin-700-normal.woff2"); font-weight:700; }}
@font-face {{ font-family:"Serif"; src:url("assets/instrument-serif-latin-400-normal.woff2"); }}
body {{ margin:0; background:#000; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; background:{CREAM}; color:{INK}; font-family:"Karla";
  background-image:radial-gradient(circle at 50% 0%, rgba(168,132,44,.16) 0%, rgba(241,236,224,0) 55%); }}
#world {{ position:absolute; left:0; top:0; width:2160px; height:7680px; }}
section {{ position:absolute; width:1080px; height:1920px; }}
i {{ font-family:"Serif"; font-style:italic; font-weight:400; }}
.big {{ position:absolute; left:80px; right:80px; top:700px; text-align:center; font-weight:700; font-size:104px; line-height:1.08; letter-spacing:-.03em; }}
.hook .hw {{ display:inline-block; }}
.cw {{ display:inline-block; opacity:0; }}
.uw {{ position:relative; display:inline-block; }}
#under {{ position:absolute; left:-10px; right:-10px; bottom:-34px; width:calc(100% + 20px); height:44px; overflow:visible; }}
svg path {{ fill:none; stroke:{GOLD2}; stroke-width:12; stroke-linecap:round; stroke-dasharray:1; stroke-dashoffset:1; }}
.num {{ position:absolute; left:60px; right:60px; top:150px; height:470px; display:flex; flex-direction:column; justify-content:center; align-items:center;
  text-align:center; font-size:72px; font-weight:700; opacity:0; letter-spacing:-.02em; line-height:1; }}
.num b {{ display:block; font-size:200px; letter-spacing:-.05em; }} .num i {{ display:block; font-size:100px; color:{TEAL}; margin-top:6px; }}
.num .sm {{ display:block; font-size:64px; margin-bottom:6px; }}
.gold {{ color:{GOLD}; }}
#n7 .half {{ position:relative; display:inline-block; font-size:80px; padding:10px 24px; margin-top:4px; }}
#ring {{ position:absolute; left:-30px; top:-30px; width:calc(100% + 60px); height:150px; overflow:visible; }}
#p5 {{ position:absolute; left:0; right:0; top:150px; height:470px; display:flex; flex-direction:column; justify-content:center; align-items:center; }}
#p5 .lead {{ font-size:72px; font-weight:700; margin-bottom:22px; opacity:0; }}
#p5 .row {{ display:flex; gap:10px; }}
.pill {{ display:inline-flex; align-items:center; gap:18px; border-radius:999px; padding:14px 34px; font-size:44px; font-weight:700; opacity:0; margin:8px; }}
.pill.fill {{ background:{TEAL}; color:{CREAM}; box-shadow:0 14px 30px -14px rgba(46,114,99,.8); }}
.pill.line {{ border:4px solid {INK}; color:{INK}; background:rgba(255,255,255,.35); }}
.pill.xl {{ font-size:64px; padding:18px 46px; }}
#star {{ position:absolute; left:0; top:640px; }}
.title {{ position:absolute; left:70px; right:70px; text-align:center; font-size:80px; font-weight:700; letter-spacing:-.02em; line-height:1.1; opacity:0; }}
#t8 {{ top:220px; }} #t9 {{ top:1380px; }}
#pills {{ position:absolute; left:50px; right:50px; top:400px; display:flex; flex-wrap:wrap; justify-content:center; }}
#pills .pill {{ font-size:46px; padding:12px 34px; margin:10px; }} #pills .ar {{ font-family:"Ar"; font-size:72px; line-height:1.3; }}
.hlw {{ position:relative; display:inline-block; }} .hlw span:last-child {{ position:relative; }}
.hl {{ position:absolute; left:-12px; right:-12px; top:18%; bottom:4%; background:{GOLD2}; border-radius:12px; transform-origin:left center; transform:scaleX(0); }}
.caret {{ color:{TEAL}; font-weight:500; }}
#a10wrap {{ position:absolute; left:0; right:0; top:0; height:1920px; }}
#a10 {{ font-size:170px; color:{TEAL}; opacity:0; }} #a10 i {{ color:{INK}; }}
#ring2 {{ position:absolute; left:-30px; top:-50px; width:calc(100% + 60px); height:280px; overflow:visible; }}
#site {{ position:absolute; left:110px; right:110px; top:760px; display:flex; justify-content:center; align-items:center; gap:22px; background:{TEAL}; color:{CREAM};
  border-radius:999px; padding:28px; font-size:56px; font-weight:700; opacity:0; box-shadow:0 20px 40px -18px rgba(46,114,99,.9); }}
.tile {{ position:relative; width:70px; height:70px; border-radius:18px; background:{CREAM}; display:grid; place-items:center; }}
.tile span {{ font-family:"Ar"; font-weight:700; font-size:44px; color:{INK}; margin-top:-6px; }}
.tile em {{ position:absolute; right:10px; top:9px; width:11px; height:11px; border-radius:50%; background:{RED}; }}
#free {{ position:absolute; left:0; right:0; top:930px; text-align:center; font-size:40px; font-weight:500; color:#4f6163; opacity:0; }}
#send {{ position:absolute; left:120px; right:120px; top:1040px; text-align:center; font-size:44px; font-weight:700; color:{INK}; border:4px solid {INK};
  border-radius:999px; padding:20px; opacity:0; }}
#src {{ position:absolute; left:90px; right:90px; top:1650px; text-align:center; font-size:26px; color:#6b7a7c; opacity:0; }}
.orb {{ position:absolute; width:520px; height:520px; border-radius:50%; border:70px solid rgba(46,114,99,.07); pointer-events:none; }}
#orbA {{ left:-260px; top:-200px; }} #orbB {{ right:-240px; bottom:-220px; border-color:rgba(168,132,44,.08); }}
"""
    star = f"""
const P = {json.dumps(pts)}, F = {json.dumps(N["frac"])}, R = {c * 0.5:.2f};
const G = {{grow:0, gold:0, t:0}}, cv = document.getElementById("star"), X = cv.getContext("2d");
function drawStar() {{
  X.clearRect(0, 0, 1080, 1080); const n = P.length, shown = G.grow * n;
  for (let i = 0; i < n; i++) {{
    const k = shown - i; if (k <= 0) break;
    const s = Math.min(1, k / 140), pop = s < 1 ? 1 + 0.6 * Math.sin(s * Math.PI) : 1;
    const g = G.gold * F[i] / 100;
    X.globalAlpha = Math.min(1, (0.5 + 0.45 * s) * (0.85 + 0.25 * g + 0.1 * Math.sin(G.t * 2 + i)));
    const q = Math.min(1, g * 1.6);
    X.fillStyle = q > 0.02 ? `rgb(${{Math.round(46 + 187 * q)}},${{Math.round(114 + 71 * q)}},${{Math.round(99 - 26 * q)}})` : "{TEAL}";
    X.beginPath(); X.arc(540 + P[i][0], 540 + P[i][1], R * s * pop * (1 + 0.35 * g), 0, 6.29); X.fill();
  }}
  X.globalAlpha = 1;
}}
const BL = {{v:0}};
function blurUpd() {{ document.getElementById("world").style.filter = `blur(${{(this.targets()[0].v * 10).toFixed(1)}}px)`; }}
"""
    js = [j.replace('"#blur", {v:0}', 'BL, {v:0}') for j in js]
    open(os.path.join(out, "index.html"), "w").write(f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" /><title>{ID}</title>
<script src="assets/gsap.min.js"></script><style>{css}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{END:.2f}">
{body}
{chr(10).join(au + sfx)}
</div><script>{star}
const tl = gsap.timeline({{ paused: true, onUpdate: drawStar }});
tl.to(G, {{t:{END:.2f}, duration:{END:.2f}, ease:"none"}}, 0);
{chr(10).join(js)}
drawStar();
window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;</script></body></html>
""")
    print(f"{ID}: {END:.1f}s · star spacing {c:.2f}px · line starts " + ", ".join(f"{k} {v:.2f}" for k, v in at.items()))

if __name__ == "__main__":
    build()
