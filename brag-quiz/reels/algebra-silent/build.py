#!/usr/bin/env python3
"""The algebra story as a silent reel (owner, 27 Oct 2026, #299), in the style of the reference he sent ("7 Islamic ways to get rich
by 2027"): a dark maroon room with a checker floor, text typed out with one word in italic serif, a fan of numbered cards, flat icons
on the floor, numbered points ("01 / 05") with a wipe between them, the duʿāʾ in a dark box with its source in a pill. No voice:
only sound effects, the same kinds as the reference (a key tick as text types, a thud when the cards drop, a tick for each card,
pops, low whooshes on the wipes), mixed here into one track.

  python3 brag-quiz/reels/algebra-silent/build.py
  then  cd brag-quiz/reels/algebra-silent/out/v && npx hyperframes render -o ../algebra-silent-raw.mp4
Sources as in the voiced reel (#298): al-Khwārizmī's x² + 10x = 39; algebrista "bone-setter"; the duʿāʾ: al-Tirmidhī 284."""
import html, os, shutil, subprocess
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
V6 = os.path.join(ROOT, "brag-output-v6/composition/assets"); SFX = os.path.join(ROOT, "brag-quiz/sfx")
SR = 48000; END = 999                                             # set at the end, from the last line
INK, MAR, CREAM, GOLD, SKY, BONE = "#17262B", "#B4322A", "#F1ECE0", "#E9B949", "#2E7263", "#EADFC8"   # ink, rubric, paper, gold, verdigris, bone
TEAL = SKY

js, snd, body = [], [], []
T = js.append
def S(name, t, gain=1.0): snd.append((name, t, gain))

def typed(id, parts, t0, rate=0.032, tick=3):
    """Text that types out a character at a time (a key tick every few), from t0; parts: [(text, 'em'|None)]. Returns (html, end)."""
    out, n, t = "", 0, t0
    for txt, st in parts:
        span = ""
        for ch in txt:
            span += f'<span class="ch" id="{id}{n}">{html.escape(ch)}</span>'
            T(f'tl.set("#{id}{n}", {{opacity:1}}, {t:.3f});')
            if n % tick == 0 and ch != " ": S("soft/type.wav", t, 0.5 + 0.3 * ((n * 7) % 5) / 4)
            n += 1; t += rate
        out += f'<em>{span}</em>' if st == "em" else ("<br>" if st == "br" else span)
    return out, t

def words(id, ws, t0, gap=0.28):
    """Arabic, a word at a time (letters must stay joined, so never a letter at a time)."""
    out = ""
    for k, (w, cls) in enumerate(ws):
        out += f'<span class="aw {cls}" id="{id}{k}">{w}</span> '
        T(f'tl.fromTo("#{id}{k}", {{opacity:0, y:14}}, {{opacity:1, y:0, duration:0.25, ease:"power2.out"}}, {t0 + k * gap:.2f});')
        S("soft/tick.wav", t0 + k * gap, 0.7)
    return out

def pop(sel, t, s0=0.4, sound="ref/tap.wav", g=1.0):
    T(f'tl.fromTo("{sel}", {{opacity:0, scale:{s0}}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(2.4)", immediateRender:false}}, {t:.2f});')
    if sound: S(sound, t, g)

def scene(id, t0, t1):
    T(f'tl.set("#{id}", {{opacity:1}}, {t0:.2f});')
    if t1 < END: T(f'tl.set("#{id}", {{opacity:0}}, {t1:.2f});')

WIPES = []
def wipe(t, colour):
    """A panel sweeps across from the right (a low whoosh); the scenes swap while it covers the frame."""
    k = len(WIPES); WIPES.append(f'<div class="wipe" id="w{k}" style="background:{colour}"></div>')
    T(f'tl.fromTo("#w{k}", {{x:1100}}, {{x:0, duration:0.22, ease:"power3.in"}}, {t:.2f});')
    T(f'tl.to("#w{k}", {{x:-1100, duration:0.26, ease:"power3.out"}}, {t + 0.26:.2f});')
    S("ref/swoosh-low.wav", t, 1.0); S("soft/whoosh.wav", t + 0.05, 0.5)
    return t + 0.24

def head(id, num, parts, t0):
    """A point's number, its heading (types out) and returns the html and when the heading is done."""
    h, t = typed(id + "h", parts, t0 + 0.15, rate=0.045, tick=2)
    T(f'tl.fromTo("#{id}n", {{opacity:0}}, {{opacity:1, duration:0.2}}, {t0:.2f});')
    return f'<div class="num" id="{id}n">{num:02d} / 05</div><div class="hd">{h}</div>', t

FIG = lambda x, extra="": f'<div class="fig" style="left:{x}px" {extra}><i></i><b></b></div>'   # the little person on the floor
BONE_SVG = lambda id, w: f'''<svg id="{id}" width="{w}" viewBox="0 0 400 110"><g fill="{BONE}" stroke="{INK}" stroke-width="6">
<path d="M40 30a22 22 0 1 1 30-14h260a22 22 0 1 1 30 14a22 22 0 1 1-30 14v22a22 22 0 1 1-30 14h-260a22 22 0 1 1-30-14a22 22 0 1 1 30-14z" transform="translate(0,6)"/></g></svg>'''

# ---- 0 · hook, then the title and the fan of cards ------------------------------------------------------------------------
hook, t = typed("k", [(" is an", None), ("", "br"), ("Arabic word.", "em")], 0.3, rate=0.05, tick=2); hook = "Algebra" + hook   # a word on frame 0
TITLE_T = 2.0
T(f'tl.set("#hook", {{opacity:0}}, {TITLE_T:.2f});')
T(f'tl.fromTo("#title", {{opacity:0, scale:1.08}}, {{opacity:1, scale:1, duration:0.25, ease:"power2.out"}}, {TITLE_T:.2f});')
ICONS = [  # one per point: the bone, the book, the square, the sign, the prayer mat
    f'<svg viewBox="0 0 100 60" width="78"><path d="M12 22a8 8 0 1 1 11-6h54a8 8 0 1 1 11 6a8 8 0 1 1-11 6v8a8 8 0 1 1-11 6h-54a8 8 0 1 1-11-6a8 8 0 1 1 11-6z" fill="{INK}"/><path d="M48 14l5 9-6 7 5 9" stroke="{CREAM}" stroke-width="3" fill="none"/></svg>',
    f'<svg viewBox="0 0 100 70" width="78"><path d="M50 14C38 6 18 6 6 10v50c12-4 32-4 44 4c12-8 32-8 44-4V10C82 6 62 6 50 14z" fill="{INK}"/><path d="M50 14v50" stroke="{CREAM}" stroke-width="3"/></svg>',
    f'<svg viewBox="0 0 80 80" width="66"><rect x="6" y="6" width="68" height="68" fill="none" stroke="{INK}" stroke-width="6"/><rect x="42" y="42" width="32" height="32" fill="{INK}"/></svg>',
    f'<svg viewBox="0 0 90 80" width="72"><path d="M45 4v14M20 18h50" stroke="{INK}" stroke-width="5"/><rect x="8" y="22" width="74" height="48" rx="6" fill="{INK}"/><path d="M24 46h42" stroke="{CREAM}" stroke-width="7" stroke-linecap="round"/></svg>',
    f'<svg viewBox="0 0 80 90" width="60"><rect x="10" y="6" width="60" height="78" rx="6" fill="{INK}"/><path d="M40 20l14 16v38H26V36z" fill="none" stroke="{CREAM}" stroke-width="4"/></svg>',
]
cards = ""
for i in range(5):
    a = (i - 2) * 15; col = MAR if i == 2 else (CREAM if i % 2 == 0 else SKY)
    fg = CREAM if i == 2 else INK
    if i % 2: fg = CREAM
    icon = ICONS[i] if fg == INK else ICONS[i].replace(f'stroke="{CREAM}"', 'stroke="#@"').replace(f'fill="{INK}"', f'fill="{fg}"').replace(f'stroke="{INK}"', f'stroke="{fg}"').replace('stroke="#@"', f'stroke="{INK}"')
    cards += f'<div class="card" id="cd{i}" style="background:{col};color:{fg}"><span>{i + 1}</span>{icon}</div>'
    if i == 2:
        T(f'tl.fromTo("#cd2", {{opacity:0, y:-260, rotation:0}}, {{opacity:1, y:0, duration:0.3, ease:"power3.in"}}, {TITLE_T:.2f});')
    else:
        k = [1, 3, 0, 4].index(i); tt = 2.75 + k * 0.2
        T(f'tl.fromTo("#cd{i}", {{opacity:0, rotation:0}}, {{opacity:1, rotation:{a}, duration:0.3, ease:"back.out(1.6)"}}, {tt:.2f});')
        S("soft/tick-lo.wav", tt, 1.0); S("ref/click.wav", tt, 0.35)
S("soft/thump.wav", TITLE_T + 0.28, 1.0); S("boom.wav", TITLE_T + 0.28, 0.45)
T(f'tl.fromTo("#cd2", {{scale:1}}, {{scale:1.12, duration:0.18, yoyo:true, repeat:1, ease:"power2.out"}}, 3.75);')
T('tl.fromTo("#spark i", {opacity:0, scale:0}, {opacity:1, scale:1, duration:0.3, stagger:0.04, ease:"back.out(3)"}, 3.75);')
S("ref/click-x2.wav", 3.75, 0.9); S("soft/shimmer.wav", 3.75, 0.35)
spark = "".join(f'<i style="left:{540 + 230 * np.cos(np.radians(200 + 28 * k)):.0f}px;top:{1035 + 150 * np.sin(np.radians(200 + 28 * k)):.0f}px"></i>' for k in range(6))
body.append(f'''<div class="sc" id="s0" style="opacity:1">
 <div class="tx big" id="hook" style="top:360px">{hook}</div>
 <div class="tx big" id="title" style="top:330px">How a <em>broken bone</em><br>became <em>algebra</em></div>
 <div id="fan">{cards}</div><div id="spark">{spark}</div></div>''')

# ---- 1 · you learnt it at school -----------------------------------------------------------------------------------------------
t1 = wipe(5.6, TEAL); scene("s0", 0, t1); A = t1 + 0.25
l1, t = typed("a", [("You learnt algebra at school.", None)], A)
l2, t = typed("b", [("Nobody told you where the ", None), ("word", "em"), (" comes from.", None)], t + 0.35)
pop("#board", A + 0.1, 0.6, "soft/tick-lo.wav")
BOOK_T = t + 0.2
T(f'tl.to("#board", {{opacity:0, scale:0.5, duration:0.2}}, {BOOK_T:.2f});'); pop("#book1", BOOK_T + 0.1, 0.3, "ref/click-x2.wav")
T(f'tl.fromTo("#rays1 i", {{opacity:0, scaleY:0}}, {{opacity:1, scaleY:1, duration:0.25, stagger:0.03}}, {BOOK_T + 0.3:.2f});'); S("soft/shimmer.wav", BOOK_T + 0.3, 0.3)
rays = "".join(f'<i style="transform:rotate({a}deg) translateY(-130px)"></i>' for a in (-60, -35, -12, 12, 35, 60))
body.append(f'''<div class="sc" id="s1"><div class="tx" style="top:420px">{l1}<br>{l2}</div>
 {FIG(300)}<div id="board" class="obj" style="left:560px;top:1000px">x² + 10x = 39</div>
 <div id="book1" class="obj book" style="left:560px;top:1040px"><div id="rays1">{rays}</div><i></i><i></i></div></div>''')

# ---- 01 · the word al-jabr -----------------------------------------------------------------------------------------------------
t2 = wipe(BOOK_T + 2.0, CREAM); scene("s1", t1, t2); A = t2 + 0.2
h, t = head("p1", 1, [("The word ", None), ("al-jabr", "em")], A)
b, t = typed("p1b", [("In Arabic, it means setting a broken bone: putting broken pieces back together.", None)], t + 0.2)
CR = A + 1.3
T(f'tl.to("#b1L", {{x:-40, rotation:-14, duration:0.3, ease:"power2.out"}}, {CR:.2f});'); T(f'tl.to("#b1R", {{x:40, rotation:12, duration:0.3, ease:"power2.out"}}, {CR:.2f});')
S("soft/crack.wav", CR, 1.0); S("soft/thump.wav", CR, 0.5)
SET = t + 0.1
T(f'tl.to("#b1L, #b1R", {{x:0, rotation:0, duration:0.28, ease:"back.out(2)"}}, {SET:.2f});'); S("soft/thump.wav", SET + 0.2, 0.8)
T(f'tl.fromTo("#seam", {{opacity:0}}, {{opacity:1, duration:0.3}}, {SET + 0.25:.2f});'); S("soft/shimmer.wav", SET + 0.25, 0.4)
pop("#jabr", SET + 0.6, 0.4, "ref/click-x2.wav")
T(f'tl.fromTo("#bonebox", {{opacity:0, y:-80}}, {{opacity:1, y:0, duration:0.3, ease:"power3.in"}}, {A + 0.4:.2f});'); S("soft/thump.wav", A + 0.68, 0.7)
bone = BONE_SVG("bb", 520)
body.append(f'''<div class="sc" id="s2"><div class="hdw">{h}</div><div class="tx sm" style="top:560px">{b}</div>
 <div class="ar" id="jabr" style="top:800px">الْجَبْر</div>
 <div class="obj" id="bonebox" style="left:280px;top:1060px;width:520px;height:150px">
  <div id="b1L" style="position:absolute;left:0;top:0;width:262px;height:150px;overflow:hidden;transform-origin:100% 60%">{bone}</div>
  <div id="b1R" style="position:absolute;left:262px;top:0;width:258px;height:150px;overflow:hidden;transform-origin:0 60%"><div style="margin-left:-262px">{bone}</div></div>
  <div id="seam" style="position:absolute;left:254px;top:22px;width:16px;height:100px;background:{GOLD};border-radius:6px;box-shadow:0 0 22px {GOLD}"></div></div></div>''')

# ---- 02 · Baghdad --------------------------------------------------------------------------------------------------------------
t3 = wipe(SET + 2.3, TEAL); scene("s2", t2, t3); A = t3 + 0.2
h, t = head("p2", 2, [("Baghdad", "em")], A)
b, t = typed("p2b", [("1,200 years ago, a scholar called al-\u2060Khwārizmī wrote a book on solving problems this way.", None)], t + 0.2)
pop("#book2", t - 0.6, 0.3, "ref/click-x2.wav")
T(f'tl.fromTo("#rays2 i", {{opacity:0, scaleY:0}}, {{opacity:1, scaleY:1, duration:0.25, stagger:0.03}}, {t - 0.3:.2f});'); S("soft/shimmer.wav", t - 0.3, 0.3)
pop("#ktitle", t + 0.2, 0.7, "soft/tick.wav")
body.append(f'''<div class="sc" id="s3"><div class="hdw">{h}</div><div class="tx sm" style="top:560px">{b}</div>
 {FIG(300, 'id="sch"')}<div id="book2" class="obj book" style="left:560px;top:1040px"><div id="rays2">{rays}</div><i></i><i></i></div>
 <div class="ar sm" id="ktitle" style="top:800px">كِتَابُ الْجَبْرِ وَالْمُقَابَلَة</div></div>''')

# ---- 03 · his example, drawn to scale (x = 150 px, 5 = 250 px) -----------------------------------------------------------------
t4 = wipe(t + 2.2, CREAM); scene("s3", t3, t4); A = t4 + 0.2
h, t = head("p3", 3, [("His ", None), ("example", "em")], A)
b, t = typed("p3b", [("A square plus 10 of its sides makes 39.", None)], t + 0.2)
pop("#eq", A + 0.5, 0.6, "soft/tick-lo.wav")
pop("#sq", t - 0.9, 0.3, "ref/tap.wav"); pop("#strip", t - 0.4, 0.3, "ref/tap.wav")
steps = [("Split the 10 into two fives.", 1.9), ("One corner is missing: 5 × 5 = 25.", 2.1), ("39 + 25 = 64. A perfect square: its side is 8.", 2.3), ("Take away the 5:", 1.3)]
st_html, tt = "", t + 0.5
for k, (s, hold) in enumerate(steps):
    sh, te = typed(f"q{k}", [(s, None)], tt, rate=0.028)
    st_html += f'<div class="step" id="st{k}">{sh}</div>'
    if k: T(f'tl.set("#st{k - 1}", {{opacity:0}}, {tt:.2f});')
    if k == 0:   # the strip parts in two: one five stays, the other turns down below the square
        T(f'tl.set("#strip", {{opacity:0}}, {te:.2f});'); T(f'tl.set("#fA, #fB", {{opacity:1}}, {te:.2f});')
        T(f'tl.to("#fB", {{x:-450, y:200, rotation:90, duration:0.55, ease:"power3.inOut"}}, {te + 0.1:.2f});')     # turned down below the square
        T(f'tl.to("#dia", {{x:125, duration:0.55, ease:"power3.inOut"}}, {te + 0.1:.2f});')     # the square now sits in the middle
        S("ref/short-swoosh.wav", te + 0.1, 1.0); S("soft/tick-lo.wav", te + 0.62, 1.0)
    if k == 1:
        T(f'tl.fromTo("#corner", {{opacity:0}}, {{opacity:1, duration:0.2}}, {te - 0.6:.2f});'); S("soft/tick.wav", te - 0.6, 0.8)
        T(f'tl.to("#corner", {{backgroundColor:"{GOLD}", borderColor:"{GOLD}", duration:0.3}}, {te + 0.1:.2f});'); pop("#corner b", te + 0.1, 0.3, "ref/click-x2.wav")
        S("soft/shimmer.wav", te + 0.1, 0.3)
    if k == 2:
        T(f'tl.fromTo("#big", {{opacity:0}}, {{opacity:1, duration:0.25}}, {te - 0.4:.2f});'); S("soft/thump.wav", te - 0.4, 0.7)
        pop("#s8b", te, 0.4, "ref/tap.wav")
    tt = te + hold
pop("#x3", tt - 0.9, 0.3, None); S("soft/thump.wav", tt - 0.9, 0.9); S("boom.wav", tt - 0.9, 0.35); S("soft/shimmer.wav", tt - 0.85, 0.4)
body.append(f'''<div class="sc" id="s4"><div class="hdw">{h}</div><div class="tx sm" style="top:560px">{b}</div>
 <div id="eq" class="eq">x² + 10x = 39</div>
 <div id="dia"><div id="sq" class="blk" style="left:0;top:0;width:150px;height:150px">x²</div>
  <div id="strip" class="blk" style="left:150px;top:0;width:500px;height:150px">10x</div>
  <div id="fA" class="blk" style="left:150px;top:0;width:250px;height:150px;opacity:0">5x</div>
  <div id="fB" class="blk" style="left:400px;top:0;width:250px;height:150px;opacity:0"><span style="transform:rotate(-90deg)">5x</span></div>
  <div id="corner" class="blk dash" style="left:150px;top:150px;width:250px;height:250px;opacity:0"><b>25</b></div>
  <div id="big" style="position:absolute;left:-10px;top:-10px;width:420px;height:420px;border:6px solid {GOLD};border-radius:14px;opacity:0"></div>
  <div class="eight" id="s8b" style="left:-70px;top:170px">8</div></div>
 {st_html}<div id="x3" class="eq gold" style="top:1390px">x = 3</div></div>''')

# ---- 04 · al-jabr becomes algebra ----------------------------------------------------------------------------------------------
t5 = wipe(tt + 0.6, TEAL); scene("s4", t4, t5); A = t5 + 0.2
h, t = head("p4", 4, [("al-jabr", "em"), (" → ", None), ("algebra", "em")], A)
b, t = typed("p4b", [("Europe translated his book into Latin.", None)], t + 0.2)
pop("#ms", A + 0.4, 0.6, "soft/tick-lo.wav")
FL = t + 0.1
T(f'tl.to("#ms .ar", {{opacity:0, y:-20, duration:0.25}}, {FL:.2f});'); T(f'tl.fromTo("#ms .la", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.3}}, {FL + 0.15:.2f});')
S("soft/flip.wav", FL, 1.0)
b2, t = typed("p4c", [("In Spain, a bone-\u2060setter was even called an ", None), ("algebrista", "em"), (".", None)], FL + 0.7)
SG = t - 0.4
T(f'tl.fromTo("#sign", {{opacity:0, y:-120, rotation:0}}, {{opacity:1, y:0, duration:0.3, ease:"power3.in"}}, {SG:.2f});'); S("soft/thump.wav", SG + 0.28, 0.8)
T(f'tl.fromTo("#sign", {{rotation:7}}, {{rotation:-5, duration:0.6, yoyo:true, repeat:2, ease:"sine.inOut", immediateRender:false}}, {SG + 0.3:.2f});'); S("soft/creak.wav", SG + 0.35, 0.45)
body.append(f'''<div class="sc" id="s5"><div class="hdw">{h}</div><div class="tx sm" style="top:560px">{b}<br>{b2}</div>
 <div id="ms"><div class="ar">الْجَبْر</div><div class="la">algebra</div><small>Latin, 1100s</small></div>
 <div id="sign"><div class="rope"></div><div class="plate">ALGEBRISTA{BONE_SVG("sb", 200)}</div></div></div>''')

# ---- 05 · your turn: the duʿāʾ -------------------------------------------------------------------------------------------------
t6 = wipe(t + 2.0, CREAM); scene("s5", t5, t6); A = t6 + 0.2
h, t = head("p5", 5, [("Your ", None), ("turn", "em")], A)
b, t = typed("p5b", [("Between the two sajdahs of every salah, you ask Allah for exactly this:", None)], t + 0.2)
T(f'tl.fromTo("#box", {{opacity:0, scaleY:0.2}}, {{opacity:1, scaleY:1, duration:0.3, ease:"power3.out"}}, {t + 0.1:.2f});'); S("soft/thump.wav", t + 0.1, 0.9); S("boom.wav", t + 0.1, 0.3)
du = words("dw", [("اللَّهُمَّ", ""), ("اغْفِرْ لِي", ""), ("وَارْحَمْنِي", ""), ("وَاجْبُرْنِي", "gold")], t + 0.5, 0.35)
tr, t = typed("p5t", [("“O Allah, forgive me, have mercy on me, and ", None), ("mend me", "em"), (".”", None)], t + 2.0, rate=0.03)
T(f'tl.fromTo("#dw3", {{scale:1}}, {{scale:1.15, duration:0.2, yoyo:true, repeat:1}}, {t - 0.3:.2f});'); S("soft/shimmer.wav", t - 0.3, 0.4)
pop("#src", t + 0.25, 0.3, "ref/click-x2.wav")
body.append(f'''<div class="sc" id="s6"><div class="hdw">{h}</div><div class="tx sm" style="top:560px">{b}</div>
 <div id="box"><div class="du">{du}</div><div class="tr">{tr}</div><div id="src">JĀMIʿ AT-TIRMIDHĪ 284</div></div></div>''')

# ---- the end ---------------------------------------------------------------------------------------------------------------------
t7 = wipe(t + 2.6, TEAL); scene("s6", t6, t7); A = t7 + 0.25
e1, t = typed("e1", [("Know what you're saying", None), ("", "br"), ("in your ", None), ("salah", "em"), (".", None)], A, rate=0.04, tick=2)
pop("#logo", A, 0.6, "soft/tick-lo.wav")
pop("#site", t + 0.2, 0.4, "ref/click-x2.wav"); S("soft/thump.wav", t + 0.2, 0.7)
e2, t = typed("e2", [("Did you know? Tell me in the comments.", None)], t + 0.9, rate=0.03)
scene("s7", t7, END)
END = round(t + 1.6, 2)
body.append(f'''<div class="sc" id="s7"><div id="logo"><span class="tile"><span>ر</span><em></em></span><b>رَفِيق</b></div>
 <div class="tx big" style="top:520px;font-size:76px">{e1}</div><div id="site">rafiq-arabic.com</div><div class="tx sm" style="top:1080px">{e2}</div></div>''')

# ---- sounds: one track, mixed here, plus a low room tone under it ---------------------------------------------------------------
def load(f):
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(SFX, f), "-f", "s16le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True).stdout, np.int16)
    return x.reshape(-1, 2).astype(np.float32) / 32768
def mix(path):
    n = int(END * SR); out = np.zeros((n, 2), np.float32); cache = {}
    room = load("soft/drone.wav"); reps = int(np.ceil(n / len(room))) + 1
    tone = np.concatenate([room] * reps)[:n] * 0.06
    fade = np.minimum(1, np.minimum(np.arange(n) / (0.8 * SR), (n - np.arange(n)) / (0.6 * SR)))[:, None]
    out += tone * fade
    for f, t, g in snd:
        if f not in cache:
            x = load(f)
            if f == "soft/shimmer.wav": x = x[:int(1.2 * SR)] * np.linspace(1, 0, int(1.2 * SR))[:, None] ** 2
            cache[f] = x / (np.abs(x).max() + 1e-9)
        x = cache[f] * g; i = int(t * SR); j = min(n, i + len(x))
        if i < n: out[i:j] += x[:j - i]
    out *= 0.89 / np.abs(out).max()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", path], input=out.tobytes(), check=True)

def build():
    out = os.path.join(HERE, "out", "v"); a = os.path.join(out, "assets")
    if os.path.exists(out): shutil.rmtree(out)
    os.makedirs(a)
    for f in ("karla-latin-500-normal.woff2", "karla-latin-700-normal.woff2", "jetbrains-mono-latin-500-normal.woff2", "ibm-plex-sans-arabic-arabic-700-normal.woff2"): shutil.copy(os.path.join(V6, "fonts", f), a)
    for f in ("playfair-display-latin-700-normal.woff2", "playfair-display-latin-700-italic.woff2", "playfair-display-latin-500-italic.woff2"): shutil.copy(os.path.join(ROOT, "brag-quiz/fonts", f), a); shutil.copy(os.path.join(V6, "lib/gsap.min.js"), a)
    mix(os.path.join(a, "sfx.wav"))
    css = f"""
@font-face {{ font-family:"KA"; src:url("assets/karla-latin-500-normal.woff2"); font-weight:500; }}
@font-face {{ font-family:"KA"; src:url("assets/karla-latin-700-normal.woff2"); font-weight:700; }}
@font-face {{ font-family:"MO"; src:url("assets/jetbrains-mono-latin-500-normal.woff2"); }}
@font-face {{ font-family:"SE"; src:url("assets/playfair-display-latin-700-normal.woff2"); font-weight:700; }}
@font-face {{ font-family:"SE"; src:url("assets/playfair-display-latin-700-italic.woff2"); font-weight:700; font-style:italic; }}
@font-face {{ font-family:"SE"; src:url("assets/playfair-display-latin-500-italic.woff2"); font-weight:500; font-style:italic; }}
@font-face {{ font-family:"AR"; src:url("assets/ibm-plex-sans-arabic-arabic-700-normal.woff2"); }}
* {{ margin:0; box-sizing:border-box; }} html, body {{ width:1080px; height:1920px; overflow:hidden; background:#000; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; background:{INK}; color:{CREAM}; font-family:SE; font-weight:700; font-variant-numeric:lining-nums; }}
#wall {{ position:absolute; inset:0 0 auto 0; height:1180px; background:
  linear-gradient(rgba(241,236,224,.035) 2px, transparent 2px) 0 0/90px 90px, linear-gradient(90deg, rgba(241,236,224,.035) 2px, transparent 2px) 0 0/90px 90px,
  radial-gradient(ellipse at 50% 60%, #22393f 0%, {INK} 75%); }}
#floorw {{ position:absolute; left:0; right:0; top:1180px; bottom:0; perspective:700px; perspective-origin:50% 0; overflow:hidden; }}
#floor {{ position:absolute; left:-1400px; right:-1400px; top:0; height:2600px; transform:rotateX(68deg); transform-origin:50% 0;
  background:repeating-conic-gradient(#245a4e 0 25%, #1a3d37 0 50%) 0 0/180px 180px; }}
#floorw::after {{ content:""; position:absolute; inset:0; background:linear-gradient({INK} 0%, rgba(23,38,43,.2) 30%, rgba(23,38,43,.55) 100%); }}
.sc {{ position:absolute; inset:0; opacity:0; }}
.tx {{ position:absolute; left:70px; right:70px; text-align:center; font-size:62px; line-height:1.25; }}
.tx.big {{ font-size:90px; line-height:1.12; }} .tx.sm {{ font-size:54px; font-weight:700; line-height:1.3; color:#dfe6e3; }}
.ch {{ opacity:0; }} #title .ch, #title {{ opacity:1; }} #title {{ opacity:0; }}
em {{ font-family:SE; font-style:italic; font-weight:700; color:{GOLD}; }}
#hook em {{ border-bottom:3px solid {GOLD}; }}
.num {{ position:absolute; top:330px; left:0; right:0; text-align:center; font-family:MO; font-size:34px; letter-spacing:.3em; color:#8fb3a9; opacity:0; }}
.hdw .hd, .hd {{ position:absolute; top:390px; left:60px; right:60px; text-align:center; font-size:96px; line-height:1.05; }}
#fan {{ position:absolute; left:0; right:0; top:860px; height:400px; }}
.card {{ position:absolute; left:450px; top:0; width:180px; height:250px; border-radius:20px; transform-origin:50% 230%; border:5px solid {INK};
  display:flex; flex-direction:column; align-items:center; justify-content:space-around; padding:14px 0 30px; box-shadow:0 18px 30px rgba(0,0,0,.45); opacity:0; }}
.card span {{ font-family:SE; font-style:italic; font-size:70px; font-weight:700; line-height:1; }} #cd2 {{ z-index:2; }}
#spark i {{ position:absolute; width:16px; height:16px; border-radius:50%; background:{GOLD}; opacity:0; }}
.fig {{ position:absolute; top:960px; width:100px; height:250px; }}
.fig i {{ position:absolute; left:22px; top:0; width:56px; height:56px; border-radius:50%; background:{BONE}; }}
.fig b {{ position:absolute; left:10px; top:66px; width:80px; height:184px; border-radius:40px 40px 10px 10px; background:{BONE}; }}
.obj {{ position:absolute; opacity:0; }}
#board {{ padding:28px 34px; border-radius:14px; background:#0f1a1d; border:8px solid {GOLD}; font-family:SE; font-style:italic; font-weight:700; font-size:62px; color:{CREAM}; }}
.book {{ width:240px; height:170px; }} .book > i {{ position:absolute; top:20px; width:116px; height:150px; background:{BONE}; border:6px solid {INK};
  background-image:repeating-linear-gradient(transparent 0 26px, rgba(23,38,43,.5) 26px 31px); background-position:0 30px; }}
.book > i:nth-of-type(1) {{ left:2px; border-radius:12px 2px 2px 12px; transform:skewY(6deg); }} .book > i:nth-of-type(2) {{ left:122px; border-radius:2px 12px 12px 2px; transform:skewY(-6deg); }}
#rays1, #rays2 {{ position:absolute; left:120px; top:90px; }} #rays1 i, #rays2 i {{ position:absolute; left:-4px; top:-30px; width:8px; height:56px; border-radius:4px; background:{BONE}; transform-origin:50% 100%; opacity:0; }}
.ar {{ position:absolute; left:0; right:0; text-align:center; font-family:AR; font-size:150px; color:{GOLD}; direction:rtl; }} .ar.sm {{ font-size:70px; color:{CREAM}; }}
#jabr, #ktitle {{ opacity:0; }}
.eq {{ position:absolute; top:715px; left:0; right:0; text-align:center; font-family:SE; font-style:italic; font-weight:700; font-size:104px; color:{CREAM}; opacity:0; }}
.eq.gold {{ color:{GOLD}; font-size:130px; }}
#dia {{ position:absolute; left:215px; top:880px; width:650px; height:400px; }}
.blk {{ position:absolute; display:grid; place-items:center; background:{TEAL}; color:{CREAM}; border:5px solid {INK}; font-family:SE; font-style:italic; font-weight:700; font-size:58px; border-radius:6px; opacity:0; }}
#sq {{ background:{CREAM}; color:{INK}; }} .blk.dash {{ background:transparent; border:5px dashed {GOLD}; }} .blk.dash b {{ font-family:SE; font-weight:700; font-size:84px; color:{INK}; opacity:0; }}
.eight {{ position:absolute; font-family:SE; font-style:italic; font-size:72px; color:{GOLD}; font-weight:700; opacity:0; }}
.step {{ position:absolute; top:1320px; left:60px; right:60px; text-align:center; font-size:54px; font-weight:700; line-height:1.2; }}
#ms {{ position:absolute; left:290px; top:900px; width:500px; height:300px; border-radius:14px; background:{CREAM}; box-shadow:0 20px 40px rgba(0,0,0,.5); opacity:0; }}
#ms .ar {{ top:40px; font-size:130px; color:{MAR}; }} #ms .la {{ position:absolute; top:70px; left:0; right:0; text-align:center; font-family:SE; font-style:italic; font-weight:700; font-size:120px; color:{MAR}; opacity:0; }}
#ms small {{ position:absolute; bottom:22px; left:0; right:0; text-align:center; font-family:SE; font-style:italic; font-weight:500; font-size:32px; color:#5c6e70; }}
#sign {{ position:absolute; left:340px; top:1220px; width:400px; transform-origin:50% 0; opacity:0; }} .rope {{ margin:0 auto; width:8px; height:50px; background:{BONE}; }}
.plate {{ padding:18px 0 10px; border-radius:16px; background:{CREAM}; border:6px solid {INK}; text-align:center; font-size:52px; color:{TEAL}; letter-spacing:.04em; font-family:KA; }}
#box {{ position:absolute; left:70px; right:70px; top:820px; padding:50px 40px 40px; border-radius:18px; background:#0f1a1d; border:3px solid {TEAL}; opacity:0; transform-origin:50% 0; }}
.du {{ text-align:center; direction:rtl; font-family:AR; font-size:74px; line-height:1.6; }} .aw {{ display:inline-block; opacity:0; }} .aw.gold {{ color:{GOLD}; }}
.tr {{ margin-top:24px; text-align:center; font-size:52px; font-weight:700; line-height:1.3; }}
#src {{ margin:30px auto 0; width:max-content; padding:10px 26px; border-radius:30px; background:{MAR}; font-family:MO; font-size:28px; letter-spacing:.12em; color:{GOLD}; opacity:0; }}
#logo {{ position:absolute; top:330px; left:0; right:0; display:flex; justify-content:center; align-items:center; gap:18px; opacity:0; }}
#logo .tile {{ position:relative; width:84px; height:84px; border-radius:22px; background:{CREAM}; display:grid; place-items:center; }}
#logo .tile span {{ font-family:AR; font-size:52px; color:{INK}; margin-top:-6px; }} #logo .tile em {{ position:absolute; right:13px; top:12px; width:13px; height:13px; border-radius:50%; background:{GOLD}; }}
#logo b {{ font-family:AR; font-size:64px; }}
#site {{ position:absolute; top:860px; left:50%; margin-left:-340px; width:680px; font-family:KA; padding:24px 0; text-align:center; border-radius:60px; background:{GOLD}; color:{INK}; font-size:58px; opacity:0; }}
.wipe {{ position:absolute; inset:0; z-index:50; transform:translateX(1100px); }}
"""
    open(os.path.join(out, "index.html"), "w").write(f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" /><title>algebra-silent</title>
<script src="assets/gsap.min.js"></script><style>{css}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{END}">
<div id="wall"></div><div id="floorw"><div id="floor"></div></div>
{chr(10).join(body)}
{chr(10).join(WIPES)}
<audio id="fx" src="assets/sfx.wav" data-start="0" data-duration="{END}" data-volume="1" data-track-index="1"></audio>
</div><script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;</script></body></html>
""")
    print("built", END, "s,", len(snd), "sounds")

if __name__ == "__main__":
    build()
