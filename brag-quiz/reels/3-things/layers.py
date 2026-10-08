import json, os, sys
from playwright.sync_api import sync_playwright
C = json.load(open("config.json")); N = 1677
times = [float(x) for x in sys.argv[1:]]
for d in ("back", "front", "pv"): os.makedirs(d, exist_ok=True)
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
    p = b.new_page(viewport={"width": 1080, "height": 1920}); errs = []; p.on("pageerror", lambda e: errs.append(str(e)))
    p.goto("file:///tmp/claude-0/edit3/layers.html"); p.evaluate(f"C = {json.dumps(C)}"); p.evaluate("document.fonts.ready"); p.wait_for_timeout(500)
    todo = [(None, t) for t in times] if times else [(i, i / 30) for i in range(N)]
    for i, t in todo:
        for L in ("back", "front"):
            p.evaluate(f"update({t}, '{L}')")
            if L == "front": p.wait_for_timeout(0)
            p.evaluate("Promise.all([...document.images].filter(i => i.offsetParent).map(i => i.decode().catch(() => 0)))")
            p.screenshot(path=f"pv/{L}_{t:.2f}.png" if i is None else f"{L}/{i:05d}.png", omit_background=True)
    b.close(); print("layers done", errs[:3])
