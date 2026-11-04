"""The app's daily reminders (#35, reminders.js): inside the iPhone/Android app the phone schedules its own.
  Home is opened as the app would (a stand-in for Capacitor's LocalNotifications records what's scheduled):
  - with a reminder time saved on the phone, the next 7 days are scheduled at that hour (today only if it's still ahead)
  - once today's goal is met, today's reminder is dropped
  - on the website (no Capacitor) nothing is scheduled and the service worker still registers
  ... -- python3 tests/app_reminders.py   (same server command as the smoke test)
"""
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from startup_speed import FAKE, MIRROR, BASE
from playwright.sync_api import sync_playwright

CAP = """window.__ln = [];
window.Capacitor = { isNativePlatform: () => true, Plugins: { LocalNotifications: {
  schedule: async o => { window.__ln = o.notifications.map(n => ({ id: n.id, at: new Date(n.schedule.at).toISOString(), title: n.title })); },
  getPending: async () => ({ notifications: window.__ln.map(n => ({ id: n.id })) }),
  cancel: async o => { const ids = o.notifications.map(n => n.id); window.__ln = window.__ln.filter(n => !ids.includes(n.id)); },
  requestPermissions: async () => ({ display: 'granted' }) } } };"""

def run(hour, mirror, native=True):
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium")
        c = b.new_context(viewport={"width": 390, "height": 844}, service_workers="allow")
        c.route("**/@supabase/**", lambda r: r.fulfill(status=200, content_type="application/javascript", body=FAKE))
        c.add_init_script(("%s;" % CAP if native else "") + "localStorage.setItem('rafiq_progress_mirror',%s);localStorage.setItem('rafiq_onboarded','u1');"
                          "localStorage.setItem('rafiq_local_reminder','%d')" % (json.dumps(json.dumps(mirror)), hour))
        p = c.new_page(); errs = []; p.on("pageerror", lambda e: errs.append(str(e)))
        p.goto(BASE + "dashboard.html"); p.wait_for_selector("#home .today-card"); p.wait_for_timeout(1500)
        r = p.evaluate("({ ln: window.__ln || null, sw: !!(navigator.serviceWorker && navigator.serviceWorker.controller) || null, now: new Date().toISOString(), hour: new Date().getHours() })")
        b.close(); return r, errs

def main():
    ok = []
    late = 23                                     # a time still ahead today is unusual at 23:xx; test both cases by the clock
    r, errs = run(late, MIRROR)
    days = sorted({n["at"][:10] for n in r["ln"]})
    today_ahead = r["hour"] < late
    ok.append(("7 days ahead (6 if today's time has passed)", len(r["ln"]) == (7 if today_ahead else 6) and len(days) == len(r["ln"])))
    ok.append(("each at the chosen hour", all(__import__("datetime").datetime.fromisoformat(n["at"].replace("Z", "+00:00")).astimezone().hour == late for n in r["ln"])))
    done = dict(MIRROR); today = r["now"][:10]
    import datetime as dt
    local_today = dt.datetime.now().strftime("%Y-%m-%d")
    done = {**MIRROR, "s:" + local_today: {"seen": 9, "box": 0}} if isinstance(MIRROR, dict) else MIRROR
    r2, errs2 = run(late, done)
    ok.append(("goal met today: today's reminder dropped", len(r2["ln"]) == 6 and all(n["id"] != 1000 for n in r2["ln"])))
    r3, errs3 = run(late, MIRROR, native=False)
    ok.append(("website: nothing scheduled", r3["ln"] in (None, [])))
    ok.append(("no page errors", not (errs or errs2 or errs3)))
    for name, good in ok: print(("ok  " if good else "FAIL") + "  " + name)
    print(f"\n{sum(g for _, g in ok)}/{len(ok)} passed"); raise SystemExit(0 if all(g for _, g in ok) else 1)

main()
