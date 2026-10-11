#!/usr/bin/env python3
"""Carousel: "Think understanding the Quran is too hard?" (owner, 11 Oct 2026). Eight 1080x1350 slides on how few words make up
the salah. Numbers come from the app's own count (salah.js: every word of a four-rakah prayer in salah-data.js times REPS,
not counting the surah after al-Fatiha): 425 words, 90 different, top 5 = 34%, top 20 = 56%. Hook checked with TypeSafe
(tools/typesafe-exp/salah_numbers_carousel.py); slide 1 also comes as an alternative cover, "20 words = over half of your salah".

  python3 brag-quiz/build_salah_numbers.py   ->  brag-quiz/stills/sn-1.png ... sn-8.png, sn-1-alt.png
"""
import html, json, os, subprocess
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
FONTS = "file://" + os.path.join(ROOT, "brag-output-v6/composition/assets/fonts")
SERIF = "file://" + os.path.join(HERE, "fonts/instrument-serif-latin-400-normal.woff2")
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
e = html.escape

# the app's count, with salah.js's own matching rules (bare, wid, REPS)
COUNT = r"""
eval(require("fs").readFileSync("salah-data.js","utf8").replace("const SALAH","global.SALAH"));
const bare = s => String(s).replace(/[۝؟?!.،,:؛﴿﴾0-9٠-٩]/g, "").replace(/([ً-ِْ])ّ/g, "ّ$1").trim();
const wid = w => "sw:" + bare(w.ar);
const REPS = { takbir:22, opening:1, refuge:1, fatiha1:4, fatiha2:4, ruku:12, rising:4, sujud:[24,4], tashahhud:2, salawat:1, taslim:2 };
const F = {}, seen = new Map();
SALAH.parts.forEach(p => { const r = REPS[p.id]; if(r) p.lines.forEach((l, i) => { const n = Array.isArray(r) ? (r[i] || 0) : r;
  l.words.forEach(w => { const k = wid(w); F[k] = (F[k] || 0) + n; if(!seen.has(k)) seen.set(k, w); }); }); });
const words = [...seen.entries()].map(([k, w]) => ({ ar: w.ar, en: w.en, root: !!w.root, n: F[k] })).sort((a, b) => b.n - a.n);
console.log(JSON.stringify(words));
"""
WORDS = json.loads(subprocess.check_output(["node", "-e", COUNT], cwd=ROOT))
TOTAL = sum(w["n"] for w in WORDS)                                  # 425
TOP = [w for w in WORDS if w["root"]][:20]                          # as the app picks its 20 most-said words
pct = lambda ws: round(100 * sum(w["n"] for w in ws) / TOTAL)
assert (TOTAL, len(WORDS), pct(TOP[:5]), pct(TOP)) == (425, 90, 34, 56), (TOTAL, len(WORDS), pct(TOP[:5]), pct(TOP))

INK, TEAL, RED, GOLD, BG = "#17262b", "#2e7263", "#b4322a", "#a8842c", "#f1ece0"
CSS = f"""
@font-face {{ font-family:"Plex Arabic"; src:url("{FONTS}/ibm-plex-sans-arabic-arabic-700-normal.woff2"); font-weight:700; }}
@font-face {{ font-family:"Karla"; src:url("{FONTS}/karla-latin-500-normal.woff2"); font-weight:500; }}
@font-face {{ font-family:"Karla"; src:url("{FONTS}/karla-latin-700-normal.woff2"); font-weight:700; }}
@font-face {{ font-family:"JetBrains Mono"; src:url("{FONTS}/jetbrains-mono-latin-500-normal.woff2"); font-weight:500; }}
@font-face {{ font-family:"Instrument Serif"; src:url("{SERIF}"); }}
* {{ box-sizing:border-box; }}
body {{ margin:0; width:1080px; height:1350px; overflow:hidden; position:relative; background:{BG}; color:{INK}; font-family:"Karla",sans-serif;
  background-image:radial-gradient(circle at 50% -10%, rgba(168,132,44,.22) 0%, rgba(168,132,44,.05) 40%, rgba(241,236,224,0) 62%); }}
body.dark {{ background:{INK}; color:{BG}; background-image:radial-gradient(circle at 50% 0%, rgba(168,132,44,.30) 0%, rgba(23,38,43,0) 60%); }}
.brand {{ position:absolute; top:62px; left:0; right:0; display:flex; justify-content:center; align-items:center; gap:14px; z-index:2; }}
.brand b {{ font-family:"Plex Arabic"; font-size:40px; font-weight:700; }}
.tile {{ position:relative; width:56px; height:56px; border-radius:14px; background:{INK}; display:grid; place-items:center; }}
.dark .tile {{ background:{BG}; }} .tile span {{ font-family:"Plex Arabic"; font-weight:700; font-size:34px; color:{BG}; margin-top:-5px; }}
.dark .tile span {{ color:{INK}; }}
.tile em {{ position:absolute; right:9px; top:8px; width:9px; height:9px; border-radius:50%; background:{RED}; }}
.kick {{ position:absolute; top:160px; left:0; right:0; text-align:center; font-family:"JetBrains Mono"; font-size:26px; letter-spacing:.16em; color:#4f6163; }}
.dark .kick {{ color:rgba(241,236,224,.6); }}
h1 {{ position:absolute; left:80px; right:80px; margin:0; text-align:center; font-weight:700; letter-spacing:-.025em; line-height:1.06; }}
h1 i {{ font-family:"Instrument Serif"; font-weight:400; font-style:italic; letter-spacing:0; }}
.red {{ color:{RED}; }} .teal {{ color:{TEAL}; }} .gold {{ color:#E9B949; }}
.sub {{ position:absolute; left:110px; right:110px; text-align:center; font-size:38px; font-weight:500; line-height:1.3; color:#4f6163; }}
.dark .sub {{ color:rgba(241,236,224,.75); }}
.swipe {{ position:absolute; bottom:70px; left:0; right:0; text-align:center; font-size:40px; font-weight:700; color:{TEAL}; }}
.dark .swipe {{ color:#E9B949; }}
.note {{ position:absolute; bottom:64px; left:90px; right:90px; text-align:center; font-size:30px; color:#6b7a7c; line-height:1.35; }}
.grid {{ position:absolute; left:40px; display:grid; grid-template-columns:repeat(25, 34px); gap:6px; }}
.grid i {{ width:34px; height:34px; border-radius:9px; background:rgba(23,38,43,.12); }}
.grid i.on {{ background:{TEAL}; }} .grid i.first {{ background:{INK}; }} .grid i.hot {{ background:{RED}; }}
.big {{ font-family:"Instrument Serif"; font-style:italic; font-weight:400; }}
/* cover: a field of the prayer's words */
.field {{ position:absolute; inset:0; -webkit-mask-image:linear-gradient(to bottom, transparent 0, #000 22%, #000 70%, transparent 100%); overflow:hidden; font-family:"Plex Arabic"; font-weight:700; color:rgba(241,236,224,.08); font-size:64px;
  line-height:1.55; text-align:center; padding:20px 10px; word-spacing:18px; }}
.field b {{ color:rgba(233,185,73,.28); font-weight:700; }}
.dark h1 {{ text-shadow:0 0 30px {INK}, 0 0 60px {INK}; }}
.prayers {{ position:absolute; top:700px; left:90px; right:90px; display:flex; justify-content:space-between; }}
.pr {{ width:160px; text-align:center; }} .pr .dots {{ display:flex; flex-wrap:wrap; justify-content:center; gap:12px; height:120px; align-content:flex-end; }}
.pr .dots i {{ width:46px; height:46px; border-radius:50%; background:{TEAL}; box-shadow:0 8px 16px -8px rgba(46,114,99,.7); }}
.pr b {{ display:block; margin-top:22px; font-size:34px; }} .pr span {{ font-family:"Plex Arabic"; font-size:34px; color:#6b7a7c; }}
.five {{ position:absolute; top:1075px; left:60px; right:60px; display:flex; justify-content:center; gap:16px; direction:rtl; }}
.chip {{ background:#fff8; border:3px solid rgba(180,50,42,.35); border-radius:24px; padding:10px 18px 14px; text-align:center; min-width:150px; }}
.chip .ar {{ font-family:"Plex Arabic"; font-weight:700; font-size:50px; color:{RED}; line-height:1.4; }}
.chip .en {{ direction:ltr; font-size:22px; font-weight:700; color:#4f6163; }}
.list {{ position:absolute; top:320px; left:50px; right:50px; display:grid; grid-template-columns:1fr 1fr; column-gap:36px; row-gap:12px; }}
.row {{ display:grid; grid-template-columns:34px 1fr; align-items:center; column-gap:10px; }}
.row .k {{ font-family:"JetBrains Mono"; font-size:22px; color:#8a9799; }}
.row .bar {{ position:relative; height:80px; border-radius:16px; background:rgba(23,38,43,.06); overflow:hidden; }}
.row .fill {{ position:absolute; left:0; top:0; bottom:0; background:rgba(46,114,99,.22); border-radius:16px; }}
.row.t5 .fill {{ background:rgba(180,50,42,.22); }}
.row .ar {{ position:absolute; right:14px; top:-2px; font-family:"Plex Arabic"; font-weight:700; font-size:46px; line-height:80px; }}
.row .en {{ position:absolute; left:16px; top:10px; font-size:26px; font-weight:700; line-height:1.05; max-width:230px; white-space:nowrap; }}
.row .n {{ position:absolute; left:16px; bottom:9px; font-family:"JetBrains Mono"; font-size:22px; color:{TEAL}; }}
.row.t5 .n {{ color:{RED}; }}
.donut {{ position:absolute; top:420px; left:290px; width:500px; height:500px; }}
.donut .c {{ position:absolute; inset:0; display:grid; place-items:center; text-align:center; }}
.donut .c b {{ font-family:"Instrument Serif"; font-style:italic; font-weight:400; font-size:190px; line-height:.9; color:{TEAL}; }}
.donut .c span {{ display:block; font-size:30px; font-weight:700; margin:10px auto 0; max-width:250px; line-height:1.15; }}
.save {{ position:absolute; top:880px; left:120px; right:120px; display:grid; gap:24px; }}
.save div {{ border-radius:28px; padding:26px 30px; font-size:40px; font-weight:700; text-align:center; line-height:1.2; }}
.save .s1 {{ background:#22363c; }} .save .s2 {{ background:#E9B949; color:{INK}; }}
"""
BRAND = '<div class="brand"><div class="tile"><span>ر</span><em></em></div><b>رَفِيق</b></div>'

def grid(top, cls):
    """425 squares, one per word said, sorted by how often the word is said. cls(i, word, first) -> class."""
    sq, i = [], 0
    for w in WORDS:
        for j in range(w["n"]):
            sq.append(f'<i class="{cls(i, w, j == 0)}"></i>'); i += 1
    return f'<div class="grid" style="top:{top}px">{"".join(sq)}</div>'

def field():
    hot = {w["ar"] for w in TOP[:5]}
    seq = [WORDS[(i * 7) % len(WORDS)] for i in range(150)]          # every word of the prayer, mixed, the top 5 picked out in gold
    return '<div class="field" lang="ar">' + " ".join(f'<b>{e(w["ar"])}</b>' if w["ar"] in hot else e(w["ar"]) for w in seq) + "</div>"

def donut(p):
    r, c = 210, 2 * 3.14159 * 210
    return (f'<div class="donut"><svg viewBox="0 0 500 500" width="500" height="500"><circle cx="250" cy="250" r="{r}" fill="none" stroke="rgba(23,38,43,.08)" stroke-width="56"/>'
            f'<circle cx="250" cy="250" r="{r}" fill="none" stroke="{TEAL}" stroke-width="56" stroke-linecap="round" stroke-dasharray="{c * p / 100:.1f} {c:.1f}" transform="rotate(-90 250 250)"/></svg>'
            f'<div class="c"><div><b>{p}%</b><span>of everything you say in salah</span></div></div></div>')

def slides():
    t5 = sum(w["n"] for w in TOP[:5]); top5 = {w["ar"] for w in TOP[:5]}
    # 1-10 down the left column, 11-20 down the right (the grid fills row by row)
    rows = "".join(f'<div class="row{" t5" if k < 5 else ""}"><div class="k">{k + 1}</div><div class="bar"><div class="fill" style="width:{100 * TOP[k]["n"] / TOP[0]["n"]:.0f}%"></div>'
                   f'<div class="en">{e(TOP[k]["en"])}</div><div class="n">×{TOP[k]["n"]}</div><div class="ar" lang="ar">{e(TOP[k]["ar"])}</div></div></div>'
                   for k in [i // 2 + (10 if i % 2 else 0) for i in range(20)])
    chips = "".join(f'<div class="chip"><div class="ar" lang="ar">{e(w["ar"])}</div><div class="en">{e(w["en"])}<br>×{w["n"]}</div></div>' for w in TOP[:5])
    pr = "".join(f'<div class="pr"><div class="dots">{"<i></i>" * n}</div><b>{name}</b></div>'
                 for name, n in [("Fajr", 2), ("Dhuhr", 4), ("ʿAsr", 4), ("Maghrib", 3), ("ʿIshāʾ", 4)])
    cover = lambda h: (f'<body class="dark">{field()}{BRAND}<h1 style="top:400px;font-size:112px">{h}</h1>'
                       f'<div class="swipe">Swipe →</div></body>')
    return {
     "1": cover('Think understanding the <i class="gold">Quran</i> is too hard?'),
     "1-alt": cover('<span class="gold">20 words</span> = over <i>half</i> of your salah'),
     "2": f'<body>{BRAND}<div class="kick">START WITH WHAT YOU ALREADY KNOW</div>'
          f'<h1 style="top:220px;font-size:76px">You recite <span class="teal">Al-Fātiḥa</span>, the Quran’s first surah, <i class="red">17 times</i> a day.</h1>'
          f'<div class="prayers" style="top:560px">{pr}</div><div class="sub" style="top:900px">Once in every rakʿah of your five prayers. And the rest of your salah is full of the same few words.</div></body>',
     "3": f'<body>{BRAND}<div class="kick">ONE FOUR-RAKʿAH PRAYER</div><h1 style="top:215px;font-size:84px"><i class="teal">425</i> words</h1>'
          f'{grid(400, lambda i, w, f: "on")}<div class="note">Every word of Dhuhr, ʿAsr or ʿIshāʾ: one square each. Not counting the surah after al-Fātiḥa.</div></body>',
     "4": f'<body>{BRAND}<div class="kick">BUT HOW MANY DIFFERENT WORDS?</div><h1 style="top:215px;font-size:84px">Only <i class="teal">90</i></h1>'
          f'{grid(400, lambda i, w, f: "first" if f else "")}<div class="note">Dark: the first time you say a word. Light: you’re saying it again.</div></body>',
     "5": f'<body>{BRAND}<div class="kick">AND JUST FIVE OF THEM…</div><h1 style="top:215px;font-size:84px">are <i class="red">a third</i> of it</h1>'
          f'{grid(350, lambda i, w, f: "hot" if w["ar"] in top5 else "")}<div class="five">{chips}</div>'
          f'<div class="note">{t5} of the 425 words.</div></body>',
     "6": f'<body>{BRAND}<div class="kick">YOUR 20 MOST-SAID WORDS</div><h1 style="top:215px;font-size:64px">How often you say each one</h1>'
          f'<div class="list">{rows}</div><div class="note">Times said in one four-rakʿah prayer.</div></body>',
     "7": f'<body>{BRAND}<div class="kick">LEARN THOSE 20</div><h1 style="top:215px;font-size:80px">and you understand <i class="teal">over half</i> of your salah</h1>'
          f'{donut(pct(TOP))}<div class="sub" style="top:990px">Top 5: {pct(TOP[:5])}% · top 10: {pct(TOP[:10])}% · top 20: {pct(TOP)}%</div>'
          f'<div class="note">Counted word by word from a four-rakʿah prayer, without the surah after al-Fātiḥa.</div></body>',
     "8": f'<body class="dark">{field()}{BRAND}<h1 style="top:300px;font-size:80px">It’s not the whole Quran.<br><i class="gold">But it’s a real start,</i><br>in your very next prayer.</h1>'
          f'<div class="save"><div class="s1">Save this 📌 for your next salah</div><div class="s2">Send it to someone who thinks Arabic is too hard</div></div></body>',
    }

if __name__ == "__main__":
    out = os.path.join(HERE, "stills"); os.makedirs(out, exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME if os.path.exists(CHROME) else None)
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for k, body in slides().items():
            tmp = os.path.join(out, "_page.html"); open(tmp, "w").write(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>{body}</html>')
            pg.goto("file://" + tmp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)   # a file page, so the local fonts load
            pg.screenshot(path=os.path.join(out, f"sn-{k}.png")); print(f"sn-{k}.png")
        b.close()
    os.remove(os.path.join(out, "_page.html"))
