"""The basics (#165), a section between the reading starter and unit 1:
  - it comes after the reading starter and before unit 1; unit 1 opens once it's done (lessons + check)
  - Home calls it "Before unit 1" and still numbers the units 1, 2, 3 …
  - a lesson: teaching screens, then 8 picks; a missed pick comes back until it's right; its words become met
  - the check at the end: 18 questions, 80% to pass
  - learners already in the units aren't sent back to it; placement at unit 1 starts here

  python3 .claude/skills/webapp-testing/scripts/with_server.py \
    --server "python3 -m http.server 8765 >/dev/null 2>&1" --port 8765 -- python3 tests/basics_section.py
"""
import json, os, sys
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8765/"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
seen = lambda *ks: {k: {"box": 0, "seen": 1} for k in ks}
ALPHA = ["letters1", "letters2", "letters3", "letters4", "letters5", "letters6", "letters7", "vowels", "rules", "hear"]
LESSONS = ["b-the", "b-gender", "b-people", "b-this", "b-many", "b-my"]

def page_with(b, mirror, errors):
    c = b.new_context(viewport={"width": 390, "height": 844})
    c.route("**/@supabase/**", lambda r: r.abort())
    c.route("https://fonts.googleapis.com/**", lambda r: r.abort())
    c.add_init_script("if(!localStorage.getItem('__seeded')){localStorage.setItem('rafiq_progress_mirror',%s);localStorage.setItem('__seeded','1')}"
                      % json.dumps(json.dumps(mirror)))
    p = c.new_page(); p.on("pageerror", lambda e: errors.append(str(e)))
    return p

kicker = lambda p: p.evaluate("(() => { const k = document.querySelector('.kicker'); return k ? k.textContent.trim() : ''; })()")
go = lambda p: (p.locator("button.go:not([disabled])").first.click(timeout=15000), p.wait_for_timeout(200))
def main():
    ok, errors = [], []
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME if os.path.exists(CHROME) else None)

        # where it sits
        p = page_with(b, seen(*[f"p:00|{k}" for k in ALPHA]), errors); p.goto(BASE + "dashboard.html"); p.wait_for_timeout(1500)
        order = p.evaluate("RafiqPath.units().slice(0, 3).map(u => u.n)")
        ok.append(("reading starter, the basics, unit 1: " + str(order), order == ["00", "0b", "01"]))
        nxt = p.evaluate("(() => { const n = RafiqPath.next(); return n.unit.n + '|' + n.step.key; })()")
        ok.append(("after the letters, next is the basics (" + nxt + ")", nxt == "0b|b-the"))
        ok.append(("unit 1 locked until the basics are done", not p.evaluate("RafiqPath.unitOpen('01')")))
        home = p.inner_text("#home")
        ok.append(("Home says 'Before unit 1'", "before unit 1" in home.lower()))
        ok.append(("Home still numbers unit 1 as 1", "1. Greetings" in home))
        p.close()

        # a lesson: teach, 8 picks, a miss comes back
        p = page_with(b, seen(*[f"p:00|{k}" for k in ALPHA], "p:0b|b-the"), errors); p.goto(BASE + "learn.html?u=0b&s=b-gender"); p.wait_for_timeout(1500)
        teach = 0
        while kicker(p).startswith("Masculine and feminine ·") and "practise" not in kicker(p):
            teach += 1; go(p)
        picks, missed = 0, False
        for _ in range(20):
            if "practise" not in kicker(p): break
            right = p.evaluate("""(() => { const L = BASICS[1], card = document.querySelector('.card').innerText;
              const d = L.drills.find(d => card.includes(d[0]) && (!d[1] || card.includes(d[1].replace('___','').trim()))); return d ? d[2][0] : null; })()""")
            opts = p.locator(".opt")
            if not missed:                                               # the first one wrong on purpose
                [o for o in opts.all() if o.inner_text() != right][0].click(); missed = True
            else:
                [o for o in opts.all() if o.inner_text() == right][0].click()
            p.wait_for_timeout(120); picks += 1; go(p)
        ok.append(("gender lesson: %d teaching screens, %d picks (8 + the one missed)" % (teach, picks), teach == 2 and picks == 9))
        ok.append(("lesson done, its words met", p.evaluate("RafiqPath.stepDone('0b','b-gender') && RafiqPath.metWords().has(27) && !Progress.isNew('v:27')")))
        p.close()

        # the check at the end, then unit 1 opens
        p = page_with(b, seen(*[f"p:00|{k}" for k in ALPHA], *[f"p:0b|{k}" for k in LESSONS]), errors)
        p.goto(BASE + "learn.html?u=0b&s=test"); p.wait_for_timeout(1500)
        n = 0
        while kicker(p).startswith("Unit test") and n < 30:
            p.evaluate("[...document.querySelectorAll('.opt')].find(b => b.textContent === asking.right).click()"); p.wait_for_timeout(100); go(p); n += 1
        ok.append(("the check: %d questions, passed" % n, n == 18 and "the basics passed" in p.inner_text(".done")))
        ok.append(("unit 1 open", p.evaluate("RafiqPath.unitOpen('01')")))
        p.close()

        # existing learners aren't sent back; placement at unit 1 starts at the basics
        p = page_with(b, seen("p:00|placed", "p:01|words1", "p:01|words2"), errors); p.goto(BASE + "dashboard.html"); p.wait_for_timeout(1500)
        nxt = p.evaluate("(() => { const n = RafiqPath.next(); return n.unit.n + '|' + n.step.key; })()")
        ok.append(("already in unit 1: carries on there (" + nxt + ")", nxt.startswith("01|")))
        ok.append(("…and the basics still open", p.evaluate("RafiqPath.unitOpen('0b') && RafiqPath.stepOpen('0b','b-the')")))
        p.close()
        p = page_with(b, {}, errors); p.goto(BASE + "dashboard.html"); p.wait_for_timeout(1500)
        p.evaluate("(() => { const u = RafiqPath.units(); RafiqPath.place(u.findIndex(x => x.n === '0b')); })()")
        ok.append(("placed at the basics: reading starter skipped, basics next", p.evaluate("RafiqPath.next().unit.n") == "0b"))
        p.close()
        b.close()
    ok.append(("no page errors " + "; ".join(e[:120] for e in errors[:3]), not errors))
    for name, good in ok: print(("ok   " if good else "FAIL ") + name)
    sys.exit(0 if all(g for _, g in ok) else 1)

if __name__ == "__main__":
    main()
