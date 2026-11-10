#!/usr/bin/env python3
"""The word carousels redone with drawings and popping colour (owner, 28 Oct 2026, #304: "carousels with a boring plain background and no
pictures or drawings don't perform well… add some pics, drawings and make it not boring. Add more popping colour"). Same words and course
sentences as build_word_carousels.py (SETS), new look: a bold colour per slide with doodles, the English word on a tilted sticker, the
Arabic big with an ink outline, a drawn scene for the sentence (faceless figures: no eyes, owner, 27 Oct), the sentence on a card with a
hard ink shadow, the note on a sticky note.

  python3 brag-quiz/build_pop_carousel.py [set ...]   ->  brag-quiz/stills/<set>-pop/<set>-<n>.png   (sets with ART below)
  python3 brag-quiz/build_pop_carousel.py --tiktok [set ...]   ->  brag-quiz/stills/<set>-tiktok/<set>-<nn>.jpg, 1080×1920 for TikTok photo mode
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
.ar i {{ font-style:normal; color:#FFE66D; }}
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

def kaaba(x, y, s=1.0):                                                 # the Kaaba, three-quarter view, base at (x, y)
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M-120 -230 L -50 -262 L 140 -262 L 70 -230 Z" fill="#3a3a3a" {O}/>'
            f'<path d="M70 -230 L 140 -262 L 140 -32 L 70 0 Z" fill="#2b2b2b" {O}/><rect x="-120" y="-230" width="190" height="230" fill="#1d1d1d" {O}/>'
            f'<rect x="-117" y="-188" width="184" height="26" fill="{GOLD}"/><path d="M73 -188 L 137 -218 L 137 -192 L 73 -162 Z" fill="{GOLD}"/>'
            f'<rect x="12" y="-128" width="38" height="96" rx="4" fill="{GOLD}" {O}/></g>')
def sun(x, y, s=1.0, c="#FFE66D"):
    rays = "".join(f'<path d="M0 -96 L 0 -136" transform="rotate({a})" stroke="{INK}" stroke-width="14" stroke-linecap="round"/><path d="M0 -96 L 0 -136" transform="rotate({a})" stroke="{c}" stroke-width="6" stroke-linecap="round"/>' for a in range(0, 360, 30))
    return f'<g transform="translate({x},{y}) scale({s})">{rays}<circle r="78" fill="{c}" {O}/></g>'
def flower(x, y, c, s=1.0):
    pet = "".join(f'<ellipse cx="0" cy="-26" rx="15" ry="24" transform="rotate({a})" fill="{c}" {O}/>' for a in range(0, 360, 72))
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M0 0 L 0 -90" stroke="{INK}" stroke-width="12"/><path d="M0 0 L 0 -90" stroke="#2E7263" stroke-width="5"/>'
            f'<path d="M0 -40 C 20 -60 40 -50 44 -40 C 30 -30 12 -32 0 -40 Z" fill="#7bd389" {O}/><g transform="translate(0,-110)">{pet}<circle r="14" fill="{GOLD}" {O}/></g></g>')
def flake(x, y, s=1.0):
    arms = "".join(f'<g transform="rotate({a})"><path d="M0 0 L 0 -40 M 0 -24 L -12 -36 M 0 -24 L 12 -36" stroke="#fff" stroke-width="7" stroke-linecap="round" fill="none"/></g>' for a in range(0, 360, 60))
    return f'<g transform="translate({x},{y}) scale({s})">{arms}</g>'
def house(x, y, s=1.0, c="#FFF8EC"):                                    # a little house with its door wide open and nobody home
    return (f'<g transform="translate({x},{y}) scale({s})"><rect x="-130" y="-170" width="260" height="170" fill="{c}" {O}/>'
            f'<path d="M-160 -166 L 0 -280 L 160 -166 Z" fill="{RED}" {O}/><rect x="-40" y="-120" width="80" height="120" fill="#3a2a1c" {O}/>'
            f'<path d="M40 -120 L 86 -100 L 86 14 L 40 0 Z" fill="#c48f66" {O}/><rect x="-108" y="-130" width="50" height="50" fill="#9fd8ff" {O}/></g>')
def star(x, y, r, c=GOLD):
    import math
    pts = " ".join(f"{x + (r if k % 2 == 0 else r * .45) * math.sin(k * math.pi / 5):.1f},{y - (r if k % 2 == 0 else r * .45) * math.cos(k * math.pi / 5):.1f}" for k in range(10))
    return f'<polygon points="{pts}" fill="{c}" {O}/>'
def lantern(x, y, s=1.0):                                               # a Ramadan lantern hanging from a chain at (x, y)
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M0 0 L 0 40" stroke="{INK}" stroke-width="5"/><path d="M-24 40 L 24 40 L 0 20 Z" fill="{GOLD}" {O}/>'
            f'<path d="M-34 44 L 34 44 L 28 120 L 0 140 L -28 120 Z" fill="{GOLD}" {O}/><path d="M-18 58 L 18 58 L 14 112 L 0 124 L -14 112 Z" fill="#fff6c9"/></g>')
def seated(x, y, s=1.0, skin=SKIN[0], top=None, body="#4D96FF", beard=None, arm="fold"):    # sitting cross-legged on the floor at (x, y)
    return (f'<ellipse cx="{x}" cy="{y - 14 * s:.0f}" rx="{76 * s:.0f}" ry="{26 * s:.0f}" fill="{INK}"/>'
            + person(x, y + 36 * s, s, skin, top, body, beard, arm, legs=False))
def balloon(x, y, c):
    return f'<path d="M{x} {y + 70} q -16 40 6 80" fill="none" stroke="{INK}" stroke-width="4"/><ellipse cx="{x}" cy="{y}" rx="44" ry="56" fill="{c}" {O}/><path d="M{x - 8} {y + 54} L {x + 8} {y + 54} L {x} {y + 70} Z" fill="{c}" {O}/>'
def drops(pts, s=1.0):
    return "".join(f'<path transform="translate({x},{y}) scale({s})" d="M0 -26 C 14 -6 18 4 18 10 A 18 18 0 0 1 -18 10 C -18 4 -14 -6 0 -26 Z" fill="#cfe9ff" {O}/>' for x, y in pts)
def tap(x, y, to):                                                       # a tap on the wall at (x, y), water falling to y = to
    return (f'<rect x="{x - 150}" y="{y - 20}" width="130" height="40" rx="8" fill="#cfd8dc" {O}/><path d="M{x - 30} {y - 20} L {x + 20} {y - 20} Q {x + 40} {y - 20} {x + 40} {y} L {x + 40} {y + 30} L {x} {y + 30} L {x} {y + 20} L {x - 30} {y + 20} Z" fill="#cfd8dc" {O}/>'
            f'<rect x="{x - 14}" y="{y - 50}" width="28" height="30" rx="6" fill="{RED}" {O}/>'
            f'<path d="M{x + 8} {y + 34} L {x + 8} {to}" stroke="{INK}" stroke-width="30" stroke-linecap="round"/><path d="M{x + 8} {y + 34} L {x + 8} {to}" stroke="#9fd8ff" stroke-width="18" stroke-linecap="round"/>')
def ring(x, y, r):                                                       # the bit to wash, ringed
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{INK}" stroke-width="16"/><circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="#FFE66D" stroke-width="9" stroke-dasharray="20 12"/>'
def bighead(x, y, r=150, skin=SKIN[1], top="hair:#2a1d14", ears=True, beard=None):   # a big faceless head and shoulders, centre (x, y)
    g = f'<path d="M{x - 1.9 * r:.0f} 400 C {x - 1.8 * r:.0f} {y + 1.1 * r:.0f} {x + 1.8 * r:.0f} {y + 1.1 * r:.0f} {x + 1.9 * r:.0f} 400 Z" fill="#2E7263" {O}/>'
    if ears: g += "".join(f'<ellipse cx="{x + d * r * .98:.0f}" cy="{y + 6}" rx="{r * .17:.0f}" ry="{r * .26:.0f}" fill="{skin}" {O}/>' for d in (-1, 1))
    g += f'<ellipse cx="{x}" cy="{y}" rx="{r * .95:.0f}" ry="{r:.0f}" fill="{skin}" {O}/>'
    if beard: g += f'<path d="M{x - .8 * r:.0f} {y + .2 * r:.0f} C {x - .7 * r:.0f} {y + 1.2 * r:.0f} {x + .7 * r:.0f} {y + 1.2 * r:.0f} {x + .8 * r:.0f} {y + .2 * r:.0f} C {x + .4 * r:.0f} {y + .55 * r:.0f} {x - .4 * r:.0f} {y + .55 * r:.0f} {x - .8 * r:.0f} {y + .2 * r:.0f} Z" fill="{beard}" {O}/>'
    if top and top.startswith("hair"): g += f'<path d="M{x - .93 * r:.0f} {y - .1 * r:.0f} C {x - 1.0 * r:.0f} {y - 1.25 * r:.0f} {x + 1.0 * r:.0f} {y - 1.25 * r:.0f} {x + .93 * r:.0f} {y - .1 * r:.0f} C {x + .6 * r:.0f} {y - .55 * r:.0f} {x - .6 * r:.0f} {y - .55 * r:.0f} {x - .93 * r:.0f} {y - .1 * r:.0f} Z" fill="{top.split(":")[1]}" {O}/>'
    return g
def palm(x, y, rot, skin=SKIN[1], sleeve="#2E7263", fx=None, fy=None):   # a hand at (x, y) on an arm coming in from (fx, fy)
    g = ""
    if fx is not None: g += f'<path d="M{fx} {fy} L {x} {y}" stroke="{INK}" stroke-width="58" stroke-linecap="round"/><path d="M{fx} {fy} L {x} {y}" stroke="{sleeve}" stroke-width="46" stroke-linecap="round"/>'
    return g + f'<ellipse cx="{x}" cy="{y}" rx="62" ry="36" transform="rotate({rot} {x} {y})" fill="{skin}" {O}/>'

def lbadge(x, y, sun):                                                  # the ل of al-: crossed out (a sun letter, silent) or ticked (a moon letter, said)
    g = (f'<g transform="translate({x},{y})"><rect x="-150" y="-70" width="300" height="140" rx="28" fill="{PAPER}" {O}/>'
         + (sun_(-80, 0, 0.42) if sun else moon(-80, 0, 0.7))
         + f'<text x="40" y="38" text-anchor="middle" font-family="AR" font-size="110" fill="{INK}">ل</text>')
    if sun: g += f'<path d="M-6 -46 L 86 50" stroke="{RED}" stroke-width="16" stroke-linecap="round"/><text x="0" y="112" text-anchor="middle" font-family="FR" font-size="34" fill="#fff" stroke="{INK}" stroke-width="6" paint-order="stroke">silent</text>'
    else: g += f'<path d="M84 -10 L 104 14 L 140 -34" fill="none" stroke="#2E7263" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/><text x="0" y="112" text-anchor="middle" font-family="FR" font-size="34" fill="#fff" stroke="{INK}" stroke-width="6" paint-order="stroke">say it</text>'
    return g + '</g>'
def sun_(x, y, s=1.0): return sun(x, y, s, "#FFC93C")
def hills(c="#7bd389"): return f'<path d="M0 400 C 180 300 360 320 540 370 C 720 310 900 300 1080 360 L 1080 400 Z" fill="{c}" {O}/>'
def rehal(x, y, s=1.0):                                                 # an open mushaf on its folding stand
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M-150 0 L 0 -90 L 150 0 M -150 -10 L 0 60 L 150 -10" fill="none" stroke="#8a5a2b" stroke-width="16" stroke-linecap="round"/>'
            f'<path d="M0 -60 C -50 -96 -120 -100 -170 -80 L -150 20 C -100 0 -40 4 0 34 Z" fill="#fff" {O}/><path d="M0 -60 C 50 -96 120 -100 170 -80 L 150 20 C 100 0 40 4 0 34 Z" fill="#fff" {O}/>'
            + "".join(f'<path d="M{a} {b} L {a + 90 * d} {b - 12}" stroke="{INK}" stroke-width="4" opacity=".5"/>' for d in (-1, 1) for a, b in ((d * 26, -40), (d * 26, -20), (d * 26, 0))) + '</g>')
def car(x, y, s=1.0, c="#FF7A59"):
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M-170 -30 L -150 -90 Q -140 -110 -110 -110 L 70 -110 Q 100 -110 120 -80 L 150 -40 L 170 -36 Q 190 -30 190 -10 L 190 0 L -170 0 Z" fill="{c}" {O}/>'
            f'<path d="M-120 -96 L 0 -96 L 0 -48 L -140 -48 Z M 20 -96 L 90 -96 L 120 -48 L 20 -48 Z" fill="#cfe9ff" {O}/>'
            f'<circle cx="-100" cy="4" r="34" fill="{INK}"/><circle cx="-100" cy="4" r="14" fill="#cfd8dc"/><circle cx="120" cy="4" r="34" fill="{INK}"/><circle cx="120" cy="4" r="14" fill="#cfd8dc"/></g>')
def board(x, y, w=420, h=230):
    return (f'<rect x="{x - w / 2}" y="{y - h}" width="{w}" height="{h}" rx="14" fill="#2E5E4E" stroke="#8a5a2b" stroke-width="14"/>'
            f'<text x="{x}" y="{y - h / 2 + 30}" text-anchor="middle" font-family="AR" font-size="84" fill="#fff">أ ب ت</text>')
def bag(x, y, s=1.0, c="#9B6BFF"):
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M-46 -150 C -46 -200 46 -200 46 -150" fill="none" stroke="{INK}" stroke-width="14"/>'
            f'<rect x="-90" y="-160" width="180" height="160" rx="26" fill="{c}" {O}/><rect x="-50" y="-100" width="100" height="44" rx="10" fill="#FFE66D" {O}/></g>')
def bookc(x, y, s=1.0, c="#4D96FF"):
    return f'<g transform="translate({x},{y}) scale({s})"><rect x="-70" y="-180" width="140" height="180" rx="10" fill="{c}" {O}/><rect x="-50" y="-150" width="100" height="40" rx="6" fill="#fff" {O}/></g>'
def crane(x, y):
    return (f'<rect x="{x}" y="{y - 330}" width="22" height="330" fill="#FFC93C" {O}/><path d="M{x - 60} {y - 330} L {x + 220} {y - 330}" stroke="{INK}" stroke-width="16"/>'
            f'<path d="M{x - 60} {y - 330} L {x + 220} {y - 330}" stroke="#FFC93C" stroke-width="8"/><path d="M{x + 180} {y - 330} L {x + 180} {y - 220}" stroke="{INK}" stroke-width="4"/>'
            f'<rect x="{x + 150}" y="{y - 220}" width="60" height="40" fill="#FF7A59" {O}/>')
def heart(x, y, s=1.0, c=RED):
    return f'<path transform="translate({x},{y}) scale({s})" d="M0 30 C -60 -10 -50 -60 -20 -60 C -6 -60 0 -48 0 -40 C 0 -48 6 -60 20 -60 C 50 -60 60 -10 0 30 Z" fill="{c}" {O}/>'

PICS = "file://" + os.path.join(os.path.dirname(S.HERE), "pics")
def pic(i, x, y, d=300):                                                 # one of the app's word pictures (pics/<id>.svg), a round badge centred at (x, y)
    r = d / 2
    return (f'<circle cx="{x + 8}" cy="{y + 8}" r="{r + 4}" fill="{INK}"/><circle cx="{x}" cy="{y}" r="{r + 4}" fill="{INK}"/>'
            f'<image href="{PICS}/{i}.svg" x="{x - r}" y="{y - r}" width="{d}" height="{d}"/>')
def arrow(x1, x2, y):
    return f'<path d="M{x1} {y} L {x2} {y}" stroke="{INK}" stroke-width="14" stroke-linecap="round"/><path d="M{x2 - 26} {y - 26} L {x2} {y} L {x2 - 26} {y + 26}" fill="none" stroke="{INK}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>'
def tag(x, y, t, c="#FFF8EC", fs=46):
    w = 30 + len(t) * fs * 0.55
    return f'<rect x="{x - w / 2}" y="{y - fs * 0.85}" width="{w}" height="{fs * 1.3}" rx="{fs * 0.4}" fill="{c}" {O}/><text x="{x}" y="{y + fs * 0.2}" text-anchor="middle" font-family="FR" font-size="{fs}" fill="{INK}">{t}</text>'
def bee(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})"><ellipse cx="-14" cy="-40" rx="26" ry="34" fill="#fff" opacity=".85" {O}/><ellipse cx="18" cy="-40" rx="26" ry="34" fill="#fff" opacity=".85" {O}/>'
            f'<ellipse cx="0" cy="0" rx="58" ry="40" fill="#FFC93C" {O}/><path d="M-18 -38 C -26 -10 -26 10 -18 38 M 10 -40 C 2 -12 2 12 10 40" stroke="{INK}" stroke-width="14" fill="none"/>'
            f'<circle cx="58" cy="-4" r="22" fill="{INK}"/><path d="M-58 0 L -80 0" stroke="{INK}" stroke-width="8" stroke-linecap="round"/></g>')
def ant(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})">' + "".join(f'<path d="M{dx} 0 L {dx - 14} 30 M {dx} 0 L {dx + 14} 30" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>' for dx in (-20, 0, 20))
            + f'<ellipse cx="-44" cy="-4" rx="30" ry="22" fill="#7a3b1c" {O}/><ellipse cx="0" cy="-6" rx="20" ry="16" fill="#7a3b1c" {O}/><circle cx="34" cy="-14" r="18" fill="#7a3b1c" {O}/>'
            f'<path d="M40 -30 C 46 -50 60 -54 66 -50 M 30 -30 C 30 -54 42 -60 50 -60" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/></g>')
def cotton(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M0 0 L 0 -150 M 0 -90 L -60 -150 M 0 -110 L 60 -170" stroke="#2E7263" stroke-width="12" stroke-linecap="round"/>'
            + "".join(f'<g transform="translate({a},{b})"><circle r="34" fill="#fff" {O}/><circle cx="-22" cy="10" r="24" fill="#fff" {O}/><circle cx="22" cy="10" r="24" fill="#fff" {O}/><circle r="30" fill="#fff"/></g>' for a, b in ((0, -170), (-64, -168), (64, -188)))
            + '</g>')
def cloud(x, y, s=1.0, c="#fff"):
    return f'<g transform="translate({x},{y}) scale({s})"><path d="M-110 30 C -150 30 -150 -30 -104 -26 C -100 -80 -20 -90 0 -46 C 20 -96 110 -80 100 -20 C 150 -20 150 30 110 30 Z" fill="{c}" {O}/></g>'
def book2(x, y, s=1.0, c="#8a5a2b", tilt=0):
    return f'<g transform="translate({x},{y}) rotate({tilt}) scale({s})"><rect x="-70" y="-180" width="140" height="180" rx="10" fill="{c}" {O}/><path d="M-50 -150 L 50 -150 M -50 -125 L 30 -125" stroke="#fff" stroke-width="6" opacity=".6"/></g>'

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
},
 "months": {
 "cover": ("#FFC93C", None, ["#fff", "#FF7A59", "#9B6BFF"], None),
 "Muḥarram": ("#9B6BFF", "#FFE66D", ["#FFE66D", "#fff"], kaaba(540, 372, 1.25) + moon(880, 110, 0.9) + star(200, 90, 34) + star(300, 170, 20, "#fff") + star(790, 250, 22, "#fff")),
 "Ṣafar": ("#FFB23F", "#fff", ["#fff", "#FF7A59"], house(300, 372, 1.1)
          + "".join(f'<ellipse cx="{x}" cy="{368 - (i % 2) * 14}" rx="13" ry="7" fill="{INK}" opacity=".55"/>' for i, x in enumerate(range(460, 820, 46)))
          + person(900, 372, 0.72, SKIN[1], "kufi", "#4D96FF", "#2a1d14") + f'<text x="640" y="190" text-anchor="middle" font-family="FR" font-size="210" fill="#fff" stroke="{INK}" stroke-width="10" paint-order="stroke">0</text>'),
 "Rabīʿ": ("#2EB67D", "#FFE66D", ["#FFE66D", "#fff"], sun(900, 110, 0.75) + f'<ellipse cx="540" cy="430" rx="640" ry="110" fill="#7bd389" {O}/>'
          + "".join(flower(x, y, c, k) for x, y, c, k in ((150, 360, "#FF7A59", 1.0), (290, 340, "#F49AC1", 1.2), (440, 365, "#FFE66D", 0.9), (590, 345, "#9B6BFF", 1.15), (740, 365, "#fff", 1.0), (880, 350, "#FF7A59", 1.1)))),
 "Jumādā": ("#4D96FF", "#FFE66D", ["#fff", "#cfe9ff"], f'<ellipse cx="640" cy="340" rx="330" ry="50" fill="#cfe9ff" {O}/><path d="M440 330 L 520 350 L 600 325 M 700 345 L 780 330 L 840 352" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round"/>'
          + person(250, 372, 1.1, SKIN[3], "hijab:#FF7A59", "#9B6BFF", None, "fold", scarf="#FFE66D") + flake(560, 90, 1.1) + flake(780, 160, 0.8) + flake(920, 80, 1.0) + flake(440, 200, 0.7)),
 "Rajab": ("#F49AC1", "#FFE66D", ["#FFE66D", "#fff"], person(330, 372, 1.15, SKIN[2], "kufi", "#fff", "#2a1d14", "self") + moon(720, 150, 1.3) + star(860, 90, 46) + star(940, 230, 26, "#fff") + star(600, 280, 22, "#fff")),
 "Shaʿbān": ("#FF7A59", "#FFE66D", ["#FFE66D", "#fff"],
          "".join(f'<path d="M540 400 C 540 300 {x} 300 {x} {y}" fill="none" stroke="{INK}" stroke-width="58" stroke-linecap="round"/><path d="M540 400 C 540 300 {x} 300 {x} {y}" fill="none" stroke="#FFF8EC" stroke-width="44" stroke-linecap="round"/>' for x, y in ((180, 150), (540, 120), (900, 150)))
          + person(180, 160, 0.42, SKIN[0], "kufi", "#4D96FF", "#2a1d14") + person(540, 130, 0.42, SKIN[3], "hijab:#2E7263", "#FFC93C") + person(900, 160, 0.42, SKIN[2], "kufi", "#9B6BFF", "#2a1d14")
          + person(300, 380, 0.5, SKIN[4], "hijab:#9B6BFF", "#2EB67D") + person(780, 380, 0.5, SKIN[1], "kufi", "#FFC93C", "#2a1d14")),
 "Ramaḍān": ("#FFC93C", "#fff", ["#fff", "#FF7A59"], sun(720, 150, 1.25, "#FF7A59")
          + "".join(f'<path d="M{x} 330 q 14 -20 0 -40 t 0 -40" fill="none" stroke="#fff" stroke-width="8" stroke-linecap="round"/>' for x in (520, 640, 760, 880))
          + f'<path d="M0 400 C 200 330 360 330 560 380 C 760 330 920 340 1080 380 L 1080 400 Z" fill="#e8a75a" {O}/>'
          + person(230, 372, 1.05, SKIN[1], "kufi", "#2E7263", "#2a1d14", "fold") + lantern(420, 0, 0.9)),
 "Shawwāl": ("#2E7263", "#FFE66D", ["#FFC93C", "#fff"], person(260, 372, 1.05, SKIN[0], "kufi", "#FFC93C", "#2a1d14", "wave") + person(820, 372, 1.05, SKIN[3], "hijab:#F49AC1", "#4D96FF", None, "wave")
          + cal(540, 230, "1", "#FF7A59", 0.95) + balloon(420, 90, "#FF7A59") + balloon(680, 70, "#9B6BFF") + moon(960, 70, 0.6)),
 "Dhū al-Qaʿdah": ("#9B6BFF", "#FFE66D", ["#FFE66D", "#fff"], f'<rect x="150" y="345" width="780" height="40" rx="12" fill="{RED}" {O}/><path d="M190 365 L 890 365" stroke="{GOLD}" stroke-width="6" stroke-dasharray="18 12"/>'
          + seated(330, 350, 1.0, SKIN[1], "kufi", "#FFC93C", "#2a1d14") + seated(750, 350, 1.0, SKIN[4], "hair:#2a1d14", "#2EB67D", "#2a1d14") + teaglass(540, 340, 0.8)),
 "Dhū al-Ḥijjah": ("#4D96FF", "#FFE66D", ["#FFE66D", "#fff"], kaaba(540, 330, 1.05)
          + "".join(person(x, 385, 0.55, sk, top, "#fff") for x, sk, top in ((110, SKIN[0], None), (220, SKIN[3], "hijab:#fff"), (330, SKIN[1], None), (760, SKIN[2], None), (870, SKIN[4], "hijab:#fff"), (980, SKIN[1], None)))),
 "end": ("#2E7263", None, ["#FFC93C", "#fff", "#FF7A59"], None),
},
 "wudu": {
 "cover": ("#4D96FF", None, ["#fff", "#cfe9ff", "#FFE66D"], None),
 "hands": ("#2EB67D", "#FFE66D", ["#fff", "#cfe9ff"], tap(540, 40, 230) + palm(470, 270, 20, fx=250, fy=420) + palm(615, 270, -20, fx=830, fy=420) + drops(((380, 200), (700, 190), (330, 280), (760, 290)), 0.9)),
 "mouth": ("#4D96FF", "#FFE66D", ["#fff", "#cfe9ff"], bighead(540, 190, 150, SKIN[1], "hair:#2a1d14", True, "#2a1d14") + ring(540, 270, 52) + drops(((700, 300), (740, 240), (360, 300)), 0.8)),
 "nose": ("#9B6BFF", "#FFE66D", ["#fff", "#cfe9ff"], bighead(540, 190, 150, SKIN[3], "hair:#3a2a1c") + ring(540, 205, 44) + drops(((690, 150), (380, 140), (720, 230)), 0.8)),
 "face": ("#2E7263", "#FFE66D", ["#fff", "#cfe9ff"], bighead(540, 190, 150, SKIN[2], "hair:#2a1d14", True, "#2a1d14") + ring(540, 200, 128) + drops(((330, 120), (760, 110), (310, 240), (780, 250), (540, 30)), 0.9)),
 "elbow": ("#FF7A59", "#FFE66D", ["#fff", "#FFE66D"], f'<rect x="40" y="200" width="360" height="104" rx="30" fill="#4D96FF" {O}/><rect x="360" y="216" width="520" height="72" rx="36" fill="{SKIN[1]}" {O}/>'
          + f'<ellipse cx="930" cy="252" rx="66" ry="40" fill="{SKIN[1]}" {O}/>' + tap(760, 30, 205) + ring(470, 252, 62) + drops(((640, 330), (560, 345), (840, 330)), 0.8)),
 "head": ("#F49AC1", "#FFE66D", ["#fff", "#4D96FF"], bighead(540, 210, 145, SKIN[0], "hair:#3a2a1c", True, "#3a2a1c") + ring(540, 100, 70)
          + palm(560, 70, -8, SKIN[0], "#2E7263", 860, 170) + f'<path d="M380 40 C 450 -10 630 -10 700 40" fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round" stroke-dasharray="4 18"/>'),
 "ears": ("#FFB23F", "#fff", ["#fff", "#FF7A59"], bighead(540, 190, 150, SKIN[4], "hair:#2a1d14") + ring(393, 196, 54) + ring(687, 196, 54) + drops(((300, 90), (790, 90)), 0.8)),
 "feet": ("#2EB67D", "#FFE66D", ["#fff", "#cfe9ff"], f'<rect x="430" y="-10" width="120" height="170" fill="#2E7263" {O}/><rect x="442" y="150" width="96" height="190" fill="{SKIN[2]}" {O}/>'
          + f'<path d="M442 290 C 425 330 420 372 462 372 L 735 372 C 770 372 775 338 745 326 C 690 306 610 300 538 286 Z" fill="{SKIN[2]}" {O}/><ellipse cx="748" cy="340" rx="12" ry="9" fill="#e8c4a6" {O}/>'
          + f'<g transform="rotate(-35 800 100)">{jug(800, 180, 0.9)}</g>' + f'<path d="M712 52 C 670 90 645 180 645 300" fill="none" stroke="{INK}" stroke-width="26" stroke-linecap="round"/><path d="M712 52 C 670 90 645 180 645 300" fill="none" stroke="#9fd8ff" stroke-width="14" stroke-linecap="round"/>'
          + ring(500, 320, 56) + drops(((380, 330), (800, 350), (720, 280)), 0.8)),
 "end": ("#2E7263", None, ["#cfe9ff", "#fff", "#FFE66D"], None),
},
 "sun-moon": {
 "cover": ("#FFC93C", None, ["#fff", "#FF7A59", "#4D96FF"], None),
 "the sun": ("#FF7A59", "#FFE66D", ["#FFE66D", "#fff"], hills() + sun(720, 160, 1.2, "#FFE66D") + lbadge(240, 150, True)),
 "the moon": ("#1D3557", "#FFE66D", ["#FFE66D", "#fff"], hills("#2E7263") + moon(720, 150, 1.4) + star(560, 80, 26, "#fff") + star(900, 260, 20, "#fff") + star(960, 70, 30) + lbadge(240, 150, False)),
 "peace": ("#2EB67D", "#FFE66D", ["#FFE66D", "#fff"], person(560, 372, 1.05, SKIN[1], "kufi", "#4D96FF", "#2a1d14", "wave") + person(860, 372, 1.05, SKIN[3], "kufi", "#FFC93C", "#3a2a1c", "wave")
          + lbadge(220, 150, True)),
 "the book": ("#4D96FF", "#FFE66D", ["#FFE66D", "#fff"], person(700, 372, 1.15, SKIN[2], "hijab:#9B6BFF", "#FF7A59", None, "book:#FFE66D") + bookc(920, 372, 0.9, "#2EB67D") + lbadge(240, 150, False)),
 "the Most Merciful": ("#9B6BFF", "#FFE66D", ["#FFE66D", "#fff"], f'<rect x="440" y="340" width="560" height="40" rx="12" fill="{RED}" {O}/>' + rehal(720, 300, 1.1) + lbadge(240, 150, True)),
 "praise": ("#2E7263", "#FFE66D", ["#FFC93C", "#fff"], f'<rect x="520" y="355" width="400" height="30" rx="8" fill="#FF7A59" {O}/>' + person(720, 372, 1.15, SKIN[0], "kufi", "#fff", "#e6e6e6", "self")
          + moon(960, 90, 0.6) + lbadge(240, 150, False)),
 "the light": ("#1D3557", "#FFE66D", ["#FFE66D", "#9B6BFF"], f'<circle cx="720" cy="190" r="170" fill="#FFE66D" opacity=".25"/><circle cx="720" cy="190" r="110" fill="#FFE66D" opacity=".3"/>' + lantern(720, 30, 1.5) + lbadge(240, 150, True)),
 "the House": ("#FFB23F", "#fff", ["#fff", "#FF7A59"], kaaba(720, 372, 1.1) + lbadge(240, 150, False)),
 "end": ("#2E7263", None, ["#FFC93C", "#fff", "#FF7A59"], None),
},
 "she": {
 "cover": ("#F49AC1", None, ["#fff", "#FFE66D", "#9B6BFF"], None),
 "teacher": ("#2EB67D", "#FFE66D", ["#FFE66D", "#fff"], board(540, 300) + person(200, 372, 1.0, SKIN[1], "kufi", "#4D96FF", "#2a1d14", "wave") + person(880, 372, 1.0, SKIN[3], "hijab:#FF7A59", "#9B6BFF", None, "wave")),
 "student": ("#4D96FF", "#FFE66D", ["#FFE66D", "#fff"], person(380, 372, 1.05, SKIN[2], "kufi", "#2EB67D", None, "book:#FFE66D") + person(700, 372, 1.05, SKIN[2], "hijab:#F49AC1", "#FFC93C", None, "book:#FF7A59")),
 "doctor": ("#9B6BFF", "#FFE66D", ["#FFE66D", "#fff"], person(420, 372, 1.15, SKIN[4], "hijab:#2E7263", "#fff", None, "fold")
          + f'<path d="M370 250 C 360 300 400 330 420 300" fill="none" stroke="{INK}" stroke-width="7"/>'
          + f'<g transform="translate(780,190)"><rect x="-110" y="-110" width="220" height="220" rx="30" fill="#fff" {O}/><path d="M-26 -70 H 26 V -26 H 70 V 26 H 26 V 70 H -26 V 26 H -70 V -26 H -26 Z" fill="{RED}" {O}/></g>'),
 "engineer": ("#FF7A59", "#FFE66D", ["#FFE66D", "#fff"], crane(660, 372) + person(380, 372, 1.15, SKIN[0], "hijab:#4D96FF", "#2E7263", None, "book:#9fd8ff")
          + f'<path d="M318 108 C 318 60 442 60 442 108 Z" fill="#FFC93C" {O}/><rect x="306" y="100" width="148" height="18" rx="8" fill="#FFC93C" {O}/>'),
 "big": ("#FFB23F", "#fff", ["#fff", "#FF7A59"], house(300, 372, 1.25) + car(760, 360, 1.25)),
 "new": ("#2E7263", "#FFE66D", ["#FFC93C", "#fff"], bookc(380, 372, 1.2, "#4D96FF") + bag(700, 372, 1.3) + star(530, 120, 34) + star(850, 90, 26, "#fff") + star(250, 90, 22, "#fff")),
 "watch out: mum": ("#F49AC1", "#FFE66D", ["#fff", "#FFE66D"], person(470, 372, 1.15, SKIN[1], "hijab:#2E7263", "#9B6BFF", None, "fold") + person(660, 372, 0.7, SKIN[1], "hair:#2a1d14", "#FFC93C", None, "wave")
          + heart(570, 80, 1.1)),
 "end": ("#9B6BFF", None, ["#FFE66D", "#fff", "#F49AC1"], None),
},
 "plurals": {
 "cover": ("#9B6BFF", None, ["#fff", "#FFE66D", "#FF7A59"], None),
 "books": ("#4D96FF", "#FFE66D", ["#FFE66D", "#fff"], bookc(190, 360, 1.3, "#FF7A59") + tag(190, 60, "1") + arrow(330, 470, 250) + bookc(640, 360, 1.15, "#2EB67D") + bookc(790, 360, 1.25, "#FFC93C") + bookc(940, 360, 1.1, "#9B6BFF") + tag(790, 60, "3+")),
 "houses": ("#2EB67D", "#FFE66D", ["#FFE66D", "#fff"], house(190, 372, 0.8) + tag(190, 60, "1") + arrow(330, 470, 250) + house(620, 372, 0.6) + house(800, 372, 0.7) + house(970, 372, 0.55) + tag(800, 60, "3+")),
 "pens": ("#FF7A59", "#FFE66D", ["#FFE66D", "#fff"], pic(692, 190, 210, 260) + arrow(360, 480, 210) + pic(692, 620, 230, 190) + pic(692, 790, 190, 190) + pic(692, 950, 230, 190)),
 "men": ("#9B6BFF", "#FFE66D", ["#FFE66D", "#fff"], person(190, 372, 1.0, SKIN[1], "kufi", "#4D96FF", "#2a1d14") + arrow(330, 450, 230)
          + "".join(person(x, 372, 0.9, sk, "kufi", bd, "#2a1d14") for x, sk, bd in ((600, SKIN[0], "#FFC93C"), (780, SKIN[2], "#2EB67D"), (960, SKIN[3], "#fff")))),
 "children": ("#F49AC1", "#FFE66D", ["#fff", "#FFE66D"], person(190, 372, 0.75, SKIN[1], "hair:#2a1d14", "#4D96FF", None, "wave") + arrow(320, 440, 240)
          + person(590, 372, 0.7, SKIN[0], "hair:#3a2a1c", "#FFC93C", None, "wave") + person(760, 372, 0.72, SKIN[2], "hijab:#9B6BFF", "#2EB67D") + person(930, 372, 0.68, SKIN[3], "hair:#2a1d14", "#FF7A59", None, "wave")),
 "masjids": ("#2E7263", "#FFE66D", ["#FFC93C", "#fff"], mosque(190, 372, 0.7) + arrow(370, 480, 250) + mosque(650, 372, 0.6) + mosque(880, 372, 0.6, "#FFE66D")),
 "teachers": ("#FFB23F", "#fff", ["#fff", "#FF7A59"], board(540, 300, 360, 200) + person(170, 372, 0.95, SKIN[1], "kufi", "#4D96FF", "#2a1d14", "wave") + person(330, 372, 0.9, SKIN[2], "kufi", "#2EB67D", "#2a1d14")
          + person(770, 372, 0.95, SKIN[3], "hijab:#FF7A59", "#9B6BFF", None, "wave") + person(930, 372, 0.9, SKIN[0], "hijab:#2E7263", "#FFC93C")),
 "end": ("#9B6BFF", None, ["#FFE66D", "#fff", "#FF7A59"], None),
},
 "opposites": {
 "cover": ("#FF7A59", None, ["#fff", "#FFE66D", "#4D96FF"], None),
 "big ↔ small": ("#4D96FF", "#FFE66D", ["#FFE66D", "#fff"], house(300, 372, 1.35) + house(800, 372, 0.6)),
 "new ↔ old": ("#2EB67D", "#FFE66D", ["#FFE66D", "#fff"], bookc(320, 372, 1.5, "#FF7A59") + star(160, 120, 34) + star(470, 90, 26, "#fff") + book2(770, 372, 1.4, "#8a5a2b", 8)
          + f'<path d="M640 120 l 30 20 M 700 90 l 10 30 M 880 110 l -26 26" stroke="#d9cbae" stroke-width="8" stroke-linecap="round"/>'),
 "near ↔ far": ("#9B6BFF", "#FFE66D", ["#FFE66D", "#fff"], f'<path d="M0 390 C 300 380 600 300 1080 260 L 1080 390 Z" fill="#7bd389" {O}/>' + mosque(300, 380, 0.95) + mosque(900, 270, 0.32) + person(560, 380, 0.8, SKIN[1], "kufi", "#FFC93C", "#2a1d14", "wave")),
 "tall ↔ short": ("#FFB23F", "#fff", ["#fff", "#FF7A59"], person(400, 380, 1.3, SKIN[2], "kufi", "#4D96FF", "#2a1d14", "wave") + person(680, 380, 0.85, SKIN[2], "hair:#2a1d14", "#2EB67D")),
 "easy ↔ hard": ("#F49AC1", "#FFE66D", ["#fff", "#FFE66D"], board(300, 300, 340, 200).replace("أ ب ت", "1 + 1") + board(780, 300, 340, 200).replace("أ ب ت", "∑ ∫ √")),
 "open ↔ closed": ("#2E7263", "#FFE66D", ["#FFC93C", "#fff"], house(300, 372, 1.1) + f'<g transform="translate(780,372)"><rect x="-120" y="-300" width="240" height="300" rx="12" fill="#8a5a2b" {O}/><circle cx="80" cy="-150" r="14" fill="{GOLD}" {O}/><rect x="-90" y="-270" width="180" height="100" rx="8" fill="none" stroke="{INK}" stroke-width="6" opacity=".4"/></g>'),
 "end": ("#FF7A59", None, ["#FFC93C", "#fff", "#4D96FF"], None),
},
 "house": {
 "cover": ("#2EB67D", None, ["#fff", "#FFE66D", "#FF7A59"], None),
 "house": ("#FF7A59", "#FFE66D", ["#FFE66D", "#fff"], house(540, 372, 1.3) + person(840, 372, 0.9, SKIN[1], "hijab:#2E7263", "#9B6BFF", None, "wave") + person(240, 372, 0.9, SKIN[1], "kufi", "#4D96FF", "#2a1d14", "wave")),
 "door": ("#4D96FF", "#FFE66D", ["#FFE66D", "#fff"], pic(7, 540, 200, 360)),
 "room": ("#9B6BFF", "#FFE66D", ["#FFE66D", "#fff"], pic(669, 360, 200, 330) + pic(741, 740, 200, 330)),
 "kitchen": ("#FFB23F", "#fff", ["#fff", "#FF7A59"], pic(672, 540, 200, 360)),
 "window": ("#2E7263", "#FFE66D", ["#FFC93C", "#fff"], pic(741, 540, 200, 360)),
 "bed": ("#F49AC1", "#FFE66D", ["#fff", "#FFE66D"], pic(95, 540, 200, 360) + moon(880, 90, 0.8)),
 "end": ("#2EB67D", None, ["#FFE66D", "#fff", "#FF7A59"], None),
},
 "weather": {
 "cover": ("#4D96FF", None, ["#fff", "#FFE66D", "#cfe9ff"], None),
 "sun": ("#FFB23F", "#fff", ["#fff", "#FF7A59"], sun(540, 200, 1.6, "#FFE66D")),
 "rain": ("#4D96FF", "#FFE66D", ["#fff", "#cfe9ff"], pic(349, 540, 200, 360)),
 "clouds": ("#9fd8ff", "#FFE66D", ["#fff", "#4D96FF"], cloud(330, 150, 1.4) + cloud(760, 230, 1.1) + cloud(560, 330, 0.7, "#eaf2f7") + sun(900, 80, 0.5, "#FFE66D")),
 "wind": ("#2EB67D", "#FFE66D", ["#fff", "#FFE66D"], pic(425, 540, 200, 360)),
 "snow": ("#1D3557", "#FFE66D", ["#fff", "#cfe9ff"], pic(353, 380, 200, 300) + pic(371, 760, 200, 300)),
 "cold ↔ hot": ("#9B6BFF", "#FFE66D", ["#FFE66D", "#fff"], pic(350, 340, 200, 320) + pic(360, 740, 200, 320)),
 "end": ("#4D96FF", None, ["#FFE66D", "#fff", "#cfe9ff"], None),
},
 "english": {
 "cover": ("#FFC93C", None, ["#fff", "#FF7A59", "#9B6BFF"], None),
 "coffee": ("#FF7A59", "#FFE66D", ["#FFE66D", "#fff"], dallah(400, 360, 1.3) + finjan(620, 360, 1.3) + finjan(760, 360, 1.3)),
 "sugar": ("#F49AC1", "#FFE66D", ["#fff", "#FFE66D"], pic(331, 540, 200, 360)),
 "cotton": ("#2EB67D", "#FFE66D", ["#FFE66D", "#fff"], cotton(380, 380, 1.3) + cotton(720, 380, 1.1)),
 "giraffe": ("#FFB23F", "#fff", ["#fff", "#FF7A59"], pic(686, 540, 200, 360)),
 "lemon": ("#4D96FF", "#FFE66D", ["#FFE66D", "#fff"], pic(733, 540, 200, 360)),
 "syrup": ("#9B6BFF", "#FFE66D", ["#FFE66D", "#fff"], pic(685, 540, 200, 360)),
 "jar": ("#2E7263", "#FFE66D", ["#FFC93C", "#fff"], pic(189, 540, 200, 360)),
 "end": ("#FFC93C", None, ["#fff", "#FF7A59", "#9B6BFF"], None),
},
 "replies": {
 "cover": ("#2E7263", None, ["#FFC93C", "#fff", "#FF7A59"], None),
 "peace": ("#4D96FF", "#FFE66D", ["#FFE66D", "#fff"], person(380, 372, 1.15, SKIN[1], "kufi", "#2EB67D", "#2a1d14", "wave") + person(700, 372, 1.15, SKIN[3], "kufi", "#FFC93C", "#3a2a1c", "wave")),
 "good morning": ("#FFB23F", "#fff", ["#fff", "#FF7A59"], sun(540, 120, 0.9, "#FFE66D") + person(300, 372, 1.0, SKIN[0], "hijab:#9B6BFF", "#2EB67D", None, "wave") + person(780, 372, 1.0, SKIN[2], "hijab:#2E7263", "#FF7A59", None, "wave")),
 "how are you?": ("#9B6BFF", "#FFE66D", ["#FFE66D", "#fff"], person(360, 372, 1.1, SKIN[1], "kufi", "#4D96FF", "#2a1d14", "wave") + person(720, 372, 1.1, SKIN[4], "kufi", "#fff", "#e6e6e6", "self")),
 "thank you": ("#2EB67D", "#FFE66D", ["#FFE66D", "#fff"], person(330, 372, 1.05, SKIN[3], "hijab:#FF7A59", "#4D96FF", None, "self") + teaglass(560, 330, 1.0) + person(780, 372, 1.05, SKIN[0], "hair:#3a2a1c", "#FFC93C", None, "wave")),
 "may Allah reward you": ("#FF7A59", "#FFE66D", ["#FFE66D", "#fff"], person(330, 372, 1.05, SKIN[2], "kufi", "#2E7263", "#2a1d14", "self") + bag(560, 360, 0.9, "#FFC93C") + person(790, 372, 1.05, SKIN[1], "kufi", "#9B6BFF", "#2a1d14", "fold")),
 "after a sneeze": ("#F49AC1", "#FFE66D", ["#fff", "#FFE66D"], person(360, 372, 1.1, SKIN[0], "kufi", "#4D96FF", "#2a1d14", "self") + tag(360, 60, "Achoo!", "#fff", 50) + person(740, 372, 1.1, SKIN[3], "hair:#2a1d14", "#2EB67D", None, "wave")),
 "goodbye": ("#4D96FF", "#FFE66D", ["#FFE66D", "#fff"], person(300, 372, 1.05, SKIN[1], "hijab:#2E7263", "#FFC93C", None, "wave") + car(760, 360, 1.2)),
 "end": ("#2E7263", None, ["#FFC93C", "#fff", "#FF7A59"], None),
},
 "animals": {
 "cover": ("#2EB67D", None, ["#fff", "#FFE66D", "#FF7A59"], None),
 "the cow": ("#FFB23F", "#fff", ["#fff", "#FF7A59"], pic(719, 540, 200, 360)),
 "livestock": ("#2EB67D", "#FFE66D", ["#FFE66D", "#fff"], pic(742, 250, 200, 280) + pic(540, 540, 210, 280) + pic(650, 830, 200, 280)),
 "the bee": ("#4D96FF", "#FFE66D", ["#FFE66D", "#fff"], flower(300, 380, "#FF7A59", 1.3) + flower(820, 380, "#F49AC1", 1.1) + bee(560, 170, 1.4) + bee(860, 90, 0.7)),
 "the ant": ("#FFC93C", "#fff", ["#fff", "#FF7A59"], hills("#7bd389") + "".join(ant(x, 330 - (i % 2) * 10, 0.9) for i, x in enumerate((200, 420, 640, 860)))),
 "the spider": ("#1D3557", "#FFE66D", ["#FFE66D", "#fff"], pic(705, 540, 200, 360) + moon(900, 90, 0.7)),
 "the elephant": ("#9B6BFF", "#FFE66D", ["#FFE66D", "#fff"], pic(633, 540, 200, 360)),
 "end": ("#2EB67D", None, ["#FFE66D", "#fff", "#FF7A59"], None),
},
 "phrases": {
 "cover": ("#FF7A59", None, ["#fff", "#FFE66D", "#9B6BFF"], None),
 "bismillāh": ("#2EB67D", "#FFE66D", ["#FFE66D", "#fff"], person(300, 372, 1.05, SKIN[1], "kufi", "#4D96FF", "#2a1d14", "fold") + plate(680, 330, 1.4, "dates") + teaglass(900, 330, 0.9)),
 "in shāʾ Allāh": ("#4D96FF", "#FFE66D", ["#FFE66D", "#fff"], cal(540, 230, "?", "#FF7A59", 1.25) + tag(540, 360, "tomorrow", "#FFE66D", 44)),
 "mā shāʾ Allāh": ("#9B6BFF", "#FFE66D", ["#FFE66D", "#fff"], hills() + "".join(flower(x, 360, c, k) for x, c, k in ((200, "#FF7A59", 1.2), (380, "#FFE66D", 1.0), (560, "#F49AC1", 1.3), (740, "#fff", 1.0), (900, "#FF7A59", 1.15))) + sun(540, 90, 0.5, "#FFE66D")),
 "subḥān Allāh": ("#1D3557", "#FFE66D", ["#FFE66D", "#fff"], hills("#2E7263") + moon(760, 140, 1.4) + star(300, 90, 36) + star(480, 200, 22, "#fff") + star(160, 230, 18, "#fff") + star(940, 280, 24, "#fff") + star(600, 60, 18, "#fff")),
 "al-ḥamdu lillāh": ("#FFB23F", "#fff", ["#fff", "#FF7A59"], person(420, 372, 1.15, SKIN[3], "hijab:#2E7263", "#9B6BFF", None, "self") + heart(700, 170, 1.6)),
 "Allāhu akbar": ("#2E7263", "#FFE66D", ["#FFC93C", "#fff"], mosque(540, 380, 1.0)),
 "end": ("#FF7A59", None, ["#FFC93C", "#fff", "#9B6BFF"], None),
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

def tall(body, seed):
    """The 4:5 slide inside a 9:16 TikTok photo (owner, 8 Nov 2026: uploads from the phone): the same slide in the middle, the slide's colour
    above and below with a few more doodles, so TikTok's own buttons and caption sit over the plain bands, not the words."""
    bg = re.search(r'<body style="background:([^"]+)">', body).group(1)
    dc = re.findall(r'(?:fill|stroke)="(#[0-9A-Fa-f]{6})" (?:opacity|stroke-width)', body)[:3] or ["#fff"]
    r = random.Random(seed); bands = ""
    for y0, y1 in ((20, 265), (1655, 1900)):
        for _ in range(7):
            x, y, c = r.uniform(40, 1040), r.uniform(y0, y1), r.choice(dc)
            bands += (f'<path d="M{x} {y - 22} Q {x + 4} {y - 4} {x + 22} {y} Q {x + 4} {y + 4} {x} {y + 22} Q {x - 4} {y + 4} {x - 22} {y} Q {x - 4} {y - 4} {x} {y - 22} Z" fill="{c}" opacity=".85"/>'
                      if r.random() < 0.5 else f'<circle cx="{x}" cy="{y}" r="{r.uniform(8, 16):.0f}" fill="none" stroke="{c}" stroke-width="6" opacity=".7"/>')
    inner = body[body.index(">") + 1:body.rindex("</body>")]
    return (f'<body style="background:{bg};height:1920px"><svg style="position:absolute;inset:0" viewBox="0 0 1080 1920">{bands}</svg>'
            f'<div style="position:absolute;left:0;top:285px;width:1080px;height:1350px;overflow:hidden">{inner}</div></body>')

if __name__ == "__main__":
    TALL = "--tiktok" in sys.argv; ids = [a for a in sys.argv[1:] if not a.startswith("--")]
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=S.CHROME if os.path.exists(S.CHROME) else None)
        pg = b.new_page(viewport={"width": 1080, "height": 1920 if TALL else 1350})
        for sid in ART:
            if ids and sid not in ids: continue
            out = os.path.join(S.HERE, "stills", sid + ("-tiktok" if TALL else "-pop")); os.makedirs(out, exist_ok=True)
            for k, body in slides(sid).items():
                if TALL: body = tall(body, int(k) * 7)
                tmp = os.path.join(out, "_s.html"); open(tmp, "w").write(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>{body}</html>')
                pg.goto("file://" + tmp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
                if TALL: pg.screenshot(path=os.path.join(out, f"{sid}-{int(k):02d}.jpg"), type="jpeg", quality=92)
                else: pg.screenshot(path=os.path.join(out, f"{sid}-{k}.png"))
            os.remove(os.path.join(out, "_s.html")); print(sid, "->", out)
        b.close()
