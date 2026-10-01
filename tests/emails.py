"""Emails (#177):
  - every email renders: welcome (with the basics and Your salah), "2 days left", "last day", and the new
    "your free week has ended" with the plans (Your salah in Complete), a Choose a plan link and the refund line
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
    open(os.path.join(d, "common.ts"), "w").write("export const SITE = 'https://rafiq-arabic.com';\n")
    open(os.path.join(d, "run.ts"), "w").write(
        "import { welcome, trialSoon, trialLast, trialEnded, text } from './emails.ts';\n"
        "const end = new Date('2026-10-08T09:00:00Z');\n"
        "const all = { welcome: welcome('Sam Ali', end), soon: trialSoon('Sam', end), last: trialLast(null), ended: trialEnded('Sam') };\n"
        "console.log(JSON.stringify(Object.fromEntries(Object.entries(all).map(([k, m]) => [k, { ...m, text: text(m.html) }]))));\n")
    out = subprocess.run(["node", "--experimental-strip-types", "--no-warnings", os.path.join(d, "run.ts")],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)

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
    m = render()
    w, e = m["welcome"], m["ended"]
    ok.append(("welcome: mentions the basics and Your salah, and the free week's end date",
               "the basics" in w["html"] and "Your salah" in w["html"] and "Thursday 8 October" in w["html"]))
    ok.append(("ended: subject " + repr(e["subject"]), e["subject"] == "Your free week of Rafiq has ended"))
    ok.append(("ended: progress saved, Choose a plan → plans.html, refund line",
               "saved" in e["html"] and "https://rafiq-arabic.com/plans.html" in e["html"] and "14 days" in e["html"]))
    ok.append(("ended and 2-days-left: Complete lists Your salah", all("<b>Your salah</b> in full" in m[k]["html"] for k in ("ended", "soon"))))
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
        ok.append(("the 'has ended' column exists", psql("select count(*) from information_schema.columns where table_name = 'billing' and column_name = 'trial_ended_sent_at'") == "1"))
    finally:
        run(BIN + "/pg_ctl", "-D", d + "/data", "-m", "fast", "stop")
    for name, good in ok: print(("ok   " if good else "FAIL ") + name)
    sys.exit(0 if all(g for _, g in ok) else 1)

if __name__ == "__main__":
    main()
