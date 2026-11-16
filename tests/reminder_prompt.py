"""The reminder prompt on Home, in a browser (#377): a learner with no reminder is asked once, from their second
study day; picking a time sets an email reminder; someone who said "No reminders", or has one, isn't asked.

  python3 .claude/skills/webapp-testing/scripts/with_server.py \
    --server "python3 -m http.server 8765 >/dev/null 2>&1" --port 8765 -- python3 tests/reminder_prompt.py
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from startup_speed import FAKE, MIRROR, BASE
from playwright.sync_api import sync_playwright

# the fake sign-in, with the reminders table answering window.__rem (one row, or none) and everything else window.__rows
REM = FAKE.replace("return { from: q,", "return { from: t => t === 'reminders' ? one(window.__rem) : q(),") \
          .replace("const session = ", "const one = v => { const o = new Proxy(function(){}, { get: (t, k) => k === 'then' ? (res => wait({ data: v || null, error: null }).then(res)) : () => o }); return o; };\n  const session = ")
assert REM.count("one(window.__rem)") == 1 and REM.count("const one = ") == 1, "FAKE in tests/startup_speed.py has changed: update the two replacements above"
ok, errors = [], []

def home(b, days, rem="null"):
    # the learner's progress 'on the server': MIRROR, plus this many study days
    rows = [{"item_id": k, "box": v["box"], "due": None, "seen": v["seen"]} for k, v in MIRROR.items()] + \
           [{"item_id": "s:2026-11-0%d" % (i + 1), "box": 0, "due": None, "seen": 1} for i in range(days)]
    c = b.new_context(viewport={"width": 390, "height": 760})
    c.route("**/@supabase/**", lambda r: r.fulfill(status=200, content_type="application/javascript", body=REM))
    c.add_init_script("window.__rows = %s; window.__rem = %s; localStorage.setItem('rafiq_onboarded','u1');" % (json.dumps(rows), rem))
    p = c.new_page(); p.on("pageerror", lambda e: errors.append(str(e)))
    p.goto(BASE + "dashboard.html"); p.wait_for_timeout(3500)       # the prompt runs after the page has loaded
    return c, p

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium")

    c, p = home(b, 1)
    ok.append(("one study day: not asked yet", p.locator("#remPrompt .rem-card").count() == 0)); c.close()

    c, p = home(b, 2)
    ok.append(("a second study day, no reminder: asked", p.locator("#remPrompt .rem-card").count() == 1 and "Want a daily reminder?" in p.inner_text("#remPrompt")))
    p.locator("#remPrompt [data-h='19']").click(); p.wait_for_timeout(1500)
    t = p.inner_text("#remPrompt")
    ok.append(("picking 19:00 sets an email reminder", "Reminder set for 19:00" in t and "You’ll get an email" in t)); c.close()

    c, p = home(b, 2, "{enabled: false, by_email: false}")
    ok.append(("said \"No reminders\": not asked", p.locator("#remPrompt .rem-card").count() == 0)); c.close()

    c, p = home(b, 2, "{enabled: true, hour: 19, by_email: true}")
    ok.append(("already has a reminder: not asked", p.locator("#remPrompt .rem-card").count() == 0)); c.close()
    b.close()

ok.append(("no page errors " + "; ".join(errors[:3]), not errors))
for name, good in ok: print(("ok  " if good else "FAIL"), name)
print("\n%d of %d passed" % (sum(g for _, g in ok), len(ok)))
sys.exit(0 if all(g for _, g in ok) else 1)
