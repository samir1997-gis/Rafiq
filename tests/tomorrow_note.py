"""The end of a lesson says what comes back tomorrow (#376): a count of the words and sentences due by then,
and no line at all when nothing is due.

  python3 .claude/skills/webapp-testing/scripts/with_server.py \
    --server "python3 -m http.server 8765 >/dev/null 2>&1" --port 8765 -- python3 tests/tomorrow_note.py
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from startup_speed import FAKE, MIRROR, BASE
from playwright.sync_api import sync_playwright

ok, errors = [], []
END = "(() => { const u = RafiqPath.units().find(x => x.n === '01'); finish(u, RafiqPath.steps(u)[0], ''); })()"

def page(b):
    c = b.new_context(viewport={"width": 390, "height": 760})
    c.route("**/@supabase/**", lambda r: r.fulfill(status=200, content_type="application/javascript", body=FAKE))
    c.add_init_script("if(!sessionStorage.getItem('t')){sessionStorage.setItem('t',1);localStorage.setItem('rafiq_progress_mirror', JSON.stringify(%s));}" % json.dumps(MIRROR))
    p = c.new_page(); p.on("pageerror", lambda e: errors.append(str(e)))
    p.goto(BASE + "learn.html?u=01&s=meet1"); p.wait_for_timeout(2500)
    return c, p

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium")

    c, p = page(b)
    p.evaluate(END); p.wait_for_timeout(500)
    ok.append(("nothing due tomorrow: no line", p.locator("#tmrw").count() == 0))
    c.close()

    c, p = page(b)
    p.evaluate("Progress.grade('v:1','good',1)")
    p.evaluate(END); p.wait_for_timeout(500)
    ok.append(("one due: singular wording", p.locator("#tmrw").count() == 1 and "1 word or sentence comes back" in p.inner_text("#tmrw")))
    c.close()

    c, p = page(b)
    p.evaluate("Progress.grade('v:1','good',1); Progress.grade('v:2','good',1); Progress.grade('v:3','good',30)")
    p.evaluate(END); p.wait_for_timeout(500)
    ok.append(("two due tomorrow and one due in a month: counts 2", "2 words and sentences come back" in p.inner_text("#tmrw")))
    c.close()
    b.close()

ok.append(("no page errors " + "; ".join(errors[:3]), not errors))
for name, good in ok: print(("ok  " if good else "FAIL"), name)
print("\n%d of %d passed" % (sum(g for _, g in ok), len(ok)))
sys.exit(0 if all(g for _, g in ok) else 1)
