"""Units 13 to 16 (#344): Ramadan & Eid, Health & the body, Travel & directions, Telling stories.
  - the path has 16 units, and units 1 to 12 teach exactly the words they taught before
  - each new unit: 40 words of its own (none taught earlier), each with Arabic, a reading and a meaning,
    no two with the same meaning; three conversations, the first one being the unit's dialogue; 4 ladders,
    4 swaps, 6 changes, 5 builds, 5 speaking prompts; grammar cards whose checks have one right answer;
    6 gaps with four different choices; 5 sentences to fix
  - Home lists them after unit 12 and no longer announces units to come; a learner who has finished
    unit 12 is sent to unit 13; the landing and plans pages say 16 units
  - unit 13 in the browser: a word lesson runs to its end and its words are met; the conversation, the
    grammar cards and Practise open; the unit test, passed, opens unit 14
  - after unit 16's test the path is finished

  python3 .claude/skills/webapp-testing/scripts/with_server.py \
    --server "python3 -m http.server 8765 >/dev/null 2>&1" --port 8765 -- python3 tests/new_units.py
"""
import json, os, sys
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8765/"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
NEW = ["13", "14", "15", "16"]
seen = lambda *ks: {k: {"box": 0, "seen": 1} for k in ks}
UPTO = lambda n: seen("p:00|placed", "p:0b|placed", *[f"p:{i:02d}|placed" for i in range(1, n)])     # everything before unit n skipped

def page_with(b, mirror, errors, path):
    c = b.new_context(viewport={"width": 390, "height": 844})
    c.route("**/@supabase/**", lambda r: r.abort())                       # signed out: progress from the local copy
    c.route("https://fonts.googleapis.com/**", lambda r: r.abort())
    c.add_init_script("if(!localStorage.getItem('__seeded')){localStorage.setItem('rafiq_progress_mirror',%s);localStorage.setItem('__seeded','1')}"
                      % json.dumps(json.dumps(mirror)))
    p = c.new_page(); p.on("pageerror", lambda e: errors.append(path + ": " + str(e)))
    p.goto(BASE + path); p.wait_for_timeout(1500)
    return p

kicker = lambda p: p.evaluate("(document.querySelector('.kicker') || {}).textContent || ''").strip()
go = lambda p: (p.locator(".foot button.go:not([disabled])").first.click(timeout=15000), p.wait_for_timeout(200))
done = lambda p: p.locator(".done").count() > 0

# what's wrong with each new unit's content, as a list of short notes (empty = fine)
CONTENT = """(() => { const out = [], AR = /[\\u0600-\\u06FF]/, LAT = /[A-Za-z]/, by = new Map(VOCAB.map(w => [w.id, w]));
  const earlier = new Set(PATH.slice(0, 12).flatMap(u => u.words).concat(BASICS.flatMap(l => l.words))), taken = new Set();
  const ar = (where, s) => { if(typeof s !== 'string' || !AR.test(s) || LAT.test(s)) out.push(where + ': not Arabic: ' + s); };
  for(const n of %s){
    const p = PATH.find(u => u.n === n), u = DATA.find(x => x.n === n), e = EXTRA[n], note = t => out.push(n + ' ' + t);
    if(!p || !u || !e){ note('missing'); continue; }
    if(p.words.length !== 40 || new Set(p.words).size !== 40) note('not 40 different words');
    p.words.forEach(id => { const w = by.get(id);
      if(!w || !w.ar || !w.en || !w.tr) note('word ' + id + ' incomplete');
      if(earlier.has(id) || taken.has(id)) note('word ' + id + ' is taught earlier'); taken.add(id); });
    const gl = p.words.map(id => (by.get(id) || {}).en); if(new Set(gl).size !== gl.length) note('two words with the same meaning');
    if(u.convos.length !== 3 || u.convos.some(c => c.lines.length < 10 || c.lines.length > 12 || c.lines.some(l => l.length !== 3))) note('conversations');
    u.convos.forEach(c => c.lines.forEach(l => { ar(n + ' line', l[1]); if(AR.test(l[2])) note('Arabic in a translation'); }));
    if(JSON.stringify(u.dialogue) !== JSON.stringify(u.convos[0].lines)) note('the dialogue is not conversation 1');
    if(u.ladders.length !== 4 || u.ladders.some(l => l.steps.length !== 5 || !l.en)) note('ladders');
    if(u.subs.length !== 4 || u.subs.some(s => typeof s.tpl[0] !== 'string' || !s.tpl.some(Array.isArray))) note('swaps');
    if(u.transforms.length !== 6 || u.transforms.some(t => t.task.length !== 2 || !t.src || !t.ans || t.src === t.ans)) note('changes');
    if(u.builds.length !== 5 || u.builds.some(x => x.parts.length !== 4 || !x.en)) note('builds');
    if(u.prompts.length !== 5 || u.prompts.some(x => x.length !== 4)) note('prompts');
    u.prompts.forEach(x => { ar(n + ' prompt', x[0]); ar(n + ' model', x[2]); });
    if(e.grammar.length < 3 || e.grammar.some(g => !g.t || !g.ar || !g.h || !g.tr || !g.en)) note('grammar cards');
    e.grammar.forEach(g => { if(g.check && (g.check[1].length < 2 || new Set(g.check[1]).size !== g.check[1].length || !(g.check[2] >= 0 && g.check[2] < g.check[1].length))) note('a card check'); });
    if(e.cloze.length !== 6 || e.cloze.some(c => c.q.split('___').length !== 2 || c.o.length !== 4 || new Set(c.o).size !== 4 || !(c.a >= 0 && c.a < 4) || !c.w)) note('gaps');
    if(e.fix.length !== 5 || e.fix.some(f => !f.bad || !f.good || f.bad === f.good || !f.w)) note('fixes');
  }
  return out; })()""" % json.dumps(NEW)
# units 1 to 12 as they were before #344: the same words in the same order (learners' finished lessons depend on it)
OLD = "(() => { let k = 0; PATH.slice(0, 12).forEach((u, ui) => u.words.forEach((id, i) => { k = (k * 31 + id * (i + 1) + ui) % 1000000007; })); return [PATH.slice(0, 12).map(u => u.words.length), k]; })()"

def main():
    ok, errors = [], []
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME if os.path.exists(CHROME) else None)

        # the content, read from the page's own data
        p = page_with(b, UPTO(13), errors, "dashboard.html")
        units = p.evaluate("PATH.map(u => u.n + ' ' + u.en)")
        ok.append(("the path has 16 units, ending " + " | ".join(units[12:]), len(units) == 16 and units[12:] == ["13 Ramadan & Eid", "14 Health & the body", "15 Travel & directions", "16 Telling stories"]))
        old = p.evaluate(OLD)
        ok.append(("units 1 to 12 teach the words they did before " + str(old), old == [[40, 40, 45, 40, 40, 39, 40, 22, 40, 40, 26, 26], 448654497]))
        bad = p.evaluate(CONTENT)
        ok.append(("each new unit's words, conversations, drills and grammar are complete " + "; ".join(bad[:6]), not bad))
        steps = p.evaluate("RafiqPath.steps(RafiqPath.units().find(u => u.n === '13')).map(s => s.key)")
        want = ["meet1", "review1", "meet2", "review2", "listen", "grammar", "meet3", "review3", "meet4", "review4", "practise",
                "meet5", "review5", "meet6", "review6", "meet7", "review7", "meet8", "review8", "chat", "speak", "test"]
        ok.append(("a new unit's steps: 8 lessons of 5 with their reviews, as units 4 to 12", steps == want))

        # Home
        nxt = p.evaluate("(() => { const n = RafiqPath.next(); return n.unit.n + '|' + n.step.key; })()")
        ok.append(("after unit 12, next is unit 13 (" + nxt + ")", nxt == "13|meet1"))
        home = p.inner_text("#home")
        ok.append(("Home lists units 13 to 16", all(t in home for t in ["13. Ramadan & Eid", "14. Health & the body", "15. Travel & directions", "16. Telling stories"])))
        ok.append(("…and no longer says more units are coming", "More units coming" not in home and p.evaluate("RafiqPath.COMING.length") == 0))
        ok.append(("unit 14 is locked until 13 is done", not p.evaluate("RafiqPath.unitOpen('14')") and p.locator(".unit.later").count() == 3))
        p.close()
        for path, text in (("index.html", "all 16 units"), ("plans.html", "All 16 units")):
            p = page_with(b, {}, errors, path)
            ok.append((f"{path} says 16 units", text in p.inner_text("body") and "12 units" not in p.inner_text("body"))); p.close()

        # unit 13: a word lesson to its end
        p = page_with(b, UPTO(13), errors, "learn.html?u=13&s=meet1")
        first = p.inner_text("#w"); n = 0
        while not done(p) and n < 30:
            if p.locator(".opt").count(): p.locator(".opt").first.click(); p.wait_for_timeout(120)
            go(p); n += 1
        ok.append(("unit 13's first lesson opens on رَمَضان and runs to its end (%d screens)" % n, first == "رَمَضان" and done(p)))
        ok.append(("its five words are met and in review", p.evaluate("RafiqPath.stepDone('13','meet1') && [795, 718, 796, 797, 798].every(id => RafiqPath.metWords().has(id) && !Progress.isNew('v:' + id))")))
        p.close()

        # the conversation, the grammar cards, Practise
        some = UPTO(13) | seen(*[f"p:13|{k}" for k in ["meet1", "review1", "meet2", "review2"]])
        p = page_with(b, some, errors, "learn.html?u=13&s=listen")
        ok.append(("the conversation (" + kicker(p) + ")", kicker(p) == "The crescent · line 1 of 11")); p.close()
        p = page_with(b, some | seen("p:13|listen"), errors, "learn.html?u=13&s=grammar")
        cards = checks = 0
        while not done(p) and cards + checks < 12:
            if p.locator(".opt").count(): checks += 1; p.locator(".opt").first.click(); p.wait_for_timeout(120)
            else: cards += 1
            go(p)
        ok.append(("three grammar cards, each with a quick check (%d, %d)" % (cards, checks), cards == 3 and checks == 3 and done(p))); p.close()
        p = page_with(b, some, errors, "session.html?unit=13&n=10")
        ok.append(("Practise opens on the unit's sentences", "UNIT 13 · RAMADAN & EID" in p.inner_text("body").upper())); p.close()

        # the unit test, passed, opens the next unit; after unit 16's, the path is finished
        for n in ("13", "16"):
            keys = [k for k in want if k != "test"]
            p = page_with(b, UPTO(int(n)) | seen(*[f"p:{n}|{k}" for k in keys]), errors, f"learn.html?u={n}&s=test")
            q = 0
            while kicker(p).startswith("Unit test") and q < 30:
                p.evaluate("[...document.querySelectorAll('.opt')].find(b => b._o === asking.right).click()"); p.wait_for_timeout(100); go(p); q += 1
            passed = "passed" in p.inner_text(".done")
            if n == "13": ok.append(("unit 13's test: %d questions, passed, and unit 14 opens" % q, q == 18 and passed and p.evaluate("RafiqPath.unitOpen('14')")))
            else: ok.append(("unit 16's test passed: the path is finished", passed and p.evaluate("RafiqPath.next().finishedAll")))
            p.close()
        b.close()
    ok.append(("no page errors " + "; ".join(e[:160] for e in errors[:3]), not errors))
    for name, good in ok: print(("ok   " if good else "FAIL ") + name)
    sys.exit(0 if all(g for _, g in ok) else 1)

if __name__ == "__main__":
    main()
