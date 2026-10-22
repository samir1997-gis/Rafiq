"""The fuller reading starter and basics (#276, #277):
  - the reading starter: a Play round after each letter group, then the vowel marks, sounding out, your
    first words, three sets of reading rules, the listening test and al-Fātiḥah's first line (22 steps);
    the basics: words to keep you going, describing words, your first verbs, put it together (11 steps)
  - the alphabet board: a letter is met, known once it's right on two different days, gold once it's
    also been read inside words twice; Home shows the board while you're in the reading starter
  - the starter is done when every letter is known: until then the letter check-in is next, and a new
    step opens with a check-in on letters from an earlier day
  - two new letter groups a day is plenty: a third asks first
  - Play: about a dozen questions, stars for right first time, a run of right answers counted
  - sounding out, first words, al-Fātiḥah's first line (a read-along without the recitation)
  - the basics: three drills from earlier lessons end each lesson; Put it together builds six sentences

  python3 .claude/skills/webapp-testing/scripts/with_server.py \
    --server "python3 -m http.server 8765 >/dev/null 2>&1" --port 8765 -- python3 tests/starter_game.py
"""
import datetime, json, os, sys
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8765/"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
LETTERS = "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"
NOW = datetime.datetime.now(datetime.timezone.utc)
TODAY, YESTERDAY = NOW.isoformat(), (NOW - datetime.timedelta(days=1)).isoformat()
ALPHA = [k for i in range(1, 8) for k in (f"letters{i}", f"play{i}")] + ["vowels", "sound", "firstwords", "rules", "rules2", "rules3", "hear", "line"]
row = lambda at=TODAY, box=0: {"box": box, "seen": 1, "at": at}
steps = lambda keys, at=TODAY: {f"p:00|{k}": row(at) for k in keys}
letters = lambda chs, at, box=2: {f"l:{c}": row(at, box) for c in chs}
known = {**{f"lk:{c}": row() for c in LETTERS}, **letters(LETTERS, TODAY)}

def page_with(b, mirror, errors, path):
    c = b.new_context(viewport={"width": 390, "height": 844})
    c.route("**/@supabase/**", lambda r: r.abort())
    c.route("https://fonts.googleapis.com/**", lambda r: r.abort())
    c.add_init_script("if(!localStorage.getItem('__seeded')){localStorage.setItem('rafiq_progress_mirror',%s);localStorage.setItem('__seeded','1')}"
                      % json.dumps(json.dumps(mirror)))
    p = c.new_page(); p.on("pageerror", lambda e: errors.append(str(e)))
    p.goto(BASE + path); p.wait_for_timeout(1500)
    return p

kicker = lambda p: p.evaluate("(() => { const k = document.querySelector('.kicker'); return k ? k.textContent.trim() : ''; })()")
go = lambda p: (p.locator("button.go:not([disabled])").first.click(timeout=15000), p.wait_for_timeout(200))
pick = lambda p, text: (p.locator(".opt", has_text=text).first.click(), p.wait_for_timeout(150))
# the letter a "Which letter is this?" card asks for, from the meaning of its example word
LQ = "(() => { const c = document.querySelector('.card').innerText; return ALPHABET_GROUPS.flatMap(g => g.letters).find(l => c.includes('\"' + l[4] + '\"'))[0]; })()"

def main():
    ok, errors = [], []
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME if os.path.exists(CHROME) else None)

        # the steps
        p = page_with(b, {}, errors, "dashboard.html")
        k0 = p.evaluate("RafiqPath.steps(RafiqPath.units()[0]).map(s => s.key)")
        kb = p.evaluate("RafiqPath.steps(RafiqPath.units()[1]).map(s => s.key)")
        ok.append(("reading starter: 22 steps, a Play round after each group", k0 == ALPHA))
        ok.append(("the basics: 11 steps " + str(kb), kb == ["b-the", "b-keep", "b-my", "b-people", "b-gender", "b-describe", "b-of", "b-many", "b-verbs", "b-together", "test"]))

        # the board's letter states
        p.close(); p = page_with(b, {**letters("ت", YESTERDAY), **letters("ث", YESTERDAY, 1)}, errors, "dashboard.html")
        st = p.evaluate("""(() => { const s = RafiqPath.letterState, out = [s('ب')];
          RafiqPath.letterAnswer('ب', true); out.push(s('ب'));            // first answer: met
          RafiqPath.letterAnswer('ب', true); out.push(s('ب'));            // right again, same day: still met
          RafiqPath.letterAnswer('ت', true); out.push(s('ت'));            // right yesterday, right today: known
          RafiqPath.letterAnswer('ث', true); out.push(s('ث'));            // missed yesterday: still met
          RafiqPath.letterAnswer('ت', true, true); RafiqPath.letterAnswer('ت', true, true); out.push(s('ت'));   // read in words twice: gold
          return out; })()""")
        ok.append(("letter states " + str(st), st == ["new", "met", "met", "known", "met", "gold"]))
        p.close()
        p = page_with(b, letters("ابت", YESTERDAY) | letters("ث", YESTERDAY, 1) | letters("ج", TODAY), errors, "dashboard.html")
        ci = p.evaluate("RafiqPath.checkInLetters()")
        ok.append(("check-in: letters from before today, missed first " + "".join(ci), ci == ["ث", "ا", "ب", "ت"]))
        p.close()

        # Home shows the board while you're in the reading starter
        p = page_with(b, steps(["letters1"]) | letters("ابتث", TODAY), errors, "dashboard.html")
        ok.append(("Home: the board, 4 letters met", p.locator(".board").count() == 1 and p.locator(".bl.met").count() == 4
                   and "0 of 28 known" in p.inner_text(".board").lower()))
        p.close()

        # every step done, letters not known yet: the check-in is next; with nothing to ask today, a night's sleep
        p = page_with(b, steps(ALPHA) | letters(LETTERS, TODAY), errors, "dashboard.html")
        nxt = p.evaluate("(() => { const n = RafiqPath.next(); return n.unit.n + '|' + n.step.key; })()")
        ok.append(("all steps done, letters not known: " + nxt, nxt == "00|checkin" and not p.evaluate("RafiqPath.unitOpen('0b')")))
        ok.append(("Home: come back tomorrow", "night’s sleep" in p.inner_text(".today-card")))
        p.close()
        p = page_with(b, steps(ALPHA) | letters(LETTERS, YESTERDAY), errors, "dashboard.html")
        ok.append(("Home: the letter check-in", "Letter check-in" in p.inner_text(".today-card") and p.locator(".today-card a.cont").count() == 1))
        p.goto(BASE + "learn.html?u=00&s=checkin"); p.wait_for_timeout(1500)
        n = 0
        while kicker(p).startswith("Check-in") and n < 12:
            pick(p, p.evaluate(LQ)); go(p); n += 1
        ok.append(("check-in: %d letters, then %s" % (n, p.inner_text(".done h2")), n == 10 and "10 letters turned green" in p.inner_text(".done h2")))
        ok.append(("…10 known now", p.evaluate("RafiqPath.LETTERS.filter(c => RafiqPath.letterState(c) === 'known').length") == 10))
        p.close()

        # a new step opens with a check-in on letters from an earlier day
        p = page_with(b, steps(["letters1"], YESTERDAY) | letters("ابتث", YESTERDAY), errors, "learn.html?u=00&s=play1")
        ok.append(("Play 1 opens with a check-in (" + kicker(p) + ")", kicker(p).startswith("Check-in: letters from before · 1 of 4")))
        p.close()

        # two new letter groups today is plenty
        p = page_with(b, steps(["letters1", "play1", "letters2", "play2"]) | letters("ابتثجحخ", TODAY), errors, "learn.html?u=00&s=letters3")
        ok.append(("a third group today: asked first", "plenty of new letters" in p.inner_text(".done h2")))
        p.locator("button.go", has_text="Keep going anyway").click(); p.wait_for_timeout(400)
        ok.append(("…and on if you insist (" + kicker(p) + ")", kicker(p).startswith("Warm-up") or kicker(p).startswith("Letters")))
        p.close()

        # Play: right first time every time
        p = page_with(b, steps(["letters1"]) | letters("ابتث", TODAY), errors, "learn.html?u=00&s=play1")
        n, runs = 0, []
        while kicker(p).startswith("Play") and n < 20:
            runs.append(kicker(p)); pick(p, p.evaluate("playAnswer")); go(p); n += 1
        ok.append(("Play 1: %d questions" % n, 9 <= n <= 13))
        ok.append(("a run of right answers counted", any("🔥 3 in a row" in k for k in runs)))
        ok.append(("3 stars, saved", p.locator(".stars").get_attribute("aria-label") == "3 of 3 stars" and p.evaluate("RafiqPath.stars('00','play1')") == 3
                   and p.evaluate("RafiqPath.stepDone('00','play1')")))
        ok.append(("the board after it", p.locator(".abc .abc-l.st-met").count() >= 4))
        p.close()

        # sounding out and first words
        before = ALPHA[:ALPHA.index("sound")]
        p = page_with(b, steps(before) | known, errors, "learn.html?u=00&s=sound")
        n = 0
        while kicker(p).startswith("Sounding out") and n < 20:
            if p.locator(".sx button").count():
                for x in p.locator(".sx button").all(): x.click()
                go(p)
            else:
                right = p.evaluate("(() => { const w = document.querySelector('#w').textContent; return SOUNDING.find(s => s[0] === w)[1].map(x => x[1]).join(''); })()")
                pick(p, right); go(p)
            n += 1
        ok.append(("sounding out: %d screens, done" % n, n == 14 and p.evaluate("RafiqPath.stepDone('00','sound')")))
        p.goto(BASE + "learn.html?u=00&s=firstwords"); p.wait_for_timeout(1500)
        n = 0
        while kicker(p).startswith("Your first words") and n < 15:
            right = p.evaluate("(() => { const w = document.querySelector('#w').textContent; return FIRST_WORDS.find(s => s[0] === w)[1]; })()")
            p.locator(".opt").filter(has_text=right).filter(has_not_text=right + "a").first.click(); p.wait_for_timeout(150); go(p); n += 1
        ok.append(("first words: %d read, done (%s)" % (n, p.inner_text(".wnote")), n == 12 and "12 of 12" in p.inner_text(".wnote")))
        ok.append(("letters read inside words turn gold (ب: %s)" % p.evaluate("RafiqPath.letterState('ب')"), p.evaluate("RafiqPath.letterState('ب')") == "gold"))
        p.close()

        # al-Fātiḥah's first line: read it, then (no recitation here) a read-along
        before = ALPHA[:ALPHA.index("line")]
        p = page_with(b, steps(before) | known, errors, "learn.html?u=00&s=line")
        ok.append(("first line: verse 1 (" + kicker(p) + ")", kicker(p) == "Read your first line · al-Fātiḥah 1:1"))
        p.locator(".fl button").first.click(); p.wait_for_timeout(100)
        ok.append(("tap a word: how it's read", "bismi" in p.locator(".fl button").first.inner_text()))
        go(p); p.wait_for_timeout(1500)
        ok.append(("then the recitation, or why there's none: " + p.inner_text("#nt"), kicker(p).startswith("Al-Fātiḥah 1:1") and p.inner_text("#nt") != "Loading the recitation…"))
        go(p); go(p); go(p); p.wait_for_timeout(300)
        ok.append(("two verses, then done", "first line of al-Fātiḥah" in p.inner_text(".done") and p.evaluate("RafiqPath.stepDone('00','line')")))
        ok.append(("…every letter known: the reading starter is done", p.evaluate("RafiqPath.unitDone(RafiqPath.units()[0])")))
        p.close()

        # the basics: words to keep you going, and put it together
        alpha = steps(ALPHA) | known
        p = page_with(b, alpha | {"p:0b|b-the": row()}, errors, "learn.html?u=0b&s=b-keep")
        ok.append(("words to keep you going (" + kicker(p) + ")", kicker(p) == "Words to keep you going · 1 of 2"))
        p.close()
        done = {f"p:0b|{k}": row() for k in ["b-the", "b-keep", "b-my", "b-people", "b-gender", "b-describe", "b-of", "b-many", "b-verbs"]}
        p = page_with(b, alpha | done, errors, "learn.html?u=0b&s=b-together")
        n = 0
        while kicker(p).startswith("Put it together ·") and "your sentence" not in kicker(p) and n < 8:
            p.locator("button.go", has_text="Show the answer").click(); p.wait_for_timeout(150); go(p); n += 1
        ok.append(("put it together: %d sentences, then yours (%s)" % (n, kicker(p)), n == 6 and kicker(p) == "Put it together · your sentence"))
        p.locator("button.go", has_text="Finish the lesson").click(); p.wait_for_timeout(300)
        ok.append(("…done, the check is next", p.evaluate("RafiqPath.stepDone('0b','b-together')") and p.evaluate("RafiqPath.next().step.key") == "test"))
        p.close()
        b.close()
    ok.append(("no page errors " + "; ".join(e[:160] for e in errors[:3]), not errors))
    for name, good in ok: print(("ok   " if good else "FAIL ") + name)
    sys.exit(0 if all(g for _, g in ok) else 1)

if __name__ == "__main__":
    main()
