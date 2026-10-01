"""How long each main page takes to show its content for a signed-in learner (#171), with every server
call taking LATENCY ms (a normal phone connection), and with no connection at all after a first visit.

  python3 .claude/skills/webapp-testing/scripts/with_server.py \
    --server "python3 -m http.server 8765 >/dev/null 2>&1" --port 8765 -- python3 tests/startup_speed.py
"""
import json, os, sys, time
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8765/"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
LATENCY = int(os.environ.get("LATENCY", "400"))
# a signed-in learner; every call to the server takes LATENCY ms
FAKE = """
window.supabase = { createClient: () => {
  const wait = v => new Promise(r => setTimeout(() => r(v), %d));
  // a query answers with window.__rows (rows 'on the server'), or nothing
  const q = () => { const o = new Proxy(function(){}, { get: (t, k) => k === 'then'
      ? (res => wait({ data: window.__rows || null, error: null, count: 0 }).then(res)) : () => o }); return o; };
  const session = { access_token: 't', expires_at: Date.now() / 1000 + 3600, user: { id: 'u1', email: 't@example.com', user_metadata: { name: 'Aisha' } } };
  return { from: q, rpc: q, functions: { invoke: () => wait({ data: null, error: null }) }, auth: {
    getSession: async () => ({ data: { session } }), getUser: () => wait({ data: { user: session.user } }),
    onAuthStateChange: () => ({ data: { subscription: { unsubscribe() {} } } }), signOut: async () => ({}) } };
} };
""" % LATENCY
seen = lambda *ks: {k: {"box": 0, "seen": 1} for k in ks}
ALPHA = ["letters1", "letters2", "letters3", "letters4", "letters5", "letters6", "letters7", "vowels", "rules", "hear"]
MIRROR = seen(*[f"p:00|{k}" for k in ALPHA], *[f"p:0b|b-{k}" for k in ["the", "my", "people", "gender", "of", "many"]], "p:0b|test", "p:01|words1")
PAGES = [("Home", "dashboard.html", "#home .today-card"), ("Your salah", "salah.html", "#salah .parts"),
         ("Lesson", "learn.html?u=01&s=words2", ".stage .card"), ("Progress", "progress.html", ".urow"),
         ("Practise", "practise.html", "main a, main button")]

def timed(p, url, sel):
    t = time.time(); p.goto(BASE + url, wait_until="commit")
    try: p.wait_for_selector(sel, timeout=15000); return round((time.time() - t) * 1000)
    except Exception: return None

def main():
    out = {}
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME if os.path.exists(CHROME) else None)
        c = b.new_context(viewport={"width": 390, "height": 844}, service_workers="allow")
        c.route("**/@supabase/**", lambda r: r.fulfill(status=200, content_type="application/javascript", body=FAKE))
        c.route("https://fonts.googleapis.com/**", lambda r: r.abort())
        c.add_init_script("if(!localStorage.getItem('__s')){localStorage.setItem('rafiq_progress_mirror',%s);localStorage.setItem('rafiq_onboarded','u1');localStorage.setItem('rafiq_billing',JSON.stringify({plan:null,status:null,trial_ends_at:new Date(Date.now()+5*864e5).toISOString()}));localStorage.setItem('rafiq_salah_on','1');localStorage.setItem('__s','1')}"
                          % json.dumps(json.dumps(MIRROR)))
        p = c.new_page()
        p.goto(BASE + "dashboard.html"); p.wait_for_timeout(2500)        # first visit: the offline copy is saved
        for name, url, sel in PAGES:
            timed(p, url, sel)                                          # warm, as on a phone that's used the app before
            out[name] = [timed(p, url, sel)]
        c.set_offline(True)
        for name, url, sel in PAGES:
            out[name].append(timed(p, url, sel))
        # the background sync: newer rows from the server arrive, and nothing done here in the meantime is lost
        c2 = b.new_context(viewport={"width": 390, "height": 844})
        c2.route("**/@supabase/**", lambda r: r.fulfill(status=200, content_type="application/javascript", body=FAKE))
        c2.add_init_script("localStorage.setItem('rafiq_progress_mirror',%s);localStorage.setItem('rafiq_onboarded','u1');"
                           "window.__rows=[{item_id:'v:15',box:3,due:'2099-01-01',seen:4,updated_at:'2026-10-01T00:00:00Z'}];"
                           "addEventListener('rafiq:progress',()=>window.__repainted=true)" % json.dumps(json.dumps(MIRROR)))
        q = c2.new_page(); q.goto(BASE + "dashboard.html"); q.wait_for_selector("#home .today-card")
        q.evaluate("Progress.grade('v:16','good')")                       # done here before the server answers
        q.wait_for_timeout(LATENCY * 3 + 800)
        synced = q.evaluate("[Progress.get('v:15') && Progress.get('v:15').seen, !!Progress.get('v:16'), !!window.__repainted]")
        b.close()
    ok = []
    print(f"server calls take {LATENCY} ms")
    print(f"{'page':<11} online(ms)  offline(ms)")
    for k, (on, off) in out.items():
        print(f"{k:<11} {str(on) if on is not None else 'blank':>9}  {str(off) if off is not None else 'blank':>10}")
        ok.append((f"{k} shows within 600 ms, online and offline", on is not None and off is not None and on < 600 and off < 600))
    ok.append(("newer progress from the server arrives in the background " + str(synced), synced[0] == 4))
    ok.append(("…without losing what was done here first", synced[1]))
    ok.append(("…and Home repaints", synced[2]))
    for name, good in ok: print(("ok   " if good else "FAIL ") + name)
    sys.exit(0 if all(g for _, g in ok) else 1)

if __name__ == "__main__":
    main()
