"""The reading starter and the basics, with more ways to practise what they teach (#361).
  The reading starter
  - a letter lesson: each letter is met, written (traced on a pad: Next waits for it, scribbling doesn't
    count, Skip goes on), then recalled twice with a gap, by ear (its name is played) and by eye (its
    sound is picked); a letter missed comes back at the end; the letters end up met, as before
  - the vowel marks: each is read on another letter one card after it's met; a miss comes back
  - reading rules: a guess before each rule (a wrong one costs nothing), the checks together at the
    end, a missed check back once more
  - your first words: a word read wrong comes back; the word's drawing shows with its meaning
  - Play: its done screen offers Beat the clock on the letters met so far, which scores nothing
  The basics
  - a lesson opens with a guess, then the teaching, a Match-up on its examples, the eight picks, one or
    two answers built from tiles (a tile that doesn't belong; only tiles with a recording), three from
    earlier lessons, and the sentence so far with Record yourself
  - a lesson whose answers are single words has no Build it
  - the check's done screen offers Beat the clock on the basics' words

  python3 .claude/skills/webapp-testing/scripts/with_server.py \
    --server "python3 -m http.server 8765 >/dev/null 2>&1" --port 8765 -- python3 tests/starter_depth.py
"""
import datetime, json, os, sys
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8765/"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
LETTERS = "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"
TODAY = datetime.datetime.now(datetime.timezone.utc).isoformat()
ALPHA = [k for i in range(1, 8) for k in (f"letters{i}", f"play{i}")] + ["vowels", "sound", "firstwords", "rules", "rules2", "rules3", "hear", "line"]
BASICS = ["b-the", "b-keep", "b-my", "b-people", "b-gender", "b-describe", "b-of", "b-many", "b-verbs", "b-together"]
row = lambda box=0: {"box": box, "seen": 1, "at": TODAY}
steps = lambda keys, n="00": {f"p:{n}|{k}": row() for k in keys}
known = {**{f"lk:{c}": row() for c in LETTERS}, **{f"l:{c}": row(2) for c in LETTERS}}

def page_with(b, mirror, errors, path):
    c = b.new_context(viewport={"width": 390, "height": 844})
    c.route("**/@supabase/**", lambda r: r.abort())                       # signed out: progress from the local copy
    c.route("https://fonts.googleapis.com/**", lambda r: r.abort())
    c.add_init_script("if(!localStorage.getItem('__seeded')){localStorage.setItem('rafiq_progress_mirror',%s);localStorage.setItem('__seeded','1')}"
                      % json.dumps(json.dumps(mirror)))
    p = c.new_page(); p.on("pageerror", lambda e: errors.append(str(e)))
    p.goto(BASE + path); p.wait_for_timeout(1500)
    return p

kicker = lambda p: p.evaluate("(document.querySelector('.kicker') || {}).textContent || ''").strip()
go = lambda p: (p.locator(".foot button.go:not([disabled])").first.click(timeout=15000), p.wait_for_timeout(200))
next_off = lambda p: p.locator(".foot button.go").first.is_disabled()
done = lambda p: p.locator(".done").count() > 0
def opt(p, js):
    """Click the option the JS test picks (b is the button)."""
    p.evaluate("[...document.querySelectorAll('.opt')].find(b => %s).click()" % js); p.wait_for_timeout(200)

def trace(p):
    """Touch the middle of every cell of the letter on the pad, one dab at a time."""
    box, t = p.locator(".trace canvas").bounding_box(), p.evaluate("traceTarget")
    for x, y in t["pts"]:
        p.mouse.move(box["x"] + x * box["width"] / t["S"], box["y"] + y * box["height"] / t["S"]); p.mouse.down(); p.mouse.up()
    p.wait_for_timeout(150)

def scribble(p):
    """Rub over the whole pad: far more ink off the letter than on it."""
    box = p.locator(".trace canvas").bounding_box()
    p.mouse.move(box["x"] + 8, box["y"] + 8); p.mouse.down()
    for i in range(1, 12):
        y = box["y"] + box["height"] * i / 12
        p.mouse.move(box["x"] + (box["width"] - 8 if i % 2 else 8), y, steps=6)
    p.mouse.up(); p.wait_for_timeout(150)

# the right choice on a basics pick: the drill whose question, Arabic and choices are the ones on screen
DRILL = """(() => { const card = document.querySelector('.card').innerText, os = [...document.querySelectorAll('.opt')];
  return BASICS.flatMap(l => l.drills).find(d => card.includes(d[0]) && (!d[1] || card.includes(d[1].replace('___','').trim()))
    && d[2].length === os.length && d[2].every(o => os.some(b => b.textContent === o)))[2][0]; })()"""

def main():
    ok, errors = [], []
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME if os.path.exists(CHROME) else None)

        # ── a letter lesson ──
        p = page_with(b, {}, errors, "learn.html?u=00&s=letters1")
        go(p); go(p)                                                       # the alphabet, the first letter's card
        ok.append(("after a letter's card, write it (" + kicker(p) + ")", kicker(p).endswith("write it") and p.locator(".trace canvas").count() == 1))
        ok.append(("Next waits for the letter to be written", next_off(p)))
        scribble(p)
        ok.append(("scribbling over the pad doesn't count (" + p.inner_text("#msg") + ")", next_off(p) and "Off the lines" in p.inner_text("#msg")))
        p.locator("#clr").click(); p.wait_for_timeout(100)
        ok.append(("Clear starts it again", p.inner_text("#msg") == "" and next_off(p)))
        trace(p)
        ok.append(("traced: written, and on (" + p.inner_text("#msg") + ")", not next_off(p) and "Written" in p.inner_text("#msg")))
        go(p)
        order, asked, missed = ["meet", "write"], {}, None
        for _ in range(60):
            if done(p): break
            k = kicker(p)
            if k.endswith("write it"):
                order.append("write")
                if order.count("write") == 2: p.locator(".foot button.go", has_text="Skip").click(); p.wait_for_timeout(200)       # Skip goes on without it
                else: trace(p); go(p)
            elif p.locator(".opt").count():
                ch, way = p.evaluate("playAnswer"), "ear" if p.locator(".hear-big").count() else "eye"
                order.append("redo" if k == "One more try" else way)
                if k != "One more try": asked.setdefault(ch, []).append(way)
                if missed is None and way == "eye": missed = ch; opt(p, "b._l[0] !== playAnswer")      # one miss, on a sound
                else: opt(p, "(b._l ? b._l[0] : b.textContent) === playAnswer")
                go(p)
            else: order.append("meet"); go(p)
        ok.append(("recall starts after the second letter, not at the end: " + " ".join(order[:8]), order[:8] == ["meet", "write", "meet", "write", "ear", "meet", "write", "ear"]))
        ok.append(("each letter recalled by ear and by eye " + str(asked), len(asked) == 4 and all(sorted(v) == ["ear", "eye"] for v in asked.values())))
        ok.append(("the letter missed comes back at the end", order[-1] == "redo" and order.count("redo") == 1))
        ok.append(("the lesson is done, its four letters met", p.evaluate("RafiqPath.stepDone('00','letters1') && [...'ابتث'].every(c => RafiqPath.letterState(c) === 'met')")))
        ok.append(("…and no letter of a later group touched", p.evaluate("RafiqPath.letterState('ج')") == "new"))
        p.close()

        # ── the vowel marks ──
        p = page_with(b, steps(ALPHA[:14]) | known, errors, "learn.html?u=00&s=vowels")
        order, on, miss = [], set(), False
        for _ in range(50):
            if done(p): break
            k = kicker(p)
            if k.startswith("The vowel marks"): order.append("meet"); go(p); continue
            shown = p.evaluate("(document.querySelector('#w') || {}).textContent || ''")
            if shown:                                                      # a mark on another letter: how is it said?
                order.append("redo" if k == "One more try" else "read"); on.add(shown[0])
                right = p.evaluate("w => Object.keys(MARK_ON).flatMap(c => VOWEL_MARKS.map(v => onLetter(v, c))).find(x => x[0] === w)[1]", shown)
            else:
                order.append("which"); right = p.evaluate("k => VOWEL_MARKS.find(v => k.includes('\"' + v[1] + '\"'))[0]", k)
            if not miss and shown: miss = True; opt(p, "b.textContent !== %s" % json.dumps(right))
            else: opt(p, "b.textContent === %s" % json.dumps(right))
            go(p)
        ok.append(("each mark is read one card after it's met: " + " ".join(order[:6]), order[:6] == ["meet", "meet", "read", "meet", "read", "meet"]))
        ok.append(("9 marks met, 9 read on other letters (%s), 4 picked from the written forms" % "".join(sorted(on)),
                   order.count("meet") == 9 and order.count("read") == 9 and order.count("which") == 4 and "ب" not in on and len(on) >= 3))
        ok.append(("the mark missed comes back at the end; the lesson is done", order[-1] == "redo" and p.evaluate("RafiqPath.stepDone('00','vowels')")))
        p.close()

        # ── reading rules ──
        p = page_with(b, steps(ALPHA[:17]) | known, errors, "learn.html?u=00&s=rules")
        right = lambda: p.evaluate("(q => { const c = READING_RULES.find(r => r[3][0] === q)[3]; return c[1][c[2]]; })(document.querySelector('.card .en').innerText)")
        ok.append(("a rule opens with a guess (" + kicker(p) + ")", "have a guess first" in kicker(p) and p.locator("#gh").count() == 1 and p.locator(".card.note").count() == 0))
        opt(p, "b.textContent !== %s" % json.dumps(right()))               # a wrong guess
        ok.append(("a wrong guess: the right one and why, and on", not next_off(p) and p.locator(".opt.right").count() == 1 and p.locator(".why:not(.hide)").count() == 1))
        go(p)
        ok.append(("then the rule (" + kicker(p) + ")", kicker(p) == "Reading rules · 1 of 3" and p.locator(".card.note").count() == 1))
        order, miss = ["guess"], False
        for _ in range(30):
            if done(p): break
            k = kicker(p)
            if p.locator(".opt").count():
                order.append("guess" if "guess" in k else "redo" if k == "One more try" else "check")
                if order[-1] == "check" and not miss: miss = True; opt(p, "b.textContent !== %s" % json.dumps(right()))
                else: opt(p, "b.textContent === %s" % json.dumps(right()))
            else: order.append("rule")
            go(p)
        ok.append(("guess, rule, three times, then the checks together, the missed one back: " + " ".join(order),
                   order == ["guess", "rule"] * 3 + ["check"] * 3 + ["redo"] and p.evaluate("RafiqPath.stepDone('00','rules')")))
        p.close()

        # ── your first words ──
        p = page_with(b, steps(ALPHA[:16]) | known, errors, "learn.html?u=00&s=firstwords")
        ks, pics = [], 0
        for n in range(20):
            if done(p): break
            ks.append(kicker(p))
            r = p.evaluate("FIRST_WORDS.find(s => s[0] === document.querySelector('#w').textContent)[1]")
            opt(p, "b.textContent %s %s" % ("!==" if n == 2 else "===", json.dumps(r)))
            pics += p.locator("#m:not(.hide) .wpic").count(); go(p)
        ok.append(("a word read wrong comes back at the end (%d screens, last: %s)" % (len(ks), ks[-1]), len(ks) == 13 and ks[-1].endswith("one more try") and "11 of 12" in p.inner_text(".wnote")))
        ok.append(("the word's drawing shows with its meaning (%d of 13)" % pics, pics >= 10))
        p.close()

        # ── Play: the bonus round on the letters ──
        p = page_with(b, steps(["letters1"]) | {f"l:{c}": row(2) for c in "ابتث"}, errors, "learn.html?u=00&s=play1")
        for _ in range(20):
            if not kicker(p).startswith("Play"): break
            opt(p, "b.textContent === playAnswer"); go(p)
        before = p.evaluate("JSON.stringify(Progress.ids('l').map(i => [i, Progress.get(i).box, Progress.get(i).seen]))")
        p.locator(".foot button.go", has_text="Bonus").click(); p.wait_for_timeout(300)
        ok.append(("Play's done screen offers Beat the clock (" + kicker(p) + ")", kicker(p) == "Beat the clock · tap its sound" and p.locator(".sp-opts .opt").count() == 2))
        for _ in range(4):
            opt(p, "b._w.ar === document.querySelector('#w').textContent"); p.wait_for_timeout(200)
        ok.append(("a letter, two sounds, a point for each right (" + p.inner_text("#s") + ")", p.inner_text("#s").endswith("4") and p.inner_text("#w") in "ابتث"))
        p.evaluate("(() => { const n = Date.now; Date.now = () => n() + 60000; })()"); p.wait_for_timeout(500)
        ok.append(("time up: a score to beat, kept apart from the words' (" + p.inner_text(".done h2") + ")", "4 right" in p.inner_text(".done h2")
                   and p.evaluate("localStorage.getItem('rafiq_letters_best')") == "4" and p.evaluate("localStorage.getItem('rafiq_speed_best')") is None))
        ok.append(("…and nothing scored for the letters", p.evaluate("JSON.stringify(Progress.ids('l').map(i => [i, Progress.get(i).box, Progress.get(i).seen]))") == before))
        p.close()

        # ── a basics lesson ──
        alpha = steps(ALPHA) | known
        p = page_with(b, alpha | steps(BASICS[:5], "0b"), errors, "learn.html?u=0b&s=b-describe")
        ok.append(("a lesson opens with a guess (" + kicker(p) + ")", kicker(p) == "Describing words · before you start, have a guess" and p.locator("#gh").count() == 1))
        opt(p, "b.textContent !== %s" % json.dumps(p.evaluate(DRILL)))
        ok.append(("a wrong guess: the right one and why, and on to the teaching", p.locator(".opt.right").count() == 1 and p.locator(".why:not(.hide)").count() == 1))
        go(p)
        order, tiles = ["guess"], []
        for _ in range(60):
            if done(p): break
            k = kicker(p)
            if "match-up" in k:
                order.append("match")
                ids = p.evaluate("[...document.querySelectorAll('.mt[data-side=a]')].map(b => b.dataset.id)")
                for i in ids:
                    p.locator(f".mt[data-side=a][data-id='{i}']").click(); p.locator(f".mt[data-side=e][data-id='{i}']").click()
                ok.append(("Match-up on the lesson's examples (%d pairs: %s)" % (len(ids), p.inner_text("#v")), 3 <= len(ids) <= 5 and "All matched" in p.inner_text("#v")))
                go(p)
            elif "build it" in k:
                order.append("build")
                want = p.evaluate("BASICS.flatMap(l => l.drills).find(d => d[0] === document.querySelector('.card .en').innerText)[2][0].split(' ')")
                pool = p.locator(".tl-tile").all_inner_texts(); tiles.append((want, pool))
                if len(tiles) == 1:                                        # the tile that doesn't belong, first: not accepted
                    extra = [t for t in pool if t not in want][0]
                    for t in [want[0], extra]: p.evaluate("t => [...document.querySelectorAll('.tl-pool .tl-tile')].find(b => b.textContent === t).click()", t)
                    p.locator(".tl-check").click(); p.wait_for_timeout(300)
                    ok.append(("Build it: the wrong tile isn't accepted", next_off(p)))
                    p.locator(".tl-clear").click(); p.wait_for_timeout(200)
                for t in want: p.evaluate("t => [...document.querySelectorAll('.tl-pool .tl-tile')].find(b => b.textContent === t).click()", t)
                p.locator(".tl-check").click(); p.wait_for_timeout(300); go(p)
            elif p.locator(".opt").count():
                order.append("fresh" if k.startswith("Keep it fresh") else "pick"); opt(p, "b.textContent === %s" % json.dumps(p.evaluate(DRILL))); go(p)
            elif "so far" in k or k == "A bonus":
                order.append("sofar"); ok.append(("the sentence so far, with Record yourself", p.locator("#rec").count() == 1)); go(p)
            else: order.append("teach"); go(p)
        want = ["guess", "teach", "teach", "match"] + ["pick"] * 8 + ["build"] * 2 + ["fresh"] * 3 + ["sofar"]
        ok.append(("guess, teaching, Match-up, 8 picks, 2 built, 3 from earlier, the sentence: " + " ".join(order), order == want))
        ok.append(("each build has a tile that doesn't belong " + str([len(t[1]) - len(t[0]) for t in tiles]), len(tiles) == 2 and all(len(pool) > len(w) for w, pool in tiles)))
        ok.append(("every tile has a recording", p.evaluate("ts => ts.every(t => !!RQ.clipId(t))", [t for _, pool in tiles for t in pool])))
        ok.append(("the lesson is done, its words met", p.evaluate("RafiqPath.stepDone('0b','b-describe') && RafiqPath.metWords().has(161)")))
        p.close()

        # a lesson of single-word answers: no Build it
        p = page_with(b, alpha | steps(BASICS[:2], "0b"), errors, "learn.html?u=0b&s=b-my")
        seen = []
        for _ in range(60):
            if done(p): break
            k = kicker(p); seen.append(k.split(" · ")[-1])
            if "match-up" in k:
                for i in p.evaluate("[...document.querySelectorAll('.mt[data-side=a]')].map(b => b.dataset.id)"):
                    p.locator(f".mt[data-side=a][data-id='{i}']").click(); p.locator(f".mt[data-side=e][data-id='{i}']").click()
            elif p.locator(".opt").count(): opt(p, "b.textContent === %s" % json.dumps(p.evaluate(DRILL)))
            go(p)
        ok.append(("‘My, your’: a guess and a Match-up, no Build it", "match-up" in seen and "build it" not in seen and seen[0].endswith("have a guess") and done(p)))
        p.close()

        # ── the check: the bonus round on the basics' words ──
        p = page_with(b, alpha | steps(BASICS, "0b"), errors, "learn.html?u=0b&s=test")
        for _ in range(30):
            if not kicker(p).startswith("Unit test"): break
            opt(p, "b.textContent === asking.right"); go(p)
        p.locator(".foot button.go", has_text="Bonus").click(); p.wait_for_timeout(300)
        ok.append(("the check's done screen offers Beat the clock on the basics' words (" + kicker(p) + ")", kicker(p) == "Beat the clock · tap the meaning"
                   and p.evaluate("RafiqPath.units().find(u => u.basics).words.includes(document.querySelector('.sp-opts .opt')._w.id)")))
        p.close()
        b.close()
    ok.append(("no page errors " + "; ".join(e[:160] for e in errors[:3]), not errors))
    for name, good in ok: print(("ok   " if good else "FAIL ") + name)
    sys.exit(0 if all(g for _, g in ok) else 1)

if __name__ == "__main__":
    main()
