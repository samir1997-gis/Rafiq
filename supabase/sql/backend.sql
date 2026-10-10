-- backend.sql — plans, the free week, the emails around them, and deleting an account.
-- Applied by the "Backend deploy" GitHub Action (tools/backend-deploy.js); safe to run again.

-- One row per account. Learners can read their own row; only the server
-- (Edge Functions, with the service key) writes it.
create table if not exists public.billing (
  user_id uuid primary key references auth.users(id) on delete cascade,
  trial_ends_at timestamptz not null,
  plan text check (plan in ('essentials','complete')),
  status text,                        -- Stripe: trialing | active | past_due | canceled | …
  interval text,                      -- month | year
  current_period_end timestamptz,
  cancel_at_period_end boolean not null default false,
  stripe_customer_id text,
  stripe_subscription_id text,
  welcome_sent_at timestamptz,
  trial_soon_sent_at timestamptz,     -- "2 days left" email
  trial_last_sent_at timestamptz,     -- "last day" email
  updated_at timestamptz not null default now()
);
alter table public.billing enable row level security;
drop policy if exists "read own billing" on public.billing;
create policy "read own billing" on public.billing for select using (auth.uid() = user_id);

-- Server-only things live in the private schema: not reachable with the public key.
create schema if not exists private;
revoke all on schema private from anon, authenticated;
create table if not exists private.config (key text primary key, value text not null);

-- The free week: 7 days from joining (#170, kept at 7). From the soft launch (1 Oct 2026)
-- new accounts get exactly that; accounts from the beta already have their row, ending
-- 17 Oct (a week after the planned 10 Oct launch), and keep it.
create or replace function private.trial_end_for(joined timestamptz) returns timestamptz
language sql immutable as $$
  select joined + interval '7 days'
$$;

-- every new account starts its free week
create or replace function private.billing_for_new_user() returns trigger
language plpgsql security definer set search_path = public, private as $$
begin
  -- never let this block a sign-up
  begin
    insert into public.billing (user_id, trial_ends_at) values (new.id, private.trial_end_for(new.created_at))
    on conflict (user_id) do nothing;
  exception when others then raise warning 'billing row not created for %: %', new.id, sqlerrm;
  end;
  return new;
end $$;
drop trigger if exists billing_new_user on auth.users;
create trigger billing_new_user after insert on auth.users
  for each row execute function private.billing_for_new_user();

-- accounts that already exist
insert into public.billing (user_id, trial_ends_at)
  select id, private.trial_end_for(created_at) from auth.users
  on conflict (user_id) do nothing;

-- "Your free week has ended" email (#177), sent once, the day after.
alter table public.billing add column if not exists trial_ended_sent_at timestamptz;
-- "Thank you for subscribing" (#178): which subscription it was last sent for, so a repeated
-- Stripe event never sends it twice.
alter table public.billing add column if not exists subscribed_email_sub text;
-- "You've cancelled" (#182): which cancellation it was sent for.
alter table public.billing add column if not exists cancel_email_for text;
-- when this account was last refunded automatically: the automatic refund is once per account
alter table public.billing add column if not exists refunded_at timestamptz;

-- Welcome email: when an address is confirmed, call the emails function. Google (and Apple)
-- accounts are created already confirmed, so a new account that arrives confirmed counts too (#177).
create extension if not exists pg_net;
create or replace function private.welcome_on_confirm() returns trigger
language plpgsql security definer set search_path = public, private as $$
declare url text; secret text;
begin
  if new.email_confirmed_at is not null and (tg_op = 'INSERT' or old.email_confirmed_at is null) then
    select value into url from private.config where key = 'emails_url';
    select value into secret from private.config where key = 'hook_secret';
    -- never let the email block confirming an address
    begin
      if url is not null then
        perform net.http_post(url, jsonb_build_object('kind','welcome','user_id',new.id),
          '{}'::jsonb, jsonb_build_object('Content-Type','application/json','x-rafiq-hook',secret));
      end if;
    exception when others then raise warning 'welcome email not queued for %: %', new.id, sqlerrm;
    end;
  end if;
  return new;
end $$;
drop trigger if exists welcome_on_confirm on auth.users;
create trigger welcome_on_confirm after update of email_confirmed_at on auth.users
  for each row execute function private.welcome_on_confirm();
-- after billing_new_user (triggers fire in name order), so the billing row is there; the email
-- itself goes out after the sign-up commits (pg_net), and the function sends it only once
drop trigger if exists welcome_on_signup on auth.users;
create trigger welcome_on_signup after insert on auth.users
  for each row when (new.email_confirmed_at is not null) execute function private.welcome_on_confirm();

-- Free-week reminder emails: once a day at 09:00 UTC.
create extension if not exists pg_cron;
create or replace function private.run_trial_reminders() returns void
language plpgsql security definer set search_path = public, private as $$
declare url text; secret text;
begin
  select value into url from private.config where key = 'emails_url';
  select value into secret from private.config where key = 'hook_secret';
  if url is not null then
    perform net.http_post(url, jsonb_build_object('kind','trial_reminders'),
      '{}'::jsonb, jsonb_build_object('Content-Type','application/json','x-rafiq-hook',secret));
  end if;
end $$;
select cron.unschedule(jobid) from cron.job where jobname = 'rafiq-trial-reminders';
select cron.schedule('rafiq-trial-reminders', '0 9 * * *', 'select private.run_trial_reminders()');

-- Delete my account: removes every row that belongs to the account, in every
-- public table with a user_id (so tables added later are covered too). Only
-- the server can run it; the account itself is then deleted by the function.
create or replace function public.delete_user_data(uid uuid) returns void
language plpgsql security definer set search_path = public as $$
declare t text;
begin
  for t in select table_name from information_schema.columns
           where table_schema = 'public' and column_name = 'user_id' loop
    execute format('delete from public.%I where user_id = $1', t) using uid;
  end loop;
end $$;
revoke all on function public.delete_user_data(uuid) from public, anon, authenticated;
grant execute on function public.delete_user_data(uuid) to service_role;

-- Report a problem / contact support: every message is kept here (for the admin
-- page, #29) as well as emailed to support@. Only the server reads or writes it.
create table if not exists public.reports (
  id bigserial primary key,
  created_at timestamptz not null default now(),
  user_id uuid references auth.users(id) on delete set null,
  email text,
  kind text not null,
  message text not null,
  page text,
  context text,
  user_agent text
);
alter table public.reports enable row level security;
create index if not exists reports_recent on public.reports (created_at desc);

-- FSRS memory state per reviewed item (stability, difficulty, state, reps, lapses,
-- last review), written by progress.js. box and due stay as before.
alter table public.item_progress add column if not exists fsrs jsonb;

-- The AI tutor (supabase/functions/tutor, #127): one row per question, for the daily
-- limit, the cost per learner, and checking a sample of answers. Only the server reads or writes it.
create table if not exists public.tutor_usage (
  id bigserial primary key,
  created_at timestamptz not null default now(),
  user_id uuid not null references auth.users(id) on delete cascade,
  mode text not null,                 -- chat | why
  model text not null,
  input_tokens int not null default 0,
  output_tokens int not null default 0,
  cache_read_tokens int not null default 0,
  cache_write_tokens int not null default 0,
  question text,
  answer text
);
alter table public.tutor_usage enable row level security;
create index if not exists tutor_usage_user_day on public.tutor_usage (user_id, created_at desc);

-- Where learners drop off (#26), worked out from what the app already saves, so
-- nothing new is tracked: 'p:<unit>|<step>' rows are lessons finished, and
-- 's:<YYYY-MM-DD>' rows are the days someone studied (UTC, like the account's
-- join date). One row per account here; private.funnel() adds them up by the
-- week people joined. Server only. In the SQL editor: select * from private.funnel();
create or replace view private.funnel_people as
select u.id as user_id,
  u.created_at::date as joined,
  u.email_confirmed_at is not null as confirmed,
  exists (select 1 from public.item_progress p where p.user_id = u.id
          and p.item_id like 'p:%' and p.item_id not like '%|placed') as first_lesson,
  exists (select 1 from public.item_progress p where p.user_id = u.id
          and p.item_id = 's:' || to_char(u.created_at::date + 1, 'YYYY-MM-DD')) as back_next_day,
  exists (select 1 from public.item_progress p where p.user_id = u.id and p.item_id like 's:%'
          and p.item_id >= 's:' || to_char(u.created_at::date + 7, 'YYYY-MM-DD')) as back_after_week,
  b.stripe_subscription_id is not null as chose_plan,      -- went through checkout (card given)
  coalesce(b.status = 'active' and not b.cancel_at_period_end, false) as paying,   -- cancelled plans run to the period's end, but aren't counted (#191)
  -- where they first came from (#186): a link's utm_source, the site that linked, or 'direct'; saved at sign-up
  coalesce(nullif(u.raw_user_meta_data->'source'->>'src', ''), 'unknown') as source,
  nullif(u.raw_user_meta_data->'source'->>'campaign', '') as campaign,
  -- the landing page's taster (#207), noted with the source: 'done', 'started', or 'no'
  coalesce(nullif(u.raw_user_meta_data->'source'->>'taster', ''), 'no') as taster
from auth.users u left join public.billing b on b.user_id = u.id
where coalesce(u.raw_app_meta_data->>'admin', '') <> 'true';   -- the Rafiq team's own accounts aren't counted (#191)

-- "Back the next day" only counts people who joined at least a day ago, and "back after
-- a week" people who joined at least a week ago, so a new week doesn't look like a drop.
create or replace function private.funnel() returns table (
  week_of date, joined bigint, confirmed bigint, first_lesson bigint,
  could_be_back_next_day bigint, back_next_day bigint,
  could_be_back_after_week bigint, back_after_week bigint,
  chose_plan bigint, paying bigint)
language sql stable security definer set search_path = private, public as $$
  select date_trunc('week', f.joined)::date,
    count(*), count(*) filter (where f.confirmed), count(*) filter (where f.first_lesson),
    count(*) filter (where f.joined <= current_date - 1), count(*) filter (where f.back_next_day),
    count(*) filter (where f.joined <= current_date - 7), count(*) filter (where f.back_after_week),
    count(*) filter (where f.chose_plan), count(*) filter (where f.paying)
  from private.funnel_people f
  group by 1 order by 1 desc
$$;
revoke all on function private.funnel() from public, anon, authenticated;

-- The same steps by where people came from (#186), for people who joined in the last N days:
-- which post or ad brings people who sign up, study and pay. select * from private.funnel_by_source(30);
create or replace function private.funnel_by_source(days int default 30) returns table (
  source text, campaign text, joined bigint, first_lesson bigint, back_next_day bigint, chose_plan bigint, paying bigint)
language sql stable security definer set search_path = private, public as $$
  select f.source, f.campaign, count(*), count(*) filter (where f.first_lesson), count(*) filter (where f.back_next_day),
    count(*) filter (where f.chose_plan), count(*) filter (where f.paying)
  from private.funnel_people f where f.joined > current_date - days
  group by 1, 2 order by 3 desc, 1
$$;
revoke all on function private.funnel_by_source(int) from public, anon, authenticated;

-- The same steps by whether people did the landing page's taster first (#207), for people who
-- joined in the last N days. select * from private.funnel_by_taster(30);
create or replace function private.funnel_by_taster(days int default 30) returns table (
  taster text, joined bigint, first_lesson bigint, back_next_day bigint, chose_plan bigint, paying bigint)
language sql stable security definer set search_path = private, public as $$
  select f.taster, count(*), count(*) filter (where f.first_lesson), count(*) filter (where f.back_next_day),
    count(*) filter (where f.chose_plan), count(*) filter (where f.paying)
  from private.funnel_people f where f.joined > current_date - days
  group by 1 order by 2 desc, 1
$$;
revoke all on function private.funnel_by_taster(int) from public, anon, authenticated;

-- For the owner dashboard (admin-stats, #189): the service key can call these through the API;
-- learners (anon, authenticated) can't. The function itself checks the caller is an admin.
create or replace function public.admin_funnel_by_source(days int default 7) returns table (
  source text, campaign text, joined bigint, first_lesson bigint, back_next_day bigint, chose_plan bigint, paying bigint)
language sql stable security definer set search_path = private, public as $$ select * from private.funnel_by_source(days) $$;
create or replace function public.admin_account_count() returns bigint
language sql stable security definer set search_path = public as $$
  select count(*) from auth.users where coalesce(raw_app_meta_data->>'admin', '') <> 'true' $$;
revoke all on function public.admin_funnel_by_source(int) from public, anon, authenticated;
revoke all on function public.admin_account_count() from public, anon, authenticated;
grant execute on function public.admin_funnel_by_source(int) to service_role;
grant execute on function public.admin_account_count() to service_role;


-- Taps on the way to an account (#225): how many opened the sign-up form from "Start your free week",
-- pressed Create account, or pressed Continue with Google, per day. Only the step and the day are kept,
-- nothing about who. login.html calls public.tap(step); the owner dashboard reads public.admin_taps(days).
create table if not exists private.taps (day date not null, step text not null, n int not null default 0, primary key (day, step));
create or replace function public.tap(step text) returns void
language sql volatile security definer set search_path = private as $$
  insert into private.taps (day, step, n) select current_date, tap.step, 1 where tap.step in ('signup_page', 'create', 'google')
  on conflict (day, step) do update set n = taps.n + 1
$$;
revoke all on function public.tap(text) from public;
grant execute on function public.tap(text) to anon, authenticated;
create or replace function public.admin_taps(days int default 7) returns table (step text, n bigint)
language sql stable security definer set search_path = private as $$
  select t.step, sum(t.n) from private.taps t where t.day > current_date - days group by 1
$$;
revoke all on function public.admin_taps(int) from public, anon, authenticated;
grant execute on function public.admin_taps(int) to service_role;
