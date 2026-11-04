"""App store purchases (#345): what each RevenueCat event does to an account's billing row (supabase/functions/_shared/store.ts).
  - a purchase in the free week is 'trialing' until the store's first charge; a straight purchase is 'active'
  - App Store and Google Play product ids give the plan and the period (Google's arrive as "<subscription>:<base plan>")
  - cancelling keeps the plan to the end of the period; a refund through Apple or Google ends it now; expiry ends it
  - renewals, billing problems; events that aren't used, sandbox-only ids, and ones without a Rafiq account are skipped
  - the owner's alert says which store, and a price not in pounds is shown as it was paid
  python3 tests/store_webhook.py          (needs Node 22)
"""
import json, os, shutil, subprocess, tempfile
ROOT = os.path.join(os.path.dirname(__file__), "..")
UID = "6f1c2a9e-1b2c-4d3e-8f9a-0b1c2d3e4f50"

def run():
    d = tempfile.mkdtemp()
    shutil.copy(os.path.join(ROOT, "supabase/functions/_shared/store.ts"), d)
    ev = lambda **k: {"app_user_id": UID, "store": "APP_STORE", "product_id": "rafiq_complete_monthly", "period_type": "NORMAL",
                      "expiration_at_ms": 1767225600000, "event_timestamp_ms": 1765000000000, "original_transaction_id": "t1",
                      "currency": "GBP", "price_in_purchased_currency": 11.99, **k}
    cases = {
        "trial": ev(type="INITIAL_PURCHASE", period_type="TRIAL"),
        "buy": ev(type="INITIAL_PURCHASE", store="PLAY_STORE", product_id="rafiq_essentials:yearly", price_in_purchased_currency=79.99),
        "renew": ev(type="RENEWAL"),
        "cancel": ev(type="CANCELLATION", cancel_reason="UNSUBSCRIBE"),
        "cancelTrial": ev(type="CANCELLATION", cancel_reason="UNSUBSCRIBE", period_type="TRIAL"),
        "refund": ev(type="CANCELLATION", cancel_reason="CUSTOMER_SUPPORT"),
        "expire": ev(type="EXPIRATION"),
        "billing": ev(type="BILLING_ISSUE"),
        "dollars": ev(type="INITIAL_PURCHASE", currency="USD", price_in_purchased_currency=14.99),
        "change": ev(type="PRODUCT_CHANGE"),
        "test": {"type": "TEST"},
        "anon": ev(type="INITIAL_PURCHASE", app_user_id="$RCAnonymousID:abc", aliases=["$RCAnonymousID:abc"]),
        "alias": ev(type="RENEWAL", app_user_id="$RCAnonymousID:abc", aliases=["$RCAnonymousID:abc", UID]),
        "stripe": ev(type="INITIAL_PURCHASE", store="STRIPE"),
        "other": ev(type="INITIAL_PURCHASE", product_id="rafiq_coins"),
    }
    open(os.path.join(d, "run.ts"), "w").write(
        "import { fromEvent } from './store.ts';\n"
        f"const cases = {json.dumps(cases)};\n"
        "console.log(JSON.stringify(Object.fromEntries(Object.entries(cases).map(([k, e]) => [k, fromEvent(e)]))));\n")
    r = subprocess.run(["node", "--experimental-strip-types", "--no-warnings", os.path.join(d, "run.ts")], capture_output=True, text=True, check=True)
    return json.loads(r.stdout)

def main():
    r, ok = run(), []
    u = lambda k: r[k].get("update") or {}
    ok.append(("free week: trialing, Complete monthly, first charge at the period's end",
               u("trial").get("status") == "trialing" and u("trial").get("plan") == "complete" and u("trial").get("interval") == "month"
               and r["trial"]["alert"]["firstCharge"] and r["trial"]["source"] == "apple"))
    ok.append(("Google: Essentials yearly, active, £79.99, 'through Google Play'",
               u("buy").get("status") == "active" and u("buy").get("plan") == "essentials" and u("buy").get("interval") == "year"
               and u("buy").get("source") == "google" and r["buy"]["alert"]["pence"] == 7999 and "Google Play" in r["buy"]["alert"]["via"]))
    ok.append(("renewal: active, no alert", u("renew").get("status") == "active" and "alert" not in r["renew"]))
    ok.append(("cancel: keeps the plan to the end, alert 'keep'", u("cancel").get("plan") == "complete" and u("cancel").get("cancel_at_period_end") is True
               and r["cancel"]["alert"]["kind"] == "keep"))
    ok.append(("cancel in the free week: alert 'free'", r["cancelTrial"]["alert"]["kind"] == "free"))
    ok.append(("refund: plan ends now", u("refund").get("plan") is None and u("refund").get("status") == "canceled" and r["refund"]["alert"]["kind"] == "refund"))
    ok.append(("expiry: plan ends", u("expire").get("plan") is None and u("expire").get("status") == "canceled"))
    ok.append(("billing problem: past_due, plan kept", u("billing").get("status") == "past_due" and u("billing").get("plan") == "complete"))
    ok.append(("a price in dollars: £0 and the price shown as paid", r["dollars"]["alert"]["pence"] == 0 and "14.99 USD" in r["dollars"]["alert"]["via"]))
    ok.append(("skipped: plan change (applied at renewal), test, anonymous id, Stripe, unknown product",
               all(r[k].get("skip") for k in ("change", "test", "anon", "stripe", "other"))))
    ok.append(("an account id among the aliases is used", r["alias"].get("uid") == UID))
    for name, good in ok: print(("ok  " if good else "FAIL") + "  " + name)
    print(f"\n{sum(g for _, g in ok)}/{len(ok)} passed")
    raise SystemExit(0 if all(g for _, g in ok) else 1)

main()
