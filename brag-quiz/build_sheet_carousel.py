#!/usr/bin/env python3
"""Carousels for the week of 21 Nov 2026 (#395), at TikTok's 9:16. Never the pastel page (owner, 10 Nov 2026; FORMATS.md): our colours,
light (paper: cream, ink, rubric red, a warm light from the top, grain, cards with real shadows) or dark (deep teal lit from the top,
gold Arabic with a soft glow, cream text, grain), Amiri for the Arabic, Instrument Serif for titles, Karla for the rest.

  dots       Same shape, different dots: the nine letter families (the alphabet series; ink letters, red dots)
  join       The 6 letters that never join the next one, with a "count the pieces" quiz on رَبَّنا وَلَكَ الْحَمْدُ
  starter    The reading starter as it is on the live site (screens from main, stills/starter-screens/), free week, link in bio
  this-that  هَذا هَذِهِ ذَلِكَ تِلْكَ: this and that for a he and a she (the course's own sentences, al-Baqarah 2:2, Yūnus 10:1)
  khutbah    The words that open the khutbah (khuṭbat al-ḥājah, an-Nasāʾī 1404), word by word: it's all "we"
  salah      Your salah cheat sheet: what you say in each position, word by word (salah-data.js)

  python3 brag-quiz/build_sheet_carousel.py [set ...]   ->   brag-quiz/stills/<set>-tiktok/<set>-01.jpg ... (1080 x 1920)
"""
import os, re, sys
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
F = os.path.join(HERE, "fonts"); F6 = os.path.join(ROOT, "brag-output-v6/composition/assets/fonts")
W, H = 1080, 1920
INK, SOFT, RED, TEAL, GOLD, CREAM = "#17262B", "#5C6B6E", "#B4322A", "#2E7263", "#E9B949", "#F1ECE0"

GRAIN = ("url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' "
         "baseFrequency='.9' numOctaves='3' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .55 0'/></filter>"
         "<rect width='300' height='300' filter='url(%23n)'/></svg>\")")

CSS = f"""
@font-face {{ font-family:AM; src:url('file://{F}/amiri-arabic-700-normal.woff2'); }}
@font-face {{ font-family:IS; src:url('file://{F}/instrument-serif-latin-400-normal.woff2'); }}
@font-face {{ font-family:KA; src:url('file://{F6}/karla-latin-500-normal.woff2'); font-weight:500; }}
@font-face {{ font-family:KA; src:url('file://{F6}/karla-latin-700-normal.woff2'); font-weight:700; }}
* {{ box-sizing:border-box; margin:0; }}
body {{ width:{W}px; height:{H}px; overflow:hidden; font-family:KA, sans-serif; }}
.slide {{ position:relative; width:{W}px; height:{H}px; overflow:hidden; }}
.slide::after {{ content:""; position:absolute; inset:0; background-image:{GRAIN}; opacity:.07; pointer-events:none; mix-blend-mode:multiply; }}
.light {{ background:radial-gradient(ellipse 130% 60% at 35% -5%, #fffdf6 0%, #f6f1e4 38%, {CREAM} 62%, #e3d8c2 100%); color:{INK}; }}
.light::before {{ content:""; position:absolute; inset:0; background:linear-gradient(115deg, rgba(255,250,235,.55) 0%, rgba(255,250,235,0) 38%),
                 radial-gradient(ellipse 90% 50% at 50% 115%, rgba(23,38,43,.16), rgba(23,38,43,0)); pointer-events:none; }}
.dark {{ background:radial-gradient(ellipse 120% 62% at 50% -8%, #2c4d55 0%, #1a3038 34%, #14232a 60%, #0a1418 100%); color:{CREAM}; }}
.dark::before {{ content:""; position:absolute; inset:0; background:radial-gradient(ellipse 70% 30% at 50% 0%, rgba(233,185,73,.16), rgba(233,185,73,0)); pointer-events:none; }}
.dark::after {{ mix-blend-mode:screen; opacity:.05; }}
.top {{ position:absolute; left:80px; right:80px; top:96px; display:flex; align-items:center; gap:18px; font-weight:700; font-size:30px; letter-spacing:.2em; }}
.logo {{ width:58px; height:58px; border-radius:14px; display:flex; align-items:center; justify-content:center; font-family:AM; font-size:38px; padding-bottom:8px; }}
.light .logo {{ background:{INK}; color:{CREAM}; box-shadow:0 6px 14px rgba(23,38,43,.22); }} .dark .logo {{ background:{GOLD}; color:#14232a; }}
.light .top {{ color:{SOFT}; }} .dark .top {{ color:#c9b98f; }}
.bgl {{ position:absolute; font-family:AM; font-size:1200px; line-height:1; right:-160px; bottom:-120px; transform:rotate(-8deg); pointer-events:none; }} .light .bgl {{ color:rgba(23,38,43,.035); text-shadow:2px 3px 0 rgba(255,255,255,.7); }} .dark .bgl {{ color:rgba(233,185,73,.045); }}
.top .pg {{ margin-left:auto; letter-spacing:.08em; }}
.body {{ position:absolute; left:70px; right:70px; top:210px; bottom:320px; z-index:1; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; gap:34px; }}
.k {{ font-weight:700; font-size:34px; letter-spacing:.2em; }} .light .k {{ color:{RED}; }} .dark .k {{ color:{GOLD}; }}
.t {{ font-family:IS; font-size:132px; line-height:1.0; letter-spacing:-.01em; }}
.t2 {{ font-family:IS; font-size:100px; line-height:1.04; }}
.s {{ font-size:48px; line-height:1.36; font-weight:500; max-width:880px; }} .light .s {{ color:{SOFT}; }} .dark .s {{ color:#d9d2bf; }}
.s b {{ font-weight:700; }} .light .s b {{ color:{INK}; }} .dark .s b {{ color:{CREAM}; }}
.ar {{ font-family:AM; direction:rtl; unicode-bidi:isolate; line-height:1.55; }}
.r {{ color:{RED}; }} .dark .r {{ color:#ff8a72; }} .g {{ color:{GOLD}; }} .light .g {{ color:#a8842c; }} .tl {{ color:{TEAL}; }} .dark .tl {{ color:#7fd0bd; }}
.card {{ width:100%; border-radius:34px; padding:34px 40px; display:flex; flex-direction:column; align-items:center; gap:10px; }}
.light .card {{ background:linear-gradient(180deg, #fffdf7, #faf6ec); box-shadow:0 2px 0 rgba(255,255,255,.9) inset, 0 34px 70px -18px rgba(23,38,43,.28), 0 6px 18px rgba(23,38,43,.08); }}
.dark .card {{ background:linear-gradient(180deg, rgba(241,236,224,.075), rgba(241,236,224,.03)); border:1.5px solid rgba(233,185,73,.32);
              box-shadow:0 30px 70px -20px rgba(0,0,0,.6), 0 0 0 1px rgba(0,0,0,.2) inset; }}
.dark .glow {{ text-shadow:0 0 40px rgba(233,185,73,.45), 0 0 6px rgba(233,185,73,.4); color:{GOLD}; }}
.st {{ position:relative; display:inline-block; font-family:AM; }} .st .d {{ color:{RED}; }} .st .b {{ position:absolute; inset:0; }}
.fam {{ display:flex; justify-content:center; gap:46px; direction:rtl; }}
.fam .col {{ display:flex; flex-direction:column; align-items:center; }}
.fam .st {{ font-size:230px; line-height:1.45; }} .fam .nm, .fam .snd {{ direction:ltr; unicode-bidi:isolate; }}
.nm {{ font-weight:700; font-size:54px; margin-top:-10px; }} .snd {{ font-size:40px; margin-top:6px; max-width:330px; line-height:1.25; }} .light .snd {{ color:{SOFT}; }} .dark .snd {{ color:#cfc6ae; }}
.rule {{ font-size:50px; font-weight:700; line-height:1.3; }}
.note {{ font-size:40px; line-height:1.4; }} .light .note {{ color:{SOFT}; }} .dark .note {{ color:#cfc6ae; }}
.chips {{ display:flex; justify-content:center; gap:22px; direction:rtl; flex-wrap:wrap; }}
.chip {{ display:flex; flex-direction:column; align-items:center; padding:18px 26px 22px; border-radius:24px; min-width:200px; }}
.light .chip {{ background:#fff; box-shadow:0 14px 30px -12px rgba(23,38,43,.3); }} .dark .chip {{ background:rgba(241,236,224,.07); border:1px solid rgba(233,185,73,.28); }}
.chip .ar {{ font-size:84px; line-height:1.5; }} .chip span {{ font-size:36px; font-weight:700; direction:ltr; }}
.pieces {{ display:flex; justify-content:center; gap:16px; direction:rtl; flex-wrap:wrap; }}
.pc {{ font-family:AM; font-size:92px; line-height:1.5; padding:0 22px 10px; border-radius:22px; position:relative; }}
.light .pc {{ background:#fff; box-shadow:0 12px 26px -12px rgba(23,38,43,.3); }}
.pc i {{ position:absolute; top:10px; left:12px; font-family:KA; font-style:normal; font-size:24px; font-weight:700; color:{RED}; }}
.opts {{ display:grid; grid-template-columns:1fr 1fr; gap:26px; width:100%; }}
.opt {{ position:relative; border-radius:30px; padding:20px 0 26px; font-family:AM; font-size:150px; line-height:1.4; }}
.light .opt {{ background:#fff; box-shadow:0 18px 36px -14px rgba(23,38,43,.32); }}
.opt b {{ position:absolute; left:24px; top:18px; font-family:KA; font-size:36px; color:{RED}; }}
.phone {{ width:530px; border-radius:66px; padding:16px; background:linear-gradient(160deg, #2a3a40, #0f1a1d); box-shadow:0 50px 90px -30px rgba(23,38,43,.55), 0 0 0 2px #3b4c52 inset; }}
.phone img {{ width:100%; display:block; border-radius:48px; }}
.ask {{ font-family:IS; font-size:92px; line-height:1.08; }}
.swipe {{ font-weight:700; font-size:38px; letter-spacing:.08em; }} .light .swipe {{ color:{TEAL}; }} .dark .swipe {{ color:{GOLD}; }}
hr.l {{ width:120px; border:0; height:4px; border-radius:2px; }} .light hr.l {{ background:{RED}; }} .dark hr.l {{ background:{GOLD}; }}
"""

def stack(letter, base, size=None):
    """A letter with its dots in red: the dotted letter in red, the same shape without dots in ink on top (Amiri)."""
    st = f' style="font-size:{size}px"' if size else ""
    return f'<span class="st"{st}><span class="d">{letter}</span><span class="b">{base}</span></span>'

MARKS = re.compile("[ً-ٰٟۖ-ۭ]")
NONJOIN = set("اأإآٱدذرزوؤةءى")
def pieces(word):
    """A word split where its letters don't join: after ا د ذ ر ز و (and ة, ى at the end), and around ء. Vowel marks stay with their letter."""
    out, cur = [], ""
    for ch in word:
        if MARKS.match(ch): cur += ch; continue
        if cur and (ch == "ء" or (MARKS.sub("", cur)[-1:] in NONJOIN)): out.append(cur); cur = ""
        cur += ch
    if cur: out.append(cur)
    return out

def top(kicker, i, n, theme):
    return f'<div class="top"><span class="logo">ر</span><span>RAFIQ · {kicker}</span><span class="pg">{i}/{n}</span></div>'

WM = "ع"   # the watermark letter behind the slides (each set sets its own)
def page(theme, kicker, inner, i, n):
    return f'<div class="slide {theme}"><div class="bgl">{WM}</div>{top(kicker, i, n, theme)}<div class="body">{inner}</div></div>'

A = lambda w, cls="", size=None: f'<span class="ar {cls}"' + (f' style="font-size:{size}px"' if size else "") + f'>{w}</span>'

# ---------------------------------------------------------------- dots
FAMS = [  # (letter, dotless base, name, sound)
    [("ب", "ٮ", "bāʾ", "b"), ("ت", "ٮ", "tāʾ", "t"), ("ث", "ٮ", "thāʾ", "th, as in “think”")],
    [("ج", "ح", "jīm", "j"), ("ح", "ح", "ḥāʾ", "a breathy h"), ("خ", "ح", "khāʾ", "kh, as in “loch”")],
    [("د", "د", "dāl", "d"), ("ذ", "د", "dhāl", "th, as in “this”")],
    [("ر", "ر", "rāʾ", "r"), ("ز", "ر", "zāy", "z")],
    [("س", "س", "sīn", "s"), ("ش", "س", "shīn", "sh")],
    [("ص", "ص", "ṣād", "a heavy s"), ("ض", "ص", "ḍād", "a heavy d")],
    [("ط", "ط", "ṭāʾ", "a heavy t"), ("ظ", "ط", "ẓāʾ", "a heavy th")],
    [("ع", "ع", "ʿayn", "a squeeze in the throat"), ("غ", "ع", "ghayn", "like gargling")],
    [("ف", "ڡ", "fāʾ", "f"), ("ق", "ٯ", "qāf", "a k, further back")],
]
def fam(f, size=280):
    return '<div class="fam">' + "".join(f'<div class="col">{stack(l, b, size)}<div class="nm">{n}</div><div class="snd">{s}</div></div>' for l, b, n, s in f) + '</div>'

def dots():
    global WM; WM = "ح"
    K, n = "THE ALPHABET", 9
    S = []
    S.append(f'<div class="k">LEARN TO READ ARABIC</div><div class="t">Same shape.<br>Different dots.</div>'
             f'<div class="fam" style="gap:40px">{"".join(stack(l, b, 300) for l, b, *_ in FAMS[0])}</div>'
             '<div class="s"><b>20 of the 28 Arabic letters</b> share their shape with another letter. Only the dots tell them apart.</div>'
             '<div class="swipe">SWIPE FOR ALL 9 FAMILIES →</div>')
    S.append(f'<div class="k">FAMILY 1</div>{fam(FAMS[0])}<hr class="l"><div class="rule">One dot below · two on top · three on top</div>'
             '<div class="note">At the start of a word, two more letters take this shape:</div>'
             f'<div class="ar" style="font-size:110px;letter-spacing:.1em">{A("نـ · يـ")}</div>')
    S.append(f'<div class="k">FAMILY 2</div>{fam(FAMS[1])}<hr class="l"><div class="rule">A dot below · no dot · a dot on top</div>')
    for k, (a, b, lab) in enumerate([(2, 3, "Add one dot on top"), (4, 5, "Three dots · and one dot on top"), (6, 7, "Add one dot on top")]):
        S.append(f'<div class="k">FAMILIES {3 + 2 * k} AND {4 + 2 * k}</div>{fam(FAMS[a], 230)}{fam(FAMS[b], 230)}<hr class="l"><div class="rule">{lab}</div>')
    S.append(f'<div class="k">FAMILY 9</div>{fam(FAMS[8])}<hr class="l"><div class="rule">One dot · two dots</div>'
             '<div class="note">At the end of a word their tails differ a little. At the start and in the middle, only the dots do.</div>')
    S.append('<div class="k">YOUR TURN</div><div class="t2">Which one is <span class="r">khāʾ</span>?</div><div class="opts">'
             + "".join(f'<div class="opt"><b>{i}</b><span class="ar">{l}</span></div>' for i, l in enumerate(["ج", "ح", "خ", "غ"], 1))
             + '</div><div class="s">Comment <b>1, 2, 3 or 4</b> 👇</div>')
    S.append('<div class="k">SAVE THIS 📌</div><div class="ask">Read it again<br>the next time you open the Qur’an.</div>'
             f'<div class="fam" style="gap:30px">{"".join(stack(l, b, 170) for l, b, *_ in FAMS[1])}</div>'
             '<div class="s">Send it to someone learning to read Arabic, and follow for the next part: <b>the letters that never join.</b></div>')
    return [page("light", K, s, i + 1, n) for i, s in enumerate(S)]

# ---------------------------------------------------------------- join
def word_red(w):
    """The word with its non-joining letters in red (colour spans keep the joins in Chrome)."""
    out = ""
    for ch in w: out += f'<span class="r">{ch}</span>' if ch in NONJOIN else ch
    return out.replace('</span><span class="r">', "")

def pc_row(ws, numbered=False):
    ps = [p for w in ws for p in pieces(w)]
    return '<div class="pieces">' + "".join(f'<span class="pc">{f"<i>{k}</i>" if numbered else ""}{p}</span>' for k, p in enumerate(ps, 1)) + '</div>', len(ps)

def join():
    global WM; WM = "و"
    K, n = "THE ALPHABET", 9
    S = []
    S.append('<div class="k">LEARN TO READ ARABIC</div><div class="t">6 letters that<br>never join<br>the next one</div>'
             f'<div class="ar" style="font-size:190px;letter-spacing:.12em">{A("ا د ذ ر ز و")}</div>'
             '<div class="s">That’s why Arabic words have <b>little gaps</b> in them.</div><div class="swipe">SWIPE TO SPOT THEM →</div>')
    row, k = pc_row(["دِين"])
    S.append('<div class="k">THE RULE</div><div class="t2">Most letters join<br>on both sides.</div>'
             '<div class="s">These six join the letter <b>before</b> them, never the letter <b>after</b>.</div>'
             f'<div class="card"><div class="ar" style="font-size:150px">{word_red("دِين")}</div><div class="note">dīn · religion</div>{row}'
             f'<div class="note">One word, {k} pieces</div></div>')
    for lab, items in [("<bdi>ا</bdi> · ALIF", [("اللَّهُ أَكْبَرُ", "Allāhu akbar"), ("سَلام", "salām · peace")]),
                       ("<bdi>د ذ</bdi> · DĀL AND DHĀL", [("دِين", "dīn · religion"), ("ذِكْر", "dhikr · remembrance")]),
                       ("<bdi>ر ز</bdi> · RĀʾ AND ZĀY", [("رَحْمَة", "raḥmah · mercy"), ("زَمْزَم", "zamzam")]),
                       ("<bdi>و</bdi> · WĀW", [("وُضُوء", "wuḍūʾ"), ("نُور", "nūr · light")])]:
        cards = ""
        for w, en in items:
            row, k = pc_row(w.split())
            cards += f'<div class="card"><div class="ar" style="font-size:130px">{word_red(w)}</div><div class="note">{en}</div>{row}<div class="note">{k} pieces</div></div>'
        S.append(f'<div class="k">{lab}</div>{cards}' + ('<div class="note">Every red letter ends a piece.</div>' if lab.endswith("ALIF") else ""))
    line = "رَبَّنا وَلَكَ الْحَمْدُ"
    S.append('<div class="k">YOUR TURN</div><div class="t2">Count the pieces</div>'
             f'<div class="card"><div class="ar" style="font-size:140px">{line}</div><div class="note">You say it every time you rise from rukūʿ.</div></div>'
             '<div class="s">How many separate pieces? <b>Comment your number</b> 👇 then swipe.</div>')
    row, k = pc_row(line.split(), True)
    row = row.replace('class="pieces"', 'class="pieces" style="gap:10px"').replace('class="pc"', 'class="pc" style="font-size:72px;padding:0 14px 6px"')
    S.append(f'<div class="k">THE ANSWER</div><div class="t2"><span class="r">{k}</span> pieces</div>'
             f'<div class="card"><div class="ar" style="font-size:130px">{word_red(line)}</div>{row}</div>'
             '<div class="s">Every red letter ends a piece. Did you get it?</div>')
    S.append('<div class="k">SAVE THIS 📌</div><div class="ask">Six letters.<br>Now you’ll see the gaps everywhere.</div>'
             f'<div class="ar" style="font-size:150px;letter-spacing:.1em">{A("ا د ذ ر ز و", "r")}</div>'
             '<div class="s">Send it to someone learning to read Arabic 🤍</div>')
    return [page("light", K, s, i + 1, n) for i, s in enumerate(S)]

# ---------------------------------------------------------------- starter (the one post in five that shows the app)
def starter():
    global WM; WM = "ب"
    K, n = "READING ARABIC", 6
    import base64
    shot = lambda f: ('<div class="phone"><img src="data:image/jpeg;base64,'
                      + base64.b64encode(open(os.path.join(HERE, "stills/starter-screens", f), "rb").read()).decode() + '"></div>')
    S = ['<div class="k">CAN’T READ ARABIC YET?</div><div class="t">Learn the letters<br>a few minutes<br>a day</div>'
         f'<div class="ar" style="font-size:120px;letter-spacing:.08em">{A("ا ب ت ث ج ح خ")}</div>'
         '<div class="s">Rafiq’s reading starter takes you from the first letter to reading words, <b>in small groups</b>.</div>'
         '<div class="swipe">SWIPE TO SEE IT →</div>',
         f'<div class="k">ALL 28 LETTERS</div>{shot("s1-intro.jpg")}<div class="s">Tap any letter to hear its name.</div>',
         f'<div class="k">MEET EACH LETTER</div>{shot("s2-meet.jpg")}<div class="s">Its sound, its shapes, and real words you can tap to hear.</div>',
         f'<div class="k">CHECK YOURSELF</div>{shot("s3-check.jpg")}<div class="s">Then a quick check, so it sticks.</div>',
         f'<div class="k">ONE STEP AT A TIME</div>{shot("s4-home.jpg")}<div class="s">Home shows your next step. About 5 minutes each.</div>',
         '<div class="k">TRY IT FREE</div><div class="ask">Your first letters,<br>today.</div>'
         f'<div class="ar" style="font-size:150px">{A("رَفِيق", "")}</div>'
         '<div class="s"><b>Free for a week, no card.</b><br>Link in bio 🔗</div>']
    return [page("light", K, s, i + 1, n) for i, s in enumerate(S)]

# ---------------------------------------------------------------- this / that
def this_that():
    global WM; WM = "ه"
    K, n = "ARABIC GRAMMAR", 9
    big = lambda w, en, gender, sent, sen, src: (
        f'<div class="ar" style="font-size:220px;line-height:1.35">{w}</div><div class="t2">{en}</div><div class="k" style="color:{TEAL}">{gender}</div>'
        f'<div class="card"><div class="ar" style="font-size:96px">{sent}</div><div class="note" style="color:{INK};font-size:36px;font-weight:700">{sen}</div>'
        + (f'<div class="note">{src}</div>' if src else "") + '</div>')
    S = ['<div class="k">ARABIC GRAMMAR</div><div class="t">“This” and “that”<br>have a he<br>and a she</div>'
         f'<div class="chips"><div class="chip">{A("هَذا")}<span>this · he</span></div><div class="chip">{A("هَذِهِ")}<span>this · she</span></div>'
         f'<div class="chip">{A("ذَلِكَ")}<span>that · he</span></div><div class="chip">{A("تِلْكَ")}<span>that · she</span></div></div>'
         '<div class="swipe">SWIPE TO LEARN ALL 4 →</div>',
         big("هَذا", "this", "FOR A “HE” WORD", f'<span class="r">هَذا</span> بَيْتٌ كَبِيرٌ', "This is a big house.", ""),
         big("هَذِهِ", "this", "FOR A “SHE” WORD", f'<span class="r">هَذِهِ</span> غُرْفَتِي', "This is my room.", ""),
         big("ذَلِكَ", "that", "FOR A “HE” WORD", f'<span class="r">ذَٰلِكَ</span> الْكِتَابُ لَا رَيْبَ فِيهِ', "That is the Book, about which there is no doubt.",
             "al-Baqarah 2:2 · you hear it at the start of al-Baqarah"),
         big("تِلْكَ", "that", "FOR A “SHE” WORD", f'<span class="r">تِلْكَ</span> آيَاتُ الْكِتَابِ الْحَكِيمِ', "These are the verses of the wise Book.",
             "Yūnus 10:1 · plurals of things take the “she” words too"),
         '<div class="k">HOW DO YOU KNOW?</div><div class="t2">Look at the end<br>of the word</div>'
         f'<div class="card"><div class="ar" style="font-size:110px">مَدْرَسَ<span class="r">ة</span></div><div class="rule">ة on the end: a “she” word → هَذِهِ</div></div>'
         f'<div class="card"><div class="ar" style="font-size:110px">مَسْجِد</div><div class="rule">most other words: a “he” → هَذا</div></div>'
         f'<div class="note">Watch out: {A("أُمّ", "", 44)} mother and {A("شَمْس", "", 44)} sun are “she” words with no ة.</div>',
         '<div class="k">YOUR TURN</div><div class="t2"><span class="ar">هَذا</span> or <span class="ar">هَذِهِ</span>?</div>'
         + "".join(f'<div class="card" style="padding:12px 40px 18px;gap:0"><div style="display:flex;direction:rtl;justify-content:center;align-items:center;gap:24px"><span style="display:inline-block;width:190px;height:6px;border-radius:3px;background:#B4322A;margin-top:40px"></span><span class="ar" style="font-size:76px">{w}</span></div><div class="note">{i}. {en}</div></div>'
                   for i, (w, en) in enumerate([("مَدْرَسَةٌ", "a school"), ("مَسْجِدٌ", "a mosque"), ("شَمْسٌ", "a sun"), ("كُتُبٌ", "books")], 1))
         + '<div class="s">Comment your 4 answers 👇 then swipe.</div>',
         '<div class="k">THE ANSWERS</div>'
         + "".join(f'<div class="card" style="padding:12px 40px 18px;gap:0"><div class="ar" style="font-size:76px"><span class="r">{t}</span> {w}</div><div class="note">{i}. {why}</div></div>'
                   for i, (t, w, why) in enumerate([("هَذِهِ", "مَدْرَسَةٌ", "ة on the end"), ("هَذا", "مَسْجِدٌ", "a “he” word"),
                                                    ("هَذِهِ", "شَمْسٌ", "a “she” word with no ة"), ("هَذِهِ", "كُتُبٌ", "a plural of things")], 1))
         + '<div class="s">How many did you get? <b>0 to 4</b> 👇</div>',
         '<div class="k">SAVE THIS 📌</div><div class="ask">Four little words<br>you’ll hear in every sūrah.</div>'
         f'<div class="ar" style="font-size:120px">{A("هَذا · هَذِهِ · ذَلِكَ · تِلْكَ")}</div>'
         '<div class="s">Send it to your Arabic study buddy 🤍</div>']
    return [page("light", K, s, i + 1, n) for i, s in enumerate(S)]

# ---------------------------------------------------------------- khutbah (dark)
def khutbah():
    global WM; WM = "ن"
    K, n = "JUMUʿAH", 8
    LINE = "الْحَمْدُ لِلَّهِ نَسْتَعِينُهُ وَنَسْتَغْفِرُهُ وَنَعُوذُ بِاللَّهِ مِنْ شُرُورِ أَنْفُسِنا"
    w = lambda ar, en, *notes: (f'<div class="ar glow" style="font-size:150px">{ar}</div><div class="t2">{en}</div>'
                                + "".join(f'<div class="card"><div class="note" style="color:#e9e2cf;font-size:44px">{x}</div></div>' for x in notes))
    S = ['<div class="k">JUMUʿAH MUBĀRAK</div><div class="t">The words that<br>open the khutbah</div>'
         f'<div class="ar glow" style="font-size:84px;line-height:1.7">{LINE}</div>'
         '<div class="s">You hear them almost every Friday. Here they are, <b>word by word.</b></div><div class="swipe">SWIPE →</div>',
         w("الْحَمْدُ لِلَّهِ", "All praise is for Allah", "You already say this one every day."),
         w('<span class="r">نَ</span>سْتَعِينُ<span class="tl">هُ</span>', "We ask Him for help",
           f'You say {A("نَسْتَعِينُ", "g", 52)} in every rakʿah: {A("وَإِيّاكَ نَسْتَعِينُ", "g", 52)} (al-Fātiḥah 1:5).',
           '<span class="r">نَـ</span> = we · <span class="tl">ـهُ</span> = Him'),
         w('وَ<span class="r">نَ</span>سْتَغْفِرُ<span class="tl">هُ</span>', "And we ask Him for forgiveness",
           f'The same word as {A("أَسْتَغْفِرُ اللَّهَ", "g", 52)}: <b>I</b> ask Allah for forgiveness. Swap أَ for <span class="r">نَـ</span>, and it’s <b>we</b>.'),
         w('وَ<span class="r">نَ</span>عُوذُ بِاللَّهِ', "And we seek refuge in Allah",
           f'Like {A("أَعُوذُ بِاللَّهِ", "g", 52)} before al-Fātiḥah: <b>I</b> seek refuge. Here it’s <b>we</b> again.'),
         w('مِنْ شُرُورِ أَنْفُسِ<span class="r">نا</span>', "From the evil of our own selves", '<span class="r">ـنا</span> on the end = our'),
         '<div class="k">DID YOU NOTICE?</div><div class="t2">It’s all “we”</div>'
         f'<div class="ar glow" style="font-size:84px;line-height:1.7">الْحَمْدُ لِلَّهِ <span class="r">نَ</span>سْتَعِينُهُ وَ<span class="r">نَ</span>سْتَغْفِرُهُ '
         f'وَ<span class="r">نَ</span>عُوذُ بِاللَّهِ مِنْ شُرُورِ أَنْفُسِ<span class="r">نا</span></div>'
         '<div class="s">Four times in one line: the imam opens by speaking for <b>all of us.</b></div>'
         '<div class="note">From the khuṭbat al-ḥājah the Prophet ﷺ taught (an-Nasāʾī 1404, Abū Dāwūd 2118). The wording varies a little between narrations.</div>',
         '<div class="k">SEND THIS 🤍</div><div class="ask">to who you’re going<br>to Jumuʿah with</div>'
         f'<div class="ar glow" style="font-size:130px">جُمُعَة مُبارَكَة</div>'
         '<div class="s">What does the imam say next? <b>Comment it</b> 👇</div>']
    return [page("dark", K, s, i + 1, n) for i, s in enumerate(S)]

# ---------------------------------------------------------------- salah cheat sheet (dark)
POS = [("RUKŪʿ · BOWING", "سُبْحانَ رَبِّيَ الْعَظِيمِ", "Glory be to my Lord, the Magnificent.", [("سُبْحانَ", "Glory be to"), ("رَبِّيَ", "my Lord"), ("الْعَظِيمِ", "the Magnificent")]),
       ("RISING FROM RUKŪʿ", "سَمِعَ اللَّهُ لِمَنْ حَمِدَهُ", "Allah hears the one who praises Him.", [("سَمِعَ", "hears"), ("اللَّهُ", "Allah"), ("لِمَنْ", "the one who"), ("حَمِدَهُ", "praises Him")]),
       ("STANDING STRAIGHT", "رَبَّنا وَلَكَ الْحَمْدُ", "Our Lord, and to You belongs all praise.", [("رَبَّنا", "Our Lord"), ("وَلَكَ", "and to You"), ("الْحَمْدُ", "all praise")]),
       ("SUJŪD · PROSTRATION", "سُبْحانَ رَبِّيَ الْأَعْلى", "Glory be to my Lord, the Most High.", [("سُبْحانَ", "Glory be to"), ("رَبِّيَ", "my Lord"), ("الْأَعْلى", "the Most High")]),
       ("BETWEEN THE TWO SUJŪD", "رَبِّ اغْفِرْ لِي", "My Lord, forgive me.", [("رَبِّ", "My Lord"), ("اغْفِرْ", "forgive"), ("لِي", "me")])]
def salah():
    global WM; WM = "س"
    K, n = "YOUR SALAH", 8
    S = ['<div class="k">SAVE THIS 📌</div><div class="t">Your salah<br>cheat sheet</div>'
         '<div class="s">What you say in each position, <b>word by word.</b> Read it once before your next prayer.</div>'
         f'<div class="ar glow" style="font-size:96px;line-height:1.6">سُبْحانَ رَبِّيَ الْعَظِيمِ</div><div class="swipe">5 POSITIONS · SWIPE →</div>']
    for k, (lab, line, en, ws) in enumerate(POS, 1):
        chips = "".join(f'<div class="chip"><span class="ar g" style="font-size:{68 if len(ws) > 3 else 80}px">{a}</span><span>{m}</span></div>' for a, m in ws)
        S.append(f'<div class="k">{k} · {lab}</div><div class="ar glow" style="font-size:{110 if len(line) > 22 else 130}px;line-height:1.5">{line}</div>'
                 f'<div class="t2" style="font-size:66px">{en}</div><div class="chips">{chips}</div>')
    S.append('<div class="k">DID YOU NOTICE?</div><div class="t2" style="font-size:78px">Bowing down:<br><span class="g">the Magnificent</span>.<br>Forehead on the ground:<br><span class="g">the Most High</span>.</div>'
             f'<div class="card"><div class="ar glow" style="font-size:90px">الْعَظِيمِ · الْأَعْلى</div>'
             '<div class="note" style="color:#e9e2cf">At your lowest point, you say “the Most High”.</div></div>')
    S.append('<div class="k">SAVE THIS 📌</div><div class="ask">Send it to someone<br>learning their salah 🤍</div>'
             '<div class="s">Which part do you want <b>word by word</b> next? Comment it 👇</div>')
    return [page("dark", K, s, i + 1, n) for i, s in enumerate(S)]

SETS = {"dots": dots, "join": join, "starter": starter, "this-that": this_that, "khutbah": khutbah, "salah": salah}

def render(name, slides):
    out = os.path.join(HERE, "stills", f"{name}-tiktok"); os.makedirs(out, exist_ok=True)
    for f in os.listdir(out):
        if f.endswith(".jpg"): os.remove(os.path.join(out, f))
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium" if os.path.exists("/opt/pw-browsers/chromium") else None)
        pg = b.new_page(viewport={"width": W, "height": H})
        for i, s in enumerate(slides, 1):
            pg.set_content(f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{s}</body></html>", wait_until="load")
            pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(250)
            over = pg.evaluate("""() => { const b = document.querySelector('.body').getBoundingClientRect();
                 return [...document.querySelectorAll('.body > *')].some(e => { const r = e.getBoundingClientRect(); return r.top < b.top - 1 || r.bottom > b.bottom + 1; }); }""")
            if over: print(f"  ! {name} slide {i}: content runs outside the safe area")
            png = os.path.join(out, f"{name}-{i:02d}.png"); pg.screenshot(path=png)
            from PIL import Image
            Image.open(png).convert("RGB").save(png[:-4] + ".jpg", quality=92); os.remove(png)
        b.close()
    print(f"{name}: {len(slides)} slides -> {out}")

if __name__ == "__main__":
    for name in (sys.argv[1:] or SETS):
        render(name, SETS[name]())
