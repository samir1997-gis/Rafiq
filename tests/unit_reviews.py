"""Slower new words (#335): lessons of 5 words, each followed by a review.
  - after a lesson, its review is next: ten questions, three of the words just met and seven earlier
    ones (those due first); with few earlier words yet, more of the new ones
  - a right answer moves a due word on in the schedule, a miss brings a word back tomorrow
  - finishing the review counts as the recap (#158) and opens the next lesson
  - progress saved in lessons of 10 carries over: a lesson of 10 counts as both of its halves, a review
    counts as done once a later step is, old addresses (s=words2) open the lesson they became, and the
    words met each day still count
  - Home (#336): each finished or current unit opens to its steps: done ones to redo, the next one,
    and the rest locked, numbered 1.01, 1.02 … (#337); a lesson names its words; it stays open when Home repaints
  - a team account (app_metadata.admin, #338) has every unit and step open; its own progress is unchanged

  python3 .claude/skills/webapp-testing/scripts/with_server.py \
    --server "python3 -m http.server 8765 >/dev/null 2>&1" --port 8765 -- python3 tests/unit_reviews.py
"""
import json, os, sys, datetime
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8765/"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
TODAY = datetime.date.today().isoformat()
TOMORROW = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
IN3 = (datetime.date.today() + datetime.timedelta(days=3)).isoformat()   # not due yet: box 3 comes back after 4 days, so last reviewed yesterday
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
    if p.evaluate("!!asking.build"):               # units 1 and 2 (#358): a phrase built from tiles; "Show the answer" is a miss
        i = p.evaluate("(() => { window.__q = asking; return asking.id; })()")
        if right:
            for t in p.evaluate("asking.parts"): p.locator(".tl-pool .tl-tile", has_text=t).first.click()
            p.locator(".tl-check").click()
        else: p.get_by_text("Show the answer").click()
    else:                                          # the choice itself is kept on the button (_o): a picture has no text
        i = p.evaluate("""right => { const x = asking, o = [...document.querySelectorAll('.opt')];
          window.__q = x; (right ? o.find(b => b._o === x.right) : o.find(b => b._o !== x.right)).click(); return x.id; }""", right)
    p.evaluate("""() => { if(asking === window.__q){ const n = document.querySelector('button.go:not([disabled])'); if(n) n.click(); } }""")
    p.wait_for_function("asking !== window.__q || !!document.querySelector('.done')", polling=100, timeout=10000); p.wait_for_timeout(100)
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
                **{f"v:{i}": {"box": 3, "seen": 2, "due": IN3, "at": "2026-10-01T10:00:00.000Z"} for i in ids["u1"]},
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

        # Home: each unit opens to its steps (#336)
        p = page_with(b, seen(*START, *[f"p:01|{k}" for k in OLD_U1], "p:02|meet1", "p:02|review1", "p:02|meet2"), errors)
        p.set_viewport_size({"width": 390, "height": 844}); p.goto(BASE + "dashboard.html"); p.wait_for_timeout(1500)
        ok.append(("finished and current units open, later ones stay locked", p.evaluate("document.querySelectorAll('details.ud').length") == 4
                   and p.evaluate("document.querySelectorAll('.unit.later').length") == 10))
        p.locator("details.ud[data-u='01'] > summary").click(); p.locator("details.ud[data-u='02'] > summary").click(); p.wait_for_timeout(400)
        u1 = p.evaluate("""[...document.querySelectorAll('details.ud[data-u="01"] .ustep')].map(e => [e.className, e.getAttribute('href') || ''])""")
        ok.append(("unit 1: all 22 steps done, each one to redo", len(u1) == 22 and all("done" in c and h.startswith("learn.html?u=01&s=") for c, h in u1)))
        u2 = p.evaluate("""[...document.querySelectorAll('details.ud[data-u="02"] .ustep')].map(e => [e.className.split(' ')[1], e.tagName, e.getAttribute('href') || ''])""")
        ok.append(("unit 2: done, then the next one, then locked (%s)" % " ".join(c for c, _, _ in u2[:5]),
                   [c for c, _, _ in u2[:5]] == ["done", "done", "done", "next", "locked"] and u2[3][2] == "learn.html?u=02&s=review2" and u2[4][1] == "SPAN"))
        nos = p.evaluate("""[...document.querySelectorAll('details.ud[data-u="01"] .sno')].map(e => e.textContent)""")
        ok.append(("steps numbered 1.01 to 1.22 (%s … %s)" % (nos[0] if nos else "", nos[-1] if nos else ""), nos == ["1.%02d" % k for k in range(1, 23)]))
        ok.append(("unit 2 numbered from 2.01", p.evaluate("""document.querySelector('details.ud[data-u="02"] .sno').textContent""") == "2.01"))
        first = p.evaluate("""document.querySelector('details.ud[data-u="01"] .ustep small').textContent""")
        ok.append(("a lesson names its five words (" + first + ")", first.count(" · ") == 4))
        p.evaluate("paintHome()"); p.wait_for_timeout(200)
        ok.append(("still open after Home repaints", p.evaluate("[...document.querySelectorAll('details.ud[open]')].map(d => d.dataset.u).join()") == "01,02"))
        ok.append(("no sideways scroll", p.evaluate("document.documentElement.scrollWidth") <= 390))
        p.locator("details.ud[data-u='01'] a.ustep").nth(2).click(); p.wait_for_timeout(1500)
        ok.append(("Redo opens that lesson (" + kicker(p) + ")", "s=meet2" in p.url and kicker(p).startswith("New word"))); p.close()

        # a team account: every unit and step open (#338); a learner's stays locked
        def team_page(admin):
            c = b.new_context(viewport={"width": 390, "height": 844})
            c.route("**/@supabase/**", lambda r: r.abort()); c.route("https://fonts.googleapis.com/**", lambda r: r.abort())
            sess = json.dumps({"access_token": "x", "user": {"id": "t", "app_metadata": {"admin": admin}}})
            c.add_init_script("if(!localStorage.getItem('__seeded')){localStorage.setItem('rafiq_progress_mirror',%s);localStorage.setItem('sb-test-auth-token',%s);localStorage.setItem('__seeded','1')}"
                              % (json.dumps(json.dumps(seen(*START, "p:01|meet1"))), json.dumps(sess)))
            q = c.new_page(); q.on("pageerror", lambda e: errors.append(str(e))); q.goto(BASE + "dashboard.html"); q.wait_for_timeout(1500); return q
        p = team_page(True)
        ok.append(("team: every unit open", p.evaluate("RafiqPath.units().every(u => RafiqPath.unitOpen(u.n)) && RafiqPath.stepOpen('12', 'test')")))
        ok.append(("team: no locked rows on Home, units ahead marked open", p.evaluate("document.querySelectorAll('.unit.later').length") == 0
                   and p.evaluate("document.querySelectorAll('details.ud').length") == 14 and "Open to the team" in p.inner_text("details.ud[data-u='12']")
                   and "team account: every unit open" in p.inner_text("#home")))
        ok.append(("team: progress unchanged, the review is still next (" + nxt(p) + ")", nxt(p) == "01|review1"))
        p.goto(BASE + "learn.html?u=12&s=meet3"); p.wait_for_timeout(1500)
        ok.append(("team: a later unit's lesson opens (" + kicker(p) + ")", kicker(p).startswith("New word"))); p.close()
        p = team_page(False)
        ok.append(("a learner's later units stay locked", not p.evaluate("RafiqPath.unitOpen('12')") and p.evaluate("document.querySelectorAll('.unit.later').length") == 11
                   and "team account" not in p.inner_text("#home"))); p.close()
        b.close()
    ok.append(("no page errors " + "; ".join(e[:120] for e in errors[:3]), not errors))
    for name, good in ok: print(("ok   " if good else "FAIL ") + name)
    sys.exit(0 if all(g for _, g in ok) else 1)

if __name__ == "__main__":
    main()
