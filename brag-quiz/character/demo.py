import json, os, sys
from playwright.sync_api import sync_playwright
SEGS = json.load(open("/tmp/claude-0/char/segs.json")); FPS = 30; DUR = 20.2
th = sys.argv[1]; times = [float(x) for x in sys.argv[2:]]
os.makedirs(f"/tmp/claude-0/char/f_{th}", exist_ok=True)
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
    p = b.new_page(viewport={"width": 1080, "height": 1920}); errs = []; p.on("pageerror", lambda e: errs.append(str(e)))
    p.goto("file:///home/user/Rafiq/brag-quiz/character/rafiq.html")
    p.evaluate(f"document.body.className='{th}'; demoInit()"); p.evaluate("document.fonts.ready"); p.wait_for_timeout(400)
    for i, t in enumerate(times or [f / FPS for f in range(int(DUR * FPS))]):
        p.evaluate(f"demo({t}, {json.dumps(SEGS)})" if i == 0 else f"demo({t}, window.__S)") if False else None
    p.evaluate(f"window.__S = {json.dumps(SEGS)}")
    for i, t in enumerate(times or [f / FPS for f in range(int(DUR * FPS))]):
        p.evaluate(f"demo({t}, window.__S)")
        p.screenshot(path=f"/tmp/claude-0/char/f_{th}/{'pv_%05.2f' % t if times else '%05d' % i}.png")
    b.close(); print(th, "errors:", errs[:3])
