"""Emails (#177):
  - every email renders: welcome (with the basics and Your salah), "2 days left", "last day", and the new
    "your free week has ended" with the plans (Your salah in Complete), a Choose a plan link and the refund line
  - "thank you for subscribing" (#178) gives the plan, monthly or yearly, the price and when the first payment is
    taken (the end of the free week, or today); "payment received" gives the amount, the next payment and the receipt;
    the subscription is read the same from Stripe's older and newer formats
  - the welcome email is asked for once per account: for a sign-up that arrives already confirmed (Google,
    Apple) as well as one that confirms by email later; never again after that
  The SQL part runs supabase/sql/backend.sql's billing and welcome sections on a throwaway Postgres, with
  pg_net's http_post stood in for by a table that records each call.

  python3 tests/emails.py          (needs Node 22 and Postgres 16: /usr/lib/postgresql/16/bin)
"""
import json, os, re, shutil, subprocess, sys, tempfile

ROOT = os.path.join(os.path.dirname(__file__), "..")
BIN = "/usr/lib/postgresql/16/bin"

def render():
    d = tempfile.mkdtemp()
    shutil.copy(os.path.join(ROOT, "supabase/functions/_shared/emails.ts"), d)
    shutil.copy(os.path.join(ROOT, "supabase/functions/_shared/sub-info.ts"), d)
    open(os.path.join(d, "common.ts"), "w").write("export const SITE = 'https://rafiq-arabic.com';\n")
    open(os.path.join(d, "run.ts"), "w").write(
        "import { welcome, trialSoon, trialLast, trialEnded, subscribed, paymentReceived, text } from './emails.ts';\n"
        "import { subInfo } from './sub-info.ts';\n"
        "const end = new Date('2026-10-08T09:00:00Z');\n"
        # a subscription in the free week, older API shape; and one charged at once, newer shape (period on the item)
        "const oldSub = { status: 'trialing', trial_end: Date.parse('2026-10-17T23:00:00Z') / 1000, current_period_end: 1,\n"
        "  items: { data: [{ price: { lookup_key: 'rafiq_essentials_monthly', unit_amount: 699, recurring: { interval: 'month' } } }] } };\n"
        "const newSub = { status: 'active', trial_end: null,\n"
        "  items: { data: [{ current_period_end: 2, price: { lookup_key: 'rafiq_complete_yearly', unit_amount: 7999, recurring: { interval: 'year' } } }] } };\n"
        "const a = subInfo(oldSub), b = subInfo(newSub);\n"
        "const all = { welcome: welcome('Sam Ali', end), soon: trialSoon('Sam', end), last: trialLast(null), ended: trialEnded('Sam'),\n"
        "  subTrial: subscribed('Sam', a.plan, a.interval, a.pence, a.firstCharge), subNow: subscribed('Sam', b.plan, b.interval, b.pence, b.firstCharge),\n"
        "  paid: paymentReceived('Sam', 'essentials', 699, new Date('2026-11-18T00:00:00Z'), 'https://invoice.stripe.com/i/x') };\n"
        "console.error(JSON.stringify({ a, b }));\n"
        "console.log(JSON.stringify(Object.fromEntries(Object.entries(all).map(([k, m]) => [k, { ...m, text: text(m.html) }]))));\n")
    r = subprocess.run(["node", "--experimental-strip-types", "--no-warnings", os.path.join(d, "run.ts")],
                       capture_output=True, text=True, check=True)
    return json.loads(r.stdout), json.loads(r.stderr)

def sql_part():
    s = open(os.path.join(ROOT, "supabase/sql/backend.sql")).read()
    s = s[s.index("create table if not exists public.billing"):s.index("-- Free-week reminder emails")]
    return s.replace("create extension if not exists pg_net;", "")

SETUP = """
create schema auth; create schema net;
create role anon; create role authenticated;
create table auth.users (id uuid primary key, email text, created_at timestamptz default now(), email_confirmed_at timestamptz);
create function auth.uid() returns uuid language sql as 'select null::uuid';
create table net.calls (url text, body jsonb);
create function net.http_post(url text, body jsonb, params jsonb, headers jsonb) returns bigint
  language sql as 'insert into net.calls values (url, body) returning 1';
"""

def main():
    ok = []
    m, info = render()
    w, e = m["welcome"], m["ended"]
    ok.append(("welcome: mentions the basics and Your salah, and the free week's end date",
               "the basics" in w["html"] and "Your salah" in w["html"] and "Thursday 8 October" in w["html"]))
    ok.append(("ended: subject " + repr(e["subject"]), e["subject"] == "Your free week of Rafiq has ended"))
    ok.append(("ended: progress saved, Choose a plan → plans.html, refund line",
               "saved" in e["html"] and "https://rafiq-arabic.com/plans.html" in e["html"] and "14 days" in e["html"]))
    ok.append(("ended and 2-days-left: Complete lists Your salah", all("<b>Your salah</b> in full" in m[k]["html"] for k in ("ended", "soon"))))
    a, b = info["a"], info["b"]
    ok.append(("subscription read: free week, Essentials monthly £6.99, first charge at the week's end " + str(a),
               a["plan"] == "essentials" and a["interval"] == "month" and a["pence"] == 699 and a["firstCharge"].startswith("2026-10-17T23")))
    ok.append(("subscription read (newer format): Complete yearly £79.99, charged now " + str(b),
               b["plan"] == "complete" and b["interval"] == "year" and b["pence"] == 7999 and b["firstCharge"] is None))
    st, sn, pd = m["subTrial"], m["subNow"], m["paid"]
    ok.append(("thank you, in the free week: " + repr(st["subject"]),
               st["subject"] == "Thank you for subscribing to Rafiq Essentials" and "paid monthly" in st["html"] and "£6.99</b> a month" in st["html"]
               and "Sunday 18 October" in st["html"] and "free week ends" in st["html"] and "Settings → Your plan" in st["html"]))
    ok.append(("thank you, charged at once: yearly, £79.99, taken today",
               "paid yearly" in sn["html"] and "£79.99</b> a year" in sn["html"] and "has been taken today" in sn["html"]))
    ok.append(("payment received: " + repr(pd["subject"]),
               pd["subject"] == "Payment received: £6.99 for Rafiq Essentials" and "Wednesday 18 November" in pd["html"]
               and "https://invoice.stripe.com/i/x" in pd["html"] and "14 days" in pd["html"]))
    ok.append(("every email has a plain-text copy, no template leftovers",
               all(x["text"] and "${" not in x["html"] + x["text"] for x in m.values())))

    d = tempfile.mkdtemp(); os.chmod(d, 0o777)
    pg = ["sudo", "-u", "postgres"] if os.geteuid() == 0 else []
    run = lambda *a: subprocess.run(pg + list(a), check=True, capture_output=True, text=True)
    run(BIN + "/initdb", "-D", d + "/data", "-A", "trust")
    run(BIN + "/pg_ctl", "-D", d + "/data", "-l", d + "/log", "-o", f"-k {d} -p 54330 -c listen_addresses=''", "-w", "start")
    try:
        psql = lambda q: run("psql", "-h", d, "-p", "54330", "-d", "postgres", "-v", "ON_ERROR_STOP=1", "-At", "-c", q).stdout.strip()
        psql(SETUP); psql(sql_part())
        psql("insert into private.config values ('emails_url', 'https://x/functions/v1/emails'), ('hook_secret', 's')")
        calls = lambda: [json.loads(r) for r in psql("select body from net.calls").splitlines()]
        g, e1 = "00000000-0000-0000-0000-00000000000a", "00000000-0000-0000-0000-00000000000b"
        psql(f"insert into auth.users (id, email, email_confirmed_at) values ('{g}', 'g@example.com', now())")   # Google
        c = calls()
        ok.append(("Google sign-up (arrives confirmed): welcome asked for once", c == [{"kind": "welcome", "user_id": g}]))
        ok.append(("…and its billing row with the free week is there",
                   psql(f"select trial_ends_at::date - created_at::date from public.billing b join auth.users u on u.id = b.user_id where b.user_id = '{g}'") == "7"))
        psql(f"insert into auth.users (id, email) values ('{e1}', 'e@example.com')")                          # email sign-up
        ok.append(("email sign-up: nothing until confirmed", len(calls()) == 1))
        psql(f"update auth.users set email_confirmed_at = now() where id = '{e1}'")
        ok.append(("…confirmed: welcome asked for", calls()[-1] == {"kind": "welcome", "user_id": e1} and len(calls()) == 2))
        psql(f"update auth.users set email_confirmed_at = now() + interval '1 minute' where id in ('{g}', '{e1}')")
        ok.append(("confirming again: no second welcome", len(calls()) == 2))
        # the webhook's claim: update … where col is null or col <> id, returning; a repeat of the same event claims nothing
        claim = lambda col, id: psql(f"update public.billing set {col} = '{id}' where user_id = '{g}' and ({col} is null or {col} <> '{id}') returning user_id").split("\n")[0].replace("UPDATE 0", "")
        ok.append(("thank-you email: the first event claims it, the same event again doesn't, a new subscription does",
                   claim("subscribed_email_sub", "sub_1") == g and claim("subscribed_email_sub", "sub_1") == "" and claim("subscribed_email_sub", "sub_2") == g))
        ok.append(("payment email: once per invoice", claim("paid_email_invoice", "in_1") == g and claim("paid_email_invoice", "in_1") == ""
                   and claim("paid_email_invoice", "in_2") == g))
        ok.append(("the columns that stop repeat emails exist", psql("select count(*) from information_schema.columns where table_name = 'billing' and column_name in "
                   "('trial_ended_sent_at', 'subscribed_email_sub', 'paid_email_invoice')") == "3"))
    finally:
        run(BIN + "/pg_ctl", "-D", d + "/data", "-m", "fast", "stop")
    for name, good in ok: print(("ok   " if good else "FAIL ") + name)
    sys.exit(0 if all(g for _, g in ok) else 1)

if __name__ == "__main__":
    main()
