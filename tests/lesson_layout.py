"""Lesson screens are laid out like Pray along (#151): heading pinned at the top, the exercise
centred, the page fitting the phone without scrolling, and listening exercises showing
the cue (🔊 Listen, then 🗣 Now say it).

  python3 .claude/skills/webapp-testing/scripts/with_server.py \
    --server "python3 -m http.server 8765 >/dev/null 2>&1" --port 8765 -- python3 tests/lesson_layout.py
"""
import os, sys
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8765/"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

def main():
    ok = []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME if os.path.exists(CHROME) else None, args=["--autoplay-policy=no-user-gesture-required"])
        ctx = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
        ctx.route("**/@supabase/**", lambda r: r.abort())          # signed out: the app runs from local progress
        pg = ctx.new_page(); errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.goto(BASE + "dashboard.html", wait_until="load"); pg.wait_for_timeout(600)
        pg.evaluate("RafiqPath.units().slice(0,2).forEach(u => RafiqPath.steps(u).forEach(s => RafiqPath.complete(u.n, s.key))); RafiqPath.recapDone()")   # straight into the lesson, no recap first
        n = pg.evaluate("RafiqPath.units().find(u => !u.pre).n")
        for step, cue in (("words1", True), ("listen", True), ("grammar", False), ("speak", False)):
            pg.goto(f"{BASE}learn.html?u={n}&s={step}", wait_until="load")
            seen = []
            for _ in range(40):
                c = pg.evaluate("(document.querySelector('.x-mid .pa-cue') || {}).textContent || ''").strip()
                if c and (not seen or seen[-1] != c): seen.append(c)
                pg.wait_for_timeout(100)
            v = pg.evaluate("""[!!document.querySelector('.x-screen > .x-top .kicker'), !!document.querySelector('.x-screen > .x-mid'),
              document.documentElement.scrollHeight <= innerHeight]""")
            ok.append((f"{step}: heading pinned, exercise centred, fits the screen", all(v)))
            if cue: ok.append((f"{step}: cue Listen → Now say it {seen}", seen[:1] == ['🔊Listen'] and '🗣Now say it' in seen))
        ok.append(("no page errors", not errors))
        b.close()
    for name, good in ok: print(("ok   " if good else "FAIL ") + name)
    sys.exit(0 if all(g for _, g in ok) else 1)

if __name__ == "__main__":
    main()
