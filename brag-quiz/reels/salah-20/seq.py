#!/usr/bin/env python3
"""The Day of Judgement graphics for the 20-words salah reel, rebuilt as two continuous sequences (owner, 13 Oct 2026):
no cut back to the speaker in the middle of a moment, and every word comes in and leaves with motion, the way the owner's
reference does it (small white words build up, the key word lands big in gold; lines leave upwards with a blur; pages whip).

  A   "you wake up in the grave … Munkar and Nakir … questioning you" → straight into "you wait in the barzakh"
  BC  "resurrected" (the ground cracks) → 50,000 years counting high on the same page → the sun comes down onto that ground
      → the heat and the sweat → the crowd, afraid → whip → "the first thing, the very first thing that you are questioned
      about" → the hadith and its reference on the same page, held until he says "salah" (build.py cuts back to him there)

Nothing depicts the angels or a face: the grave is its three questions, the gathering is anonymous silhouettes.
Sources: the grave questions (Abu Dawud 4753), 50,000 years (Qur'an 70:4), the sun and the sweat (Muslim 2864),
the first thing asked about (Tirmidhi 413, Nasa'i 465). Times are the take's, mapped through the cut (timemap.py).

  python3 seq.py /tmp/reel-salah        → out/seqA, out/seqBC; then in each: npx hyperframes render -o ../<id>.mp4
"""
import math, os, random, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE); from timemap import loader
W = sys.argv[1]; m = loader(W)
FONTS = os.path.join(ROOT, "brag-quiz/fonts"); GSAP = os.path.join(ROOT, "brag-output-v6/composition/assets/lib/gsap.min.js")
GOLD, RED, PAPER, INK = "#E9B949", "#C8372D", "#F1ECE0", "#17262B"
SEQ = {"seqA": (7.25, 15.90), "seqBC": (20.80, 39.95)}     # take times; build.py cuts these in over the speaker

CSS = f"""
@font-face {{ font-family:"Anton"; src:url("assets/anton-latin-400-normal.woff2"); }}
@font-face {{ font-family:"Instrument Serif"; src:url("assets/instrument-serif-latin-400-normal.woff2"); }}
@font-face {{ font-family:"Ar"; src:url("assets/ibm-plex-sans-arabic-arabic-700-normal.woff2"); font-weight:700; }}
body {{ margin:0; background:#000; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; background:#000; }}
#cam {{ position:absolute; inset:0; transform-origin:50% 45%; }}
.page {{ position:absolute; inset:0; overflow:hidden; }}
.full {{ position:absolute; inset:0; }}
.line {{ position:absolute; left:60px; right:60px; display:flex; flex-wrap:wrap; justify-content:center; align-items:baseline;
        column-gap:18px; font-family:Anton; text-transform:uppercase; color:#fff; line-height:1.0; text-shadow:0 6px 30px rgba(0,0,0,.7); }}
.line span {{ display:inline-block; transform-origin:50% 80%; }}
.s {{ font-size:60px; letter-spacing:.02em; }}
.k {{ font-size:150px; color:{GOLD}; }}
.q {{ position:absolute; left:80px; right:80px; text-align:center; font-family:"Instrument Serif"; font-size:72px; color:{PAPER};
     text-shadow:0 4px 24px rgba(0,0,0,.8); }}
.q b {{ font-family:Anton; font-weight:400; color:{GOLD}; }}
.ar {{ font-family:Ar; font-weight:700; }}
#vig {{ position:absolute; inset:0; pointer-events:none; background:radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 45%, rgba(0,0,0,.75) 100%); }}
"""

class Seq:
    """One composition: html pieces, GSAP lines, and the take → sequence time map."""
    def __init__(self, sid):
        self.sid = sid; self.a, self.b = SEQ[sid]; self.dur = round(m(self.b) - m(self.a), 3); self.html = []; self.js = []; self.n = 0
    def t(self, take): return round(m(take) - m(self.a), 3)          # a word's time in the take → in this sequence
    def line(self, words, top, out=None, page=None, k_size=None, color=None):
        """Words that build up one at a time: (text, take time, key?). Key words land big from a zoom, the rest rise in.
        out: take time the whole line leaves (upwards, blurred)."""
        lid = f"L{self.n}"; self.n += 1; spans = []
        for i, (w, at, key) in enumerate(words):
            css = ([f"font-size:{k_size}px"] if k_size else []) + ([f"color:{color}"] if color else [])
            st = f' style="{";".join(css)}"' if key and css else ""
            spans.append(f'<span id="{lid}w{i}" class="{"k" if key else "s"}"{st}>{w}</span>')
            if key: self.js.append(f'tl.fromTo("#{lid}w{i}", {{opacity:0, scale:1.9, filter:"blur(14px)"}}, {{opacity:1, scale:1, filter:"blur(0px)", duration:0.24, ease:"back.out(2.2)"}}, {self.t(at):.2f});')
            else: self.js.append(f'tl.fromTo("#{lid}w{i}", {{opacity:0, y:40, filter:"blur(8px)"}}, {{opacity:1, y:0, filter:"blur(0px)", duration:0.16, ease:"power3.out"}}, {self.t(at):.2f});')
        self.add(f'<div class="line" id="{lid}" style="top:{top}px">{"".join(spans)}</div>', page)
        if out: self.js.append(f'tl.to("#{lid}", {{opacity:0, y:-90, filter:"blur(12px)", duration:0.22, ease:"power2.in"}}, {self.t(out) - 0.22:.2f});')
        return lid
    def add(self, h, page=None): (self.pages[page] if page else self.html).append(h)
    def write(self, body):
        out = os.path.join(HERE, "out", self.sid); a = os.path.join(out, "assets")
        if os.path.exists(out): shutil.rmtree(out)
        os.makedirs(a)
        for f in os.listdir(FONTS): shutil.copy(os.path.join(FONTS, f), a)
        shutil.copy(GSAP, a)
        js = [f'tl.fromTo("#cam", {{scale:1}}, {{scale:1.06, duration:{self.dur}, ease:"none"}}, 0);'] + self.js
        open(os.path.join(out, "index.html"), "w").write(f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<title>{self.sid}</title><script src="assets/gsap.min.js"></script><style>{CSS}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{self.dur}">
<div id="cam">{body}</div><div id="vig"></div></div>
<script>const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;</script></body></html>
""")
        print(f"{self.sid}: {self.dur}s")

def dots(n, seed, w=1080, h=1920, r=(2, 5)):
    rnd = random.Random(seed); return [(rnd.uniform(0, w), rnd.uniform(0, h), rnd.uniform(*r), rnd.random()) for _ in range(n)]

def whip(s, out_sel, in_sel, at, axis="y"):
    """A page leaves and the next arrives in one blurred move (the page-to-page motion of the reference)."""
    d = -1920 if axis == "y" else -1080
    s.js.append(f'tl.to("{out_sel}", {{{axis}:{d}, filter:"blur(22px)", duration:0.3, ease:"power3.in"}}, {at - 0.3:.2f});')
    s.js.append(f'tl.fromTo("{in_sel}", {{{axis}:{-d}, filter:"blur(22px)"}}, {{{axis}:0, filter:"blur(0px)", duration:0.32, ease:"power3.out"}}, {at - 0.12:.2f});')

def seq_a():
    s = Seq("seqA"); s.pages = {"g": [], "b": []}
    ps = dots(45, 1, h=1300); st = dots(170, 2, w=2200, h=2200, r=(1.5, 4))
    s.add('<div class="full" style="background:linear-gradient(#06080c 0%,#0f1318 60%,#1a1612 100%)"></div>'
          '<div id="beam" class="full" style="background:linear-gradient(90deg,transparent 40%,rgba(233,185,73,.16) 50%,transparent 60%);opacity:0"></div>'
          + "".join(f'<div class="p" style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;width:{r:.1f}px;height:{r:.1f}px;border-radius:50%;background:rgba(233,185,73,{.25 + .5 * o:.2f})"></div>' for x, y, r, o in ps) +
          '<svg class="full" viewBox="0 0 1080 1920"><path d="M0 1500 Q540 1420 1080 1500 L1080 1920 L0 1920Z" fill="#0b0907"/>'
          '<ellipse cx="540" cy="1515" rx="330" ry="70" fill="#17120d"/><ellipse id="glow" cx="540" cy="1500" rx="260" ry="40" fill="rgba(233,185,73,.3)" opacity="0"/></svg>', "g")
    s.line([("you", 7.34, 0), ("wake", 7.56, 0), ("up", 7.80, 0), ("in the", 7.98, 0), ("grave", 8.28, 1)], 330, out=9.90, page="g")
    s.line([("Munkar", 9.96, 1), ("&", 10.32, 0), ("Nakir", 10.54, 1), ("in front", 11.02, 0), ("of you", 11.42, 0)], 300, out=12.10, page="g", k_size=140, color=PAPER)
    s.line([("they're", 12.12, 0), ("questioning", 12.36, 1), ("you", 12.72, 0)], 260, page="g", k_size=130)
    qs = ["Who is your <b>Lord</b>?", "What is your <b>religion</b>?", 'Who is your <b>Prophet</b> <span class="ar" style="font-size:52px">ﷺ</span>?']
    for i, q in enumerate(qs):                             # the three questions come in one by one, sliding from alternate sides
        s.add(f'<div class="q" id="q{i}" style="top:{640 + i * 170}px">{q}</div>', "g")
        s.js.append(f'tl.fromTo("#q{i}", {{opacity:0, x:{260 if i % 2 == 0 else -260}, filter:"blur(12px)"}}, {{opacity:1, x:0, filter:"blur(0px)", duration:0.32, ease:"power3.out"}}, {s.t(12.40) + i * 0.45:.2f});')
    s.line([("you wait", 13.56, 0), ("in the", 14.08, 0)], 1230, page="g")
    s.js += ['tl.to("#beam", {opacity:1, duration:1.2, ease:"power2.out"}, 0.1);', 'tl.to("#glow", {opacity:1, duration:1.2}, 0.3);',
             f'tl.to(".p", {{y:-160, duration:{s.t(14.3):.2f}, ease:"none", stagger:{{each:0.02, from:"random"}}}}, 0);']
    # the barzakh: the grave page whips up and away, the night sky comes in, the word in Arabic blooms
    s.add(f'<div class="full" style="background:linear-gradient(#020306 0%,#070b14 65%,#141620 100%)"></div>'
          f'<div id="sky" style="position:absolute;left:-560px;top:-700px;width:2200px;height:2200px;transform-origin:50% 50%">'
          + "".join(f'<div style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;width:{r:.1f}px;height:{r:.1f}px;border-radius:50%;background:#fff;opacity:{.3 + .7 * o:.2f}"></div>' for x, y, r, o in st) +
          f'</div><div class="full" style="top:1300px;background:linear-gradient(rgba(233,185,73,0) 0%,rgba(233,185,73,.10) 8%,#08080b 30%)"></div>'
          f'<div id="arz" class="ar" lang="ar" style="position:absolute;left:0;right:0;top:700px;text-align:center;font-size:240px;color:rgba(241,236,224,.95);text-shadow:0 0 50px rgba(233,185,73,.45)">البَرْزَخ</div>', "b")
    s.line([("al-barzakh", 14.38, 1)], 1080, page="b", k_size=110)
    s.add(f'<div class="q" id="bt" style="top:1230px;font-size:56px">between this life and the next</div>', "b")
    s.js += [f'tl.fromTo("#arz", {{opacity:0, scale:1.25, filter:"blur(18px)"}}, {{opacity:1, scale:1, filter:"blur(0px)", duration:0.5, ease:"power3.out"}}, {s.t(14.38) - 0.05:.2f});',
             f'tl.fromTo("#bt", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.35, ease:"power3.out"}}, {s.t(14.38) + 0.35:.2f});',
             f'tl.to("#sky", {{rotation:10, duration:{s.dur}, ease:"none"}}, 0);']
    whip(s, "#pg", "#pb", s.t(14.34))
    s.write(f'<div class="page" id="pg">{"".join(s.html + s.pages["g"])}</div><div class="page" id="pb" style="transform:translateY(1920px)">{"".join(s.pages["b"])}</div>')

def seq_bc():
    s = Seq("seqBC"); s.pages = {"j": [], "f": []}
    rnd = random.Random(3); cracks = []
    for k in range(7):                                    # jagged lines out from the centre of the ground
        x, y, pts = 540, 1500, []
        ang = -2.9 + k * 0.9 + rnd.uniform(-.2, .2)
        for _ in range(9):
            x += 60 * math.cos(ang) + rnd.uniform(-25, 25); y += 22 * math.sin(ang) + rnd.uniform(-18, 18); pts.append(f"{x:.0f},{y:.0f}")
        cracks.append("540,1500 " + " ".join(pts))
    dust = dots(60, 4, h=600); r6 = random.Random(5); drops = [(r6.uniform(60, 1020), r6.uniform(-300, 700), r6.uniform(.6, 1.2)) for _ in range(26)]
    r7 = random.Random(6); figs = []
    for row in range(6):                                  # the crowd: far rows small and high, near rows big and low
        sc = 0.32 + row * 0.16; y = 1420 + row * 95; n = int(24 - row * 2.5)
        for i in range(n): figs.append((-200 + i * (1500 / n) + r7.uniform(-30, 30), y, sc * r7.uniform(.9, 1.1), row))
    fig = lambda x, y, sc, r: (f'<g transform="translate({x:.0f} {y:.0f}) scale({sc:.2f})"><g class="f{r % 2}"><circle cx="0" cy="-150" r="30"/>'
                               f'<path d="M-45 -110 Q0 -128 45 -110 L58 60 L-58 60Z"/></g></g>')
    J = s.pages["j"]
    J.append('<div class="full" style="background:linear-gradient(#0a0807 0%,#151009 55%,#0c0906 100%)"></div>'
             '<div id="warm" class="full" style="background:linear-gradient(#3a1406 0%,#7a2c0a 45%,#2a0d04 100%);opacity:0"></div>'
             f'<div id="sun" style="position:absolute;left:190px;top:-760px;width:700px;height:700px;border-radius:50%;'
             f'background:radial-gradient(circle,#fff6d8 0%,#ffd36b 30%,#f29a2e 55%,rgba(242,120,40,0) 72%)"></div>'
             '<svg class="full" viewBox="0 0 1080 1920"><path id="ground" d="M0 1300 L1080 1300 L1080 1920 L0 1920Z" fill="#100c08"/>'
             + "".join(f'<polyline class="ck" points="{c}" fill="none" stroke="{GOLD}" stroke-width="7" stroke-linecap="round" stroke-dasharray="1400" stroke-dashoffset="1400" style="filter:drop-shadow(0 0 14px {GOLD})"/>' for c in cracks) +
             '</svg><div id="heat" class="full" style="opacity:0;background:repeating-linear-gradient(0deg,rgba(255,170,80,0) 0px,rgba(255,170,80,.08) 14px,rgba(255,170,80,0) 28px)"></div>'
             + "".join(f'<div class="dust" style="position:absolute;left:{x:.0f}px;top:{1360 + y * 0.4:.0f}px;width:{r * 1.5:.1f}px;height:{r * 1.5:.1f}px;border-radius:50%;background:rgba(233,185,73,{.4 + .5 * o:.2f});opacity:0"></div>' for x, y, r, o in dust)
             + "".join(f'<svg class="drop" style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;width:{26 * sc:.0f}px;height:{40 * sc:.0f}px;opacity:0" viewBox="0 0 26 40"><path d="M13 0 C13 0 0 18 0 26 A13 13 0 0 0 26 26 C26 18 13 0 13 0Z" fill="rgba(210,235,255,.75)"/></svg>' for x, y, sc in drops)
             + '<svg id="rows" class="full" viewBox="0 0 1080 1920" style="overflow:visible;transform:translateY(700px)"><g fill="#0a0503">' + "".join(fig(*f) for f in figs) + '</g></svg>'
             '<div id="flash" class="full" style="background:#fff3d0;opacity:0"></div>')
    # resurrected: the ground cracks open with light
    s.line([("you're", 20.88, 0), ("resurrected", 21.14, 1)], 330, out=21.95, page="j", k_size=140)
    tr = s.t(21.14)
    s.js += [f'tl.to(".ck", {{strokeDashoffset:0, duration:0.9, ease:"power2.out", stagger:0.06}}, {tr - 0.25:.2f});',
             f'tl.fromTo("#flash", {{opacity:0.55}}, {{opacity:0, duration:0.45, immediateRender:false}}, {tr:.2f});',
             f'tl.fromTo(".dust", {{opacity:0, y:0}}, {{opacity:1, y:-900, duration:2.4, ease:"power2.out", stagger:{{each:0.01, from:"random"}}}}, {tr:.2f});',
             f'tl.fromTo("#cam", {{x:-16}}, {{x:0, duration:0.45, ease:"elastic.out(1,0.3)", immediateRender:false}}, {tr:.2f});']
    # 50,000 years, high on the same page: the number races, a punch on "50" and "thousand", YEARS slams in red
    s.line([("on a day", 21.70, 0), ("that lasts", 22.62, 0)], 220, out=25.95, page="j")
    J.append(f'<div id="ctr" style="position:absolute;left:0;right:0;top:320px;text-align:center;font-family:Anton;font-size:260px;color:{GOLD};line-height:1;opacity:0;text-shadow:0 8px 40px rgba(0,0,0,.6)">0</div>')
    s.line([("years", 24.44, 1)], 610, out=25.95, page="j", k_size=170, color=RED)
    t50, ty = s.t(23.24), s.t(24.44)
    s.js += [f'tl.fromTo("#ctr", {{opacity:0, scale:1.6, filter:"blur(12px)"}}, {{opacity:1, scale:1, filter:"blur(0px)", duration:0.2, ease:"back.out(2)"}}, {t50 - 0.05:.2f});',
             f'(() => {{ const o = {{v:0}}; tl.to(o, {{v:50000, duration:{ty - t50:.2f}, ease:"power2.in", onUpdate:() => {{ document.getElementById("ctr").textContent = Math.round(o.v).toLocaleString("en-GB"); }}}}, {t50:.2f}); }})();']
    for w in (23.24, 23.92):
        s.js.append(f'tl.fromTo("#ctr", {{scale:1.14}}, {{scale:1, duration:0.25, ease:"power2.out", immediateRender:false}}, {s.t(w):.2f});')
    s.js.append(f'tl.to("#ctr", {{opacity:0, y:-120, scale:0.6, filter:"blur(10px)", duration:0.3, ease:"power2.in"}}, {s.t(25.95) - 0.3:.2f});')
    # the sun comes down onto the cracked ground; the sky burns; then the heat and the sweat
    tsun = s.t(26.04)
    s.js += [f'tl.to("#sun", {{y:980, scale:1.35, duration:1.4, ease:"power2.out"}}, {tsun - 0.25:.2f});',
             f'tl.to("#warm", {{opacity:1, duration:1.2, ease:"power2.out"}}, {tsun - 0.2:.2f});',
             f'tl.to(".ck", {{stroke:"#fff1c4", duration:1.0}}, {tsun:.2f});',
             f'tl.to("#heat", {{opacity:1, duration:0.6}}, {s.t(28.16):.2f});',
             f'tl.fromTo("#heat", {{y:0, skewX:0}}, {{y:-60, skewX:2, duration:0.8, ease:"sine.inOut", yoyo:true, repeat:5, immediateRender:false}}, {s.t(28.16):.2f});',
             f'tl.fromTo(".drop", {{y:0, opacity:0}}, {{y:900, opacity:1, duration:2.2, ease:"power1.in", stagger:{{each:0.06, from:"random"}}}}, {s.t(28.86):.2f});']
    s.line([("the", 25.90, 0), ("sun", 26.04, 1), ("is on top", 26.38, 0), ("of your head", 26.96, 0)], 1110, out=28.10, page="j", k_size=150)
    s.line([("it's", 28.16, 0), ("hot", 28.32, 1), ("you're", 28.86, 0), ("sweating", 29.02, 1)], 1110, out=29.62, page="j", k_size=120, color=RED)
    # the crowd rises into the ground: everybody, afraid
    tc = s.t(29.68)
    s.js += [f'tl.to("#rows", {{y:0, duration:0.9, ease:"power3.out"}}, {tc:.2f});',
             f'tl.fromTo("#rows", {{x:50}}, {{x:-50, duration:{s.t(32.6) - tc:.2f}, ease:"none"}}, {tc:.2f});',
             f'tl.fromTo(".f0", {{y:0}}, {{y:-6, duration:0.8, yoyo:true, repeat:3, ease:"sine.inOut"}}, {tc:.2f});']
    s.line([("you look", 29.68, 0), ("around you", 29.92, 0)], 1150, out=30.62, page="j")
    s.line([("everybody", 30.66, 1), ("is", 31.08, 0), ("afraid", 31.50, 1)], 1090, page="j", k_size=130)
    # whip to the dark page: the first thing, the very first thing, questioned about → the hadith, held until "salah"
    F = s.pages["f"]
    F.append('<div class="full" style="background:#030303"></div>'
             '<div class="full" style="background:radial-gradient(ellipse 560px 1100px at 50% 0%,rgba(255,240,200,.2) 0%,rgba(255,240,200,0) 70%)"></div>')
    l1 = s.line([("and the", 32.82, 0), ("first thing", 33.04, 1)], 300, page="f", k_size=150)
    l2 = s.line([("the very", 34.18, 0), ("first thing", 34.88, 1)], 470, page="f", k_size=165, color=RED)
    l3 = s.line([("that you", 36.00, 0), ("are", 36.60, 0), ("questioned", 36.82, 0), ("about", 37.26, 0)], 690, page="f")
    th = s.t(37.75)                                        # the three lines step up, the hadith comes in under them
    s.js += [f'tl.to("#{l1}", {{y:-140, scale:0.75, opacity:0.55, duration:0.4, ease:"power3.inOut"}}, {th:.2f});',
             f'tl.to("#{l2}", {{y:-200, scale:0.8, duration:0.4, ease:"power3.inOut"}}, {th:.2f});',
             f'tl.to("#{l3}", {{y:-240, scale:0.85, opacity:0.75, duration:0.4, ease:"power3.inOut"}}, {th:.2f});']
    qw = "“The first thing a servant will be brought to account for on the Day of Resurrection is the prayer.”".split()
    F.append(f'<div id="hd" style="position:absolute;left:70px;right:70px;top:760px;padding:46px 48px 40px;border-radius:30px;background:rgba(23,38,43,.92);'
             f'box-shadow:0 30px 80px rgba(0,0,0,.6);border:2px solid rgba(233,185,73,.35)">'
             f'<div style="font-family:Anton;font-size:40px;letter-spacing:.12em;color:{GOLD};margin-bottom:18px">THE PROPHET <span class="ar" style="font-size:36px">ﷺ</span> SAID</div>'
             f'<div style="font-family:\'Instrument Serif\';font-size:66px;line-height:1.18;color:{PAPER}">' + " ".join(f'<span class="hw" style="display:inline-block">{w}</span>' for w in qw) + '</div>'
             f'<div id="ref" style="font-family:Anton;font-size:44px;color:{GOLD};margin-top:26px;letter-spacing:.04em">TIRMIDHI 413 · NASA\'I 465</div></div>')
    s.js += [f'tl.fromTo("#hd", {{opacity:0, y:220, filter:"blur(14px)"}}, {{opacity:1, y:0, filter:"blur(0px)", duration:0.45, ease:"power3.out"}}, {th + 0.1:.2f});',
             f'tl.fromTo(".hw", {{opacity:0, y:24, filter:"blur(6px)"}}, {{opacity:1, y:0, filter:"blur(0px)", duration:0.16, ease:"power3.out", stagger:0.055}}, {th + 0.35:.2f});',
             f'tl.fromTo("#ref", {{opacity:0, x:-120}}, {{opacity:1, x:0, duration:0.35, ease:"power3.out"}}, {th + 0.35 + 0.055 * len(qw) + 0.1:.2f});']
    whip(s, "#pj", "#pf", s.t(32.80), axis="x")
    s.write(f'<div class="page" id="pj">{"".join(s.html + J)}</div><div class="page" id="pf" style="transform:translateX(1080px)">{"".join(F)}</div>')

if __name__ == "__main__":
    seq_a(); seq_bc()
