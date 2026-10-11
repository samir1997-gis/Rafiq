#!/usr/bin/env python3
"""Motion graphics for the owner's "first thing you're asked about" reel (10 Oct 2026): one silent 1080x1920 clip per
moment of the script, cut in over his talking shots by the reel template (which adds the sound effects).

Nothing depicts the angels or a face: the grave is its three questions, the gathering is anonymous silhouettes.
Sources: the grave questions (Abu Dawud 4753), a day of 50,000 years (Qur'an 70:4), the sun a mile away and the sweat
(Muslim 2864), the first thing asked about (Tirmidhi 413, Nasa'i 465), 20 words = 56% of a four-rak'ah prayer without
the surah (salah-data.js with salah.js REPS).

  python3 brag-quiz/reels/accountable/graphics.py [id ...]
  then in each brag-quiz/reels/accountable/out/<id>: npx hyperframes render -o ../<id>.mp4
"""
import os, random, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
FONTS = os.path.join(ROOT, "brag-quiz/fonts"); GSAP = os.path.join(ROOT, "brag-output-v6/composition/assets/lib/gsap.min.js")
GOLD, RED, PAPER, INK = "#E9B949", "#C8372D", "#F1ECE0", "#17262B"

CSS = f"""
@font-face {{ font-family:"Anton"; src:url("assets/anton-latin-400-normal.woff2"); }}
@font-face {{ font-family:"Instrument Serif"; src:url("assets/instrument-serif-latin-400-normal.woff2"); }}
@font-face {{ font-family:"Ar"; src:url("assets/ibm-plex-sans-arabic-arabic-700-normal.woff2"); font-weight:700; }}
body {{ margin:0; background:#000; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; background:#000; }}
#cam {{ position:absolute; inset:0; transform-origin:50% 45%; }}
.full {{ position:absolute; inset:0; }}
.label {{ position:absolute; left:0; right:0; text-align:center; font-family:Anton; letter-spacing:.08em; color:{GOLD}; }}
.big {{ position:absolute; left:0; right:0; text-align:center; font-family:Anton; line-height:.95; text-transform:uppercase; }}
.cap {{ position:absolute; left:90px; right:90px; text-align:center; font-family:"Instrument Serif"; color:#fff; font-size:64px;
       line-height:1.2; text-shadow:0 4px 24px rgba(0,0,0,.8); }}
.ar {{ font-family:Ar; font-weight:700; }}
#vig {{ position:absolute; inset:0; pointer-events:none;
       background:radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 45%, rgba(0,0,0,.75) 100%); }}
"""

def dots(n, seed, w=1080, h=1920, r=(2, 5), cls="p", color="#fff"):
    rnd = random.Random(seed)
    return [(rnd.uniform(0, w), rnd.uniform(0, h), rnd.uniform(*r), rnd.random()) for _ in range(n)]

def scene(sid, dur, body, js):
    out = os.path.join(HERE, "out", sid); a = os.path.join(out, "assets")
    if os.path.exists(out): shutil.rmtree(out)
    os.makedirs(a)
    for f in os.listdir(FONTS): shutil.copy(os.path.join(FONTS, f), a)
    shutil.copy(GSAP, a)
    js = [f'tl.fromTo("#cam", {{scale:1}}, {{scale:1.07, duration:{dur}, ease:"none"}}, 0);'] + js   # a slow push-in throughout
    open(os.path.join(out, "index.html"), "w").write(f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<title>{sid}</title><script src="assets/gsap.min.js"></script><style>{CSS}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{dur}">
<div id="cam">{body}</div><div id="vig"></div></div>
<script>const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;</script></body></html>
""")
    print(f"{sid}: {dur}s")

def grave():
    """After death: the grave at night, a column of light, the three questions."""
    ps = dots(45, 1, h=1300)
    body = (f'<div class="full" style="background:linear-gradient(#06080c 0%,#0f1318 60%,#1a1612 100%)"></div>'
            f'<div id="beam" class="full" style="background:linear-gradient(90deg,transparent 40%,rgba(233,185,73,.16) 50%,transparent 60%);opacity:0"></div>'
            + "".join(f'<div class="p" style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;width:{r:.1f}px;height:{r:.1f}px;border-radius:50%;background:rgba(233,185,73,{.25 + .5 * o:.2f})"></div>' for x, y, r, o in ps) +
            f'<svg class="full" viewBox="0 0 1080 1920"><path d="M0 1380 Q540 1300 1080 1380 L1080 1920 L0 1920Z" fill="#0b0907"/>'
            f'<ellipse cx="540" cy="1395" rx="330" ry="70" fill="#17120d"/><ellipse id="glow" cx="540" cy="1380" rx="260" ry="40" fill="rgba(233,185,73,.25)" opacity="0"/></svg>'
            f'<div class="label" style="top:240px;font-size:54px">THE GRAVE</div>'
            + "".join(f'<div class="cap q" id="q{i}" style="top:{560 + i * 150}px;opacity:0">{q}</div>' for i, q in
                      enumerate(["Who is your Lord?", "What is your religion?", "Who is your Prophet?"])))
    js = ['tl.to("#beam", {opacity:1, duration:1.6, ease:"power2.out"}, 0.2);', 'tl.to("#glow", {opacity:1, duration:1.6}, 0.4);',
          'tl.fromTo(".label", {opacity:0, letterSpacing:"0.3em"}, {opacity:1, letterSpacing:"0.08em", duration:1.0, ease:"power3.out"}, 0.1);',
          'tl.to(".p", {y:-140, duration:5, ease:"none", stagger:{each:0.02, from:"random"}}, 0);']
    js += [f'tl.fromTo("#q{i}", {{opacity:0, y:20, filter:"blur(8px)"}}, {{opacity:1, y:0, filter:"blur(0px)", duration:0.6, ease:"power3.out"}}, {0.9 + i * 1.1:.1f});' for i in range(3)]
    scene("g1-grave", 5.0, body, js)

def barzakh():
    """Waiting in the barzakh: stars turning slowly over a dim horizon, time passing."""
    st = dots(170, 2, w=2200, h=2200, r=(1.5, 4))
    body = (f'<div class="full" style="background:linear-gradient(#020306 0%,#070b14 65%,#141620 100%)"></div>'
            f'<div id="sky" style="position:absolute;left:-560px;top:-700px;width:2200px;height:2200px;transform-origin:50% 50%">'
            + "".join(f'<div style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;width:{r:.1f}px;height:{r:.1f}px;border-radius:50%;background:#fff;opacity:{.3 + .7 * o:.2f}"></div>' for x, y, r, o in st) +
            f'</div><div class="full" style="top:1300px;background:linear-gradient(rgba(233,185,73,0) 0%,rgba(233,185,73,.10) 8%,#08080b 30%)"></div>'
            f'<div id="arz" class="big ar" lang="ar" style="top:700px;font-size:230px;color:rgba(241,236,224,.9)">البَرْزَخ</div>'
            f'<div class="label" style="top:1060px;font-size:58px">AL-BARZAKH</div>'
            f'<div class="cap" id="c" style="top:1180px;opacity:0">between this life and the next</div>')
    js = ['tl.to("#sky", {rotation:14, duration:5.5, ease:"none"}, 0);',
          'tl.fromTo("#arz", {opacity:0, scale:1.08, filter:"blur(14px)"}, {opacity:1, scale:1, filter:"blur(0px)", duration:1.4, ease:"power3.out"}, 0.3);',
          'tl.fromTo(".label", {opacity:0}, {opacity:1, duration:0.8}, 1.2);', 'tl.to("#c", {opacity:1, duration:0.8}, 2.0);']
    scene("g2-barzakh", 5.5, body, js)

def resurrection():
    """The Day comes: the ground cracks with light, dust rises, RESURRECTED lands."""
    rnd = random.Random(3); cracks = []
    for k in range(7):                                    # jagged lines out from the centre of the ground
        x, y, pts = 540, 1450, []
        ang = -2.9 + k * 0.9 + rnd.uniform(-.2, .2)
        for _ in range(9):
            x += 60 * __import__("math").cos(ang) + rnd.uniform(-25, 25); y += 22 * __import__("math").sin(ang) + rnd.uniform(-18, 18); pts.append(f"{x:.0f},{y:.0f}")
        cracks.append("540,1450 " + " ".join(pts))
    ps = dots(60, 4, h=600)
    body = (f'<div class="full" style="background:linear-gradient(#0a0807 0%,#151009 55%,#0c0906 100%)"></div>'
            f'<svg class="full" viewBox="0 0 1080 1920"><path d="M0 1250 L1080 1250 L1080 1920 L0 1920Z" fill="#100c08"/>'
            + "".join(f'<polyline class="ck" points="{c}" fill="none" stroke="{GOLD}" stroke-width="7" stroke-linecap="round" stroke-dasharray="1400" stroke-dashoffset="1400" style="filter:drop-shadow(0 0 14px {GOLD})"/>' for c in cracks) +
            f'</svg><div id="flash" class="full" style="background:#fff3d0;opacity:0"></div>'
            + "".join(f'<div class="dust" style="position:absolute;left:{x:.0f}px;top:{1320 + y * 0.4:.0f}px;width:{r * 1.5:.1f}px;height:{r * 1.5:.1f}px;border-radius:50%;background:rgba(233,185,73,{.4 + .5 * o:.2f});opacity:0"></div>' for x, y, r, o in ps) +
            f'<div id="t" class="big" style="top:520px;font-size:190px;color:{GOLD};opacity:0">RESUR&shy;RECTED</div>')
    js = ['tl.to(".ck", {strokeDashoffset:0, duration:1.4, ease:"power2.in", stagger:0.08}, 0.3);',
          'tl.to("#flash", {opacity:0.5, duration:0.08}, 2.2);', 'tl.to("#flash", {opacity:0, duration:0.6}, 2.3);',
          'tl.fromTo(".dust", {opacity:0, y:0}, {opacity:1, y:-900, duration:2.2, ease:"power2.out", stagger:{each:0.01, from:"random"}}, 2.2);',
          'tl.fromTo("#t", {opacity:0, scale:1.4}, {opacity:1, scale:1, duration:0.35, ease:"power4.out"}, 2.25);',
          'tl.fromTo("#cam", {x:-14}, {x:0, duration:0.4, ease:"elastic.out(1,0.3)"}, 2.25);']
    scene("g3-resurrection", 4.5, body, js)

def years():
    """A day that lasts 50,000 years: the number counts up."""
    body = (f'<div class="full" style="background:radial-gradient(ellipse at 50% 30%,#3a1c0c 0%,#120806 60%,#050303 100%)"></div>'
            f'<div class="label" style="top:520px;font-size:64px">ONE DAY</div>'
            f'<div id="n" class="big" style="top:640px;font-size:300px;color:{GOLD}">0</div>'
            f'<div id="y" class="big" style="top:960px;font-size:170px;color:{RED};opacity:0">YEARS</div>'
            f'<div class="cap" id="c" style="top:1260px;opacity:0;font-size:52px">Qurʾān 70:4</div>')
    js = ['const o = {v:0};',
          'tl.to(o, {v:50000, duration:2.4, ease:"power2.inOut", onUpdate:()=>{document.getElementById("n").textContent = Math.round(o.v).toLocaleString("en-GB");}}, 0.4);',
          'tl.fromTo(".label", {opacity:0}, {opacity:1, duration:0.6}, 0.1);',
          'tl.fromTo("#y", {opacity:0, y:40}, {opacity:1, y:0, duration:0.4, ease:"power3.out"}, 2.8);',
          'tl.fromTo("#n", {scale:1}, {scale:1.06, duration:0.15, yoyo:true, repeat:1}, 2.8);', 'tl.to("#c", {opacity:1, duration:0.6}, 3.1);']
    scene("g4-50000-years", 4.5, body, js)

def sun():
    """The sun brought a mile away; heat shimmer; sweat falling."""
    rnd = random.Random(5); drops = [(rnd.uniform(60, 1020), rnd.uniform(-300, 900), rnd.uniform(.6, 1.2)) for _ in range(26)]
    body = (f'<div class="full" style="background:linear-gradient(#2a0d04 0%,#6b2508 45%,#1a0904 100%)"></div>'
            f'<div id="sun" style="position:absolute;left:190px;top:-200px;width:700px;height:700px;border-radius:50%;'
            f'background:radial-gradient(circle,#fff6d8 0%,#ffd36b 30%,#f29a2e 55%,rgba(242,120,40,0) 72%)"></div>'
            f'<div id="heat" class="full" style="background:repeating-linear-gradient(0deg,rgba(255,170,80,.0) 0px,rgba(255,170,80,.07) 14px,rgba(255,170,80,0) 28px)"></div>'
            + "".join(f'<svg class="drop" style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;width:{26 * s:.0f}px;height:{40 * s:.0f}px" viewBox="0 0 26 40"><path d="M13 0 C13 0 0 18 0 26 A13 13 0 0 0 26 26 C26 18 13 0 13 0Z" fill="rgba(210,235,255,.75)"/></svg>' for x, y, s in drops) +
            f'<div class="big" id="t1" style="top:1150px;font-size:150px;color:{GOLD};opacity:0">THE SUN</div>'
            f'<div class="big" id="t2" style="top:1300px;font-size:120px;color:#fff;opacity:0">A MILE AWAY</div>'
            f'<div class="cap" id="c" style="top:1470px;opacity:0;font-size:48px">Ṣaḥīḥ Muslim 2864</div>')
    js = ['tl.fromTo("#sun", {y:-300, scale:0.6}, {y:420, scale:1.5, duration:4.6, ease:"power1.out"}, 0);',
          'tl.fromTo("#heat", {y:0, skewX:0}, {y:-60, skewX:2, duration:1.2, ease:"sine.inOut", yoyo:true, repeat:4}, 0);',
          'tl.fromTo(".drop", {y:0, opacity:0}, {y:900, opacity:1, duration:2.6, ease:"power1.in", stagger:{each:0.08, from:"random"}}, 1.0);',
          'tl.fromTo("#t1", {opacity:0, y:30}, {opacity:1, y:0, duration:0.4, ease:"power3.out"}, 1.2);',
          'tl.fromTo("#t2", {opacity:0, y:30}, {opacity:1, y:0, duration:0.4, ease:"power3.out"}, 1.8);', 'tl.to("#c", {opacity:1, duration:0.6}, 2.4);']
    scene("g5-sun", 5.0, body, js)

def crowd():
    """All of humanity gathered on one plain, afraid: rows of anonymous silhouettes in the heat."""
    rnd = random.Random(6); figs = []
    for row in range(7):                                  # far rows small and high, near rows big and low
        s = 0.35 + row * 0.18; y = 980 + row * 120; n = int(26 - row * 2.5)
        for i in range(n):
            x = -200 + i * (1500 / n) + rnd.uniform(-30, 30)
            figs.append((x, y, s * rnd.uniform(.9, 1.1), row))
    fig = lambda x, y, s, r: (f'<g transform="translate({x:.0f} {y:.0f}) scale({s:.2f})"><g class="f{r % 2}"><circle cx="0" cy="-150" r="30"/>'
                               f'<path d="M-45 -110 Q0 -128 45 -110 L58 60 L-58 60Z"/></g></g>')   # sway on the inner group, so GSAP keeps the placement
    body = (f'<div class="full" style="background:linear-gradient(#5a2209 0%,#2a1006 50%,#0d0604 100%)"></div>'
            f'<div class="full" style="background:radial-gradient(circle at 50% 8%,rgba(255,214,120,.55) 0%,rgba(255,150,60,0) 40%)"></div>'
            f'<svg id="rows" class="full" viewBox="0 0 1080 1920" style="overflow:visible"><g fill="#0a0503">'
            + "".join(fig(*f) for f in figs) + f'</g></svg>'
            f'<div class="big" id="t" style="top:360px;font-size:130px;color:{GOLD};opacity:0">ALL OF<br>HUMANITY</div>'
            f'<div class="cap" id="c" style="top:640px;opacity:0">everyone you see, afraid</div>')
    js = ['tl.fromTo("#rows", {x:60}, {x:-60, duration:5, ease:"none"}, 0);',
          'tl.fromTo(".f0", {y:0}, {y:-5, duration:0.9, yoyo:true, repeat:5, ease:"sine.inOut"}, 0);',
          'tl.fromTo(".f1", {y:-5}, {y:0, duration:1.1, yoyo:true, repeat:4, ease:"sine.inOut"}, 0);',
          'tl.fromTo("#t", {opacity:0, y:30}, {opacity:1, y:0, duration:0.5, ease:"power3.out"}, 0.6);', 'tl.to("#c", {opacity:1, duration:0.8}, 1.6);']
    scene("g6-crowd", 5.0, body, js)

def first():
    """And the first thing you're asked about: your salah."""
    body = (f'<div class="full" style="background:#030303"></div>'
            f'<div id="spot" class="full" style="background:radial-gradient(ellipse 520px 1100px at 50% 0%,rgba(255,240,200,.22) 0%,rgba(255,240,200,0) 70%);opacity:0"></div>'
            f'<div class="big" id="a" style="top:420px;font-size:110px;color:#fff;opacity:0">THE FIRST THING</div>'
            f'<div class="big" id="b" style="top:540px;font-size:110px;color:#fff;opacity:0">YOU\'RE ASKED ABOUT</div>'
            f'<div class="big ar" id="s" lang="ar" style="top:760px;font-size:300px;color:{RED};opacity:0;text-shadow:0 0 60px rgba(200,55,45,.6)">الصَّلاة</div>'
            f'<div class="cap" id="c" style="top:1250px;opacity:0">your salah</div>')
    js = ['tl.to("#spot", {opacity:1, duration:1.0}, 0);',
          'tl.fromTo("#a", {opacity:0, y:20}, {opacity:1, y:0, duration:0.4, ease:"power3.out"}, 0.3);',
          'tl.fromTo("#b", {opacity:0, y:20}, {opacity:1, y:0, duration:0.4, ease:"power3.out"}, 0.9);',
          'tl.fromTo("#s", {opacity:0, scale:1.3, filter:"blur(10px)"}, {opacity:1, scale:1, filter:"blur(0px)", duration:0.5, ease:"power4.out"}, 1.8);',
          'tl.to("#c", {opacity:1, duration:0.6}, 2.5);']
    scene("g7-first-question", 4.5, body, js)

def hadith():
    """The hadith, word by word on a dark card, then its reference."""
    words = "“The first thing a servant will be brought to account for on the Day of Resurrection is the prayer.”".split()
    body = (f'<div class="full" style="background:radial-gradient(ellipse at 50% 40%,#1c1a16 0%,#070706 75%)"></div>'
            f'<div class="label" style="top:470px;font-size:50px">THE PROPHET ﷺ SAID</div>'.replace("ﷺ", '<span class="ar" style="font-size:40px">ﷺ</span>') +
            f'<div class="cap" style="top:620px;font-size:78px;line-height:1.25">' + " ".join(f'<span class="w" style="opacity:0">{w}</span>' for w in words) + '</div>'
            f'<div class="cap" id="r" style="top:1360px;font-size:46px;color:{GOLD};opacity:0">Tirmidhi 413 · Nasāʾī 465</div>')
    js = ['tl.fromTo(".label", {opacity:0}, {opacity:1, duration:0.5}, 0.1);',
          'tl.to(".w", {opacity:1, duration:0.25, stagger:0.16}, 0.5);', f'tl.to("#r", {{opacity:1, duration:0.6}}, {0.5 + 0.16 * len(words) + 0.3:.2f});']
    scene("g8-hadith", round(0.5 + 0.16 * len(words) + 2.2, 1), body, js)

def twenty():
    """20 words make up more than half: 425 squares (every word of a four-rak'ah prayer, no surah), 238 light up."""
    cols, sq, gap = 25, 34, 8; x0 = (1080 - cols * (sq + gap) + gap) // 2
    cells = "".join(f'<div class="c{" on" if i < 238 else ""}" style="position:absolute;left:{x0 + (i % cols) * (sq + gap)}px;top:{560 + (i // cols) * (sq + gap)}px;width:{sq}px;height:{sq}px;border-radius:9px;background:rgba(241,236,224,.10)"></div>' for i in range(425))
    body = (f'<div class="full" style="background:#0b0d0f"></div>'
            f'<div class="big" id="t" style="top:250px;font-size:150px;color:{GOLD}">20 WORDS</div>' + cells +
            f'<div class="big" id="p" style="top:1360px;font-size:200px;color:#fff;opacity:0">56%</div>'
            f'<div class="big" id="m" style="top:1570px;font-size:90px;color:{RED};opacity:0">MORE THAN HALF</div>')
    js = ['tl.fromTo("#t", {opacity:0, y:20}, {opacity:1, y:0, duration:0.4, ease:"power3.out"}, 0.1);',
          'tl.fromTo(".c", {opacity:0}, {opacity:1, duration:0.4, stagger:0.0015}, 0.2);',
          f'tl.to(".on", {{backgroundColor:"{GOLD}", duration:0.2, stagger:0.006}}, 1.1);',
          'tl.fromTo("#p", {opacity:0, scale:1.3}, {opacity:1, scale:1, duration:0.35, ease:"power4.out"}, 2.6);',
          'tl.fromTo("#m", {opacity:0, y:20}, {opacity:1, y:0, duration:0.4, ease:"power3.out"}, 3.0);']
    scene("g9-twenty-words", 5.0, body, js)

ALL = {"g1-grave": grave, "g2-barzakh": barzakh, "g3-resurrection": resurrection, "g4-50000-years": years, "g5-sun": sun,
       "g6-crowd": crowd, "g7-first-question": first, "g8-hadith": hadith, "g9-twenty-words": twenty}
if __name__ == "__main__":
    for k, fn in ALL.items():
        if len(sys.argv) < 2 or k in sys.argv[1:]: fn()
