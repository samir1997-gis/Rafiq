#!/usr/bin/env python3
"""Light, meme-style "POV" photo carousels (1080x1920, TikTok photo mode; the middle is safe for Instagram's 4:5 crop):
big text, one big emoji per slide (Noto Color Emoji, open licence), the brand colours, an end card.
Chosen with TypeSafe (tools/typesafe-exp/fun_content.py): the punchline is a fact from the app (the 20 words you say
most are about 56% of the prayer, salah.js), never a made-up "I understand 60%" testimonial.

  python3 brag-quiz/build_pov.py [pov-salah|pov-imam ...]   ->  brag-quiz/stills/<id>-<n>.png
"""
import html, os, sys
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
FONTS = "file://" + os.path.join(ROOT, "brag-output-v6/composition/assets/fonts")
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
e = html.escape

# each slide: (small label or "", main text, emoji, Arabic line or "", its meaning or "")
POSTS = {
  "pov-salah": [
    ("", "POV: you just finished praying", "🤲", "", ""),
    ("", "…and you didn't understand a single word you said", "😶", "", ""),
    ("you, every day:", "“I say this every single day. What does it even MEAN?”", "😩", "", ""),
    ("your friend:", "Akhi 😭 start with the 20 words you say most. That's over half of your salah.", "🙋‍♂️", "", ""),
    ("next salah:", "wait… I KNOW what that means", "🥹", "سُبْحانَ رَبِّيَ الْعَظِيمِ", "Glory be to my Lord, the Magnificent."),
  ],
  "pov-imam": [
    ("", "POV: the imam starts reciting…", "🕌", "", ""),
    ("", "…and it's a surah you actually learned word by word", "👀", "", ""),
    ("", "understanding every word, for the first time", "🥹", "قُلْ هُوَ اللَّهُ أَحَدٌ", "Say: He is Allah, the One. (al-Ikhlāṣ 112:1)"),
  ],
}
END = ("Your salah, word by word.", "Start with the 20 words you say most.", "rafiq-arabic.com · 7 days free")

CSS = f"""
@font-face {{ font-family: "Plex Arabic"; src: url("{FONTS}/ibm-plex-sans-arabic-arabic-700-normal.woff2"); font-weight: 700; }}
@font-face {{ font-family: "Karla"; src: url("{FONTS}/karla-latin-700-normal.woff2"); font-weight: 700; }}
@font-face {{ font-family: "Karla"; src: url("{FONTS}/karla-latin-500-normal.woff2"); font-weight: 500; }}
* {{ box-sizing:border-box; margin:0; }}
body {{ width:1080px; height:1920px; overflow:hidden; background:#f1ece0; color:#17262b; font-family:"Karla","Noto Color Emoji",sans-serif;
  display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; padding:0 90px; position:relative;
  background-image:radial-gradient(circle at 50% 30%, rgba(168,132,44,.20) 0%, rgba(241,236,224,0) 60%); }}
.lab {{ font-size:46px; font-weight:500; color:#2e7263; margin-bottom:22px; }}
.t {{ font-size:84px; font-weight:700; line-height:1.12; letter-spacing:-.02em; }}
.em {{ font-family:"Noto Color Emoji"; font-size:300px; line-height:1.15; margin-top:60px; }}
.ar {{ font-family:"Plex Arabic"; font-weight:700; direction:rtl; font-size:104px; line-height:1.6; color:#2e7263; margin-top:40px; }}
.en {{ font-size:44px; font-weight:500; color:#4f6163; margin-top:6px; }}
.brand {{ position:absolute; bottom:120px; left:0; right:0; display:flex; justify-content:center; align-items:center; gap:14px; opacity:.85; }}
.brand b {{ font-family:"Plex Arabic"; font-size:40px; }}
.tile {{ position:relative; width:56px; height:56px; border-radius:14px; background:#17262b; display:grid; place-items:center; }}
.tile span {{ font-family:"Plex Arabic"; font-weight:700; font-size:34px; color:#f1ece0; margin-top:-5px; }}
.tile em {{ position:absolute; right:9px; top:8px; width:9px; height:9px; border-radius:50%; background:#b4322a; }}
.url {{ margin-top:70px; font-size:48px; font-weight:700; color:#f1ece0; background:#2e7263; border-radius:999px; padding:22px 52px; }}
"""
BRAND = '<div class="brand"><div class="tile"><span>ر</span><em></em></div><b>رَفِيق</b></div>'

def page(inner, brand=True):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{inner}{BRAND if brand else ""}</body></html>'

def slides(post):
    out = [page((f'<div class="lab">{e(lab)}</div>' if lab else '') + f'<div class="t">{e(t)}</div>'
                + (f'<div class="ar">{e(ar)}</div><div class="en">{e(en)}</div>' if ar else '')
                + f'<div class="em">{em}</div>') for lab, t, em, ar, en in post]
    out.append(page('<div class="tile" style="width:150px;height:150px;border-radius:38px"><span style="font-size:96px">ر</span>'
                    '<em style="width:22px;height:22px;right:24px;top:20px"></em></div>'
                    f'<div class="t" style="margin-top:60px">{e(END[0])}</div><div class="en" style="font-size:52px;margin-top:24px">{e(END[1])}</div>'
                    f'<div class="url">{e(END[2])}</div>', brand=False))
    return out

if __name__ == "__main__":
    out = os.path.join(HERE, "stills"); os.makedirs(out, exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME if os.path.exists(CHROME) else None)
        p = b.new_page(viewport={"width": 1080, "height": 1920})
        for pid in (sys.argv[1:] or POSTS):
            for n, h in enumerate(slides(POSTS[pid]), 1):
                tmp = os.path.join(out, "_page.html"); open(tmp, "w").write(h)
                p.goto("file://" + tmp); p.evaluate("document.fonts.ready"); p.wait_for_timeout(250)   # a file page, so the local fonts load
                p.screenshot(path=os.path.join(out, f"{pid}-{n}.png"))
            print(pid)
        b.close()
    os.remove(os.path.join(out, "_page.html"))
