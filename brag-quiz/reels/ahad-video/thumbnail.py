#!/usr/bin/env python3
"""YouTube thumbnail for the long Aḥad video (#315; owner, 9 Nov 2026: "research successful YouTube thumbnails"). What the research says
(vidIQ's study of 500 breakout videos, July 2026: a face in 69% of them, 80% of the top 50; a median of five words; guides: 3-5 words, bold,
outlined, one focal point that reads at phone size; no clickbait the video doesn't pay off): his face big on the left, cut out of the
footage on "aḥad" (ahad1.mp4 at 150.1 s), a white rim to lift him off the background; on the right أَحَد huge in gold over Makkah at midday
(the a_makkah graphic, darkened), with HIS ONLY WORD above it. 1280 x 720.

  python3 thumbnail.py CUTOUT.png BG.png OUT.png       (CUTOUT: rembg of the frame; BG: a_makkah at 3 s, cropped to 16:9)
"""
import os, sys
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
CUT, BG, OUT = sys.argv[1:4]
F = os.path.join(ROOT, "brag-quiz", "fonts")
HTML = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family:Anton; src:url("file://{F}/anton-latin-400-normal.woff2"); }}
@font-face {{ font-family:Am; src:url("file://{F}/amiri-arabic-700-normal.woff2"); }}
body {{ margin:0; width:1280px; height:720px; overflow:hidden; background:#120a05; }}
.bg {{ position:absolute; inset:0; background:url("file://{BG}") center/cover; filter:saturate(1.2) brightness(.55) contrast(1.15); }}
.heat {{ position:absolute; inset:0; background:radial-gradient(ellipse at 74% 30%, rgba(255,190,90,.55), rgba(0,0,0,0) 55%),
        linear-gradient(90deg, rgba(10,6,3,.85) 0%, rgba(10,6,3,.2) 45%, rgba(10,6,3,.35) 100%); }}
.me {{ position:absolute; left:-170px; bottom:-120px; height:900px; filter:drop-shadow(0 0 0 #fff) drop-shadow(6px 0 0 #fff) drop-shadow(-6px 0 0 #fff)
      drop-shadow(0 6px 0 #fff) drop-shadow(0 -6px 0 #fff) drop-shadow(0 24px 40px rgba(0,0,0,.7)) saturate(1.15) contrast(1.08); }}
.top {{ position:absolute; right:30px; top:28px; width:640px; text-align:center; font-family:Anton; font-size:96px; line-height:1; color:#fff;
       letter-spacing:.01em; -webkit-text-stroke:5px #120a05; paint-order:stroke fill; text-shadow:0 8px 24px rgba(0,0,0,.6); }}
.top em {{ font-style:normal; color:#ff4a3d; }}
.ar {{ position:absolute; right:30px; top:225px; width:640px; text-align:center; font-family:Am; font-size:265px; line-height:1.25; direction:rtl;
      color:#F2C14E; -webkit-text-stroke:10px #120a05; paint-order:stroke fill;
      text-shadow:0 0 50px rgba(255,190,80,.75), 0 14px 30px rgba(0,0,0,.7); }}
.tl {{ position:absolute; right:40px; bottom:46px; width:640px; text-align:center; font-family:Anton; font-size:46px; letter-spacing:.24em; color:#F1ECE0;
      -webkit-text-stroke:3px #120a05; paint-order:stroke fill; }}
</style></head><body><div class="bg"></div><div class="heat"></div>
<img class="me" src="file://{CUT}">
<div class="top">HIS <em>ONLY</em> WORD</div><div class="ar">أَحَد</div></body></html>"""
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium" if os.path.exists("/opt/pw-browsers/chromium") else None); p = b.new_page(viewport={"width": 1280, "height": 720})
    tmp = OUT + ".html"; open(tmp, "w").write(HTML); p.goto("file://" + tmp); p.evaluate("document.fonts.ready"); p.wait_for_timeout(500)
    p.screenshot(path=OUT); b.close(); os.remove(tmp)
print(OUT)
