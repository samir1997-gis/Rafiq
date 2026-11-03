"""Slower new words (#335): lessons of 5 words, each followed by a review.
  - after a lesson, its review is next: ten questions, three of the words just met and seven earlier
    ones (those due first); with few earlier words yet, more of the new ones
  - a right answer moves a due word on in the schedule, a miss brings a word back tomorrow
  - finishing the review counts as the recap (#158) and opens the next lesson
  - progress saved in lessons of 10 carries over: a lesson of 10 counts as both of its halves, a review
    counts as done once a later step is, old addresses (s=words2) open the lesson they became, and the
    words met each day still count

  python3 .claude/skills/webapp-testing/scripts/with_server.py \
    --server "python3 -m http.server 8765 >/dev/null 2>&1" --port 8765 -- python3 tests/unit_reviews.py
"""
import json, os, sys, datetime
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8765/"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
TODAY = datetime.date.today().isoformat()
TOMORROW = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
seen = lambda *ks: {k: {"box": 0, "seen": 1} for k in ks}
START = ["p:00|placed", "p:0b|placed"]
OLD_U1 = ["words1", "words2", "grammar", "words3", "words4", "practise", "listen", "chat", "speak", "test"]

def page_with(b, mirror, errors):
    c = b.new_context(viewport={"width": 390, "height": 844})
    c.route("**/@supabase/**", lambda r: r.abort())
    c.route("https://fonts.googleapis.com/**", lambda r: r.abort())
    c.add_init_script("if(!localStorage.getItem('__seeded')){localStorage.setItem('rafiq_progress_mirror',%s);localStorage.setItem('__seeded','1')}"
                      % json.dumps(json.dumps(mirror)))
    p = c.new_page(); p.on("pageerror", lambda e: errors.append(str(e)))
    return p

kicker = lambda p: p.evaluate("(() => { const k = document.querySelector('.kicker'); return k ? k.textContent.trim() : ''; })()")
nxt = lambda p: p.evaluate("(() => { const n = RafiqPath.next(); return n.unit.n + '|' + (n.step && n.step.key); })()")

def answer(p, right):
    """Answer the question on screen, right or wrong; returns its item id. Then Next (a right answer
    can move on by itself, so whichever comes first)."""
    i = p.evaluate("""right => { const x = asking, o = [...document.querySelectorAll('.opt')];
      window.__q = x; (right ? o.find(b => b.textContent === x.right) : o.find(b => b.textContent !== x.right)).click(); return x.id; }""", right)
    p.evaluate("""() => { if(asking === window.__q){ const n = document.querySelector('button.go:not([disabled])'); if(n) n.click(); } }""")
    p.wait_for_function("asking !== window.__q || !!document.querySelector('.done')", timeout=10000); p.wait_for_timeout(100)
    return i

def main():
    ok, errors = [], []
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME if os.path.exists(CHROME) else None)

        # the first lesson: its review is next, and with no earlier words it's the five just met
        p = page_with(b, seen(*START, "p:01|meet1"), errors); p.goto(BASE + "dashboard.html"); p.wait_for_timeout(1200)
        ok.append(("after the first lesson, its review is next (" + nxt(p) + ")", nxt(p) == "01|review1"))
        p.goto(BASE + "learn.html?u=01&s=review1"); p.wait_for_timeout(1200)
        ok.append(("first review: the five words just met (" + kicker(p) + ")", kicker(p) == "Review · 1 of 5")); p.close()

        # later on: three new words, seven earlier ones, the due ones first
        p = page_with(b, seen(*START), errors); p.goto(BASE + "dashboard.html"); p.wait_for_timeout(1200)
        ids = p.evaluate("""(() => { const u = n => RafiqPath.units().find(x => x.n === n);
          return { u1: RafiqPath.wordsOf(u('01')).map(w => w.id), u2: RafiqPath.wordsOf(u('02'), 0).map(w => w.id) }; })()""")
        p.close()
        due4 = ids["u1"][:4]
        rows = {**seen(*START, *[f"p:01|{k}" for k in OLD_U1], "p:02|meet1"),
                **{f"v:{i}": {"box": 3, "seen": 2, "due": "2099-01-01", "at": "2026-10-01T10:00:00.000Z"} for i in ids["u1"]},
                **{f"v:{i}": {"box": 2, "seen": 2, "due": "2026-10-20", "at": "2026-10-10T10:00:00.000Z"} for i in due4},
                **{f"v:{i}": {"box": 1, "seen": 1, "due": TOMORROW, "at": TODAY + "T09:00:00.000Z"} for i in ids["u2"]}}
        p = page_with(b, rows, errors); p.goto(BASE + "learn.html?u=02&s=review1"); p.wait_for_timeout(1200)
        asked, k0 = [], kicker(p)
        for q in range(10):
            asked.append(p.evaluate("asking.id")); answer(p, q != 9)          # the last one wrong
        new = [a for a in asked if int(a[2:]) in ids["u2"]]
        ok.append(("ten questions (" + k0 + ")", k0 == "Review · 1 of 10" and len(asked) == 10))
        ok.append(("three of the new words, seven earlier ones (%d new)" % len(new), len(new) == 3 and len(set(asked)) == 10))
        ok.append(("every word due is in it", all(f"v:{i}" in asked for i in due4)))
        moved = p.evaluate("([ids, t]) => ids.filter(i => Progress.get(i).due > t).length", [[f"v:{i}" for i in due4 if f"v:{i}" != asked[9]], TODAY])
        ok.append(("a due word answered right moves on (%d)" % moved, moved == len([i for i in due4 if f"v:{i}" != asked[9]])))
        last = p.evaluate("id => Progress.get(id)", asked[9])
        ok.append(("a miss comes back tomorrow (%s, box %s)" % (last["due"], last["box"]), last["due"] == TOMORROW and last["box"] == 1))
        ok.append(("the done screen gives the score", "9 of 10 right" in p.inner_text(".done")))
        ok.append(("the review is done and counts as the recap", p.evaluate("RafiqPath.stepDone('02','review1') && !RafiqPath.recapDue()")))
        ok.append(("then the next lesson (" + nxt(p) + ")", nxt(p) == "02|meet2")); p.close()

        # progress saved in lessons of 10
        p = page_with(b, seen(*START, *[f"p:01|{k}" for k in OLD_U1], "p:04|placed", "p:02|placed", "p:03|placed", "p:05|words1"), errors)
        p.goto(BASE + "dashboard.html"); p.wait_for_timeout(1200)
        ok.append(("an old lesson of 10 counts as both halves", p.evaluate("RafiqPath.stepDone('05','meet1') && RafiqPath.stepDone('05','meet2') && !RafiqPath.stepDone('05','meet3')")))
        ok.append(("the review between them counts as done", p.evaluate("RafiqPath.stepDone('05','review1')")))
        ok.append(("the review after them is next (" + nxt(p) + ")", nxt(p) == "05|review2"))
        ok.append(("unit 1 finished in lessons of 10 is still finished", p.evaluate("RafiqPath.unitDone(RafiqPath.units().find(u => u.n === '01'))")))
        ok.append(("its 40 words still count as met", p.evaluate("RafiqPath.wordsOf(RafiqPath.units().find(u => u.n === '01')).every(w => RafiqPath.metWords().has(w.id))")))
        ok.append(("an old address opens the lesson it became", p.evaluate("RafiqPath.stepKey('words2') === 'meet3' && RafiqPath.stepKey('grammar') === 'grammar'")))
        p.close()
        today = {**seen(*START), "p:01|words1": {"box": 0, "seen": 1, "at": TODAY + "T10:00:00.000Z"}}
        p = page_with(b, today, errors); p.goto(BASE + "dashboard.html"); p.wait_for_timeout(1200)
        ok.append(("a lesson of 10 finished today still counts 10 words today", p.evaluate("RafiqPath.period(1).words") >= 10)); p.close()
        b.close()
    ok.append(("no page errors " + "; ".join(e[:120] for e in errors[:3]), not errors))
    for name, good in ok: print(("ok   " if good else "FAIL ") + name)
    sys.exit(0 if all(g for _, g in ok) else 1)

if __name__ == "__main__":
    main()
