#!/usr/bin/env python3
"""Motion graphics for the owner's "tomorrow people" reel (25 Oct 2026, #292): one silent 1080x1920 clip per moment of the script,
cut in full screen over his talking shots while he keeps talking (as in reels/accountable and reels/salah-20). The beat times
inside each clip are placeholders until his take arrives; then they're set from his word timings and the clips re-rendered.

Nothing depicts a face or the Dajjal: he is his name only. Sources: at-taswīf from sawfa; al-Ḥijr 15:3; the Dajjal the greatest
trial from Adam to the Hour (Muslim 2946); the sun rising from the west, the Dajjal and the Beast, after which faith won't benefit
a soul that didn't believe before (Muslim 158); Ibn ʿUmar's saying (al-Bukhārī 6416).

  python3 brag-quiz/reels/tomorrow/graphics.py [id ...]
  then in each brag-quiz/reels/tomorrow/out/<id>: npx hyperframes render -o ../<id>.mp4
"""
import os, random, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
FONTS = os.path.join(ROOT, "brag-quiz/fonts"); GSAP = os.path.join(ROOT, "brag-output-v6/composition/assets/lib/gsap.min.js")
GOLD, RED, PAPER, INK, TEAL = "#E9B949", "#C8372D", "#F1ECE0", "#17262B", "#2E7263"

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
.ar {{ font-family:Ar; font-weight:700; direction:rtl; }}
.g {{ color:{GOLD}; }} .r {{ color:{RED}; }}
#vig {{ position:absolute; inset:0; pointer-events:none;
       background:radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 45%, rgba(0,0,0,.75) 100%); }}
"""
IN = lambda sel, t, y=30, d=0.5: f'tl.fromTo("{sel}", {{opacity:0, y:{y}, filter:"blur(10px)"}}, {{opacity:1, y:0, filter:"blur(0px)", duration:{d}, ease:"power3.out"}}, {t});'
OUT = lambda sel, t: f'tl.to("{sel}", {{opacity:0, y:-40, filter:"blur(10px)", duration:0.35, ease:"power2.in"}}, {t});'
SLAM = lambda sel, t: (f'tl.fromTo("{sel}", {{opacity:0, scale:1.5}}, {{opacity:1, scale:1, duration:0.3, ease:"power4.out"}}, {t});'
                       f'tl.fromTo("#cam", {{x:-16}}, {{x:0, duration:0.45, ease:"elastic.out(1,0.3)"}}, {t});')

def dots(n, seed, w=1080, h=1920, r=(2, 5)):
    rnd = random.Random(seed)
    return [(rnd.uniform(0, w), rnd.uniform(0, h), rnd.uniform(*r), rnd.random()) for _ in range(n)]

def scene(sid, dur, body, js, vig=True):
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
<div id="cam">{body}</div>{'<div id="vig"></div>' if vig else ''}</div>
<script>const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;</script></body></html>
""")
    print(f"{sid}: {dur}s")

def tomorrow():
    """The hook: a desk calendar whose pages keep flipping, and every page says TOMORROW; the three excuses build up; THE TOMORROW PEOPLE."""
    pages = "".join(f'<div class="pg" id="pg{i}" style="z-index:{10 - i}"><b>SOON</b><i>TOMORROW</i><small>day {i + 1}</small></div>' for i in range(7))
    lines = [("I'll start praying…", 0.5), ("I'll start learning Arabic…", 1.6), ("I'll quit smoking…", 2.7)]
    body = (f'<div class="full" style="background:radial-gradient(ellipse at 50% 30%,#22363d 0%,#0d1619 70%)"></div>'
            f'<style>#cal {{ position:absolute; left:250px; top:260px; width:580px; height:600px; perspective:1800px; }}'
            f'.pg {{ position:absolute; inset:0; background:{PAPER}; border-radius:28px; overflow:hidden; transform-origin:50% 0; box-shadow:0 30px 60px -20px rgba(0,0,0,.7); }}'
            f'.pg b {{ display:block; height:130px; background:{RED}; color:{PAPER}; font-family:Anton; font-size:64px; letter-spacing:.2em; text-align:center; line-height:130px; font-weight:400; }}'
            f'.pg i {{ display:block; font-family:Anton; font-style:normal; font-size:130px; color:{INK}; text-align:center; margin-top:110px; }}'
            f'.pg small {{ display:block; font-family:"Instrument Serif"; font-style:italic; font-size:48px; color:#6b7173; text-align:center; margin-top:40px; }}'
            f'.rings {{ position:absolute; left:250px; top:240px; width:580px; display:flex; justify-content:space-around; z-index:20; }}'
            f'.rings span {{ width:26px; height:60px; border-radius:13px; background:#3a4a50; }}</style>'
            f'<div id="cal">{pages}</div><div class="rings">{"<span></span>" * 6}</div>'
            + "".join(f'<div class="cap ex" id="x{i}" style="top:{990 + i * 120}px;opacity:0">{s} <span class="g">tomorrow.</span></div>' for i, (s, _) in enumerate(lines))
            + f'<div class="big" id="t" style="top:1000px;font-size:200px;color:{GOLD};opacity:0">THE TOMORROW<br><span style="color:{PAPER}">PEOPLE</span></div>')
    flips = [0.6, 1.3, 1.9, 2.4, 2.8, 3.1, 3.35]                    # the pages go faster and faster
    js = [f'tl.to("#pg{i}", {{rotationX:-110, opacity:0, duration:0.35, ease:"power2.in"}}, {t});' for i, t in enumerate(flips[:6])]
    js += [IN(f"#x{i}", t) for i, (_, t) in enumerate(lines)]
    js += [OUT(".ex", 3.6), SLAM("#t", 3.9)]
    scene("t1-tomorrow", 5.5, body, js)

def taswif():
    """The Arabic word: سَوْفَ ("I will… later") grows into التَّسْوِيف, procrastination, its root letters in gold."""
    ps = dots(40, 11, h=1920)
    body = (f'<div class="full" style="background:radial-gradient(ellipse at 50% 40%,#1d2f35 0%,#0b1316 75%)"></div>'
            + "".join(f'<div class="p" style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;width:{r:.1f}px;height:{r:.1f}px;border-radius:50%;background:rgba(233,185,73,{.15 + .4 * o:.2f})"></div>' for x, y, r, o in ps)
            + f'<div class="label" id="k" style="top:300px;font-size:52px;opacity:0">THERE’S A WORD FOR IT</div>'
            f'<div class="big ar" id="sw" style="top:470px;font-size:260px;line-height:1.5;color:{PAPER};opacity:0">سَوْفَ</div>'
            f'<div class="cap" id="swc" style="top:900px;opacity:0"><i>sawfa</i>: “I will… later”</div>'
            f'<div class="big ar" id="ts" style="top:520px;font-size:230px;line-height:1.5;color:{PAPER};opacity:0">التَّسْوِيف</div>'
            f'<div class="big ar" id="rl" style="top:880px;font-size:110px;line-height:1.4;color:{GOLD};letter-spacing:.3em;opacity:0">س و ف</div>'
            f'<div class="big" id="tsl" style="top:1110px;font-size:120px;color:{GOLD};opacity:0">AT-TASWĪF</div>'
            f'<div class="cap" id="tsc" style="top:1260px;opacity:0">procrastination: <i>saying “sawfa”</i></div>')
    js = ['tl.to(".p", {y:-120, duration:5, ease:"none", stagger:{each:0.02, from:"random"}}, 0);',
          IN("#k", 0.1), IN("#sw", 0.3, 0, 0.8), IN("#swc", 1.0),
          OUT("#sw, #swc", 2.0),
          'tl.fromTo("#ts", {opacity:0, scale:0.7, filter:"blur(14px)"}, {opacity:1, scale:1, filter:"blur(0px)", duration:0.7, ease:"expo.out"}, 2.3);',
          IN("#rl", 2.8, 20), IN("#tsl", 3.2), IN("#tsc", 3.6)]
    scene("t2-taswif", 5.0, body, js)

def hijr():
    """Al-Ḥijr 15:3 on a paper page, word by word; فَسَوْفَ يَعْلَمُونَ is swept in gold."""
    words = ["ذَرْهُمْ", "يَأْكُلُوا", "وَيَتَمَتَّعُوا", "وَيُلْهِهِمُ", "الْأَمَلُ", "فَسَوْفَ", "يَعْلَمُونَ"]
    sp = lambda i: f'<span class="w" id="w{i}">{words[i]}</span>'
    ar = f'{sp(0)} {sp(1)} {sp(2)}<br>{sp(3)} {sp(4)}<br><span id="hl">{sp(5)} {sp(6)}</span>'
    body = (f'<div class="full" style="background:radial-gradient(ellipse at 50% 35%,#fbf7ee 0%,{PAPER} 60%,#ddd3bf 100%)"></div>'
            f'<style>.w {{ display:inline-block; opacity:0; position:relative; }} #hl {{ padding:0 24px; border-radius:20px; background:linear-gradient(rgba(233,185,73,.5),rgba(233,185,73,.5)) right / 0% 100% no-repeat; }}</style>'
            f'<div class="label" id="k" style="top:330px;font-size:50px;color:{RED};opacity:0">AL-ḤIJR 15:3</div>'
            f'<div class="ar" style="position:absolute;left:80px;right:80px;top:470px;text-align:center;font-size:92px;line-height:1.7;color:{INK}">{ar}</div>'
            f'<div class="cap" id="en" style="top:1180px;color:{INK};text-shadow:none;opacity:0">“Let them eat and enjoy themselves,<br>distracted by false hope.<br><span style="color:{TEAL}">They will come to know.</span>”</div>')
    js = [IN("#k", 0.1)] + [IN(f"#w{i}", 0.4 + i * 0.32, 20, 0.4) for i in range(len(words))]
    js += ['tl.to("#hl", {backgroundSize:"100% 100%", duration:0.6, ease:"power2.inOut"}, 2.9);', IN("#en", 3.3)]
    scene("t3-hijr", 6.0, body, js, vig=False)

def dajjal():
    """The Dajjal: no figure, only his name in red over a fogged, red-lit horizon; the greatest trial from Adam to the Hour."""
    fog = "".join(f'<div class="fog" style="position:absolute;left:{-400 + i * 300}px;top:{1050 + (i % 3) * 90}px;width:900px;height:260px;border-radius:50%;background:radial-gradient(ellipse,rgba(200,190,180,.16),rgba(200,190,180,0) 70%)"></div>' for i in range(7))
    body = (f'<div class="full" style="background:linear-gradient(#050405 0%,#140707 55%,#2a0a08 72%,#080505 100%)"></div>'
            f'<div id="glow" class="full" style="background:radial-gradient(ellipse at 50% 72%,rgba(200,55,45,.55) 0%,rgba(200,55,45,0) 50%);opacity:0"></div>'
            f'<svg class="full" viewBox="0 0 1080 1920"><path d="M0 1390 L160 1350 L300 1380 L470 1330 L640 1375 L820 1340 L1080 1385 L1080 1920 L0 1920Z" fill="#070505"/></svg>{fog}'
            f'<div class="big ar" id="ar" style="top:560px;font-size:210px;line-height:1.4;color:{RED};opacity:0">الدَّجّال</div>'
            f'<div class="big" id="t" style="top:880px;font-size:130px;color:{PAPER};letter-spacing:.06em;opacity:0">AD-DAJJĀL</div>'
            f'<div class="cap" id="c" style="top:1500px;font-size:52px;opacity:0">the greatest trial from Adam to the Hour<br><span style="font-size:42px;color:{GOLD}">Ṣaḥīḥ Muslim 2946</span></div>')
    js = ['tl.to("#glow", {opacity:1, duration:2.0, ease:"power2.out"}, 0);', 'tl.to(".fog", {x:120, duration:4.5, ease:"none", stagger:0.1}, 0);',
          'tl.fromTo("#ar", {opacity:0, scale:1.15, filter:"blur(20px)"}, {opacity:1, scale:1, filter:"blur(0px)", duration:1.2, ease:"power3.out"}, 0.3);',
          IN("#t", 1.2), IN("#c", 2.2)]
    scene("t4-dajjal", 4.5, body, js)

def sunwest():
    """The sun rises from the west: a pre-dawn horizon with W on the left and E on the right; the sun comes up on the wrong side."""
    st = dots(90, 21, h=1100, r=(1.5, 3.5))
    body = (f'<div id="sky" class="full" style="background:linear-gradient(#03050b 0%,#0b1426 60%,#16213a 100%)"></div>'
            f'<div id="dawn" class="full" style="background:radial-gradient(ellipse at 18% 74%,rgba(255,170,80,.75) 0%,rgba(242,120,40,.35) 28%,rgba(242,120,40,0) 55%);opacity:0"></div>'
            + "".join(f'<div class="st" style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;width:{r:.1f}px;height:{r:.1f}px;border-radius:50%;background:#fff;opacity:{.3 + .6 * o:.2f}"></div>' for x, y, r, o in st)
            + f'<div id="sun" style="position:absolute;left:20px;top:1380px;width:360px;height:360px;border-radius:50%;background:radial-gradient(circle,#fff6d8 0%,#ffd36b 35%,#f29a2e 58%,rgba(242,120,40,0) 72%)"></div>'
            f'<svg class="full" viewBox="0 0 1080 1920"><path d="M0 1420 Q540 1395 1080 1420 L1080 1920 L0 1920Z" fill="#05070c"/></svg>'
            f'<div class="label" id="w" style="left:60px;right:auto;top:1450px;font-size:90px;color:{GOLD}">W</div>'
            f'<div class="label" id="e" style="left:auto;right:60px;top:1450px;font-size:90px;color:#3d4660">E</div>'
            f'<div class="big" id="t1" style="top:430px;font-size:150px;color:{PAPER};opacity:0">THE SUN RISES</div>'
            f'<div class="big" id="t2" style="top:590px;font-size:140px;color:{GOLD};opacity:0">FROM THE WEST</div>')
    js = ['tl.fromTo("#sun", {y:120}, {y:-300, duration:4.5, ease:"power1.out"}, 0.3);', 'tl.to("#dawn", {opacity:1, duration:3.0}, 0.5);',
          'tl.to(".st", {opacity:0.05, duration:3.0}, 1.0);', 'tl.fromTo("#w", {scale:1}, {scale:1.25, duration:0.4, yoyo:true, repeat:3, ease:"sine.inOut"}, 0.8);',
          IN("#t1", 1.6), SLAM("#t2", 2.3)]
    scene("t5-sun-west", 5.0, body, js)

def toolate():
    """Too late: a doorway of light closes, slow then slam; faith won't benefit a soul that didn't believe before (Muslim 158)."""
    body = (f'<div class="full" style="background:linear-gradient(#07090b 0%,#0e1417 100%)"></div>'
            f'<style>#arch {{ position:absolute; left:290px; top:420px; width:500px; height:820px; border-radius:250px 250px 10px 10px; overflow:hidden; background:#0b0f11; border:14px solid #2a3338; }}'
            f'#light {{ position:absolute; inset:0; background:radial-gradient(ellipse at 50% 60%,#fffdf2 0%,#fff1c2 35%,#e9b949 70%,#a8842c 100%); }}'
            f'.lf {{ position:absolute; top:0; height:100%; width:50%; background:{INK}; }} #lL {{ left:0; transform-origin:0 50%; }} #lR {{ right:0; transform-origin:100% 50%; }}</style>'
            f'<div id="spill" style="position:absolute;left:140px;top:1230px;width:800px;height:240px;background:radial-gradient(ellipse,rgba(233,185,73,.45),rgba(233,185,73,0) 70%)"></div>'
            f'<div id="arch"><div id="light"></div><div class="lf" id="lL"></div><div class="lf" id="lR"></div></div>'
            f'<div id="flash" class="full" style="background:#fff3d0;opacity:0"></div>'
            f'<div class="big" id="t" style="top:1310px;font-size:200px;color:{RED};opacity:0">TOO LATE.</div>'
            f'<div class="cap" id="c" style="top:1560px;font-size:50px;opacity:0">“…faith will not benefit a soul<br>that did not believe before.”<br><span style="font-size:40px;color:{GOLD}">Ṣaḥīḥ Muslim 158</span></div>')
    js = ['tl.fromTo(["#lL", "#lR"], {scaleX:0.05}, {scaleX:0.6, duration:1.4, ease:"sine.in"}, 0.3);',
          'tl.to(["#lL", "#lR"], {scaleX:1, duration:0.18, ease:"power4.in"}, 1.7);', 'tl.to("#spill", {opacity:0, duration:0.3}, 1.75);',
          'tl.to("#flash", {opacity:0.35, duration:0.06}, 1.88);', 'tl.to("#flash", {opacity:0, duration:0.5}, 1.94);',
          SLAM("#t", 1.9), IN("#c", 2.7)]
    scene("t6-too-late", 5.0, body, js)

def graves():
    """The graveyard is full of people who said "I'll start tomorrow": rows of headstones at night, each one engraved TOMORROW."""
    rows, stones = [(1000, 0.55, 8), (1230, 1.0, 4), (1620, 1.9, 2)], ""
    for r, (y, s, n) in enumerate(rows):
        w = 1080 / n
        for i in range(n):
            x = w * i + w / 2 + (w / 4 if r == 1 else 0) - 90 * s; txt = "I'LL START<br>TOMORROW" if (r == 2 and i == 1) else "TOMORROW"
            x = min(x, 1080 - 180 * s + 60)
            stones += (f'<div class="gs r{r}" style="left:{x:.0f}px;top:{y - 260 * s:.0f}px;width:{180 * s:.0f}px;height:{260 * s:.0f}px;font-size:{30 * s:.0f}px;z-index:{r}">'
                       f'<span>{txt}</span></div>')
    fog = "".join(f'<div class="fog" style="position:absolute;left:{-300 + i * 260}px;top:{1000 + (i % 3) * 140}px;width:800px;height:220px;border-radius:50%;background:radial-gradient(ellipse,rgba(190,205,215,.13),rgba(190,205,215,0) 70%)"></div>' for i in range(7))
    body = (f'<div class="full" style="background:linear-gradient(#03050a 0%,#0b1220 55%,#151c26 100%)"></div>'
            f'<div style="position:absolute;left:720px;top:230px;width:170px;height:170px;border-radius:50%;background:radial-gradient(circle,#f6f1e1 0%,#e8e0c8 60%,rgba(232,224,200,0) 72%);box-shadow:0 0 120px 40px rgba(246,241,225,.15)"></div>'
            f'<style>.gs {{ position:absolute; border-radius:46% 46% 6px 6px / 30% 30% 6px 6px; background:linear-gradient(#5d666c,#3a4247); box-shadow:inset -8px 0 0 rgba(0,0,0,.25);'
            f' display:flex; align-items:center; justify-content:center; text-align:center; font-family:Anton; color:rgba(225,230,232,.55); letter-spacing:.05em; line-height:1.1; text-shadow:0 -2px 0 rgba(0,0,0,.5); }}</style>'
            f'<svg class="full" viewBox="0 0 1080 1920"><path d="M0 900 Q540 860 1080 900 L1080 1920 L0 1920Z" fill="#0a0d12"/></svg>{stones}{fog}')
    js = ['tl.to(".fog", {x:100, duration:5.5, ease:"none", stagger:0.1}, 0);']
    js += [f'tl.fromTo(".r{r}", {{y:80, opacity:0}}, {{y:0, opacity:1, duration:0.8, ease:"power3.out", stagger:0.07}}, {0.2 + r * 0.6});' for r in range(3)]
    scene("t7-graves", 5.5, body, js)

def ibnumar():
    """Ibn ʿUmar: evening falls (don't wait for the morning), then morning comes (don't wait for the evening). Al-Bukhārī 6416."""
    body = (f'<div id="eve" class="full" style="background:linear-gradient(#1a1030 0%,#5a2a3a 45%,#d9773a 75%,#2a1810 100%)"></div>'
            f'<div id="morn" class="full" style="background:linear-gradient(#7fb3d9 0%,#cfe3ee 50%,#f6e3a8 78%,#3a3020 100%);opacity:0"></div>'
            f'<div id="sun" style="position:absolute;left:390px;top:1000px;width:300px;height:300px;border-radius:50%;background:radial-gradient(circle,#fff6d8 0%,#ffd36b 38%,#f29a2e 60%,rgba(242,120,40,0) 72%)"></div>'
            f'<svg class="full" viewBox="0 0 1080 1920"><path d="M0 1300 Q540 1270 1080 1300 L1080 1920 L0 1920Z" fill="#0d0b0a"/></svg>'
            f'<div class="label" id="k" style="top:300px;font-size:50px;opacity:0">IBN ʿUMAR SAID</div>'
            f'<div class="cap" id="c1" style="top:430px;font-size:76px;opacity:0">“When evening comes,<br>don’t wait for the <span class="g">morning.</span>”</div>'
            f'<div class="cap" id="c2" style="top:430px;font-size:76px;color:{INK};text-shadow:none;opacity:0">“When morning comes,<br>don’t wait for the <span style="color:{RED}">evening.</span>”</div>'
            f'<div class="cap" id="ref" style="top:1500px;font-size:44px;color:{GOLD};opacity:0">Ṣaḥīḥ al-Bukhārī 6416</div>')
    js = [IN("#k", 0.1), IN("#c1", 0.4), 'tl.to("#sun", {y:420, duration:2.6, ease:"power1.in"}, 0.2);', OUT("#c1", 2.9),
          'tl.to("#morn", {opacity:1, duration:0.8}, 3.0);', 'tl.to("#sun", {y:-250, duration:2.8, ease:"power2.out"}, 3.0);',
          'tl.to("#k", {color:"#a8842c", duration:0.5}, 3.0);', IN("#c2", 3.3), IN("#ref", 4.2)]
    scene("t8-ibn-umar", 6.5, body, js)

def today():
    """The ending: the TOMORROW page tears off the calendar; TODAY underneath; START NOW."""
    body = (f'<div class="full" style="background:radial-gradient(ellipse at 50% 35%,#fbf7ee 0%,{PAPER} 60%,#ddd3bf 100%)"></div>'
            f'<style>.pg {{ position:absolute; left:250px; top:330px; width:580px; height:600px; background:#fff; border-radius:28px; overflow:hidden; box-shadow:0 30px 60px -24px rgba(23,38,43,.45); }}'
            f'.pg b {{ display:block; height:130px; color:{PAPER}; font-family:Anton; font-size:64px; letter-spacing:.2em; text-align:center; line-height:130px; font-weight:400; }}'
            f'.pg i {{ display:block; font-family:Anton; font-style:normal; font-size:150px; text-align:center; margin-top:120px; }}'
            f'#top {{ transform-origin:15% 0; }}</style>'
            f'<div class="pg" id="under"><b style="background:{TEAL}">NOW</b><i style="color:{TEAL}">TODAY</i></div>'
            f'<div class="pg" id="top"><b style="background:{RED}">SOON</b><i style="color:{INK}">TOMORROW</i></div>'
            f'<div class="big" id="t" style="top:1120px;font-size:190px;color:{INK};opacity:0">START <span style="color:{RED}">NOW.</span></div>')
    js = ['tl.to("#top", {rotation:-14, duration:0.25, ease:"power2.out"}, 0.8);',
          'tl.to("#top", {rotation:-60, y:1400, x:-260, opacity:0, duration:0.9, ease:"power2.in"}, 1.05);',
          'tl.fromTo("#under i", {scale:0.9}, {scale:1.08, duration:0.18, yoyo:true, repeat:1, ease:"power2.out"}, 1.35);', SLAM("#t", 2.2)]
    scene("t9-today", 4.5, body, js, vig=False)

ALL = {"t1-tomorrow": tomorrow, "t2-taswif": taswif, "t3-hijr": hijr, "t4-dajjal": dajjal, "t5-sun-west": sunwest,
       "t6-too-late": toolate, "t7-graves": graves, "t8-ibn-umar": ibnumar, "t9-today": today}
if __name__ == "__main__":
    for k in (sys.argv[1:] or ALL): ALL[k]()
