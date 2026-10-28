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
