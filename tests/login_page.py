"""The login page (#172):
  - the opening plays once a visit (mark draws, word is written, card rises), is gone within 2 s,
    can be tapped away, and never plays for reduced motion
  - Sign in / Create account is a sliding switch; the name field folds open for a new account
  - a missing or wrong-looking email shows under the field, without asking the server
  - signing in: the button becomes a spinner, then a tick, then you're in; a wrong password shakes the card
  - show / hide password

  python3 .claude/skills/webapp-testing/scripts/with_server.py \
    --server "python3 -m http.server 8765 >/dev/null 2>&1" --port 8765 -- python3 tests/login_page.py
"""
import os, sys
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8765/"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
VIDEO = os.environ.get("LOGIN_VIDEO")       # a folder: record the run there
FAKE = """
window.__calls = [];
window.supabase = { createClient: () => {
  const q = () => { const o = new Proxy(function(){}, { get: (t, k) => k === 'then'
      ? (res => res({ data: { onboarded: true }, error: null })) : () => o }); return o; };
  const user = { id: 'u1', email: 'sam@example.com', user_metadata: { name: 'Sam' } };
  return { from: q, auth: {
    getSession: async () => ({ data: { session: null } }), getUser: async () => ({ data: { user } }),
    signInWithPassword: async ({ password }) => { __calls.push('signin'); await new Promise(r => setTimeout(r, 900));
      return password === 'right-password' ? { data: { user }, error: null } : { data: {}, error: { message: 'Invalid login credentials' } }; },
    onAuthStateChange: () => ({ data: { subscription: { unsubscribe() {} } } }) } };
} };
"""

def ctx_for(b, **kw):
    c = b.new_context(viewport={"width": 390, "height": 844}, **kw)
    c.route("**/@supabase/**", lambda r: r.fulfill(status=200, content_type="application/javascript", body=FAKE))
    c.route("**/auth/v1/settings", lambda r: r.fulfill(status=200, content_type="application/json", body='{"external":{"google":true,"apple":true}}'))
    c.route("https://fonts.googleapis.com/**", lambda r: r.abort())
    c.route("**/dashboard.html", lambda r: r.fulfill(status=200, content_type="text/html", body="<p>home</p>"))   # where we land isn't under test
    return c

def main():
    ok, errors = [], []
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME if os.path.exists(CHROME) else None)
        c = ctx_for(b, **({"record_video_dir": VIDEO, "record_video_size": {"width": 390, "height": 844}} if VIDEO else {}))
        p = c.new_page(); p.on("pageerror", lambda e: errors.append(str(e)))
        intro = lambda: p.evaluate("document.documentElement.classList.contains('intro')")

        # the opening
        p.goto(BASE + "login.html"); p.wait_for_timeout(300)
        ok.append(("the opening plays on first visit", intro()))
        p.wait_for_timeout(1800)
        ok.append(("…and is over within 2 s", not intro()))
        ok.append(("the card is fully there", p.evaluate("getComputedStyle(document.getElementById('authForm')).opacity") == "1"))
        p.reload(); p.wait_for_timeout(200)
        ok.append(("not again in the same visit", not intro()))

        # the switch
        h = lambda: p.evaluate("document.getElementById('nameField').getBoundingClientRect().height")
        ok.append(("signing in: no name field (%dpx), and it can't be tabbed to" % h(), h() < 2 and p.evaluate("document.getElementById('nameField').inert")))
        p.click("#seg [data-mode=signup]"); p.wait_for_timeout(500)
        ok.append(("Create account: the name field folds open (%dpx)" % h(), h() > 50 and p.locator("#submitBtn").inner_text() == "Create account"))
        ok.append(("…and the pill has slid across", p.evaluate("getComputedStyle(document.querySelector('.seg .pill')).transform") != "none"))
        p.click("#seg [data-mode=signin]"); p.wait_for_timeout(500)

        # checks under the field, no server call
        p.click("#submitBtn"); p.wait_for_timeout(200)
        ok.append(("no email: said under the field", "Enter your email" in p.inner_text("#authForm .field.bad")))
        p.fill("#email", "sam@example"); p.wait_for_timeout(100)
        ok.append(("typing clears it", p.locator(".field.bad").count() == 0))
        p.click("#submitBtn"); p.wait_for_timeout(200)
        ok.append(("a wrong-looking email: said under the field", "look right" in p.inner_text("#authForm .field.bad") and p.evaluate("__calls.length") == 0))
        p.fill("#email", "sam@example.com"); p.click("#submitBtn"); p.wait_for_timeout(200)
        ok.append(("no password: said under that field", "Enter your password" in p.inner_text("#authForm .field.bad")))

        # show / hide
        p.fill("#pw", "wrong-one"); p.click("#eye")
        ok.append(("show password", p.get_attribute("#pw", "type") == "text"))
        p.click("#eye")
        ok.append(("hide it again", p.get_attribute("#pw", "type") == "password"))

        # wrong password: spinner, then the message and a shake
        p.click("#submitBtn"); p.wait_for_timeout(450)
        ok.append(("spinner while it checks (%dpx wide)" % p.evaluate("document.getElementById('submitBtn').offsetWidth"),
                   p.evaluate("document.getElementById('submitBtn').classList.contains('busy')") and p.evaluate("document.getElementById('submitBtn').offsetWidth") <= 60))
        p.wait_for_timeout(700)
        ok.append(("wrong password: told, the button is back", "don’t match" in p.inner_text("#msg") and p.inner_text("#submitBtn") == "Sign in"))

        # right password: tick, then in
        p.fill("#pw", "right-password"); p.click("#submitBtn"); p.wait_for_timeout(1050)
        ok.append(("a tick before going in", p.evaluate("document.getElementById('submitBtn').classList.contains('ok')")))
        p.wait_for_url("**/dashboard.html", timeout=4000)
        ok.append(("then in", p.url.endswith("dashboard.html")))
        c.close()

        # reduced motion: no opening
        c = ctx_for(b, reduced_motion="reduce"); p = c.new_page(); p.on("pageerror", lambda e: errors.append(str(e)))
        p.goto(BASE + "login.html"); p.wait_for_timeout(200)
        ok.append(("reduced motion: no opening", not intro()))
        c.close()

        # tapping skips it
        c = ctx_for(b); p = c.new_page(); p.on("pageerror", lambda e: errors.append(str(e)))
        p.goto(BASE + "login.html"); p.wait_for_timeout(300); p.mouse.click(20, 20); p.wait_for_timeout(50)
        ok.append(("a tap skips the opening", not intro()))
        c.close()
        b.close()
    ok.append(("no page errors " + "; ".join(e[:120] for e in errors[:3]), not errors))
    for name, good in ok: print(("ok   " if good else "FAIL ") + name)
    sys.exit(0 if all(g for _, g in ok) else 1)

if __name__ == "__main__":
    main()
