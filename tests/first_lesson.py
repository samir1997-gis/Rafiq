"""The faster start (#348): straight after confirming their email a learner gets a two-minute first lesson with their
own name, a "well done", two questions, then Home with a tour they can skip at every step.

  - onboarding opens on the lesson (no questions first, no video card)
  - the lesson: say hello, pick its meaning, "my name", their name in Arabic, then build the sentence from tiles
    (a tile out of order shakes and isn't taken)
  - well done, with their name; the two words are in their reviews and today has a step done
  - two questions (can you read Arabic letters, a reminder time), then Home with the tour
  - the tour: Skip ends it for good; "Show me more" carries on through Practise and ends back on Home
  - Settings → More → Show me around starts it again
  - an account that has done the lesson (a second confirm link, another tab) goes straight to the questions

Run (from the repo root), with the webapp-testing skill's server helper:
  python3 .claude/skills/webapp-testing/scripts/with_server.py \
    --server "python3 -m http.server 8765 >/dev/null 2>&1" --port 8765 -- python3 tests/first_lesson.py
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from startup_speed import FAKE, MIRROR, BASE
from playwright.sync_api import sync_playwright

ok, errors = [], []

def context(b, init, w=390, h=760):
    c = b.new_context(viewport={"width": w, "height": h})
    c.route("**/@supabase/**", lambda r: r.fulfill(status=200, content_type="application/javascript", body=FAKE))
    c.add_init_script("if(!sessionStorage.getItem('t')){sessionStorage.setItem('t',1);" + init + "}")
    p = c.new_page(); p.on("pageerror", lambda e: errors.append(str(e)))
    return c, p

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium")

    # a brand-new account, signed up as Samir
    c, p = context(b, "localStorage.setItem('bay_name','Samir');")
    p.goto(BASE + "onboarding.html"); p.wait_for_timeout(1500)
    ok.append(("onboarding opens on the first lesson, not the questions", p.is_visible("#first") and not p.is_visible("#qs")))
    ok.append(("no video card any more", p.locator("video").count() == 0))
    ok.append(("step 1: say hello (السَّلامُ عَلَيْكُمْ)", "السَّلامُ عَلَيْكُمْ" in p.inner_text("#flBody")))
    p.click("#flNext"); p.wait_for_timeout(400)
    ok.append(("step 2: Next waits for the right meaning", p.is_disabled("#flNext")))
    p.locator(".fl-opts .opt", has_text="Thank you").click(); p.wait_for_timeout(200)
    still = p.is_disabled("#flNext")
    p.locator(".fl-opts .opt", has_text="Peace be upon you").click(); p.wait_for_timeout(200)
    ok.append(("…a wrong pick doesn't move on; the right one does", still and not p.is_disabled("#flNext")))
    p.click("#flNext"); p.wait_for_timeout(400)
    ok.append(("step 3: my name (اسْمِي)", "اسْمِي" in p.inner_text("#flBody")))
    p.click("#flNext"); p.wait_for_timeout(400)
    ok.append(("step 4: their own name in Arabic (سَمِير)", "Samir" in p.inner_text("#flBody h1") and "سَمِير" in p.inner_text("#flBody")))
    p.click("#flNext"); p.wait_for_timeout(400)
    name_tile = p.locator(".fl-tile", has_text="Samir")
    name_tile.click(); p.wait_for_timeout(450)
    ok.append(("step 5: a tile out of order isn't taken", p.locator(".fl-piece").count() == 0 and "shake" in (name_tile.get_attribute("class") or "")))
    p.locator(".fl-tile", has_text="as-salāmu").click(); p.wait_for_timeout(200)
    p.locator(".fl-tile", has_text="ismī").click(); p.wait_for_timeout(200)
    p.locator(".fl-tile", has_text="Samir").click(); p.wait_for_timeout(300)
    ok.append(("…in order, the sentence builds and Finish appears", p.locator(".fl-piece").count() == 3 and p.inner_text("#flNext") == "Finish"))
    p.click("#flNext"); p.wait_for_timeout(700)
    ok.append(("well done, with their name", p.is_visible("#well") and p.inner_text("#wellH") == "Well done, Samir!"))
    got = p.evaluate("[Progress.isNew('v:1'), Progress.isNew('v:784'), RafiqPath.doneToday()]")
    ok.append(("the two words are in their reviews and today has a step done (%s)" % got, got == [False, False, 1]))
    p.click("#wellGo"); p.wait_for_timeout(300)
    ok.append(("then two questions", p.is_visible("#qs") and p.locator("#qs .q").count() == 2))
    p.locator("#qs .opt", has_text="Not yet").click(); p.locator("#qs .opt", has_text="Evening").click()
    p.click("#doneBtn"); p.wait_for_url("**/dashboard.html", timeout=8000)
    p.wait_for_selector("#tour", timeout=8000)
    ok.append(("Home opens with the tour", "Welcome to Rafiq, Samir" in p.inner_text("#tour")))
    p.click("#tour .t-skip"); p.wait_for_timeout(300)
    ok.append(("Skip ends it for good", p.locator("#tour").count() == 0 and p.evaluate("localStorage.getItem('rafiq_tour')") is None))
    p.reload(); p.wait_for_timeout(2500)
    ok.append(("…and it doesn't come back", p.locator("#tour").count() == 0))
    # Settings → More → Show me around, then all the way through "Show me more"
    p.goto(BASE + "settings.html"); p.wait_for_timeout(1200)
    p.click("#tourAgain"); p.wait_for_url("**/dashboard.html", timeout=8000); p.wait_for_selector("#tour", timeout=8000)
    home = 0
    while not p.locator("#tour .t-go", has_text="Show me more").count():
        p.locator("#tour .t-go").last.click(); p.wait_for_timeout(250); home += 1
    stops = p.inner_text("#tour .t-k")
    p.locator("#tour .t-go", has_text="Show me more").click()
    p.wait_for_url("**/practise.html", timeout=8000); p.wait_for_selector("#tour", timeout=8000)
    more = 0
    while p.locator("#tour").count():
        p.locator("#tour .t-go").last.click(); p.wait_for_timeout(250); more += 1
        if more > 20: break
    p.wait_for_timeout(800)
    ok.append(("Settings starts the tour again; Home's part has its stops, then 'Show me more' (%d stops)" % home, home >= 6))
    ok.append(("…carries on through Practise (%d stops) and ends back on Home" % more, more >= 6 and p.url.endswith("dashboard.html")
               and p.evaluate("localStorage.getItem('rafiq_tour')") is None))
    c.close()

    # an account that did the lesson already (the confirm link opened twice): straight to the questions
    c, p = context(b, "localStorage.setItem('bay_name','Maryam');localStorage.setItem('rafiq_first_lesson','u1');")
    uid = None
    p.goto(BASE + "onboarding.html"); p.wait_for_timeout(1500)
    if not p.is_visible("#qs"):        # the fake account's id may differ: set it from the page and reload
        uid = p.evaluate("UID"); p.evaluate("id => localStorage.setItem('rafiq_first_lesson', id)", uid); p.reload(); p.wait_for_timeout(1500)
    ok.append(("an account that has done the lesson goes straight to the questions", p.is_visible("#qs") and not p.is_visible("#first")))
    c.close()

    # a name with no Arabic spelling: shown as typed, never invented
    c, p = context(b, "localStorage.setItem('bay_name','Zebedee');")
    p.goto(BASE + "onboarding.html"); p.wait_for_timeout(1200)
    for _ in range(3):
        if p.locator(".fl-opts").count(): p.locator(".fl-opts .opt", has_text="Peace be upon you").click(); p.wait_for_timeout(200)
        p.click("#flNext"); p.wait_for_timeout(350)
    ok.append(("a name with no Arabic spelling is shown as typed", "Zebedee" in p.inner_text("#flBody") and "اسْمِي" in p.inner_text("#flBody")))
    c.close()
    b.close()

ok.append(("no page errors " + "; ".join(errors[:3]), not errors))
for name, good in ok: print(("ok  " if good else "FAIL"), name)
print("\n%d of %d passed" % (sum(g for _, g in ok), len(ok)))
sys.exit(0 if all(g for _, g in ok) else 1)
