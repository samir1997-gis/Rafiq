"""First-lesson basics (#163):
  - the reading starter has a Reading rules step (ة, ال, sun letters, the joining alif, stopping),
    one rule a screen, each followed by a quick check; learners already past it aren't sent back
  - units 2 and 3 get "How it works, part 2" after their later words; learners past the unit aren't sent back
  - a card with a quick check asks it straight after the card: "How do you say ‘we study’?" → نَدْرُسُ

  python3 .claude/skills/webapp-testing/scripts/with_server.py \
    --server "python3 -m http.server 8765 >/dev/null 2>&1" --port 8765 -- python3 tests/basics.py
"""
import json, os, sys
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8765/"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
seen = lambda *ks: {k: {"box": 0, "seen": 1} for k in ks}
U1 = ["words1", "words2", "grammar", "words3", "words4", "practise", "listen", "chat", "speak", "test"]

def page_with(b, mirror, errors):
    c = b.new_context(viewport={"width": 390, "height": 844})
    c.route("**/@supabase/**", lambda r: r.abort())
    c.route("https://fonts.googleapis.com/**", lambda r: r.abort())
    c.add_init_script("if(!localStorage.getItem('__seeded')){localStorage.setItem('rafiq_progress_mirror',%s);localStorage.setItem('__seeded','1')}"
                      % json.dumps(json.dumps(mirror)))
    p = c.new_page(); p.on("pageerror", lambda e: errors.append(str(e)))
    return p

kicker = lambda p: p.evaluate("(() => { const k = document.querySelector('.kicker'); return k ? k.textContent.trim() : ''; })()")
go = lambda p: (p.locator("button.go:not([disabled])").first.click(timeout=15000), p.wait_for_timeout(250))

def main():
    ok, errors = [], []
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME if os.path.exists(CHROME) else None)
        keys = lambda p, n: p.evaluate(f"RafiqPath.steps(RafiqPath.units().find(u => u.n === '{n}')).map(s => s.key)")

        # the steps
        p = page_with(b, {}, errors); p.goto(BASE + "dashboard.html"); p.wait_for_timeout(1500)
        k0 = keys(p, "00")
        ok.append(("reading starter: rules after the vowel marks " + str(k0[-3:]), k0[-3:] == ["vowels", "rules", "hear"]))
        ok.append(("unit 1 has no part 2", "grammar2" not in keys(p, "01")))
        for n in ("02", "03"):
            k = keys(p, n)
            ok.append((f"unit {n}: part 2 after the last words, before Practise", "grammar2" in k and k.index("grammar2") == k.index("practise") - 1
                       and all(k.index(w) < k.index("grammar2") for w in k if w.startswith("words"))))
        p.close()

        # learners already past aren't sent back
        p = page_with(b, seen(*[f"p:00|{k}" for k in ["letters1", "letters2", "letters3", "letters4", "letters5", "letters6", "letters7", "vowels", "hear"]], "p:01|words1"), errors)
        p.goto(BASE + "dashboard.html"); p.wait_for_timeout(1500)
        ok.append(("into unit 1 without the rules step: reading starter still done", p.evaluate("RafiqPath.unitDone(RafiqPath.units()[0])")))
        p.close()
        u2 = [f"p:02|{k}" for k in ["words1", "words2", "grammar", "words3", "words4", "practise", "listen", "chat", "speak", "test"]]
        p = page_with(b, seen("p:00|placed", *[f"p:01|{k}" for k in U1], *u2, "p:03|words1"), errors); p.goto(BASE + "dashboard.html"); p.wait_for_timeout(1500)
        ok.append(("into unit 3 without unit 2's part 2: unit 2 still done", p.evaluate("RafiqPath.unitDone(RafiqPath.units().find(u => u.n === '02'))")))
        p.close()
        p = page_with(b, seen("p:00|placed", *[f"p:01|{k}" for k in U1], *u2), errors); p.goto(BASE + "dashboard.html"); p.wait_for_timeout(1500)
        nxt = p.evaluate("(() => { const n = RafiqPath.next(); return n.unit.n + '|' + n.step.key; })()")
        ok.append(("everything in unit 2 but part 2: part 2 is next (" + nxt + ")", nxt == "02|grammar2"))
        p.close()

        # the reading rules step: 5 rules, each with a quick check
        alpha = seen(*[f"p:00|{k}" for k in ["letters1", "letters2", "letters3", "letters4", "letters5", "letters6", "letters7", "vowels"]])
        p = page_with(b, alpha, errors); p.goto(BASE + "learn.html?u=00&s=rules"); p.wait_for_timeout(1500)
        rules = checks = 0
        for _ in range(12):
            k = kicker(p)
            if k.startswith("Reading rules"): rules += 1; go(p)
            elif k.startswith("Quick check"):
                checks += 1; p.locator(".opt").first.click(); p.wait_for_timeout(150); go(p)
            else: break
        ok.append(("reading rules: %d rules, %d checks" % (rules, checks), rules == 5 and checks == 5))
        ok.append(("reading rules step done", p.evaluate("RafiqPath.stepDone('00','rules')")))
        p.close()

        # unit 2 part 2: "How do you say ‘we study’?"
        p = page_with(b, seen("p:00|placed", *[f"p:01|{k}" for k in U1], *u2[:5]), errors)
        p.goto(BASE + "learn.html?u=02&s=grammar2"); p.wait_for_timeout(1500)
        cards, found = [], None
        for _ in range(10):
            k = kicker(p)
            if k.startswith("How it works"): cards.append(p.inner_text(".gh")); go(p)
            elif k.startswith("Quick check"):
                q = p.inner_text(".card .en")
                if "we study" in q:
                    found = sorted(p.eval_on_selector_all(".opt", "o => o.map(x => x.textContent)"))
                    p.locator(".opt", has_text="نَدْرُسُ").first.click(); p.wait_for_timeout(150)
                    found = (found, p.locator(".opt.right").inner_text(), p.locator(".opt.wrong").count())
                else: p.locator(".opt").first.click(); p.wait_for_timeout(150)
                go(p)
            else: break
        ok.append(("unit 2 part 2: 3 cards " + " / ".join(cards), len(cards) == 3))
        ok.append(("‘we study’: pick from أَدْرُسُ نَدْرُسُ يَدْرُسُ, نَدْرُسُ is right " + str(found),
                   bool(found) and found[0] == sorted(["أَدْرُسُ", "نَدْرُسُ", "يَدْرُسُ"]) and found[1] == "نَدْرُسُ" and found[2] == 0))
        ok.append(("part 2 done", p.evaluate("RafiqPath.stepDone('02','grammar2')")))
        p.close()
        b.close()
    ok.append(("no page errors " + "; ".join(e[:120] for e in errors[:3]), not errors))
    for name, good in ok: print(("ok   " if good else "FAIL ") + name)
    sys.exit(0 if all(g for _, g in ok) else 1)

if __name__ == "__main__":
    main()
