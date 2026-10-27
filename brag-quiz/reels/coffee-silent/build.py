#!/usr/bin/env python3
"""The coffee story as a silent reel (owner, 27 Oct 2026, #300), the same look as the silent algebra reel (#299,
reels/algebra-silent): our colours, Playfair Display, text typed out with one word in italic serif, a fan of numbered cards, numbered
points with a wipe between them; no voice, only sound effects. Every move eased as MOTION-STYLE.md says (entrances ease out, exits ease in,
interface springs with a slight overshoot, nothing linear).

  python3 brag-quiz/reels/coffee-silent/build.py
  then  cd brag-quiz/reels/coffee-silent/out/v && npx hyperframes render -o ../raw.mp4
Sources as the voiced reel (#300): qahwa "wine" in the old lexicographers, "because it takes away the appetite" (Hattox); Yemeni Sufis in the
1400s; Makkah, Cairo, Istanbul's kahve; Dutch koffie, English "coffee" first recorded 1582."""
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
        T(f'tl.fromTo("#{id}{k}", {{opacity:0, y:14}}, {{opacity:1, y:0, duration:0.25, ease:"power3.out"}}, {t0 + k * gap:.2f});')
        S("soft/tick.wav", t0 + k * gap, 0.7)
    return out

def pop(sel, t, s0=0.4, sound="ref/tap.wav", g=1.0):
    T(f'tl.fromTo("{sel}", {{opacity:0, scale:{s0}}}, {{opacity:1, scale:1, duration:0.4, ease:"back.out(1.4)", immediateRender:false}}, {t:.2f});')
    if sound: S(sound, t, g)

def scene(id, t0, t1):
    T(f'tl.set("#{id}", {{opacity:1}}, {t0:.2f});')
    if t1 < END: T(f'tl.set("#{id}", {{opacity:0}}, {t1:.2f});')

WIPES = []
def wipe(t, colour):
    """A panel sweeps across from the right (a low whoosh); the scenes swap while it covers the frame."""
    k = len(WIPES); WIPES.append(f'<div class="wipe" id="w{k}" style="background:{colour}"></div>')
    T(f'tl.fromTo("#w{k}", {{x:1100}}, {{x:0, duration:0.24, ease:"power3.out"}}, {t:.2f});')
    T(f'tl.to("#w{k}", {{x:-1100, duration:0.26, ease:"power3.in"}}, {t + 0.26:.2f});')
    S("ref/swoosh-low.wav", t, 1.0); S("soft/whoosh.wav", t + 0.05, 0.5)
    return t + 0.24

def head(id, num, parts, t0):
    """A point's number, its heading (types out) and returns the html and when the heading is done."""
    h, t = typed(id + "h", parts, t0 + 0.15, rate=0.045, tick=2)
    T(f'tl.fromTo("#{id}n", {{opacity:0}}, {{opacity:1, duration:0.25, ease:"power3.out"}}, {t0:.2f});')
    return f'<div class="num" id="{id}n">{num:02d} / 05</div><div class="hd">{h}</div>', t

FIG = lambda x, extra="": f'<div class="fig" style="left:{x}px" {extra}><i></i><b></b></div>'   # the little person on the floor
CUP = lambda w: f'''<svg width="{w}" viewBox="0 0 220 200"><path class="stm" d="M80 50 C 65 30, 95 20, 80 0 M110 50 C 95 30, 125 20, 110 0 M140 50 C 125 30, 155 20, 140 0" fill="none" stroke="{BONE}" stroke-width="6" stroke-linecap="round" opacity=".7"/>
<path d="M40 60 L 50 160 C 52 180, 66 190, 84 190 L 136 190 C 154 190, 168 180, 170 160 L 180 60 Z" fill="{BONE}" stroke="{INK}" stroke-width="6"/><path d="M178 80 C 215 80, 215 140, 170 145" fill="none" stroke="{BONE}" stroke-width="12"/>
<path d="M44 74 L 176 74" stroke="#6B4226" stroke-width="12"/></svg>'''
GLASS = lambda w: f'''<svg width="{w}" viewBox="0 0 160 240"><path d="M20 10 C 20 120, 140 120, 140 10 Z" fill="{BONE}" stroke="{INK}" stroke-width="6"/><path d="M26 40 C 34 104, 126 104, 134 40 Z" fill="{MAR}"/>
<path d="M80 100 L 80 210 M 35 222 L 125 222" stroke="{BONE}" stroke-width="12" stroke-linecap="round"/></svg>'''
POT = lambda w: f'''<svg width="{w}" viewBox="0 0 240 260"><path d="M60 70 C 40 160, 50 230, 90 250 L 170 250 C 210 230, 220 160, 190 70 Z" fill="{BONE}" stroke="{INK}" stroke-width="6"/>
<path d="M190 100 C 230 90, 240 50, 236 20" fill="none" stroke="{BONE}" stroke-width="12" stroke-linecap="round"/><path d="M80 70 L 170 70 L 150 30 L 100 30 Z" fill="{GOLD}" stroke="{INK}" stroke-width="6"/></svg>'''

# ---- 0 · hook, then the title and the fan of cards ------------------------------------------------------------------------
hook, t = typed("k", [("", "br"), ("wine.", "em")], 0.5, rate=0.07, tick=1); hook = "Coffee used to mean" + hook   # the line on frame 0
TITLE_T = 2.0
T(f'tl.to("#hook", {{opacity:0, duration:0.15, ease:"power2.in"}}, {TITLE_T - 0.15:.2f});')
T(f'tl.fromTo("#title", {{opacity:0, scale:1.08}}, {{opacity:1, scale:1, duration:0.3, ease:"power3.out"}}, {TITLE_T:.2f});')
ICONS = [  # one per point: the wine glass, the moon, the route, the ship, the cup
    f'<svg viewBox="0 0 60 90" width="50"><path d="M8 4 C 8 46, 52 46, 52 4 Z" fill="{INK}"/><path d="M30 40 L 30 80 M 14 84 L 46 84" stroke="{INK}" stroke-width="6" stroke-linecap="round"/></svg>',
    f'<svg viewBox="0 0 80 80" width="66"><path d="M50 6 A 34 34 0 1 0 74 56 A 28 28 0 1 1 50 6 Z" fill="{INK}"/></svg>',
    f'<svg viewBox="0 0 80 80" width="66"><path d="M14 70 C 30 50, 20 30, 40 22 C 56 16, 60 10, 66 8" fill="none" stroke="{INK}" stroke-width="6" stroke-dasharray="8 6"/><circle cx="14" cy="70" r="8" fill="{INK}"/><circle cx="66" cy="8" r="8" fill="{INK}"/></svg>',
    f'<svg viewBox="0 0 90 80" width="72"><path d="M10 52 L 80 52 L 66 72 L 22 72 Z" fill="{INK}"/><path d="M44 50 L 44 6 L 74 44 Z" fill="{INK}"/></svg>',
    f'<svg viewBox="0 0 90 80" width="72"><path d="M12 20 L 18 66 C 19 72, 24 76, 30 76 L 56 76 C 62 76, 67 72, 68 66 L 74 20 Z" fill="{INK}"/><path d="M72 30 C 88 30, 88 56, 70 58" fill="none" stroke="{INK}" stroke-width="6"/></svg>',
]
cards = ""
for i in range(5):
    a = (i - 2) * 15; col = MAR if i == 2 else (CREAM if i % 2 == 0 else SKY)
    fg = CREAM if i in (1, 2, 3) else INK
    icon = ICONS[i] if fg == INK else ICONS[i].replace(f'fill="{INK}"', f'fill="{fg}"').replace(f'stroke="{INK}"', f'stroke="{fg}"')
    cards += f'<div class="card" id="cd{i}" style="background:{col};color:{fg}"><span>{i + 1}</span>{icon}</div>'
    if i == 2:
        T(f'tl.fromTo("#cd2", {{opacity:0, y:-260, rotation:0}}, {{opacity:1, y:0, duration:0.35, ease:"power3.out"}}, {TITLE_T:.2f});')
    else:
        k = [1, 3, 0, 4].index(i); tt = 2.75 + k * 0.2
        T(f'tl.fromTo("#cd{i}", {{opacity:0, rotation:0}}, {{opacity:1, rotation:{a}, duration:0.35, ease:"back.out(1.4)"}}, {tt:.2f});')
        S("soft/tick-lo.wav", tt, 1.0); S("ref/click.wav", tt, 0.35)
S("soft/thump.wav", TITLE_T + 0.2, 1.0); S("boom.wav", TITLE_T + 0.2, 0.45)
T(f'tl.fromTo("#cd2", {{scale:1}}, {{scale:1.1, duration:0.2, yoyo:true, repeat:1, ease:"power2.inOut"}}, 3.75);')
T('tl.fromTo("#spark i", {opacity:0, scale:0}, {opacity:1, scale:1, duration:0.3, stagger:0.04, ease:"back.out(1.4)"}, 3.75);')
S("ref/click-x2.wav", 3.75, 0.9); S("soft/shimmer.wav", 3.75, 0.35)
spark = "".join(f'<i style="left:{540 + 230 * np.cos(np.radians(200 + 28 * k)):.0f}px;top:{1035 + 150 * np.sin(np.radians(200 + 28 * k)):.0f}px"></i>' for k in range(6))
body.append(f'''<div class="sc" id="s0" style="opacity:1">
 <div class="tx big" id="hook" style="top:360px">{hook}</div>
 <div class="tx big" id="title" style="top:330px">How <em>qahwa</em><br>became <em>coffee</em></div>
 <div id="fan">{cards}</div><div id="spark">{spark}</div></div>''')

# ---- 1 · you drink it every day ------------------------------------------------------------------------------------------------
t1 = wipe(5.6, TEAL); scene("s0", 0, t1); A = t1 + 0.25
l1, t = typed("a", [("You drink it every morning.", None)], A)
l2, t = typed("b", [("Nobody told you the ", None), ("word", "em"), (" is Arabic.", None)], t + 0.35)
pop("#cup1", A + 0.1, 0.6, "soft/tick-lo.wav")
T(f'tl.fromTo("#cup1 .stm", {{y:0}}, {{y:-12, duration:0.8, yoyo:true, repeat:3, ease:"sine.inOut"}}, {A + 0.4:.2f});')
QT = t + 0.15
pop("#qw1", QT, 0.5, "ref/click-x2.wav"); S("soft/shimmer.wav", QT + 0.1, 0.3)
body.append(f'''<div class="sc" id="s1"><div class="tx" style="top:420px">{l1}<br>{l2}</div>
 {FIG(300)}<div id="cup1" class="obj" style="left:540px;top:1010px">{CUP(220)}</div>
 <div class="ar" id="qw1" style="top:740px;opacity:0">قَهْوَة</div></div>''')

# ---- 01 · the word qahwa -------------------------------------------------------------------------------------------------------
t2 = wipe(QT + 2.0, CREAM); scene("s1", t1, t2); A = t2 + 0.2
h, t = head("p1", 1, [("The word ", None), ("qahwa", "em")], A)
b, t = typed("p1b", [("Old Arabic dictionaries say it meant wine, because it takes away your appetite.", None)], t + 0.2)
pop("#qw2", A + 0.5, 0.5, "soft/tick-lo.wav")
pop("#gl2", t - 1.6, 0.4, "ref/tap.wav")
T(f'tl.fromTo("#plate", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.4, ease:"power3.out"}}, {t - 1.0:.2f});')
AW = t + 0.2
T(f'tl.to("#plate", {{x:700, rotation:25, opacity:0, duration:0.5, ease:"power2.in"}}, {AW:.2f});'); S("ref/swoosh.wav", AW, 0.6)
body.append(f'''<div class="sc" id="s2"><div class="hdw">{h}</div><div class="tx sm" style="top:560px">{b}</div>
 <div class="ar" id="qw2" style="top:800px;opacity:0">قَهْوَة</div>
 <div id="gl2" class="obj" style="left:330px;top:1000px">{GLASS(150)}</div>
 <div id="plate" class="obj" style="left:530px;top:1130px"><svg width="260" viewBox="0 0 260 110"><ellipse cx="130" cy="60" rx="124" ry="44" fill="{BONE}" stroke="{INK}" stroke-width="6"/>
  <ellipse cx="130" cy="56" rx="76" ry="24" fill="none" stroke="#c9c2b4" stroke-width="5"/><path d="M95 50 C 110 30, 150 30, 160 50" fill="#e7a35a" stroke="{INK}" stroke-width="5"/></svg></div></div>''')

# ---- 02 · Yemen, the 1400s -----------------------------------------------------------------------------------------------------
t3 = wipe(AW + 1.8, TEAL); scene("s2", t2, t3); A = t3 + 0.2
h, t = head("p2", 2, [("Yemen", "em"), (", the 1400s", None)], A)
b, t = typed("p2b", [("Sufis drank a dark brew of coffee beans to stay awake for their night prayers.", None)], t + 0.2)
T(f'tl.fromTo("#moon", {{opacity:0, x:-80}}, {{opacity:1, x:0, duration:0.7, ease:"power3.out"}}, {A + 0.3:.2f});'); S("soft/whoosh.wav", A + 0.3, 0.4)
T(f'tl.fromTo("#stars2 i", {{opacity:0, scale:0}}, {{opacity:1, scale:1, duration:0.3, stagger:0.07, ease:"back.out(1.4)"}}, {A + 0.6:.2f});')
for k in range(5): S("soft/tick.wav", A + 0.6 + k * 0.07 * 1.4, 0.4)
pop("#pot", A + 1.2, 0.6, "soft/tick-lo.wav")
BE = A + 2.2
T(f'tl.fromTo(".bean", {{opacity:0, y:-200}}, {{opacity:1, y:0, duration:0.45, stagger:0.15, ease:"power3.out"}}, {BE:.2f});')
T(f'tl.to(".bean", {{opacity:0, y:50, duration:0.25, stagger:0.1, ease:"power2.in"}}, {BE + 0.75:.2f});')
for k in range(4): S("soft/tick.wav", BE + 0.4 + k * 0.15, 0.6)
T(f'tl.fromTo("#mat2", {{opacity:0, scaleY:0}}, {{opacity:1, scaleY:1, duration:0.45, ease:"back.out(1.4)", transformOrigin:"50% 100%"}}, {t - 0.6:.2f});'); S("soft/thump.wav", t - 0.5, 0.5)
b2, t = typed("p2c", [("They gave it the old name: ", None), ("qahwa", "em"), (".", None)], t + 0.5)
pop("#tag2", t - 0.3, 0.4, "ref/click-x2.wav"); S("soft/shimmer.wav", t - 0.2, 0.3)
stars = "".join(f'<i style="left:{x}px;top:{y}px"></i>' for x, y in ((140, 900), (290, 960), (430, 880), (720, 950), (960, 900)))
beans = "".join(f'<i class="bean" style="left:{x}px"></i>' for x in (600, 640, 680, 620))
body.append(f'''<div class="sc" id="s3"><div class="hdw">{h}</div><div class="tx sm" style="top:560px">{b}<br>{b2}</div>
 <svg id="moon" viewBox="0 0 100 100" width="130" style="position:absolute;left:820px;top:960px;opacity:0"><path d="M60 10 A 40 40 0 1 0 90 70 A 32 32 0 1 1 60 10 Z" fill="{GOLD}"/></svg>
 <div id="stars2">{stars}</div>
 <div id="mat2" class="obj" style="left:180px;top:1060px;width:150px;height:200px;border-radius:70px 70px 8px 8px;background:{TEAL};border:6px solid {INK};box-shadow:inset 0 0 0 14px {TEAL}, inset 0 0 0 19px {GOLD}"></div>
 {beans}<div id="pot" class="obj" style="left:560px;top:1000px">{POT(200)}</div>
 <div id="tag2" class="obj" style="left:575px;top:860px"><span class="tagp tar" style="font-size:72px">قَهْوَة</span></div></div>''')

# ---- 03 · the route ------------------------------------------------------------------------------------------------------------
t4 = wipe(t + 2.0, CREAM); scene("s3", t3, t4); A = t4 + 0.2
h, t = head("p3", 3, [("The ", None), ("route", "em")], A)
b, t = typed("p3b", [("From Yemen to Makkah and Cairo, then Istanbul, where it became ", None), ("kahve", "em"), (".", None)], t + 0.2)
T(f'tl.fromTo("#map", {{opacity:0, scaleY:0.2}}, {{opacity:1, scaleY:1, duration:0.35, ease:"power3.out"}}, {A + 0.4:.2f});'); S("soft/thump.wav", A + 0.45, 0.6)
CITY = [("pY", "Yemen", 640, 1440), ("pM", "Makkah", 540, 1280), ("pC", "Cairo", 360, 1120), ("pI", "Istanbul", 520, 920)]
mt, svgp = A + 1.6, ""
for i, (p, nm, x, y) in enumerate(CITY):
    if i:
        px, py = CITY[i - 1][2:]
        svgp += f'<path id="r{i}" d="M{px} {py} L {x} {y}" pathLength="1" stroke="{GOLD}" stroke-width="7" stroke-dasharray="1" stroke-dashoffset="1" fill="none"/>'
        T(f'tl.fromTo("#r{i}", {{strokeDashoffset:1}}, {{strokeDashoffset:0, duration:0.5, ease:"power2.inOut"}}, {mt - 0.5:.2f});')
    svgp += f'<g id="{p}" style="opacity:0;transform-origin:{x}px {y}px"><circle cx="{x}" cy="{y}" r="18" fill="{MAR}" stroke="{CREAM}" stroke-width="5"/><text x="{x + (30 if i != 2 else -30)}" y="{y + 14}" text-anchor="{"start" if i != 2 else "end"}">{nm}</text></g>'
    pop(f"#{p}", mt, 0.3, "ref/tap.wav"); mt += 0.75
pop("#kahve", max(t, mt) + 0.1, 0.4, "ref/click-x2.wav"); t = max(t, mt)
body.append(f'''<div class="sc" id="s4"><div class="hdw">{h}</div><div class="tx sm" style="top:560px">{b}</div>
 <div id="map"><svg width="940" height="680" viewBox="70 850 940 680" style="position:absolute;left:0;top:0">
  <path d="M120 1010 C 300 980, 560 1000, 900 1020 L 900 1060 C 560 1050, 300 1040, 120 1060 Z" fill="#245a4e"/>
  <path d="M420 1150 C 480 1250, 560 1360, 640 1490 L 680 1470 C 600 1340, 520 1230, 460 1140 Z" fill="#245a4e"/>{svgp}</svg>
  <div id="kahve" class="obj" style="left:690px;top:110px"><span class="tagp">kahve</span></div></div></div>''')

# ---- 04 · koffie → coffee ------------------------------------------------------------------------------------------------------
t5 = wipe(t + 2.3, TEAL); scene("s4", t4, t5); A = t5 + 0.2
h, t = head("p4", 4, [("koffie", "em"), (" → ", None), ("coffee", "em")], A)
b, t = typed("p4b", [("Ships carried it to Europe. The Dutch said koffie, and by 1582, English had a new word.", None)], t + 0.2)
CH = [("ch0", "قَهْوَة", "wa"), ("ch1", "kahve", ""), ("ch2", "koffie", ""), ("ch3", "coffee", "")]   # not w0…: the wipes use those
ct, chain = A + 1.0, ""
for i, (id, w, c) in enumerate(CH):
    chain += f'<div class="wc {c}" id="{id}">{w}</div>' + ('<div class="arw">↓</div>' if i < 3 else "")
    if i < 3: pop(f"#{id}", ct, 0.6, "soft/tick-lo.wav"); ct += 0.9
T(f'tl.fromTo(".arw", {{opacity:0, y:-10}}, {{opacity:1, y:0, duration:0.3, stagger:0.9, ease:"power3.out"}}, {A + 1.45:.2f});')
pop("#yr", t - 0.6, 0.5, "ref/tap.wav")
CF = t + 0.3
T(f'tl.fromTo("#ch3", {{opacity:0, scale:1.8}}, {{opacity:1, scale:1, duration:0.45, ease:"back.out(1.7)"}}, {CF:.2f});')   # the one slam
S("soft/thump.wav", CF + 0.15, 1.0); S("boom.wav", CF + 0.15, 0.4); S("soft/shimmer.wav", CF + 0.1, 0.4)
body.append(f'''<div class="sc" id="s5"><div class="hdw">{h}</div><div class="tx sm" style="top:560px">{b}</div>
 <div id="chain">{chain}</div><div id="yr" class="obj" style="left:790px;top:1390px"><span class="tagp" style="background:{MAR};color:{GOLD}">1582</span></div></div>''')

# ---- 05 · your turn: maqha -----------------------------------------------------------------------------------------------------
t6 = wipe(CF + 2.2, CREAM); scene("s5", t5, t6); A = t6 + 0.2
h, t = head("p5", 5, [("Your ", None), ("turn", "em")], A)
b, t = typed("p5b", [("A masjid is the place of sujood. So what is this?", None)], t + 0.2)
T(f'tl.fromTo("#box", {{opacity:0, scaleY:0.2}}, {{opacity:1, scaleY:1, duration:0.35, ease:"power3.out"}}, {A + 0.5:.2f});'); S("soft/thump.wav", A + 0.55, 0.8)
pop("#msj", A + 0.9, 0.6, "soft/tick.wav")
T(f'tl.to("#msj .m", {{color:"{GOLD}", duration:0.3, ease:"power2.out"}}, {t - 1.4:.2f});'); S("soft/tick-lo.wav", t - 1.4, 0.5)
T(f'tl.to("#msj", {{opacity:0.3, scale:0.7, y:-40, duration:0.45, ease:"power2.inOut"}}, {t:.2f});')
pop("#mq", t + 0.3, 0.6, "soft/tick-lo.wav")
T(f'tl.to("#mq .m", {{color:"{GOLD}", duration:0.3, ease:"power2.out"}}, {t + 0.9:.2f});')
o0 = t + 1.3
for i in range(3): pop(f"#op{i}", o0 + i * 0.25, 0.8, "ref/tap.wav", 0.6)
c0 = o0 + 1.1
for k, nm in enumerate(("3", "2", "1")):
    T(f'tl.set("#cd", {{textContent:"{nm}", opacity:1}}, {c0 + k:.2f});'); T(f'tl.fromTo("#cd", {{scale:1.4}}, {{scale:1, duration:0.35, ease:"power3.out"}}, {c0 + k:.2f});')
    S("ref/click.wav", c0 + k, 1.0)
AN = c0 + 3
T(f'tl.to("#cd", {{opacity:0, duration:0.2, ease:"power2.in"}}, {AN - 0.1:.2f});')
T(f'tl.to("#op1", {{backgroundColor:"{GOLD}", color:"{INK}", scale:1.06, duration:0.35, ease:"back.out(1.4)"}}, {AN:.2f});'); S("ref/click-x2.wav", AN, 1.0); S("soft/shimmer.wav", AN, 0.4)
T(f'tl.to(["#op0", "#op2"], {{opacity:0.3, duration:0.3, ease:"power2.in"}}, {AN:.2f});')
an, t = typed("p5a", [("A café: the place of ", None), ("qahwa", "em"), (".", None)], AN + 0.4)
body.append(f'''<div class="sc" id="s6"><div class="hdw">{h}</div><div class="tx sm" style="top:560px">{b}</div>
 <div id="box"><div class="aw2" id="msj"><span class="m">مَـ</span>سْجِد</div><div class="aw2" id="mq" style="color:{CREAM}"><span class="m">مَـ</span>قْهى</div>
  {''.join(f'<div class="op2" id="op{i}">{x}</div>' for i, x in enumerate(("a coffee pot", "a café", "a coffee bean")))}
  <div class="ans">{an}</div></div><div id="cd">3</div></div>''')

# ---- the end ---------------------------------------------------------------------------------------------------------------------
t7 = wipe(t + 2.2, TEAL); scene("s6", t6, t7); A = t7 + 0.25
e1, t = typed("e1", [("Every coffee you order is", None), ("", "br"), ("a little bit of ", None), ("Arabic", "em"), (".", None)], A, rate=0.04, tick=2)
pop("#logo", A, 0.6, "soft/tick-lo.wav")
pop("#site", t + 0.2, 0.4, "ref/click-x2.wav"); S("soft/thump.wav", t + 0.2, 0.7)
e2, t = typed("e2", [("How do you take yours? Tell me in the comments.", None)], t + 0.9, rate=0.03)
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
#box {{ position:absolute; left:70px; right:70px; top:720px; padding:30px 40px 40px; border-radius:18px; background:#0f1a1d; border:3px solid {TEAL}; opacity:0; transform-origin:50% 0; }}
.du {{ text-align:center; direction:rtl; font-family:AR; font-size:74px; line-height:1.6; }} .aw {{ display:inline-block; opacity:0; }} .aw.gold {{ color:{GOLD}; }}
.tr {{ margin-top:24px; text-align:center; font-size:52px; font-weight:700; line-height:1.3; }}
#src {{ margin:30px auto 0; width:max-content; padding:10px 26px; border-radius:30px; background:{MAR}; font-family:MO; font-size:28px; letter-spacing:.12em; color:{GOLD}; opacity:0; }}
#logo {{ position:absolute; top:330px; left:0; right:0; display:flex; justify-content:center; align-items:center; gap:18px; opacity:0; }}
#logo .tile {{ position:relative; width:84px; height:84px; border-radius:22px; background:{CREAM}; display:grid; place-items:center; }}
#logo .tile span {{ font-family:AR; font-size:52px; color:{INK}; margin-top:-6px; }} #logo .tile em {{ position:absolute; right:13px; top:12px; width:13px; height:13px; border-radius:50%; background:{GOLD}; }}
#logo b {{ font-family:AR; font-size:64px; }}
#site {{ position:absolute; top:860px; left:50%; margin-left:-340px; width:680px; font-family:KA; padding:24px 0; text-align:center; border-radius:60px; background:{GOLD}; color:{INK}; font-size:58px; opacity:0; }}
.tagp {{ display:inline-block; padding:8px 30px; border-radius:40px; background:{CREAM}; color:{MAR}; font-size:56px; box-shadow:0 12px 24px rgba(0,0,0,.4); }}
.tagp.tar {{ font-family:AR; direction:rtl; }}
#stars2 i {{ position:absolute; width:14px; height:14px; border-radius:50%; background:#fff6d8; opacity:0; }}
.bean {{ position:absolute; top:980px; width:34px; height:46px; border-radius:50%; background:#6B4226; border:4px solid {INK}; opacity:0; }}
#map {{ position:absolute; left:70px; top:850px; width:940px; height:680px; border-radius:24px; background:#0f1a1d; border:3px solid {TEAL}; overflow:hidden; opacity:0; transform-origin:50% 0; }}
#map text {{ font-family:KA; font-weight:700; font-size:40px; fill:{CREAM}; }}
#chain {{ position:absolute; left:0; right:0; top:800px; text-align:center; }}
.wc {{ display:block; width:max-content; margin:0 auto; padding:6px 44px; border-radius:60px; background:{CREAM}; color:{INK}; font-family:SE; font-style:italic; font-size:76px; line-height:1.3; opacity:0; }}
.wc.wa {{ font-family:AR; direction:rtl; font-style:normal; color:{MAR}; font-size:66px; line-height:1.6; }} #ch3 {{ background:{GOLD}; font-size:110px; }}
.arw {{ font-family:KA; font-size:50px; color:{GOLD}; line-height:70px; height:70px; opacity:0; }}
.aw2 {{ text-align:center; font-family:AR; font-size:120px; line-height:1.4; direction:rtl; opacity:0; }}
#mq {{ margin-top:-30px; }}
.op2 {{ width:600px; margin:16px auto 0; padding:14px; border-radius:40px; background:#22393f; text-align:center; font-family:KA; font-size:48px; color:{CREAM}; opacity:0; }}
.ans {{ margin-top:30px; text-align:center; font-size:56px; }}
#cd {{ position:absolute; left:0; right:0; top:1330px; text-align:center; font-size:130px; color:{GOLD}; opacity:0; }}
.wipe {{ position:absolute; inset:0; z-index:50; transform:translateX(1100px); }}
"""
    open(os.path.join(out, "index.html"), "w").write(f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" /><title>coffee-silent</title>
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
