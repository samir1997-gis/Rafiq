#!/usr/bin/env python3
"""Motion graphics for the three scripts ready to film (owner, 1 Nov 2026: "you can start making the graphics for all three"):
in shāʾ Allāh (#314, reels/insha/SCRIPT.md), aḥad (#315, reels/ahad/SCRIPT.md) and Dajjāl (#316, reels/dajjal/SCRIPT.md). One silent
1080x1920 clip per 🎬 cue, cut in full screen over his talking shots while he keeps talking, in the hijab video's look (its CSS and helpers,
reels/hijab-video/graphics.py). Nothing is filmed yet, so each beat sits at a planned time in its clip (B below); when the footage comes, the
edit re-times them to his words (as T in the hijab graphics) and the sound effects go on in the edit, checked as audible.
Every ayah and hadith is on screen in Arabic and English with its reference. Faceless figures (owner, 27 Oct). Easing as MOTION-STYLE.md.

  python3 brag-quiz/reels/scripts-gfx/graphics.py [set|id ...]    sets: insha ahad dajjal → out/<id>.mp4
"""
import os, shutil, subprocess, sys
from importlib.machinery import SourceFileLoader
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
H = SourceFileLoader("hg", os.path.join(ROOT, "brag-quiz/reels/hijab-video/graphics.py")).load_module()
CSS, IN, POP, OUT, SLAM, DRAW, card, stars = H.CSS, H.IN, H.POP, H.OUT, H.SLAM, H.DRAW, H.card, H.stars
GOLD, RED, PAPER, INK, TEAL, SKIN = H.GOLD, H.RED, H.PAPER, H.INK, H.TEAL, H.SKIN
CSS += f"""
.tag {{ position:absolute; left:0; right:0; text-align:center; font-family:Serif; font-size:52px; color:#cfe0dc; opacity:0; }}
.box {{ position:absolute; left:140px; right:140px; height:150px; border-radius:20px; background:{PAPER}; color:{INK}; font-family:Anton; font-size:84px;
  display:flex; align-items:center; justify-content:center; box-shadow:0 18px 40px rgba(0,0,0,.45); opacity:0; }}
.chat {{ position:absolute; max-width:700px; padding:26px 38px; border-radius:44px; font-family:Serif; font-size:64px; line-height:1.15; opacity:0;
  box-shadow:0 14px 30px rgba(0,0,0,.4); }}
.chat.me {{ right:90px; background:{TEAL}; color:#fff; border-bottom-right-radius:10px; }} .chat.them {{ left:90px; background:{PAPER}; color:{INK}; border-bottom-left-radius:10px; }}
.stamp {{ position:absolute; font-family:Anton; color:{RED}; border:10px solid {RED}; border-radius:18px; padding:4px 30px; opacity:0; }}
.mini {{ position:absolute; font-family:Am; color:{PAPER}; opacity:0; }}
#lt {{ filter:blur(70px); }}   /* the glows: soft light, not a disc */
"""
ROOTS = lambda letters, branches, top=300: (     # a root in tiles with its words branching under it: [(arabic, english, colour)]
    f'<div class="ar g" id="rt" style="top:{top}px;font-size:150px;letter-spacing:.25em">{letters}</div>'
    + "".join(f'<div class="ar" id="br{i}" style="top:{top + 330 + i * 300}px;font-size:{150 if len(a) < 7 else 120}px;{c}">{a}</div>'
              f'<div class="tag" id="bt{i}" style="top:{top + 560 + i * 300}px">{e}</div>' for i, (a, e, c) in enumerate(branches)))
def person_lying(x, y, s=1.0):                       # faceless, on his back
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M-260 0 C -250 -60 230 -70 250 0 Z" fill="#3a2a22"/>'
            f'<circle cx="-300" cy="-30" r="54" fill="#6b4a32"/><path d="M200 -10 L 330 -20 L 330 10 L 200 10 Z" fill="#3a2a22"/></g>')
def figure(x, y, s, c, id=""):                       # faceless, standing
    return (f'<g transform="translate({x},{y}) scale({s})"><g id="{id}"><path d="M-70 0 L -56 -200 C -52 -250 52 -250 56 -200 L 70 0 Z" fill="{c}"/>'
            f'<circle cx="0" cy="-290" r="58" fill="{c}"/></g></g>')   # animate the inner group; the outer one places it
SUNSAND = (f'<rect x="0" y="0" width="1080" height="1920" fill="#f2c46b" opacity=".18"/><circle id="sun" cx="540" cy="420" r="230" fill="#fff4cf"/>'
           f'<circle cx="540" cy="420" r="320" fill="#ffe7a3" opacity=".35"/>'
           f'<path d="M-50 1180 C 250 1100 520 1180 760 1130 C 900 1100 1000 1120 1130 1100 L 1130 1920 L -50 1920 Z" fill="#d79b55"/>'
           f'<path d="M-50 1400 C 300 1330 600 1420 1130 1360 L 1130 1920 L -50 1920 Z" fill="#c4823f"/>'
           + "".join(f'<path class="heat" d="M{x} 1080 c 20 -30 -20 -60 0 -90 c 20 -30 -20 -60 0 -90" fill="none" stroke="#fff4cf" stroke-width="6" opacity=".5"/>'
                     for x in (200, 420, 660, 880)))

# ---- the detailed scenes (owner, 8 Nov 2026): textured sand, heat haze, light, faceless figures with clothes and shadow
DEFS = ('<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff3d6"/><stop offset=".45" stop-color="#f7cf8e"/><stop offset="1" stop-color="#e9a45e"/></linearGradient>'
        '<radialGradient id="glow"><stop offset="0" stop-color="#fffbe8" stop-opacity="1"/><stop offset=".4" stop-color="#ffe2a0" stop-opacity=".6"/><stop offset="1" stop-color="#ffd27a" stop-opacity="0"/></radialGradient>'
        '<linearGradient id="sand" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e2b578"/><stop offset=".5" stop-color="#cf9858"/><stop offset="1" stop-color="#a86f3a"/></linearGradient>'
        '<radialGradient id="hotsand" cx=".5" cy=".75" r=".8"><stop offset="0" stop-color="#ff9a3c"/><stop offset=".5" stop-color="#c8561e"/><stop offset="1" stop-color="#5a230d"/></radialGradient>'
        '<linearGradient id="skin" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6b4330"/><stop offset=".6" stop-color="#4a2d1f"/><stop offset="1" stop-color="#2e1a11"/></linearGradient>'
        '<linearGradient id="shadeR" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".35"/></linearGradient>'
        '<linearGradient id="rockg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9a9184"/><stop offset=".5" stop-color="#6f675c"/><stop offset="1" stop-color="#3f3a33"/></linearGradient>'
        '<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="3" seed="4"/>'
        '<feColorMatrix values="0 0 0 0 0.25  0 0 0 0 0.16  0 0 0 0 0.08  0 0 0 0.9 -0.25"/></filter>'
        '<pattern id="grainp" width="1080" height="1920" patternUnits="userSpaceOnUse"><rect width="1080" height="1920" filter="url(#grain)"/></pattern>'
        '<filter id="haze" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence id="hz" type="turbulence" baseFrequency="0.004 0.03" numOctaves="2" seed="2" result="n"/>'
        '<feDisplacementMap in="SourceGraphic" in2="n" scale="10"/></filter>'
        '<filter id="soft"><feGaussianBlur stdDeviation="6"/></filter><filter id="sh"><feGaussianBlur stdDeviation="10"/></filter></defs>')
HAZE = 'tl.fromTo("#hz", {attr:{baseFrequency:"0.004 0.03"}}, {attr:{baseFrequency:"0.006 0.045"}, duration:3, yoyo:true, repeat:2, ease:"sine.inOut"}, 0.05);'
HOUSES = "".join(f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#d9b88c"/><rect x="{x + w}" y="{y + 10}" width="{w // 4}" height="{h - 10}" fill="#b08b62"/>'
                 f'<rect x="{x + w // 3}" y="{y + h - 50}" width="22" height="50" fill="#5a3f28"/><rect x="{x + 12}" y="{y + 20}" width="16" height="16" fill="#6b4c32"/></g>'
                 for x, y, w, h in ((40, 1180, 120, 120), (180, 1150, 150, 150), (350, 1190, 100, 110), (640, 1180, 130, 120), (790, 1140, 160, 160), (960, 1190, 110, 110)))
DUST = "".join(f'<circle class="dst" cx="{x}" cy="{y}" r="{r}" fill="#fff1d0" opacity=".5"/>' for x, y, r in ((120, 900, 4), (300, 700, 3), (520, 980, 5), (760, 760, 3), (930, 1000, 4), (640, 600, 3), (220, 1100, 3)))
DRIFT = 'tl.fromTo(".dst", {x:0, y:0}, {x:60, y:-40, duration:6, ease:"none", stagger:0.2}, 0.05);'
def ROBED(robe, wrap, s=1.0, trim=None):     # a faceless man in a long robe and head-wrap, standing, his shadow under him
    return (f'<g transform="scale({s})"><ellipse cx="0" cy="8" rx="90" ry="16" fill="#3b2614" opacity=".35"/>'
            f'<path d="M-62 0 L-48 -300 C -44 -350 44 -350 48 -300 L62 0 Z" fill="{robe}"/><path d="M-62 0 L-48 -300 C -44 -350 44 -350 48 -300 L62 0 Z" fill="url(#shadeR)"/>'
            + (f'<path d="M-6 -340 L-10 0 M6 -340 L10 0" stroke="{trim}" stroke-width="5"/>' if trim else "")
            + f'<path d="M-48 -300 C -80 -250 -90 -190 -70 -150" stroke="{robe}" stroke-width="30" fill="none" stroke-linecap="round"/>'
            f'<path d="M48 -300 C 80 -250 90 -190 70 -150" stroke="{robe}" stroke-width="30" fill="none" stroke-linecap="round"/>'
            f'<circle cx="0" cy="-385" r="44" fill="#6b4a32"/><path d="M-50 -390 C -50 -450 50 -450 50 -390 C 30 -405 -30 -405 -50 -390 Z" fill="{wrap}"/>'
            f'<path d="M-46 -395 C -60 -330 -40 -320 -36 -300" stroke="{wrap}" stroke-width="16" fill="none"/></g>')
DRAGGED = ('<ellipse cx="0" cy="20" rx="210" ry="18" fill="#3b2614" opacity=".35"/>'      # pulled along by his wrists, half lying
           '<path d="M-200 0 C -150 -40 -40 -60 60 -50 L70 10 C -40 20 -150 20 -200 10Z" fill="#efe6d4"/>'
           '<path d="M60 -50 C 120 -60 170 -80 200 -150 L210 -140 C 190 -60 140 -20 70 0Z" fill="url(#skin)"/>'
           '<circle cx="-230" cy="-40" r="40" fill="url(#skin)"/><path d="M-170 -20 C -120 -90 -60 -130 0 -150" stroke="#4a2d1f" stroke-width="26" fill="none" stroke-linecap="round"/>')
LYING = ('<path d="M-300 0 C -280 -55 260 -65 300 0 Z" fill="#efe6d4"/><path d="M-300 0 C -280 -55 260 -65 300 0 Z" fill="url(#shadeR)"/>'
         '<path d="M-150 -40 C -60 -70 80 -70 160 -40 L160 0 L-150 0Z" fill="url(#skin)"/>'
         '<circle cx="-345" cy="-30" r="46" fill="url(#skin)"/><path d="M280 -10 L400 -20 L400 10 L280 10Z" fill="url(#skin)"/>'
         '<path d="M-150 -20 C -190 20 -230 30 -270 30" stroke="#4a2d1f" stroke-width="24" fill="none" stroke-linecap="round"/>')
BOULDER = ('<g transform="translate(540 1190)"><ellipse cx="0" cy="150" rx="200" ry="22" fill="#3b2614" opacity=".25"/>'
           '<path d="M-210 60 L-170 -80 L-60 -140 L80 -130 L190 -60 L215 70 L120 130 L-120 135Z" fill="url(#rockg)"/>'
           '<path d="M-170 -80 L-60 -140 L80 -130 L20 -60 L-90 -50Z" fill="#b1a898" opacity=".55"/>'
           '<path d="M-60 -20 L-10 30 L-30 90 M60 -40 L90 20 L70 80 M-130 40 L-90 70" stroke="#2e2a25" stroke-width="6" fill="none"/>'
           '<path d="M-210 60 L-170 -80 L-60 -140 L80 -130 L190 -60 L215 70 L120 130 L-120 135Z" fill="url(#grainp)" opacity=".5"/></g>')
IMPACT = "".join(f'<circle class="imp" cx="540" cy="1360" r="{r}" fill="none" stroke="#f6e3c0" stroke-width="{w}" opacity="0"/>' for r, w in ((120, 18), (200, 10)))
PUFFS = "".join(f'<circle class="pf" cx="{x}" cy="1470" r="{r}" fill="#e9cfa2" opacity="0" filter="url(#soft)"/>' for x, r in ((120, 40), (60, 30), (180, 34)))

def gfx(gid):
    """→ (duration, body html, js). Times in seconds from the clip's start; first elements on screen by 0.05 s."""
    b, j = [], []
    # ---------------- in shāʾ Allāh (#314) ----------------
    if gid == "i_no":            # "We've turned in shāʾ Allāh into a polite no. It's the opposite."
        b += ['<div class="big" id="t" style="top:640px;font-size:150px">IN SHĀʾ ALLĀH<br>= <span class="r" id="no" style="position:relative">NO</span>?</div>',
              f'<svg class="full" viewBox="0 0 1080 1920"><path id="x" d="M560 960 L 820 860" stroke="{GOLD}" stroke-width="22" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/></svg>',
              '<div class="big g" id="op" style="top:1150px;font-size:120px">THE OPPOSITE.</div>']
        j += [IN("#t", 0.05, 30), DRAW("#x", 1.6, 0.35), SLAM("#op", 2.0)]; d = 3.6
    elif gid == "i_chat":        # "Are you coming tonight?" "In shāʾ Allāh…" and we all know what that means
        b += ['<div class="chat me" id="c0" style="top:560px">Are you coming tonight?</div>', '<div class="chat them" id="c1" style="top:820px">In shāʾ Allāh… 🤲</div>',
              f'<div class="stamp" id="eq" style="left:520px;top:1010px;font-size:90px;transform:rotate(-8deg)">= NO 😅</div>']
        j += [POP("#c0", 0.05, 0.8), POP("#c1", 0.9, 0.8), f'tl.to("#c1", {{opacity:0.45, duration:0.4, ease:"power2.out"}}, 2.0);', SLAM("#eq", 2.1)]; d = 3.8
    elif gid == "i_split":       # "It's three words. In: if. Shāʾa: willed. Allāh."
        for i, (a, e, x) in enumerate((("إِنْ", "if", 760), ("شاءَ", "willed", 420), ("اللّٰهُ", "Allah", 80))):
            b += [f'<div class="ar" id="w{i}" style="top:640px;left:{x}px;right:auto;width:260px;font-size:150px">{a}</div>',
                  f'<div class="tag" id="e{i}" style="top:900px;left:{x}px;right:auto;width:260px">{e}</div>']
            j += [POP(f"#w{i}", 0.05 + i * 0.7, 0.6), IN(f"#e{i}", 0.3 + i * 0.7, 20)]
        b += ['<div class="big" id="t" style="top:1180px;font-size:110px">“IF ALLAH <span class="g">WILLS</span>”</div>']; j += [IN("#t", 2.4, 30)]; d = 4.2
    elif gid == "i_past":        # "look at that verb: shāʾa. It's in the past tense"
        b += ['<div class="ar g" id="w" style="top:560px;font-size:280px">شاءَ</div>',
              f'<div class="stamp" id="p" style="left:600px;top:1000px;font-size:110px;transform:rotate(-10deg)">PAST</div>',
              '<div class="tag" id="e" style="top:1240px">shāʾa · “willed”</div>']
        j += [POP("#w", 0.05, 0.7), IN("#e", 0.6, 20), SLAM("#p", 1.3)]; d = 3.0
    elif gid == "i_pens":        # "The pens have been lifted, and the pages have dried." (at-Tirmidhī 2516)
        b += [f'<svg class="full" viewBox="0 0 1080 1920"><rect x="260" y="360" width="560" height="420" rx="16" fill="{PAPER}"/>'
              + "".join(f'<rect class="ln" x="310" y="{410 + i * 60}" width="{460 - (i % 3) * 60}" height="16" rx="8" fill="#5c6e70"/>' for i, _ in enumerate(range(6)))
              + f'<g id="pen"><path d="M700 300 L 760 300 L 740 640 L 720 680 L 700 640 Z" fill="{GOLD}"/><path d="M700 300 L 760 300 L 760 270 L 700 270 Z" fill="{INK}"/></g></svg>',
              card("c", "رُفِعَتِ <b>الأَقْلامُ</b> وَجَفَّتِ <b>الصُّحُفُ</b>", "“The pens have been lifted, and the pages have dried.”", "AT-TIRMIDHĪ 2516", 980)]
        j += [f'tl.fromTo(".ln", {{scaleX:0}}, {{scaleX:1, duration:0.3, stagger:0.12, ease:"power2.out", transformOrigin:"0% 50%"}}, 0.05);',
              f'tl.to("#pen", {{y:-420, rotation:20, opacity:0, duration:0.8, ease:"power2.in", svgOrigin:"730 640"}}, 1.2);',
              f'tl.to(".ln", {{fill:"{INK}", duration:0.6, ease:"power2.out"}}, 1.9);', IN("#c", 1.4, 40)]; d = 4.5
    elif gid == "i_root":        # shāʾa and shayʾ share a root: a thing is something willed
        b += [ROOTS("ش ي ء", [("شاءَ", "to will", ""), ("شَيْء", "a thing = <i style=\"color:#E9B949\">something willed</i>", "")])]
        j += [POP("#rt", 0.05, 0.6)] + [x for i in range(2) for x in (POP(f"#br{i}", 0.8 + i * 0.9, 0.6), IN(f"#bt{i}", 1.1 + i * 0.9, 20))]; d = 3.8
    elif gid == "i_kahf":        # al-Kahf 18:23–24, لِشَيْءٍ and يَشاءَ light up together
        b += [card("c", "وَلا تَقُولَنَّ <b class=\"k\">لِشَيْءٍ</b> إِنِّي فاعِلٌ ذٰلِكَ غَدًا ﴿٢٣﴾ إِلّا أَنْ <b class=\"k\">يَشاءَ</b> اللّٰهُ ﴿٢٤﴾",
                   "“Never say of <i>anything</i>, ‘I will do that tomorrow’, except: if Allah <i>wills</i>.”", "AL-KAHF 18:23–24", 640)]
        j += [IN("#c", 0.05, 40), f'tl.fromTo("#c .k", {{backgroundColor:"rgba(233,185,73,0)"}}, {{backgroundColor:"rgba(233,185,73,.75)", duration:0.4, stagger:0.15, ease:"power2.out"}}, 1.6);']; d = 4.6
    elif gid == "i_camel":       # "tie your camel, then put your trust in Allah" (at-Tirmidhī 2517)
        b += [f'<svg class="full" viewBox="0 0 1080 1920"><circle id="lt" cx="540" cy="760" r="420" fill="#fff1c4" opacity="0"/>'
              f'<path d="M300 1000 C 300 860 360 780 470 790 C 520 700 600 700 640 790 C 700 780 740 720 760 640 C 770 600 820 600 830 640 L 840 700 C 860 760 820 860 760 900 L 760 1000 L 720 1000 L 720 920 L 400 920 L 400 1000 L 360 1000 Z" fill="#c98a4a"/>'
              f'<rect x="150" y="760" width="40" height="300" rx="10" fill="#7a4a24"/>'
              f'<path id="rope" d="M180 800 C 260 820 300 860 380 880" fill="none" stroke="{PAPER}" stroke-width="10" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/></svg>',
              card("c", "<b>اعْقِلْها</b> وَتَوَكَّلْ", "“Tie it, and put your trust [in Allah].”", "AT-TIRMIDHĪ 2517", 1220)]
        j += [IN("#c", 0.05, 30), DRAW("#rope", 0.8, 0.6), f'tl.fromTo("#lt", {{opacity:0}}, {{opacity:0.35, duration:1.0, ease:"power3.out"}}, 1.8);']; d = 4.0
    elif gid == "i_tawakkul":    # tawakkul ← و ك ل → wakīl
        b += [ROOTS("و ك ل", [("تَوَكُّل", "tawakkul: trusting your affairs to Him", ""), ("وَكِيل", "wakīl: the one you hand them to", "")])]
        j += [POP("#rt", 0.05, 0.6)] + [x for i in range(2) for x in (POP(f"#br{i}", 0.8 + i * 0.9, 0.6), IN(f"#bt{i}", 1.1 + i * 0.9, 20))]; d = 3.8
    elif gid == "i_worries":     # the job, the exam, the marriage, the results… then they fall away; at-Tirmidhī 2516
        for i, w in enumerate(("THE JOB", "THE EXAM", "THE MARRIAGE", "THE RESULTS")):
            b.append(f'<div class="box" id="w{i}" style="top:{1180 - i * 175}px;transform:rotate({(-3, 2, -2, 3)[i]}deg)">{w}</div>')
            j.append(f'tl.fromTo("#w{i}", {{opacity:0, y:-300}}, {{opacity:1, y:0, duration:0.4, ease:"back.out(1.4)"}}, {0.05 + i * 0.45:.2f});')
        j.append(f'tl.to(".box", {{y:1400, rotation:(i) => [-25, 30, -40, 20][i], opacity:0, duration:0.8, stagger:0.08, ease:"power2.in"}}, 2.6);')
        b.append(card("c", "لَوِ اجْتَمَعَتْ عَلى أَنْ يَنْفَعُوكَ بِشَيْءٍ لَمْ يَنْفَعُوكَ إِلّا بِشَيْءٍ <b>قَدْ كَتَبَهُ اللّٰهُ لَكَ</b>",
                      "“If they all gathered to benefit you, they could only do it with what <i>Allah had already written for you</i>.”", "AT-TIRMIDHĪ 2516", 620))
        j.append(IN("#c", 3.3, 40)); d = 6.0
    elif gid == "i_hadid":       # al-Ḥadīd 57:23
        b += [card("c", "لِكَيْلا تَأْسَوْا عَلى ما فاتَكُمْ وَلا تَفْرَحُوا بِما آتاكُمْ",
                   "“so that you don’t <i>despair</i> over what you missed, nor <i>gloat</i> over what you were given”", "AL-ḤADĪD 57:23", 660)]
        j += [IN("#c", 0.05, 40)]; d = 4.0
    elif gid == "i_allah":       # "Say it as letting go": اللّٰه, slow push-in
        b += [f'<svg class="full" viewBox="0 0 1080 1920"><circle id="lt" cx="540" cy="860" r="460" fill="#fff1c4" opacity="0"/></svg>',
              '<div class="ar g" id="w" style="top:620px;font-size:300px">اللّٰه</div>', '<div class="big" id="t" style="top:1240px;font-size:110px">SAY IT AS<br><span class="g">LETTING GO</span></div>']
        j += [POP("#w", 0.05, 0.7), f'tl.fromTo("#w", {{scale:1}}, {{scale:1.12, duration:4, ease:"power1.inOut"}}, 0.5);',
              f'tl.fromTo("#lt", {{opacity:0}}, {{opacity:0.3, duration:1.4, ease:"power3.out"}}, 0.3);', IN("#t", 1.2, 30)]; d = 4.5
    # ---------------- aḥad (#315) ----------------
    elif gid == "a_word":        # black screen, a single word fades up: أَحَد
        b += ['<div class="ar" id="w" style="top:680px;font-size:300px">أَحَد</div>']
        j += [f'tl.fromTo("#w", {{opacity:0.05, scale:0.92}}, {{opacity:1, scale:1, duration:1.8, ease:"power2.out"}}, 0.05);']; d = 3.0
    elif gid == "a_scene":       # Makkah, midday, the burning sand, Bilāl on his back, the rock
        b += [f'<svg class="full" viewBox="0 0 1080 1920">{SUNSAND}{person_lying(560, 1260, 1.0)}'
              f'<path id="rock" d="M380 1240 L 430 1080 L 560 1040 L 700 1090 L 740 1230 Z" fill="#7d7468"/></svg>',
              '<div class="big" id="t" style="top:1500px;font-size:96px">MAKKAH · <span class="g">MIDDAY</span></div>']
        j += [IN("#t", 0.05, 30), f'tl.fromTo(".heat", {{y:0}}, {{y:-30, duration:0.8, yoyo:true, repeat:5, stagger:0.15, ease:"sine.inOut"}}, 0.05);',
              f'tl.fromTo("#rock", {{y:-700, opacity:0}}, {{y:0, opacity:1, duration:0.5, ease:"power3.in"}}, 1.6);',
              f'tl.fromTo("#cam", {{y:-10}}, {{y:10, duration:0.05, yoyo:true, repeat:5, ease:"sine.inOut", immediateRender:false}}, 2.1);', 'tl.set("#cam", {y:0}, 2.4);']; d = 4.5
    elif gid == "a_slam":        # "Aḥad. Aḥad." twice, with a shake
        b += [f'<svg class="full" viewBox="0 0 1080 1920">{SUNSAND}</svg>', '<div class="ar" id="w0" style="top:420px;font-size:260px">أَحَد</div>',
              '<div class="ar g" id="w1" style="top:900px;font-size:260px">أَحَد</div>']
        j += [SLAM("#w0", 0.05), SLAM("#w1", 1.0)]; d = 2.6
    elif gid == "a_root":        # wāḥid ← و ح د → aḥad
        b += [ROOTS("و ح د", [("وَاحِد", "wāḥid: one, the number", ""), ("أَحَد", "aḥad: the One, no second", "color:#E9B949")])]
        j += [POP("#rt", 0.05, 0.6)] + [x for i in range(2) for x in (POP(f"#br{i}", 0.8 + i * 0.9, 0.6), IN(f"#bt{i}", 1.1 + i * 0.9, 20))]; d = 3.8
    elif gid == "a_count":       # wāḥid is a number: 1, 2, 3… aḥad has no second
        b += ['<div class="ar" id="w" style="top:330px;font-size:180px">وَاحِد</div>']
        b += [f'<div class="big" id="n{i}" style="top:650px;left:{140 + i * 290}px;right:auto;width:220px;font-size:220px">{i + 1}</div>' for i in range(3)]
        b += ['<div class="ar g" id="a" style="top:1060px;font-size:180px">أَحَد</div>', '<div class="big" id="t" style="top:1400px;font-size:96px">NO <span class="g">SECOND</span></div>']
        j += [IN("#w", 0.05, 20)] + [POP(f"#n{i}", 0.6 + i * 0.4, 0.5) for i in range(3)] + [POP("#a", 2.2, 0.6), SLAM("#t", 2.8)]; d = 4.4
    elif gid == "a_ikhlas":      # al-Ikhlāṣ 112:1 and 112:4: أَحَد lit at the start and at the end
        b += [card("c1", "قُلْ هُوَ اللّٰهُ <b>أَحَدٌ</b>", "“Say: He is Allah, <i>the One</i>.”", "AL-IKHLĀṢ 112:1", 420),
              card("c4", "وَلَمْ يَكُنْ لَهُ كُفُوًا <b>أَحَدٌ</b>", "“and there is <i>no one</i> equal to Him.”", "AL-IKHLĀṢ 112:4", 1020)]
        j += [IN("#c1", 0.05, 40), IN("#c4", 2.0, 40)]; d = 4.6
    elif gid == "a_free":        # not al-Lāt, not al-ʿUzzā, not the man standing over him: they crack and fade; "he was the free one"
        b += [f'<svg class="full" viewBox="0 0 1080 1920"><g id="idols"><rect x="140" y="560" width="200" height="420" rx="20" fill="#5a4a3a"/><rect x="740" y="560" width="200" height="420" rx="20" fill="#5a4a3a"/>'
              f'{figure(540, 1050, 1.5, "#0e1a1e", "sh")}'
              + "".join(f'<path class="cr" d="{d}" fill="none" stroke="{GOLD}" stroke-width="7" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>' for d in (
                  "M240 560 L 220 700 L 260 780 L 230 980", "M840 560 L 860 690 L 820 800 L 850 980", "M540 620 L 520 760 L 560 880 L 530 1050"))
              + '</g></svg>',
              '<div class="mini" id="l0" style="left:150px;top:1000px;width:180px;text-align:center;font-size:56px">اللّات</div>',
              '<div class="mini" id="l1" style="left:750px;top:1000px;width:180px;text-align:center;font-size:56px">العُزّى</div>',
              '<div class="big" id="t" style="top:1350px;font-size:110px">HE WAS THE<br><span class="g">FREE ONE</span></div>']
        j += [IN("#idols", 0.05, 30), IN("#l0", 0.3, 10), IN("#l1", 0.5, 10),
              f'tl.fromTo(".cr", {{strokeDashoffset:1}}, {{strokeDashoffset:0, duration:0.35, stagger:0.2, ease:"power2.inOut"}}, 1.2);',
              f'tl.to("#idols, #l0, #l1", {{opacity:0, y:120, duration:0.6, ease:"power2.in"}}, 2.2);', SLAM("#t", 2.8)]; d = 4.6
    elif gid == "a_rock":        # Abū Bakr bought him and set him free: the rock lifts, light
        b += [f'<svg class="full" viewBox="0 0 1080 1920">{SUNSAND}<circle id="lt" cx="540" cy="1100" r="520" fill="#fff8e0" opacity="0"/>{person_lying(560, 1260, 1.0)}'
              f'<path id="rock" d="M380 1240 L 430 1080 L 560 1040 L 700 1090 L 740 1230 Z" fill="#7d7468"/></svg>',
              '<div class="big" id="t" style="top:1520px;font-size:120px">SET <span class="g">FREE</span></div>']
        j += [f'tl.to("#rock", {{y:-900, x:300, rotation:25, opacity:0, duration:0.9, ease:"power2.in", svgOrigin:"560 1150"}}, 0.6);',
              f'tl.fromTo("#lt", {{opacity:0}}, {{opacity:0.6, duration:1.2, ease:"power3.out"}}, 1.2);', IN("#t", 1.4, 30)]; d = 3.8
    elif gid == "a_kaba":        # years later, Bilāl gives the adhān on top of the Kaʿbah
        b += [f'<svg class="full" viewBox="0 0 1080 1920">{stars(5, 90)}<rect x="290" y="900" width="500" height="520" fill="#111"/><rect x="290" y="1010" width="500" height="44" fill="{GOLD}"/>'
              f'<rect x="440" y="1250" width="90" height="170" fill="{GOLD}" opacity=".85"/>{figure(540, 900, 0.7, PAPER, "bil")}</svg>',
              '<div class="ar g" id="ak" style="top:330px;font-size:150px">اللّٰهُ أَكْبَر</div>', '<div class="tag" id="e" style="top:560px">the adhān from the Kaʿbah</div>']
        j += [IN("#bil", 0.05, 30), POP("#ak", 0.9, 0.6), IN("#e", 1.3, 20),
              f'tl.fromTo("#ak", {{scale:1}}, {{scale:1.06, duration:0.6, yoyo:true, repeat:3, ease:"sine.inOut", immediateRender:false}}, 1.4);']; d = 4.0
    elif gid == "a_jannah":      # "I heard your footsteps ahead of me in Jannah" (al-Bukhārī 1149)
        b += [f'<svg class="full" viewBox="0 0 1080 1920"><circle id="lt" cx="540" cy="760" r="500" fill="#fff1c4" opacity="0"/>'
              + "".join(f'<ellipse class="fs" cx="{x}" cy="{y}" rx="26" ry="44" fill="{GOLD}" opacity="0" transform="rotate({r} {x} {y})"/>' for x, y, r in
                        ((480, 1200, -10), (600, 1080, 10), (470, 960, -10), (590, 840, 10), (480, 720, -10), (600, 600, 10))) + '</svg>',
              card("c", "سَمِعْتُ <b>دَفَّ نَعْلَيْكَ</b> بَيْنَ يَدَيَّ فِي الْجَنَّةِ", "“I heard <i>your footsteps</i> ahead of me in Jannah.”", "AL-BUKHĀRĪ 1149", 1260)]
        j += [f'tl.fromTo("#lt", {{opacity:0}}, {{opacity:0.3, duration:1.2, ease:"power3.out"}}, 0.05);',
              f'tl.to(".fs", {{opacity:1, duration:0.2, stagger:0.25, ease:"power2.out"}}, 0.3);', IN("#c", 1.6, 40)]; d = 4.6
    # the edit's new ones (6 Nov 2026), for the lines he recorded facing the window: that footage is never shown, these cover all of it
    elif gid == "a_why":         # "And why did Bilāl choose that word? Why aḥad?"
        b += ['<div class="big" id="t" style="top:520px;font-size:200px">WHY</div>', '<div class="ar g" id="w" style="top:760px;font-size:300px">أَحَد</div>',
              '<div class="big g" id="q" style="top:1260px;font-size:260px">?</div>']
        j += [IN("#t", 0.05, 30), POP("#w", 1.0, 0.6), SLAM("#q", 1.8)]; d = 3.0
    elif gid == "a_deny":        # "Umayyah wanted him to deny Muḥammad ﷺ, and worship al-Lāt and al-ʿUzzā, to put partners besides Allah"
        b += ['<div class="tag" id="h" style="top:250px;font-size:60px">what Umayyah demanded</div>',
              f'<div class="stamp" id="s" style="left:110px;top:400px;font-size:120px;transform:rotate(-4deg)">DENY MUḤAMMAD</div>',
              f'<svg class="full" viewBox="0 0 1080 1920"><g id="idols"><rect x="190" y="760" width="200" height="420" rx="20" fill="#5a4a3a"/>'
              f'<rect x="690" y="760" width="200" height="420" rx="20" fill="#5a4a3a"/></g></svg>',
              '<div class="mini" id="l0" style="left:190px;top:1200px;width:200px;text-align:center;font-size:62px">اللّات</div>',
              '<div class="mini" id="l1" style="left:690px;top:1200px;width:200px;text-align:center;font-size:62px">العُزّى</div>',
              '<div class="big" id="t" style="top:1450px;font-size:100px">PARTNERS<br><span class="r">BESIDES ALLAH</span></div>']
        j += [IN("#h", 0.05, 20), SLAM("#s", 0.8), IN("#idols", 1.8, 40), IN("#l0", 2.0, 10), IN("#l1", 2.3, 10), SLAM("#t", 3.2)]; d = 4.6
    elif gid == "a_noroom":      # "the one word that leaves no room for any partnership: aḥad"
        b += ['<div class="ar" id="al" style="top:520px;font-size:200px">اللّٰه</div>',
              '<div class="big" id="p0" style="top:880px;left:120px;right:auto;width:300px;font-size:150px;color:#7f9590">+ ?</div>',
              '<div class="big" id="p1" style="top:880px;left:660px;right:auto;width:300px;font-size:150px;color:#7f9590">+ ?</div>',
              f'<svg class="full" viewBox="0 0 1080 1920"><path id="x0" d="M150 870 L 400 1060 M400 870 L 150 1060" stroke="{RED}" stroke-width="20" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" fill="none"/>'
              f'<path id="x1" d="M690 870 L 940 1060 M940 870 L 690 1060" stroke="{RED}" stroke-width="20" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" fill="none"/></svg>',
              '<div class="big" id="t" style="top:1150px;font-size:100px">NO ROOM FOR<br>ANY <span class="g">PARTNER</span></div>',
              '<div class="ar g" id="w" style="top:1420px;font-size:220px">أَحَد</div>']
        j += [IN("#al", 0.05, 30), POP("#p0", 0.5, 0.6), POP("#p1", 0.7, 0.6), DRAW("#x0", 1.4, 0.3), DRAW("#x1", 1.6, 0.3), IN("#t", 1.7, 30), SLAM("#w", 3.0)]; d = 4.4
    elif gid == "a_tawhid":      # "That's the whole of tawḥīd in a single word."
        b += ['<div class="ar g" id="w" style="top:380px;font-size:280px">أَحَد</div>', '<div class="big" id="eq" style="top:860px;font-size:160px">=</div>',
              '<div class="big g" id="t" style="top:1060px;font-size:220px">TAWḤĪD</div>', '<div class="tag" id="e" style="top:1330px;font-size:64px">Allah is One, with no partner</div>',
              '<div class="big" id="o" style="top:1520px;font-size:96px">IN ONE WORD</div>']
        j += [POP("#w", 0.05, 0.7), IN("#eq", 0.6, 20), SLAM("#t", 1.0), IN("#e", 1.6, 20), IN("#o", 2.4, 30)]; d = 3.6
    elif gid == "a_fear":        # "…was able to say this word with so much conviction and without fear."
        b += [f'<svg class="full" viewBox="0 0 1080 1920">{SUNSAND}<circle id="lt" cx="540" cy="900" r="420" fill="#fff4cf" opacity="0"/></svg>',
              '<div class="ar" id="w" style="top:700px;font-size:280px">أَحَد</div>',
              '<div class="big" id="c" style="top:1300px;font-size:110px">WITH <span class="g">CONVICTION</span></div>',
              '<div class="big" id="f" style="top:1460px;font-size:110px">WITHOUT <span class="r">FEAR</span></div>']
        j += [POP("#w", 0.05, 0.8), f'tl.fromTo("#lt", {{opacity:0}}, {{opacity:0.45, duration:1.2, ease:"power3.out"}}, 0.3);', IN("#c", 1.0, 30), SLAM("#f", 2.0)]; d = 3.6
    elif gid == "a_very":        # "Bilāl wasn't just refusing their idols, he was saying the very thing they were trying to make him deny."
        b += [f'<svg class="full" viewBox="0 0 1080 1920"><g id="idols"><rect x="190" y="360" width="200" height="420" rx="20" fill="#5a4a3a"/>'
              f'<rect x="690" y="360" width="200" height="420" rx="20" fill="#5a4a3a"/>'
              + "".join(f'<path class="cr" d="{d}" fill="none" stroke="{GOLD}" stroke-width="7" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>' for d in (
                  "M290 360 L 270 500 L 310 580 L 280 780", "M790 360 L 810 490 L 770 600 L 800 780")) + '</g></svg>',
              '<div class="big" id="r" style="top:860px;font-size:96px">NOT JUST <span class="r">REFUSING</span></div>',
              '<div class="ar g" id="w" style="top:560px;font-size:280px">أَحَد</div>',
              '<div class="big" id="t" style="top:1150px;font-size:96px">THE VERY THING<br>THEY WANTED HIM<br>TO <span class="g">DENY</span></div>']
        j += [IN("#idols", 0.05, 30), IN("#r", 0.4, 30), f'tl.fromTo(".cr", {{strokeDashoffset:1}}, {{strokeDashoffset:0, duration:0.35, stagger:0.2, ease:"power2.inOut"}}, 1.0);',
              f'tl.to("#idols, #r", {{opacity:0, y:120, duration:0.5, ease:"power2.in"}}, 1.8);', SLAM("#w", 2.4), IN("#t", 3.0, 30)]; d = 4.6
    elif gid == "a_say":         # "Next time you're reading Sūrat al-Ikhlāṣ, say aḥad with as much conviction as Bilāl did."
        b += [card("c1", "قُلْ هُوَ اللّٰهُ <b>أَحَدٌ</b>", "“Say: He is Allah, <i>the One</i>.”", "AL-IKHLĀṢ 112:1", 460),
              '<div class="big" id="t" style="top:1080px;font-size:130px">SAY IT<br>LIKE <span class="g">BILĀL</span></div>']
        j += [IN("#c1", 0.05, 40), SLAM("#t", 2.0)]; d = 3.6
    elif gid == "a_none":        # "Aḥad is one with no second, no equal, no parts" (the owner's edit, 7 Nov 2026)
        b += ['<div class="ar g" id="w" style="top:360px;font-size:260px">أَحَد</div>']
        b += [f'<div class="big" id="n{i}" style="top:{860 + i * 210}px;font-size:140px">NO <span class="g">{x}</span></div>' for i, x in enumerate(("SECOND", "EQUAL", "PARTS"))]
        j += [POP("#w", 0.05, 0.7)] + [SLAM(f"#n{i}", 0.9 + i * 0.7) for i in range(3)]; d = 3.6
    elif gid == "a_alone":       # "used like that, it's used exclusively for Allah alone"
        b += ['<div class="ar" id="al" style="top:520px;font-size:300px">اللّٰه</div>', '<div class="tag" id="e" style="top:1000px;font-size:64px">aḥad, used like that, is only ever said of</div>',
              '<div class="big g" id="t" style="top:1150px;font-size:170px">ALLAH ALONE</div>']
        j += [POP("#al", 0.05, 0.7), f'tl.fromTo("#al", {{scale:1}}, {{scale:1.06, duration:3, ease:"sine.inOut"}}, 0.5);', IN("#e", 0.8, 20), SLAM("#t", 2.0)]; d = 3.4
    elif gid == "a_qul":         # "the word Allah uses for Himself in the Qur'an: qul huwa Allāhu aḥad"
        b += ['<div class="tag" id="h" style="top:420px;font-size:60px">the word Allah uses for Himself</div>',
              card("c1", "قُلْ هُوَ اللّٰهُ <b>أَحَدٌ</b>", "“Say: He is Allah, <i>the One</i>.”", "AL-IKHLĀṢ 112:1", 640)]
        j += [IN("#h", 0.05, 20), IN("#c1", 0.8, 40), f'tl.fromTo("#c1", {{scale:1}}, {{scale:1.05, duration:3, ease:"sine.inOut"}}, 1.4);']; d = 3.6
    # the owner's re-cut (8 Nov 2026: "more detailed, more realistic… show what I'm describing"): Makkah, the dragging, the sand, the boulder
    elif gid == "a_makkah":      # "1400 years ago, Makkah, scorching sun"
        b += [f'<svg class="full" viewBox="0 0 1080 1920">{DEFS}<g id="sc" filter="url(#haze)">'
              '<rect width="1080" height="1920" fill="url(#sky)"/><circle id="sun" cx="540" cy="360" r="150" fill="#fffbe8"/>'
              '<circle id="sung" cx="540" cy="360" r="330" fill="url(#glow)"/>'
              '<path d="M-20 1010 L120 820 L230 900 L360 760 L520 880 L640 790 L790 900 L930 800 L1100 950 L1100 1100 L-20 1100Z" fill="#b98a5c"/>'
              '<path d="M-20 1090 L90 960 L260 1040 L420 930 L600 1050 L760 960 L940 1060 L1100 990 L1100 1200 L-20 1200Z" fill="#8f6440"/>'
              '<path d="M-20 1090 L90 960 L260 1040 L420 930 L600 1050 L760 960 L940 1060 L1100 990 L1100 1200 L-20 1200Z" fill="url(#grainp)" opacity=".35"/>'
              + HOUSES + '<g id="kaba"><rect x="470" y="1150" width="140" height="150" fill="#16130f"/><rect x="470" y="1150" width="140" height="150" fill="url(#shadeR)"/>'
              '<rect x="470" y="1182" width="140" height="14" fill="#c9a24a"/></g>'
              '<path d="M-20 1330 C 260 1270 640 1360 1100 1300 L1100 1920 L-20 1920Z" fill="url(#sand)"/>'
              '<path d="M-20 1330 C 260 1270 640 1360 1100 1300 L1100 1920 L-20 1920Z" fill="url(#grainp)" opacity=".5"/>'
              + DUST + '</g></svg>',
              '<div class="big" id="t" style="top:1520px;font-size:120px">MAKKAH</div>',
              '<div class="tag" id="e" style="top:1660px;font-size:56px;color:#3b2a1c">about 1,400 years ago · midday</div>']
        j += [f'tl.fromTo("#sc", {{scale:1.0, transformOrigin:"50% 60%"}}, {{scale:1.08, duration:6, ease:"sine.inOut"}}, 0.05);', HAZE,
              IN("#e", 0.05, 20), SLAM("#t", 1.2), f'tl.fromTo("#sung", {{scale:0.8, opacity:0.6, transformOrigin:"50% 50%"}}, {{scale:1.25, opacity:1, duration:1.2, ease:"power2.out"}}, 2.0);',
              f'tl.fromTo("#sun", {{scale:1, transformOrigin:"50% 50%"}}, {{scale:1.12, duration:1.0, ease:"power2.out"}}, 2.0);', DRIFT]; d = 6.0
    elif gid == "a_drag":        # "a black slave from Abyssinia is dragged out by his tyrant master, Umayyah"
        b += [f'<svg class="full" viewBox="0 0 1080 1920">{DEFS}<g id="sc" filter="url(#haze)">'
              '<rect width="1080" height="1920" fill="url(#sky)"/><circle cx="880" cy="260" r="260" fill="url(#glow)"/>'
              '<rect x="-20" y="560" width="470" height="720" fill="#a9825c"/><rect x="-20" y="560" width="470" height="720" fill="url(#grainp)" opacity=".4"/>'
              + "".join(f'<rect x="{x}" y="{y}" width="110" height="52" fill="none" stroke="#8a6646" stroke-width="3"/>' for x in range(-20, 450, 112) for y in range(560, 1280, 104))
              + '<rect x="130" y="900" width="170" height="380" rx="80" fill="#2a1d14"/><rect x="-20" y="540" width="490" height="30" fill="#7d5b3d"/>'
              '<path d="M-20 1270 C 300 1240 700 1300 1100 1250 L1100 1920 L-20 1920Z" fill="url(#sand)"/>'
              '<path d="M-20 1270 C 300 1240 700 1300 1100 1250 L1100 1920 L-20 1920Z" fill="url(#grainp)" opacity=".5"/>'
              '<ellipse cx="560" cy="1500" rx="420" ry="40" fill="#5e3d22" opacity=".35"/>'
              '<g id="grp"><g id="um" transform="translate(760 1470)">' + ROBED("#6e1f1f", "#f3ead8", 1.15, "#c9a24a") + '</g>'
              '<path id="rope" d="M690 1250 C 600 1300 520 1330 430 1360" stroke="#6b4a2a" stroke-width="9" fill="none" stroke-linecap="round"/>'
              '<g id="bl" transform="translate(300 1440)">' + DRAGGED + '</g></g>' + PUFFS + '</g></svg>',
              '<div class="big" id="t" style="top:300px;font-size:104px;color:#17262B">DRAGGED OUT</div>',
              '<div class="tag" id="e" style="top:420px;font-size:52px;color:#3b2a1c;text-shadow:none">by his master, Umayyah ibn Khalaf</div>']
        j += [f'tl.fromTo("#grp", {{x:-380}}, {{x:120, duration:5.5, ease:"power1.inOut"}}, 0.05);', HAZE,
              f'tl.fromTo("#bl", {{rotation:-4, svgOrigin:"300 1440"}}, {{rotation:3, duration:0.5, yoyo:true, repeat:9, ease:"sine.inOut"}}, 0.05);',
              f'tl.fromTo(".pf", {{opacity:0, scale:0.4, x:0}}, {{opacity:0.7, scale:1.6, x:-120, duration:0.9, stagger:{{each:0.35, repeat:-1}}, ease:"power2.out"}}, 0.3);',
              SLAM("#t", 1.0), IN("#e", 2.5, 20)]; d = 6.0
    elif gid == "a_burn":        # "placed on the ground, where the sand is so hot it starts to burn away at your skin"
        b += [f'<svg class="full" viewBox="0 0 1080 1920">{DEFS}<g id="sc">'
              '<rect width="1080" height="1920" fill="url(#sky)"/><rect id="hot" y="1120" width="1080" height="800" fill="url(#hotsand)"/>'
              '<rect y="1120" width="1080" height="800" fill="url(#grainp)" opacity=".6"/>'
              + "".join(f'<path class="rip" d="M-40 {y} C 200 {y - 30} 420 {y + 30} 640 {y} S 1000 {y - 25} 1120 {y}" stroke="#ffcf8a" stroke-width="3" fill="none" opacity=".25"/>' for y in range(1100, 1920, 90))
              + '<rect y="0" width="1080" height="1000" fill="url(#sky)" opacity=".55"/>'
              '<g transform="translate(560 1130) scale(1.35)">' + LYING + '</g>'
              '<path id="burn" d="M-40 1150 C 300 1125 760 1125 1140 1150 L1140 1205 C 760 1175 300 1175 -40 1205Z" fill="#ff5a1f" opacity="0" filter="url(#soft)"/>'
              + "".join(f'<path class="smk" d="M{x} 1120 c -30 -60 30 -120 0 -180 c -30 -60 30 -120 0 -180" stroke="#e9e0d6" stroke-width="16" fill="none" stroke-linecap="round" opacity="0" filter="url(#soft)"/>' for x in (200, 420, 640, 860))
              + '</g></svg>',
              '<div class="big" id="t" style="top:280px;font-size:110px;color:#17262B">THE SAND <span class="r">BURNS</span></div>',
              '<div class="tag" id="e" style="top:420px;font-size:56px;color:#3b2a1c;text-shadow:none">it starts to burn away at his skin</div>']
        j += [f'tl.fromTo("#sc", {{scale:1.12, transformOrigin:"50% 60%"}}, {{scale:1.0, duration:7, ease:"sine.out"}}, 0.05);',
              f'tl.fromTo("#hot", {{opacity:0.35}}, {{opacity:1, duration:2.5, ease:"power2.in"}}, 1.5);',
              f'tl.fromTo(".rip", {{y:0}}, {{y:-60, duration:1.2, repeat:5, ease:"none"}}, 0.05);',
              IN("#t", 1.5, 30), f'tl.to("#burn", {{opacity:0.75, duration:1.4, ease:"power2.in"}}, 2.6);',
              f'tl.fromTo(".smk", {{opacity:0, y:40}}, {{opacity:0.45, y:-160, duration:1.6, stagger:{{each:0.3, repeat:-1}}, ease:"sine.out"}}, 3.0);', IN("#e", 3.8, 20)]; d = 7.0
    elif gid == "a_boulder":     # "placed on his back, and the men grab a big boulder and place it on his chest"
        b += [f'<svg class="full" viewBox="0 0 1080 1920">{DEFS}<g id="sc" filter="url(#haze)">'
              '<rect width="1080" height="1920" fill="url(#sky)"/><circle cx="540" cy="300" r="300" fill="url(#glow)"/><circle cx="540" cy="300" r="120" fill="#fffbe8"/>'
              '<path d="M-20 1080 C 300 1030 700 1100 1100 1050 L1100 1920 L-20 1920Z" fill="url(#sand)"/>'
              '<path d="M-20 1080 C 300 1030 700 1100 1100 1050 L1100 1920 L-20 1920Z" fill="url(#grainp)" opacity=".5"/>'
              '<ellipse cx="540" cy="1420" rx="380" ry="46" fill="#5e3d22" opacity=".35"/>'
              '<g transform="translate(540 1380)">' + LYING + '</g>'
              '<g id="carry"><g transform="translate(250 1380)">' + ROBED("#5b4632", "#e9dfcb", 1.0) + '</g><g transform="translate(830 1380)">' + ROBED("#4b3a2a", "#e9dfcb", 1.0) + '</g>'
              '<g id="rock">' + BOULDER + '</g></g>' + IMPACT + '</g></svg>',
              '<div class="big" id="t" style="top:1560px;font-size:104px">A <span class="r">BOULDER</span></div>',
              '<div class="big" id="t2" style="top:1690px;font-size:80px">ON HIS CHEST</div>']
        j += [f'tl.fromTo("#carry", {{x:620, y:0}}, {{x:0, y:0, duration:1.6, ease:"power2.out"}}, 1.0);', HAZE,
              f'tl.fromTo("#rock", {{y:0}}, {{y:-160, duration:0.6, ease:"power2.out"}}, 3.0);', SLAM("#t", 3.0),
              f'tl.to("#rock", {{y:150, duration:0.32, ease:"power3.in"}}, 4.1);', f'tl.to("#carry > g:not(#rock)", {{x:"+=0", opacity:0.0, duration:0.6, ease:"power2.in"}}, 4.6);',
              f'tl.fromTo(".imp", {{opacity:0.9, scale:0.3}}, {{opacity:0, scale:2.2, duration:0.8, stagger:0.05, ease:"expo.out", immediateRender:false}}, 4.42);',
              f'tl.fromTo("#cam", {{x:-16, y:10}}, {{x:16, y:-10, duration:0.05, yoyo:true, repeat:7, ease:"sine.inOut", immediateRender:false}}, 4.42);', 'tl.set("#cam", {x:0, y:0}, 4.85);',
              IN("#t2", 4.5, 20)]; d = 7.0
    # ---------------- Dajjāl (#316) ----------------
    elif gid == "d_word":       # "Did you know there's more than one Dajjāl? Let me explain." (owner's hook, 2 Nov): the word, then two more ghost in
        b += ['<div class="ar" id="w" style="top:600px;font-size:280px">دَجّال</div>',
              '<div class="ar" id="w1" style="top:400px;left:40px;right:auto;width:440px;font-size:130px;color:#7f9590">دَجّال</div>',
              '<div class="ar" id="w2" style="top:400px;left:600px;right:auto;width:440px;font-size:130px;color:#7f9590">دَجّال</div>',
              '<div class="big" id="t" style="top:1180px;font-size:130px">MORE THAN<br><span class="g">ONE?</span></div>']
        j += [POP("#w", 0.05, 0.7), POP("#w1", 1.1, 0.4), POP("#w2", 1.3, 0.4), SLAM("#t", 1.6)]; d = 3.2
    elif gid == "d_thirty":      # "there could be hundreds, even thousands living amongst us" (as filmed, 2 Nov): the word multiplies, the count runs past 1,000
        for i in range(30):
            x, y = 70 + (i % 5) * 190, 300 + (i // 5) * 190
            b.append(f'<div class="ar" id="m{i}" style="left:{x}px;right:auto;top:{y}px;width:180px;font-size:66px;color:#9fb6b0">دَجّال</div>')
        b.append('<div class="big" id="n" style="top:1520px;font-size:200px"><span id="nn">0</span><span class="g" id="pl" style="opacity:0">+</span></div>')
        j += [f'tl.fromTo(".ar", {{opacity:0, scale:0.5}}, {{opacity:1, scale:1, duration:0.25, stagger:0.06, ease:"back.out(1.4)"}}, 0.05);',
              IN("#n", 0.05, 0), '(() => { const o = {v:0}, el = document.getElementById("nn"); tl.to(o, {v:1000, duration:2.0, ease:"power2.out", onUpdate:() => el.textContent = Math.round(o.v).toLocaleString("en-GB")}, 0.05); })();',
              POP("#pl", 2.1, 0.4)]; d = 3.2
    elif gid == "d_root":        # "the word dajjāl comes from the root dāl, jīm, lām. Dajala, which means to cover or coat something" (as filmed)
        for i, (l, x) in enumerate((("د", 700), ("ج", 440), ("ل", 180))):
            b.append(f'<div class="ar g" id="l{i}" style="top:520px;left:{x}px;right:auto;width:200px;font-size:220px">{l}</div>')
            b.append(f'<div class="tag" id="n{i}" style="top:850px;left:{x}px;right:auto;width:200px">{("dāl", "jīm", "lām")[i]}</div>')
            j += [POP(f"#l{i}", 0.05 + i * 1.1, 0.5), IN(f"#n{i}", 0.3 + i * 1.1, 10)]
        b += ['<div class="ar" id="v" style="top:1060px;font-size:150px">دَجَلَ</div>', '<div class="big" id="t" style="top:1330px;font-size:100px">TO <span class="g">COVER</span>, TO <span class="g">COAT</span></div>']
        j += [IN("#v", 3.6, 30), SLAM("#t", 4.4)]; d = 6.0
    elif gid == "d_camel":       # "the Arabs used it for coating a sick camel with tar to hide what was underneath" (as filmed)
        b += [f'<svg class="full" viewBox="0 0 1080 1920"><g id="cam1"><path d="M300 1100 C 300 960 360 880 470 890 C 520 800 600 800 640 890 C 700 880 740 820 760 740 C 770 700 820 700 830 740 L 840 800 C 860 860 820 960 760 1000 L 760 1100 L 720 1100 L 720 1020 L 400 1020 L 400 1100 L 360 1100 Z" fill="#c98a4a"/>'
              + "".join(f'<circle cx="{x}" cy="{y}" r="{r_}" fill="#8a5a3a"/>' for x, y, r_ in ((430, 930, 26), (560, 960, 34), (650, 920, 22), (500, 990, 18)))
              + f'</g><defs><clipPath id="cc"><path d="M300 1100 C 300 960 360 880 470 890 C 520 800 600 800 640 890 C 700 880 740 820 760 740 C 770 700 820 700 830 740 L 840 800 C 860 860 820 960 760 1000 L 760 1100 L 720 1100 L 720 1020 L 400 1020 L 400 1100 L 360 1100 Z"/></clipPath></defs>'
              f'<g clip-path="url(#cc)"><rect id="tar" x="280" y="680" width="580" height="440" fill="#141414" opacity=".92"/></g></svg>',   # the camel's shape on a wrapper: the sweep's own clip would replace it
              '<div class="big" id="t" style="top:430px;font-size:110px">COATED WITH <span class="g">TAR</span></div>', '<div class="tag" id="e" style="top:1220px">to hide what was underneath</div>']
        j += [IN("#cam1", 0.05, 30), IN("#t", 0.3, 30), f'tl.fromTo("#tar", {{clipPath:"inset(0 100% 0 0)"}}, {{clipPath:"inset(0 0% 0 0)", duration:1.1, ease:"power2.inOut"}}, 1.4);', IN("#e", 2.4, 20)]; d = 4.4
    elif gid == "d_hadith":      # al-Bukhārī 3609
        b += [card("c", "دَجّالُونَ كَذّابُونَ <b>قَرِيبٌ مِنْ ثَلاثِينَ</b>، كُلُّهُمْ يَزْعُمُ أَنَّهُ رَسُولُ اللّٰهِ",
                   "“…until about <i>thirty</i> dajjāls, liars, appear, each claiming to be a messenger of Allah.”", "AL-BUKHĀRĪ 3609", 640)]
        j += [IN("#c", 0.05, 40)]; d = 4.5
    elif gid == "d_gild":        # د ج ل: to coat; gilding something cheap so it looks precious
        b += ['<div class="ar g" id="rt" style="top:260px;font-size:150px;letter-spacing:.25em">د ج ل</div>', '<div class="tag" id="e" style="top:480px">to coat · to cover · to gild</div>',
              f'<svg class="full" viewBox="0 0 1080 1920"><g id="rust"><rect x="290" y="760" width="500" height="380" rx="24" fill="#6b4a32"/>'
              + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#4a3020"/>' for x, y, r in ((360, 820, 30), (700, 900, 40), (450, 1060, 34), (620, 1080, 22), (520, 880, 18)))
              + f'</g><rect id="gold" x="290" y="760" width="500" height="380" rx="24" fill="url(#gg)"/><defs><linearGradient id="gg" x1="0" x2="1"><stop offset="0" stop-color="#b8892a"/>'
              f'<stop offset=".5" stop-color="#ffe08a"/><stop offset="1" stop-color="#b8892a"/></linearGradient></defs></svg>',
              '<div class="big" id="t" style="top:1260px;font-size:96px">GOLD PAINT<br>OVER A <span class="r">LIE</span></div>']
        j += [POP("#rt", 0.05, 0.6), IN("#e", 0.5, 20), IN("#rust", 0.3, 30),
              f'tl.fromTo("#gold", {{clipPath:"inset(0 100% 0 0)"}}, {{clipPath:"inset(0 0% 0 0)", duration:1.0, ease:"power2.inOut"}}, 1.6);', IN("#t", 2.6, 30)]; d = 4.6
    elif gid == "d_form":        # dajala → dajjāl, the doubled jīm, like kadhdhāb
        b += ['<div class="ar" id="v" style="top:330px;font-size:160px">دَجَلَ</div>', '<div class="tag" id="ve" style="top:560px">to coat (once)</div>',
              '<div class="ar" id="w" style="top:760px;font-size:200px">دَ<span class="g">جّ</span>ال</div>', '<div class="tag" id="we" style="top:1030px">dajjāl: <i style="color:#E9B949">does it again and again</i></div>',
              '<div class="ar" id="k" style="top:1220px;font-size:130px;color:#9fb6b0">كَ<span class="g">ذّ</span>اب</div>', '<div class="tag" id="ke" style="top:1420px">like kadhdhāb: a liar who never stops</div>']
        j += [IN("#v", 0.05, 20), IN("#ve", 0.3, 20), POP("#w", 1.0, 0.6), IN("#we", 1.4, 20),
              f'tl.fromTo("#w .g", {{textShadow:"0 0 0px #E9B949"}}, {{textShadow:"0 0 40px #E9B949", duration:0.5, yoyo:true, repeat:3, ease:"sine.inOut"}}, 1.4);', IN("#k", 2.6, 20), IN("#ke", 2.9, 20)]; d = 4.6
    elif gid == "d_one":         # the thirty shrink away; one large silhouette: al-Masīḥ ad-Dajjāl
        for i in range(10):
            b.append(f'<div class="ar" id="m{i}" style="left:{60 + (i % 5) * 200}px;right:auto;top:{300 + (i // 5) * 160}px;width:180px;font-size:60px;color:#9fb6b0;opacity:1">دَجّال</div>')
        b += [f'<svg class="full" viewBox="0 0 1080 1920">{figure(540, 1500, 2.6, "#050a0c", "big1")}</svg>',
              '<div class="ar g" id="w" style="top:620px;font-size:130px">المَسِيحُ الدَّجّال</div>', '<div class="tag" id="e" style="top:840px">al-Masīḥ ad-Dajjāl · the greatest of them</div>']
        j += [f'tl.to(".ar:not(#w)", {{opacity:0, scale:0.3, duration:0.4, stagger:0.04, ease:"power2.in"}}, 0.3);',
              f'tl.fromTo("#big1", {{opacity:0, y:200}}, {{opacity:1, y:0, duration:0.9, ease:"power3.out"}}, 0.9);', POP("#w", 1.6, 0.6), IN("#e", 2.0, 20)]; d = 4.0
    elif gid == "d_doors":       # something like Paradise and Fire; what he calls Paradise is the Fire (al-Bukhārī 3338)
        b += [f'<svg class="full" viewBox="0 0 1080 1920"><defs><radialGradient id="fire"><stop offset="0" stop-color="#ffcc55"/><stop offset=".6" stop-color="#e2571f"/><stop offset="1" stop-color="#7a1a0a"/></radialGradient></defs>'
              f'<path id="fl" d="M200 1300 L 200 640 C 200 470 480 470 480 640 L 480 1300 Z" fill="url(#fire)" opacity="0"/>'
              f'<path id="gd" d="M200 1300 L 200 640 C 200 470 480 470 480 640 L 480 1300 Z" fill="{GOLD}"/>'
              f'<path id="cr" d="M340 520 L 310 700 L 370 860 L 300 1050 L 360 1300" fill="none" stroke="#7a1a0a" stroke-width="10" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>'
              f'<path d="M600 1300 L 600 640 C 600 470 880 470 880 640 L 880 1300 Z" fill="#3a1410"/></svg>',
              '<div class="tag" id="l0" style="top:1340px;left:200px;right:auto;width:280px">“paradise”</div>', '<div class="tag" id="l1" style="top:1340px;left:600px;right:auto;width:280px">“fire”</div>',
              card("c", "فَالَّتِي يَقُولُ إِنَّها الجَنَّةُ <b>هِيَ النّارُ</b>", "“what he calls Paradise <i>is the Fire</i>.”", "AL-BUKHĀRĪ 3338", 1480)]
        j += [IN("#gd", 0.05, 30), IN("#l0", 0.3, 10), IN("#l1", 0.5, 10), DRAW("#cr", 1.2, 0.5),
              f'tl.to("#gd", {{opacity:0, duration:0.5, ease:"power2.in"}}, 1.8);', f'tl.to("#fl", {{opacity:1, duration:0.5, ease:"power2.out"}}, 1.8);', IN("#c", 2.4, 40)]; d = 4.8
    elif gid == "d_masih":       # al-Masīḥ ×2: ʿĪsā the true one, the Dajjāl the false; ʿĪsā ends him (Muslim 2937)
        b += ['<div class="ar g" id="w0" style="top:420px;font-size:150px">المَسِيح</div>', '<div class="tag" id="e0" style="top:640px">ʿĪsā ؑ · the true one</div>',
              '<div class="ar" id="w1" style="top:900px;font-size:150px;color:#7a8a8c">المَسِيح</div>', '<div class="tag" id="e1" style="top:1120px">the Dajjāl · the false one</div>',
              f'<svg class="full" viewBox="0 0 1080 1920"><path id="cr" d="M300 960 L 420 1010 L 520 950 L 640 1030 L 780 980" fill="none" stroke="{RED}" stroke-width="10" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/></svg>',
              '<div class="tag" id="ref" style="top:1300px;color:#E9B949">ʿĪsā ends him · Muslim 2937</div>']
        j += [POP("#w0", 0.05, 0.6), IN("#e0", 0.4, 20), POP("#w1", 1.0, 0.6), IN("#e1", 1.4, 20), DRAW("#cr", 2.0, 0.4),
              f'tl.to("#w1", {{opacity:0.25, duration:0.5, ease:"power2.in"}}, 2.4);', IN("#ref", 2.6, 20)]; d = 4.2
    elif gid == "d_kafir":       # kāfir written between his eyes; every believer reads it, literate or not
        b += [f'<svg class="full" viewBox="0 0 1080 1920"><circle cx="540" cy="760" r="320" fill="#8a6a50"/><path d="M220 1300 C 240 1000 840 1000 860 1300 Z" fill="#1a1a1a"/></svg>',
              '<div class="ar" id="k" style="top:540px;font-size:150px;color:#1a0f0a;letter-spacing:.2em">ك ف ر</div>',
              card("c", "مَكْتُوبٌ بَيْنَ عَيْنَيْهِ كافِرٌ، <b>يَقْرَؤُهُ كُلُّ مُؤْمِنٍ</b> كاتِبٍ وَغَيْرِ كاتِبٍ",
                   "“Between his eyes is written <i>kāfir</i>; every believer will read it, whether they can write or not.”", "AL-BUKHĀRĪ 7131 · MUSLIM 2934", 1240)]
        j += [f'tl.fromTo("#k", {{opacity:0, filter:"blur(12px)"}}, {{opacity:1, filter:"blur(0px)", duration:1.0, ease:"power2.out"}}, 0.5);', IN("#c", 1.7, 40)]; d = 4.8
    elif gid == "d_dua":         # the duʿāʾ in every salah (Muslim 588)
        b += ['<div class="big" id="t" style="top:300px;font-size:96px">IN <span class="g">EVERY</span> SALAH</div>',
              card("c", "اللّٰهُمَّ إِنِّي أَعُوذُ بِكَ مِنْ عَذابِ جَهَنَّمَ، وَمِنْ عَذابِ القَبْرِ، وَمِنْ فِتْنَةِ المَحْيا وَالمَماتِ، وَمِنْ شَرِّ <b>فِتْنَةِ المَسِيحِ الدَّجّالِ</b>",
                   "“O Allah, I seek refuge in You… from the evil of <i>the trial of al-Masīḥ ad-Dajjāl</i>.”", "MUSLIM 588", 560)]
        j += [IN("#t", 0.05, 30), IN("#c", 0.6, 40)]; d = 4.8
    elif gid == "d_kahf":        # the first ten ayahs of al-Kahf protect you (Muslim 809)
        b += ['<div class="ar g" id="w" style="top:300px;font-size:150px">سُورَةُ الكَهْف</div>']
        b += [f'<div class="big" id="n{i}" style="top:{600 + (i // 5) * 180}px;left:{120 + (i % 5) * 170}px;right:auto;width:150px;font-size:110px;color:#9fb6b0">{i + 1}</div>' for i in range(10)]
        b += [card("c", "مَنْ حَفِظَ <b>عَشْرَ آياتٍ</b> مِنْ أَوَّلِ سُورَةِ الكَهْفِ عُصِمَ مِنَ الدَّجّالِ",
                   "“Whoever memorises <i>the first ten ayahs</i> of Sūrat al-Kahf is protected from the Dajjāl.”", "MUSLIM 809", 1040)]
        j += [POP("#w", 0.05, 0.6), f'tl.fromTo("[id^=n]", {{opacity:0, scale:0.5}}, {{opacity:1, scale:1, duration:0.3, stagger:0.12, ease:"back.out(1.4)"}}, 0.5);',
              f'tl.to("[id^=n]", {{color:"{GOLD}", duration:0.3, stagger:0.06, ease:"power2.out"}}, 1.9);', IN("#c", 2.2, 40)]; d = 4.8
    else:
        raise SystemExit(f"no graphic {gid}")
    return d, b, j

SETS = {"insha": "i_no i_chat i_split i_past i_pens i_root i_kahf i_camel i_tawakkul i_worries i_hadid i_allah".split(),
        "ahad": "a_word a_scene a_slam a_root a_count a_ikhlas a_free a_rock a_kaba a_jannah a_why a_deny a_noroom a_tawhid a_fear a_very a_say a_none a_alone a_qul a_makkah a_drag a_burn a_boulder".split(),
        "dajjal": "d_word d_root d_camel d_thirty d_hadith d_gild d_form d_one d_doors d_masih d_kafir d_dua d_kahf".split()}

# Re-timing to a take (WARP, JSON in the environment: {gid: {"at": [[planned s, s in the take's graphic], ...], "d": length}}): every
# tween's start moves through the anchors (straight lines between them, the same pace beyond the ends), so each beat lands on its word.
WARP = __import__("json").loads(os.environ.get("WARP", "{}"))
OUT = os.environ.get("OUT", os.path.join(HERE, "out"))
def warp(gid, js, d):
    w = WARP.get(gid)
    if not w: return js, d
    at = sorted(w["at"])
    def f(t):
        if t <= at[0][0]: return max(0.05, at[0][1] + t - at[0][0])
        for (p0, q0), (p1, q1) in zip(at, at[1:]):
            if t <= p1: return q0 + (t - p0) * (q1 - q0) / (p1 - p0)
        return at[-1][1] + t - at[-1][0]
    import re
    js = [re.sub(r", (\d+(?:\.\d+)?)\);", lambda m: f", {f(float(m.group(1))):.2f});", x) for x in js]
    return js, w.get("d", round(f(d), 2))

def build(gid):
    d, body, js = gfx(gid)
    js, d = warp(gid, js, d)
    out = os.path.join(OUT, gid); a = os.path.join(out, "assets")
    if os.path.exists(out): shutil.rmtree(out)
    os.makedirs(a)
    for f in ("anton-latin-400-normal.woff2", "instrument-serif-latin-400-normal.woff2", "amiri-arabic-700-normal.woff2"): shutil.copy(os.path.join(H.FONTS, f), a)
    shutil.copy(H.GSAP, a)
    open(os.path.join(out, "index.html"), "w").write(f"""<!doctype html><html><head><meta charset="UTF-8"><style>{CSS}</style><script src="assets/gsap.min.js"></script></head>
<body><div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{d}"><div id="cam">
{chr(10).join(body)}</div><div id="vig"></div></div>
<script>const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;</script></body></html>""")
    return out, d

if __name__ == "__main__":
    ids = [g for x in (sys.argv[1:] or list(SETS)) for g in SETS.get(x, [x])]
    for gid in ids:
        out, d = build(gid)
        if os.environ.get("BUILD_ONLY"): print(gid, d); continue
        r = subprocess.run(["npx", "-y", "hyperframes", "render", "-o", f"../{gid}.mp4"], cwd=out, capture_output=True, text=True)
        print(gid, d, "ok" if r.returncode == 0 else r.stdout[-400:] + r.stderr[-400:], flush=True)
