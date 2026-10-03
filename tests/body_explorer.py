"""The body explorer (#202), Practise → Everyday essentials → The body:
  - the essentials menu has a card for it: "46 words · tap to hear"
  - the words: every zone the words name is in the drawing, every word is in a view, and the
    words also in vocab-data.js spell them as it does (with ال)
  - tap a region (label or shape) → it's said and the drawing zooms in; the breadcrumb and
    ← Back take you out again; the back turns the figure round
  - tap a part → it's said (both forms of a pair), lit up, and named at the end of the breadcrumb
  - in every view, on a phone and a wide screen: labels inside the drawing, none overlapping

  python3 .claude/skills/webapp-testing/scripts/with_server.py \
    --server "python3 -m http.server 8765 >/dev/null 2>&1" --port 8765 -- python3 tests/body_explorer.py
"""
import os, re, sys
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8765/"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
# every view, and the taps from the whole body that reach it
ROUTES = {"body": [], "back": ["back"], "head": ["head"], "arm": ["arm"], "hand": ["arm", "hand"],
          "leg": ["leg"], "foot": ["leg", "foot"], "torso": ["torso"], "inside": ["torso", "inside"]}

def open_body(ctx, reduce=False):
    p = ctx.new_page(); errors = []
    p.on("pageerror", lambda e: errors.append(str(e)))
    if reduce: p.emulate_media(reduced_motion="reduce")
    p.goto(BASE + "practise.html#essentials"); p.wait_for_timeout(900)
    # what gets said: audio.js's RQ.speak, recorded
    p.evaluate("window.SAID = []; RQ.speak = (t, el, after) => { SAID.push(t); if(after) after(); }")
    card = p.inner_text("[data-body]")
    p.click("[data-body]"); p.wait_for_selector(".bx-lab"); p.wait_for_timeout(300)
    return p, errors, card

said = lambda p: p.evaluate("SAID[SAID.length - 1] || ''")
crumbs = lambda p: re.sub(r"\s*›\s*", " › ", " ".join(p.inner_text(".bx-crumbs").split()))
labels = lambda p: p.evaluate("[...document.querySelectorAll('.bx-lab')].map(b => b.dataset.id)")
def tap(p, pid, wait=1200):
    p.click(f'.bx-lab[data-id="{pid}"]'); p.wait_for_timeout(wait)

def layout_ok(p):
    """labels inside the stage and not overlapping each other"""
    return p.evaluate("""(() => {
      const s = document.querySelector('.bx-stage').getBoundingClientRect();
      const r = [...document.querySelectorAll('.bx-lab')].map(b => b.getBoundingClientRect());
      const inside = r.every(a => a.left >= s.left - 1 && a.right <= s.right + 1 && a.top >= s.top - 1 && a.bottom <= s.bottom + 1);
      const apart = r.every((a, i) => r.every((b, j) => i >= j || a.right <= b.left || b.right <= a.left || a.bottom <= b.top || b.bottom <= a.top));
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
        p, errs, card = open_body(ctx)

        ok.append(("menu card: " + " ".join(card.split()), "The body" in card and "46 words · tap to hear" in card))
        data = p.evaluate("""(() => {
          const views = RafiqBody.VIEWS, ids = new Set(BODY_WORDS.map(w => w.id)), shown = new Set();
          Object.values(views).forEach(v => v.l.concat(v.r).forEach(x => shown.add(x)));
          return {
            noZone: BODY_WORDS.filter(w => !document.getElementById(w.svgZoneId)).map(w => w.id),
            notShown: BODY_WORDS.filter(w => w.level > 0 && !shown.has(w.id)).map(w => w.id),
            unknown: [...shown].filter(x => !ids.has(x)),
            noPoint: [...shown].filter(x => !RafiqBody.AT[x]),
            vocabOff: BODY_WORDS.filter(w => w.vocab && !(w.vocabAr && w.ar.includes(w.vocabAr))).map(w => w.id),
            shape: BODY_WORDS.every(w => ['id','ar','en','tr','level','parent','svgZoneId','audioId'].every(k => k in w)),
            head: BODY_WORDS.find(w => w.id === 'head').ar };
        })()""")
        ok.append(("every word's zone is in the drawing " + str(data["noZone"]), not data["noZone"]))
        ok.append(("every word is in a view " + str(data["notShown"]), not data["notShown"]))
        ok.append(("views only name known words, each with a point " + str(data["unknown"] + data["noPoint"]), not data["unknown"] and not data["noPoint"]))
        ok.append(("words in vocab-data.js spelt as there " + str(data["vocabOff"]), not data["vocabOff"]))
        ok.append(("entries have id, ar, en, tr, level, parent, svgZoneId, audioId", data["shape"]))
        ok.append(("the head's Arabic comes from vocab-data.js: " + data["head"], data["head"] == "الرَّأْس"))

        ok.append(("whole body: 10 regions", len(labels(p)) == 10 and crumbs(p) == "Body"))
        ok.append(("no ← Back at the top", p.is_hidden(".bx-up")))

        tap(p, "head")
        ok.append(("tap the head: said " + said(p), said(p) == "الرَّأْس"))
        ok.append(("… zoomed in: " + crumbs(p), crumbs(p) == "Body › Head" and len(labels(p)) == 12))
        p.click("#z-eye ellipse >> nth=0"); p.wait_for_timeout(200)       # the shape, not the label
        ok.append(("tap the eye in the drawing: said " + said(p), said(p) == "العَيْن"))
        ok.append(("… lit up and named: " + crumbs(p), crumbs(p) == "Body › Head › eye"
                   and p.evaluate("document.getElementById('z-eye').classList.contains('on')")
                   and "on" in p.get_attribute('.bx-lab[data-id="eye"]', "class")))
        tap(p, "teeth", 200)
        ok.append(("a pair says both forms: " + said(p), said(p) == "السِّنّ، الأَسْنان"))
        p.click(".bx-up"); p.wait_for_timeout(1200)
        ok.append(("← Back zooms out: " + crumbs(p), crumbs(p) == "Body" and len(labels(p)) == 10))

        tap(p, "arm"); tap(p, "hand")
        ok.append(("arm, then hand: " + crumbs(p), crumbs(p) == "Body › Arm › Hand"))
        tap(p, "thumb", 200)
        ok.append(("… the thumb: " + said(p), said(p) == "الإِبْهام" and crumbs(p) == "Body › Arm › Hand › thumb"))
        p.click('.bx-crumbs button[data-i="0"]'); p.wait_for_timeout(1200)
        ok.append(("the breadcrumb's Body goes straight back: " + crumbs(p), crumbs(p) == "Body"))

        tap(p, "back")
        ok.append(("the back turns the figure round: " + crumbs(p), crumbs(p) == "Body › Back" and labels(p) == ["back"]
                   and p.evaluate("getComputedStyle(document.querySelector('[data-in=\"back\"]')).opacity") == "1"))
        p.keyboard.press("Escape"); p.wait_for_timeout(1200)
        ok.append(("Escape zooms out", crumbs(p) == "Body"))

        tap(p, "torso"); tap(p, "inside"); tap(p, "heart", 200)
        ok.append(("torso, inside, the heart: " + crumbs(p), crumbs(p) == "Body › Torso / trunk › Internal organs › heart" and said(p) == "القَلْب"))
        p.click(".es-back"); p.wait_for_timeout(300)
        ok.append(("‹ All essentials goes back to the menu", p.is_visible("[data-body]")))
        errors += errs; p.close()

        # every view lays out cleanly, on a phone and a wide screen (and with reduced motion)
        for w, reduce in ((390, True), (900, False)):
            c2 = b.new_context(viewport={"width": w, "height": 900})
            c2.route("**/@supabase/**", lambda r: r.abort())
            c2.add_init_script("localStorage.setItem('rafiq_plan','complete')")
            bad = []
            for view, route in ROUTES.items():
                q, e2, _ = open_body(c2, reduce)
                for pid in route: tap(q, pid, 100 if reduce else 1200)
                if not layout_ok(q): bad.append(view)
                errors += e2; q.close()
            ok.append((f"{w}px wide{' (reduced motion)' if reduce else ''}: labels fit and don't overlap {bad}", not bad))
            c2.close()
        b.close()

    for name, good in ok: print(("ok   " if good else "FAIL ") + name)
    for e in errors: print("page error:", e)
    sys.exit(0 if all(g for _, g in ok) and not errors else 1)

if __name__ == "__main__":
    main()
