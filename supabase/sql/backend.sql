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

-- The free week never ends before a week after launch (10 Oct 2026), so
-- everyone who joined before launch gets a full week of the paid app.
create or replace function private.trial_end_for(joined timestamptz) returns timestamptz
language sql immutable as $$
  select greatest(joined + interval '7 days', timestamptz '2026-10-17 23:00:00+00')
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

-- Welcome email: when an address is confirmed, call the emails function.
create extension if not exists pg_net;
create or replace function private.welcome_on_confirm() returns trigger
language plpgsql security definer set search_path = public, private as $$
declare url text; secret text;
begin
  if old.email_confirmed_at is null and new.email_confirmed_at is not null then
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
