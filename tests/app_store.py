"""The app's purchases (#352): inside the iPhone and Android app, Plans and Settings never offer Stripe (Apple 3.1.1);
Plans is the App Store / Google Play subscription screen (RevenueCat), with the terms Apple asks for (3.1.2) and Restore purchases.
The website's pages are unchanged. Runs on app/www (built with node app/build-web.js if it's missing), with the app stood in for.

  python3 .claude/skills/webapp-testing/scripts/with_server.py --server "python3 -m http.server 8766 -d app/www >/dev/null 2>&1" --port 8766 \
    --server "python3 -m http.server 8767 >/dev/null 2>&1" --port 8767 -- python3 tests/app_store.py
"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from startup_speed import FAKE, MIRROR
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not os.path.exists(os.path.join(ROOT, "app/www/app-store.js")): subprocess.run(["node", "app/build-web.js"], cwd=ROOT, check=True)
APP, WEB = "http://localhost:8766/", "http://localhost:8767/"
CAP = """window.__buys=[];window.Capacitor={isNativePlatform:()=>true,getPlatform:()=>'ios',Plugins:{Browser:{open:o=>{window.__opened=o.url}},
 Purchases:{configure:async o=>{window.__conf=o},
  getOfferings:async()=>({current:{availablePackages:[
   {identifier:'$rc_annual',packageType:'ANNUAL',product:{identifier:'rafiq_complete_yearly',priceString:'£79.99',pricePerMonthString:'£6.67',introPrice:{price:0}}},
   {identifier:'$rc_monthly',packageType:'MONTHLY',product:{identifier:'rafiq_complete_monthly',priceString:'£11.99'}},
   {identifier:'ess_y',packageType:'ANNUAL',product:{identifier:'rafiq_essentials_yearly',priceString:'£49.99',pricePerMonthString:'£4.17',introPrice:{price:0}}},
   {identifier:'ess_m',packageType:'MONTHLY',product:{identifier:'rafiq_essentials_monthly',priceString:'£6.99'}}]}}),
  purchasePackage:async o=>{window.__buys.push(o.aPackage.product.identifier);throw {userCancelled:true}},
  restorePurchases:async()=>({customerInfo:{entitlements:{active:{}}}})}}};"""
BILL = {"plan": "complete", "status": "active", "interval": "year", "source": "stripe", "current_period_end": "2027-05-01T00:00:00Z", "cancel_at_period_end": False, "has_customer": True}
ok, errors = [], []
def ctx(b, init, keyed=False):
    c = b.new_context(viewport={"width": 390, "height": 844})
    for pat in ("**/vendor/supabase.js", "**/@supabase/**"): c.route(pat, lambda r: r.fulfill(status=200, content_type="application/javascript", body=FAKE))
    if keyed: c.route("**/app-store.js", lambda r: r.fulfill(status=200, content_type="application/javascript",
                     body=open(os.path.join(ROOT, "app/www/app-store.js")).read().replace("ios: ''", "ios: 'appl_test'")))
    calls = []; c.route("**/functions/v1/billing", lambda r: (calls.append(1), r.fulfill(status=200, content_type="application/json", body="{}")))
    c.add_init_script(init + "localStorage.setItem('rafiq_progress_mirror',%s);localStorage.setItem('rafiq_onboarded','u1');" % json.dumps(json.dumps(MIRROR)))
    p = c.new_page(); p.on("pageerror", lambda e: errors.append(str(e)) if "registerPlugin" not in str(e) else None)   # the stand-in app has no plugin registry
    return c, p, calls
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium")
    c, p, _ = ctx(b, CAP); p.goto(APP + "plans.html"); p.wait_for_timeout(2000)
    t = p.inner_text("main")
    ok.append(("app, before the store is set up: no Stripe, plans 'opening soon', Restore purchases, Terms and Privacy",
               "Stripe" not in t and "checkout" not in t.lower() and p.locator("[data-price]").all_inner_texts() == ["Opening soon"] * 2
               and p.locator("#spRestore").count() == 1 and p.locator(".sp-fine a[href='terms.html'], .sp-fine a[href='privacy.html']").count() == 2))
    ok.append(("…and the auto-renewal terms Apple asks for", "renews automatically" in t and "24 hours" in t))
    c.close()
    c, p, calls = ctx(b, CAP, keyed=True); p.goto(APP + "plans.html"); p.wait_for_timeout(2000)
    ok.append(("app, with the store: the store's prices, tied to the Rafiq account", p.locator("[data-price]").all_inner_texts() == ["£49.99 / year", "£79.99 / year"]
               and p.evaluate("window.__conf.appUserID") == "u1"))
    p.locator("[data-buy]").last.click(); p.wait_for_timeout(500)
    ok.append(("buying asks the store, never Stripe; cancelling there says nothing", p.evaluate("window.__buys") == ["rafiq_complete_yearly"] and not calls and p.inner_text("#spMsg") == ""))
    p.click(".sp-seg button[data-i=month]"); p.wait_for_timeout(200)
    ok.append(("monthly prices", p.locator("[data-price]").all_inner_texts() == ["£6.99 / month", "£11.99 / month"]))
    p.click("#spRestore"); p.wait_for_timeout(500)
    ok.append(("Restore with nothing to restore says so", "No subscription found" in p.inner_text("#spMsg")))
    c.close()
    for base, cap, tag in ((APP, CAP, "app"), (WEB, "", "website")):
        c, p, _ = ctx(b, cap + "localStorage.setItem('rafiq_billing',%s);" % json.dumps(json.dumps(BILL))); p.goto(base + "settings.html"); p.wait_for_timeout(2500)
        btns = p.locator("#planActs > *").all_inner_texts()
        if tag == "app": ok.append(("app Settings, a plan bought on the website: managed there, no Stripe buttons (%s)" % btns, btns == [] and "rafiq-arabic.com" in p.inner_text("#planInfo")))
        else: ok.append(("website Settings unchanged: Cancel subscription and Manage billing (%s)" % btns, btns == ["Cancel subscription", "Manage billing"]))
        c.close()
    c, p, _ = ctx(b, ""); p.goto(WEB + "plans.html"); p.wait_for_timeout(1500)
    ok.append(("website Plans unchanged: Stripe's page, no store screen", p.locator(".card[data-plan]").count() == 2 and p.locator(".sp-card").count() == 0))
    c.close(); b.close()
ok.append(("no page errors " + "; ".join(errors[:3]), not errors))
for n, g in ok: print(("ok  " if g else "FAIL"), n)
print("\n%d of %d passed" % (sum(g for _, g in ok), len(ok))); sys.exit(0 if all(g for _, g in ok) else 1)
