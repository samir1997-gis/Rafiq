"""Units 1 and 2: lessons on tested methods, with games (#358). Unit 3 on keeps the earlier lesson.
  - Meet: the meaning is hidden until it's tapped, and Next waits for that (guess first)
  - recall is spread through the lesson, not left to the end: the first question comes after the
    second word; each word is asked three ways (its meaning, by ear with pictures, in Arabic) and
    is in the Match-up game
  - a "tap the picture" question never offers two words drawn with the same picture
  - Match-up: a wrong pair stays open, right pairs lock, the time is kept as the best
  - single words are picked in Arabic, phrases are built from tiles
  - a missed word comes back at the end until it's right; misses in the lesson aren't scored, and
    the five words go into review, due tomorrow, as before
  - Review: three kinds of question in turn; its done screen offers Beat the clock, which adds a
    point for a right answer, takes time off for a miss, ends on a score to beat, and scores nothing
    into the review schedule

  python3 .claude/skills/webapp-testing/scripts/with_server.py \
    --server "python3 -m http.server 8765 >/dev/null 2>&1" --port 8765 -- python3 tests/unit_games.py
"""
import json, os, sys, datetime
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8765/"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
TOMORROW = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
seen = lambda *ks: {k: {"box": 0, "seen": 1} for k in ks}
START = ["p:00|placed", "p:0b|placed"]

def page_with(b, mirror, errors):
    c = b.new_context(viewport={"width": 390, "height": 844})
    c.route("**/@supabase/**", lambda r: r.abort())                       # signed out: progress from the local copy
    c.route("https://fonts.googleapis.com/**", lambda r: r.abort())
    c.add_init_script("if(!localStorage.getItem('__seeded')){localStorage.setItem('rafiq_progress_mirror',%s);localStorage.setItem('__seeded','1')}"
                      % json.dumps(json.dumps(mirror)))
    p = c.new_page(); p.on("pageerror", lambda e: errors.append(str(e)))
    return p

kicker = lambda p: p.evaluate("(document.querySelector('.kicker') || {}).textContent || ''").strip()
def go_on(p):
    p.locator(".foot button.go:not([disabled])").first.click(); p.wait_for_timeout(150)
def kind(p):
    return p.evaluate("asking.build ? 'build' : asking.pic ? 'pic' : asking.quiet ? 'say' : asking.kicker.startsWith('Hear') ? 'hear' : 'mean'")
def answer(p, right=True):
    """Answer the question on screen (a pick, or a phrase built from tiles); returns (word id, its kind)."""
    i, k = p.evaluate("asking.id"), kind(p)
    if k == "build":
        if right:
            p.evaluate("""() => { for(const t of asking.parts) [...document.querySelectorAll('.tl-pool .tl-tile')].find(b => b.textContent === t).click(); }""")      # the exact tile: another may hold it inside
            p.locator(".tl-check").click()
        else: p.get_by_text("Show the answer").click()
    else:
        p.evaluate("right => { const x = asking, o = [...document.querySelectorAll('.opt')]; (right ? o.find(b => b._o === x.right) : o.find(b => b._o !== x.right)).click(); }", right)
    p.wait_for_timeout(100)
    return i, k

def walk(p, miss=False):
    """Go through a Meet lesson to its done screen. miss: the first build is given up ("Show the answer") and
    Match-up starts with a wrong pair. Returns (the screens in order, {word id: the ways it was asked},
    the word missed on a build, what Match-up did)."""
    order, asked, wrong_id, match = [], {}, None, {}
    for _ in range(60):
        if p.locator(".done").count(): break
        k = kicker(p)
        if k.startswith("🕌"): go_on(p); continue                       # the salah bridge, before the done screen
        if p.locator(".guess").count(): p.locator(".guess").click(); order.append("meet")
        elif k.startswith("New word"): order.append("meet")             # its meaning already shown
        elif p.locator(".mt").count():
            order.append("match")
            ids = p.evaluate("[...new Set([...document.querySelectorAll('.mt')].map(b => b.dataset.id))]")
            pair = lambda a, e: (p.locator(f".mt[data-side=a][data-id='{a}']").click(), p.locator(f".mt[data-side=e][data-id='{e}']").click())
            if miss:
                pair(ids[0], ids[1]); p.wait_for_timeout(100)
                match["wrong stays open"] = p.locator(".mt[disabled]").count() == 0 and p.locator(".foot button.go").first.is_disabled()
                match["missed"] = "v:" + ids[0]
            for i in ids: pair(i, i)
            p.wait_for_timeout(200)
            match["right pairs lock"] = p.locator(".mt.right[disabled]").count() == 10
            match["the time is shown and kept"] = "All matched in" in p.inner_text("#v") and p.evaluate("localStorage.getItem('rafiq_match_best') !== null")
        elif k.startswith("One more try"):
            order.append("again"); i, _ = answer(p); asked.setdefault(i, []).append("again")
        else:
            # a different word from the one missed in Match-up: a word is only asked again once
            give_up = miss and kind(p) == "build" and wrong_id is None and p.evaluate("asking.id") != match.get("missed")
            i, t = answer(p, not give_up); asked.setdefault(i, []).append(t); order.append(t)
            if give_up: wrong_id = i
        go_on(p)
    return order, asked, wrong_id, match

def main():
    ok, errors = [], []
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME if os.path.exists(CHROME) else None)

        # ── the Meet lesson, unit 1, first lesson ─────────────────────────────────────────
        p = page_with(b, seen(*START), errors); p.goto(BASE + "learn.html?u=01&s=meet1"); p.wait_for_timeout(1500)
        ok.append(("the meaning is hidden until it's tapped, and Next waits",
                   p.locator(".guess").count() == 1 and not p.locator("#m").is_visible() and p.locator(".foot button.go").first.is_disabled()))
        p.locator(".guess").click(); p.wait_for_timeout(100)
        ok.append(("a tap shows it", p.locator("#m .en").is_visible() and p.locator(".guess").count() == 0 and p.locator(".foot button.go").first.is_enabled()))
        order, asked, _, _ = walk(p)
        ok.append(("recall starts after the second word, not at the end " + str(order[:4]), order[:3] == ["meet", "meet", "mean"]))
        ok.append(("five words met, a Match-up game (%d, %d)" % (order.count("meet"), order.count("match")), order.count("meet") == 5 and order.count("match") == 1))
        ways = lambda a, last: all("mean" in v and set(v) & {"pic", "hear"} and last in v for v in a.values())
        ok.append(("single words: each asked by meaning, by ear, and in Arabic (a pick) " + str(list(asked.values())[0]), len(asked) == 5 and ways(asked, "say")))
        ok.append(("nothing missed, nothing asked again", "again" not in order))
        rows = p.evaluate("ids => ids.map(i => Progress.get(i))", list(asked))
        ok.append(("the five words are in review, due tomorrow", all(r and r["due"] == TOMORROW and r["box"] >= 1 for r in rows)))
        ok.append(("the lesson is done and its review is next", p.evaluate("RafiqPath.stepDone('01','meet1') && RafiqPath.next().step.key === 'review1'"))); p.close()

        # the third lesson is phrases: built from tiles; a miss on a build and a wrong pair in Match-up
        p = page_with(b, seen(*START, *[f"p:01|{k}" for k in ("meet1", "review1", "meet2", "review2")]), errors)
        p.goto(BASE + "learn.html?u=01&s=meet3"); p.wait_for_timeout(1500)
        order, asked, wrong_id, match = walk(p, miss=True)
        ok.append(("phrases: each asked by meaning, by ear, and built from tiles " + str(list(asked.values())[0]), len(asked) == 5 and ways(asked, "build")))
        ok.append(("Match-up: a wrong pair stays open", match.get("wrong stays open")))
        ok.append(("Match-up: right pairs lock", match.get("right pairs lock")))
        ok.append(("Match-up: the time is shown and kept as the best", match.get("the time is shown and kept")))
        ok.append(("the two missed words come back at the end (%d)" % order.count("again"),
                   order.count("again") == 2 and "again" in asked[wrong_id] and "again" in asked[match["missed"]] and order[-2:] == ["again", "again"]))
        ok.append(("the done screen says what the lesson did", "recalled each word 4 times" in p.inner_text(".done") and "Match-up in" in p.inner_text(".done")))
        rows = p.evaluate("ids => ids.map(i => Progress.get(i))", list(asked))
        ok.append(("misses in the lesson aren't scored: all five due tomorrow", all(r and r["due"] == TOMORROW and r["box"] >= 1 for r in rows)))

        # a picture question never offers two words drawn the same (unit 2: to pray and prayer share one)
        twins = p.evaluate("""(() => { const u = RafiqPath.units().find(x => x.n === '02'), pool = RafiqPath.wordsOf(u); let bad = 0, pics = 0;
          for(const id of [64, 151]) for(let k = 0; k < 40; k++){ const x = question({t:'pic', id}, pool); if(!x.pic) continue; pics++;
            if(x.opts.some((a, i) => x.opts.some((b, j) => i < j && samePic(a, b)))) bad++; }
          return [pics, bad, samePic(64, 151)]; })()""")
        ok.append(("tap the picture: no two the same in 80 questions " + str(twins), twins[0] == 80 and twins[1] == 0 and twins[2])); p.close()

        # unit 3 keeps the earlier lesson and review
        p = page_with(b, seen(*START, "p:01|placed", "p:02|placed"), errors); p.goto(BASE + "learn.html?u=03&s=meet1"); p.wait_for_timeout(1500)
        ok.append(("unit 3: the meaning is shown straight away", p.locator(".guess").count() == 0 and p.locator(".card .en").is_visible())); p.close()

        # ── the review, unit 1 ────────────────────────────────────────────────────────────
        done = [f"p:01|{k}" for k in ("meet1", "review1", "meet2", "review2", "meet3")]
        p = page_with(b, seen(*START, *done), errors); p.goto(BASE + "learn.html?u=01&s=review3"); p.wait_for_timeout(1500)
        kinds = []
        for q in range(10):
            kinds.append(answer(p)[1]); go_on(p)
        turn = all(k == "mean" for k in kinds[0::3]) and all(k in ("pic", "hear") for k in kinds[1::3]) and all(k in ("say", "build") for k in kinds[2::3])
        ok.append(("review: three kinds of question in turn " + str(kinds[:6]), turn))
        ok.append(("its done screen offers the bonus game", p.locator(".done").count() == 1 and p.get_by_text("Bonus game").count() == 1))
        before = p.evaluate("JSON.stringify(Progress.ids().map(i => Progress.get(i)))")
        p.get_by_text("Bonus game").click(); p.wait_for_timeout(300)
        pick = lambda right: p.evaluate("""right => { const w = document.querySelector('#w').textContent, o = [...document.querySelectorAll('.sp-opts .opt')];
          (right ? o.find(b => b._w.ar === w) : o.find(b => b._w.ar !== w)).click(); }""", right)
        for _ in range(3): pick(True); p.wait_for_timeout(350)
        ok.append(("Beat the clock: a right answer is a point (" + p.inner_text("#s") + ")", p.inner_text("#s").strip() == "⚡ 3"))
        left = lambda: p.evaluate("+document.querySelector('#t').textContent.split(':')[1]")
        t0 = left(); pick(False); p.wait_for_timeout(500)
        ok.append(("a miss shows the right one and costs time (%d → %d s)" % (t0, left()), p.locator(".sp-opts .opt.right").count() == 1 and t0 - left() >= 3 and p.inner_text("#s").strip() == "⚡ 3"))
        p.evaluate("(() => { const now = Date.now; Date.now = () => now() + 60000; })()")           # the 40 seconds pass
        p.wait_for_selector(".done", timeout=5000); p.wait_for_timeout(200)
        ok.append(("it ends on the score, with Play again and the way on", "3 right in 40 seconds" in p.inner_text(".done") and p.get_by_text("Play again").count() == 1
                   and p.get_by_text("Continue learning").count() == 1 and p.evaluate("localStorage.getItem('rafiq_speed_best')") == "3"))
        ok.append(("nothing in it is scored into review", p.evaluate("JSON.stringify(Progress.ids().map(i => Progress.get(i)))") == before)); p.close()

        # unit 3's review: the two kinds it had, and no bonus
        u12 = [f"p:0{u}|placed" for u in (1, 2)]
        p = page_with(b, seen(*START, *u12, "p:03|meet1"), errors); p.goto(BASE + "learn.html?u=03&s=review1"); p.wait_for_timeout(1500)
        kinds = []
        for q in range(p.evaluate("+document.querySelector('.kicker').textContent.split(' of ')[1]")):
            kinds.append(answer(p)[1]); go_on(p)
        ok.append(("unit 3's review: by meaning and by ear only, no bonus " + str(sorted(set(kinds))), set(kinds) == {"mean", "hear"} and p.get_by_text("Bonus game").count() == 0)); p.close()

        ok.append(("no page errors " + str(errors[:2]), not errors))
        b.close()
    for name, good in ok: print(("ok   " if good else "FAIL ") + name)
    sys.exit(0 if all(g for _, g in ok) else 1)

if __name__ == "__main__":
    main()
