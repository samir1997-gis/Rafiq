#!/usr/bin/env python3
"""q1-quran-count (owner, 11 Oct 2026): "Think understanding the Quran is too hard?", in the style of a viral frames.of.quran
data reel: a dark sky, one dot per verse (6,236), numbers counting up, no talking, the fountain underneath.

Every number is counted here from the Quranic Arabic Corpus v0.4 (corpus.quran.com, downloaded on first run): 6,236 verses,
77,429 words, 4,831 different words (dictionary forms, "lemmas") from 1,642 roots; the 100 most common words are 54.8% of all the
words, the top 10 about a quarter. Each verse's dot turns gold by how much of it is top-100 words. Hook and ending chosen with
TypeSafe (tools/typesafe-exp/quran_count_video.py).

  python3 brag-quiz/reels/quran-count/build.py      then in brag-quiz/reels/quran-count/out/q1-quran-count:
  npx hyperframes render -o ../q1-quran-count.mp4    and level it to -16 LUFS (loudnorm), as the other reels
"""
import collections, json, os, re, shutil, subprocess, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
V6 = os.path.join(ROOT, "brag-output-v6/composition/assets")
GSAP = os.path.join(V6, "lib/gsap.min.js")
CORPUS = os.path.expanduser("~/.cache/rafiq/quranic-corpus-morphology-0.4.txt")
CORPUS_URL = "https://raw.githubusercontent.com/cltk/arabic_morphology_quranic-corpus/master/quranic-corpus-morphology-0.4.txt"
ID = "q1-quran-count"

# the top 10, in the corpus's order (Buckwalter lemma -> how it's written, what it means)
TEN = {"min": ("مِنْ", "from"), "{ll~ah": ("ٱللَّه", "Allah"), "maA": ("مَا", "what · not"), "laA": ("لَا", "no · not"),
       "fiY": ("فِي", "in"), "qaAla": ("قَالَ", "he said"), "<in~": ("إِنَّ", "indeed"), "{l~a*iY": ("ٱلَّذِي", "who · which"),
       "EalaY`": ("عَلَىٰ", "on"), "kaAna": ("كَانَ", "was")}

def count():
    if not os.path.exists(CORPUS):
        os.makedirs(os.path.dirname(CORPUS), exist_ok=True); urllib.request.urlretrieve(CORPUS_URL, CORPUS)
    words, verses = {}, []
    for line in open(CORPUS, encoding="utf-8"):
        if not line.startswith("("): continue
        loc, form, tag, feat = line.rstrip("\n").split("\t")
        s, v, w, _ = map(int, loc.strip("()").split(":"))
        if (s, v) not in verses[-1:]: verses.append((s, v))
        d = words.setdefault((s, v, w), {"lem": None, "root": None})
        if "STEM" in feat:
            m = re.search(r"LEM:([^|]+)", feat); r = re.search(r"ROOT:([^|]+)", feat)
            d["lem"] = m and m.group(1); d["root"] = r and r.group(1)
    lem = collections.Counter(d["lem"] for d in words.values() if d["lem"])
    top = [l for l, _ in lem.most_common(100)]; top100 = set(top)
    share = lambda n: 100 * sum(c for _, c in lem.most_common(n)) / len(words)
    per = collections.defaultdict(lambda: [0, 0])
    for (s, v, _), d in words.items(): per[(s, v)][0] += 1; per[(s, v)][1] += d["lem"] in top100
    n = dict(verses=len(verses), words=len(words), lemmas=len(lem), roots=len({d["root"] for d in words.values() if d["root"]}),
             top10=share(10), top100=share(100), ten=[(TEN[l][0], TEN[l][1], c) for l, c in lem.most_common(10)],
             frac=[round(100 * per[k][1] / per[k][0]) for k in verses])
    assert top[:10] == list(TEN), top[:10]
    assert (n["verses"], n["words"], n["lemmas"], n["roots"], round(n["top100"])) == (6236, 77429, 4831, 1642, 55), n
    return n

def build():
    N = count()
    out = os.path.join(HERE, "out", ID); a = os.path.join(out, "assets")
    if os.path.exists(out): shutil.rmtree(out)
    os.makedirs(a)
    for f in ("ibm-plex-sans-arabic-arabic-700-normal.woff2", "karla-latin-500-normal.woff2", "karla-latin-700-normal.woff2"):
        shutil.copy(os.path.join(V6, "fonts", f), a)
    shutil.copy(os.path.join(ROOT, "brag-quiz/fonts/instrument-serif-latin-400-normal.woff2"), a)
    shutil.copy(GSAP, a)
    for f in ("swoosh-low.wav", "charge-swoosh.wav", "tap.wav"): shutil.copy(os.path.join(ROOT, "brag-quiz/sfx/ref", f), a)
    T = 23.0
    # the fountain, played on past its 22 s (two copies crossfaded), as Comp does in build_teach.py
    src = os.path.join(V6, "sfx-gen/fountain.mp3")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-i", src, "-filter_complex",
                    f"[0][1]acrossfade=d=2:c1=tri:c2=tri,volume=6dB,atrim=0:{T + 0.5:.2f},afade=t=in:d=0.6,afade=t=out:st={T - 1.4:.2f}:d=1.4",
                    "-c:a", "libmp3lame", "-q:a", "3", os.path.join(a, "fountain.mp3")], check=True)
    au = ['<audio id="bed" src="assets/fountain.mp3" data-start="0" data-duration="23.00" data-volume="0.1" data-track-index="8"></audio>',
          '<audio id="s1" src="assets/swoosh-low.wav" data-start="2.70" data-duration="1.5" data-volume="0.45" data-track-index="6"></audio>',
          '<audio id="s2" src="assets/charge-swoosh.wav" data-start="11.40" data-duration="2.0" data-volume="0.4" data-track-index="7"></audio>']
    au += [f'<audio id="t{k}" src="assets/tap.wav" data-start="{15.9 + 0.18 * k:.2f}" data-duration="0.3" data-volume="0.35" data-track-index="{10 + k % 2}"></audio>'
           for k in range(10)]
    ten = "".join(f'<div class="w"><div class="ar" lang="ar">{ar}</div><div class="en">{en}</div><div class="n">×{c:,}</div></div>' for ar, en, c in N["ten"])
    lines = {  # id: (text, in, out)
        "l1": ('Think understanding the <i>Quran</i> is too hard?', 0, 2.6),
        "l2": ('We counted every word of it.', 2.7, 5.4),
        "l3": ('Each dot is one verse.<br><span>All <b>6,236</b> of them.</span>', 5.5, 8.4),
        "l4": ('<b id="nw">0</b> words.<br><span id="l4b">But only <b>4,831</b> different ones.</span>', 8.5, 11.3),
        "l5": ('Just <b>100</b> of them make up<br><b class="big" id="pc">0%</b><br><span>of every word in the Quran.</span>', 11.4, 15.6),
        "l6": ('The top 10 alone: <b>a quarter</b>.', 15.7, 19.4),
        "l7": ('Think the Quran is too hard to understand?<br><b>Start with 100 words.</b>', 19.5, 23.5),
    }
    divs = "".join(f'<div class="line" id="{k}">{t}</div>' for k, (t, _, _) in lines.items())
    js = []
    for k, (_, t0, t1) in lines.items():
        js.append(f'tl.fromTo("#{k}", {{opacity:{1 if t0 == 0 else 0}, y:{0 if t0 == 0 else 18}, filter:"blur({0 if t0 == 0 else 8}px)"}}, '
                  f'{{opacity:1, y:0, filter:"blur(0px)", duration:0.6, ease:"power3.out"}}, {t0});')
        if t1 < T: js.append(f'tl.to("#{k}", {{opacity:0, y:-12, filter:"blur(6px)", duration:0.4, ease:"power2.in"}}, {t1 - 0.4});')
    js += ['tl.fromTo("#l4b", {opacity:0}, {opacity:1, duration:0.5}, 9.6);',
           f'(() => {{ const o = {{v:0}}; tl.to(o, {{v:{N["words"]}, duration:1.0, ease:"power2.out", onUpdate:() => {{ document.getElementById("nw").textContent = Math.round(o.v).toLocaleString("en-GB"); }}}}, 8.6); }})();',
           f'(() => {{ const o = {{v:0}}; tl.to(o, {{v:{N["top100"]:.1f}, duration:3.0, ease:"power1.inOut", onUpdate:() => {{ document.getElementById("pc").textContent = Math.round(o.v) + "%"; }}}}, 11.6); }})();',
           'tl.fromTo("#ten", {opacity:0}, {opacity:1, duration:0.4}, 15.8);',
           'tl.fromTo("#ten .w", {opacity:0, y:30, scale:0.9}, {opacity:1, y:0, scale:1, duration:0.5, stagger:0.18, ease:"back.out(1.6)"}, 15.85);',
           'tl.to("#ten", {opacity:0, duration:0.4}, 19.1);',
           'tl.fromTo("#ask", {opacity:0, y:20, scale:0.96}, {opacity:1, y:0, scale:1, duration:0.5, ease:"back.out(1.6)"}, 20.3);',
           'tl.fromTo("#panel", {opacity:0}, {opacity:1, duration:0.5}, 20.2);',
           'tl.fromTo("#free", {opacity:0}, {opacity:1, duration:0.4}, 20.7);',
           'tl.fromTo("#send", {opacity:0, y:12}, {opacity:1, y:0, duration:0.4, ease:"power3.out"}, 21.2);',
           'tl.fromTo("#src", {opacity:0}, {opacity:1, duration:0.5}, 5.6);',
           'tl.fromTo("#brand", {opacity:0}, {opacity:0.9, duration:0.5}, 0.2);']
    css = """
@font-face { font-family:"Ar"; src:url("assets/ibm-plex-sans-arabic-arabic-700-normal.woff2"); font-weight:700; }
@font-face { font-family:"Karla"; src:url("assets/karla-latin-500-normal.woff2"); font-weight:500; }
@font-face { font-family:"Karla"; src:url("assets/karla-latin-700-normal.woff2"); font-weight:700; }
@font-face { font-family:"Instrument Serif"; src:url("assets/instrument-serif-latin-400-normal.woff2"); }
body { margin:0; background:#000; } #root { position:relative; width:1080px; height:1920px; overflow:hidden;
  background:radial-gradient(ellipse 120% 70% at 50% 0%, #16294a 0%, #0a1426 45%, #050a14 100%); }
canvas { position:absolute; inset:0; }
.line { position:absolute; top:250px; left:70px; right:70px; text-align:center; font-family:"Instrument Serif"; font-size:92px; line-height:1.12;
  color:#eef1f7; opacity:0; text-shadow:0 4px 30px rgba(5,10,20,.9); }
.line i { color:#E9B949; } .line b { color:#E9B949; font-weight:400; } .line span { font-size:64px; color:rgba(238,241,247,.8); }
.line .big { font-size:220px; line-height:1; display:inline-block; margin:18px 0 6px; }
#l1 { top:700px; font-size:104px; } #l7 { top:300px; } #l7 b { display:inline-block; margin-top:20px; font-size:104px; }
#ten { position:absolute; top:560px; left:60px; right:60px; display:grid; grid-template-columns:repeat(2, 1fr); gap:22px; opacity:0; direction:rtl; }
.w { background:rgba(10,20,38,.82); border:2px solid rgba(233,185,73,.35); border-radius:28px; padding:14px 26px 18px; display:grid;
  grid-template-columns:auto 1fr; grid-template-rows:auto auto; column-gap:22px; align-items:center; backdrop-filter:blur(6px); }
.w .ar { grid-row:1 / 3; font-family:"Ar"; font-weight:700; font-size:78px; color:#E9B949; line-height:1.35; }
.w .en { direction:ltr; text-align:left; font-family:"Karla"; font-weight:700; font-size:36px; color:#eef1f7; }
.w .n { direction:ltr; text-align:left; font-family:"Karla"; font-weight:500; font-size:28px; color:rgba(238,241,247,.6); }
#ask { position:absolute; top:1330px; left:110px; right:110px; text-align:center; font-family:"Karla"; font-weight:700; font-size:50px; color:#0a1426;
  background:#E9B949; border-radius:999px; padding:28px 34px; opacity:0; }
#panel { position:absolute; top:1290px; left:70px; right:70px; height:390px; border-radius:44px; background:rgba(5,10,20,.86);
  box-shadow:0 0 80px 40px rgba(5,10,20,.7); opacity:0; }
#free { position:absolute; top:1480px; left:0; right:0; text-align:center; font-family:"Karla"; font-weight:500; font-size:34px; color:rgba(238,241,247,.75); opacity:0; }
#send { position:absolute; top:1580px; left:0; right:0; text-align:center; font-family:"Karla"; font-weight:700; font-size:40px; color:#E9B949; opacity:0; }
#src { position:absolute; bottom:120px; left:80px; right:80px; text-align:center; font-family:"Karla"; font-weight:500; font-size:26px;
  color:rgba(238,241,247,.45); line-height:1.35; opacity:0; }
#brand { position:absolute; top:90px; left:0; right:0; text-align:center; font-family:"Ar"; font-weight:700; font-size:44px; color:#eef1f7; opacity:0; }
"""
    draw = """
const C = document.getElementById("c"), X = C.getContext("2d"), W = 1080, H = 1920, n = FRAC.length;
let seed = 7; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
const COLS = 76, SP = 11.6, GX = (W - (COLS - 1) * SP) / 2, GY = 760;
const D = FRAC.map((f, i) => ({ gx: GX + (i % COLS) * SP, gy: GY + Math.floor(i / COLS) * SP, sx: rnd() * W, sy: rnd() * H * 0.9,
  ph: rnd() * 6.28, d: rnd(), f: f / 100 }));
const STARS = Array.from({length: 260}, () => ({ x: rnd() * W, y: rnd() * H, r: 0.6 + rnd() * 1.4, ph: rnd() * 6.28 }));
const cl = (v) => Math.max(0, Math.min(1, v)), io = (v) => v < .5 ? 4 * v * v * v : 1 - Math.pow(-2 * v + 2, 3) / 2;
function draw(t) {
  X.clearRect(0, 0, W, H);
  for (const s of STARS) { X.globalAlpha = 0.25 + 0.25 * Math.sin(s.ph + t * 1.3); X.fillStyle = "#cfd8ea"; X.beginPath(); X.arc(s.x, s.y, s.r, 0, 6.29); X.fill(); }
  const gold = io(cl((t - 11.6) / 3.0)), dim = 1 - 0.55 * cl((t - 15.6) / 0.5) + 0.35 * cl((t - 19.4) / 0.6);
  for (let i = 0; i < n; i++) {
    const p = D[i], c = io(cl((t - 2.7 - p.d * 1.2) / 1.6));
    const x = p.sx + Math.sin(p.ph + t * .6) * 18 + (p.gx - p.sx - Math.sin(p.ph + t * .6) * 18) * c,
          y = p.sy + Math.cos(p.ph + t * .5) * 18 + (p.gy - p.sy - Math.cos(p.ph + t * .5) * 18) * c;
    const lit = cl((t - 5.6 - 2.2 * i / n) / 0.35), flash = lit * (1 - cl((t - 5.95 - 2.2 * i / n) / 0.8));
    const g = gold * p.f;
    const free = 1 - c;                                   // still drifting: a brighter swarm, as in the reference
    let a = (0.22 + 0.45 * free * (0.6 + 0.4 * Math.sin(p.ph + t * 3)) + 0.33 * lit + 0.45 * flash + 0.6 * g) * dim;
    const r = 2.1 + 0.8 * free + 1.6 * flash + 2.0 * g;
    X.globalAlpha = cl(a);
    X.fillStyle = `rgb(${Math.round(150 + 83 * g)},${Math.round(185 + 0 * g)},${Math.round(235 - 162 * g)})`;
    X.beginPath(); X.arc(x, y, r, 0, 6.29); X.fill();
  }
  X.globalAlpha = 1;
}
"""
    open(os.path.join(out, "index.html"), "w").write(f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" /><title>{ID}</title>
<script src="assets/gsap.min.js"></script><style>{css}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{T}">
<canvas id="c" width="1080" height="1920"></canvas>
<div id="brand" lang="ar">رَفِيق</div>{divs}<div id="ten">{ten}</div>
<div id="panel"></div><div id="ask">Learn the 100 at rafiq-arabic.com</div><div id="free">Free for a week · no card needed</div><div id="send">Send this to someone learning the Quran 🤍</div>
<div id="src">Counted from the Quranic Arabic Corpus (corpus.quran.com). “Different words” = dictionary forms, counting every form of each word.</div>
{chr(10).join(au)}
</div><script>const FRAC = {json.dumps(N["frac"])};
{draw}
const tl = gsap.timeline({{ paused: true }});
(() => {{ const o = {{t:0}}; tl.to(o, {{t:{T}, duration:{T}, ease:"none", onUpdate:() => draw(o.t)}}, 0); }})();
draw(0);
{chr(10).join(js)}
window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;</script></body></html>
""")
    print(f"{ID}: {T}s · {N['verses']} verses, {N['words']} words, {N['lemmas']} lemmas, {N['roots']} roots, top 10 {N['top10']:.1f}%, top 100 {N['top100']:.1f}%")

if __name__ == "__main__":
    build()
