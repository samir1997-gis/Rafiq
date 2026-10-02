"""Where learners drop off (#26): private.funnel() in supabase/sql/backend.sql, run on a throwaway
Postgres with a handful of made-up accounts, one per case:
  joined, confirmed, finished a first lesson (a 'placed' row doesn't count), studied the next day,
  studied a week or more later, went through checkout, paying; and the "could be back" counts
  leave out people who joined too recently to have come back.

  python3 tests/funnel.py          (needs Postgres 16 installed: /usr/lib/postgresql/16/bin)
"""
import os, re, subprocess, sys, tempfile

BIN = "/usr/lib/postgresql/16/bin"
SQL = open(os.path.join(os.path.dirname(__file__), "..", "supabase/sql/backend.sql")).read()
FUNNEL = SQL[SQL.index("-- Where learners drop off"):]

SETUP = """
create schema auth; create schema private;
create role anon; create role authenticated; create role service_role;
create table auth.users (id uuid primary key, created_at timestamptz, email_confirmed_at timestamptz, raw_user_meta_data jsonb default '{}');
create table public.item_progress (user_id uuid, item_id text, primary key (user_id, item_id));
create table public.billing (user_id uuid primary key, status text, stripe_subscription_id text);
"""
# a fixed Monday three weeks back, so the made-up people all land in one week
DATA = """
with d as (select date_trunc('week', current_date - 21)::date as mon)
insert into auth.users select * from (values
  ('00000000-0000-0000-0000-000000000001'::uuid, (select mon from d)::timestamptz, null::timestamptz),       -- joined, nothing else
  ('00000000-0000-0000-0000-000000000002', (select mon from d), (select mon from d)),                         -- confirmed, only placed
  ('00000000-0000-0000-0000-000000000003', (select mon from d), (select mon from d)),                         -- lesson, next day
  ('00000000-0000-0000-0000-000000000004', (select mon from d), (select mon from d)),                         -- lesson, a week later, paying
  ('00000000-0000-0000-0000-000000000005', current_date::timestamptz, current_date::timestamptz)             -- joined today
) v;
insert into public.item_progress values
  ('00000000-0000-0000-0000-000000000002', 'p:00|placed'),
  ('00000000-0000-0000-0000-000000000003', 'p:00|letters1'),
  ('00000000-0000-0000-0000-000000000003', 's:' || to_char(date_trunc('week', current_date - 21)::date + 1, 'YYYY-MM-DD')),
  ('00000000-0000-0000-0000-000000000004', 'p:0b|b-the'),
  ('00000000-0000-0000-0000-000000000004', 's:' || to_char(date_trunc('week', current_date - 21)::date + 9, 'YYYY-MM-DD')),
  ('00000000-0000-0000-0000-000000000005', 'p:00|letters1');
insert into public.billing values
  ('00000000-0000-0000-0000-000000000003', 'trialing', 'sub_3'),
  ('00000000-0000-0000-0000-000000000004', 'active', 'sub_4');
update auth.users set raw_user_meta_data = '{"source": {"src": "tiktok", "campaign": "meet-rafiq"}}'
  where id in ('00000000-0000-0000-0000-000000000003', '00000000-0000-0000-0000-000000000004');
update auth.users set raw_user_meta_data = '{"name": "A", "source": {"src": "instagram.com"}}' where id = '00000000-0000-0000-0000-000000000001';
"""

def main():
    d = tempfile.mkdtemp(); os.chmod(d, 0o777)
    pg = ["sudo", "-u", "postgres"] if os.geteuid() == 0 else []
    run = lambda *a, **k: subprocess.run(pg + list(a), check=True, capture_output=True, text=True, **k)
    data, sock = d + "/data", d
    run(BIN + "/initdb", "-D", data, "-A", "trust")
    run(BIN + "/pg_ctl", "-D", data, "-l", d + "/log", "-o", f"-k {sock} -p 54329 -c listen_addresses=''", "-w", "start")
    try:
        psql = lambda sql: run("psql", "-h", sock, "-p", "54329", "-d", "postgres", "-v", "ON_ERROR_STOP=1", "-At", "-F", "|", "-c", sql).stdout.strip()
        psql(SETUP); psql(FUNNEL); psql(DATA)
        rows = [r.split("|") for r in psql("select * from private.funnel()").splitlines()]
        new, old = (list(map(int, r[1:])) for r in (rows[0], rows[-1]))   # newest week first
        src = {r.split("|")[0]: r.split("|")[1:] for r in psql("select * from private.funnel_by_source(30)").splitlines()}
        ok = [
            ("the week three weeks back: 4 joined, 3 confirmed, 2 finished a lesson (placed doesn't count) " + str(old[:3]), old[:3] == [4, 3, 2]),
            ("…all 4 could be back the next day, 1 was " + str(old[3:5]), old[3:5] == [4, 1]),
            ("…all 4 could be back after a week, 1 was " + str(old[5:7]), old[5:7] == [4, 1]),
            ("…2 chose a plan, 1 paying " + str(old[7:]), old[7:] == [2, 1]),
            ("this week: 1 joined today, not yet counted as able to come back " + str(new), new[0] == 1 and new[3] == 0 and new[5] == 0),
            ("by source: tiktok (meet-rafiq) 2 joined, 2 lessons, 1 next day, 2 chose a plan, 1 paying " + str(src.get("tiktok")),
             src.get("tiktok") == ["meet-rafiq", "2", "2", "1", "2", "1"]),
            ("…instagram.com 1 joined, nothing else; no source saved shows as unknown (2) " + str(src.get("instagram.com")) + str(src.get("unknown")),
             src.get("instagram.com") == ["", "1", "0", "0", "0", "0"] and src.get("unknown", [None, None])[1] == "2"),
            ("the dashboard's wrappers: the service key gets the same rows and the account count, a learner gets nothing",
             psql("set role service_role; select count(*) from public.admin_funnel_by_source(30)").splitlines()[-1] == str(len(src))
             and psql("set role service_role; select public.admin_account_count()").splitlines()[-1] == "5"
             and "permission denied" in subprocess.run(pg + ["psql", "-h", sock, "-p", "54329", "-d", "postgres", "-c",
                "set role authenticated; select * from public.admin_funnel_by_source(30)"], capture_output=True, text=True).stderr),
            ("the learner's own key can't run it", "permission denied" in subprocess.run(pg + ["psql", "-h", sock, "-p", "54329", "-d", "postgres", "-c",
                "set role authenticated; select * from private.funnel()"], capture_output=True, text=True).stderr),
        ]
    finally:
        run(BIN + "/pg_ctl", "-D", data, "-m", "fast", "stop")
    for name, good in ok: print(("ok   " if good else "FAIL ") + name)
    sys.exit(0 if all(g for _, g in ok) else 1)

if __name__ == "__main__":
    main()
