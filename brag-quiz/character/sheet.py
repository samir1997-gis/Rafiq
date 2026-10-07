import sys
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
    for th in ("light", "dark"):
        p = b.new_page(viewport={"width": 2160, "height": 1350})
        errs = []; p.on("pageerror", lambda e: errs.append(str(e)))
        p.goto("file:///home/user/Rafiq/brag-quiz/character/rafiq.html")
        p.evaluate(f"document.body.className='{th}'; sheet()"); p.evaluate("document.fonts.ready"); p.wait_for_timeout(500)
        p.screenshot(path=f"/tmp/claude-0/char/sheet_{th}.png", full_page=True); print(th, errs)
    b.close()
