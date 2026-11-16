"""The body explorer (#202, redesigned #392), Practise → Everyday essentials → The body:
  - the essentials menu has a card for it: "46 words · tap to hear"
  - the words: every zone the words name is in the drawing, every word is in a view with a dot,
    and the words also in vocab-data.js spell them as it does (with ال)
  - it opens full screen; each part has a dot; tap a dot (or the shape) → it's said, lit up and
    shown on the card (Arabic, English, how it's said); "Look closer" zooms into a region; ‹ and
    Escape zoom out; Turn round shows the back; ✕ goes back to the menu
  - Find it: the word is asked, the right dot moves on, a wrong one comes back later, and the end
    card says how many were found first time
  - in every view, on a phone and a wide screen: dots inside the stage, above the card, none on top
    of another

  python3 .claude/skills/webapp-testing/scripts/with_server.py \
    --server "python3 -m http.server 8765 >/dev/null 2>&1" --port 8765 -- python3 tests/body_explorer.py
"""
import os, sys
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8765/"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
# every view, and the dots to look closer at from the whole body to reach it ("turn" = Turn round)
ROUTES = {"body": [], "back": ["turn"], "head": ["head"], "mouth": ["head", "mouth"], "arm": ["arm"], "hand": ["arm", "hand"],
          "leg": ["leg"], "foot": ["leg", "foot"], "torso": ["torso"], "inside": ["torso", "inside"]}

def open_body(ctx, reduce=False):
    p = ctx.new_page(); errors = []
    p.on("pageerror", lambda e: errors.append(str(e)))
    if reduce: p.emulate_media(reduced_motion="reduce")
    p.goto(BASE + "practise.html#essentials"); p.wait_for_timeout(900)
    # what gets said: audio.js's RQ.speak, recorded
    p.evaluate("window.SAID = []; RQ.speak = (t, el, after) => { SAID.push(t); if(after) after(); }")
    card = p.inner_text("[data-body]")
    p.click("[data-body]"); p.wait_for_selector(".bx-dot"); p.wait_for_timeout(300)
    return p, errors, card

said = lambda p: p.evaluate("SAID[SAID.length - 1] || ''")
title = lambda p: p.evaluate("document.querySelector('.bx-crumbs').firstChild.textContent.trim()")
dots = lambda p: p.evaluate("[...document.querySelectorAll('.bx-dot')].map(b => b.dataset.id)")
card = lambda p: " ".join(p.inner_text(".bx-card").split())
def tap(p, pid, wait=250):
    p.click(f'.bx-dot[data-id="{pid}"]'); p.wait_for_timeout(wait)
def closer(p, pid, wait=1100):
    if pid == "turn": p.click(".bx-turn")
    else: tap(p, pid, 150); p.click(".bx-more")
    p.wait_for_timeout(wait)

def layout_ok(p):
    """dots inside the stage, clear of the card, and no dot's centre inside another dot"""
    return p.evaluate("""(() => {
      const s = document.querySelector('.bx-stage').getBoundingClientRect(), c = document.querySelector('.bx-card').getBoundingClientRect();
      const r = [...document.querySelectorAll('.bx-dot')].map(b => b.getBoundingClientRect());
      const mid = a => [(a.left + a.right) / 2, (a.top + a.bottom) / 2];
      const inside = r.every(a => a.left >= s.left && a.right <= s.right && a.top >= s.top && a.bottom <= c.top + 8);
      const apart = r.every((a, i) => r.every((b, j) => i >= j || Math.hypot(mid(a)[0] - mid(b)[0], mid(a)[1] - mid(b)[1]) >= 22));
      return inside && apart;
    })()""")

def main():
    ok, errors = [], []
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME if os.path.exists(CHROME) else None)
        ctx = b.new_context(viewport={"width": 390, "height": 844})
        ctx.route("**/@supabase/**", lambda r: r.abort())
        ctx.route("https://fonts.googleapis.com/**", lambda r: r.abort())
        ctx.add_init_script("localStorage.setItem('rafiq_plan','complete')")
        p, errs, menu = open_body(ctx)

        ok.append(("menu card: " + " ".join(menu.split()), "The body" in menu and "46 words · tap to hear" in menu))
        data = p.evaluate("""(() => {
          const views = RafiqBody.VIEWS, ids = new Set(BODY_WORDS.map(w => w.id)), shown = new Set();
          Object.values(views).forEach(v => v.parts.forEach(x => shown.add(x)));
          return {
            noZone: BODY_WORDS.filter(w => !document.getElementById(w.svgZoneId)).map(w => w.id),
            notShown: BODY_WORDS.filter(w => w.level > 0 && !shown.has(w.id)).map(w => w.id),
            unknown: [...shown].filter(x => !ids.has(x)),
            noPoint: [...shown].filter(x => !RafiqBody.AT[x]),
            lost: BODY_WORDS.filter(w => w.level > 0 && !(views[w.parent] && views[w.parent].parts.includes(w.id)) && w.id !== 'back').map(w => w.id),
            vocabOff: BODY_WORDS.filter(w => w.vocab && !(w.vocabAr && w.ar.includes(w.vocabAr))).map(w => w.id),
            shape: BODY_WORDS.every(w => ['id','ar','en','tr','level','parent','svgZoneId','audioId'].every(k => k in w)),
            head: BODY_WORDS.find(w => w.id === 'head').ar };
        })()""")
        ok.append(("every word's zone is in the drawing " + str(data["noZone"]), not data["noZone"]))
        ok.append(("every word is in a view " + str(data["notShown"]), not data["notShown"]))
        ok.append(("views only name known words, each with a dot " + str(data["unknown"] + data["noPoint"]), not data["unknown"] and not data["noPoint"]))
        ok.append(("each word is dotted in its parent's view " + str(data["lost"]), not data["lost"]))
        ok.append(("words in vocab-data.js spelt as there " + str(data["vocabOff"]), not data["vocabOff"]))
        ok.append(("entries have id, ar, en, tr, level, parent, svgZoneId, audioId", data["shape"]))
        ok.append(("the head's Arabic comes from vocab-data.js: " + data["head"], data["head"] == "الرَّأْس"))

        full = p.evaluate("(() => { const r = document.querySelector('.bx-full').getBoundingClientRect(); return r.width >= innerWidth && r.height >= innerHeight; })()")
        ok.append(("it fills the screen", full))
        ok.append(("whole body: 7 dots, no ‹ yet, nothing said: " + title(p), len(dots(p)) == 7 and title(p) == "Body" and p.is_hidden(".bx-up") and said(p) == ""))
        ok.append(("the card says what to do: " + card(p)[:40], "Tap a dot to hear it" in card(p) and p.is_visible(".bx-play")))

        tap(p, "head")
        ok.append(("tap the head's dot: said " + said(p), said(p) == "الرَّأْس"))
        ok.append(("… on the card, one word: " + card(p), "الرَّأْس" in card(p) and "the head" in card(p) and "ar-raʾs" in card(p)
                   and "on" in p.get_attribute('.bx-dot[data-id="head"]', "class")
                   and p.evaluate("document.getElementById('z-head').classList.contains('on')")))
        ok.append(("… still the whole body until Look closer", title(p) == "Body" and p.is_visible(".bx-more")))
        p.click(".bx-more"); p.wait_for_timeout(1100)
        ok.append(("Look closer: the head, 9 dots: " + title(p), title(p) == "Head" and len(dots(p)) == 9 and p.is_visible(".bx-up")))
        ok.append(("the face is drawn only here", p.evaluate("getComputedStyle(document.querySelector('.face')).opacity") == "1"))
        p.click("#z-ear ellipse >> nth=1"); p.wait_for_timeout(250)         # the shape (the other ear), not the dot
        ok.append(("tap the ear in the drawing: said " + said(p), "the ear" in card(p) and said(p) == p.inner_text(".bx-card .a")))
        closer(p, "mouth"); tap(p, "teeth")
        ok.append(("the mouth has its own view; a pair says both forms: " + said(p), title(p) == "Mouth" and said(p) == "السِّنّ، الأَسْنان"))
        ok.append(("heard count: " + p.inner_text(".bx-crumbs small"), p.inner_text(".bx-crumbs small") == "1 of 3 heard"))
        p.click(".bx-up"); p.wait_for_timeout(1100)
        ok.append(("‹ zooms out one step: " + title(p), title(p) == "Head"))
        p.keyboard.press("Escape"); p.wait_for_timeout(1100)
        ok.append(("Escape zooms out", title(p) == "Body" and p.evaluate("getComputedStyle(document.querySelector('.face')).opacity") == "0"))

        closer(p, "turn")
        ok.append(("Turn round: said " + said(p) + ", the back: " + title(p), said(p) == "الظَّهْر" and title(p) == "Back" and dots(p) == ["back"]
                   and p.evaluate("getComputedStyle(document.querySelector('path[data-in=\"back\"]')).opacity") == "1" and p.is_hidden(".bx-play")))
        p.click(".bx-up"); p.wait_for_timeout(1100)
        closer(p, "torso"); closer(p, "inside"); tap(p, "heart")
        ok.append(("torso, inside, the heart: " + said(p), title(p) == "Internal organs" and said(p) == "القَلْب"))
        p.keyboard.press("Escape"); p.wait_for_timeout(1100); p.keyboard.press("Escape"); p.wait_for_timeout(1100)

        # Find it, on the whole body: one wrong tap first, then every one right
        p.click(".bx-play"); p.wait_for_timeout(300)
        want = lambda: p.evaluate("(() => { const a = document.querySelector('.bx-card .a').textContent; return BODY_WORDS.find(w => w.ar === a && RafiqBody.VIEWS.body.parts.includes(w.id)).id; })()")
        first = want()
        ok.append(("Find it asks for a part and says it: " + card(p), "tap this part" in card(p).lower() and said(p) == p.inner_text(".bx-card .a") and p.is_hidden(".bx-turn")))
        wrong = next(d for d in dots(p) if d != first)
        tap(p, wrong, 700)
        ok.append(("a wrong tap moves to another word; the missed one comes back later", want() != first and title(p) == "Body"))
        n = 0
        while p.locator(".bx-again").count() == 0 and n < 12:
            tap(p, want(), 900); n += 1
        ok.append((f"all 7 found in {n} taps: " + card(p), n == 7 and "Found all 7" in card(p) and "6 of 7 first time" in card(p)))
        p.click(".bx-done"); p.wait_for_timeout(300)
        ok.append(("Explore goes back to the dots", "Tap a dot to hear it" in card(p) and len(dots(p)) == 7))
        p.click(".bx-x"); p.wait_for_timeout(300)
        ok.append(("✕ goes back to the menu, and the page scrolls again", p.is_visible("[data-body]") and p.locator(".bx-full").count() == 0
                   and p.evaluate("document.documentElement.style.overflow") != "hidden"))
        errors += errs; p.close()

        # every view lays out cleanly, on a phone, a small phone and a wide screen (and with reduced motion)
        for w, h, reduce in ((390, 844, True), (360, 640, True), (900, 900, False)):
            c2 = b.new_context(viewport={"width": w, "height": h})
            c2.route("**/@supabase/**", lambda r: r.abort())
            c2.add_init_script("localStorage.setItem('rafiq_plan','complete')")
            bad = []
            for view, route in ROUTES.items():
                q, e2, _ = open_body(c2, reduce)
                for pid in route: closer(q, pid, 150 if reduce else 1100)
                if not layout_ok(q): bad.append(view)
                errors += e2; q.close()
            ok.append((f"{w}×{h}{' (reduced motion)' if reduce else ''}: dots fit, clear of the card, none on another {bad}", not bad))
            c2.close()
        b.close()

    for name, good in ok: print(("ok   " if good else "FAIL ") + name)
    for e in errors: print("page error:", e)
    sys.exit(0 if all(g for _, g in ok) and not errors else 1)

if __name__ == "__main__":
    main()
