#!/usr/bin/env python3
"""Still salah quizzes as two-slide carousels (#197): slide 1 asks, slide 2 answers. 1080x1350 (Instagram 4:5;
also TikTok photo posts). The format won with TypeSafe (tools/typesafe-exp/quiz_stills.py); meanings from salah-data.js.

  python3 brag-quiz/build_stills.py [id ...]   ->  brag-quiz/stills/<id>-1-question.png, <id>-2-answer.png
"""
import html, json, os, sys
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
FONTS = "file://" + os.path.join(ROOT, "brag-output-v6/composition/assets/fonts")
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
e = html.escape

CSS = f"""
@font-face {{ font-family: "Plex Arabic"; src: url("{FONTS}/ibm-plex-sans-arabic-arabic-700-normal.woff2"); font-weight: 700; }}
@font-face {{ font-family: "Karla"; src: url("{FONTS}/karla-latin-500-normal.woff2"); font-weight: 500; }}
@font-face {{ font-family: "Karla"; src: url("{FONTS}/karla-latin-700-normal.woff2"); font-weight: 700; }}
@font-face {{ font-family: "JetBrains Mono"; src: url("{FONTS}/jetbrains-mono-latin-500-normal.woff2"); font-weight: 500; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; width:1080px; height:1350px; overflow:hidden; background:#f1ece0; color:#17262b; font-family:"Karla",sans-serif;
  background-image:radial-gradient(circle at 50% -10%, rgba(168,132,44,.22) 0%, rgba(168,132,44,.05) 40%, rgba(241,236,224,0) 62%); }}
.brand {{ position:absolute; top:62px; left:0; right:0; display:flex; justify-content:center; align-items:center; gap:14px; }}
.brand b {{ font-family:"Plex Arabic"; font-size:40px; font-weight:700; }}
.tile {{ position:relative; width:56px; height:56px; border-radius:14px; background:#17262b; display:grid; place-items:center; }}
.tile span {{ font-family:"Plex Arabic"; font-weight:700; font-size:34px; color:#f1ece0; margin-top:-5px; }}
.tile em {{ position:absolute; right:9px; top:8px; width:9px; height:9px; border-radius:50%; background:#b4322a; }}
.kicker {{ position:absolute; top:160px; left:0; right:0; text-align:center; font-family:"JetBrains Mono"; font-size:26px; letter-spacing:.16em; color:#4f6163; }}
.q {{ position:absolute; top:206px; left:90px; right:90px; text-align:center; font-size:62px; font-weight:700; line-height:1.12; letter-spacing:-.02em; }}
.word {{ position:absolute; top:400px; left:0; right:0; text-align:center; font-family:"Plex Arabic"; font-weight:700; font-size:176px; line-height:1.3; }}
.opts {{ position:absolute; top:690px; left:100px; right:100px; display:grid; grid-template-columns:1fr 1fr; gap:22px; }}
.opt {{ height:130px; border-radius:30px; background:#f7f3ea; border:4px solid rgba(23,38,43,.13); display:flex; align-items:center; justify-content:center;
  font-size:42px; font-weight:700; text-align:center; padding:0 12px; line-height:1.1; white-space:nowrap; box-shadow:0 12px 24px -16px rgba(23,38,43,.35); }}
.opt.ok {{ background:#e3efe9; border-color:#2e7263; color:#17262b; }}
.opt.dim {{ opacity:.3; }}
.foot {{ position:absolute; bottom:70px; left:0; right:0; text-align:center; font-size:40px; font-weight:700; color:#2e7263; }}
.foot i {{ font-style:normal; display:inline-block; margin-left:10px; }}
.line {{ position:absolute; top:1000px; left:70px; right:70px; text-align:center; }}
.line .ar {{ font-family:"Plex Arabic"; font-weight:700; font-size:66px; color:#2e7263; line-height:1.5; }}
.line .en {{ font-size:40px; font-weight:700; line-height:1.25; margin-top:4px; }}
.line .where {{ font-size:32px; color:#4f6163; margin-top:10px; }}
.url {{ position:absolute; bottom:56px; left:50%; transform:translateX(-50%); font-size:38px; font-weight:700; color:#f1ece0; background:#2e7263; border-radius:999px; padding:16px 40px; white-space:nowrap; }}
"""

def page(s, answer):
    opts = "".join(f'<div class="opt{" ok" if answer and i == s["answer"] else " dim" if answer else ""}">{e(o)}{" ✓" if answer and i == s["answer"] else ""}</div>'
                   for i, o in enumerate(s["options"]))
    tail = (f'<div class="line"><div class="ar" lang="ar">{e(s["line"])}</div><div class="en">{e(s["line_en"])}</div><div class="where">{e(s["where"])}</div></div>'
            f'<div class="url">Learn every word · rafiq-arabic.com</div>') if answer else '<div class="foot">Swipe for the answer <i>→</i></div>'
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="brand"><div class="tile"><span>ر</span><em></em></div><b>رَفِيق</b></div>
<div class="kicker">{"THE ANSWER" if answer else "YOUR SALAH · QUICK QUIZ"}</div>
<div class="q">{"What does this word in your salah mean?"}</div>
<div class="word" lang="ar">{e(s["word"])}</div>
<div class="opts">{opts}</div>{tail}</body></html>"""

if __name__ == "__main__":
    out = os.path.join(HERE, "stills"); os.makedirs(out, exist_ok=True)
    items = [s for s in json.load(open(os.path.join(HERE, "stills.json"))) if len(sys.argv) < 2 or s["id"] in sys.argv[1:]]
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME if os.path.exists(CHROME) else None)
        p = b.new_page(viewport={"width": 1080, "height": 1350})
        for s in items:
            for n, (answer, name) in enumerate([(False, "question"), (True, "answer")], 1):
                tmp = os.path.join(out, "_page.html"); open(tmp, "w").write(page(s, answer))
                p.goto("file://" + tmp); p.evaluate("document.fonts.ready"); p.wait_for_timeout(200)   # a file page, so the local fonts load
                p.screenshot(path=os.path.join(out, f"{s['id']}-{n}-{name}.png"))
            print(s["id"])
        b.close()
    if os.path.exists(os.path.join(out, "_page.html")): os.remove(os.path.join(out, "_page.html"))
