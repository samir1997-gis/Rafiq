# Stills of the built page at given seconds (the timeline seeked in Chromium), tiled into out/preview.png
import os, sys
from playwright.sync_api import sync_playwright
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); ts = [float(x) for x in sys.argv[1:]]
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium"); p = b.new_page(viewport={"width": 1080, "height": 1920})
    p.goto("file://" + os.path.join(H, "out/cream/index.html")); p.evaluate("document.fonts.ready"); p.wait_for_timeout(500)
    ims = []
    for t in ts:
        p.evaluate(f"void window.__timelines.main.seek({t}, false)"); p.wait_for_timeout(60)
        f = f"/tmp/claude-0/-home-user-Rafiq/bf1032a0-f0b5-5e18-93a0-773acecc0718/scratchpad/pv{t}.png"; p.screenshot(path=f)
        ims.append(Image.open(f).resize((270, 480)))
    b.close()
cols = min(8, len(ims)); rows = (len(ims) + cols - 1) // cols; sh = Image.new("RGB", (270 * cols, 480 * rows), "white")
for k, im in enumerate(ims): sh.paste(im, ((k % cols) * 270, (k // cols) * 480))
sh.save(os.path.join(H, "out/preview.png")); print(len(ims))
