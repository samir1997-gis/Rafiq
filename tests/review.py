"""Review that grows with progress (#158):
  - every unit ends with a unit test; learners already past a unit aren't sent back for it
  - a new word comes back for review tomorrow
  - every two lessons, the next lesson starts with a 5-word recap of earlier words
  - the unit test: 18 questions; below 80% the missed ones are reviewed before a retake,
    missed words come back tomorrow, and a pass opens the next unit

  python3 .claude/skills/webapp-testing/scripts/with_server.py \
    --server "python3 -m http.server 8765 >/dev/null 2>&1" --port 8765 -- python3 tests/review.py
"""
import json, os, sys, datetime
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8765/"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
TOMORROW = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
seen = lambda *ks: {k: {"box": 0, "seen": 1} for k in ks}
U1 = ["words1", "words2", "grammar", "words3", "words4", "practise", "listen", "chat", "speak"]

def page_with(b, mirror, errors, local=None):
    c = b.new_context(viewport={"width": 390, "height": 844})
    c.route("**/@supabase/**", lambda r: r.abort())
    c.route("https://fonts.googleapis.com/**", lambda r: r.abort())
    extra = "".join("localStorage.setItem(%s,%s);" % (json.dumps(k), json.dumps(v)) for k, v in (local or {}).items())
    c.add_init_script("if(!localStorage.getItem('__seeded')){localStorage.setItem('rafiq_progress_mirror',%s);%slocalStorage.setItem('__seeded','1')}"
                      % (json.dumps(json.dumps(mirror)), extra))
    p = c.new_page(); p.on("pageerror", lambda e: errors.append(str(e)))
    return p

kicker = lambda p: p.evaluate("(() => { const k = document.querySelector('.kicker'); return k ? k.textContent.trim() : ''; })()")

def answer(p, right):
    """Answer the question on screen, right or wrong, then Next."""
    p.evaluate("""right => { const x = asking, o = [...document.querySelectorAll('.opt')];
      (right ? o.find(b => b.textContent === x.right) : o.find(b => b.textContent !== x.right)).click(); }""", right)
    p.wait_for_timeout(100)
    p.locator("button.go:not([disabled])").first.click(); p.wait_for_timeout(150)

def main():
    ok, errors = [], []
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME if os.path.exists(CHROME) else None)

        # the test step, and learners already past a unit
        unit1 = seen("p:00|placed", *[f"p:01|{k}" for k in U1])
        p = page_with(b, unit1, errors); p.goto(BASE + "dashboard.html"); p.wait_for_timeout(1500)
        nxt = p.evaluate("(() => { const n = RafiqPath.next(); return n.unit.n + '|' + n.step.key; })()")
        ok.append(("every step of unit 1 but the test: next is the test (" + nxt + ")", nxt == "01|test"))
        ok.append(("unit 2 stays locked until the test is passed", not p.evaluate("RafiqPath.unitOpen('02')"))); p.close()
        p = page_with(b, {**unit1, **seen("p:02|words1")}, errors); p.goto(BASE + "dashboard.html"); p.wait_for_timeout(1500)
        ok.append(("already into unit 2: unit 1 counts as done without its test", p.evaluate("RafiqPath.unitDone(RafiqPath.units().find(u => u.n === '01'))"))); p.close()

        # a new word comes back tomorrow
        p = page_with(b, seen("p:00|placed"), errors); p.goto(BASE + "learn.html?u=01&s=words1"); p.wait_for_timeout(1500)
        p.evaluate("Progress.grade('v:' + RafiqPath.wordsOf(RafiqPath.units().find(u => u.n === '01'), 0)[0].id, 'good', 1)")
        due = p.evaluate("Progress.get('v:' + RafiqPath.wordsOf(RafiqPath.units().find(u => u.n === '01'), 0)[0].id).due")
        ok.append(("a word just met is due tomorrow (" + str(due) + ")", due == TOMORROW)); p.close()

        # the recap: two lessons done, so the next one starts with five earlier words
        met = {**unit1, **seen("p:01|test", "p:02|words1"), **{f"v:{i}": {"box": 3, "seen": 1, "due": "2099-01-01"} for i in range(1, 400)}}
        p = page_with(b, met, errors, {"rafiq_recap": "2"}); p.goto(BASE + "learn.html?u=02&s=words2"); p.wait_for_timeout(1500)
        heads = []
        for _ in range(5):
            heads.append(kicker(p)); answer(p, True)
        ok.append(("recap first: " + " / ".join(heads[:2]), all(h.startswith("Quick recap") for h in heads) and heads[4].endswith("5 of 5")))
        ok.append(("recap result", "5 of 5" in p.inner_text(".done h2")))
        p.locator("button.go").first.click(); p.wait_for_timeout(400)
        ok.append(("then the lesson (" + kicker(p) + ")", kicker(p).startswith("New word")))
        ok.append(("recap counter reset", p.evaluate("localStorage.getItem('rafiq_recap')") == "0"))
        p.close()
        p = page_with(b, met, errors, {"rafiq_recap": "1"}); p.goto(BASE + "learn.html?u=02&s=words2"); p.wait_for_timeout(1500)
        ok.append(("one lesson since the last recap: straight into the lesson", kicker(p).startswith("New word"))); p.close()

        # the unit test: fail, review the mistakes, retake, pass
        p = page_with(b, unit1, errors); p.goto(BASE + "learn.html?u=01&s=test"); p.wait_for_timeout(1500)
        heads, missed_id = [], None
        while kicker(p).startswith("Unit test"):
            heads.append(kicker(p))
            if missed_id is None and p.evaluate("asking.id.startsWith('v:')"): missed_id = p.evaluate("asking.id")
            answer(p, len(heads) > 5)                                        # 5 wrong: 13 of 18, under 80%
        ok.append(("18 questions (" + (heads[-1] if heads else "none") + ")", len(heads) == 18))
        ok.append(("13 of 18 is not a pass", "Not quite" in p.inner_text(".done")))
        ok.append(("a missed word comes back tomorrow", p.evaluate(f"Progress.get('{missed_id}').due") == TOMORROW))
        ok.append(("unit 2 still locked", not p.evaluate("RafiqPath.unitOpen('02')")))
        p.goto(BASE + "learn.html?u=01&s=test"); p.wait_for_timeout(1200)          # coming back: the review, not the test
        ok.append(("coming back before the review: the review (" + kicker(p) + ")", kicker(p).startswith("Your mistakes")))
        n = 0
        for _ in range(12):
            if not kicker(p).startswith("Your mistakes"): break
            p.locator("button.go").first.click(); p.wait_for_timeout(150)          # Try it
            answer(p, n != 0); n += 1                                                # one still wrong: it comes back
        ok.append(("reviewed 5 mistakes, one twice (%d tries)" % n, n == 6 and "Mistakes reviewed" in p.inner_text(".done")))
        p.locator("button.go").first.click(); p.wait_for_timeout(300)             # Try the test again
        k = 0
        while kicker(p).startswith("Unit test") and k < 30:
            answer(p, True); k += 1
        ok.append(("retake passed", "passed" in p.inner_text(".done")))
        ok.append(("unit 2 open", p.evaluate("RafiqPath.unitOpen('02') && RafiqPath.stepDone('01','test')")))
        p.close()
        b.close()
    ok.append(("no page errors " + "; ".join(e[:120] for e in errors[:3]), not errors))
    for name, good in ok: print(("ok   " if good else "FAIL ") + name)
    sys.exit(0 if all(g for _, g in ok) else 1)

if __name__ == "__main__":
    main()
