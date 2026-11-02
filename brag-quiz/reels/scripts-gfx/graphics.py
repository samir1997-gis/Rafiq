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
    # ---------------- Dajjāl (#316) ----------------
    elif gid == "d_word":        # "Did you know there's more than one Dajjāl? Let me explain." (owner's hook, 2 Nov): the word, then two more ghost in
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
        "ahad": "a_word a_scene a_slam a_root a_count a_ikhlas a_free a_rock a_kaba a_jannah".split(),
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
