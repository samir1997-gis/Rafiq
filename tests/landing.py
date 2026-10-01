"""The landing page (index.html, #176):
  - "What's inside" is eight compact tiles: 2 across on a phone, 4 on a computer; a tap opens one (and closes it)
  - on a computer, hovering a box lifts it, and a tile's detail drops down over the row below (nothing moves)
  - sections fade in as they're scrolled to, and every one ends up visible; the numbers count up to the real values
  - with reduced motion, everything is there at once, nothing moves
  - no sideways scroll on a phone, no page errors

  python3 .claude/skills/webapp-testing/scripts/with_server.py \
    --server "python3 -m http.server 8765 >/dev/null 2>&1" --port 8765 -- python3 tests/landing.py
  SHOTS=dir to save screenshots.
"""
import os, sys
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8765/"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
SHOTS = os.environ.get("SHOTS")

def page_for(b, errors, **kw):
    c = b.new_context(**kw)
    c.route("**/@supabase/**", lambda r: r.abort()); c.route("https://fonts.googleapis.com/**", lambda r: r.abort())
    p = c.new_page(); p.on("pageerror", lambda e: errors.append(str(e)))
    return c, p

def scroll_through(p):
    h = p.evaluate("document.body.scrollHeight")
    for y in range(0, h + 800, 400):
        p.mouse.wheel(0, 400); p.wait_for_timeout(60)
    p.wait_for_timeout(900)

def main():
    ok, errors = [], []
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME if os.path.exists(CHROME) else None)

        # phone
        c, p = page_for(b, errors, viewport={"width": 390, "height": 844}, has_touch=True)
        p.goto(BASE + "index.html"); p.wait_for_timeout(600)
        ok.append(("phone: no sideways scroll", p.evaluate("document.documentElement.scrollWidth") <= 390))
        hidden = p.evaluate("[...document.querySelectorAll('.reveal')].filter(e => getComputedStyle(e).opacity === '0').length")
        ok.append(("phone: sections further down wait to fade in (%d)" % hidden, hidden > 5))
        cols = p.evaluate("getComputedStyle(document.querySelector('.tiles')).gridTemplateColumns.split(' ').length")
        ok.append(("phone: 8 tiles, 2 across", p.locator(".tile").count() == 8 and cols == 2))
        scroll_through(p)
        left = p.evaluate("[...document.querySelectorAll('.reveal')].filter(e => getComputedStyle(e).opacity !== '1').length")
        ok.append(("phone: after scrolling, everything is visible (%d left)" % left, left == 0))
        ok.append(("phone: the numbers count up to 12 and 785", p.evaluate("[...document.querySelectorAll('[data-count]')].map(b => b.textContent).join(',')") == "12,785"))
        t = p.locator(".tile").nth(2); t.scroll_into_view_if_needed()
        closed = t.evaluate("e => e.querySelector('.more > span').getBoundingClientRect().height")
        t.tap(); p.wait_for_timeout(450)
        opened = t.evaluate("e => e.querySelector('.more > span').getBoundingClientRect().height")
        ok.append(("phone: tapping Your salah opens its detail (%d → %dpx)" % (closed, opened), closed < 2 and opened > 30 and t.get_attribute("aria-expanded") == "true"))
        t.tap(); p.wait_for_timeout(450)
        ok.append(("phone: tapping again closes it", t.get_attribute("aria-expanded") == "false"))
        p.locator(".note summary").first.tap(); p.wait_for_timeout(200)
        ok.append(("phone: Good to know folds open", p.evaluate("document.querySelector('.note').open")))
        if SHOTS: p.evaluate("window.scrollTo(0,0)"); p.wait_for_timeout(300); p.screenshot(path=SHOTS + "/landing-phone.png", full_page=True)
        c.close()

        # computer
        c, p = page_for(b, errors, viewport={"width": 1280, "height": 800})
        p.goto(BASE + "index.html"); p.wait_for_timeout(600); scroll_through(p)
        cols = p.evaluate("getComputedStyle(document.querySelector('.tiles')).gridTemplateColumns.split(' ').length")
        ok.append(("computer: 4 tiles across", cols == 4))
        t = p.locator(".tile").nth(1); t.scroll_into_view_if_needed(); p.wait_for_timeout(300)
        box = t.bounding_box(); p.mouse.move(box["x"] + 30, box["y"] + 30); p.wait_for_timeout(500)
        lift = p.evaluate("(() => { const m = getComputedStyle(document.querySelectorAll('.tile')[1]).transform; return m === 'none' ? 0 : new DOMMatrix(m).m42; })()")
        more = t.evaluate("e => e.querySelector('.more').getBoundingClientRect().height")
        below = p.locator(".tile").nth(5).bounding_box()["y"]
        p.mouse.move(5, 5); p.wait_for_timeout(450)
        moved = abs(p.locator(".tile").nth(5).bounding_box()["y"] - below)
        ok.append(("computer: hovering a tile lifts it (%.1fpx) and shows its detail (%dpx) without moving the row below (%dpx)" % (lift, more, moved),
                   lift < -2 and more > 30 and moved < 1))
        pl = p.locator(".plan.best"); pl.scroll_into_view_if_needed(); bb = pl.bounding_box(); p.mouse.move(bb["x"] + 60, bb["y"] + 60); p.wait_for_timeout(450)
        glow = p.evaluate("getComputedStyle(document.querySelector('.plan.best')).boxShadow")
        ok.append(("computer: hovering a plan lifts it with a glow", glow != "none"))
        if SHOTS:
            p.evaluate("window.scrollTo(0, document.querySelector('.tiles').getBoundingClientRect().top + scrollY - 120)"); p.wait_for_timeout(300)
            t.hover(); p.wait_for_timeout(500); p.screenshot(path=SHOTS + "/landing-desktop.png")
        c.close()

        # reduced motion
        c, p = page_for(b, errors, viewport={"width": 390, "height": 844}, reduced_motion="reduce")
        p.goto(BASE + "index.html"); p.wait_for_timeout(400)
        left = p.evaluate("[...document.querySelectorAll('.reveal')].filter(e => getComputedStyle(e).opacity !== '1').length")
        ok.append(("reduced motion: everything there at once", left == 0 and not p.evaluate("document.documentElement.classList.contains('js-motion')")))
        c.close()
        b.close()
    ok.append(("no page errors " + "; ".join(e[:120] for e in errors[:3]), not errors))
    for name, good in ok: print(("ok   " if good else "FAIL ") + name)
    sys.exit(0 if all(g for _, g in ok) else 1)

if __name__ == "__main__":
    main()
