"""Signed out after time away (#373): a learner whose browser has been idle past the limit is sent to sign-in with a
message, not to the landing page. The limit is 30 days, or a day on a device they marked as shared. Log out is unchanged.

  python3 .claude/skills/webapp-testing/scripts/with_server.py \
    --server "python3 -m http.server 8765 >/dev/null 2>&1" --port 8765 -- python3 tests/idle_signout.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from startup_speed import FAKE, BASE
from playwright.sync_api import sync_playwright

# the fake sign-in, but signing out really ends the session (kept in localStorage so it survives the redirect)
OUT = FAKE.replace("getSession: async () => ({ data: { session } })",
                   "getSession: async () => ({ data: { session: localStorage.getItem('t_out') ? null : session } })") \
          .replace("signOut: async () => ({})", "signOut: async () => { localStorage.setItem('t_out', '1'); return {}; }")
assert OUT.count("t_out") == 2, "FAKE in tests/startup_speed.py has changed: update the two replacements above"
DAY = 86400000
ok, errors = [], []

def page(b, init):
    c = b.new_context(viewport={"width": 390, "height": 760})
    c.route("**/@supabase/**", lambda r: r.fulfill(status=200, content_type="application/javascript", body=OUT))
    # 'rafiq_onboarded': a learner who has finished the sign-up questions, so Home doesn't send them there
    c.add_init_script("if(!sessionStorage.getItem('t')){sessionStorage.setItem('t',1);localStorage.setItem('rafiq_onboarded','u1');" + init + "}")
    p = c.new_page(); p.on("pageerror", lambda e: errors.append(str(e)))
    return c, p

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium")

    c, p = page(b, f"localStorage.setItem('bay_last_active', String(Date.now() - 31 * {DAY}));")
    p.goto(BASE + "dashboard.html"); p.wait_for_timeout(2500)
    ok.append(("31 days away: sent to sign-in, not the landing page: " + p.url, p.url.endswith("login.html?away=1")))
    ok.append(("…with a line that says why", "signed out after a while away" in p.inner_text("#msg")))
    c.close()

    c, p = page(b, f"localStorage.setItem('bay_last_active', String(Date.now() - 2 * {DAY}));")
    p.goto(BASE + "dashboard.html"); p.wait_for_timeout(2500)
    ok.append(("2 days away on their own device: still signed in: " + p.url, "dashboard.html" in p.url))
    c.close()

    c, p = page(b, f"localStorage.setItem('bay_last_active', String(Date.now() - 2 * {DAY})); localStorage.setItem('rafiq_shared', '1');")
    p.goto(BASE + "dashboard.html"); p.wait_for_timeout(2500)
    ok.append(("2 days away on a shared device: sent to sign-in: " + p.url, p.url.endswith("login.html?away=1")))
    c.close()

    c, p = page(b, "")
    p.goto(BASE + "dashboard.html"); p.wait_for_timeout(2000)
    p.evaluate("logout()"); p.wait_for_timeout(2000)
    ok.append(("Log out still goes to the landing page: " + p.url, p.url.endswith("index.html")))
    c.close()

    c, p = page(b, "localStorage.setItem('t_out', '1');")
    p.goto(BASE + "login.html"); p.wait_for_timeout(1500)
    p.check("#shared")
    on = p.evaluate("localStorage.getItem('rafiq_shared')")
    p.uncheck("#shared")
    ok.append(("the shared-device box is remembered, and forgotten when unticked", on == "1" and p.evaluate("localStorage.getItem('rafiq_shared')") is None))
    c.close()
    b.close()

ok.append(("no page errors " + "; ".join(errors[:3]), not errors))
for name, good in ok: print(("ok  " if good else "FAIL"), name)
print("\n%d of %d passed" % (sum(g for _, g in ok), len(ok)))
sys.exit(0 if all(g for _, g in ok) else 1)
