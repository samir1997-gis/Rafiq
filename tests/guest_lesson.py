"""The first lesson before the account (#381): a visitor does the two-minute first lesson as a guest, is asked to
create an account to keep it, and after sign-up the lesson counts without doing it again.

  - not signed in, onboarding.html?guest=1: the lesson runs; nothing is saved; "Create my free account" goes to sign-up
  - signed up after the guest lesson: straight to the two questions, the two words saved, today has a step done
  - not signed in without ?guest: sent to sign-in as before; signed in with ?guest: the ordinary start

  python3 .claude/skills/webapp-testing/scripts/with_server.py \
    --server "python3 -m http.server 8765 >/dev/null 2>&1" --port 8765 -- python3 tests/guest_lesson.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from startup_speed import FAKE, BASE
from playwright.sync_api import sync_playwright

NOBODY = FAKE.replace("getSession: async () => ({ data: { session } })", "getSession: async () => ({ data: { session: null } })") \
             .replace("getUser: () => wait({ data: { user: session.user } })", "getUser: () => wait({ data: { user: null } })")
assert NOBODY.count("session: null") == 1 and NOBODY.count("user: null") == 1, "FAKE in tests/startup_speed.py has changed"
ok, errors = [], []

def context(b, fake, init=""):
    c = b.new_context(viewport={"width": 390, "height": 760})
    c.route("**/@supabase/**", lambda r: r.fulfill(status=200, content_type="application/javascript", body=fake))
    c.add_init_script("if(!sessionStorage.getItem('t')){sessionStorage.setItem('t',1);" + init + "}")
    p = c.new_page(); p.on("pageerror", lambda e: errors.append(str(e)))
    return c, p

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium")

    # a visitor, not signed in
    c, p = context(b, NOBODY)
    p.goto(BASE + "onboarding.html?guest=1"); p.wait_for_timeout(1800)
    ok.append(("a guest stays on the lesson: " + p.url.split("/")[-1], "onboarding.html" in p.url and p.is_visible("#first")))
    p.click("#flNext"); p.wait_for_timeout(400)
    p.locator(".fl-opts .opt", has_text="Peace be upon you").click(); p.wait_for_timeout(200)
    p.click("#flNext"); p.wait_for_timeout(400)
    p.click("#flNext"); p.wait_for_timeout(400)
    ok.append(("no name yet, so step 4 is 'Now a name': " + p.inner_text("#flBody h1"), "Now a name" in p.inner_text("#flBody h1")))
    p.click("#flNext"); p.wait_for_timeout(400)
    for t in ("as-salāmu", "ismī", "Samir"):
        p.locator(".fl-tile", has_text=t).click(); p.wait_for_timeout(250)
    ok.append(("the sentence builds and Finish appears", p.locator(".fl-piece").count() == 3 and p.inner_text("#flNext") == "Finish"))
    p.click("#flNext"); p.wait_for_timeout(700)
    ok.append(("well done asks for an account: " + p.inner_text("#wellGo"), p.is_visible("#well") and p.inner_text("#wellGo") == "Create my free account"
               and "Create your free account" in p.inner_text("#well .fl-note")))
    got = p.evaluate("[localStorage.getItem('rafiq_guest_lesson'), Progress.isNew('v:1')]")
    ok.append(("the guest lesson is remembered on this device, nothing is saved yet (%s)" % got, got == ["1", True]))
    p.click("#wellGo"); p.wait_for_timeout(1200)
    ok.append(("the button goes to Create account: " + p.url.split("/")[-1], p.url.endswith("login.html?mode=signup")))
    c.close()

    # the same person, now signed up: the lesson counts, and the questions come next
    c, p = context(b, FAKE, "localStorage.setItem('rafiq_guest_lesson','1');")
    p.goto(BASE + "onboarding.html"); p.wait_for_timeout(1800)
    ok.append(("after sign-up: straight to the questions", p.is_visible("#qs") and not p.is_visible("#first")))
    got = p.evaluate("[Progress.isNew('v:1'), RafiqPath.doneToday() >= 1, localStorage.getItem('rafiq_guest_lesson')]")
    ok.append(("…the two words are saved, today has a step done, the flag is gone (%s)" % got, got == [False, True, None]))
    c.close()

    c, p = context(b, NOBODY)
    p.goto(BASE + "onboarding.html"); p.wait_for_timeout(2000)
    ok.append(("not signed in and not a guest: sent to sign-in: " + p.url.split("/")[-1], "login.html" in p.url))
    c.close()

    c, p = context(b, FAKE)
    p.goto(BASE + "onboarding.html?guest=1"); p.wait_for_timeout(2000)
    ok.append(("signed in with ?guest=1: the ordinary start: " + p.url.split("/")[-1], p.url.endswith("onboarding.html")))
    c.close()
    b.close()

ok.append(("no page errors " + "; ".join(errors[:3]), not errors))
for name, good in ok: print(("ok  " if good else "FAIL"), name)
print("\n%d of %d passed" % (sum(g for _, g in ok), len(ok)))
sys.exit(0 if all(g for _, g in ok) else 1)
