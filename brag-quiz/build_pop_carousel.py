#!/usr/bin/env python3
"""The word carousels redone with drawings and popping colour (owner, 28 Oct 2026, #304: "carousels with a boring plain background and no
pictures or drawings don't perform well… add some pics, drawings and make it not boring. Add more popping colour"). Same words and course
sentences as build_word_carousels.py (SETS), new look: a bold colour per slide with doodles, the English word on a tilted sticker, the
Arabic big with an ink outline, a drawn scene for the sentence (faceless figures: no eyes, owner, 27 Oct), the sentence on a card with a
hard ink shadow, the note on a sticky note.

  python3 brag-quiz/build_pop_carousel.py [set ...]   ->  brag-quiz/stills/<set>-pop/<set>-<n>.png   (sets with ART below)
"""
import os, random, re, sys
from playwright.sync_api import sync_playwright
import build_salah_numbers as S
from build_word_carousels import SETS, COVER, ar_spans

INK, PAPER, GOLD, RED, TEAL = "#17262B", "#FFF8EC", "#E9B949", "#B4322A", "#2E7263"
SKIN = ["#e8c4a6", "#c48f66", "#8d5f3e", "#d9b08c", "#a8784f"]
F = "file://" + os.path.join(S.HERE, "fonts")
CSS = f"""
@font-face {{ font-family:"FR"; src:url("{F}/fredoka-latin-700-normal.woff2"); font-weight:700; }}
@font-face {{ font-family:"FR"; src:url("{F}/fredoka-latin-600-normal.woff2"); font-weight:600; }}
@font-face {{ font-family:"AR"; src:url("{F}/ibm-plex-sans-arabic-arabic-700-normal.woff2"); }}
* {{ margin:0; box-sizing:border-box; }}
body {{ width:1080px; height:1350px; overflow:hidden; position:relative; font-family:FR; font-weight:700; color:{INK}; }}
.dood {{ position:absolute; inset:0; pointer-events:none; }}
.top {{ position:absolute; top:34px; left:40px; right:40px; display:flex; justify-content:space-between; align-items:center; }}
.brand {{ display:flex; align-items:center; gap:10px; background:{PAPER}; border:4px solid {INK}; border-radius:40px; padding:6px 20px 6px 8px; box-shadow:5px 5px 0 {INK}; }}
.brand .tile {{ position:relative; width:46px; height:46px; border-radius:14px; background:{INK}; display:grid; place-items:center; }}
.brand .tile span {{ font-family:AR; font-size:30px; color:{PAPER}; margin-top:-4px; }}
.brand .tile em {{ position:absolute; right:7px; top:6px; width:8px; height:8px; border-radius:50%; background:{RED}; }}
.brand b {{ font-family:AR; font-size:34px; }}
.cnt {{ background:{INK}; color:{PAPER}; border-radius:30px; padding:8px 22px; font-size:30px; }}
.en {{ position:absolute; top:128px; left:0; right:0; text-align:center; }}
.en span {{ display:inline-block; background:{PAPER}; border:5px solid {INK}; border-radius:22px; padding:4px 34px; font-size:70px; box-shadow:7px 7px 0 {INK}; transform:rotate(-3deg); }}
.ar {{ position:absolute; top:285px; left:0; right:0; text-align:center; font-family:AR; font-size:190px; line-height:1.35; direction:rtl; color:#fff;
  -webkit-text-stroke:10px {INK}; paint-order:stroke fill; text-shadow:10px 10px 0 {INK}; }}
.tr {{ position:absolute; top:560px; left:0; right:0; text-align:center; }}
.tr span {{ display:inline-block; background:{INK}; color:{PAPER}; border-radius:30px; padding:4px 26px; font-size:38px; font-weight:600; }}
.art {{ position:absolute; left:0; right:0; top:608px; height:390px; }}
.art svg {{ display:block; margin:0 auto; }}
.card {{ position:absolute; left:70px; right:70px; background:{PAPER}; border:5px solid {INK}; border-radius:30px; box-shadow:10px 10px 0 {INK}; padding:22px 30px 20px; text-align:center; transform:rotate(1deg); }}
.card .s {{ font-family:AR; font-size:54px; direction:rtl; line-height:1.55; }}
.card .s i {{ font-style:normal; padding:0 10px; border-radius:12px; }}
.card .t {{ font-family:FR; font-weight:600; font-size:28px; color:#5c6e70; margin-top:2px; }}
.card .m {{ font-size:34px; margin-top:6px; }}
.note {{ position:absolute; left:110px; right:110px; bottom:34px; background:#FFE66D; border:4px solid {INK}; padding:14px 24px; font-size:32px; line-height:1.25; text-align:center; transform:rotate(-1.5deg); box-shadow:6px 6px 0 {INK}; }}
.note span {{ font-family:AR; unicode-bidi:isolate; }}
.cov {{ position:absolute; top:150px; left:30px; right:30px; text-align:center; line-height:1.25; }}
.cov b {{ display:inline-block; margin:10px 8px; padding:4px 30px; border:6px solid {INK}; border-radius:26px; font-size:104px; box-shadow:8px 8px 0 {INK}; }}
.bubble {{ position:absolute; left:120px; right:120px; background:{PAPER}; border:6px solid {INK}; border-radius:44px; padding:26px; text-align:center; font-size:66px; line-height:1.1; box-shadow:9px 9px 0 {INK}; }}
.bubble:after {{ content:""; position:absolute; left:50%; bottom:-46px; margin-left:-24px; border:24px solid transparent; border-top:40px solid {INK}; }}
.swipe {{ position:absolute; bottom:46px; left:0; right:0; text-align:center; font-size:40px; }}
.swipe span {{ display:inline-block; background:{INK}; color:{PAPER}; border-radius:40px; padding:10px 34px; }}
.endq {{ position:absolute; top:190px; left:60px; right:60px; text-align:center; font-size:110px; line-height:1.05; color:{PAPER}; -webkit-text-stroke:8px {INK}; paint-order:stroke fill; text-shadow:9px 9px 0 {INK}; }}
.endq i {{ font-style:normal; color:{GOLD}; }}
.ends {{ position:absolute; bottom:60px; left:120px; right:120px; }}
.ends div {{ background:{PAPER}; border:5px solid {INK}; border-radius:30px; padding:16px; margin-top:18px; text-align:center; font-size:40px; box-shadow:7px 7px 0 {INK}; }}
"""

# ---- the drawings: faceless figures (no eyes), flat, with an ink outline ------------------------------------------------------
O = f'stroke="{INK}" stroke-width="6" stroke-linejoin="round"'
def person(x, y, s=1.0, skin=SKIN[0], top=None, body="#4D96FF", beard=None, arm=None, scarf=None, legs=True):
    """A standing figure, feet at (x, y). top: 'kufi', 'hijab:<colour>', 'hair:<colour>'; arm: 'self', 'fold', 'book:<colour>', 'wave'."""
    g = f'<g transform="translate({x - 100 * s:.0f},{y - 300 * s:.0f}) scale({s})">'
    if legs: g += f'<rect x="72" y="230" width="24" height="70" rx="10" fill="{INK}"/><rect x="104" y="230" width="24" height="70" rx="10" fill="{INK}"/>'
    g += f'<path d="M50 250 L 62 128 Q 100 104 138 128 L 150 250 Z" fill="{body}" {O}/>'
    if top and top.startswith("hijab"):
        c = top.split(":")[1]
        g += f'<path d="M100 22 C 58 22 46 66 50 98 C 52 128 44 150 56 170 L 144 170 C 156 150 148 128 150 98 C 154 66 142 22 100 22 Z" fill="{c}" {O}/>'
        g += f'<ellipse cx="100" cy="82" rx="30" ry="36" fill="{skin}" {O}/>'
    else:
        g += f'<circle cx="100" cy="76" r="38" fill="{skin}" {O}/>'
        if beard: g += f'<path d="M74 92 C 76 122 124 122 126 92 C 114 104 86 104 74 92 Z" fill="{beard}" {O}/>'
        if top == "kufi": g += f'<path d="M64 62 C 66 30 134 30 136 62 Z" fill="#fff" {O}/>'
        elif top and top.startswith("hair"): g += f'<path d="M62 70 C 58 26 142 26 138 70 C 122 50 78 50 62 70 Z" fill="{top.split(":")[1]}" {O}/>'
    if arm == "self": g += f'<path d="M136 140 C 160 170 130 186 104 178" fill="none" stroke="{body}" stroke-width="22" stroke-linecap="round"/><circle cx="102" cy="176" r="12" fill="{skin}" {O}/>'
    elif arm == "fold": g += f'<path d="M64 150 C 80 172 120 172 136 150" fill="none" stroke="{body}" stroke-width="22" stroke-linecap="round"/><ellipse cx="100" cy="166" rx="18" ry="11" fill="{skin}" {O}/>'
    elif arm and arm.startswith("book"):
        g += f'<path d="M64 150 C 80 176 120 176 136 150" fill="none" stroke="{body}" stroke-width="22" stroke-linecap="round"/>'
        g += f'<path d="M70 150 L 100 160 L 130 150 L 130 186 L 100 196 L 70 186 Z" fill="{arm.split(":")[1]}" {O}/><path d="M100 160 L 100 196" stroke="{INK}" stroke-width="4"/>'
    elif arm == "wave": g += f'<path d="M138 136 C 168 110 170 80 160 60" fill="none" stroke="{body}" stroke-width="22" stroke-linecap="round"/><circle cx="160" cy="56" r="13" fill="{skin}" {O}/>'
    if scarf: g += f'<path d="M64 130 Q 100 150 136 130 L 136 146 Q 100 166 64 146 Z" fill="{scarf}" {O}/>'
    return g + "</g>"

def hand(x, y, flip=False, colour=SKIN[1]):                              # a big pointing hand coming in from the side
    t = f'translate({x},{y}) scale({-1 if flip else 1},1)'
    return (f'<g transform="{t}"><rect x="-260" y="-34" width="200" height="68" rx="20" fill="#FFE66D" {O}/>'
            f'<path d="M-70 -40 L 20 -40 C 40 -40 40 -14 20 -14 L 90 -14 C 116 -14 116 16 90 16 L 0 16 C 20 26 10 50 -10 46 L -70 40 Z" fill="{colour}" {O}/></g>')

def sparkles(seed, colours):                                             # the doodles round every slide
    r = random.Random(seed); out = ""
    for _ in range(16):
        x, y, c, k = r.uniform(0, 1080), r.uniform(0, 1350), r.choice(colours), r.random()
        if k < 0.35: out += f'<path d="M{x} {y - 22} Q {x + 4} {y - 4} {x + 22} {y} Q {x + 4} {y + 4} {x} {y + 22} Q {x - 4} {y + 4} {x - 22} {y} Q {x - 4} {y - 4} {x} {y - 22} Z" fill="{c}" opacity=".85"/>'
        elif k < 0.6: out += f'<circle cx="{x}" cy="{y}" r="{r.uniform(8, 18):.0f}" fill="none" stroke="{c}" stroke-width="6" opacity=".7"/>'
        elif k < 0.8: out += f'<path d="M{x} {y} q 20 -20 40 0 t 40 0 t 40 0" fill="none" stroke="{c}" stroke-width="7" stroke-linecap="round" opacity=".7"/>'
        else: out += f'<circle cx="{x}" cy="{y}" r="7" fill="{c}" opacity=".8"/>'
    return f'<svg class="dood" viewBox="0 0 1080 1350">{out}</svg>'

def mosque(x, y, s=1.0, c="#fff"):
    return (f'<g transform="translate({x},{y}) scale({s})"><rect x="-150" y="-160" width="300" height="160" fill="{c}" {O}/>'
            f'<path d="M-90 -160 C -90 -260 90 -260 90 -160 Z" fill="{GOLD}" {O}/><path d="M0 -262 L 0 -296" stroke="{INK}" stroke-width="6"/>'
            f'<path d="M-6 -300 A 10 10 0 1 0 6 -290" fill="none" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="160" y="-300" width="44" height="300" fill="{c}" {O}/><path d="M160 -300 L 182 -350 L 204 -300 Z" fill="{GOLD}" {O}/>'
            f'<path d="M-36 0 L -36 -70 C -36 -110 36 -110 36 -70 L 36 0 Z" fill="{TEAL}" {O}/></g>')

def glass(x, y, s=1.0, fill="#9fd8ff"):                                # a tall glass, feet at (x, y)
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M-36 -84 L 36 -84 L 32 0 L -32 0 Z" fill="{fill}"/>'
            f'<path d="M-42 -124 L 42 -124 L 34 0 L -34 0 Z" fill="none" {O}/><path d="M-26 -110 L -22 -20" stroke="#fff" stroke-width="7" stroke-linecap="round" opacity=".7"/></g>')
def steam(x, y, s=1.0):
    return "".join(f'<path d="M{x + dx} {y} c -14 -20 14 -34 0 -56 c -10 -16 6 -26 0 -40" fill="none" stroke="#fff" stroke-width="{8 * s:.0f}" stroke-linecap="round"/>' for dx in (-22 * s, 0, 22 * s))
def teaglass(x, y, s=1.0):                                              # a little tea glass on a saucer, with steam
    return (f'<g transform="translate({x},{y}) scale({s})"><ellipse cx="0" cy="0" rx="70" ry="16" fill="#fff" {O}/>'
            f'<path d="M-34 -100 C -46 -60 -24 -40 -28 -8 L 28 -8 C 24 -40 46 -60 34 -100 Z" fill="#c8551f" {O}/></g>' + steam(x, y - 112 * s, s))
def plate(x, y, s=1.0, food="dates"):
    g = f'<g transform="translate({x},{y}) scale({s})"><ellipse cx="0" cy="0" rx="130" ry="34" fill="#fff" {O}/>'
    if food == "dates": g += "".join(f'<ellipse cx="{dx}" cy="{dy}" rx="26" ry="15" fill="#7a3b1c" {O}/>' for dx, dy in ((-60, -14), (-20, -20), (24, -14), (64, -18), (-36, -38), (14, -42), (52, -40)))
    elif food == "bread": g += f'<path d="M-100 -10 C -100 -90 100 -90 100 -10 Z" fill="#d9944a" {O}/>' + "".join(f'<path d="M{dx} -62 L {dx + 24} -30" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>' for dx in (-50, -10, 30))
    return g + "</g>"
def jug(x, y, s=1.0, c="#cfe9ff"):
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M-50 0 L -56 -110 C -56 -130 -40 -150 -30 -160 L 40 -160 L 50 -110 L 56 0 Z" fill="{c}" {O}/>'
            f'<path d="M50 -130 C 100 -120 96 -40 54 -40" fill="none" stroke="{INK}" stroke-width="12"/><path d="M-50 -60 L 52 -60" stroke="#4D96FF" stroke-width="8"/></g>')
def dallah(x, y, s=1.0):                                                # an Arabic coffee pot
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M-60 0 C -80 -40 -50 -80 -36 -100 L -30 -150 L 30 -150 L 36 -100 C 50 -80 80 -40 60 0 Z" fill="{GOLD}" {O}/>'
            f'<path d="M-30 -150 C -24 -190 24 -190 30 -150 Z" fill="{GOLD}" {O}/><circle cx="0" cy="-196" r="10" fill="{GOLD}" {O}/>'
            f'<path d="M-40 -110 C -90 -120 -110 -170 -130 -190" fill="none" stroke="{INK}" stroke-width="22" stroke-linecap="round"/><path d="M-40 -110 C -90 -120 -110 -170 -130 -190" fill="none" stroke="{GOLD}" stroke-width="10" stroke-linecap="round"/>'
            f'<path d="M50 -120 C 100 -110 100 -40 56 -30" fill="none" stroke="{INK}" stroke-width="12"/></g>')
def finjan(x, y, s=1.0):
    return f'<g transform="translate({x},{y}) scale({s})"><path d="M-34 -50 L 34 -50 L 24 0 L -24 0 Z" fill="#fff" {O}/><path d="M-26 -34 L 26 -34" stroke="#8a5a2b" stroke-width="10"/></g>'
def moon(x, y, s=1.0, c="#FFE66D"):
    return f'<path transform="translate({x},{y}) scale({s})" d="M20 -60 A 62 62 0 1 0 20 60 A 48 48 0 1 1 20 -60 Z" fill="{c}" {O}/>'
def cal(x, y, num, col, s=1.0, cross=False):                            # a calendar page with a big number
    g = (f'<g transform="translate({x},{y}) scale({s})"><rect x="-110" y="-130" width="220" height="236" rx="24" fill="#fff" {O}/>'
         f'<path d="M-110 -70 L -110 -106 Q -110 -130 -86 -130 L 86 -130 Q 110 -130 110 -106 L 110 -70 Z" fill="{col}" {O}/>'
         f'<rect x="-60" y="-150" width="18" height="44" rx="9" fill="{INK}"/><rect x="42" y="-150" width="18" height="44" rx="9" fill="{INK}"/>'
         f'<text x="0" y="72" text-anchor="middle" font-family="FR" font-size="150" fill="{INK}">{num}</text>')
    if cross: g += f'<path d="M-80 -50 L 80 90 M 80 -50 L -80 90" stroke="{RED}" stroke-width="18" stroke-linecap="round"/>'
    return g + "</g>"
def bed(x, y, s=1.0):                                                   # someone fast asleep
    return (f'<g transform="translate({x},{y}) scale({s})"><rect x="-210" y="-70" width="420" height="70" rx="16" fill="#fff" {O}/>'
            f'<rect x="-230" y="-160" width="34" height="200" rx="12" fill="#8a5a2b" {O}/><rect x="196" y="-110" width="34" height="150" rx="12" fill="#8a5a2b" {O}/>'
            f'<ellipse cx="-140" cy="-86" rx="56" ry="26" fill="#fff" {O}/><circle cx="-130" cy="-118" r="38" fill="{SKIN[2]}" {O}/>'
            f'<path d="M-100 -60 C -100 -120 190 -120 196 -60 Z" fill="#4D96FF" {O}/></g>'
            f'<text x="{x + 30}" y="{y - 200 * s:.0f}" font-family="FR" font-size="{70 * s:.0f}" fill="#fff" stroke="{INK}" stroke-width="5" paint-order="stroke">z z Z</text>')

# per set, per slide: (background, marker colour, doodle colours, the scene's SVG)
ART = {"pronouns": {
 "cover": ("#FFC93C", None, ["#fff", "#FF7A59", "#4D96FF"], None),
 "I": ("#FF7A59", "#FFC93C", ["#FFC93C", "#fff"],
       person(470, 370, 1.15, SKIN[1], "hair:#3a2a1c", "#2E7263", "#2a1d14", "self")
       + f'<g transform="translate(640,70)"><rect x="0" y="0" width="200" height="130" rx="10" fill="#C1272D" {O}/><path d="M100 30 L 112 66 L 150 66 L 119 88 L 131 124 L 100 102 L 69 124 L 81 88 L 50 66 L 88 66 Z" fill="none" stroke="#006233" stroke-width="7"/><path d="M0 0 L 0 300" stroke="{INK}" stroke-width="8"/></g>'),
 "you (to a man)": ("#4D96FF", "#FFC93C", ["#FFC93C", "#fff", "#FF7A59"],
       person(600, 370, 1.15, SKIN[3], "kufi", "#FF7A59", "#2a1d14", "book:#2E7263")
       + f'<rect x="680" y="160" width="60" height="110" rx="16" fill="{GOLD}" {O}/>' + hand(400, 170)),
 "you (to a woman)": ("#F49AC1", "#FFE66D", ["#fff", "#9B6BFF"],
       person(600, 370, 1.15, SKIN[2], "hijab:#9B6BFF", "#2E7263", None, "book:#FFC93C") + hand(400, 170, colour=SKIN[0])),
 "he": ("#2EB67D", "#FFE66D", ["#fff", "#FFE66D"],
       mosque(330, 380, 1.0) + person(700, 380, 1.15, SKIN[0], "kufi", "#fff", "#e6e6e6", "fold")),
 "she": ("#9B6BFF", "#FFE66D", ["#fff", "#F49AC1"],
       f'<g transform="translate(210,40)"><rect x="0" y="0" width="200" height="240" rx="100" fill="#cfe5ff" {O}/><path d="M100 0 L 100 240 M 0 130 L 200 130" stroke="{INK}" stroke-width="6"/></g>'
       + person(620, 380, 1.15, SKIN[4], "hijab:#fff", "#2E7263", None, "book:#2E7263")
       + f'<path d="M560 230 L 680 230" stroke="{GOLD}" stroke-width="0"/>'),
 "we": ("#FFB23F", "#fff", ["#fff", "#FF7A59", "#2E7263"],
       f'<path d="M340 20 L 340 -10 C 340 -110 740 -110 740 -10 L 740 20" fill="none" stroke="{INK}" stroke-width="0"/>'
       f'<g><path d="M390 360 L 390 120 C 390 20 690 20 690 120 L 690 360 Z" fill="#fff" {O}/><path d="M430 360 L 430 140 C 430 70 650 70 650 140 L 650 360 Z" fill="{TEAL}" {O}/></g>'
       + "".join(f'<rect x="{x - 70}" y="340" width="140" height="40" rx="8" fill="{c}" {O}/>' for x, c in ((210, RED), (420, "#4D96FF"), (660, RED), (870, "#4D96FF")))
       + "".join(person(x, 372, 1.0, sk, top, bd, None, "fold", legs=True) for x, sk, top, bd in
                 ((210, SKIN[2], "kufi", "#fff"), (420, SKIN[0], "kufi", "#cfe5ff"), (660, SKIN[1], "kufi", "#fff"), (870, SKIN[3], "kufi", "#FFE66D")))),
 "end": ("#2E7263", None, ["#FFC93C", "#fff", "#FF7A59"], None),
},
 # family (#305): mum and child with a heart; dad and son walking to the mosque; brother at the tap for wudu; big sister and little brother;
 # grandad and uncle in the garden; grandma between two houses (she lives near us)
 "family": {
 "cover": ("#FFC93C", None, ["#fff", "#FF7A59", "#4D96FF"], None),
 "mum": ("#FF7A59", "#FFE66D", ["#FFE66D", "#fff"],
       person(600, 370, 1.15, SKIN[2], "hijab:#fff", "#2E7263", None, "fold") + person(400, 370, 0.75, SKIN[2], "hair:#3a2a1c", "#FFC93C", None, "wave")
       + f'<path d="M500 110 C 470 70 420 90 440 130 L 500 190 L 560 130 C 580 90 530 70 500 110 Z" fill="{RED}" {O}/>'),
 "dad": ("#4D96FF", "#FFC93C", ["#FFC93C", "#fff"],
       mosque(300, 380, 0.9) + person(660, 370, 1.15, SKIN[3], "kufi", "#fff", "#2a1d14") + person(820, 370, 0.75, SKIN[3], "kufi", "#FFC93C", None, "wave")),
 "brother": ("#2EB67D", "#FFE66D", ["#fff", "#FFE66D"],
       f'<g transform="translate(380,0)"><rect x="-150" y="40" width="300" height="160" rx="10" fill="#cfe5ff" {O}/>'
       f'<path d="M-10 200 L -10 130 C -10 100 60 100 60 130 L 60 150" fill="none" stroke="{INK}" stroke-width="14" stroke-linecap="round"/>'
       + "".join(f'<path d="M60 {y} C 52 {y + 16} 52 {y + 26} 60 {y + 30} C 68 {y + 26} 68 {y + 16} 60 {y} Z" fill="#4D96FF" {O}/>' for y in (162, 196, 230))
       + f'<path d="M-120 250 L 120 250 C 120 310 -120 310 -120 250 Z" fill="#fff" {O}/><rect x="-24" y="296" width="48" height="74" fill="#fff" {O}/></g>'
       + person(680, 370, 1.15, SKIN[1], "hair:#3a2a1c", "#FF7A59", "#2a1d14", "fold")),
 "sister": ("#9B6BFF", "#FFE66D", ["#fff", "#F49AC1"],
       person(460, 370, 1.2, SKIN[0], "hijab:#FFC93C", "#2E7263", None, "book:#FF7A59") + person(660, 370, 0.7, SKIN[0], "kufi", "#FF7A59", None, "wave")),
 "grandpa": ("#FFB23F", "#fff", ["#fff", "#2EB67D"],
       f'<rect x="210" y="190" width="40" height="180" fill="#8d5f3e" {O}/><circle cx="230" cy="150" r="96" fill="#2EB67D" {O}/>'
       + "".join(f'<path d="M{x} 370 L {x} 320" stroke="{TEAL}" stroke-width="6"/><circle cx="{x}" cy="312" r="14" fill="{c}" {O}/>' for x, c in ((340, RED), (380, "#fff"), (420, "#9B6BFF")))
       + person(580, 370, 1.1, SKIN[0], "kufi", "#fff", "#f4f4f4", "fold") + person(790, 370, 1.1, SKIN[0], "hair:#3a2a1c", "#4D96FF", "#2a1d14", "wave")),
 "grandma": ("#F49AC1", "#FFE66D", ["#fff", "#9B6BFF"],
       "".join(f'<g transform="translate({x},370)"><rect x="-100" y="-160" width="200" height="160" fill="{c}" {O}/><path d="M-122 -160 L 0 -250 L 122 -160 Z" fill="{RED}" {O}/>'
               f'<rect x="-26" y="-86" width="52" height="86" fill="{TEAL}" {O}/></g>' for x, c in ((200, "#fff"), (880, "#FFE66D")))
       + f'<path d="M300 362 L 780 362" stroke="{INK}" stroke-width="6" stroke-dasharray="4 18" stroke-linecap="round"/>'
       + person(540, 360, 1.05, SKIN[4], "hijab:#fff", "#9B6BFF", None, "wave")),
 "end": ("#2E7263", None, ["#FFC93C", "#fff", "#FF7A59"], None),
},
 # the little words (#308): a student with two books; coffee loved but not drunk; football with friends; tea at home; "where are you from?";
 # off to the mosque on a Friday
 "little": {
 "cover": ("#4D96FF", None, ["#fff", "#FFC93C", "#FF7A59"], None),
 "and": ("#FF7A59", "#FFE66D", ["#FFE66D", "#fff"],
       person(540, 370, 1.15, SKIN[3], "hijab:#2E7263", "#FFC93C", None, "fold")
       + "".join(f'<g transform="translate({x},{y}) rotate({r})"><rect x="-70" y="-90" width="140" height="180" rx="10" fill="{c}" {O}/><rect x="-50" y="-60" width="100" height="16" rx="6" fill="#fff"/>'
                 f'<text x="0" y="40" text-anchor="middle" font-family="{fa}" font-size="{fs}" fill="#fff">{w}</text></g>' for x, y, r, c, w, fa, fs in
                 ((270, 220, -8, "#2E7263", "ع", "AR", 76), (810, 220, 8, "#9B6BFF", "📜", "FR", 64)))
       + f'<text x="540" y="70" text-anchor="middle" font-family="FR" font-size="90" fill="{INK}">+</text>'),
 "but": ("#9B6BFF", "#FFE66D", ["#fff", "#F49AC1"],
       person(380, 370, 1.15, SKIN[1], "hair:#3a2a1c", "#FF7A59", "#2a1d14", "fold")
       + f'<g transform="translate(700,250)"><path d="M-70 -60 H70 V10 C70 60 40 90 0 90 C-40 90 -70 60 -70 10 Z" fill="#fff" {O}/><path d="M70 -40 C110 -40 110 30 70 30" fill="none" stroke="{INK}" stroke-width="10"/>'
         f'<path d="M-20 -80 C-30 -100 -10 -110 -20 -130 M20 -80 C10 -100 30 -110 20 -130" fill="none" stroke="#fff" stroke-width="8" stroke-linecap="round"/></g>'
       + f'<path d="M560 120 C 540 90 500 100 512 130 L 560 176 L 608 130 C 620 100 580 90 560 120 Z" fill="{RED}" {O}/>'
       + f'<path d="M820 120 L 900 200 M 900 120 L 820 200" stroke="{RED}" stroke-width="18" stroke-linecap="round"/>'),
 "with": ("#2EB67D", "#FFE66D", ["#fff", "#FFE66D"],
       "".join(person(x, 370, 1.0, sk, top, bd, None, arm) for x, sk, top, bd, arm in
               ((230, SKIN[0], "kufi", "#4D96FF", "wave"), (430, SKIN[2], "hair:#2a1d14", "#FF7A59", None), (850, SKIN[4], "kufi", "#FFC93C", "wave")))
       + f'<g transform="translate(640,320)"><circle r="44" fill="#fff" {O}/><path d="M0 -18 L 17 -6 L 11 14 L -11 14 L -17 -6 Z" fill="{INK}"/></g>'),
 "in": ("#FFB23F", "#fff", ["#fff", "#2EB67D"],
       f'<g transform="translate(540,385)"><rect x="-300" y="-250" width="600" height="250" fill="#fff" {O}/><path d="M-340 -250 L 0 -330 L 340 -250 Z" fill="{RED}" {O}/>'
       f'<rect x="-250" y="-200" width="220" height="150" fill="#cfe5ff" {O}/><rect x="30" y="-200" width="220" height="150" fill="#cfe5ff" {O}/></g>'
       + person(400, 325, 0.5, SKIN[2], "hijab:#9B6BFF", "#2E7263", None, "fold", legs=False) + person(680, 325, 0.5, SKIN[0], "kufi", "#FF7A59", None, "fold", legs=False)
       + "".join(f'<g transform="translate({x},285)"><rect x="-22" y="-26" width="44" height="40" rx="8" fill="{GOLD}" {O}/><path d="M22 -16 C 40 -16 40 6 22 6" fill="none" stroke="{INK}" stroke-width="6"/></g>' for x in (470, 610))),
 "from": ("#F49AC1", "#FFE66D", ["#fff", "#9B6BFF"],
       person(330, 370, 1.1, SKIN[1], "kufi", "#2E7263", "#2a1d14", "wave") + person(750, 370, 1.1, SKIN[3], "hair:#3a2a1c", "#4D96FF", "#2a1d14")
       + f'<g transform="translate(540,110)"><circle r="70" fill="#4D96FF" {O}/><path d="M-30 -50 C -10 -30 -40 -10 -20 10 C 0 30 30 10 40 30 M10 -60 C 30 -40 50 -40 60 -20" fill="none" stroke="#2EB67D" stroke-width="16" stroke-linecap="round"/></g>'
       + f'<text x="540" y="290" text-anchor="middle" font-family="FR" font-size="110" fill="{INK}">?</text>'),
 "to": ("#2E7263", "#FFE66D", ["#FFC93C", "#fff"],
       person(260, 370, 1.1, SKIN[0], "kufi", "#fff", "#2a1d14") + mosque(760, 380, 0.85)
       + f'<path d="M370 300 C 450 250 520 250 590 290" fill="none" stroke="{GOLD}" stroke-width="12" stroke-linecap="round" stroke-dasharray="2 24"/>'
       + f'<path d="M575 262 L 610 296 L 565 310" fill="none" stroke="{GOLD}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>'),
 "end": ("#FF7A59", None, ["#FFC93C", "#fff", "#4D96FF"], None),
},
 "food": {
 "cover": ("#FFC93C", None, ["#fff", "#FF7A59", "#4D96FF"], None),
 "water": ("#4D96FF", "#FFE66D", ["#fff", "#FFE66D"],
       person(330, 370, 1.1, SKIN[1], "kufi", "#2EB67D", "#2a1d14", "fold") + jug(640, 365, 1.1) + glass(820, 365, 1.25)
       + "".join(f'<path transform="translate({x},{y})" d="M0 -26 C 14 -6 18 4 18 10 A 18 18 0 0 1 -18 10 C -18 4 -14 -6 0 -26 Z" fill="#cfe9ff" {O}/>' for x, y in ((760, 90), (900, 150), (560, 110)))),
 "bread": ("#FFB23F", "#fff", ["#fff", "#FF7A59"],
       person(260, 370, 1.1, SKIN[3], "hijab:#9B6BFF", "#2E7263", None, "wave")
       + f'<rect x="440" y="300" width="560" height="26" rx="10" fill="#8a5a2b" {O}/><rect x="470" y="326" width="22" height="50" fill="#8a5a2b" {O}/><rect x="948" y="326" width="22" height="50" fill="#8a5a2b" {O}/>'
       + plate(640, 290, 1.1, "bread") + glass(880, 296, 1.1, "#ffffff")),
 "dates": ("#9B6BFF", "#FFE66D", ["#FFE66D", "#fff"],
       person(250, 370, 1.1, SKIN[0], "kufi", "#fff", "#e6e6e6", "fold") + plate(620, 330, 1.35, "dates") + moon(900, 110, 1.0)
       + f'<g transform="translate(470,40)"><path d="M0 0 L 0 50" stroke="{INK}" stroke-width="5"/><path d="M-30 50 L 30 50 L 40 110 L 0 140 L -40 110 Z" fill="{GOLD}" {O}/><path d="M-16 64 L 16 64 L 22 104 L 0 120 L -22 104 Z" fill="#fff6c9"/></g>'),
 "tea": ("#2EB67D", "#FFE66D", ["#fff", "#FFE66D"],
       person(330, 370, 1.15, SKIN[2], "hair:#2a1d14", "#FF7A59", None, "book:#4D96FF") + teaglass(720, 350, 1.4)),
 "milk": ("#F49AC1", "#FFE66D", ["#fff", "#4D96FF"],
       person(280, 370, 1.1, SKIN[4], "hijab:#2E7263", "#FFC93C", None, "self") + glass(560, 365, 1.35, "#ffffff")
       + teaglass(850, 330, 1.0) + f'<path d="M770 140 L 930 300 M 930 140 L 770 300" stroke="{RED}" stroke-width="20" stroke-linecap="round"/>'),
 "coffee": ("#FF7A59", "#FFE66D", ["#FFE66D", "#fff"],
       person(220, 370, 1.05, SKIN[1], "kufi", "#2E7263", "#2a1d14", "fold") + dallah(560, 360, 1.15) + finjan(700, 360, 1.0) + finjan(790, 360, 1.0)
       + person(930, 370, 1.05, SKIN[3], "hair:#3a2a1c", "#4D96FF", "#2a1d14", "wave")),
 "end": ("#2E7263", None, ["#FFC93C", "#fff", "#FF7A59"], None),
},
 "days": {
 "cover": ("#4D96FF", None, ["#fff", "#FFC93C", "#FF7A59"], None),
 "Sunday": ("#FF7A59", "#FFE66D", ["#FFE66D", "#fff"], cal(540, 230, "1", "#FFC93C", 1.25) + person(230, 370, 1.0, SKIN[0], "kufi", "#4D96FF", "#2a1d14", "wave")
            + person(860, 370, 1.0, SKIN[3], "hijab:#2E7263", "#FFC93C", None, "fold")),
 "Monday": ("#4D96FF", "#FFE66D", ["#FFE66D", "#fff"], cal(540, 230, "2", "#FF7A59", 1.25) + person(240, 370, 1.0, SKIN[1], "kufi", "#2EB67D", "#2a1d14", "fold") + moon(860, 120, 0.9)),
 "Tuesday": ("#2EB67D", "#FFE66D", ["#fff", "#FFE66D"], cal(420, 230, "3", "#9B6BFF", 1.25)
            + f'<g transform="translate(780,220)"><circle r="120" fill="#fff" {O}/><path d="M0 0 L 0 -120 A 120 120 0 0 1 103.9 60 Z" fill="#FFC93C" {O}/></g>'
            + f'<text x="780" y="385" text-anchor="middle" font-family="FR" font-size="44" fill="{INK}">⅓</text>'),
 "Wednesday": ("#9B6BFF", "#FFE66D", ["#FFE66D", "#fff"], cal(540, 210, "4", "#2EB67D", 1.15)
            + "".join(f'<g transform="translate({x},370)"><rect x="-50" y="-170" width="100" height="170" rx="10" fill="{c}" {O}/><path d="M-30 -22 L -30 -110 C -30 -140 0 -150 0 -150 C 0 -150 30 -140 30 -110 L 30 -22 Z" fill="none" stroke="#fff" stroke-width="7"/>'
                      f'<path d="M-40 -8 L 40 -8" stroke="#fff" stroke-width="5" stroke-dasharray="6 8"/></g>'
                      for x, c in ((150, "#FF7A59"), (290, "#FFC93C"), (790, "#2E7263"), (930, "#4D96FF")))),
 "Thursday": ("#FFB23F", "#FFE66D", ["#fff", "#FF7A59"], cal(540, 230, "5", "#4D96FF", 1.25) + person(230, 370, 1.0, SKIN[2], "hijab:#9B6BFF", "#2E7263", None, "book:#FFC93C") + moon(860, 120, 0.9, "#fff")),
 "Friday": ("#2E7263", "#FFE66D", ["#FFC93C", "#fff"], mosque(540, 300, 0.85) + cal(930, 100, "6", "#FF7A59", 0.5, cross=True)
            + "".join(person(x, 385, 0.62, sk, top, bd) for x, sk, top, bd in ((110, SKIN[0], "kufi", "#4D96FF"), (220, SKIN[3], "hijab:#FFC93C", "#FF7A59"), (330, SKIN[1], "kufi", "#fff"),
                                                                         (760, SKIN[2], "kufi", "#9B6BFF"), (870, SKIN[4], "hijab:#fff", "#2EB67D"), (980, SKIN[1], "kufi", "#FFC93C")))),
 "Saturday": ("#F49AC1", "#FFE66D", ["#fff", "#4D96FF"], bed(560, 370, 1.0) + cal(140, 190, "7", "#9B6BFF", 0.6)),
 "end": ("#FF7A59", None, ["#FFC93C", "#fff", "#4D96FF"], None),
}}
CAST = (person(130, 300, 0.85, SKIN[1], "hair:#3a2a1c", "#2E7263", "#2a1d14", "wave") + person(330, 300, 0.85, SKIN[3], "kufi", "#FF7A59", "#2a1d14")
        + person(530, 300, 0.85, SKIN[2], "hijab:#9B6BFF", "#2E7263") + person(730, 300, 0.85, SKIN[0], "kufi", "#fff", "#e6e6e6", "fold")
        + person(930, 300, 0.85, SKIN[4], "hijab:#fff", "#2E7263", None, "book:#2E7263"))

def slides(sid):
    cover, W = SETS[sid]; A = ART[sid]; n = len(W); out = {}
    bg, _, dc, _ = A["cover"]
    pal = ["#FF7A59", "#4D96FF", "#F49AC1", "#2EB67D", "#9B6BFF", "#FFB23F"]
    words = "".join(f'<b style="background:{pal[i % 6]};transform:rotate({(-3, 2, -2, 3, -1)[i % 5]}deg)">{w}</b>' for i, w in enumerate(COVER[sid].split(" · ")))
    out["1"] = (f'<body style="background:{bg}">{sparkles(1, dc)}<div class="top">{S.BRAND.replace("brand", "brand")}<div class="cnt">swipe →</div></div>'
                f'<div class="cov">{words}</div><div class="bubble" style="top:640px">{cover}</div>'
                f'<svg viewBox="0 0 1080 320" width="1080" style="position:absolute;left:0;bottom:120px">{CAST}</svg>'
                f'<div class="swipe"><span>Swipe and count your score →</span></div></body>')
    for k, (en, ar, tr, ex, note) in enumerate(W, 2):
        bg, mk, dc, art = A[en]
        s, h, t, m = ex[0]
        card = f'<div class="card" style="top:{990 if note else 1010}px"><div class="s">{s.replace(h, f"<i style=background:{mk}>{h}</i>", 1)}</div><div class="t">{t}</div><div class="m">{m}</div></div>'
        out[str(k)] = (f'<body style="background:{bg}">{sparkles(k, dc)}<div class="top">{S.BRAND}<div class="cnt">{k - 1} / {n}</div></div>'
                       f'<div class="en"><span>{en[0].upper() + en[1:]}</span></div><div class="ar">{ar}</div><div class="tr"><span>{tr}</span></div>'
                       f'<div class="art"><svg viewBox="0 0 1080 390" width="1080" height="390">{art}</svg></div>{card}'
                       + (f'<div class="note">{ar_spans(note)}</div>' if note else "") + '</body>')
    bg, _, dc, _ = A["end"]
    out[str(n + 2)] = (f'<body style="background:{bg}">{sparkles(99, dc)}<div class="top">{S.BRAND}<div class="cnt">{n + 1} / {n + 1}</div></div>'
                       f'<div class="endq">How many<br>did you know?<br><i>Comment /{n} 👇</i></div>'
                       f'<svg viewBox="0 0 1080 320" width="1080" style="position:absolute;left:0;top:640px">{CAST}</svg>'
                       '<div class="ends"><div>Save this 📌 for later</div><div>Send it to someone learning Arabic with you</div></div></body>')
    return out

if __name__ == "__main__":
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=S.CHROME if os.path.exists(S.CHROME) else None)
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for sid in ART:
            if sys.argv[1:] and sid not in sys.argv[1:]: continue
            out = os.path.join(S.HERE, "stills", sid + "-pop"); os.makedirs(out, exist_ok=True)
            for k, body in slides(sid).items():
                tmp = os.path.join(out, "_s.html"); open(tmp, "w").write(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>{body}</html>')
                pg.goto("file://" + tmp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
                pg.screenshot(path=os.path.join(out, f"{sid}-{k}.png"))
            os.remove(os.path.join(out, "_s.html")); print(sid, "->", out)
        b.close()
