import sys, os
from playwright.sync_api import sync_playwright
FPS, DUR = 30, 37.4
times = [float(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else None
os.makedirs("ov", exist_ok=True); os.makedirs("pv", exist_ok=True)
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
    p = b.new_page(viewport={"width": 1080, "height": 1920})
    errs = []; p.on("pageerror", lambda e: errs.append(str(e)))
    p.goto("file:///tmp/claude-0/edit2/overlay_light.html"); p.evaluate("document.fonts.ready"); p.wait_for_timeout(400)
    if times:
        for t in times:
            p.evaluate(f"update({t})"); p.screenshot(path=f"pv/{t:.2f}.png", omit_background=True)
    else:
        for f in range(int(round(DUR * FPS))):
            p.evaluate(f"update({f / FPS})"); p.screenshot(path=f"ov/{f:05d}.png", omit_background=True)
    b.close()
print("errors:", errs[:3])
