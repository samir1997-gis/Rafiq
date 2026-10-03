#!/usr/bin/env python3
"""A root-family carousel (1080x1350, Instagram 4:5 and TikTok photo posts): the root's three letters are
coloured inside every word, so the "same three letters" can be seen, not just told. Ends on a line from the
Quran with the root in it, and the site.

  python3 brag-quiz/build_root.py   ->  brag-quiz/stills/root-ilm-<n>.png
"""
import os
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
FONTS = "file://" + os.path.join(ROOT, "brag-output-v6/composition/assets/fonts")
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

# each word as pieces: (text, is_root_letter); the vowel marks ride with their letter
WORDS = [
    ([("عِ", 1), ("لْ", 1), ("م", 1)],                                  "knowledge", "ʿilm"),
    ([("عَ", 1), ("ا", 0), ("لِ", 1), ("م", 1)],                         "a scholar", "ʿālim"),
    ([("مُ", 0), ("عَ", 1), ("لِّ", 1), ("م", 1)],                       "a teacher", "muʿallim"),
    ([("مُ", 0), ("تَ", 0), ("عَ", 1), ("لِّ", 1), ("م", 1)],            "a learner", "mutaʿallim"),
]
LETTERS = "ع  ل  م"

CSS = f"""
@font-face {{ font-family: "Plex Arabic"; src: url("{FONTS}/ibm-plex-sans-arabic-arabic-700-normal.woff2"); font-weight: 700; }}
@font-face {{ font-family: "Karla"; src: url("{FONTS}/karla-latin-500-normal.woff2"); font-weight: 500; }}
@font-face {{ font-family: "Karla"; src: url("{FONTS}/karla-latin-700-normal.woff2"); font-weight: 700; }}
@font-face {{ font-family: "JetBrains Mono"; src: url("{FONTS}/jetbrains-mono-latin-500-normal.woff2"); font-weight: 500; }}
* {{ box-sizing:border-box; margin:0; }}
body {{ width:1080px; height:1350px; overflow:hidden; background:#f1ece0; color:#17262b; font-family:"Karla",sans-serif; position:relative;
  background-image:radial-gradient(circle at 50% -10%, rgba(168,132,44,.22) 0%, rgba(168,132,44,.05) 40%, rgba(241,236,224,0) 62%); }}
.brand {{ position:absolute; top:62px; left:0; right:0; display:flex; justify-content:center; align-items:center; gap:14px; }}
.brand b {{ font-family:"Plex Arabic"; font-size:40px; font-weight:700; }}
.tile {{ position:relative; width:56px; height:56px; border-radius:14px; background:#17262b; display:grid; place-items:center; }}
.tile span {{ font-family:"Plex Arabic"; font-weight:700; font-size:34px; color:#f1ece0; margin-top:-5px; }}
.tile em {{ position:absolute; right:9px; top:8px; width:9px; height:9px; border-radius:50%; background:#b4322a; }}
.ar {{ font-family:"Plex Arabic"; font-weight:700; direction:rtl; }}
.r {{ color:#b4322a; }}
.mid {{ position:absolute; left:80px; right:80px; text-align:center; }}
h1 {{ font-size:66px; line-height:1.12; letter-spacing:-.02em; font-weight:700; }}
.sub {{ font-size:40px; color:#4f6163; line-height:1.3; }}
.grid {{ display:grid; grid-template-columns:1fr 1fr; gap:26px; }}
.card {{ background:#f7f3ea; border:4px solid rgba(23,38,43,.12); border-radius:30px; padding:26px 10px 30px; box-shadow:0 12px 24px -16px rgba(23,38,43,.35); }}
.card .ar {{ font-size:104px; line-height:1.45; }}
.foot {{ position:absolute; bottom:70px; left:0; right:0; text-align:center; font-size:40px; font-weight:700; color:#2e7263; }}
.url {{ position:absolute; bottom:56px; left:50%; transform:translateX(-50%); font-size:38px; font-weight:700; color:#f1ece0; background:#2e7263; border-radius:999px; padding:16px 40px; white-space:nowrap; }}
.big {{ font-size:230px; line-height:1.4; }}
.tr {{ font-family:"JetBrains Mono"; font-size:36px; color:#2e7263; letter-spacing:.02em; }}
.en {{ font-size:64px; font-weight:700; }}
.chip {{ display:inline-block; font-size:34px; color:#4f6163; border:3px solid rgba(23,38,43,.14); border-radius:999px; padding:10px 28px; }}
.chip .ar {{ color:#b4322a; font-size:40px; unicode-bidi:isolate; }}
.n {{ position:absolute; top:170px; left:0; right:0; text-align:center; }}
"""

def word(pieces): return "".join(f'<span class="r">{t}</span>' if r else t for t, r in pieces)
def page(inner): return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>' \
    f'<div class="brand"><div class="tile"><span>ر</span><em></em></div><b>رَفِيق</b></div>{inner}</body></html>'

SLIDES = [
    # 1: the words first, then the question
    page(f'<div class="mid" style="top:190px"><h1>These four words share three letters.</h1>'
         f'<p class="sub" style="margin-top:22px">Can you spot them?</p></div>'
         f'<div class="mid grid" style="top:520px">' + "".join(
             f'<div class="card"><div class="ar">{"".join(t for t, _ in w)}</div></div>' for w, _, _ in WORDS) + '</div>'
         f'<div class="foot">Swipe for the answer →</div>'),
    # 2: the answer, coloured in every word
    page(f'<div class="mid" style="top:190px"><h1>The same three letters: <span class="ar r" dir="rtl" style="font-size:80px;unicode-bidi:isolate">{LETTERS}</span></h1>'
         f'<p class="sub" style="margin-top:18px">Together they mean <b style="color:#17262b">knowing</b>.</p></div>'
         f'<div class="mid grid" style="top:560px">' + "".join(
             f'<div class="card"><div class="ar">{word(w)}</div><div class="sub" style="font-size:34px">{en}</div></div>' for w, en, _ in WORDS) + '</div>'),
] + [
    # 3–6: one word each, root letters coloured
    page(f'<div class="n"><span class="chip"><span class="ar" dir="rtl">{LETTERS}</span> &nbsp;·&nbsp; <bdi>{i + 1} of {len(WORDS)}</bdi></span></div>'
         f'<div class="mid" style="top:400px"><div class="ar big">{word(w)}</div>'
         f'<div class="tr" style="margin-top:10px">{tr}</div><div class="en" style="margin-top:18px">{en}</div></div>')
    for i, (w, en, tr) in enumerate(WORDS)
] + [
    # 7: the payoff
    page('<div class="mid" style="top:200px"><p class="sub">It’s in a duʿāʾ from the Quran:</p></div>'
         '<div class="mid" style="top:380px"><div class="ar" style="font-size:112px;line-height:1.6">رَبِّ زِدْنِي <span class="r">عِلْمًا</span></div>'
         '<div class="en" style="font-size:56px;margin-top:20px">“My Lord, increase me in <span class="r">knowledge</span>.”</div>'
         '<p class="sub" style="font-size:34px;margin-top:20px">Ṭā Hā 20:114</p></div>'
         '<div class="url">Learn the words you say · rafiq-arabic.com</div>'),
]

if __name__ == "__main__":
    out = os.path.join(HERE, "stills"); os.makedirs(out, exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME if os.path.exists(CHROME) else None)
        p = b.new_page(viewport={"width": 1080, "height": 1350})
        for n, html in enumerate(SLIDES, 1):
            tmp = os.path.join(out, "_page.html"); open(tmp, "w").write(html)
            p.goto("file://" + tmp); p.evaluate("document.fonts.ready"); p.wait_for_timeout(200)   # a file page, so the local fonts load
            p.screenshot(path=os.path.join(out, f"root-ilm-{n}.png"))
        b.close()
    os.remove(os.path.join(out, "_page.html"))
    print(len(SLIDES), "slides")
