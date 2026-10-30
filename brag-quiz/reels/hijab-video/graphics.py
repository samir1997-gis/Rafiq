#!/usr/bin/env python3
"""Motion graphics for the owner's hijab video (30 Oct 2026, #307): one silent 1080x1920 clip per moment, cut in full screen over his
talking shots while he keeps talking (as reels/tomorrow). Every beat is placed from his own words in his take (TIMES: when each graphic
starts and ends in the take, its beats in take seconds), so the same clips serve all three versions. Every ayah he mentions is on screen in
Arabic and English with its reference (the text from api.quran.com, imlaei script; the English after Sahih International). Faceless figures
(owner, 27 Oct). Easing as MOTION-STYLE.md: entrances ease out, exits ease in, pops spring with a slight overshoot, nothing linear.

  python3 brag-quiz/reels/hijab-video/graphics.py [id ...]     → brag-quiz/reels/hijab-video/out/<id>/ ; then render each to out/<id>.mp4
"""
import os, random, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
FONTS = os.path.join(ROOT, "brag-quiz/fonts"); GSAP = os.path.join(ROOT, "brag-output-v6/composition/assets/lib/gsap.min.js")
GOLD, RED, PAPER, INK, TEAL, SKIN = "#E9B949", "#C8372D", "#F1ECE0", "#17262B", "#2E7263", "#c99a73"

CSS = f"""
@font-face {{ font-family:"Anton"; src:url("assets/anton-latin-400-normal.woff2"); }}
@font-face {{ font-family:"Serif"; src:url("assets/instrument-serif-latin-400-normal.woff2"); }}
@font-face {{ font-family:"Am"; src:url("assets/amiri-arabic-700-normal.woff2"); }}
body {{ margin:0; background:#000; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; background:radial-gradient(ellipse at 50% 38%, #24414a 0%, #14232a 55%, #0b1418 100%); }}
#cam {{ position:absolute; inset:0; transform-origin:50% 40%; }}
.full {{ position:absolute; left:0; top:0; width:1080px; height:1920px; overflow:visible; }}
.big {{ position:absolute; left:0; right:0; text-align:center; font-family:Anton; line-height:.95; text-transform:uppercase; color:{PAPER}; opacity:0; }}
.ar {{ position:absolute; left:0; right:0; text-align:center; font-family:Am; direction:rtl; color:{PAPER}; line-height:1.35; opacity:0; text-shadow:0 8px 30px rgba(0,0,0,.6); }}
.g {{ color:{GOLD}; }} .r {{ color:{RED}; }}
.card {{ position:absolute; left:70px; right:70px; padding:26px 34px 22px; border-radius:26px; background:rgba(241,236,224,.96); color:{INK}; text-align:center; opacity:0;
  box-shadow:0 30px 60px rgba(0,0,0,.5), inset 0 0 0 4px rgba(233,185,73,.9); }}
.card .a {{ font-family:Am; font-size:68px; direction:rtl; line-height:1.55; }} .card .a b {{ color:{TEAL}; font-weight:700; background:rgba(233,185,73,.35); border-radius:10px; padding:0 6px; }}
.card .e {{ font-family:Serif; font-size:44px; line-height:1.2; margin-top:6px; }} .card .e i {{ color:{TEAL}; }}
.card .ref {{ display:inline-block; margin-top:14px; padding:6px 22px; border-radius:30px; background:{INK}; color:{GOLD}; font-family:Anton; font-size:30px; letter-spacing:.06em; }}
.card .note {{ font-family:Serif; font-size:30px; color:#5c6e70; margin-top:6px; }}
.bub {{ position:absolute; padding:10px 28px; border-radius:40px; background:{PAPER}; color:{INK}; font-family:Anton; font-size:58px; opacity:0; box-shadow:0 14px 30px rgba(0,0,0,.45); }}
.bub.r {{ background:{RED}; color:#fff; }}
#vig {{ position:absolute; inset:0; pointer-events:none; background:radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 50%, rgba(0,0,0,.7) 100%); }}
"""
IN = lambda sel, t, y=40, d=0.5: f'tl.fromTo("{sel}", {{opacity:0, y:{y}}}, {{opacity:1, y:0, duration:{d}, ease:"power3.out"}}, {t:.2f});'
POP = lambda sel, t, s=0.6: f'tl.fromTo("{sel}", {{opacity:0, scale:{s}}}, {{opacity:1, scale:1, duration:0.45, ease:"back.out(1.4)"}}, {t:.2f});'
OUT = lambda sel, t: f'tl.to("{sel}", {{opacity:0, y:-40, duration:0.3, ease:"power2.in"}}, {t:.2f});'
SLAM = lambda sel, t: (f'tl.fromTo("{sel}", {{opacity:0, scale:1.6}}, {{opacity:1, scale:1, duration:0.4, ease:"back.out(1.7)"}}, {t:.2f});'
                       f'tl.fromTo("#cam", {{x:-14}}, {{x:14, duration:0.05, yoyo:true, repeat:5, ease:"sine.inOut", immediateRender:false}}, {t:.2f});'
                       f'tl.set("#cam", {{x:0}}, {t + 0.32:.2f});')
DRAW = lambda sel, t, d=0.7: f'tl.fromTo("{sel}", {{strokeDashoffset:1}}, {{strokeDashoffset:0, duration:{d}, ease:"power2.inOut"}}, {t:.2f});'

def card(id, ar, en, ref, top, note=""):
    return (f'<div class="card" id="{id}" style="top:{top}px"><div class="a">{ar}</div><div class="e">{en}</div>'
            + (f'<div class="note">{note}</div>' if note else "") + f'<span class="ref">{ref}</span></div>')
def stars(seed, n=70):
    r = random.Random(seed)
    return "".join(f'<circle cx="{r.uniform(0, 1080):.0f}" cy="{r.uniform(0, 1100):.0f}" r="{r.uniform(1, 3):.1f}" fill="#fff6dc" opacity="{r.uniform(.2, .8):.2f}"/>' for _ in range(n))
def hijabi(x, y, s=1.0, c=TEAL, id="hj"):
    return (f'<g id="{id}" transform="translate({x - 150 * s:.0f},{y - 640 * s:.0f}) scale({s})"><path d="M78 640 L 96 300 Q 150 250 204 300 L 222 640 Z" fill="#1f3b40"/>'
            f'<path d="M150 58 C 88 58 66 122 72 178 C 76 232 58 300 70 336 L 230 336 C 242 300 224 232 228 178 C 234 122 212 58 150 58 Z" fill="{c}"/>'
            f'<ellipse cx="150" cy="168" rx="46" ry="56" fill="{SKIN}"/></g>')

# the take's times (s): each graphic's span, and its beats
T = dict(
 opinions=(0.62, 3.6), khimar=(6.0, 11.3), bigger=(13.0, 18.8), root=(18.9, 29.3), araf=(29.3, 41.7), sad=(41.8, 48.9), maryam=(49.1, 56.2),
 musa=(56.2, 63.5), gaze=(63.9, 73.8), three=(79.6, 84.6), barrier=(84.6, 91.4), banned=(95.7, 99.06), dua=(105.1, 109.4), qiyamah=(109.4, 114.77))

def build(gid):
    t0, t1 = T[gid]; D = round(t1 - t0 + 0.3, 2); L = lambda t: round(t - t0, 2)       # take time → time in the clip
    body, js = [], []
    if gid == "opinions":       # "Hijab, everybody has an opinion": a hijabi under a light, opinions popping round her
        body += [f'<svg class="full" viewBox="0 0 1080 1920"><path d="M470 0 L 610 0 L 800 1500 L 280 1500 Z" fill="rgba(255,244,214,.12)"/>{hijabi(540, 1500, 1.15)}</svg>']
        for i, (w, x, y, c) in enumerate((("BAN IT!", 80, 420, "r"), ("OPPRESSED?", 600, 380, ""), ("MY CHOICE.", 60, 760, ""), ("WHY THOUGH?", 620, 720, ""),
                                          ("FREEDOM!", 120, 1080, ""), ("NOT HERE!", 640, 1060, "r"))):
            body.append(f'<div class="bub {c}" id="b{i}" style="left:{x}px;top:{y}px;transform:rotate({(-6, 5, -4, 6, -3, 4)[i]}deg)">{w}</div>')
            js.append(POP(f"#b{i}", L(0.8 + i * 0.4)))
        js.append(IN("#t", L(2.08), 30)); body.append('<div class="big" id="t" style="top:1580px;font-size:96px">EVERYBODY HAS <span class="g">AN OPINION</span></div>')
    elif gid == "khimar":       # "when the Qur'an tells women to cover, it uses a completely different word": حِجاب struck out, خُمُر, 24:31
        body += ['<div class="ar" id="w1" style="top:300px;font-size:210px">حِجاب</div>', f'<svg class="full" viewBox="0 0 1080 1920"><path id="x1" d="M300 470 L 780 470" stroke="{RED}" stroke-width="18" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/></svg>',
                 f'<div class="ar g" id="w2" style="top:640px;font-size:200px">خُمُر</div>',
                 card("c", "وَلْيَضْرِبْنَ <b>بِخُمُرِهِنَّ</b> عَلَىٰ جُيُوبِهِنَّ", "“and let them draw their <i>khumur</i> (head-coverings) over their chests”", "AN-NŪR 24:31", 1010)]
        js += [IN("#w1", L(6.42), 30), IN("#c", L(8.44), 40), DRAW("#x1", L(9.82), 0.35), POP("#w2", L(10.2), 0.5)]
    elif gid == "bigger":       # "that word does come up in the Qur'an, but in a much bigger context": the word, then the cosmos opening round it
        body += [f'<svg class="full" viewBox="0 0 1080 1920"><g id="cos" opacity="0">{stars(3, 160)}<circle cx="540" cy="760" r="260" fill="none" stroke="{GOLD}" stroke-width="3" opacity=".5"/>'
                 f'<circle cx="540" cy="760" r="420" fill="none" stroke="{GOLD}" stroke-width="2" opacity=".3"/><circle cx="960" cy="380" r="44" fill="#f3ead8"/><circle cx="150" cy="1150" r="70" fill="{GOLD}" opacity=".8"/></g></svg>',
                 '<div class="ar" id="w" style="top:560px;font-size:240px">حِجاب</div>', '<div class="big" id="t" style="top:1120px;font-size:150px">A MUCH <span class="g">BIGGER</span><br>CONTEXT</div>']
        js += [POP("#w", L(14.1), 0.6), f'tl.fromTo("#w", {{scale:1}}, {{scale:0.55, duration:1.2, ease:"power2.inOut"}}, {L(16.6):.2f});',
               f'tl.fromTo("#cos", {{opacity:0, scale:0.5}}, {{opacity:1, scale:1, duration:1.4, ease:"power3.out", transformOrigin:"540px 760px"}}, {L(16.6):.2f});', SLAM("#t", L(17.2))]
    elif gid == "root":         # the root ح ج ب: the letters land, then a curtain closes over a light, a shield
        letters = "".join(f'<div class="ar g" id="l{i}" style="top:330px;left:{x}px;right:auto;width:260px;font-size:230px">{c}</div>' for i, (c, x) in enumerate((("ح", 680), ("ج", 410), ("ب", 140))))
        body += [letters, '<div class="big" id="rt" style="top:250px;font-size:56px;color:#9fb6b0;letter-spacing:.2em">THE ROOT</div>',
                 f'<svg class="full" viewBox="0 0 1080 1920"><g id="lamp" opacity="0"><circle cx="540" cy="1080" r="150" fill="#ffd98a" opacity=".35"/><circle cx="540" cy="1080" r="70" fill="#ffe7b0"/></g>'
                 f'<rect id="cur" x="300" y="860" width="480" height="440" rx="20" fill="#7a2c3a" opacity="0"/>'
                 f'<g id="shd" opacity="0"><path d="M540 860 L 760 940 L 740 1150 C 720 1240 620 1300 540 1330 C 460 1300 360 1240 340 1150 L 320 940 Z" fill="{TEAL}" stroke="{GOLD}" stroke-width="10"/></g></svg>',
                 '<div class="big" id="m1" style="top:1420px;font-size:110px">TO <span class="g">COVER</span></div>', '<div class="big" id="m2" style="top:1540px;font-size:84px">TO SHIELD FROM VIEW</div>']
        js += [IN("#rt", L(20.9), 20)] + [f'tl.fromTo("#l{i}", {{opacity:0, y:-260}}, {{opacity:1, y:0, duration:0.45, ease:"power3.out"}}, {L(t):.2f});' for i, t in enumerate((22.4, 22.9, 23.4))]
        js += [f'tl.to("#l0, #l1, #l2", {{scale:1.08, duration:0.2, yoyo:true, repeat:1, ease:"power2.out"}}, {L(24.4):.2f});', IN("#lamp", L(25.4), 20),
               f'tl.fromTo("#cur", {{opacity:1, scaleX:0}}, {{scaleX:1, duration:0.6, ease:"power3.out", transformOrigin:"0% 50%"}}, {L(26.9):.2f});', IN("#m1", L(26.9), 30),
               POP("#shd", L(28.12), 0.5), IN("#m2", L(28.2), 30)]
    elif gid == "araf":         # 7:46: a wall rises between the garden and the fire
        body += [f'''<svg class="full" viewBox="0 0 1080 1920">
 <g id="gar" opacity="0"><rect x="0" y="560" width="520" height="700" fill="#1f5a3e"/>{"".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#2e8a5a"/><rect x="{x - 8}" y="{y}" width="16" height="{r + 40}" fill="#4a2f1c"/>' for x, y, r in ((110, 760, 70), (290, 700, 90), (430, 820, 60), (180, 990, 80), (380, 1050, 70)))}
  <path d="M0 1180 C 120 1140 260 1210 520 1170 L 520 1260 L 0 1260 Z" fill="#3a8fb0" opacity=".8"/></g>
 <g id="fir" opacity="0"><rect x="560" y="560" width="520" height="700" fill="#3a0f0a"/>{"".join(f'<path class="fl" d="M{x} 1260 C {x - 50} {1140 - h} {x + 30} {1100 - h} {x + 10} {1000 - h} C {x + 80} {1100 - h} {x + 90} {1180 - h} {x + 60} 1260 Z" fill="{c}"/>' for x, h, c in ((600, 40, "#e8662c"), (720, 120, "#f39a2e"), (840, 60, "#e8662c"), (950, 140, "#f6c445"), (1030, 30, "#e8662c")))}</g>
 <rect id="wall" x="515" y="1280" width="50" height="0" fill="{GOLD}" stroke="#7a5a12" stroke-width="6"/>
</svg>''', '<div class="ar g" id="sn" style="top:280px;font-size:110px">سُورَةُ الْأَعْراف</div>',
                 '<div class="big" id="pl" style="top:470px;left:60px;right:auto;width:420px;font-size:62px">PARADISE</div>', '<div class="big r" id="jl" style="top:470px;left:600px;right:auto;width:420px;font-size:62px">JAHANNAM</div>',
                 card("c", "وَبَيْنَهُمَا <b>حِجَابٌ</b>", "“And between them is a <i>ḥijāb</i> (a barrier)”", "AL-AʿRĀF 7:46", 1330)]
        js += [IN("#sn", L(30.1), 30), f'tl.fromTo("#wall", {{attr:{{y:1280, height:0}}}}, {{attr:{{y:520, height:760}}, duration:0.6, ease:"power3.out"}}, {L(35.6):.2f});', IN("#c", L(35.8), 40),
               IN("#gar", L(38.0), 20), IN("#pl", L(38.28), 20), IN("#fir", L(40.3), 20), IN("#jl", L(40.58), 20),
               f'tl.fromTo(".fl", {{scaleY:0.7}}, {{scaleY:1.15, duration:0.3, yoyo:true, repeat:5, stagger:0.06, ease:"sine.inOut", transformOrigin:"50% 100%", immediateRender:false}}, {L(40.6):.2f});']
    elif gid == "sad":          # 38:32: the sun goes down behind the horizon, a veil of dusk over it
        body += [f'''<svg class="full" viewBox="0 0 1080 1920"><defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1b1d3a"/><stop offset=".55" stop-color="#b4573a"/><stop offset="1" stop-color="#f0a35e"/></linearGradient></defs>
 <clipPath id="skyc"><rect x="0" y="300" width="1080" height="760"/></clipPath><rect x="0" y="300" width="1080" height="900" fill="url(#sky)"/><g clip-path="url(#skyc)"><circle id="sun" cx="540" cy="700" r="130" fill="#ffd98a"/></g>
 <path d="M0 1050 C 260 990 520 1060 760 1020 C 900 1000 1000 1020 1080 1010 L 1080 1200 L 0 1200 Z" fill="#3a2418"/>
 <rect id="veil" x="0" y="300" width="1080" height="760" fill="#14111f" opacity="0"/></svg>''', '<div class="ar g" id="sn" style="top:180px;font-size:100px">سُورَةُ ص</div>',
                 card("c", "حَتَّىٰ تَوَارَتْ <b>بِالْحِجَابِ</b>", "“until it was hidden behind the <i>ḥijāb</i>”", "ṢĀD 38:32", 1250, "the sun, in most of the tafsīr")]
        js += [IN("#sn", L(41.94), 30), f'tl.fromTo("#sun", {{y:0}}, {{y:420, duration:2.2, ease:"power2.in"}}, {L(45.0):.2f});',
               f'tl.fromTo("#veil", {{opacity:0}}, {{opacity:0.75, duration:1.0, ease:"power2.inOut"}}, {L(46.5):.2f});', IN("#c", L(46.46), 40)]
    elif gid == "maryam":       # 19:17: a curtain drawn across a niche with a lamp
        body += [f'''<svg class="full" viewBox="0 0 1080 1920"><path d="M300 1250 L 300 640 C 300 430 780 430 780 640 L 780 1250 Z" fill="#1d3a3f" stroke="{GOLD}" stroke-width="10"/>
 <g><path d="M540 560 L 540 640" stroke="{GOLD}" stroke-width="5"/><path d="M500 640 L 580 640 L 565 720 L 515 720 Z" fill="#ffd98a"/><circle cx="540" cy="690" r="80" fill="#ffd98a" opacity=".25"/></g>
 <g id="curL"><path d="M300 470 C 360 700 330 1000 300 1250 L 300 470 Z" fill="#8a3048"/><path d="M300 470 L 540 470 C 520 700 560 1000 540 1250 L 300 1250 Z" fill="#a33a56"/></g>
 <g id="curR"><path d="M780 470 L 540 470 C 560 700 520 1000 540 1250 L 780 1250 Z" fill="#a33a56"/></g></svg>''', '<div class="ar g" id="sn" style="top:240px;font-size:110px">سُورَةُ مَرْيَم</div>',
                 card("c", "فَاتَّخَذَتْ مِن دُونِهِمْ <b>حِجَابًا</b>", "“and she placed a <i>ḥijāb</i> (a screen) between herself and them”", "MARYAM 19:17", 1320)]
        js += [IN("#sn", L(49.28), 30), f'tl.set("#curL", {{scaleX:0, transformOrigin:"300px 0px"}}, 0); tl.set("#curR", {{scaleX:0, transformOrigin:"780px 0px"}}, 0);',
               f'tl.to("#curL", {{scaleX:1, duration:0.8, ease:"power3.out"}}, {L(52.86):.2f}); tl.to("#curR", {{scaleX:1, duration:0.8, ease:"power3.out"}}, {L(52.86):.2f});', IN("#c", L(53.3), 40)]
    elif gid == "musa":         # 42:51: a mountain at night, light behind a veil
        body += [f'''<svg class="full" viewBox="0 0 1080 1920">{stars(7)}<circle id="glow" cx="540" cy="620" r="360" fill="#fff1c4" opacity="0"/>
 <rect id="veil" x="160" y="250" width="760" height="760" rx="30" fill="rgba(241,236,224,.18)" stroke="rgba(233,185,73,.6)" stroke-width="4" opacity="0"/>
 <path d="M60 1250 L 400 760 L 520 880 L 640 700 L 1020 1250 Z" fill="#2a2a38"/><path d="M640 700 L 700 790 L 600 800 Z" fill="#cfcfe0" opacity=".5"/></svg>''',
                 '<div class="ar g" id="sn" style="top:180px;font-size:100px">سُورَةُ الشُّورَى</div>', '<div class="big" id="mu" style="top:1080px;font-size:80px">ALLAH SPOKE TO <span class="g">MŪSĀ</span></div>',
                 card("c", "إِلَّا وَحْيًا أَوْ مِن وَرَاءِ <b>حِجَابٍ</b>", "“…except by revelation, or from behind a <i>ḥijāb</i> (a veil)”", "ASH-SHŪRĀ 42:51", 1260)]
        js += [IN("#sn", L(56.62), 30), f'tl.fromTo("#glow", {{opacity:0, scale:0.4}}, {{opacity:0.55, scale:1, duration:1.2, ease:"power3.out", transformOrigin:"540px 620px"}}, {L(59.24):.2f});', IN("#mu", L(59.3), 30),
               f'tl.fromTo("#veil", {{opacity:0, y:-80}}, {{opacity:1, y:0, duration:0.7, ease:"power3.out"}}, {L(61.58):.2f});', OUT("#mu", L(61.4)), IN("#c", L(61.6), 40)]
    elif gid == "gaze":         # 24:30: men first, lower your gaze; "that is the first hijab"
        body += ['<div class="big" id="w1" style="top:300px;font-size:90px;color:#9fb6b0">BEFORE THE WOMEN…</div>', '<div class="big" id="w2" style="top:420px;font-size:190px">THE <span class="g">MEN</span></div>',
                 f'<svg class="full" viewBox="0 0 1080 1920"><g id="eye" opacity="0"><path d="M360 800 C 440 730 640 730 720 800" fill="none" stroke="{PAPER}" stroke-width="12" stroke-linecap="round"/>'
                 f'<path id="lid" d="M360 800 C 440 870 640 870 720 800" fill="none" stroke="{PAPER}" stroke-width="12" stroke-linecap="round"/>'
                 + "".join(f'<path d="M{x} 845 L {x - 8} 880" stroke="{PAPER}" stroke-width="8" stroke-linecap="round"/>' for x in (420, 480, 540, 600, 660)) + '</g></svg>',
                 card("c", "قُل لِّلْمُؤْمِنِينَ <b>يَغُضُّوا مِنْ أَبْصَارِهِمْ</b>", "“Tell the believing men to <i>lower their gaze</i>”", "AN-NŪR 24:30", 980),
                 '<div class="big" id="fh" style="top:1440px;font-size:150px">THE <span class="g">FIRST</span> HIJAB</div>']
        js += [IN("#w1", L(64.2), 30), SLAM("#w2", L(69.4)), IN("#eye", L(70.4), 20), IN("#c", L(70.6), 40), OUT("#w1", L(70.4)), SLAM("#fh", L(72.86))]
    elif gid == "three":        # "a covering, a protection, a barrier from evil": a shield and three words; arrows bounce off it
        body += [f'<svg class="full" viewBox="0 0 1080 1920"><g id="shd"><path d="M540 420 L 830 520 L 805 800 C 780 920 650 1000 540 1040 C 430 1000 300 920 275 800 L 250 520 Z" fill="{TEAL}" stroke="{GOLD}" stroke-width="12"/>'
                 f'<path d="M540 520 L 540 940 M 380 640 L 700 640" stroke="{GOLD}" stroke-width="8" opacity=".6"/></g>'
                 + "".join(f'<path class="ar{i}" d="M{x} {y} l 60 30 m -60 -30 l 20 60" stroke="#c94a3a" stroke-width="10" stroke-linecap="round" opacity="0"/>' for i, (x, y) in enumerate(((120, 380), (950, 440), (100, 900))))
                 + '</svg>'] + [f'<div class="big" id="w{i}" style="top:{1130 + i * 150}px;font-size:120px">{w}</div>' for i, w in enumerate(("A COVERING", 'A <span class="g">PROTECTION</span>', 'A <span class="r">BARRIER</span>'))]
        js += [POP("#shd", L(79.8), 0.5)] + [IN(f"#w{i}", L(t), 30) for i, t in enumerate((80.6, 81.56, 82.56))]
        js += [f'tl.fromTo(".ar{i}", {{opacity:1, x:0, y:0}}, {{opacity:0, x:{(1, -1, 1)[i] * 160}, y:{(1, 1, -1)[i] * -60}, duration:0.6, ease:"power2.out"}}, {L(84.18) + i * 0.12:.2f});' for i in range(3)]
        js += [f'tl.fromTo("#shd", {{scale:1}}, {{scale:1.06, duration:0.12, yoyo:true, repeat:3, ease:"power2.out", transformOrigin:"540px 730px", immediateRender:false}}, {L(84.18):.2f});']
    elif gid == "barrier":      # a barrier between her and Jahannam, and the evil out there: a dome of light round her
        body += [f'''<svg class="full" viewBox="0 0 1080 1920">{"".join(f'<path class="fl" d="M{x} 1600 C {x - 60} {1440 - h} {x + 30} {1400 - h} {x + 10} {1300 - h} C {x + 90} {1400 - h} {x + 100} {1480 - h} {x + 70} 1600 Z" fill="{c}" opacity="0"/>' for x, h, c in ((60, 40, "#e8662c"), (220, 110, "#f39a2e"), (400, 60, "#e8662c"), (600, 130, "#f6c445"), (790, 70, "#e8662c"), (950, 120, "#f39a2e")))}
 <path id="dome" d="M240 1300 C 240 760 840 760 840 1300 Z" fill="rgba(233,185,73,.16)" stroke="{GOLD}" stroke-width="10" opacity="0"/>
 {hijabi(540, 1290, 0.95)}
 {"".join(f'<path class="ev" d="M{x} {y} q 30 -30 60 0 t 60 0" stroke="#5a2a5a" stroke-width="14" fill="none" stroke-linecap="round" opacity="0"/>' for x, y in ((60, 560), (900, 620), (80, 980), (920, 1040)))}</svg>''',
                 '<div class="big" id="w1" style="top:280px;font-size:96px">A BARRIER FROM<br><span class="r">JAHANNAM</span></div>', '<div class="big" id="w2" style="top:500px;font-size:80px">AND FROM THE <span class="g">EVIL OUT THERE</span></div>']
        js += [f'tl.fromTo("#dome", {{opacity:0, scale:0.6}}, {{opacity:1, scale:1, duration:0.6, ease:"back.out(1.4)", transformOrigin:"540px 1300px"}}, {L(85.1):.2f});',
               IN("#w1", L(87.74), 30), f'tl.fromTo(".fl", {{opacity:0, scaleY:0.3}}, {{opacity:1, scaleY:1, duration:0.5, stagger:0.06, ease:"power3.out", transformOrigin:"50% 100%"}}, {L(87.74):.2f});',
               IN("#w2", L(90.06), 30), f'tl.fromTo(".ev", {{opacity:1, x:(i) => [0, 0, 0, 0][i]}}, {{opacity:0, x:(i) => [200, -200, 200, -200][i], duration:0.7, stagger:0.1, ease:"power2.out"}}, {L(90.36):.2f});']
    elif gid == "banned":       # "the hijab being banned left, right and centre": three stamps
        body += [f'<svg class="full" viewBox="0 0 1080 1920">{hijabi(200, 1250, 0.6, "#3f6f68", "h1")}{hijabi(540, 1250, 0.6, TEAL, "h2")}{hijabi(880, 1250, 0.6, "#4f7f63", "h3")}</svg>']
        body += [f'<div class="big r" id="s{i}" style="top:{y}px;left:{x}px;right:auto;width:340px;font-size:84px;border:8px solid {RED};border-radius:14px;padding:8px 0;transform:rotate({r}deg);background:rgba(255,255,255,.06)">BANNED</div>'
                 for i, (x, y, r) in enumerate(((30, 820, -12), (710, 800, 10), (370, 860, -4)))]
        body += ['<div class="big" id="w" style="top:330px;font-size:120px">LEFT, RIGHT<br>AND <span class="r">CENTRE</span></div>']
        js += [IN("#w", L(97.04), 30)] + [SLAM(f"#s{i}", L(t)) for i, t in enumerate((97.36, 97.82, 98.54))]
    elif gid == "dua":          # "may Allah protect our sisters in hijab"
        body += [f'<svg class="full" viewBox="0 0 1080 1920"><circle id="glow" cx="540" cy="980" r="420" fill="#fff1c4" opacity="0"/>{hijabi(380, 1350, 0.7, TEAL, "h1")}{hijabi(700, 1350, 0.7, "#3f6f68", "h2")}</svg>',
                 '<div class="big" id="w" style="top:300px;font-size:100px">MAY ALLAH <span class="g">PROTECT</span><br>OUR SISTERS</div>', '<div class="ar g" id="am" style="top:1420px;font-size:150px">آمِين</div>']
        js += [IN("#w", L(105.32), 30), f'tl.fromTo("#glow", {{opacity:0, scale:0.5}}, {{opacity:0.35, scale:1, duration:1.2, ease:"power3.out", transformOrigin:"540px 980px"}}, {L(106.38):.2f});', POP("#am", L(108.0), 0.6)]
    elif gid == "qiyamah":      # "the hijab you're wearing will be a covering for you on Yawm al-Qiyāmah"
        body += [f'<svg class="full" viewBox="0 0 1080 1920">{stars(11, 120)}<circle id="glow" cx="540" cy="900" r="460" fill="#fff1c4" opacity="0"/>{hijabi(540, 1330, 0.95)}</svg>',
                 '<div class="big" id="w" style="top:280px;font-size:110px">A <span class="g">COVERING</span> FOR YOU</div>', '<div class="ar g" id="yq" style="top:1380px;font-size:130px">يَوْمَ الْقِيامَة</div>',
                 '<div class="big" id="en" style="top:1580px;font-size:56px;color:#9fb6b0">ON THE DAY OF JUDGEMENT</div>']
        js += [f'tl.fromTo("#glow", {{opacity:0, scale:0.4}}, {{opacity:0.45, scale:1, duration:1.6, ease:"power3.out", transformOrigin:"540px 900px"}}, {L(109.8):.2f});', IN("#w", L(112.64), 30), POP("#yq", L(113.6), 0.6), IN("#en", L(113.9), 20)]
    out = os.path.join(HERE, "out", gid); a = os.path.join(out, "assets")
    if os.path.exists(out): shutil.rmtree(out)
    os.makedirs(a)
    for f in ("anton-latin-400-normal.woff2", "instrument-serif-latin-400-normal.woff2", "amiri-arabic-700-normal.woff2"): shutil.copy(os.path.join(FONTS, f), a)
    shutil.copy(GSAP, a)
    open(os.path.join(out, "index.html"), "w").write(f"""<!doctype html><html><head><meta charset="UTF-8"><style>{CSS}</style><script src="assets/gsap.min.js"></script></head>
<body><div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{D}"><div id="cam">
{chr(10).join(body)}</div><div id="vig"></div></div>
<script>const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;</script></body></html>""")
    return out

if __name__ == "__main__":
    for gid in (sys.argv[1:] or list(T)):
        out = build(gid)
        if os.environ.get("BUILD_ONLY"): continue
        r = subprocess.run(["npx", "-y", "hyperframes", "render", "-o", f"../{gid}.mp4"], cwd=out, capture_output=True, text=True)
        print(gid, "ok" if r.returncode == 0 else r.stdout[-400:] + r.stderr[-400:])
