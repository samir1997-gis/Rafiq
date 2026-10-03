"""The landing page's one-minute taster (#207):
  - under the hero: four words from the app's word list (vocab-data.js), each said with its recording
  - a wrong pick isn't marked wrong: the right meaning lights up and "Now you know it!", then Next
  - a right pick: "✓ Nice!", and it moves on by itself once the word's been said
  - no score anywhere; it ends on "You just learned 4 Arabic words" and "Keep the momentum going →",
    which goes to Create account (the free week)
  - doing it is noted with where they came from (rafiq_src: started, then done), saved with a new account
  - no sideways scroll on a phone, no page errors

  python3 .claude/skills/webapp-testing/scripts/with_server.py \
    --server "python3 -m http.server 8765 >/dev/null 2>&1" --port 8765 -- python3 tests/taster.py
"""
import json, os, sys
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8765/"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
POOL = {"بَيْت": "house", "ماء": "water", "كِتاب": "book", "باب": "door", "قَلَم": "pen"}

def main():
    ok, errors = [], []
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME if os.path.exists(CHROME) else None)
        c = b.new_context(viewport={"width": 390, "height": 844}, has_touch=True)
        c.route("**/@supabase/**", lambda r: r.abort()); c.route("https://fonts.googleapis.com/**", lambda r: r.abort())
        p = c.new_page(); p.on("pageerror", lambda e: errors.append(str(e)))
        p.goto(BASE + "index.html")
        p.wait_for_selector(".tst-word", timeout=8000)
        # what gets said: audio.js's RQ.speak, recorded (and finishing at once)
        p.evaluate("window.SAID = []; RQ.speak = (t, el, after) => { SAID.push(t); if(after) after(); }")
        ok.append(("it sits under the hero, before the film", p.evaluate(
            "document.querySelector('.hero').compareDocumentPosition(document.getElementById('taster')) & 4 && document.getElementById('taster').compareDocumentPosition(document.getElementById('film-section')) & 4") > 0))
        ok.append(("phone: no sideways scroll", p.evaluate("document.documentElement.scrollWidth") <= 390))

        seen, wrong_done = [], False
        for i in range(4):
            p.wait_for_selector(".tst-word")
            ar = p.inner_text(".tst-word").replace("🔊", "").strip()
            seen.append(ar)
            en = POOL.get(ar)
            opts = p.evaluate("[...document.querySelectorAll('.tst-opt')].map(b => b.textContent)")
            if i == 0:
                ok.append((f"word 1: {ar} with three meanings {opts}", en in opts and len(opts) == 3))
                wrong = next(o for o in opts if o != en)
                p.click(f'.tst-opt:text-is("{wrong}")'); p.wait_for_timeout(200)
                st = p.evaluate("""(() => ({ right: document.querySelector('.tst-opt.right').textContent,
                  picked: document.querySelector('.tst-opt.picked').textContent, say: document.querySelector('.tst-say').textContent,
                  red: [...document.querySelectorAll('.tst-opt')].some(b => getComputedStyle(b).backgroundColor === 'rgb(180, 50, 42)'),
                  next: !document.querySelector('.tst-next').hidden }))()""")
                ok.append(("a wrong pick: the right one lights up, nothing red, 'Now you know it!' " + st["say"],
                           st["right"] == en and st["picked"] == wrong and "Now you know it" in st["say"] and not st["red"] and st["next"]))
                ok.append(("…and the word is said: " + p.evaluate("SAID[SAID.length-1]"), p.evaluate("SAID[SAID.length-1]") == ar))
                src = json.loads(p.evaluate("localStorage.getItem('rafiq_src')"))
                ok.append(("noted as started with where they came from: " + str(src), src.get("taster") == "started" and src.get("src") == "direct"))
                p.wait_for_timeout(900)
                ok.append(("…it waits for Next", p.inner_text(".tst-word").replace("🔊", "").strip() == ar))
                p.click(".tst-next")
            else:
                p.click(f'.tst-opt:text-is("{en}")'); p.wait_for_timeout(150)
                say = p.inner_text(".tst-say")
                if i == 1: ok.append(("a right pick: " + say, "Nice" in say and p.inner_text(".tst-opt.right") == en))
                p.wait_for_timeout(1000)                               # moves on by itself
        ok.append(("four different words from the word list " + str(seen), len(set(seen)) == 4 and all(a in POOL for a in seen)))
        p.wait_for_selector(".tst-end", timeout=3000)
        end = p.inner_text(".tst-end")
        ok.append(("ends on the win: " + " ".join(end.split())[:80], "You just learned 4 Arabic words in under a minute" in end
                   and "Imagine what you’d know in a month" in end and "/" not in end.split("learned")[0]))
        go = p.get_attribute(".tst-go", "href")
        ok.append(("'Keep the momentum going →' goes to Create account: " + go, go == "login.html?mode=signup" and "Keep the momentum going" in p.inner_text(".tst-go")))
        ok.append(("…with 'no card' under it", "no card" in p.inner_text(".tst-free")))
        ok.append(("the words learned are there to hear again", p.locator(".tst-chip").count() == 4))
        p.click(".tst-chip >> nth=0")
        ok.append(("…tap one: " + p.evaluate("SAID[SAID.length-1]"), p.evaluate("SAID[SAID.length-1]") == seen[0] or p.evaluate("SAID[SAID.length-1]") in seen))
        src = json.loads(p.evaluate("localStorage.getItem('rafiq_src')"))
        ok.append(("noted as done: " + str(src), src.get("taster") == "done"))
        b.close()

    for name, good in ok: print(("ok   " if good else "FAIL ") + name)
    for e in errors: print("page error:", e)
    sys.exit(0 if all(g for _, g in ok) and not errors else 1)

if __name__ == "__main__":
    main()
