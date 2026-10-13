#!/usr/bin/env python3
"""Ten TikToks, 10-20s each, ten different styles (#239). The reading voice only; hook on screen from the first frame.

  m01-tetris      Arabic Tetris: letter blocks fall and lock into بَيْت, بِنْت, باب; the row clears when the word is said
  m02-rocket      Count down in Arabic: عَشَرَة … واحِد, then صِفْر and the rocket launches ('zero' comes from ṣifr)
  m03-swipe       Arabic or not? Swipe cards: sugar ✅, pizza ❌, lemon ✅, safari ✅, tea ❌ (but Arabic borrowed it: شاي)
  m04-catch       Sound on: animals rain down, catch the one you hear (قِطّ, جَمَل, حِصان, سَمَك)
  m05-typing      A phone keyboard: watch the letters change shape as كتاب, شكرا, سيارة are typed
  m06-pong        Opposites ping-pong: كَبِير/صَغِير, حارّ/بارِد, طَويل/قَصِير, a word on every hit
  m07-wordle      Arabic Wordle: باب → بنت → بيت
  m08-day1        Day 1 vs Day 30: the same sentence, a blur, then read word by word
  m09-speed       Read it before the timer, and it gets faster: باب, قَلَم, شاي, بَحْر, سَيَّارَة
  m10-heart-dog   قَلْب or كَلْب: one letter between "heart" and "dog"

Every word and its meaning are the app's own (vocab-data.js, alphabet-data.js, drills-data.js); brag-quiz/MIX.md lists them.

  python3 brag-quiz/build_mix.py [id ...]     then render each, then  --level
"""
import os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import build_teach as T
from build_teach import Comp, e
from build_wild import burst, shake

GOLD = "#f2c14e"
COMMON = """
@font-face { font-family:"Noto Color Emoji"; src:local("Noto Color Emoji"); }
.hook { position:absolute; top:258px; left:40px; right:40px; text-align:center; font-size:62px; font-weight:700; line-height:1.1; letter-spacing:-.02em; }
.hook b { color:var(--rubric); }
.cf { position:absolute; border-radius:4px; opacity:0; }
.emo { font-family:"Noto Color Emoji", sans-serif; }
.ar { font-family:var(--ar); font-weight:700; }
"""
DARK = """
#root { background:var(--bgd, #0f1f1e); } #glow { opacity:.3; }
#brand b { color:var(--paper); } #brand .tile { background:var(--paper); } #brand .tile span { color:var(--ink); }
#kicker { color:#9fb8b2; }
.hook { color:var(--paper); } .hook b { color:#f2c14e; }
"""

def comp(vid, kicker, css, dark=False):
    c = Comp(vid, kicker, bed=False); c.css = COMMON + (DARK if dark else "") + css
    return c

def pop(c, sel, at, s0=0.6, d=0.35, ease="back.out(2)", later=False):
    c.t(f'tl.fromTo("{sel}", {{opacity:0, scale:{s0}}}, {{opacity:1, scale:1, duration:{d}, ease:"{ease}"{", immediateRender:false" if later else ""}}}, {at:.2f});')

def hide(c, sel, at, d=0.25):
    c.t(f'tl.to("{sel}", {{opacity:0, duration:{d}}}, {at:.2f});')

def say(c, text, at):
    return c.say(text, at)

# ---------------------------------------------------------------- m01: Arabic Tetris
TET_CSS = """
#root { --bgd:#101826; }
.grid { position:absolute; inset:0; background-image:linear-gradient(rgba(255,255,255,.04) 2px, transparent 2px), linear-gradient(90deg, rgba(255,255,255,.04) 2px, transparent 2px); background-size:60px 60px; }
.well { position:absolute; top:520px; left:240px; width:600px; height:1100px; border:8px solid rgba(242,193,78,.55); border-top:none; border-radius:0 0 26px 26px;
  background:rgba(255,255,255,.03); overflow:hidden; }
.blk { position:absolute; width:200px; height:200px; box-sizing:border-box; border-radius:24px; display:grid; place-items:center; border:7px solid rgba(255,255,255,.35);
  box-shadow:inset 0 -14px 0 rgba(0,0,0,.18); }
.blk span { font-family:var(--ar); font-weight:700; font-size:120px; line-height:1; color:#fff; margin-top:-26px; }
.mw { position:absolute; left:0; right:0; height:200px; display:grid; place-items:center; opacity:0; }
.mw span { font-family:var(--ar); font-weight:700; font-size:150px; line-height:1.4; color:#f2c14e; text-shadow:0 0 30px rgba(242,193,78,.5); }
.ml { position:absolute; left:0; right:0; text-align:center; font-size:56px; font-weight:700; color:var(--paper); opacity:0; }
.ml em { font-style:normal; color:#9fb8b2; font-weight:500; }
.hud { position:absolute; top:560px; left:36px; width:180px; text-align:center; font-family:var(--ut); color:#9fb8b2; font-size:30px; letter-spacing:.12em; }
.cnt { position:relative; height:110px; overflow:hidden; margin-top:6px; }
.cnt div { height:110px; line-height:110px; font-size:90px; color:#f2c14e; letter-spacing:0; }
.cntc { position:absolute; left:0; right:0; top:0; }
.fin { position:absolute; top:900px; left:240px; width:600px; text-align:center; font-size:64px; font-weight:700; line-height:1.15; color:var(--paper); opacity:0; }
.fin b { color:#f2c14e; }
.cta { position:absolute; top:1680px; left:40px; right:40px; text-align:center; font-size:46px; font-weight:700; color:#9fb8b2; opacity:0; }
"""
TET = [("بَيْت", "بيت", "house", "bayt"), ("بِنْت", "بنت", "girl", "bint"), ("باب", "باب", "door", "bāb")]
BLK = ["#b4322a", "#2e7263", "#c98f1c", "#3b6ea8", "#7b4ca0"]

def m01():
    c = comp("m01-tetris", "ARABIC TETRIS", TET_CSS, dark=True)
    well, t = [], 0.5
    for r, (ar, bare, en, tr) in enumerate(TET):
        ids = []
        for k, ch in enumerate(bare):
            bid = f"b{r}{k}"; ids.append("#" + bid); x = 400 - 200 * k   # right to left
            well.append(f'<div class="blk" id="{bid}" style="left:{x}px; top:880px; background:{BLK[(r * 3 + k) % 5]}" data-layout-allow-overlap>'
                        f'<span lang="ar">{ch}</span></div>')
            # spawn in the middle, slide to its column, fall in Tetris steps
            c.t(f'tl.set("#{bid}", {{x:{200 - x}}}, 0);')
            c.t(f'tl.fromTo("#{bid}", {{y:-1100}}, {{y:0, duration:0.62, ease:"steps(7)"}}, {t:.2f});')
            c.t(f'tl.to("#{bid}", {{x:0, duration:0.14, ease:"power2.out"}}, {t + 0.08:.2f});')
            c.t(f'tl.fromTo("#{bid}", {{scaleY:0.86}}, {{scaleY:1, duration:0.3, ease:"elastic.out(1, 0.4)", immediateRender:false}}, {t + 0.62:.2f});')
            shake(c, ".well", t + 0.62, 7, 3)
            t += 0.72
        # the row is full: flash, the blocks melt into the joined word
        t += 0.05
        c.t(f'tl.to([{", ".join(chr(34) + i + chr(34) for i in ids)}], {{backgroundColor:"#ffffff", duration:0.12}}, {t:.2f});')
        c.t(f'tl.to([{", ".join(chr(34) + i + chr(34) for i in ids)}], {{opacity:0, scale:0.8, duration:0.2}}, {t + 0.16:.2f});')
        well.append(f'<div class="mw" id="mw{r}" style="top:880px" data-layout-allow-overlap><span lang="ar">{e(ar)}</span></div>')
        well.append(f'<div class="ml" id="ml{r}" style="top:760px" data-layout-allow-overlap>{e(en)} <em>· {e(tr)}</em></div>')
        pop(c, f"#mw{r}", t + 0.2, 1.5)
        c.t(f'tl.fromTo("#ml{r}", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.3, ease:"power3.out"}}, {t + 0.35:.2f});')
        d = say(c, ar, t + 0.25); t += 0.25 + max(d, 0.8) + 0.45
        # clear the line
        c.t(f'tl.to(["#mw{r}", "#ml{r}"], {{scaleY:0, opacity:0, duration:0.25, ease:"power2.in"}}, {t:.2f});')
        well.append(burst(c, f"k{r}", 300, 980, t + 0.1, n=22, spread=330, seed=r + 5, colors=["#f2c14e", "#fff7dc", "#b4322a", "#3b6ea8"]))
        c.t(f'tl.to(".cntc", {{y:{-(r + 1) * 110}, duration:0.3, ease:"back.out(2)"}}, {t + 0.1:.2f});')
        t += 0.45
    c.t(f'tl.fromTo(".fin", {{opacity:0, scale:0.7}}, {{opacity:1, scale:1, duration:0.4, ease:"back.out(2)"}}, {t:.2f});')
    c.t(f'tl.fromTo(".cta", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.35}}, {t + 0.8:.2f});')
    t += 2.6
    body = ('      <div class="grid"></div><div class="hook">Arabic Tetris 🧱 Letters <b>snap into words</b></div>'
            '<div class="hud">LINES<div class="cnt"><div class="cntc" data-layout-allow-overflow>' +
            "".join(f"<div data-layout-allow-occlusion>{n}</div>" for n in range(4)) + '</div></div></div>'
            f'<div class="well">{"".join(well)}</div><div class="fin">3 lines. <b>3 words read</b> 🎉</div>'
            '<div class="cta">Learn to read Arabic · rafiq-arabic.com</div>')
    c.write(body, round(t, 2))

# ---------------------------------------------------------------- m02: rocket countdown
RKT_CSS = """
#root { --bgd:#0a1430; }
.star { position:absolute; width:6px; height:6px; border-radius:50%; background:#fff; }
.n { position:absolute; top:520px; left:0; right:0; display:flex; flex-direction:column; align-items:center; opacity:0; }
.n .d { font-family:var(--ar); font-weight:700; font-size:260px; line-height:1.15; color:#f2c14e; }
.n .nw { font-family:var(--ar); font-weight:700; font-size:110px; line-height:1.4; color:var(--paper); margin-top:-30px; }
.n .nl { font-family:var(--ut); font-size:38px; color:#9fb8b2; }
.rk { position:absolute; top:1290px; left:390px; width:300px; height:300px; display:grid; place-items:center; }
.rk span { font-size:230px; line-height:1; transform:rotate(-45deg); color:#fff; }
.fire { position:absolute; top:1520px; left:470px; width:140px; height:220px; border-radius:50% 50% 50% 50% / 30% 30% 70% 70%;
  background:radial-gradient(circle at 50% 30%, #fff7dc 0%, #f2c14e 35%, #e0572e 70%, rgba(224,87,46,0) 100%); transform-origin:50% 0; opacity:0; }
.pad { position:absolute; top:1590px; left:300px; width:480px; height:26px; border-radius:13px; background:#2b3e5a; }
.puff { position:absolute; width:120px; height:120px; border-radius:50%; background:rgba(220,226,235,.85); opacity:0; }
.fact { position:absolute; top:880px; left:70px; right:70px; text-align:center; font-size:66px; font-weight:700; line-height:1.15; color:var(--paper); opacity:0; }
.fact .ar { color:#f2c14e; }
.cta { position:absolute; top:1180px; left:70px; right:70px; text-align:center; font-size:48px; font-weight:700; color:#9fb8b2; opacity:0; }
.flash { position:absolute; inset:0; background:#fff7dc; opacity:0; pointer-events:none; }
"""
NUMS = [("١٠", "عَشَرَة", "10 · ʿashara"), ("٩", "تِسْعَة", "9 · tisʿa"), ("٨", "ثَمانِيَة", "8 · thamāniya"), ("٧", "سَبْعَة", "7 · sabʿa"),
        ("٦", "سِتَّة", "6 · sitta"), ("٥", "خَمْسَة", "5 · khamsa"), ("٤", "أَرْبَعَة", "4 · arbaʿa"), ("٣", "ثَلاثَة", "3 · thalātha"),
        ("٢", "اثْنانِ", "2 · ithnān"), ("١", "واحِد", "1 · wāḥid"), ("٠", "صِفْر", "0 · ṣifr")]

def m02():
    c = comp("m02-rocket", "COUNT DOWN IN ARABIC", RKT_CSS, dark=True)
    r = random.Random(3)
    stars = "".join(f'<i class="star" id="sr{i}" style="left:{r.randint(10, 1070)}px; top:{r.randint(380, 1880)}px; opacity:{r.uniform(.3, .9):.2f}"></i>' for i in range(70))
    html, t = [], 0.5
    for i, (dg, ar, lb) in enumerate(NUMS):
        html.append(f'<div class="n" id="n{i}" data-layout-allow-overlap><div class="d" lang="ar">{dg}</div><div class="nw" lang="ar">{e(ar)}</div><div class="nl">{e(lb)}</div></div>')
        pop(c, f"#n{i}", t, 1.5, 0.25, "power3.out")
        d = say(c, ar, t + 0.02)
        if i >= 5: shake(c, ".rk", t, 4 + (i - 5) * 3, 6)                  # the rocket rumbles more each second
        if i >= 6:
            for j in range(2):
                pid = f"pf{i}{j}"; x = 380 + (j * 220) + r.randint(-30, 30)
                html.append(f'<i class="puff" id="{pid}" style="left:{x}px; top:1500px"></i>')
                c.t(f'tl.fromTo("#{pid}", {{opacity:0.9, scale:0.4, x:0, y:0}}, {{opacity:0, scale:{1.6 + (i - 6) * 0.3:.1f}, x:{(-1 if j == 0 else 1) * r.randint(80, 160)}, y:-40, duration:1.2, ease:"power2.out"}}, {t:.2f});')
        if i < len(NUMS) - 1:
            t += max(d, 0.7) + 0.12
            hide(c, f"#n{i}", t - 0.08, 0.1)
    # zero: lift-off
    c.t(f'tl.fromTo(".fire", {{opacity:0, scaleY:0.3}}, {{opacity:1, scaleY:1.4, duration:0.3, ease:"power2.out"}}, {t + 0.1:.2f});')
    c.t(f'tl.fromTo(".flash", {{opacity:0.6}}, {{opacity:0, duration:0.4, immediateRender:false}}, {t + 0.2:.2f});')
    c.t(f'tl.to([".rk", ".fire"], {{y:-1900, duration:1.3, ease:"power3.in"}}, {t + 0.4:.2f});')
    c.t(f'tl.to(".star", {{y:"+=700", scaleY:4, duration:1.3, ease:"power3.in"}}, {t + 0.4:.2f});')
    c.t(f'tl.to(".pad", {{opacity:0, duration:0.4}}, {t + 0.6:.2f});')
    t += 1.1
    hide(c, f"#n{len(NUMS) - 1}", t, 0.25)
    c.t(f'tl.fromTo(".fact", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.4, ease:"back.out(1.8)"}}, {t + 0.3:.2f});')
    c.t(f'tl.fromTo(".cta", {{opacity:0}}, {{opacity:1, duration:0.4}}, {t + 1.3:.2f});')
    t += 3.4
    body = (f'      {stars}<div class="hook">Count down in Arabic 🚀 <b>Say it with me!</b></div>' + "".join(html) +
            '<div class="pad"></div><div class="fire"></div><div class="rk"><span class="emo">🚀</span></div>'
            '<div class="fact"><span class="ar" lang="ar">صِفْر</span> (ṣifr) is where English got the word <b>“zero”</b> 🤯</div>'
            '<div class="cta">Did you count along? 👇</div><div class="flash"></div>')
    c.write(body, round(t, 2))

# ---------------------------------------------------------------- m03: Arabic or not? swipe
SW_CSS = """
.stack { position:absolute; top:470px; left:150px; width:780px; height:980px; }
.bk { position:absolute; inset:0; border-radius:56px; background:#e5dcc8; }
.cd { position:absolute; inset:0; border-radius:56px; background:#fffdf8; border:4px solid rgba(23,38,43,.12); box-shadow:0 30px 60px -30px rgba(23,38,43,.55);
  display:flex; flex-direction:column; align-items:center; padding-top:90px; box-sizing:border-box; }
.cd .em { font-size:230px; line-height:1.15; }
.cd .en { font-size:120px; font-weight:700; letter-spacing:-.03em; margin-top:10px; }
.cd .arw { margin-top:20px; text-align:center; opacity:0; }
.cd .arw .ar { font-size:110px; line-height:1.4; color:var(--verdigris); }
.cd .arw i { display:block; font-style:normal; font-size:40px; color:var(--ink-soft); margin-top:-10px; }
.stamp { position:absolute; top:70px; padding:10px 34px; border-radius:22px; font-family:var(--ut); font-size:64px; font-weight:500; letter-spacing:.06em;
  border:8px solid; transform:rotate(-12deg); opacity:0; background:rgba(255,253,248,.9); }
.stamp.y { right:50px; color:#2e7263; border-color:#2e7263; }
.stamp.n { left:50px; color:#b4322a; border-color:#b4322a; transform:rotate(12deg); }
.tm { position:absolute; bottom:60px; left:90px; right:90px; height:20px; border-radius:10px; background:rgba(23,38,43,.1); overflow:hidden; }
.tm i { position:absolute; inset:0; background:var(--rubric); transform-origin:0 50%; }
.lr { position:absolute; top:1490px; left:110px; right:110px; display:flex; justify-content:space-between; font-family:var(--ut); font-size:38px; }
.lr .l { color:#b4322a; } .lr .r { color:#2e7263; }
.twist { position:absolute; top:1570px; left:60px; right:60px; text-align:center; font-size:50px; font-weight:700; opacity:0; }
.twist .ar { color:var(--verdigris); }
.score { position:absolute; top:1700px; left:0; right:0; display:flex; justify-content:center; gap:22px; }
.score span { width:84px; height:84px; border-radius:50%; display:grid; place-items:center; font-size:46px; background:rgba(23,38,43,.07); }
.score b { opacity:0; }
.end { position:absolute; top:880px; left:60px; right:60px; text-align:center; font-size:76px; font-weight:700; line-height:1.15; opacity:0; }
"""
SWIPE = [("🍬", "sugar", True, "سُكَّر", "sukkar"), ("🍕", "pizza", False, None, "it’s Italian 🇮🇹"), ("🍋", "lemon", True, "لَيْمون", "laymūn"),
         ("🦁", "safari", True, "سَفَر", "safar · travel"), ("🍵", "tea", False, "شاي", "it’s from Chinese 🇨🇳")]

def m03():
    c = comp("m03-swipe", "ARABIC OR NOT?", SW_CSS)
    cards, t = [], 0.6
    for i, (em, en, yes, ar, tr) in enumerate(SWIPE):
        arw = (f'<div class="arw" id="aw{i}" data-layout-allow-occlusion><div class="ar" lang="ar">{e(ar)}</div><i>{e(tr)}</i></div>' if yes else
               f'<div class="arw" id="aw{i}" data-layout-allow-occlusion><i>{e(tr)}</i></div>')
        cards.append(f'<div class="cd" id="cd{i}"><div class="em emo" data-layout-allow-occlusion data-layout-allow-overlap>{em}</div><div class="en" data-layout-allow-occlusion data-layout-allow-overlap>{e(en)}</div>{arw}'
                     f'<div class="stamp {"y" if yes else "n"}" id="sp{i}" data-layout-allow-occlusion>{"ARABIC ✓" if yes else "NOPE ✗"}</div>'
                     f'<div class="tm"><i id="tm{i}"></i></div></div>')
        if i: c.t(f'tl.fromTo("#cd{i}", {{scale:0.94, y:36}}, {{scale:1, y:0, duration:0.3, ease:"power2.out", immediateRender:false}}, {t - 0.3:.2f});')
        c.t(f'tl.fromTo("#tm{i}", {{scaleX:1}}, {{scaleX:0, duration:1.1, ease:"none"}}, {t:.2f});')
        t += 1.15
        c.t(f'tl.fromTo("#sp{i}", {{opacity:0, scale:2.2}}, {{opacity:1, scale:1, duration:0.22, ease:"power3.in"}}, {t:.2f});')
        shake(c, f"#cd{i}", t + 0.22, 10, 4)
        c.t(f'tl.to("#sc{i}", {{opacity:1, duration:0.15}}, {t + 0.22:.2f});')
        c.t(f'tl.fromTo("#aw{i}", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.3}}, {t + 0.3:.2f});')
        if yes:
            d = say(c, ar, t + 0.35); t += 0.35 + max(d, 0.8) + 0.35
        elif ar:                                                  # tea: English didn't get it from Arabic, but Arabic borrowed it too
            c.t(f'tl.fromTo(".twist", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.3}}, {t + 0.5:.2f});')
            d = say(c, ar, t + 0.6); t += 0.6 + max(d, 0.8) + 0.6
        else:
            t += 0.9
        c.t(f'tl.to("#cd{i}", {{x:{1150 if yes else -1150}, rotation:{24 if yes else -24}, duration:0.42, ease:"power2.in"}}, {t:.2f});')
        t += 0.42
    hide(c, ".twist", t - 0.4)
    c.t(f'tl.fromTo(".end", {{opacity:0, scale:0.8}}, {{opacity:1, scale:1, duration:0.4, ease:"back.out(2)"}}, {t:.2f});')
    t += 2.4
    body = ('      <div class="hook">Did English get this word <b>from Arabic</b>? 👀</div>'
            '<div class="stack"><div class="bk" style="transform:rotate(-4deg) translateY(30px)"></div><div class="bk" style="transform:rotate(3deg) translateY(18px)"></div>'
            + "".join(reversed(cards)) +
            '</div><div class="end">How many did you get right? 👇</div><div class="lr"><span class="l">← NOT ARABIC</span><span class="r">FROM ARABIC →</span></div>'
            '<div class="twist">…but Arabic borrowed “tea” too: <span class="ar" lang="ar">شاي</span> 😄</div>'
            '<div class="score">' + "".join(f'<span class="emo"><b id="sc{i}">{"✅" if s[2] else "❌"}</b></span>' for i, s in enumerate(SWIPE)) + '</div>')
    c.write(body, round(t, 2))

# ---------------------------------------------------------------- m04: catch the animal you hear
CT_CSS = """
#root { background:linear-gradient(#cfe8ee, #f1ece0 75%); }
.field { position:absolute; top:470px; left:0; right:0; height:1300px; overflow:hidden; }
.fall { position:absolute; width:150px; height:150px; display:grid; place-items:center; font-size:120px; line-height:1; }
.ret { position:absolute; width:230px; height:230px; border-radius:50%; border:10px solid var(--rubric); box-sizing:border-box; opacity:0; }
.ret::before, .ret::after { content:""; position:absolute; background:var(--rubric); }
.ret::before { left:50%; top:-36px; bottom:-36px; width:8px; margin-left:-4px; }
.ret::after { top:50%; left:-36px; right:-36px; height:8px; margin-top:-4px; }
.got { position:absolute; left:0; right:0; top:1240px; display:flex; flex-direction:column; align-items:center; opacity:0; }
.got .bub { background:var(--ink); color:var(--paper); border-radius:40px; padding:18px 50px 22px; text-align:center; box-shadow:0 20px 40px -20px rgba(23,38,43,.7); }
.got .ar { font-size:110px; line-height:1.4; color:#f2c14e; }
.got i { display:block; font-style:normal; font-size:46px; font-weight:700; margin-top:-8px; }
.ask { position:absolute; top:410px; left:0; right:0; text-align:center; font-size:46px; font-weight:700; color:var(--ink-soft); opacity:0; }
.score { position:absolute; top:400px; right:50px; font-family:var(--ut); font-size:40px; color:var(--ink); }
.scw { display:inline-block; position:relative; width:32px; height:52px; overflow:hidden; vertical-align:bottom; }
.scc { position:absolute; left:0; top:0; } .scc div { height:52px; line-height:52px; color:var(--rubric); }
.end { position:absolute; top:900px; left:60px; right:60px; text-align:center; font-size:76px; font-weight:700; line-height:1.15; opacity:0; }
.end b { color:var(--rubric); }
"""
CATCH = [("قِطّ", "🐱", "cat", "qiṭṭ"), ("جَمَل", "🐪", "camel", "jamal"), ("حِصان", "🐴", "horse", "ḥiṣān"), ("سَمَك", "🐟", "fish", "samak")]
DECOY = ["🐶", "🦁", "🐮", "🐔", "🐸", "🐵", "🐘", "🦊", "🐰", "🐻", "🐼", "🐷"]
COLS = [80, 245, 410, 575, 740, 905]                             # left edge of each falling column (150 wide)
FALL_FROM, FALL_TO, FALL_T = -170, 1320, 4.4                     # field coords; seconds to cross

def m04():
    c = comp("m04-catch", "SOUND ON · CATCH IT", CT_CSS)
    r = random.Random(11); v = (FALL_TO - FALL_FROM) / FALL_T
    falls, n = [], 0
    catches = [2.5 + 3.3 * k for k in range(len(CATCH))]
    targets = []
    for k, (ar, em, en, tr) in enumerate(CATCH):
        col = [1, 4, 2, 3][k]; s = catches[k] - (520 - FALL_FROM) / v        # the target is at y=520 in the field when it's caught
        targets.append((col, s))
    def add(em, col, s, tid=None):
        nonlocal n
        fid = tid or f"f{n}"; n += 1
        falls.append(f'<div class="fall emo" id="{fid}" style="left:{COLS[col]}px; top:{FALL_FROM}px" data-layout-allow-overlap data-layout-allow-occlusion>{em}</div>')
        start = max(s, 0); y0 = (start - s) * v
        c.t(f'tl.fromTo("#{fid}", {{y:{y0:.0f}}}, {{y:{FALL_TO - FALL_FROM:.0f}, duration:{FALL_T - (start - s):.2f}, ease:"none"}}, {start:.2f});')
    # decoys: a steady rain, kept clear of each target's lane around its fall
    s = -3.5
    while s < catches[-1] + 1.5:
        col = r.randrange(6)
        if not any(col == tc and abs(s - ts) < 1.2 for tc, ts in targets):
            add(r.choice(DECOY), col, s)
        s += 0.3
    html, t = [], 0
    for k, (ar, em, en, tr) in enumerate(CATCH):
        col, s = targets[k]; add(em, col, s, f"tg{k}"); C = catches[k]
        d = say(c, ar, C - 1.9)
        c.t(f'tl.fromTo(".ask", {{opacity:0}}, {{opacity:1, duration:0.2, immediateRender:false}}, {C - 1.8:.2f}); tl.to(".ask", {{opacity:0, duration:0.2}}, {C - 0.1:.2f});')
        x, y = COLS[col] + 75, 470 + 520 + 75                   # page coords of the target's centre at the catch
        html.append(f'<div class="ret" id="rt{k}" style="left:{x - 115}px; top:{y - 115}px"></div>')
        c.t(f'tl.fromTo("#rt{k}", {{opacity:0, scale:2.2, rotation:-90}}, {{opacity:1, scale:1, rotation:0, duration:0.3, ease:"power3.out"}}, {C:.2f});')
        c.t(f'tl.to("#rt{k}", {{opacity:0, scale:0.6, duration:0.25}}, {C + 1.1:.2f});')
        # freeze the target: hide the falling one, show a still copy that grows
        c.t(f'tl.set("#tg{k}", {{opacity:0}}, {C + 0.3:.2f});')
        html.append(f'<div class="fall emo" id="hd{k}" style="left:{x - 75}px; top:{y - 75}px; opacity:0" data-layout-allow-overlap data-layout-allow-occlusion>{em}</div>')
        c.t(f'tl.set("#hd{k}", {{opacity:1}}, {C + 0.3:.2f});')
        c.t(f'tl.to("#hd{k}", {{scale:1.7, duration:0.3, ease:"back.out(2.5)"}}, {C + 0.3:.2f});')
        c.t(f'tl.to("#hd{k}", {{opacity:0, scale:0.5, duration:0.25}}, {C + 1.6:.2f});')
        html.append(f'<div class="got" id="gt{k}" data-layout-allow-overlap><div class="bub"><div class="ar" lang="ar">{e(ar)}</div><i>{e(en)} · {e(tr)}</i></div></div>')
        c.t(f'tl.fromTo("#gt{k}", {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.3, ease:"back.out(2)"}}, {C + 0.35:.2f});')
        c.t(f'tl.to("#gt{k}", {{opacity:0, duration:0.25}}, {C + 1.6:.2f});')
        c.t(f'tl.to(".scc", {{y:{-(k + 1) * 52}, duration:0.25}}, {C + 0.35:.2f});')
        html.append(burst(c, f"z{k}", x, y, C + 0.3, n=16, spread=260, seed=k + 20))
        t = C + 1.9
    c.t(f'tl.to(".field", {{opacity:0.25, duration:0.3}}, {t:.2f});')
    c.t(f'tl.fromTo(".end", {{opacity:0, scale:0.8}}, {{opacity:1, scale:1, duration:0.4, ease:"back.out(2)"}}, {t:.2f});')
    t += 2.5
    body = ('      <div class="hook">Sound on 🔊 <b>Catch the animal</b> you hear 🎯</div>'
            f'<div class="field">{"".join(falls)}</div>' + "".join(html) +
            '<div class="ask">Which one? 👀</div>'
            '<div class="score"><span class="emo">🎯</span> <span class="scw"><span class="scc" data-layout-allow-overflow>' +
            "".join(f"<div data-layout-allow-occlusion>{i}</div>" for i in range(5)) + '</span></span>/4</div>'
            '<div class="end">Caught all 4? <b>Your ears are ready</b> 👂 Tell me 👇</div>')
    c.write(body, round(t, 2))

# ---------------------------------------------------------------- m05: typing on an Arabic keyboard
TY_CSS = """
.phone { position:absolute; top:430px; left:70px; right:70px; height:1420px; border-radius:70px; background:#fffdf8; border:10px solid var(--ink);
  box-shadow:0 30px 60px -30px rgba(23,38,43,.6); overflow:hidden; }
.nbar { position:absolute; top:0; left:0; right:0; height:120px; background:#efe9dc; display:flex; align-items:center; justify-content:center; font-size:40px; font-weight:700; color:var(--ink-soft); }
.fld { position:absolute; top:150px; left:40px; right:40px; height:330px; border-radius:36px; background:#f4efe4; border:4px solid rgba(23,38,43,.1); }
.st { position:absolute; inset:0; display:flex; align-items:center; justify-content:flex-end; padding-right:60px; font-family:var(--ar); font-weight:700; font-size:190px;
  line-height:1; color:var(--ink); opacity:0; }
.st span { margin-top:-40px; }
.st.done { justify-content:center; padding:0; color:var(--verdigris); flex-direction:column; }
.st.done i { font-style:normal; font-family:var(--la); font-size:52px; color:var(--ink); margin-top:14px; }
.note { position:absolute; top:520px; left:60px; right:60px; text-align:center; font-size:52px; font-weight:700; color:var(--rubric); opacity:0; }
.kb { position:absolute; bottom:0; left:0; right:0; height:560px; background:#e3ddd0; display:flex; flex-direction:column; gap:14px; padding:26px 10px 0; box-sizing:border-box; }
.krow { display:flex; justify-content:center; gap:8px; }
.k { width:70px; height:110px; border-radius:16px; background:#fffdf8; display:grid; place-items:center; font-family:var(--ar); font-weight:700; font-size:50px; line-height:1;
  color:var(--ink); box-shadow:0 5px 0 rgba(23,38,43,.18); }
.k.ent { width:220px; font-family:var(--la); font-size:40px; background:var(--verdigris); color:var(--paper); }
.k.sp { width:420px; }
.end { position:absolute; top:520px; left:60px; right:60px; text-align:center; font-size:58px; font-weight:700; line-height:1.15; opacity:0; }
.end b { color:var(--rubric); }
"""
KB = ["ضصثقفغعهخحج", "شسيبلاتنمكط", "ئءؤرىةوزظد"]
WORDS5 = [("كتاب", "كِتاب", "book", "ك just changed shape 👀", 2), ("شكرا", "شُكْراً", "thank you", "ر doesn’t join the letter after it", 4),
          ("سيارة", "سَيَّارَة", "car", "ة only ever comes at the end", 5)]

def m05():
    c = comp("m05-typing", "TYPING IN ARABIC", TY_CSS)
    keys = {}
    rows = ""
    for ri, row in enumerate(KB):
        rows += '<div class="krow">' + "".join(f'<div class="k" id="k{ri}{j}"><span lang="ar">{ch}</span></div>' for j, ch in enumerate(row)) + '</div>'
        for j, ch in enumerate(row): keys[ch] = f"#k{ri}{j}"
    rows += '<div class="krow"><div class="k sp" id="ksp"></div><div class="k ent" id="ken">done ✓</div></div>'
    states, notes, t = [], [], 0.7
    for w, (bare, voc, en, note, at_i) in enumerate(WORDS5):
        prev = None
        for i in range(1, len(bare) + 1):
            sid = f"s{w}{i}"; states.append(f'<div class="st" id="{sid}" data-layout-allow-overlap><span lang="ar">{bare[:i]}</span></div>')
            k = keys[bare[i - 1]]
            c.t(f'tl.to("{k}", {{backgroundColor:"#2e7263", color:"#f1ece0", scale:0.86, duration:0.08}}, {t:.2f});')
            c.t(f'tl.to("{k}", {{backgroundColor:"#fffdf8", color:"#17262b", scale:1, duration:0.2}}, {t + 0.16:.2f});')
            c.t(f'tl.set("#{sid}", {{opacity:1}}, {t + 0.05:.2f});')
            if prev: c.t(f'tl.set("#{prev}", {{opacity:0}}, {t + 0.05:.2f});')
            prev = sid
            if i == at_i:
                notes.append(f'<div class="note" id="nt{w}" data-layout-allow-overlap>{note}</div>')
                c.t(f'tl.fromTo("#nt{w}", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.25}}, {t + 0.1:.2f});')
            t += 0.5
        # done: the vowelled word, said
        c.t(f'tl.to("#ken", {{scale:0.9, duration:0.08, yoyo:true, repeat:1}}, {t:.2f});')
        did = f"dn{w}"
        states.append(f'<div class="st done" id="{did}" data-layout-allow-overlap><span lang="ar">{e(voc)}</span><i>{e(en)} ✓</i></div>')
        c.t(f'tl.set("#{prev}", {{opacity:0}}, {t + 0.15:.2f});')
        pop(c, f"#{did}", t + 0.15, 1.3)
        d = say(c, voc, t + 0.25); t += 0.25 + max(d, 0.8) + 0.6
        hide(c, f"#{did}", t, 0.2); hide(c, f"#nt{w}", t, 0.2)
        t += 0.3
    c.t(f'tl.fromTo(".end", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.35}}, {t - 0.1:.2f});')
    t += 2.3
    body = ('      <div class="hook">Arabic letters <b>change shape</b> as you type ⌨️</div>'
            f'<div class="phone"><div class="nbar">Notes</div><div class="fld">{"".join(states)}</div>'
            f'{"".join(notes)}<div class="end">Same letter, new shape: <b>it’s all about who it holds hands with</b> 🤝</div>'
            f'<div class="kb">{rows}</div></div>')
    c.write(body, round(t, 2))

# ---------------------------------------------------------------- m06: opposites ping-pong
PG_CSS = """
#root { --bgd:#111417; }
.court { position:absolute; top:470px; left:60px; right:60px; height:1300px; border:6px solid rgba(241,236,224,.25); border-radius:30px; }
.net { position:absolute; top:646px; left:20px; right:20px; border-top:8px dashed rgba(241,236,224,.25); }
.pad { position:absolute; left:0; width:230px; height:34px; border-radius:17px; background:var(--paper); }
.ball { position:absolute; left:0; top:0; width:56px; height:56px; border-radius:50%; background:#f2c14e; box-shadow:0 0 30px 8px rgba(242,193,78,.55); }
.wd { position:absolute; left:0; right:0; text-align:center; opacity:0; }
.wd .ar { font-size:140px; line-height:1.5; color:var(--paper); }
.wd i { display:block; font-style:normal; font-family:var(--ut); font-size:44px; color:#9fb8b2; margin-top:4px; }
.rally { position:absolute; top:410px; left:0; right:0; text-align:center; font-family:var(--ut); font-size:36px; color:#9fb8b2; }
.end { position:absolute; top:880px; left:60px; right:60px; text-align:center; font-size:70px; font-weight:700; line-height:1.15; color:var(--paper); opacity:0; }
.end b { color:#f2c14e; }
"""
PAIRS = [("كَبِير", "big", "kabīr", "صَغِير", "small", "ṣaghīr"), ("حارّ", "hot", "ḥārr", "بارِد", "cold", "bārid"),
         ("طَويل", "tall", "ṭawīl", "قَصِير", "short", "qaṣīr")]

def m06():
    c = comp("m06-pong", "OPPOSITES PING-PONG", PG_CSS, dark=True)
    TOPY, BOTY = 60, 1206                                         # ball top at the top / bottom paddle (court coords)
    xs = [480, 760, 160, 700, 300, 820, 420]                     # ball centre x at each hit (court coords, 960 wide)
    c.t(f'tl.set(".ball", {{x:{xs[0] - 28}, y:{(TOPY + BOTY) // 2}}}, 0);')
    c.t(f'tl.set("#pt", {{x:{xs[0] - 115}}}, 0); tl.set("#pb", {{x:{xs[0] - 115}}}, 0);')
    words, t, hit = [], 0.5, 1
    for p, (a, ae, at_, b, be, bt) in enumerate(PAIRS):
        words.append(f'<div class="wd" id="wb{p}" style="top:820px" data-layout-allow-overlap><div class="ar" lang="ar">{e(a)}</div><i>{e(ae)} · {e(at_)}</i></div>')
        words.append(f'<div class="wd" id="wt{p}" style="top:200px" data-layout-allow-overlap><div class="ar" lang="ar">{e(b)}</div><i>{e(be)} · {e(bt)}</i></div>')
        for side, word, wid, pad, y in (("b", a, f"#wb{p}", "#pb", BOTY), ("t", b, f"#wt{p}", "#pt", TOPY)):
            x = xs[hit % len(xs)]; leg = 0.75
            c.t(f'tl.to(".ball", {{x:{x - 28}, y:{y}, duration:{leg}, ease:"none"}}, {t:.2f});')
            c.t(f'tl.to("{pad}", {{x:{x - 115}, duration:{leg * 0.8:.2f}, ease:"power2.out"}}, {t + 0.05:.2f});')
            t += leg
            c.t(f'tl.fromTo("{pad}", {{scaleX:1.25, scaleY:0.6}}, {{scaleX:1, scaleY:1, duration:0.35, ease:"elastic.out(1, 0.4)", immediateRender:false}}, {t:.2f});')
            pop(c, wid, t, 1.6, 0.3)
            c.t(f'tl.fromTo("{wid} .ar", {{color:"#f2c14e"}}, {{color:"#f1ece0", duration:0.8, immediateRender:false}}, {t:.2f});')
            c.t(f'tl.set("#r{hit - 1}", {{opacity:0}}, {t:.2f}); tl.set("#r{hit}", {{opacity:1}}, {t:.2f});')
            d = say(c, word, t + 0.02); t += max(d, 0.55) - 0.05; hit += 1
        hide(c, f"#wb{p}", t - 0.1); hide(c, f"#wt{p}", t - 0.1)
        t += 0.1
    c.t(f'tl.to(".ball", {{x:{430}, y:{(TOPY + BOTY) // 2}, duration:0.5, ease:"power2.out"}}, {t:.2f});')
    c.t(f'tl.fromTo(".end", {{opacity:0, scale:0.8}}, {{opacity:1, scale:1, duration:0.4, ease:"back.out(2)"}}, {t + 0.2:.2f});')
    t += 2.7
    rally = "".join(f'<span id="r{i}" style="position:absolute; left:0; right:0; opacity:{1 if i == 0 else 0}" data-layout-allow-overlap>RALLY {i}</span>' for i in range(hit))
    body = ('      <div class="hook">Arabic <b>opposites</b> ping-pong 🏓</div>'
            f'<div class="rally">{rally}</div>'
            f'<div class="court"><div class="net"></div>{"".join(words)}<div class="pad" id="pt" style="top:20px"></div><div class="pad" id="pb" style="top:1246px"></div>'
            '<div class="ball" data-layout-allow-overlap></div></div>'
            '<div class="end">Which pair should I <b>serve next</b>? 👇</div>')
    c.write(body, round(t, 2))

# ---------------------------------------------------------------- m07: Arabic Wordle
WD_CSS = """
#root { --bgd:#121213; }
.hint3 { position:absolute; top:430px; left:0; right:0; text-align:center; font-size:44px; font-weight:700; color:#9fb8b2; }
.grid3 { position:absolute; top:520px; left:0; right:0; display:flex; flex-direction:column; align-items:center; gap:18px; }
.wr { display:flex; flex-direction:row-reverse; gap:18px; }
.tl3 { width:210px; height:210px; box-sizing:border-box; border:6px solid #3a3a3c; display:grid; place-items:center; }
.tl3 span { font-family:var(--ar); font-weight:700; font-size:120px; line-height:1; color:#fff; margin-top:-24px; opacity:0; }
.lab { position:absolute; left:0; right:0; text-align:center; font-size:52px; font-weight:700; color:var(--paper); opacity:0; }
.lab .ar { color:#f2c14e; }
.cd3 { position:absolute; top:1340px; left:0; right:0; height:200px; }
.cd3 span { position:absolute; left:0; right:0; text-align:center; font-family:var(--ut); font-size:150px; line-height:200px; color:#f2c14e; opacity:0; }
.yt { position:absolute; top:1250px; left:0; right:0; text-align:center; font-size:56px; font-weight:700; color:var(--paper); opacity:0; }
.end { position:absolute; top:1560px; left:60px; right:60px; text-align:center; font-size:52px; font-weight:700; line-height:1.2; color:var(--paper); opacity:0; }
"""
GREEN, YEL, GREY = "#538d4e", "#b59f3b", "#3a3a3c"
GUESS = [("باب", "باب", "door", "bāb", [GREEN, GREY, GREY]), ("بنت", "بِنْت", "girl", "bint", [GREEN, GREY, GREEN]),
         ("بيت", "بَيْت", "house", "bayt", [GREEN, GREEN, GREEN])]

def m07():
    c = comp("m07-wordle", "ARABIC WORDLE", WD_CSS, dark=True)
    rows, labs, t = [], [], 0.6
    for r, (bare, voc, en, tr, cols) in enumerate(GUESS):
        rows.append('<div class="wr">' + "".join(f'<div class="tl3" id="t{r}{k}"><span lang="ar">{ch}</span></div>' for k, ch in enumerate(bare)) + '</div>')
        if r == 2:                                                # your turn: 3-2-1
            c.t(f'tl.fromTo(".yt", {{opacity:0, scale:1.4}}, {{opacity:1, scale:1, duration:0.3, ease:"back.out(2)"}}, {t:.2f});')
            for n in range(3):
                c.t(f'tl.fromTo(".cd3 span:nth-child({n + 1})", {{opacity:0, scale:1.6}}, {{opacity:1, scale:1, duration:0.2}}, {t + 0.4 + n * 0.8:.2f});')
                c.t(f'tl.to(".cd3 span:nth-child({n + 1})", {{opacity:0, duration:0.1}}, {t + 0.4 + n * 0.8 + 0.68:.2f});')
            t += 0.4 + 2.4
            hide(c, ".yt", t - 0.2)
        for k in range(3):                                        # type the guess in
            c.t(f'tl.to("#t{r}{k} span", {{opacity:1, duration:0.05}}, {t + k * 0.16:.2f});')
            c.t(f'tl.fromTo("#t{r}{k}", {{scale:1.12, borderColor:"#565758"}}, {{scale:1, borderColor:"#565758", duration:0.15, immediateRender:false}}, {t + k * 0.16:.2f});')
        t += 0.6
        for k in range(3):                                        # flip, colour
            at = t + k * 0.28
            c.t(f'tl.to("#t{r}{k}", {{rotationX:90, duration:0.14, ease:"power1.in"}}, {at:.2f});')
            c.t(f'tl.set("#t{r}{k}", {{backgroundColor:"{cols[k]}", borderColor:"{cols[k]}"}}, {at + 0.14:.2f});')
            c.t(f'tl.to("#t{r}{k}", {{rotationX:0, duration:0.14, ease:"power1.out"}}, {at + 0.15:.2f});')
        t += 0.28 * 3 + 0.1
        win = r == 2
        if win:
            for k in range(3):
                c.t(f'tl.to("#t{r}{k}", {{keyframes:[{{y:-40, duration:0.14}}, {{y:0, duration:0.14}}]}}, {t + k * 0.1:.2f});')
            labs.append(burst(c, "wv", 540, 1060, t + 0.1, n=34, spread=480, seed=9, colors=[GREEN, "#f2c14e", "#fff", "#b4322a"]))
        labs.append(f'<div class="lab" id="lb{r}" style="top:{1240 if not win else 1250}px" data-layout-allow-overlap>'
                    f'<span class="ar" lang="ar">{e(voc)}</span> = {e(en)} {"✅" if win else "❌"}</div>')
        c.t(f'tl.fromTo("#lb{r}", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.25}}, {t:.2f});')
        d = say(c, voc, t + 0.1); t += 0.1 + max(d, 0.7) + 0.5
        if not win: hide(c, f"#lb{r}", t - 0.2)
    c.t(f'tl.fromTo(".end", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.35}}, {t:.2f});')
    t += 2.4
    body = ('      <div class="hook">Arabic Wordle 🟩 <b>Can you get it in 3?</b></div>'
            '<div class="hint3">Hint: everyone needs one 🏠</div>'
            f'<div class="grid3">{"".join(rows)}</div>' + "".join(labs) +
            '<div class="yt">Your turn! Guess it 👇</div><div class="cd3">' + "".join(f'<span data-layout-allow-overlap>{n}</span>' for n in (3, 2, 1)) + '</div>'
            '<div class="end">Got it before me? Comment your guess 👇</div>')
    c.write(body, round(t, 2))

# ---------------------------------------------------------------- m08: Day 1 vs Day 30
D1_CSS = """
.pan { position:absolute; left:40px; right:40px; border-radius:44px; overflow:hidden; }
.p1 { top:430px; height:620px; background:#e6dccb; }
.p2 { top:1080px; height:640px; background:#fffdf8; border:4px solid rgba(23,38,43,.1); }
.tag { position:absolute; top:28px; left:40px; font-family:var(--ut); font-size:40px; letter-spacing:.08em; color:var(--ink-soft); }
.tag b { font-family:var(--la); }
.sent { position:absolute; top:150px; left:30px; right:30px; text-align:center; direction:rtl; font-family:var(--ar); font-weight:700; font-size:84px; line-height:1.6; color:var(--ink); }
.p1 .sent { filter:blur(7px); color:#6c6250; }
.sent span { display:inline-block; margin:0 10px; }
.q { position:absolute; font-size:90px; font-weight:700; color:var(--rubric); opacity:0; }
.th { position:absolute; bottom:40px; left:0; right:0; text-align:center; font-size:46px; font-weight:700; color:var(--ink-soft); opacity:0; }
.en { position:absolute; bottom:50px; left:40px; right:40px; text-align:center; font-size:46px; font-weight:700; color:var(--ink); opacity:0; }
.p2 .sent span { color:rgba(23,38,43,.25); }
.cta { position:absolute; top:1750px; left:40px; right:40px; text-align:center; font-size:44px; font-weight:700; color:var(--verdigris); opacity:0; }
"""
SENT = "اسْمِي يُوسُفُ. وَأَنْتَ، ما اسْمُكَ؟"

def m08():
    c = comp("m08-day1", "DAY 1 VS DAY 30", D1_CSS)
    words = SENT.split()
    spans = "".join(f'<span id="w{i}">{e(w)}</span>' for i, w in enumerate(words))
    spans1 = "".join(f'<span id="x{i}">{e(w)}</span>' for i, w in enumerate(words))
    # Day 1: the letters swim and question marks pop
    r = random.Random(5)
    for i in range(len(words)):
        c.t(f'tl.to("#x{i}", {{rotation:{r.choice([-8, 8])}, y:{r.choice([-14, 14])}, duration:0.35, repeat:9, yoyo:true, ease:"sine.inOut"}}, {0.2 + i * 0.07:.2f});')
    qs = ""
    for k, (x, y, ch) in enumerate([(80, 120, "?"), (900, 90, "??"), (150, 430, "🤯"), (860, 420, "?"), (500, 60, "😵‍💫")]):
        qs += f'<div class="q{" emo" if ord(ch[0]) > 1000 else ""}" id="q{k}" style="left:{x}px; top:{y}px" data-layout-allow-overlap>{ch}</div>'
        pop(c, f"#q{k}", 0.6 + k * 0.35, 0.3)
    c.t('tl.fromTo(".p1 .th", {opacity:0}, {opacity:1, duration:0.3}, 1.6);')
    # Day 30: the panel slides in, each word lights as it's said
    t = 3.6
    c.t(f'tl.fromTo(".p2", {{opacity:0, y:120}}, {{opacity:1, y:0, duration:0.45, ease:"back.out(1.6)"}}, {t:.2f});')
    t += 0.5
    d = say(c, SENT, t)
    lens = [len(w) for w in words]; tot = sum(lens); acc = 0
    for i, n in enumerate(lens):
        at = t + 0.05 + d * 0.92 * acc / tot; acc += n
        c.t(f'tl.to("#w{i}", {{color:"#2e7263", scale:1.08, duration:0.12}}, {at:.2f}); tl.to("#w{i}", {{scale:1, color:"#17262b", duration:0.25}}, {at + 0.2:.2f});')
    t += d + 0.15
    c.t(f'tl.fromTo(".p2 .en", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.3}}, {t:.2f});')
    t += 1.6
    c.t(f'tl.fromTo(".cta", {{opacity:0}}, {{opacity:1, duration:0.35}}, {t:.2f});')
    t += 2.4
    body = ('      <div class="hook">Day 1 vs Day 30 of <b>learning Arabic</b></div>'
            f'<div class="pan p1"><div class="tag">DAY 1 <b class="emo">😵‍💫</b></div><div class="sent" lang="ar">{spans1}</div>{qs}'
            '<div class="th">“is that… a squiggle?”</div></div>'
            f'<div class="pan p2"><div class="tag">DAY 30 <b class="emo">😎</b></div><div class="sent" lang="ar">{spans}</div>'
            '<div class="en">“My name is Yusuf. And you, what’s your name?”</div></div>'
            '<div class="cta">Day 30 is closer than you think · rafiq-arabic.com</div>')
    c.write(body, round(t, 2))

# ---------------------------------------------------------------- m09: read it before the timer
SP_CSS = """
#root { background:#b4322a; }
#brand b, #kicker { color:#fff7dc; } #brand .tile { background:#fff7dc; } #brand .tile span { color:var(--ink); }
.bgc { position:absolute; inset:0; opacity:0; z-index:0; }
#brand, #kicker { z-index:3; }
.lines { position:absolute; inset:-200px; background:repeating-linear-gradient(115deg, rgba(255,255,255,.07) 0 40px, transparent 40px 120px); }
.hook { color:#fff7dc; } .hook b { color:#ffd76a; }
.spd { position:absolute; top:450px; left:0; right:0; text-align:center; font-family:var(--ut); font-size:46px; color:#fff7dc; }
.spd span { position:absolute; left:0; right:0; opacity:0; }
.wd { position:absolute; top:560px; left:0; right:0; text-align:center; opacity:0; }
.wd .ar { font-size:230px; line-height:1.4; color:#fff; }
.tmr { position:absolute; top:1040px; left:140px; right:140px; height:34px; border-radius:17px; background:rgba(255,255,255,.2); overflow:hidden; }
.tmr i { position:absolute; inset:0; background:#fff7dc; transform-origin:0 50%; transform:scaleX(0); }
.mn { position:absolute; top:1140px; left:0; right:0; text-align:center; font-size:76px; font-weight:700; color:#fff7dc; opacity:0; }
.mn em { font-style:normal; font-weight:500; opacity:.75; }
.end { position:absolute; top:880px; left:60px; right:60px; text-align:center; font-size:76px; font-weight:700; line-height:1.15; color:#fff7dc; opacity:0; }
"""
SPEED = [("باب", "door", "bāb", 2.0, "#b4322a"), ("قَلَم", "pen", "qalam", 1.6, "#2e7263"), ("شاي", "tea", "shāy", 1.2, "#17262b"),
         ("بَحْر", "sea", "baḥr", 0.9, "#6b3fa0"), ("سَيَّارَة", "car", "sayyāra", 0.6, "#c4561c")]

def m09():
    c = comp("m09-speed", "SPEED READING", SP_CSS)
    html, t = [], 0.5
    c.t('tl.fromTo(".lines", {x:0}, {x:-480, duration:20, ease:"none"}, 0);')
    for i, (ar, en, tr, tm, bg) in enumerate(SPEED):
        html.append(f'<div class="bgc" id="bg{i}" style="background:{bg}"></div>')
        html.append(f'<div class="wd" id="wd{i}" data-layout-allow-overlap><div class="ar" lang="ar">{e(ar)}</div></div>')
        html.append(f'<div class="mn" id="mn{i}" data-layout-allow-overlap>{e(en)} <em>· {e(tr)}</em></div>')
        html.append(f'<span id="sp{i}" data-layout-allow-overlap>SPEED x{2.0 / tm:.1f}{" 🔥" * (i >= 3)}</span>')
        if i: c.t(f'tl.fromTo("#bg{i}", {{opacity:0, scale:1.2}}, {{opacity:1, scale:1, duration:0.25}}, {t - 0.1:.2f});')
        c.t(f'tl.fromTo("#sp{i}", {{opacity:0, x:-60}}, {{opacity:1, x:0, duration:0.2}}, {t - 0.1:.2f});')
        if i: hide(c, f"#sp{i - 1}", t - 0.1, 0.1)
        c.t(f'tl.fromTo("#wd{i}", {{opacity:0, scale:0.4, rotation:-8}}, {{opacity:1, scale:1, rotation:0, duration:0.25, ease:"back.out(2.5)"}}, {t:.2f});')
        c.t(f'tl.fromTo(".tmr i", {{scaleX:1}}, {{scaleX:0, duration:{tm}, ease:"none", immediateRender:{"true" if i == 0 else "false"}}}, {t + 0.2:.2f});')
        t += 0.2 + tm
        shake(c, f"#wd{i}", t, 12, 4)
        pop(c, f"#mn{i}", t, 0.5, 0.25)
        d = say(c, ar, t + 0.05); t += max(d, 0.75) + 0.4
        hide(c, f"#wd{i}", t - 0.1, 0.12); hide(c, f"#mn{i}", t - 0.1, 0.12)
    hide(c, f"#sp{len(SPEED) - 1}", t - 0.1, 0.1)
    c.t(f'tl.to(".tmr", {{opacity:0, duration:0.2}}, {t - 0.1:.2f});')
    c.t(f'tl.fromTo(".end", {{opacity:0, scale:0.8}}, {{opacity:1, scale:1, duration:0.4, ease:"back.out(2)"}}, {t:.2f});')
    t += 2.5
    bgs = "".join(h for h in html if 'class="bgc"' in h)
    rest = "".join(h for h in html if 'class="bgc"' not in h and not h.startswith("<span"))
    spd = "".join(h for h in html if h.startswith("<span"))
    body = (f'      {bgs}<div class="lines"></div><div class="hook">Read it <b>before the timer</b> 😤 It gets faster…</div>'
            f'<div class="spd">{spd}</div>{rest}<div class="tmr"><i></i></div>'
            '<div class="end">How many did you read in time? 👇 5/5 = 🔥</div>')
    c.write(body, round(t, 2))

# ---------------------------------------------------------------- m10: heart or dog
HD_CSS = """
.bubble { position:absolute; top:450px; left:90px; right:90px; padding:34px 40px; border-radius:46px; background:var(--ink); color:var(--paper);
  text-align:center; font-size:62px; font-weight:700; line-height:1.2; }
.bubble .ar { font-size:70px; color:#f2c14e; }
.bubble .s { position:absolute; left:0; right:0; top:34px; opacity:0; }
.bubble .s0 { position:relative; top:0; opacity:1; }
.pair { position:absolute; top:760px; left:60px; right:60px; display:flex; flex-direction:row-reverse; gap:40px; }
.pc { flex:1; height:560px; border-radius:46px; background:var(--card); border:4px solid rgba(23,38,43,.13); display:flex; flex-direction:column; align-items:center;
  justify-content:center; box-shadow:0 18px 34px -18px rgba(23,38,43,.45); opacity:0; }
.pc .em { font-size:150px; line-height:1.2; }
.pc .ar { font-size:130px; line-height:1.4; color:var(--ink); }
.pc .ar b { color:var(--rubric); }
.pc i { font-style:normal; font-size:48px; font-weight:700; color:var(--ink-soft); margin-top:-6px; }
.how { position:absolute; top:1370px; left:60px; right:60px; display:flex; flex-direction:row-reverse; gap:40px; }
.how div { flex:1; text-align:center; font-size:40px; font-weight:700; line-height:1.25; color:var(--verdigris); opacity:0; }
.how .ar { display:block; font-size:64px; color:var(--rubric); }
.xx { position:absolute; top:880px; left:200px; font-size:170px; opacity:0; z-index:2; }
.end { position:absolute; top:1620px; left:60px; right:60px; text-align:center; font-size:56px; font-weight:700; opacity:0; }
.hrt { position:absolute; font-size:70px; opacity:0; }
"""

def m10():
    c = comp("m10-heart-dog", "ONE LETTER, BIG DIFFERENCE", HD_CSS)
    t = 0.5
    # the two words
    pop(c, "#pq", t, 0.7); d = say(c, "قَلْب", t + 0.1); t += max(d, 0.8) + 0.45
    pop(c, "#pk", t, 0.7); d = say(c, "كَلْب", t + 0.1); t += max(d, 0.8) + 0.5
    # how they differ
    c.t(f'tl.fromTo(".how div", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.3, stagger:0.2}}, {t:.2f});')
    t += 2.6
    # get it wrong…
    c.t(f'tl.set(".s0", {{opacity:0}}, {t:.2f}); tl.set(".s1", {{opacity:1}}, {t:.2f});')
    shake(c, ".bubble", t + 0.1, 22, 7)
    c.t(f'tl.fromTo(".xx", {{opacity:0, scale:2}}, {{opacity:1, scale:1, duration:0.2}}, {t + 0.1:.2f});')
    c.t(f'tl.to("#pk", {{backgroundColor:"#f3d2cd", duration:0.2}}, {t + 0.1:.2f});')
    d = say(c, "كَلْب", t + 0.15); t += max(d, 0.8) + 0.9
    # …then right
    hide(c, ".xx", t, 0.15)
    c.t(f'tl.set(".s1", {{opacity:0}}, {t:.2f}); tl.set(".s2", {{opacity:1}}, {t:.2f});')
    c.t(f'tl.to("#pk", {{backgroundColor:"#f7f3ea", opacity:0.4, duration:0.25}}, {t:.2f}); tl.to("#pq", {{backgroundColor:"#d9ece5", scale:1.04, duration:0.25}}, {t:.2f});')
    r = random.Random(4); hearts = ""
    for k in range(14):
        hid = f"h{k}"; x0, y0 = r.randint(80, 980), r.randint(1100, 1500)
        hearts += f'<div class="hrt emo" id="{hid}" style="left:{x0}px; top:{y0}px" data-layout-allow-overlap>❤️</div>'
        c.t(f'tl.fromTo("#{hid}", {{opacity:0, y:0, scale:0.4}}, {{opacity:1, y:-{r.randint(250, 600)}, scale:{r.uniform(.8, 1.4):.2f}, duration:1.1, ease:"power2.out"}}, {t + 0.05 * k:.2f});')
        c.t(f'tl.to("#{hid}", {{opacity:0, duration:0.4}}, {t + 0.05 * k + 1.12:.2f});')
    d = say(c, "قَلْب", t + 0.15); t += max(d, 0.8) + 0.7
    c.t(f'tl.fromTo(".end", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.35}}, {t:.2f});')
    t += 2.4
    body = ('      <div class="hook">Say this wrong and you’ll call someone <b>a dog</b> 🐕</div>'
            '<div class="bubble"><div class="s s0">“I love you with all my…”</div>'
            '<div class="s s1" data-layout-allow-overlap>“…with all my <span class="ar" lang="ar">كَلْب</span>” 🐕</div>'
            '<div class="s s2" data-layout-allow-overlap>“…with all my <span class="ar" lang="ar">قَلْب</span>” ❤️</div></div>'
            '<div class="xx emo" data-layout-allow-overlap>❌</div>'
            '<div class="pair"><div class="pc" id="pq"><div class="em emo">❤️</div><div class="ar" lang="ar"><b>قَ</b>لْب</div><i>heart · qalb</i></div>'
            '<div class="pc" id="pk"><div class="em emo">🐕</div><div class="ar" lang="ar"><b>كَ</b>لْب</div><i>dog · kalb</i></div></div>'
            '<div class="how"><div><span class="ar" lang="ar">ق</span>a “k” from deep in the throat</div><div><span class="ar" lang="ar">ك</span>a plain English “k”</div></div>'
            + hearts + '<div class="end">Tag someone who needs this 😂👇</div>')
    c.write(body, round(t, 2))

ALL = {"m01-tetris": m01, "m02-rocket": m02, "m03-swipe": m03, "m04-catch": m04, "m05-typing": m05,
       "m06-pong": m06, "m07-wordle": m07, "m08-day1": m08, "m09-speed": m09, "m10-heart-dog": m10}
if __name__ == "__main__":
    ids = [a for a in sys.argv[1:] if not a.startswith("--")]
    T.LUFS.update({v: -16.0 for v in ALL})
    for vid, fn in ALL.items():
        if ids and vid not in ids: continue
        T.level(vid) if "--level" in sys.argv else fn()
