"""The owner dashboard (admin.html, #189), with the admin-stats function answered by a fixture (the real numbers
from 2 Oct 2026): the tiles, every day of the range drawn, referrers named (Instagram), countries with flags,
sign-ups by source, the steps to an account (#225); a non-admin sees a short message; switching the range asks again; no page errors.

  python3 .claude/skills/webapp-testing/scripts/with_server.py \
    --server "python3 -m http.server 8765 >/dev/null 2>&1" --port 8765 -- python3 tests/admin_page.py
"""
import json, os, sys
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8765/"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
SHOTS = os.environ.get("SHOTS")
FAKE = """
window.supabase = { createClient: () => {
  const q = () => { const o = new Proxy(function(){}, { get: (t, k) => k === 'then' ? (res => Promise.resolve({ data: null, error: null }).then(res)) : () => o }); return o; };
  const session = { access_token: 't', expires_at: Date.now() / 1000 + 3600, user: { id: 'u1', email: 't@example.com', user_metadata: {}, app_metadata: { admin: true } } };
  return { from: q, rpc: q, auth: { getSession: async () => ({ data: { session } }), getUser: async () => ({ data: { user: session.user } }),
    onAuthStateChange: () => ({ data: { subscription: { unsubscribe() {} } } }), updateUser: async () => ({}), signOut: async () => ({}) } };
} };
"""
from datetime import date, timedelta
TODAY = date.today()
STATS = {"days": 7, "accounts": 18, "taps": [{"step": "signup_page", "n": 6}, {"step": "create", "n": 4}],
         "sources": [{"source": "unknown", "campaign": None, "joined": 2, "first_lesson": 1, "back_next_day": 0, "chose_plan": 0, "paying": 0},
                                                {"source": "instagram", "campaign": "brother", "joined": 1, "first_lesson": 1, "back_next_day": 0, "chose_plan": 1, "paying": 0}],
         "web": {"visits": 18, "views": 19,
                 "days": [{"name": str(TODAY - timedelta(days=1)), "visits": 8, "views": 9}, {"name": str(TODAY), "visits": 10, "views": 10}],
                 "refs": [{"name": "", "visits": 14, "views": 15}, {"name": "l.instagram.com", "visits": 4, "views": 4}],
                 "countries": [{"name": "US", "visits": 9, "views": 9}, {"name": "GB", "visits": 7, "views": 8}, {"name": "XK", "visits": 1, "views": 1}],
                 "paths": [{"name": "/", "visits": 15, "views": 15}, {"name": "/dashboard.html", "visits": 2, "views": 2}],
                 "devices": [{"name": "mobile", "visits": 12, "views": 12}, {"name": "desktop", "visits": 6, "views": 7}]}}

def main():
    ok, errors, asked = [], [], []
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME if os.path.exists(CHROME) else None)
        for scheme in ("light", "dark"):
            c = b.new_context(viewport={"width": 390, "height": 844}, color_scheme=scheme, service_workers="block")
            c.route("**/@supabase/**", lambda r: r.fulfill(status=200, content_type="application/javascript", body=FAKE))
            c.route("https://fonts.googleapis.com/**", lambda r: r.abort())
            def stats(r):
                asked.append(json.loads(r.request.post_data or "{}").get("days"))
                r.fulfill(status=200, content_type="application/json", headers={"Access-Control-Allow-Origin": "*"}, body=json.dumps(STATS))
            c.route("**/functions/v1/admin-stats", stats)
            p = c.new_page(); p.on("pageerror", lambda e: errors.append(str(e)))
            p.goto(BASE + "admin.html"); p.wait_for_selector("#out:not([hidden])", timeout=8000)
            if scheme == "light":
                ok.append(("tiles: 18 visits, 19 views, 3 sign-ups, 18 accounts",
                           [p.inner_text(f"#{i}") for i in ("tVisits", "tViews", "tJoined", "tAcc")] == ["18", "19", "3", "18"]))
                ok.append(("every day of the 7 drawn, empty ones too", p.locator(".day").count() == 7))
                refs = p.inner_text("#refs")
                ok.append(("referrers named: Instagram and Direct", "Instagram" in refs and "Direct" in refs))
                cs = p.inner_text("#countries")
                ok.append(("countries with names and flags: " + cs.replace("\n", " ")[:80], "United Kingdom" in cs and "🇬🇧" in cs and "United States" in cs))
                st = p.inner_text("#steps").split("\n")
                ok.append(("steps to an account: 15 home views, 6 opened sign-up, 4 pressed Create, 0 Google, 3 accounts: " + " / ".join(st),
                           st[1::2] == ["15", "6", "4", "0", "3"]))
                ok.append(("sign-ups by source in a table", "Before tracking" in p.inner_text("#sources") and p.locator("#sources tr").count() == 3))
                p.click(".range button[data-d='30']"); p.wait_for_timeout(300)
                ok.append(("30 days asks for 30 and draws 30 days", asked[-1] == 30 and p.locator(".day").count() == 30))
                p.goto(BASE + "index.html"); p.wait_for_timeout(300)
                ok.append(("a team member's device is marked, and the visits beacon doesn't load on it",
                           p.evaluate("localStorage.getItem('rafiq_team')") == "1" and p.locator("script[src*='cloudflareinsights']").count() == 0))
                p.goto(BASE + "admin.html"); p.wait_for_selector("#out:not([hidden])", timeout=8000)
                wide = p.evaluate("document.documentElement.scrollWidth <= innerWidth")
                ok.append(("nothing wider than a phone screen", wide))
            if SHOTS: p.screenshot(path=f"{SHOTS}/admin-{scheme}.png", full_page=True)
            c.close()
        # not an admin
        c = b.new_context(viewport={"width": 390, "height": 844}, service_workers="block")
        c.route("**/@supabase/**", lambda r: r.fulfill(status=200, content_type="application/javascript", body=FAKE))
        c.route("**/functions/v1/admin-stats", lambda r: r.fulfill(status=403, content_type="application/json",
                headers={"Access-Control-Allow-Origin": "*"}, body='{"error":"not_admin"}'))
        p = c.new_page(); p.on("pageerror", lambda e: errors.append(str(e)))
        p.goto(BASE + "admin.html"); p.wait_for_timeout(800)
        ok.append(("not an admin: a short message, no numbers", "only for the Rafiq team" in p.inner_text("#msg") and p.locator("#out[hidden]").count() == 1))
        c.close(); b.close()
    ok.append(("no page errors " + "; ".join(errors[:3]), not errors))
    for name, good in ok: print(("ok   " if good else "FAIL ") + name)
    sys.exit(0 if all(g for _, g in ok) else 1)

if __name__ == "__main__":
    main()
