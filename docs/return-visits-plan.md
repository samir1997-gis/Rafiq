# Return visits: the build guide

Written 16 Nov 2026 for [#372](https://github.com/samir1997-gis/Rafiq/issues/372). It turns the ten suggestions for bringing learners back into tasks a coding session can do one at a time, with the exact files, lines, wording and tests.

**Who it's for:** a coding model that has never seen this repo, and the owner who hands it the work.

## How to use it

Give the model one task per session. Paste this, with the task number filled in:

```
You're working in the Rafiq repo on the `wip` branch. Read CLAUDE.md, then docs/return-visits-plan.md.
Do Task N from that guide and nothing else. Follow its "Rules for every task" exactly.
If a line the guide quotes isn't in the file, or a test you didn't touch fails, stop and tell me instead of guessing.
When the task's tests pass, push to wip, close the task's issue with a short note, and report what you changed and the test results.
```

Do the tasks in the order below. Each one stands alone, so a later task never needs an earlier one, except where it says so.

Every code block in the seven tasks was applied to `wip` as it stood on 16 Nov 2026 and the tests named in each task passed. Nothing from that trial was committed: the tasks are still to do. If `wip` has moved on since and a quoted line no longer matches, rule 14 applies.

## The ten suggestions and where each one stands

| # | Suggestion | What to do | Issue |
|---|---|---|---|
| 1 | Don't sign returners out onto the landing page | **Task 1** | #373 |
| 2 | Put the return-visit work live sooner | Owner step A (not for a model) | #382 |
| 3 | Test sign-up on a phone from the Instagram link | Owner step B (not for a model) | #374 |
| 4 | First lesson before the account | **Task 7** (largest, last, needs a decision first) | #381 |
| 5 | Ask for the reminder after the first lesson | Mostly built already by #348. **Task 3** finishes it | #377 |
| 6 | Two emails about learning | **Task 5** (built switched off) | #379 |
| 7 | End every session on what comes back tomorrow | **Task 2** | #376 |
| 8 | One word from the salah a day | **Task 4** | #378 |
| 9 | Offer the home-screen app after lesson one | Nothing to build: see "Already built" | none |
| 10 | Ask learners what stopped them | **Task 6** (the owner sends, never the model) | #380 |

Order to build in: Task 1, 2, 3, 4, 5, 6, 7.

## Why this matters (the numbers on 14 Nov 2026)

Of 66 accounts, 25 finished a first lesson step, 8 studied on a second day and 1 studied in the last week. The landing page turns about 5% of visits into sign-ups, so the loss is after sign-up. Every task here is about getting a learner to their second day.

## Rules for every task

1. **Branch.** Work on `wip`. Never commit, push or merge to `main`, and don't open a pull request to it.
2. **The board.** Before starting, add the `in progress` label to the task's issue. When done, close it with two or three lines: what changed, the commit, the test results. A problem or idea you meet on the way gets its own new issue with a priority label (`priority: before launch`, `priority: next` or `priority: later`).
3. **One task per session.** Don't start another until this one's tests pass and it's pushed.
4. **Files you must not edit:** `path.js`, `session.html`, `drills.html`, every `*-data.js` file, `audio.js`, `audio-manifest.json`, anything under `audio/`, and the render-audio workflow. They belong to Samir. You may read them. The one exception: Task 1 changes the `auth.js?v=` number in the script tag of `drills.html` and `session.html`, and nothing else in them. If a task seems to need any other change in one, stop and say so.
5. **Secrets and privacy.** Never print or commit a key or token, and never ask anyone to paste one into chat. The repo is public: an email address is always masked in anything you print, commit or post (the tools have a `mask()` function), and a workflow input takes an account id, never an email.
6. **Nothing that touches real people.** You may run commands marked read only (`list`, `active`, `trials`, `preview`, `ask-preview`) and offline checks (`self-test`). You may not run `run`, `ask`, `thank`, `setup`, any delete or reset, or the backend deploy. Sending is the owner's.
7. **Small changes.** Every changed line must come from the task. Match the style of the file you're in (the page scripts are terse on purpose). No tidying, no renaming, no refactoring.
8. **Script versions.** Pages load scripts as `name.js?v=N`, and the service worker serves a versioned script from its cache for good. So when you change one of those scripts you must raise its `?v=` number in every page that loads it, or learners keep the old file. Each task says which. Pages themselves (`.html`) need no version.
9. **Wording learners see.** Use the wording in this guide as written. If `TYPE_SAFE_KEY` is set in the environment (`echo ${TYPE_SAFE_KEY:+set}`), score it first with a small script shaped like `tools/typesafe-exp/install_prompt.py`. If it isn't set, add a comment on the issue headed "Wording to check" with the old and new text, and carry on.
10. **Arabic.** Never type Arabic yourself. Any Arabic comes out of the data files, read by code.
11. **Tests before pushing.** Run the tests the task names, then `node tests/progress-fsrs.test.js`, `node tests/streak.test.js` and the browser smoke test. If a test you didn't touch fails, stop and report it. One is known to fail already: `tests/tutor.py` times out (#360).
12. **The code graph.** Before searching the code, run `graphify query "<your question>"`. After changing code, run `graphify update .`.
13. **Pushing.** `git pull --rebase origin wip`, run the task's tests again if anything came in, then `git push origin wip`.
14. **When to stop and ask.** Stop if: a line this guide quotes isn't in the file (the file has changed, so don't guess where the change goes); a test you didn't touch fails; the task seems to need a protected file; or a step would send an email or change live data.

## How the browser tests work

They are Python scripts that drive a real browser against a local copy of the site.

```
pkill -f "http.server 8765" 2>/dev/null
python3 .claude/skills/webapp-testing/scripts/with_server.py \
  --server "python3 -m http.server 8765 >/dev/null 2>&1" --port 8765 -- python3 tests/NAME.py
```

- The smoke test is `tests/smoke.py` with the same command. It should end with `0 problem(s)`.
- Nothing reaches the real server. Each test swaps the Supabase library for a fake: `FAKE` in `tests/startup_speed.py`, a signed-in learner called Aisha with id `u1`.
- Saved progress is faked by putting a dictionary in `localStorage` under `rafiq_progress_mirror`. `MIRROR` in `tests/startup_speed.py` is a learner who has finished the reading starter, the basics and one lesson.
- **The fake server wins.** About half a second after a page opens, the page replaces that device copy with what the fake server holds, which is `window.__rows` (a list of rows such as `{"item_id": "s:2026-11-01", "box": 0, "due": null, "seen": 1}`), or nothing. Progress the page changes itself during the test is kept. So progress that a test needs to still be there after a page has loaded goes in `window.__rows`, set on every page load.
- **Home needs a finished sign-up.** A test that opens `dashboard.html` must set `localStorage.setItem('rafiq_onboarded','u1')`, or the fake learner is sent to the sign-up questions.
- Copy the shape of `tests/first_lesson.py`: a list of `(name, passed)` pairs, printed at the end, exit code 1 if any failed, and a final check that the page threw no errors.
- Launch the browser with `pw.chromium.launch(executable_path="/opt/pw-browsers/chromium")`.
- A new test file gets one line in the "Tests: run before pushing" list in `CLAUDE.md`, written like its neighbours.

---

## Task 1: signed out after time away goes to sign-in, with a message (#373)

**The problem.** A learner in a browser who hasn't tapped for 24 hours is signed out the next time a page opens, and dropped on the landing page with no explanation. Someone who studies at 9 am and returns at 10 am the next day meets the marketing page and can think their account has gone.

**What it should do instead.**
- The limit is 30 days on someone's own device, and stays at 1 day on a device they mark as shared.
- When the limit passes they land on the sign-in page with a line saying why.
- Scrolling counts as using the app (today only taps and keys do).
- Each time it happens it's counted, with no record of who, so the owner can see how often.
- The Log out link is unchanged: it still goes to the landing page.

**Files:** `auth.js`, `login.html`, `privacy.html`, `supabase/sql/backend.sql`, `admin.html`, `tests/funnel.py`, `tests/admin_page.py`, new `tests/idle_signout.py`, `CLAUDE.md`, and the version number in every page.

### Steps

**1. `auth.js`: the limits and the activity clock.** Find:

```js
const IDLE_LIMIT_MS = 24 * 60 * 60 * 1000;   // 24 hours
const LAST_ACTIVE_KEY = 'bay_last_active';

function markActive(){
  try { localStorage.setItem(LAST_ACTIVE_KEY, String(Date.now())); } catch(_) {}
}
```

Replace with:

```js
const IDLE_LIMIT_MS = 30 * 24 * 60 * 60 * 1000;        // 30 days on someone's own device (#373)
const IDLE_LIMIT_SHARED_MS = 24 * 60 * 60 * 1000;      // 24 hours when they ticked "shared device" on the sign-in page
const SHARED_KEY = 'rafiq_shared';
const LAST_ACTIVE_KEY = 'bay_last_active';

let _lastMark = 0;
function markActive(){
  const now = Date.now();
  if (now - _lastMark < 60000) return;                 // one write a minute is plenty (scrolling fires many events)
  _lastMark = now;
  try { localStorage.setItem(LAST_ACTIVE_KEY, String(now)); } catch(_) {}
}
```

**2. `auth.js`: which limit applies.** In `idleExpired()`, find:

```js
    return (Date.now() - last) > IDLE_LIMIT_MS;
```

Replace with:

```js
    const shared = localStorage.getItem(SHARED_KEY) === '1';
    return (Date.now() - last) > (shared ? IDLE_LIMIT_SHARED_MS : IDLE_LIMIT_MS);
```

**3. `auth.js`: where an expired session goes.** In `requireLogin()`, find:

```js
    if (idleExpired()) {
      await logout();
      return null;
    }
```

Replace with:

```js
    if (idleExpired()) {
      // away too long: sign out on this device only, and say why on the sign-in page (#373)
      try { await sb.auth.signOut({ scope: 'local' }); } catch(_) {}
      try { localStorage.removeItem(LAST_ACTIVE_KEY); } catch(_) {}
      window.location.href = 'login.html?away=1';
      return null;
    }
```

Do not change `logout()` or `logoutEverywhere()`.

**4. `auth.js`: scrolling counts.** Find `['click','keydown','touchstart'].forEach(evt=>{` and add `'scroll'` to the list: `['click','keydown','touchstart','scroll']`.

**5. `auth.js`: the comment.** The comment block headed `Idle auto-logout (shared-computer safety)` says the old behaviour. Change its text to say: 30 days on a personal device, 24 hours on one marked shared, and that the person is sent to the sign-in page with a message.

**6. Raise the version in every page.** 19 pages load `auth.js?v=11`.

```
grep -l 'auth.js?v=11' *.html | xargs sed -i 's/auth\.js?v=11/auth.js?v=12/'
grep -c 'auth.js?v=11' *.html | grep -v ':0$'      # must print nothing
grep -c 'auth.js?v=12' *.html | grep -v ':0$' | wc -l   # must print 19
```

**7. `login.html`: the message and the count.** Find these two lines, near the comment `// If already logged in`:

```js
  else if (new URLSearchParams(location.search).get('again')) showMsg('Rafiq has had a big update. Please sign in again to start fresh.', 'ok');
})();
```

Add one line between them:

```js
  else if (new URLSearchParams(location.search).get('away')) { showMsg('You were signed out after a while away. Sign in to carry on: your progress is saved.', 'ok'); tap('idle_signout'); }
```

**8. `login.html`: the shared-device tick box.** Find the line that starts `<div class="toggle" id="toggle">`. Directly after that line add:

```html
    <label class="note" style="display:block;cursor:pointer"><input type="checkbox" id="shared"> Shared device? Sign me out after a day away</label>
```

In the page's script, directly above the comment `// If already logged in`, add:

```js
// "Shared device" (#373): ticked, this browser signs out after a day away (auth.js reads rafiq_shared); otherwise after 30 days
(() => { const c = document.getElementById('shared'); if (!c) return;
  try { c.checked = localStorage.getItem('rafiq_shared') === '1'; } catch(_) {}
  c.onchange = () => { try { c.checked ? localStorage.setItem('rafiq_shared', '1') : localStorage.removeItem('rafiq_shared'); } catch(_) {} };
})();
```

**9. `privacy.html`: keep the policy true.** Find `signing you out after 24 hours without use, for safety on shared devices` and replace with `signing you out after 30 days without use, or after one day on a device you mark as shared`. Put the old and new sentence on the issue under "Wording to check": a change to the privacy page needs the owner to see it.

**10. `supabase/sql/backend.sql`: let the new step be counted.** Find:

```sql
  insert into private.taps (day, step, n) select current_date, tap.step, 1 where tap.step in ('signup_page', 'create', 'google')
```

Change the list to `('signup_page', 'create', 'google', 'idle_signout')`. In the comment above it, add that `idle_signout` counts people signed out after time away. Do not deploy: this file reaches the database when the owner updates `main`.

**11. `admin.html`: show the count.** Find `<div class="list" id="steps"></div>` and add directly after it, inside the same card: `<p class="note" id="away"></p>`. In the function `steps(w, taps, joined)`, add as its last line:

```js
  $('away').textContent = `Signed out after time away and sent to sign-in: ${t.idle_signout || 0}`;
```

**12. `tests/funnel.py`.** In the line that calls `public.tap` several times, add `select public.tap('idle_signout');` before `select public.tap('anything')`. In the check that expects `{"signup_page": "2", "create": "1"}`, expect `{"signup_page": "2", "create": "1", "idle_signout": "1"}`.

**13. `tests/admin_page.py`.** Add `{"step": "idle_signout", "n": 2}` to the `taps` list in `STATS`, and add one check that the text of `#away` ends with `: 2`. Leave the existing check on `#steps` alone.

**14. New file `tests/idle_signout.py`:**

```python
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
```

**15. `CLAUDE.md`.** Add to the tests list: `- Signed out after time away (30 days, a day on a shared device; sent to sign-in with a message; Log out unchanged): `... -- python3 tests/idle_signout.py` (same server command as the smoke test).`

### Tests to run
`tests/idle_signout.py`, `tests/login_page.py`, `tests/admin_page.py`, `tests/startup_speed.py`, `python3 tests/funnel.py`, then rule 11's three.

### Done when
All of those pass, the three `grep` lines in step 6 give the results shown, and the issue has the "Wording to check" comment for the privacy sentence and the two new lines of sign-in wording.

### Not in this task
Don't change the phone app's behaviour, the Log out link, "Sign out of every device" in Settings, or the `SIGN_IN_AGAIN_BEFORE` date.

---

## Task 2: the end of a lesson says what comes back tomorrow (#376)

**The problem.** The reason to return tomorrow is that words come back for review. The end-of-lesson screen only says so after a miss.

**What it should do.** Every finished step shows one line with how many words and sentences are due by tomorrow. No line when the number is zero.

**Files:** `learn.html`, new `tests/tomorrow_note.py`, `CLAUDE.md`. `learn.html` is a page, so no version number changes.

### Steps

**1. `learn.html`: count what's due by tomorrow.** Find the line `function finish(p, step, note, extra){`. Directly above it add:

```js
/* How many words and sentences are due by tomorrow (#376): what the learner comes back to. */
function dueTomorrow(){
  const d=new Date(); d.setDate(d.getDate()+1); const t=d.toISOString().slice(0,10);   // the way progress.js works out a due date
  return Progress.ids().filter(id=>{ if(!/^(v|d):/.test(id)) return false; const r=Progress.get(id); return r && r.box>0 && r.due && r.due<=t; }).length;
}
```

**2. `learn.html`: work it out inside `finish`.** Inside `finish`, find:

```js
  const hit = sg.reached && today===RafiqPath.GOAL;
```

Add directly under it:

```js
  const back=dueTomorrow();
```

**3. `learn.html`: show it.** Still inside `finish`, find the line:

```js
    ${note||''}${wordsNote(step)}
```

Replace with:

```js
    ${note||''}${wordsNote(step)}${back?`<div class="wnote" id="tmrw">📅 Tomorrow: <b>${back}</b> ${back===1?'word or sentence comes':'words and sentences come'} back for a quick review.</div>`:''}
```

That's the whole change. It has been tried in a browser and shows, for two words due: "📅 Tomorrow: 2 words and sentences come back for a quick review."

**4. New file `tests/tomorrow_note.py`:**

```python
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
```

**5. `CLAUDE.md`.** Add to the tests list: `- The end of a lesson says what comes back tomorrow: `... -- python3 tests/tomorrow_note.py` (same server command as the smoke test).`

### Tests to run
`tests/tomorrow_note.py`, `tests/lesson_layout.py`, `tests/unit_reviews.py`, `tests/unit_games.py`, then rule 11's three.

### Not in this task
Don't touch `wordsNote`, `doneButtons`, the streak line, or `progress.js`.

---

## Task 3: the reminder ask (#377)

**Where it stands.** The faster start (#348) already asks for a reminder time straight after the first lesson, with "No reminders" as the last choice. Don't rebuild that. Two gaps are left:

- **A.** The question's wording doesn't connect the reminder to the words just learnt.
- **B.** A learner who skipped the question is never asked again unless they use the home-screen app. The prompt on Home (`RafiqReminders.prompt` in `reminders.js`) returns at once in a browser.

**Files:** `onboarding.html`, `reminders.js`, `dashboard.html`, `settings.html` (version number only), `tests/first_lesson.py`, new `tests/reminder_prompt.py`, `CLAUDE.md`.

### Part A: wording

In `onboarding.html` find:

```html
      <h2>When should we remind you? <span style="font-weight:400;color:var(--ink-soft)">(optional)</span></h2>
```

Replace the heading text so the line reads:

```html
      <h2>When shall we bring your words back? <span style="font-weight:400;color:var(--ink-soft)">(optional)</span></h2>
```

A few lines below, find:

```html
      <p class="qnote">By email, only on days you haven’t done your lesson.</p>
```

Replace with:

```html
      <p class="qnote">We’ll email you at that time, only on days you haven’t studied. One tap stops it.</p>
```

Do not preselect a time. The learner must choose one themselves: that choice is their consent to the emails.

If `tests/first_lesson.py` checks the old heading text, update that check to the new text.

### Part B: the Home prompt for browser learners

**1. `reminders.js`.** In `async function prompt(el)`, find its first line:

```js
    if(!el || !standalone() || !sb) return;
```

Replace with:

```js
    if(!el || !sb) return;
    const inApp = standalone();
```

**2.** A few lines below, find:

```js
    const row = await load();
```

Add directly under it:

```js
    if(!inApp){
      // in a browser (#377): only someone with no reminder who has come back on a second day; "No reminders" stays a no
      if(row && (row.enabled || row.by_email === false)) return;
      try{ await Progress.init(); }catch(_){}
      if(!window.Progress || Progress.ids('s:').length < 2) return;
    }
```

**3.** Further down, find:

```js
        try{ const r = await enable(+b.dataset.h); thanks(+b.dataset.h, r.push); }
```

Replace with:

```js
        try{ const h = +b.dataset.h;
             // in a browser the reminder is an email: no notification permission is asked for
             const r = inApp ? await enable(h) : (await save({ hour: h, goal: goal(), by_email: true, enabled: true }), { push: false });
             thanks(h, r.push); }
```

**4.** Update the comment above `prompt` (it starts `Home, opened from the home-screen icon`) to add: in a browser, a learner with no reminder is asked once, from their second study day.

**5. Version.** `reminders.js?v=2` becomes `reminders.js?v=3` in `dashboard.html`, `onboarding.html` and `settings.html`:

```
sed -i 's/reminders\.js?v=2/reminders.js?v=3/' dashboard.html onboarding.html settings.html
grep -c 'reminders.js?v=3' dashboard.html onboarding.html settings.html    # each must say 1
```

**6. New file `tests/reminder_prompt.py`:**

```python
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
```

**7. `CLAUDE.md`.** Add a line for the new test.

### Tests to run
`tests/reminder_prompt.py`, `tests/first_lesson.py`, `tests/app_reminders.py`, `tests/startup_speed.py`, then rule 11's three.

### Wording to check
Post the two new lines from Part A on the issue.

---

## Task 4: one word from the salah in the daily reminder (#378)

**The idea.** A learner already has five fixed moments in the day. The daily reminder carries one word from the prayer, its meaning and where it's said. It's a trial: it only reaches people who already get reminders.

**How.** The reminder is written by `tools/send-reminders.js` (run every hour by the Reminders workflow). The words are read from `salah-data.js`, from the prayer's own phrases only. Lines with a `ref` are Qur'an and are left out. Everyone gets the same word on the same day.

**Files:** `tools/send-reminders.js`, `supabase/email-templates/daily-reminder.html`. You only read `salah-data.js`.

### Steps

**1. `tools/send-reminders.js`: the word list.** Directly above the comment `/* ---------- sending ---------- */` add:

```js
/* ---------- today's word from the salah (#378) ---------- */
const vm = require('vm');
// every word of the prayer's own phrases, once each, in the order they're said. Lines with a ref are Qur'an: left out.
function salahWords(file = path.join(__dirname, '..', 'salah-data.js')) {
  const S = vm.runInNewContext(fs.readFileSync(file, 'utf8') + '; SALAH');
  const seen = new Set(), list = [];
  for (const p of S.parts) for (const l of p.lines) {
    if (l.ref || /^fatiha/.test(p.id)) continue;
    for (const w of l.words) { if (!w.root || seen.has(w.ar)) continue; seen.add(w.ar); list.push({ ar: w.ar, en: w.en, where: p.title }); }
  }
  return list;
}
// the same word for everyone on a given day
const wordOfDay = (list, day) => list.length ? list[Math.floor(Date.parse(day + 'T00:00:00Z') / 864e5) % list.length] : null;
let WORDS = [];
try { WORDS = salahWords(); } catch (e) { console.log(`no salah word today: ${e.message}`); }   // never let this stop a reminder
```

This has been run against today's `salah-data.js`: it gives 49 words. For `2026-11-16` the word's meaning is "Glorious" and its place is "Blessings on the Prophet".

**2. Put the word in the message.** In `function message(row, today)`, find its last line:

```js
  return { title, line, reviews, streak: s, due };
```

Replace with:

```js
  return { title, line, reviews, streak: s, due, word: wordOfDay(WORDS, today) };
```

**3. Put it in the email.** In `function render(row, m)`, find:

```js
    .replace('{{LINE}}', esc(m.line)).replace('{{REVIEWS}}', m.reviews ? `<p style="margin:0 0 20px">${esc(m.reviews)}</p>` : '')
```

Replace with:

```js
    .replace('{{LINE}}', esc(m.line)).replace('{{REVIEWS}}', m.reviews ? `<p style="margin:0 0 20px">${esc(m.reviews)}</p>` : '')
    .replace('{{WORD}}', m.word ? `<p style="margin:0 0 20px">Today’s word from your salah: <b dir="rtl" lang="ar" style="font-size:20px">${esc(m.word.ar)}</b> means “${esc(m.word.en)}”. You say it in: ${esc(m.word.where)}.</p>` : '')
```

**4. The template.** In `supabase/email-templates/daily-reminder.html` find the line that is only `{{REVIEWS}}` and add a new line under it, with the same indent: `{{WORD}}`.

**5. Put it in the notification.** In `async function push(row, m)`, find:

```js
body: m.reviews ? `${m.line} ${m.reviews}` : m.line
```

Replace with:

```js
body: [m.line, m.reviews, m.word && `Today's salah word: ${m.word.ar} means "${m.word.en}".`].filter(Boolean).join(' ')
```

**6. The offline check.** In `function selfTest()`, before `console.log('self-test passed');`, add:

```js
  // today's word from the salah (#378): from the prayer's own phrases, the same for everyone on a day, never Qur'an
  const words = salahWords();
  assert.ok(words.length >= 30);
  assert.ok(words.every(w => w.ar && w.en && w.where && !/^Al-Fatiha/.test(w.where)));
  assert.deepStrictEqual(wordOfDay(words, '2026-11-16'), wordOfDay(words, '2026-11-16'));
  assert.notDeepStrictEqual(wordOfDay(words, '2026-11-16'), wordOfDay(words, '2026-11-17'));
  assert.strictEqual(wordOfDay([], '2026-11-16'), null);
  const mail = render({ name: 'Aisha', unsub: 'x' }, message({ days: [], due: 0 }, '2026-11-16'));
  assert.ok(mail.html.includes('Today’s word from your salah') && !mail.html.includes('{{'));
```

**7.** Add `salahWords` and `wordOfDay` to the `module.exports` line.

### Tests to run
`node tools/send-reminders.js self-test` must print `self-test passed`. Then rule 11's three.

### Not in this task
Don't change who gets a reminder, when, or the reminders the phone app schedules for itself (`reminders.js`). Don't run `preview`, `run` or `setup` for this task.

---

## Task 5: two study emails, built switched off (#379)

**The problem.** After the welcome email, the only emails Rafiq sends are three about the free week ending. Someone who never started, or did one lesson and drifted, hears nothing about learning.

**What to build.** Two short emails, each sent at most once per account:

| Kind | Who | When |
|---|---|---|
| `start` | Confirmed their email, never finished a lesson | 24 to 96 hours after confirming |
| `review` | Studied on 1 or 2 days, has no daily reminder | 2 to 4 days after they last studied |

Nobody gets one who: is on the Rafiq team, has unsubscribed, chose "No reminders", turned reminders off in Settings, or already has a daily reminder.

**It ships switched off.** `run` sends none until the owner changes one constant. `preview` always lists who would get one. Never switch it on yourself.

**Files:** `tools/send-reminders.js`, new `supabase/email-templates/study-nudge.html`, `onboarding.html`.

### Steps

**1. New template.** Copy `supabase/email-templates/daily-reminder.html` to `supabase/email-templates/study-nudge.html`. In the copy:
- change the first comment line to say it's the study email sent by `tools/send-reminders.js`, two kinds, `start` and `review`
- delete the `{{REVIEWS}}` line (and `{{WORD}}` if Task 4 added it)
- change the button's link from `https://rafiq-arabic.com/dashboard.html` to `https://rafiq-arabic.com/login.html` (the sign-in page sends a signed-in learner to the right place)
- change the button's label `Continue` to `{{BUTTON}}`
- replace the footer sentence with: `You’re getting this because you created a Rafiq account. <a href="{{UNSUB}}" style="color:#5C6B6E">Stop these emails</a>.`

**2. `tools/send-reminders.js`: two new columns.** In the `SETUP` text, directly after the line `using (auth.uid() = user_id) with check (auth.uid() = user_id);` add:

```sql
-- the study emails (#379): when each was sent, so each goes once per account
alter table public.reminders add column if not exists nudge_start_at timestamptz;
alter table public.reminders add column if not exists nudge_review_at timestamptz;
```

**3. The rules and the sender.** Directly above the line `if (require.main === module) (async () => {` add:

```js
/* ---------- study emails (#379): two short emails about learning, each once per account ---------- */
const NUDGES_ON = false;        // the owner switches this on (#379). Until then 'run' sends none; 'preview' still lists them
const NUDGE_HOURS = [17, 18];   // the UTC hours they go out in (two, so a late run still sends)
const NUDGES = {
  start:  { subject: 'Your first Arabic lesson takes two minutes', button: 'Start my first lesson',
            line: 'Your account is ready and your first lesson is waiting. In two minutes you’ll greet someone and say your name in Arabic.' },
  review: { subject: 'Your first words are ready to review', button: 'Review my words',
            line: 'The words you learnt are due for their first review. It takes about two minutes, and it’s what makes them stay.' } };
const NUDGE_QUERY = `
  select u.id as user_id, u.email, u.raw_user_meta_data->>'name' as name, u.email_confirmed_at as confirmed_at,
         (r.user_id is not null) as has_row, r.enabled, r.by_email, r.nudge_start_at, r.nudge_review_at,
         (select count(*) from public.item_progress p where p.user_id = u.id and p.item_id like 's:%')::int as study_days,
         (select max(substr(p.item_id, 3)) from public.item_progress p where p.user_id = u.id and p.item_id like 's:%') as last_day
  from auth.users u left join public.reminders r on r.user_id = u.id
  where u.email_confirmed_at > now() - interval '10 days' and coalesce(u.raw_app_meta_data->>'admin', '') <> 'true'`;
/* 'start' | 'review' | null for one row of NUDGE_QUERY */
function nudgeKind(row, now = new Date()) {
  if (row.by_email === false) return null;                                        // unsubscribed, or said "No reminders"
  if (row.enabled) return null;                                                   // daily reminders already reach them
  if (row.has_row && !row.nudge_start_at && !row.nudge_review_at) return null;    // turned reminders off themselves
  const hours = (now - new Date(row.confirmed_at)) / 3600e3;
  if (!row.study_days) return !row.nudge_start_at && hours >= 24 && hours < 96 ? 'start' : null;
  const since = Math.round((Date.parse(utcDay(now) + 'T00:00:00Z') - Date.parse(row.last_day + 'T00:00:00Z')) / 864e5);
  return !row.nudge_review_at && row.study_days <= 2 && since >= 2 && since <= 4 ? 'review' : null;
}
const NUDGE_TEMPLATE = fs.readFileSync(path.join(__dirname, '..', 'supabase/email-templates/study-nudge.html'), 'utf8')
  .replace(/^<!--[\s\S]*?-->\s*/, '');
function renderNudge(row, kind, token) {
  const name = (row.name || '').trim().split(/\s+/)[0], unsub = `${SITE}/unsubscribe.html?t=${token}`;
  const html = NUDGE_TEMPLATE.replace('{{GREETING}}', esc(name ? `Assalamu alaykum ${name},` : 'Assalamu alaykum,'))
    .replace('{{LINE}}', esc(NUDGES[kind].line)).replace('{{BUTTON}}', esc(NUDGES[kind].button)).replace(/\{\{UNSUB\}\}/g, unsub);
  return { html, unsub };
}
async function nudges(cmd, now = new Date()) {
  if (cmd === 'run' && (!NUDGES_ON || !NUDGE_HOURS.includes(now.getUTCHours()))) return;
  let n = 0;
  for (const row of await sql(NUDGE_QUERY)) {
    const kind = nudgeKind(row, now); if (!kind) continue;
    const who = `${row.user_id}  ${mask(row.email)}`;
    if (cmd === 'preview') { console.log(`would send the '${kind}' study email  ${who}`); n++; continue; }
    // mark first, so a retry can never send it twice; the same statement gives the unsubscribe token
    const col = kind === 'start' ? 'nudge_start_at' : 'nudge_review_at';
    const [r] = await sql(`insert into public.reminders (user_id, ${col}) values (${q(row.user_id)}, now())
                           on conflict (user_id) do update set ${col} = now() returning unsub`);
    const { html, unsub } = renderNudge(row, kind, r.unsub);
    const res = await fetch('https://api.resend.com/emails', { method: 'POST',
      headers: { Authorization: `Bearer ${KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ from: FROM, to: [row.email], reply_to: REPLY_TO, subject: NUDGES[kind].subject, html, text: text(html),
        headers: { 'List-Unsubscribe': `<${unsub}>` } }) });
    console.log(`${who}  '${kind}' study email ${res.ok ? 'sent' : 'FAILED ' + res.status}`); if (res.ok) n++;
    await new Promise(r => setTimeout(r, 600));   // Resend: 2 a second
  }
  console.log(`study emails: ${n} ${cmd === 'preview' ? `would go${NUDGES_ON ? '' : ' (switched off: none are sent)'}` : 'sent'}`);
}
```

The query and the rules have been run on a test database and pass the checks in step 5.

**4. Call it, safely.** Near the end of the file find:

```js
  if (failed) process.exit(1);
})().catch(e => { console.error(e.message); process.exit(1); });
```

Add one line above `if (failed) process.exit(1);`:

```js
  try { await nudges(cmd, now); } catch (e) { console.log(`study emails skipped: ${e.message}`); }   // never let these stop the reminders
```

The `try` matters. Until the owner has run `setup`, the two new columns don't exist and the query fails. That must only print a line, never stop the daily reminders.

**5. The offline check.** In `selfTest()`, before `console.log('self-test passed');`, add:

```js
  // the study emails (#379): who gets which, and who gets none
  const at2 = at('2026-11-16T17:10:00Z');
  const fresh = { confirmed_at: '2026-11-15T10:00:00Z', study_days: 0, last_day: null, has_row: false, enabled: null, by_email: null, nudge_start_at: null, nudge_review_at: null };
  assert.strictEqual(nudgeKind(fresh, at2), 'start');                                                          // confirmed 31 hours ago, never studied
  assert.strictEqual(nudgeKind({ ...fresh, confirmed_at: '2026-11-16T09:00:00Z' }, at2), null);                // too soon
  assert.strictEqual(nudgeKind({ ...fresh, confirmed_at: '2026-11-10T09:00:00Z' }, at2), null);                // too late
  assert.strictEqual(nudgeKind({ ...fresh, has_row: true, nudge_start_at: '2026-11-15T17:00:00Z' }, at2), null);   // sent already
  assert.strictEqual(nudgeKind({ ...fresh, has_row: true, by_email: false }, at2), null);                      // unsubscribed, or "No reminders"
  assert.strictEqual(nudgeKind({ ...fresh, has_row: true, enabled: false, by_email: true }, at2), null);       // turned reminders off in Settings
  assert.strictEqual(nudgeKind({ ...fresh, has_row: true, enabled: true, by_email: true }, at2), null);        // has a daily reminder
  const once = { ...fresh, confirmed_at: '2026-11-13T10:00:00Z', study_days: 1, last_day: '2026-11-14' };
  assert.strictEqual(nudgeKind(once, at2), 'review');                                                          // studied once, two days ago
  assert.strictEqual(nudgeKind({ ...once, last_day: '2026-11-15' }, at2), null);                               // only yesterday
  assert.strictEqual(nudgeKind({ ...once, last_day: '2026-11-11' }, at2), null);                               // five days ago: too late
  assert.strictEqual(nudgeKind({ ...once, study_days: 3 }, at2), null);                                        // a regular by now
  assert.strictEqual(nudgeKind({ ...once, has_row: true, nudge_start_at: '2026-11-14T17:00:00Z' }, at2), 'review');   // had 'start', then studied
  const nm = renderNudge({ name: 'Aisha K' }, 'start', 'tok');
  assert.ok(nm.html.includes('Assalamu alaykum Aisha,') && nm.html.includes('Start my first lesson') && nm.html.includes('unsubscribe.html?t=tok') && !nm.html.includes('{{'));
  assert.strictEqual(NUDGES_ON, false);                                                                        // ships switched off
```

**6.** Add `nudgeKind`, `renderNudge` and `NUDGES_ON` to the `module.exports` line. Update the comment at the top of the file to mention the two study emails and that `preview` lists them.

**7. `onboarding.html`: remember "No reminders".** Today that answer saves nothing, so the study emails couldn't tell it from "skipped". In `async function save()`, find:

```js
  try{ if(answers.remind && answers.remind !== 'none' && window.RafiqReminders)
         await RafiqReminders.save({ hour:+answers.remind, goal:2, by_email:true, enabled:true }); }catch(_){}
```

Replace with:

```js
  try{ if(answers.remind && answers.remind !== 'none' && window.RafiqReminders)
         await RafiqReminders.save({ hour:+answers.remind, goal:2, by_email:true, enabled:true });
       // "No reminders" is an answer too: kept, so the study emails (#379) leave this person alone
       else if(answers.remind === 'none' && window.RafiqReminders) await RafiqReminders.save({ enabled:false, by_email:false }); }catch(_){}
```

In `tests/first_lesson.py`, add a check for it at the end, as a new learner of its own (before `b.close()`):

```python
    # "No reminders" is kept as an answer (#379), so the study emails leave this person alone
    c, p = context(b, "localStorage.setItem('bay_name','Samir'); localStorage.setItem('rafiq_first_lesson','u1');")
    p.goto(BASE + "onboarding.html"); p.wait_for_timeout(1500)
    # what gets saved is noted in sessionStorage, which is still there after the page moves on to Home
    p.evaluate("RafiqReminders.save = async x => { sessionStorage.setItem('saved', JSON.stringify(x)); }")
    p.click('.q[data-key="remind"] .opt[data-val="none"]')
    p.click("#doneBtn"); p.wait_for_timeout(2500)
    saved = json.loads(p.evaluate("sessionStorage.getItem('saved')") or "null")
    ok.append(('"No reminders" is saved as an answer: ' + str(saved), saved == {"enabled": False, "by_email": False}))
    c.close()
```

### Tests to run
`node tools/send-reminders.js self-test`, `tests/first_lesson.py`, then rule 11's three.

### Done when
The self-test passes with `NUDGES_ON` still `false`, and the issue has a "Wording to check" comment with both subjects, both lines, both button labels and the footer sentence.

### Not in this task
Don't set `NUDGES_ON` to `true`. Don't run `setup`, `run` or `preview`. Don't change the welcome or free-week emails (`supabase/functions/`).

---

## Task 6: "what stopped you?", a founder email the owner sends (#380)

**The idea.** With this few learners, five replies teach more than a dashboard. A short personal email goes once to everyone who studied and then stopped.

**What to build.** Two commands in the users tool, copied from the shape of `thank-preview` and `thank` in the same file:
- `ask-preview` (read only): lists who would be asked, emails masked.
- `ask` with the second input `SEND-ASK`: sends, and records it so nobody is asked twice.

**You never run `ask`.** You run `ask-preview` once at the end, through the workflow, to show it works.

**Files:** `tools/supabase-users.js`, `.github/workflows/supabase-users.yml`, `supabase/sql/backend.sql`.

### Steps

**1. `supabase/sql/backend.sql`.** Find the line `alter table public.billing add column if not exists refunded_at timestamptz;` and add under it:

```sql
-- "what stopped you?" (#380): when this account was asked, so it's asked once
alter table public.billing add column if not exists asked_at timestamptz;
```

**2. `tools/supabase-users.js`.** Find the line `if (cmd === 'attempts') {`. Directly above it add:

```js
  if (cmd === 'ask-preview' || cmd === 'ask') {
    // "what stopped you?" (#380): a short personal email, once per account, to people who studied and then stopped
    // (last studied 7 or more days ago, not on a plan). 'ask-preview' only lists them; 'ask' sends and marks billing.asked_at.
    if (cmd === 'ask' && arg !== 'SEND-ASK') { console.error('type SEND-ASK to send'); process.exit(1); }
    const has = (await sql(`select exists(select 1 from information_schema.columns
                            where table_schema = 'public' and table_name = 'billing' and column_name = 'asked_at') as x`))[0].x;
    if (cmd === 'ask' && !has) await sql('alter table public.billing add column if not exists asked_at timestamptz');
    const people = await sql(`select u.id, u.email, coalesce(u.raw_user_meta_data->>'full_name', u.raw_user_meta_data->>'name', '') as name,
                                count(*)::int as days, max(substr(p.item_id, 3)) as last
                              from auth.users u join public.item_progress p on p.user_id = u.id and p.item_id like 's:%'
                                left join public.billing b on b.user_id = u.id
                              where u.email_confirmed_at is not null and coalesce(u.raw_app_meta_data->>'admin', '') <> 'true'
                                and coalesce(b.status, '') not in ('active', 'trialing', 'past_due') ${has || cmd === 'ask' ? 'and b.asked_at is null' : ''}
                              group by u.id, u.email, name
                              having max(substr(p.item_id, 3)) <= to_char(current_date - 7, 'YYYY-MM-DD') order by days desc, last desc`);
    console.log(`${people.length} learner(s) who studied and then stopped (last studied 7+ days ago, not asked before):`);
    for (const u of people) {
      const first = (u.name.trim().split(/\s+/)[0] || '').replace(/[<>&"]/g, '');
      console.log(`  ${mask(u.email)}  studied on ${u.days} day(s), last ${u.last}`);
      if (cmd !== 'ask') continue;
      if (!process.env.RESEND_API_KEY) { console.error('RESEND_API_KEY is not set'); process.exit(1); }
      await sql(`update public.billing set asked_at = now() where user_id = '${u.id}'`);   // mark first: never asked twice
      const paras = [u.days > 1 ? `I'm Samir, and I made Rafiq. You came back to it a few times and then stopped, and I'd really like to know why.`
                                : `I'm Samir, and I made Rafiq. You tried a lesson and didn't come back, and I'd really like to know why.`,
        `Could you hit reply with one line? What got in the way, or what you hoped to find and didn't. I read every reply myself, and it decides what we fix next.`];
      const hi = first ? `Hi ${first},` : 'Hi there,';
      const text = [hi, ...paras, 'Thank you,\nSamir'].join('\n\n');
      const html = `<div style="font-family:Georgia,serif;font-size:16px;line-height:1.6;color:#17262B;max-width:560px">` +
        [hi, ...paras].map(t => `<p>${t}</p>`).join('') + `<p>Thank you,<br>Samir</p></div>`;
      const r = await fetch('https://api.resend.com/emails', { method: 'POST',
        headers: { Authorization: `Bearer ${process.env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ from: 'Samir from Rafiq <hello@contact.rafiq-arabic.com>', to: [u.email], reply_to: 'support@rafiq-arabic.com',
                               subject: 'A quick question about Rafiq', html, text }) });
      console.log(`    email ${r.ok ? 'sent' : 'FAILED ' + r.status + ' ' + (await r.text()).slice(0, 200)}`);
      await new Promise(r => setTimeout(r, 600));
    }
    return;
  }
```

The two queries have been run on a test database.

**3. `.github/workflows/supabase-users.yml`.** In the `command` description, add `ask-preview (read only) | ask` after `thank`. In the `arg` description, add `ask: type SEND-ASK` after `thank: type SEND-THANKS`. Change nothing else in the file.

**4. Check it.** `node --check tools/supabase-users.js` must print nothing. Push, then run the "Supabase users" workflow on `wip` with command `ask-preview` and an empty second input. Paste its output (emails are already masked) into the issue.

### Done when
`ask-preview` runs on `wip` and lists people without error, and the issue has a "Wording to check" comment with the subject, both opening lines, the ask and the sign-off, plus the question "Who signs it: Samir, as in the thank-you email, or Saleh?"

### Not in this task
Never run `ask`. Don't change `thank`.

---

## Task 7: the first lesson before the account (#381)

**Do not start until the owner has answered the question in step 0.** This is the largest task: read all of it before changing anything.

**The problem.** To reach the first lesson a visitor must create an account and, for an email sign-up, leave to confirm it. 5 of the last 20 sign-ups never confirmed. The confirm link can open in a different browser from the one they signed up in (Instagram's built-in browser is the usual cause).

**What to build.** A visitor can do the two-minute first lesson as a guest. At the end they're asked to create an account to keep it. After sign-up the lesson counts, without doing it again, and they go straight to the two questions.

**How it works today (on `wip`).** `onboarding.html` runs for a signed-in new account: the first lesson (`firstLesson()`), then a "Well done" card (`#well`), then two questions (`#qs`), then Home. `finishLesson()` saves two words and marks today as studied.

**Files:** `onboarding.html`, `taster.js`, `index.html`, new `tests/guest_lesson.py`, `tests/taster.py`, `CLAUDE.md`.

### Step 0: the decision (ask on the issue, then wait)

> Where should the way in to the guest lesson go? **A:** a second link on the end card of the landing page's four-word taster, under the "Start your free week" button (the safe choice, built below). **B:** the main "Start your free week" buttons themselves. The landing page is being simplified in #210, so this needs Samir's agreement too.

Build A unless told B. If the answer is B, stop and ask for instructions: this guide doesn't cover it.

### Steps

**1. `onboarding.html`: allow a guest.** Find the line that is exactly `requireLogin();` (it's the first line of the page's main script). Replace with:

```js
/* A guest (#381): ?guest=1 with nobody signed in runs the first lesson without an account. Nothing is saved until they
   create one; rafiq_guest_lesson then tells this page, after sign-up, that the lesson is done. */
const GUEST = new URLSearchParams(location.search).get('guest') === '1';
const GUEST_KEY = 'rafiq_guest_lesson';
if(!GUEST) requireLogin();
```

**2. Split the saving out of `finishLesson`.** Find, at the top of `function finishLesson(nm, nameAr){`, these three lines:

```js
  // the two words go into their reviews, and the lesson counts as today's first step
  try{ ['v:1','v:784'].forEach(id=>{ if(Progress.isNew(id)){ Progress.grade(id,'good',1); RafiqPath.wordMet(); } }); RafiqPath.markDay(); Progress.flush&&Progress.flush(); }catch(_){}
  try{ const ids=(localStorage.getItem('rafiq_first_lesson')||'').split(','); localStorage.setItem('rafiq_first_lesson', ids.concat(UID||'1').slice(-5).join(',')); }catch(_){}
```

Replace them with one line:

```js
  if(GUEST){ try{ localStorage.setItem(GUEST_KEY, '1'); }catch(_){} } else saveFirstLesson();
```

Directly above `function finishLesson(nm, nameAr){` add the function, with the three lines moved into it unchanged:

```js
function saveFirstLesson(){
  // the two words go into their reviews, and the lesson counts as today's first step
  try{ ['v:1','v:784'].forEach(id=>{ if(Progress.isNew(id)){ Progress.grade(id,'good',1); RafiqPath.wordMet(); } }); RafiqPath.markDay(); Progress.flush&&Progress.flush(); }catch(_){}
  try{ const ids=(localStorage.getItem('rafiq_first_lesson')||'').split(','); localStorage.setItem('rafiq_first_lesson', ids.concat(UID||'1').slice(-5).join(',')); }catch(_){}
}
```

**3. The guest's "Well done" card.** At the end of `finishLesson`, find:

```js
  document.getElementById('wellGo').onclick=()=>show('qs');
```

Replace with:

```js
  if(GUEST){
    document.querySelector('#well .fl-note').innerHTML='You’ve learnt <b>2 words</b>. Create your free account to keep them: we’ll bring them back so they stick.';
    const go=document.getElementById('wellGo'); go.textContent='Create my free account';
    go.onclick=()=>{ location.href='login.html?mode=signup'; };
  } else document.getElementById('wellGo').onclick=()=>show('qs');
```

**4. The start of the page.** Find the block that begins `/* Start: the lesson, unless this account has done it already (then the questions). */` and ends with `})();`. Replace the whole block with:

```js
/* Start: the lesson, unless this account has done it already (then the questions). A guest gets the lesson; someone who
   did it as a guest and has now signed up (#381) gets it saved, and goes to the questions. */
(async()=>{
  await uidReady;
  if(GUEST && UID){ location.replace('onboarding.html'); return; }      // already signed in: the ordinary start
  try{ await Progress.init(); }catch(_){}
  if(GUEST) return firstLesson();
  let guestDone=false; try{ guestDone=localStorage.getItem(GUEST_KEY)==='1'; }catch(_){}
  if(guestDone){ saveFirstLesson(); try{ localStorage.removeItem(GUEST_KEY); }catch(_){} return show('qs'); }
  let done=false; try{ done=(localStorage.getItem('rafiq_first_lesson')||'').split(',').includes(UID||'1'); }catch(_){}
  if(done) show('qs'); else firstLesson();
})();
```

**5. `taster.js`: the way in (decision A).** Find:

```js
        <p class="tst-free">7 days free, no card.</p></div>`, pane => {
```

Replace with:

```js
        <p class="tst-free">7 days free, no card.</p>
        <a class="tst-try" href="onboarding.html?guest=1">Or try your first lesson now, no account needed →</a></div>`, pane => {
```

Leave the `tst-go` button and its link exactly as they are.

**6. `index.html`.** Find the CSS rule that starts `.tst-go:active{` and add under it:

```css
.tst-try{display:inline-block;margin-top:10px;font-size:14px;color:var(--ink-soft);text-decoration:underline}
```

Then change `taster.js?v=2` to `taster.js?v=3` (one place).

**7. New file `tests/guest_lesson.py`,** shaped like `tests/first_lesson.py`. For a visitor who isn't signed in, make a second fake from `FAKE`:

```python
NOBODY = FAKE.replace("getSession: async () => ({ data: { session } })", "getSession: async () => ({ data: { session: null } })") \
             .replace("getUser: () => wait({ data: { user: session.user } })", "getUser: () => wait({ data: { user: null } })")
assert NOBODY.count("session: null") == 1 and NOBODY.count("user: null") == 1
```

Check:

1. Not signed in, `onboarding.html?guest=1`: stays on the page (the address still contains `onboarding.html`) and `#first` is visible.
2. Walk the lesson as `tests/first_lesson.py` does. A guest has no name, so step 4's heading is "Now a name" and the tiles in step 5 are the greeting, `ismī` and Samir. After Finish: `#well` is visible, `#wellGo` reads "Create my free account", and the note contains "Create your free account".
3. Still as the guest: `localStorage.getItem('rafiq_guest_lesson')` is `'1'`, and `Progress.isNew('v:1')` is still true (nothing saved).
4. Click `#wellGo`: the address ends with `login.html?mode=signup`.
5. Signed in (the ordinary `FAKE`), with `localStorage.setItem('rafiq_guest_lesson','1')` in the init script, `onboarding.html`: `#qs` is visible and `#first` isn't; `Progress.isNew('v:1')` is false; `RafiqPath.doneToday()` is at least 1; the flag is gone.
6. Not signed in, plain `onboarding.html` (no `guest`): sent to `login.html`, as before.
7. Signed in, `onboarding.html?guest=1`: ends on `onboarding.html` without the `guest` part.
8. No page errors.

**8. `tests/taster.py`.** Add one check: the end card has a `.tst-try` link whose `href` is `onboarding.html?guest=1`. Leave the existing `.tst-go` check alone.

**9. `CLAUDE.md`.** Add a line for `tests/guest_lesson.py`.

### Tests to run
`tests/guest_lesson.py`, `tests/first_lesson.py`, `tests/taster.py`, `tests/landing.py`, `tests/login_page.py`, then rule 11's three.

### Known limit (write it in the closing note)
If the confirm link opens in a different browser from the one the guest used, that browser has no record of the guest lesson, so the lesson is offered again. Nothing is lost, it's just repeated.

### Not in this task
Don't change the main "Start your free week" buttons, the sign-in page, or what a signed-in new account sees. Don't ask the guest for their name: that is a possible follow-up, and belongs in a new issue if it seems worth it.

---

## Owner steps (not for a model)

### A. An earlier update to `main` (#382)

`main` was last updated on 11 Oct, so nothing above reaches a learner until the next update. To decide: update before mid-December or not.

If yes, before updating:
- `wip` also holds units 13 to 16. They wait on the teacher check (#367). Either that's done, or those four units are held back from this update. Holding them back means a change to `path.js`, which is Samir's.
- Every test in `CLAUDE.md` passes on `wip`.
- Try the first five minutes as a new learner on a phone at the `wip` preview address in `CLAUDE.md`.
- The update runs the backend deploy, which makes the `idle_signout` counter (Task 1) and the `asked_at` column (Task 6) real.
- After the update, run the Reminders workflow once with `setup`: it adds the two columns Task 5 needs. Safe to run twice.

### B. Sign up on a phone from the Instagram link (#374)

Ten minutes, on the live site. The steps are in the issue. If the confirm link strands people in another browser, that's the case for Task 7.

### C. Switching on what was built switched off

- **Study emails (#379).** Read the wording on the issue. Decide whether these are service emails or need an opt-out line on the sign-up form (a question about the UK email rules, for the owner, not a model). Run the Reminders workflow with `preview` to see who would get one. To switch on: change `NUDGES_ON` to `true` in `tools/send-reminders.js`, and the line in its self-test that expects `false`.
- **"What stopped you?" (#380).** Approve the wording and who signs. Run `ask-preview`. Then run `ask` with the second input `SEND-ASK`. It sends once per account.

## Already built: nothing to do

- **The home-screen app offer (suggestion 9).** Home already shows the install card once a learner has finished a first lesson step (`RafiqPWA.card` in `pwa.js`, called from `dashboard.html`), with "open this in Safari first" for Instagram's browser. It's on `wip` and goes live with the next update.
- **Asking for the reminder after the first lesson (suggestion 5).** The faster start (#348) does this on `wip`. Task 3 covers what's left.

## How to tell if it's working

Two numbers, per week of joining, from the owner dashboard and the users workflow (`active`, `trials`):

- finished a first lesson step: 38% on 14 Nov
- studied on a second day: 12% on 14 Nov

With about 7 sign-ups a week there's no room for A/B tests. Ship one change at a time and compare weeks.
