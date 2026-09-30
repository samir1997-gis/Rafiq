"""Teach first (#156), units 1-3:
  - the steps: two word lessons, then How it works, the rest of the words, Practise, and the
    conversation last (unit 4 unchanged); progress saved under the old order still counts
  - unit 1 starts with ten single words; greeting phrases are shown word by word
  - word lessons end with "Hear it, pick the word"
  - How it works has the new cards (three endings, the past, describing words, 'this house'),
    each with a common mistake crossed out
  - Practise only uses exercises made from taught words

  python3 .claude/skills/webapp-testing/scripts/with_server.py \
    --server "python3 -m http.server 8765 >/dev/null 2>&1" --port 8765 -- python3 tests/teach.py
"""
import json, os, sys, datetime
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8765/"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
TODAY = datetime.date.today().isoformat()
seen = lambda *ks: {k: {"box": 0, "seen": 1} for k in ks}

def page_with(b, mirror, errors):
    c = b.new_context(viewport={"width": 390, "height": 844})
    c.route("**/@supabase/**", lambda r: r.abort())                       # signed out: progress from the local copy
    c.route("https://fonts.googleapis.com/**", lambda r: r.abort())
    c.add_init_script("if(!localStorage.getItem('__seeded')){localStorage.setItem('rafiq_progress_mirror',%s);localStorage.setItem('__seeded','1')}"
                      % json.dumps(json.dumps(mirror)))
    p = c.new_page(); p.on("pageerror", lambda e: errors.append(str(e)))
    return p

def main():
    ok, errors = [], []
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME if os.path.exists(CHROME) else None)

        # the steps, and progress saved under the old order
        p = page_with(b, seen("p:00|placed"), errors); p.goto(BASE + "dashboard.html"); p.wait_for_timeout(1500)
        keys = lambda n: p.evaluate(f"RafiqPath.steps(RafiqPath.units().find(u => u.n === '{n}')).map(s => s.key)")
        ok.append(("unit 1 order " + str(keys("01")), keys("01") == ["words1", "words2", "grammar", "words3", "words4", "practise", "listen", "chat", "speak", "test"]))
        ok.append(("unit 3 keeps its late words before Practise", keys("03")[:3] == ["words1", "words2", "grammar"] and keys("03")[-5:] == ["practise", "listen", "chat", "speak", "test"]))
        ok.append(("unit 4 unchanged (plus its test)", keys("04") == ["words1", "listen", "grammar", "words2", "practise", "words3", "words4", "chat", "speak", "test"]))
        first = p.evaluate("RafiqPath.wordsOf(RafiqPath.units().find(u => u.n === '01'), 0).map(w => w.ar)")
        ok.append(("unit 1 starts with ten single words " + " ".join(first), len(first) == 10 and all(" " not in w.strip() for w in first)))
        bad_keys = p.evaluate("""(() => { const all = new Set(VOCAB.map(w => w.ar.trim()));
          return ['السَّلامُ عَلَيْكُم','وَعَلَيْكُمُ السَّلام','كَيْفَ حالُكَ','كَيْفَ حالُكِ','الحَمْدُ لِلَّهِ','أَهْلاً وَسَهْلاً','مَعَ السَّلامَةِ',
            'ما اسْمُكَ؟','ما اسْمُكِ؟','ما جِنْسِيَّتُكَ؟','ما جِنْسِيَّتُكِ؟','مِنْ أَيْنَ؟','ما شاءَ اللهُ','إِلى أَيْنَ'].filter(k => !all.has(k)); })()""")
        p.goto(BASE + "learn.html?u=01&s=words1"); p.wait_for_timeout(300)
        ok.append(("every phrase taken apart is a real word-list entry " + str(bad_keys), bad_keys == []))
        p.close()

        old = seen("p:00|placed", "p:01|words1", "p:01|listen", "p:01|grammar")
        p = page_with(b, old, errors); p.goto(BASE + "dashboard.html"); p.wait_for_timeout(1500)
        nxt = p.evaluate("(() => { const n = RafiqPath.next(); return n.unit.n + '|' + (n.step && n.step.key); })()")
        ok.append(("mid-unit under the old order: next is words2 (" + nxt + ")", nxt == "01|words2")); p.close()
        done = seen("p:00|placed", *[f"p:01|{k}" for k in ["words1", "listen", "grammar", "words2", "practise", "words3", "words4", "chat", "speak", "test"]])
        p = page_with(b, done, errors); p.goto(BASE + "dashboard.html"); p.wait_for_timeout(1500)
        ok.append(("unit 1 finished under the old order stays finished", p.evaluate("RafiqPath.unitDone(RafiqPath.units().find(u => u.n === '01'))"))); p.close()

        # word lessons: phrases word by word, and the hearing round
        p = page_with(b, seen("p:00|placed", "p:01|words1"), errors); p.goto(BASE + "learn.html?u=01&s=words2"); p.wait_for_timeout(1500)
        parts = p.eval_on_selector_all(".wparts span", "ss => ss.map(s => s.innerText.replace(/\\n/g, ' = '))")
        ok.append(("السَّلامُ عَلَيْكُم taken apart " + str(parts), len(parts) == 2 and "peace" in parts[0]))
        kinds, last = [], None
        for _ in range(120):
            if "learn.html" not in p.url: break
            k = p.evaluate("(() => { const k = document.querySelector('.kicker'); return k ? k.textContent.trim() : ''; })()")   # textContent: not the CSS capitals
            sig = k + p.evaluate("(document.querySelector('#stage') || document.body).innerText.slice(0, 120)")
            if k and sig != last:                  # a new screen
                kinds.append(k.split(" ")[0]); last = sig
                if k.startswith(("Hear it", "What does")):
                    p.locator(".opt").first.click(); p.wait_for_timeout(250)
                    last = k + p.evaluate("(document.querySelector('#stage') || document.body).innerText.slice(0, 120)")
            btn = p.locator("button.go:not([disabled])")
            if btn.count():
                try: btn.first.click(timeout=2000)
                except Exception: pass
            p.wait_for_timeout(250)
            if not k and not btn.count(): break
        ok.append(("words step: meet 10, pick the meaning 10, then hear it 5 (%d/%d/%d)" % (kinds.count("New"), kinds.count("What"), kinds.count("Hear")),
                   kinds.count("New") == 10 and kinds.count("What") == 10 and kinds.count("Hear") == 5)); p.close()

        # How it works in unit 2: the new cards and the crossed-out mistakes
        p = page_with(b, seen("p:00|placed", "p:01|words1", "p:01|words2", "p:01|grammar", "p:01|words3", "p:01|words4", "p:01|practise",
                              "p:01|listen", "p:01|chat", "p:01|speak", "p:02|words1", "p:02|words2"), errors)
        p.goto(BASE + "learn.html?u=02&s=grammar"); p.wait_for_timeout(1500)
        titles, bads = [], 0
        for _ in range(8):
            if not p.locator(".gh").count(): break
            titles.append(p.inner_text(".gh")); bads += p.locator(".gbad s").count()
            p.locator("button.go:not([disabled])").first.click(timeout=15000); p.wait_for_timeout(250)   # Next opens once the example has played
            if p.locator(".opt").count():                                                               # a quick check (#163)
                p.locator(".opt").first.click(); p.wait_for_timeout(150)
                p.locator("button.go:not([disabled])").first.click(); p.wait_for_timeout(250)
        ok.append(("unit 2 How it works: %d cards, %d with a crossed-out mistake" % (len(titles), bads), len(titles) == 4 and bads == 4))   # ‘My’ endings and ‘X of Y’ now taught in the basics (#166, #168)
        ok.append(("three endings and the past are taught", any("Three endings" in t for t in titles) and any("The past" in t for t in titles))); p.close()

        # Practise: only exercises made from taught words
        for n in ("01", "02", "03"):
            prev = {"01": [], "02": ["01"], "03": ["01", "02"]}[n]
            m = seen("p:00|placed", *[f"p:{u}|{k}" for u in prev for k in ["words1", "words2", "grammar", "words3", "words4", "practise", "listen", "chat", "speak"]],
                     *[f"p:{n}|{k}" for k in ["words1", "words2", "grammar", "words3", "words4", "words5"]])
            p = page_with(b, m, errors); p.goto(BASE + f"session.html?unit={n}"); p.wait_for_timeout(2000)
            r = p.evaluate(f"""(() => {{ const k = RafiqTeach.taught('{n}'), d = x => x.d;
              const text = x => x.mode==='cloze' ? d(x).q.replace('___',' ')+' '+(d(x).o||[]).join(' ') : x.mode==='fix' ? d(x).bad+' '+d(x).good
                : x.mode==='transform' ? d(x).src+' '+d(x).ans : x.mode==='build' ? d(x).parts.join(' ') : (d(x).ar||'');
              const s = Q.filter(x => x.kind === 'sentences');
              return {{ n: Q.length, s: s.length, low: s.filter(x => RafiqTeach.coverage(text(x), k) < 0.8).length }}; }})()""")
            ok.append((f"unit {n} Practise: {r['n']} items, {r['s']} sentences, {r['low']} with untaught words", r["n"] >= 8 and r["s"] >= 4 and r["low"] == 0))
            p.close()
        b.close()
    ok.append(("no page errors " + "; ".join(e[:120] for e in errors[:3]), not errors))
    for name, good in ok: print(("ok   " if good else "FAIL ") + name)
    sys.exit(0 if all(g for _, g in ok) else 1)

if __name__ == "__main__":
    main()
