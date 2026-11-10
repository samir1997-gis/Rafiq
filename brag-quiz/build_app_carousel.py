#!/usr/bin/env python3
"""The app carousel (#355): the 1-in-5 post that shows Rafiq ("About 1 in 5 shows the app and says free week, link in bio",
IDEAS.md). The pop carousels' look (bright colour, doodles, ink outlines) around the app's real screens, cropped from the store
screenshots (app/store/screenshots/appstore-N.png, #352), each under its store headline. Written straight at TikTok's 9:16.

  python3 brag-quiz/build_app_carousel.py   ->  brag-quiz/stills/app-tiktok/app-<nn>.jpg (1080×1920)
"""
import os
from PIL import Image
from playwright.sync_api import sync_playwright
import build_pop_carousel as P

ROOT = os.path.dirname(P.S.HERE); SHOTS = os.path.join(ROOT, "app/store/screenshots"); OUT = os.path.join(P.S.HERE, "stills", "app-tiktok")
INK, PAPER = P.INK, P.PAPER
SLIDES = [  # (store screenshot, headline, the word in the headline to light, background, doodles)
    (1, "5 minutes a day. Just press Continue.", "Just press Continue.", "#2EB67D", ["#FFE66D", "#fff"]),
    (2, "Understand every word of your salah", "your salah", "#4D96FF", ["#FFE66D", "#fff"]),
    (3, "Say your first sentence today", "today", "#FF7A59", ["#FFE66D", "#fff"]),
    (5, "Practise your way: scenes, verbs, spelling", "your way", "#9B6BFF", ["#FFE66D", "#fff"]),
    (4, "Stuck? Ask Rafiq, your AI tutor", "Ask Rafiq", "#FFB23F", ["#fff", "#FF7A59"]),
    (6, "Every word with audio, fully vowelled", "with audio", "#2E7263", ["#FFC93C", "#fff"])]
CSS = P.CSS + f"""
.hl {{ position:absolute; top:120px; left:60px; right:60px; text-align:center; }}
.hl span {{ display:inline-block; background:{PAPER}; border:5px solid {INK}; border-radius:26px; padding:10px 30px; font-size:58px; line-height:1.15; box-shadow:7px 7px 0 {INK}; transform:rotate(-2deg); }}
.hl em {{ font-style:normal; color:#2E7263; }}
.phone {{ position:absolute; left:50%; top:330px; width:420px; margin-left:-210px; border:8px solid {INK}; border-radius:54px; overflow:hidden; box-shadow:16px 16px 0 {INK}; background:#fff; transform:rotate(3deg); }}
.phone img {{ display:block; width:100%; }}
.cnt2 {{ position:absolute; bottom:40px; left:0; right:0; text-align:center; font-size:36px; }}
.cnt2 span {{ display:inline-block; background:{INK}; color:{PAPER}; border-radius:40px; padding:10px 30px; }}
.big1 {{ position:absolute; top:150px; left:50px; right:50px; text-align:center; font-size:92px; line-height:1.08; color:{PAPER}; -webkit-text-stroke:8px {INK}; paint-order:stroke fill; text-shadow:8px 8px 0 {INK}; }}
.big1 i {{ font-style:normal; color:#FFE66D; }}
.endbox {{ position:absolute; left:110px; right:110px; }}
.endbox div {{ background:{PAPER}; border:5px solid {INK}; border-radius:30px; padding:18px; margin-top:22px; text-align:center; font-size:48px; box-shadow:8px 8px 0 {INK}; }}
"""

def crop(k):                                                     # the phone's screen out of the store picture (below its headline)
    src = os.path.join(SHOTS, f"appstore-{k}.png"); dst = os.path.join(OUT, f"_screen{k}.png")
    Image.open(src).crop((178, 600, 1142, 2740)).save(dst); return dst

def slides():
    out = {}; n = len(SLIDES)
    shot = lambda k, rot=3, top=300, w=470: f'<div class="phone" style="top:{top}px;width:{w}px;margin-left:-{w // 2}px;transform:rotate({rot}deg)"><img src="file://{crop(k)}"></div>'
    out["1"] = (f'<body style="background:#F49AC1">{P.sparkles(5, ["#fff", "#FFE66D", "#9B6BFF"])}<div class="top">{P.S.BRAND}<div class="cnt">swipe →</div></div>'
                f'<div class="big1">Learning the Arabic<br>of my salah in<br><i>5 minutes a day</i></div>{shot(1, -4, 520, 320)}'
                '<div class="cnt2"><span>Here’s how it works →</span></div></body>')
    for i, (k, head, lit, bg, dc) in enumerate(SLIDES, 2):
        out[str(i)] = (f'<body style="background:{bg}">{P.sparkles(i * 3, dc)}<div class="top">{P.S.BRAND}<div class="cnt">{i - 1} / {n}</div></div>'
                       f'<div class="hl"><span>{head.replace(lit, f"<em>{lit}</em>")}</span></div>{shot(k, (-3, 3)[i % 2])}</body>')
    out[str(n + 2)] = (f'<body style="background:#2E7263">{P.sparkles(77, ["#FFC93C", "#fff", "#FF7A59"])}<div class="top">{P.S.BRAND}<div class="cnt">{n + 1} / {n + 1}</div></div>'
                       '<div class="big1" style="top:200px">Try it<br><i>free for a week</i></div>'
                       '<div class="endbox" style="top:560px"><div>No card needed</div><div>Lessons, reviews, salah, Ask Rafiq</div><div style="background:#FFE66D">🔗 Link in bio</div></div>'
                       '<div class="cnt2"><span>rafiq-arabic.com</span></div></body>')
    return out

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=P.S.CHROME if os.path.exists(P.S.CHROME) else None)
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        for k, body in slides().items():
            tmp = os.path.join(OUT, "_s.html"); open(tmp, "w").write(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>{P.tall(body, int(k) * 7)}</html>')
            pg.goto("file://" + tmp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(400)
            pg.screenshot(path=os.path.join(OUT, f"app-{int(k):02d}.jpg"), type="jpeg", quality=92)
        b.close()
    for f in os.listdir(OUT):
        if f.startswith("_"): os.remove(os.path.join(OUT, f))
    print("app ->", OUT)
