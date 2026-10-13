#!/usr/bin/env python3
"""Two high-energy TikToks (#237): more motion, more play. The reading voice only; hook on screen from the first frame.

  x1-machine   The Arabic word machine: a slot machine. The reels land on a root (د ر س), a pattern reel picks what to make
               ('he did it', 'a place for it', 'someone who does it') and the word drops out with a jackpot:
               دَرَسَ (toolkit-data.js VERBS), مَدْرَسَة (vocab 149), مُدَرِّس (30). Then the root swaps to ك ت ب with
               'a place for it' kept: مَكْتَبَة (279).
  x2-dots      Dots are power-ups: an arcade game. One shape, ٮ; dots fall in (one below ب, two above ت, three above ث) with a
               shake, sparks and a score. Words from alphabet-data.js: بَيْت, تَمْر, ثَلاثَة. Boss level: a shell game, find ت.

  python3 brag-quiz/build_wild.py [id ...]     then render each, then  --level
"""
import base64, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import build_teach as T
from build_teach import Comp, e, word

GOLD = "#f2c14e"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"     # the pre-installed Chromium, when the pinned Playwright wants another build
CONF = ["#b4322a", "#2e7263", "#f2c14e", "#17262b", "#e9dcc0"]

def burst(c, bid, cx, cy, at, n=26, spread=460, seed=1, colors=CONF, size=(16, 26)):
    """confetti from (cx, cy): n pieces fly out, spin and fall, all from a fixed seed so every render is the same"""
    r = random.Random(seed); html = []
    for i in range(n):
        col = colors[i % len(colors)]; w, h = size
        html.append(f'<i class="cf" id="{bid}{i}" style="left:{cx}px; top:{cy}px; width:{w}px; height:{h}px; background:{col}"></i>')
        dx, dy = r.uniform(-spread, spread), r.uniform(-spread * 0.8, spread * 0.25)
        c.t(f'tl.fromTo("#{bid}{i}", {{opacity:1, x:0, y:0, rotation:0, scale:0.4}}, {{x:{dx:.0f}, y:{dy:.0f}, rotation:{r.uniform(-540, 540):.0f}, scale:1, '
            f'duration:0.55, ease:"power3.out", immediateRender:false}}, {at:.2f});')
        c.t(f'tl.to("#{bid}{i}", {{y:"+=320", opacity:0, duration:0.75, ease:"power1.in"}}, {at + 0.56:.2f});')
    return "".join(html)

def shake(c, sel, at, amp=16, n=6):
    frames = ", ".join(f'{{x:{(amp if k % 2 == 0 else -amp) * (n - k) / n:.0f}, y:{(amp / 2 if k % 3 == 0 else -amp / 2) * (n - k) / n:.0f}, duration:0.04}}'
                       for k in range(n))
    c.t(f'tl.to("{sel}", {{keyframes:[{frames}, {{x:0, y:0, duration:0.04}}]}}, {at:.2f});')

# ---------------------------------------------------------------- x1: the word machine
M_CSS = """
.hook { position:absolute; top:258px; left:50px; right:50px; text-align:center; font-size:64px; font-weight:700; line-height:1.1; letter-spacing:-.02em; }
.hook b { color:var(--rubric); }
.cab { position:absolute; top:420px; left:60px; right:150px; height:560px; background:var(--ink); border-radius:56px;
  box-shadow:0 26px 50px -24px rgba(23,38,43,.7), inset 0 0 0 8px #2b3e43; }
.bulbs { position:absolute; top:26px; left:60px; right:60px; display:flex; justify-content:space-between; }
.bulbs i { width:22px; height:22px; border-radius:50%; background:#f2c14e; box-shadow:0 0 18px 4px rgba(242,193,78,.6); }
.plate { position:absolute; top:66px; left:0; right:0; text-align:center; font-family:var(--ut); font-size:32px; letter-spacing:.3em; color:#f2c14e; }
.reels { position:absolute; top:122px; left:0; right:0; display:flex; flex-direction:row-reverse; justify-content:center; gap:26px; }
.win { position:relative; width:220px; height:250px; background:var(--paper); border-radius:26px; overflow:hidden; box-shadow:inset 0 10px 18px -8px rgba(0,0,0,.45); }
.strip { position:absolute; top:0; left:0; right:0; }
.strip div { height:250px; display:grid; place-items:center; font-family:var(--ar); font-weight:700; font-size:160px; line-height:1; color:var(--ink); }
.strip div.q { font-family:var(--la); font-size:120px; color:rgba(23,38,43,.25); }
.strip div.hit { color:var(--rubric); }
.fl { position:absolute; inset:0; border-radius:26px; background:#f2c14e; opacity:0; }
.root { position:absolute; top:400px; left:0; right:0; text-align:center; font-size:40px; font-weight:700; color:var(--paper); }
.root span { position:absolute; left:0; right:0; opacity:0; }
.root b { color:#f2c14e; }
.lever { position:absolute; top:520px; left:948px; width:90px; height:300px; }
.lever .base { position:absolute; bottom:0; left:20px; width:50px; height:70px; border-radius:16px; background:var(--ink); }
.lever .arm { position:absolute; bottom:40px; left:37px; width:16px; height:230px; border-radius:8px; background:#8a9799; transform-origin:50% 100%; }
.lever .arm i { position:absolute; top:-34px; left:-26px; width:68px; height:68px; border-radius:50%; background:var(--rubric);
  box-shadow:inset -8px -10px 0 rgba(0,0,0,.18); }
.ptag { position:absolute; top:1010px; left:0; right:0; text-align:center; font-family:var(--ut); font-size:28px; letter-spacing:.2em; color:var(--ink-soft); }
.pwin { position:absolute; top:1052px; left:150px; right:150px; height:120px; border-radius:30px; background:var(--card); overflow:hidden;
  border:5px solid #d9a93a; box-shadow:0 12px 26px -16px rgba(23,38,43,.45); }
.pstrip { position:absolute; top:0; left:0; right:0; }
.pstrip div { height:120px; display:grid; place-items:center; font-size:52px; font-weight:700; color:var(--verdigris); }
.rays { position:absolute; top:1000px; left:90px; width:900px; height:900px; border-radius:50%; opacity:0;
  background:repeating-conic-gradient(rgba(242,193,78,.55) 0 9deg, rgba(242,193,78,0) 9deg 18deg);
  -webkit-mask:radial-gradient(circle, #000 0%, #000 30%, transparent 68%); mask:radial-gradient(circle, #000 0%, #000 30%, transparent 68%); }
.tray { position:absolute; top:1230px; left:120px; right:120px; height:390px; border-radius:44px; background:var(--card); border:5px solid var(--ink);
  display:flex; flex-direction:column; align-items:center; justify-content:center; opacity:0; box-shadow:0 26px 40px -22px rgba(23,38,43,.55); }
.tray .ar { font-family:var(--ar); font-weight:700; font-size:150px; line-height:1.4; color:var(--ink); }
.tray .ar .pr { color:var(--rubric); }
.tray .mn { font-size:50px; font-weight:700; margin-top:-6px; }
.tray .mn em { font-style:normal; color:var(--ink-soft); font-weight:500; }
.cf { position:absolute; border-radius:4px; opacity:0; }
.shelf { position:absolute; top:1690px; left:60px; right:60px; display:flex; flex-direction:row-reverse; justify-content:space-between; }
.slot { width:224px; height:150px; border-radius:28px; border:4px dashed rgba(23,38,43,.2); display:grid; place-items:center; position:relative; }
.slot b { font-family:var(--ar); font-weight:700; font-size:64px; line-height:1.4; color:var(--ink); opacity:0; }
.slot b .pr { color:var(--rubric); }
.swap { position:absolute; top:1300px; left:60px; right:60px; text-align:center; font-size:76px; font-weight:700; letter-spacing:-.02em; color:var(--rubric); opacity:0; }
.fin { position:absolute; top:1250px; left:70px; right:70px; text-align:center; font-size:72px; font-weight:700; line-height:1.12; letter-spacing:-.02em; opacity:0; }
.fin b { color:var(--rubric); }
.ask { position:absolute; top:1500px; left:70px; right:70px; text-align:center; font-size:48px; font-weight:700; color:var(--ink-soft); opacity:0; }
"""

FILL = "بتثجحخدذرزسشصضطظعغفقكلمنهوي"
ROUNDS = [("دَرَسَ", [("دَ", "r"), ("رَ", "r"), ("سَ", "r")], "he studied", "darasa", "he did it"),
          ("مَدْرَسَة", [("مَ", ""), ("دْ", "r"), ("رَ", "r"), ("سَ", "r"), ("ة", "")], "school", "madrasa", "a place for it"),
          ("مُدَرِّس", [("مُ", ""), ("دَ", "r"), ("رِّ", "r"), ("س", "r")], "teacher", "mudarris", "someone who does it"),
          ("مَكْتَبَة", [("مَ", ""), ("كْ", "r"), ("تَ", "r"), ("بَ", "r"), ("ة", "")], "library", "maktaba", "a place for it")]
PATS = ["he did it", "a place for it", "someone who does it"]
ROOTS = ["درس", "كتب"]
RH, PH = 250, 120                                                # one reel cell, one pattern cell

def x1():
    c = Comp("x1-machine", "THE ARABIC WORD MACHINE", bed=False); c.css = M_CSS
    r = random.Random(7)
    # three reels, each: ?, 14 random letters, the first root's letter, 14 more, the second root's letter
    strips, land = [], []
    for k in range(3):
        cells = ['<div class="q" data-layout-allow-occlusion>?</div>']; idx = []
        for root in ROOTS:
            cells += [f"<div data-layout-allow-occlusion>{r.choice(FILL)}</div>" for _ in range(14)]
            idx.append(len(cells)); cells.append(f'<div class="hit" data-layout-allow-occlusion>{root[k]}</div>')
        strips.append(f'<div class="win"><div class="strip" id="st{k}" data-layout-allow-overflow data-layout-allow-occlusion>{"".join(cells)}</div><i class="fl" id="fl{k}"></i></div>'); land.append(idx)
    # the pattern reel: …, then a run of patterns before each landing
    pcells, plands = ["<div data-layout-allow-occlusion>…</div>"], []
    for _, _, _, _, pat in ROUNDS:
        pcells += [f"<div data-layout-allow-occlusion>{PATS[(len(pcells) + j) % 3]}</div>" for j in range(7)]
        plands.append(len(pcells)); pcells.append(f"<div data-layout-allow-occlusion>{pat}</div>")
    total_guess = 22.0
    bulbs = "".join(f'<i class="{"ba" if i % 2 else "bb"}"></i>' for i in range(13))
    c.t(f'tl.fromTo(".bulbs .ba", {{opacity:1}}, {{opacity:0.2, duration:0.3, repeat:{int(total_guess / 0.3)}, yoyo:true, ease:"none"}}, 0);')
    c.t(f'tl.fromTo(".bulbs .bb", {{opacity:0.2}}, {{opacity:1, duration:0.3, repeat:{int(total_guess / 0.3)}, yoyo:true, ease:"none"}}, 0);')
    c.t(f'tl.fromTo(".rays", {{rotation:0}}, {{rotation:240, duration:{total_guess}, ease:"none"}}, 0);')

    def pull(at):
        c.t(f'tl.to(".lever .arm", {{rotation:28, scaleY:0.55, duration:0.22, ease:"power2.in"}}, {at:.2f});')
        c.t(f'tl.to(".lever .arm", {{rotation:0, scaleY:1, duration:0.5, ease:"elastic.out(1, 0.45)"}}, {at + 0.23:.2f});')

    def spin(at, which):
        pull(at)
        for k in range(3):
            d = 1.1 + 0.3 * k; y = -land[k][which] * RH; end = at + 0.25 + d
            c.t(f'tl.to("#st{k}", {{y:{y}, duration:{d:.2f}, ease:"back.out(0.6)"}}, {at + 0.25:.2f});')
            c.t(f'tl.fromTo("#st{k}", {{filter:"blur(9px)"}}, {{filter:"blur(0px)", duration:{d:.2f}, ease:"expo.in", immediateRender:false}}, {at + 0.25:.2f});')
            c.t(f'tl.fromTo("#fl{k}", {{opacity:0.75}}, {{opacity:0, duration:0.4, immediateRender:false}}, {end:.2f});')
            shake(c, ".cab", end, 8, 4)
        return at + 0.25 + 1.7

    t = spin(0.5, 0)
    c.inn("#rt0", t - 0.1, 14, 0.3)
    shelf_html, trays, conf = [], [], []
    for i, (ar, pieces, en, tr, pat) in enumerate(ROUNDS):
        if i == 3:                                               # the twist: swap the root, keep the pattern
            c.t(f'tl.fromTo(".swap", {{opacity:0, scale:1.6}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(2)"}}, {t:.2f});')
            c.t(f'tl.to(".swap", {{opacity:0, duration:0.25}}, {t + 1.55:.2f});')
            c.t(f'tl.to("#rt0", {{opacity:0, duration:0.2}}, {t + 0.3:.2f});')
            t = spin(t + 0.2, 1); c.inn("#rt1", t - 0.1, 14, 0.3); t += 0.1
        # the pattern reel
        c.t(f'tl.to(".pstrip", {{y:{-plands[i] * PH}, duration:0.9, ease:"back.out(0.8)"}}, {t:.2f});')
        c.t(f'tl.fromTo(".pstrip", {{filter:"blur(6px)"}}, {{filter:"blur(0px)", duration:0.9, ease:"expo.in", immediateRender:false}}, {t:.2f});')
        c.t(f'tl.fromTo(".pwin", {{scale:1}}, {{scale:1.06, duration:0.12, yoyo:true, repeat:1, immediateRender:false}}, {t + 0.9:.2f});')
        t += 1.05
        # jackpot: the word drops into the tray
        big = i == 3
        c.t(f'tl.fromTo("#tr{i}", {{opacity:0, scale:0.3, y:-160}}, {{opacity:1, scale:1, y:0, duration:0.45, ease:"back.out(2.2)"}}, {t:.2f});')
        c.t(f'tl.fromTo(".rays", {{opacity:0, scale:0.5}}, {{opacity:{1 if big else 0.8}, scale:{1.15 if big else 1}, duration:0.4, ease:"power2.out", immediateRender:false}}, {t:.2f});')
        conf.append(burst(c, f"c{i}", 540, 1420, t + 0.1, n=40 if big else 24, spread=520 if big else 420, seed=i + 3))
        shake(c, "#tr" + str(i), t + 0.45, 10, 4)
        d = c.say(ar, t + 0.2); t += max(d, 0.9) + (1.6 if big else 1.0)
        # …then into the shelf
        c.t(f'tl.to(".rays", {{opacity:0, duration:0.3}}, {t - 0.2:.2f});')
        c.t(f'tl.to("#tr{i}", {{opacity:0, scale:0.35, y:330, duration:0.4, ease:"power2.in"}}, {t:.2f});')
        c.t(f'tl.fromTo("#sh{i}", {{opacity:0, scale:1.8}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(2)"}}, {t + 0.32:.2f});')
        c.t(f'tl.to("#sl{i}", {{borderColor:"rgba(46,114,99,.65)", borderStyle:"solid", duration:0.2}}, {t + 0.32:.2f});')
        t += 0.55
        trays.append(f'<div class="tray" id="tr{i}" data-layout-allow-overlap>{word(pieces, "ar")}<div class="mn">{e(en)} <em>· {e(tr)}</em></div></div>')
        shelf_html.append(f'<div class="slot" id="sl{i}"><b id="sh{i}" lang="ar" dir="rtl">' + "".join(
            f'<span class="p{k}">{e(x)}</span>' if k else e(x) for x, k in pieces) + '</b></div>')
    c.t(f'tl.fromTo(".fin", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.45, ease:"back.out(1.8)"}}, {t:.2f});')
    c.t(f'tl.fromTo(".ask", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.4, ease:"power3.out"}}, {t + 1.2:.2f});')
    conf.append(burst(c, "cz", 540, 1330, t + 0.1, n=30, spread=480, seed=99))
    t += 3.6
    body = ('      <div class="hook">Arabic has a <b>word machine</b> 🎰</div>'
            f'<div class="cab"><div class="bulbs">{bulbs}</div><div class="plate">3 LETTERS IN · WORDS OUT</div>'
            f'<div class="reels">{"".join(strips)}</div>'
            '<div class="root"><span id="rt0" data-layout-allow-overlap>root <b>د ر س</b> · studying</span>'
            '<span id="rt1" data-layout-allow-overlap>root <b>ك ت ب</b> · writing</span></div></div>'
            '<div class="lever"><div class="base"></div><div class="arm"><i></i></div></div>'
            '<div class="ptag">PATTERN</div>'
            f'<div class="pwin"><div class="pstrip" data-layout-allow-overflow data-layout-allow-occlusion>{"".join(pcells)}</div></div>'
            '<div class="rays" data-layout-allow-overlap></div>' + "".join(trays) +
            '<div class="swap" data-layout-allow-overlap>Now swap the root 🔄</div>'
            f'<div class="shelf">{"".join(shelf_html)}</div>'
            '<div class="fin" data-layout-allow-overlap>Same pattern, new root: <b>a new word</b> 🤯</div>'
            '<div class="ask" data-layout-allow-overlap>Which root should I spin next? 👇</div>' + "".join(conf))
    c.write(body, round(t, 2))

# ---------------------------------------------------------------- x2: dots are power-ups
D_CSS = """
#root { background:#0f1f1e; } #glow { opacity:.35; }
.grid { position:absolute; inset:0; background-image:linear-gradient(rgba(242,193,78,.06) 2px, transparent 2px), linear-gradient(90deg, rgba(242,193,78,.06) 2px, transparent 2px);
  background-size:90px 90px; }
#brand b { color:var(--paper); } #brand .tile { background:var(--paper); } #brand .tile span { color:var(--ink); }
#kicker { color:#9fb8b2; }
.hook { position:absolute; top:262px; left:30px; right:30px; text-align:center; font-size:58px; font-weight:700; line-height:1.1; letter-spacing:-.02em; color:var(--paper); }
.hook b { color:#f2c14e; }
.hud { position:absolute; top:470px; left:90px; right:90px; height:70px; font-family:var(--ut); font-size:40px; color:var(--paper); }
.lvl { position:absolute; left:0; top:0; height:70px; width:420px; }
.lvl span { position:absolute; left:0; top:12px; white-space:nowrap; opacity:0; }
.lvl span.on { opacity:1; }
.lvl b { color:#f2c14e; }
.sc { position:absolute; right:0; top:0; height:70px; display:flex; gap:16px; align-items:center; }
.sc em { font-style:normal; color:#9fb8b2; }
.scw { position:relative; height:56px; width:120px; overflow:hidden; }
.scc { position:absolute; left:0; top:0; }
.scc div { height:56px; line-height:56px; color:#f2c14e; font-weight:500; }
.xp { position:absolute; top:560px; left:90px; right:90px; height:22px; border-radius:11px; background:rgba(241,236,224,.12); overflow:hidden; }
.xp i { position:absolute; inset:0; border-radius:11px; background:linear-gradient(90deg, #2e7263, #f2c14e); transform-origin:0 50%; transform:scaleX(0); }
.stage { position:absolute; top:640px; left:0; right:0; height:640px; }
.gbox { position:absolute; left:90px; top:20px; width:900px; height:600px; }
.gbox img { position:absolute; inset:0; width:900px; height:600px; }
.dt { position:absolute; background:#f2c14e; border-radius:28%; box-shadow:0 0 24px 6px rgba(242,193,78,.55); }
.sp { position:absolute; width:14px; height:14px; border-radius:3px; background:#f2c14e; opacity:0; }
.flash { position:absolute; inset:0; background:#fff7dc; opacity:0; pointer-events:none; }
.pts { position:absolute; top:690px; right:110px; font-family:var(--ut); font-size:58px; font-weight:500; color:#f2c14e; opacity:0; }
.ban { position:absolute; top:860px; left:0; right:0; height:170px; background:var(--rubric); transform:skewY(-4deg); display:flex; flex-direction:column;
  align-items:center; justify-content:center; box-shadow:0 18px 40px -16px rgba(0,0,0,.6); }
.ban b { font-family:var(--ut); font-size:66px; font-weight:500; letter-spacing:.06em; color:var(--paper); }
.ban span { font-size:44px; font-weight:700; color:#ffe2a6; }
.wc { position:absolute; top:1320px; left:150px; right:150px; height:330px; border-radius:44px; background:var(--paper); display:flex; flex-direction:column;
  align-items:center; justify-content:center; opacity:0; box-shadow:0 0 0 6px #f2c14e, 0 30px 50px -20px rgba(0,0,0,.7); }
.wc .snd { font-family:var(--ut); font-size:36px; color:var(--ink-soft); }
.wc .ar { font-family:var(--ar); font-weight:700; font-size:130px; line-height:1.45; color:var(--ink); }
.wc .ar i { font-style:normal; color:var(--rubric); }
.wc .mn { font-size:46px; font-weight:700; margin-top:-10px; color:var(--ink); }
.wc .mn em { font-style:normal; color:var(--ink-soft); font-weight:500; }
.cards { position:absolute; top:770px; left:0; right:0; height:340px; }
.card { position:absolute; left:425px; top:0; width:230px; height:320px; }
.card div { position:absolute; inset:0; border-radius:34px; display:grid; place-items:center; }
.card .fc { background:var(--paper); font-family:var(--ar); font-weight:700; font-size:180px; line-height:1; color:var(--ink); }
.card .fc span { margin-top:-40px; }
.card .bc { background:var(--rubric); opacity:0; font-size:150px; font-weight:700; color:#ffe2a6; box-shadow:inset 0 0 0 10px rgba(255,226,166,.35); }
.where { position:absolute; top:1180px; left:60px; right:60px; text-align:center; font-size:80px; font-weight:700; color:var(--paper); opacity:0; }
.where .ar { font-family:var(--ar); color:#f2c14e; }
.cd { position:absolute; top:1330px; left:0; right:0; height:200px; }
.cd span { position:absolute; left:0; right:0; text-align:center; font-family:var(--ut); font-size:170px; line-height:200px; color:#f2c14e; opacity:0; }
.win2 { position:absolute; top:1330px; left:60px; right:60px; text-align:center; font-family:var(--ut); font-size:80px; color:#f2c14e; opacity:0; }
.ask { position:absolute; top:1500px; left:60px; right:60px; text-align:center; font-size:56px; font-weight:700; line-height:1.2; color:var(--paper); opacity:0; }
.url { position:absolute; top:1660px; left:0; right:0; text-align:center; font-size:44px; font-weight:700; color:#9fb8b2; opacity:0; }
"""

LEVELS = [("ب", "بَ", "يْت", "house", "bayt", '"b" as in bed', "1 dot, underneath"),
          ("ت", "تَ", "مْر", "dates", "tamr", '"t" as in tea', "2 dots, on top"),
          ("ث", "ثَ", "لاثَة", "three", "thalātha", '"th" as in think', "3 dots, on top")]
GW, GH, GS = 1200, 800, 0.75                                    # the glyph canvas, and the scale it's shown at (900x600)

def glyph(path):
    """draws ٮ (the shape ب ت ث share) in the house font to a PNG, and finds where each letter's dots sit, by drawing
    each letter and keeping what's new against ٮ. Returns {letter: [(x0, y0, x1, y1), ...]} on the shown 900x600 box."""
    from playwright.sync_api import sync_playwright
    font = os.path.join(T.V6, "fonts", "ibm-plex-sans-arabic-arabic-700-normal.woff2")
    page = f"""<html><head><style>@font-face{{font-family:P;src:url("file://{font}");font-weight:700}}</style></head>
<body><span style="font-family:P;font-weight:700">ٮ</span><canvas id="c" width="{GW}" height="{GH}"></canvas></body></html>"""
    tmp = os.path.join(HERE, "out", "_glyph.html"); open(tmp, "w").write(page)
    js = """async () => { await document.fonts.load('700 720px P'); const W=%d, H=%d, c=document.getElementById('c'), x=c.getContext('2d');
  function draw(ch, col, bg){ x.clearRect(0,0,W,H); if (bg) { x.fillStyle=bg; x.fillRect(0,0,W,H); } x.fillStyle=col; x.font='700 720px P';
    x.textAlign='center'; x.textBaseline='middle'; x.fillText(ch, W/2, 420); return x.getImageData(0,0,W,H).data; }
  const base = draw('\\u066e', '#000', '#fff'), out = {};
  for (const ch of ['ب','ت','ث']) { const d = draw(ch, '#000', '#fff'), on = new Uint8Array(W*H);
    for (let i = 0; i < W*H; i++) on[i] = d[i*4] < 128 && base[i*4] >= 128 ? 1 : 0;
    const seen = new Uint8Array(W*H), comps = [];
    for (let s = 0; s < W*H; s++) { if (!on[s] || seen[s]) continue; const st = [s]; seen[s] = 1; let n = 0, b = [W, H, 0, 0];
      while (st.length) { const q = st.pop(), qx = q %% W, qy = (q / W) | 0; n++; b = [Math.min(b[0],qx), Math.min(b[1],qy), Math.max(b[2],qx), Math.max(b[3],qy)];
        for (const nb of [q+1, q-1, q+W, q-W]) if (nb >= 0 && nb < W*H && on[nb] && !seen[nb]) { seen[nb] = 1; st.push(nb); } }
      if (n > 400) comps.push(b); }
    out[ch] = comps; }
  draw('\\u066e', '#f1ece0', null); out.png = c.toDataURL('image/png'); return out; }""" % (GW, GH)
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME) if os.path.exists(CHROME) else pw.chromium.launch(); p = b.new_page(); p.goto("file://" + tmp); res = p.evaluate(js); b.close()
    os.remove(tmp)
    open(path, "wb").write(base64.b64decode(res.pop("png").split(",", 1)[1]))
    return {k: sorted([tuple(round(v * GS) for v in bx) for bx in v], key=lambda bx: -bx[0]) for k, v in res.items()}

def x2():
    c = Comp("x2-dots", "ARABIC SPEEDRUN · LEVEL 1-3", bed=False); c.css = D_CSS
    dots = glyph(os.path.join(c.a, "base.png"))
    gx, gy = 90, 640 + 20                                        # the glyph box on the page
    html, t = [], 0.6
    total_guess = 23.0
    score = ["0000", "0100", "0200", "0300", "0800"]
    for L, (ch, first, rest, en, tr, snd, how) in enumerate(LEVELS):
        if L:                                                    # clear the last level: its dots fly off, its word drops away
            for j in range(L):
                c.t(f'tl.to("#d{L - 1}{j}", {{y:-900, opacity:0, duration:0.45, ease:"power2.in"}}, {t:.2f});')
            c.t(f'tl.to("#wc{L - 1}", {{opacity:0, y:120, duration:0.35, ease:"power2.in"}}, {t:.2f});')
            c.t(f'tl.to(".lvl span:nth-child({L})", {{opacity:0, duration:0.15}}, {t + 0.2:.2f});')
            c.t(f'tl.to(".lvl span:nth-child({L + 1})", {{opacity:1, duration:0.15}}, {t + 0.2:.2f});')
            t += 0.4
        # the level banner sweeps through
        html.append(f'<div class="ban" id="bn{L}" data-layout-allow-overlap><b>LEVEL {L + 1}</b><span>{e(how)}</span></div>')
        c.t(f'tl.fromTo("#bn{L}", {{x:1200}}, {{x:0, duration:0.32, ease:"power3.out"}}, {t:.2f});')
        c.t(f'tl.to("#bn{L}", {{x:-1200, duration:0.28, ease:"power3.in"}}, {t + 0.62:.2f});')
        t += 0.85
        # the power-ups fall
        boxes = dots[ch]; assert len(boxes) == L + 1, (ch, boxes)
        land = t
        for j, (x0, y0, x1, y1) in enumerate(boxes):
            html.append(f'<i class="dt" id="d{L}{j}" style="left:{gx + x0}px; top:{gy + y0}px; width:{x1 - x0 + 1}px; height:{y1 - y0 + 1}px"></i>')
            at = t + j * 0.16; land = at + 0.5
            c.t(f'tl.fromTo("#d{L}{j}", {{y:-1300, opacity:1}}, {{y:0, duration:0.55, ease:"bounce.out"}}, {at:.2f});')
            cx, cy = gx + (x0 + x1) // 2, gy + (y0 + y1) // 2
            html.append(burst(c, f"s{L}{j}", cx, cy, at + 0.3, n=10, spread=170, seed=L * 10 + j, colors=["#f2c14e", "#fff7dc"], size=(14, 14)))
        shake(c, ".stage", t + 0.3, 18, 6)
        c.t(f'tl.fromTo(".flash", {{opacity:0.4}}, {{opacity:0, duration:0.35, immediateRender:false}}, {t + 0.3:.2f});')
        c.t(f'tl.fromTo(".gbox img", {{scaleY:0.9, scaleX:1.05}}, {{scaleY:1, scaleX:1, duration:0.5, ease:"elastic.out(1, 0.4)", immediateRender:false}}, {t + 0.3:.2f});')
        c.t(f'tl.to(".scc", {{y:{-(L + 1) * 56}, duration:0.3, ease:"power2.out"}}, {land:.2f});')
        c.t(f'tl.to(".xp i", {{scaleX:{(L + 1) / 3:.3f}, duration:0.45, ease:"power2.out"}}, {land:.2f});')
        c.t(f'tl.fromTo("#pt{L}", {{opacity:1, y:0}}, {{opacity:0, y:-120, duration:0.9, ease:"power1.out", immediateRender:false}}, {land:.2f});')
        html.append(f'<div class="pts" id="pt{L}">+100</div>')
        t = land + 0.25
        # the word that starts with it
        html.append(f'<div class="wc" id="wc{L}" data-layout-allow-overlap><div class="snd"><span lang="ar">{ch}</span> = {e(snd)}</div>'
                    f'<div class="ar" lang="ar"><i>{first}</i>{rest}</div><div class="mn">{e(en)} <em>· {e(tr)}</em></div></div>')
        c.t(f'tl.fromTo("#wc{L}", {{opacity:0, y:80, scale:0.85}}, {{opacity:1, y:0, scale:1, duration:0.4, ease:"back.out(1.8)"}}, {t:.2f});')
        t += max(c.say(first + rest, t + 0.3), 0.8) + 0.6
    # all clear → the boss
    c.t(f'tl.to([".gbox", ".dt", "#wc2"], {{opacity:0, scale:0.8, duration:0.35, ease:"power2.in"}}, {t:.2f});')
    c.t(f'tl.to(".lvl span:nth-child(3)", {{opacity:0, duration:0.15}}, {t + 0.2:.2f}); tl.to(".lvl span:nth-child(4)", {{opacity:1, duration:0.15}}, {t + 0.2:.2f});')
    t += 0.4
    html.append('<div class="ban" id="bnb" data-layout-allow-overlap style="background:#17262b"><b>BOSS LEVEL 👾</b><span>find the letter</span></div>')
    c.t(f'tl.fromTo("#bnb", {{x:1200}}, {{x:0, duration:0.32, ease:"power3.out"}}, {t:.2f});')
    shake(c, "#bnb", t + 0.32, 14, 5)
    c.t(f'tl.to("#bnb", {{x:-1200, duration:0.28, ease:"power3.in"}}, {t + 0.85:.2f});')
    t += 1.05
    # the shell game: ب ت ث face up, flip, shuffle
    XS = [-300, 0, 300]; slot = {0: 2, 1: 1, 2: 0}               # card → slot (ب on the right, then ت, then ث)
    cards = ""
    for k, ch in enumerate("بتث"):
        cards += (f'<div class="card" id="cd{k}"><div class="fc" data-layout-allow-overlap><span lang="ar">{ch}</span></div>'
                  f'<div class="bc" data-layout-allow-overlap>?</div></div>')
        c.t(f'tl.set("#cd{k}", {{x:{XS[slot[k]]}}}, 0);')
        c.t(f'tl.fromTo("#cd{k}", {{opacity:0, y:120, rotation:{(k - 1) * 8}}}, {{opacity:1, y:0, rotation:0, duration:0.4, ease:"back.out(2)"}}, {t + 0.1 * (2 - slot[k]):.2f});')
    t += 0.8
    def flip(k, at, down):
        a, b = (".fc", ".bc") if down else (".bc", ".fc")
        c.t(f'tl.to("#cd{k}", {{scaleX:0, duration:0.13, ease:"power1.in"}}, {at:.2f});')
        c.t(f'tl.set("#cd{k} {a}", {{opacity:0}}, {at + 0.13:.2f}); tl.set("#cd{k} {b}", {{opacity:1}}, {at + 0.13:.2f});')
        c.t(f'tl.to("#cd{k}", {{scaleX:1, duration:0.13, ease:"power1.out"}}, {at + 0.13:.2f});')
    for k in range(3): flip(k, t + k * 0.08, True)
    t += 0.55
    for a_, b_ in [(0, 1), (1, 2), (0, 2), (0, 1), (0, 2)]:     # ت ends on the left
        ka = next(k for k, s in slot.items() if s == a_); kb = next(k for k, s in slot.items() if s == b_)
        for k, to, lift in ((ka, b_, -90), (kb, a_, 90)):
            c.t(f'tl.to("#cd{k}", {{x:{XS[to]}, duration:0.34, ease:"power2.inOut"}}, {t:.2f});')
            c.t(f'tl.to("#cd{k}", {{keyframes:[{{y:{lift}, duration:0.17, ease:"power1.out"}}, {{y:0, duration:0.17, ease:"power1.in"}}]}}, {t:.2f});')
        slot[ka], slot[kb] = b_, a_
        t += 0.38
    t += 0.2
    c.t(f'tl.fromTo(".where", {{opacity:0, scale:1.5}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(2)"}}, {t:.2f});')
    t += 0.5
    for n in range(3):
        c.t(f'tl.fromTo(".cd span:nth-child({n + 1})", {{opacity:0, scale:1.6}}, {{opacity:1, scale:1, duration:0.2, ease:"power3.out"}}, {t + n * 0.7:.2f});')
        c.t(f'tl.to(".cd span:nth-child({n + 1})", {{opacity:0, duration:0.12}}, {t + n * 0.7 + 0.58:.2f});')
    t += 2.15
    for k in range(3): flip(k, t + k * 0.06, False)
    c.t(f'tl.to(["#cd0", "#cd2"], {{opacity:0.55, duration:0.3}}, {t + 0.35:.2f});')
    c.t(f'tl.to("#cd1 .fc", {{backgroundColor:"#f2c14e", duration:0.25}}, {t + 0.35:.2f});')
    c.t(f'tl.fromTo("#cd1", {{scale:1}}, {{scale:1.18, duration:0.3, ease:"back.out(3)", immediateRender:false}}, {t + 0.35:.2f});')
    html.append(burst(c, "cb", 540 + XS[slot[1]], 930, t + 0.4, n=34, spread=520, seed=42, colors=["#f2c14e", "#fff7dc", "#b4322a", "#2e7263"]))
    shake(c, ".cards", t + 0.4, 14, 5)
    c.t(f'tl.to(".scc", {{y:{-4 * 56}, duration:0.3, ease:"power2.out"}}, {t + 0.4:.2f});')
    c.t(f'tl.to(".where", {{opacity:0, duration:0.2}}, {t + 0.3:.2f});')
    c.t(f'tl.fromTo(".win2", {{opacity:0, scale:1.6}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(2)"}}, {t + 0.45:.2f});')
    t += 1.4
    c.inn(".ask", t, 30); c.inn(".url", t + 0.5, 20)
    t += 2.6
    c.t(f'tl.fromTo(".grid", {{backgroundPosition:"0px 0px"}}, {{backgroundPosition:"0px 900px", duration:{t}, ease:"none"}}, 0);')
    # keep the guessed total honest
    assert t < total_guess + 2, t
    body = ('      <div class="grid"></div>'
            '<div class="hook">1 shape + <b>dots</b> = 3 Arabic letters 🎮</div>'
            '<div class="hud"><div class="lvl">' + "".join(
                f'<span class="{"on" if i == 0 else ""}" data-layout-allow-overlap>LEVEL <b>{x}</b></span>' for i, x in enumerate(["1/3", "2/3", "3/3", "BOSS"])) +
            '</div><div class="sc"><em>SCORE</em><div class="scw"><div class="scc" data-layout-allow-overflow data-layout-allow-occlusion>' + "".join(f"<div data-layout-allow-occlusion>{s}</div>" for s in score) + '</div></div></div></div>'
            '<div class="xp"><i></i></div>'
            '<div class="stage"><div class="gbox"><img src="assets/base.png" alt=""/></div></div>'
            + "".join(html) +
            f'<div class="cards">{cards}</div>'
            '<div class="where">Where’s <span class="ar" lang="ar">ت</span>? 👀</div>'
            '<div class="cd">' + "".join(f'<span data-layout-allow-overlap>{n}</span>' for n in (3, 2, 1)) + '</div>'
            '<div class="win2" data-layout-allow-overlap>+500 ✨</div>'
            '<div class="ask">Found it? Comment your score 👇</div><div class="url">rafiq-arabic.com</div><div class="flash" data-layout-allow-overlap></div>')
    c.write(body, round(t, 2))

ALL = {"x1-machine": x1, "x2-dots": x2}
if __name__ == "__main__":
    ids = [a for a in sys.argv[1:] if not a.startswith("--")]
    T.LUFS.update({v: -16.0 for v in ALL})
    for vid, fn in ALL.items():
        if ids and vid not in ids: continue
        T.level(vid) if "--level" in sys.argv else fn()
