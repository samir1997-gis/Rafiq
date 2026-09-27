/* send-reminders.js — daily reminders (issue #31), by email (Resend) and web push.
   Run by the "Reminders" GitHub Action; needs SUPABASE_ACCESS_TOKEN and RESEND_API_KEY
   (both already used by the beta email). The repo is public, so Action logs are
   public: addresses are always masked, and a single account is chosen by id.

     node tools/send-reminders.js setup           create the reminders table, the unsubscribe
                                                  function and the push keys (safe to re-run;
                                                  the Action runs it whenever this file changes on main)
     node tools/send-reminders.js run             send what's due this hour (the hourly schedule)
     node tools/send-reminders.js preview         who 'run' would remind right now (sends nothing)
     node tools/send-reminders.js test <id>       send one account's reminder now, whatever the time

   Who gets one: people who turned reminders on in Settings, at the hour they chose
   in their own time zone (or up to two hours late, if a scheduled run was delayed),
   once a day, and only if today's goal isn't met yet. The message carries the
   streak and the number of reviews due, worked out the same way as on Home:
   a day counts when its 's:<date>' row exists, and days are UTC dates, as in path.js.

   Web push needs the web-push package (the Action installs it). Its keys are made
   by 'setup' and kept in Supabase: the public one is read by the site through
   vapid_public_key(), the private one only here, through the Management API. */
const fs = require('fs'), path = require('path'), crypto = require('crypto');
const REF = 'gaajfahtrbdybjuunfhe';
const TOKEN = process.env.SUPABASE_ACCESS_TOKEN, KEY = process.env.RESEND_API_KEY;
const FROM = 'Rafiq <hello@contact.rafiq-arabic.com>', REPLY_TO = 'feedback@rafiq-arabic.com';
const SITE = 'https://rafiq-arabic.com';
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/;
const LATE = 2;   // hours after the chosen time a missed reminder may still go out

async function sql(query) {
  const r = await fetch(`https://api.supabase.com/v1/projects/${REF}/database/query`, {
    method: 'POST', headers: { Authorization: `Bearer ${TOKEN}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ query }) });
  const t = await r.text();
  if (!r.ok) throw new Error(`query failed: ${r.status} ${t.slice(0, 300)}`);
  return JSON.parse(t);
}
const q = s => `'${String(s).replace(/'/g, "''")}'`;     // SQL string literal
const mask = e => { const [u, d = ''] = String(e || '').split('@'); const [dn, ...tld] = d.split('.');
  const m = s => s.length <= 2 ? s[0] + '*' : s.slice(0, 2) + '***' + s.slice(-1);
  return u.split('+').map(m).join('+') + '@' + m(dn || '') + (tld.length ? '.' + tld.join('.') : ''); };
const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

/* ---------- setup ---------- */
const SETUP = `
create table if not exists public.reminders (
  user_id    uuid primary key references auth.users(id) on delete cascade,
  enabled    boolean  not null default false,
  hour       smallint not null default 19 check (hour between 0 and 23),
  tz         text     not null default 'Europe/London',
  by_email   boolean  not null default true,
  push       jsonb,                                  -- the web push subscription of one device
  goal       smallint not null default 2,            -- steps a day, copied from Settings
  last_sent  date,                                   -- the local date of the last reminder (or of a check that found the goal met)
  unsub      uuid     not null default gen_random_uuid() unique,   -- for the email's unsubscribe link
  updated_at timestamptz not null default now()
);
alter table public.reminders enable row level security;
drop policy if exists "own reminders" on public.reminders;
create policy "own reminders" on public.reminders for all to authenticated
  using (auth.uid() = user_id) with check (auth.uid() = user_id);

create schema if not exists private;
revoke all on schema private from public, anon, authenticated;
create table if not exists private.keys (name text primary key, value text not null);

create or replace function public.vapid_public_key() returns text
  language sql stable security definer set search_path = '' as
  $$ select value from private.keys where name = 'vapid_public' $$;
grant execute on function public.vapid_public_key() to anon, authenticated;

-- the email's unsubscribe link: stops emails; notifications stay on if this person has them
create or replace function public.reminders_unsubscribe(token uuid) returns boolean
  language plpgsql security definer set search_path = '' as $$
  declare n int;
  begin
    update public.reminders set by_email = false, enabled = (push is not null), updated_at = now()
      where unsub = token;
    get diagnostics n = row_count;
    return n > 0;
  end $$;
grant execute on function public.reminders_unsubscribe(uuid) to anon, authenticated;`;

async function setup() {
  await sql(SETUP);
  const have = await sql(`select name from private.keys where name in ('vapid_public', 'vapid_private')`);
  if (have.length < 2) {
    const { publicKey, privateKey } = crypto.generateKeyPairSync('ec', { namedCurve: 'prime256v1' });
    const pub = publicKey.export({ format: 'jwk' }), prv = privateKey.export({ format: 'jwk' });
    const raw = Buffer.concat([Buffer.from([4]), Buffer.from(pub.x, 'base64url'), Buffer.from(pub.y, 'base64url')]);
    await sql(`delete from private.keys where name in ('vapid_public', 'vapid_private');
               insert into private.keys values ('vapid_public', ${q(raw.toString('base64url'))}), ('vapid_private', ${q(prv.d)});`);
    console.log('push keys created');
  }
  console.log('reminders are set up');
}

/* ---------- who gets a reminder ---------- */
const utcDay = (d = new Date()) => d.toISOString().slice(0, 10);
// the local date and hour in a time zone ('Europe/London' if it isn't one)
function localNow(tz, now = new Date()) {
  let f;
  try { f = new Intl.DateTimeFormat('en-CA', { timeZone: tz, year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', hourCycle: 'h23' }); }
  catch (_) { f = new Intl.DateTimeFormat('en-CA', { timeZone: 'Europe/London', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', hourCycle: 'h23' }); }
  const p = Object.fromEntries(f.formatToParts(now).map(x => [x.type, x.value]));
  return { date: `${p.year}-${p.month}-${p.day}`, hour: +p.hour };
}
// consecutive days back from today (or from yesterday, if today isn't done yet), as path.js does
function streak(days, today) {
  const set = new Set(days || []), d = new Date(today + 'T00:00:00Z');
  if (!set.has(utcDay(d))) d.setUTCDate(d.getUTCDate() - 1);
  let n = 0;
  while (set.has(utcDay(d))) { n++; d.setUTCDate(d.getUTCDate() - 1); }
  return n;
}
/* 'send' | 'done' (goal met: mark the day, send nothing) | null (not now) */
function decide(row, now = new Date()) {
  const l = localNow(row.tz, now);
  if (row.last_sent && String(row.last_sent).slice(0, 10) === l.date) return null;
  if (l.hour < row.hour || l.hour > row.hour + LATE) return null;
  return (row.done_today || 0) >= (row.goal || 2) ? 'done' : 'send';
}
function message(row, today) {
  const s = streak(row.days, today), due = +row.due || 0;
  const title = s > 1 ? `Keep your ${s}-day streak going` : 'A few minutes of Arabic today';
  const line = s > 1 ? `You're on a ${s}-day streak. A few minutes today keeps it going.`
                     : 'Your next step is ready. A few minutes is enough.';
  const reviews = due > 0 ? `${due} ${due === 1 ? 'word or sentence is' : 'words and sentences are'} due for review.` : '';
  return { title, line, reviews, streak: s, due };
}

const rows = where => sql(rowsQuery(where, utcDay()));
function rowsQuery(where, today) {
  return (`
    select r.user_id, r.hour, r.tz, r.by_email, r.push, r.goal, r.last_sent, r.unsub,
           u.email, u.raw_user_meta_data->>'name' as name,
           (select p.seen from public.item_progress p where p.user_id = r.user_id and p.item_id = ${q('s:' + today)}) as done_today,
           (select count(*) from public.item_progress p where p.user_id = r.user_id and p.box > 0 and p.due is not null
              and p.due::text <= ${q(today)} and (p.item_id like 'v:%' or p.item_id like 'd:%')) as due,
           (select array_agg(substr(p.item_id, 3)) from public.item_progress p where p.user_id = r.user_id
              and p.item_id like 's:%' and p.item_id >= ${q('s:' + utcDay(new Date(Date.now() - 400 * 864e5)))}) as days
    from public.reminders r join auth.users u on u.id = r.user_id
    where ${where}`);
}

/* ---------- sending ---------- */
const TEMPLATE = fs.readFileSync(path.join(__dirname, '..', 'supabase/email-templates/daily-reminder.html'), 'utf8')
  .replace(/^<!--[\s\S]*?-->\s*/, '');
const text = html => html.replace(/<br>/g, '\n').replace(/<\/(p|div|tr)>/g, '\n')
  .replace(/<a [^>]*href="(https[^"]+)"[^>]*>([^<]+)<\/a>/g, '$2: $1').replace(/<[^>]+>/g, '')
  .replace(/&amp;/g, '&').replace(/&rsquo;|’/g, "'").replace(/[ \t]+/g, ' ').replace(/\n\s*\n\s*/g, '\n\n').trim();

function render(row, m) {
  const name = (row.name || '').trim().split(/\s+/)[0];
  const unsub = `${SITE}/unsubscribe.html?t=${row.unsub}`;
  const html = TEMPLATE.replace('{{GREETING}}', esc(name ? `Assalamu alaykum ${name},` : 'Assalamu alaykum,'))
    .replace('{{LINE}}', esc(m.line)).replace('{{REVIEWS}}', m.reviews ? `<p style="margin:0 0 20px">${esc(m.reviews)}</p>` : '')
    .replace(/\{\{UNSUB\}\}/g, unsub);
  return { html, text: text(html), unsub };
}
async function email(row, m) {
  const { html, unsub } = render(row, m);
  const r = await fetch('https://api.resend.com/emails', { method: 'POST',
    headers: { Authorization: `Bearer ${KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ from: FROM, to: [row.email], reply_to: REPLY_TO, subject: m.title, html, text: text(html),
      headers: { 'List-Unsubscribe': `<${unsub}>` } }) });
  if (!r.ok) { const j = await r.json().catch(() => ({})); throw new Error(j.message || String(r.status)); }
}

let webpush = null;
async function pusher() {
  if (webpush !== null) return webpush;
  try { webpush = require('web-push'); } catch (_) { webpush = false; return false; }
  const k = await sql(`select name, value from private.keys where name in ('vapid_public', 'vapid_private')`);
  const v = Object.fromEntries(k.map(x => [x.name, x.value]));
  if (!v.vapid_public || !v.vapid_private) { webpush = false; return false; }
  webpush.setVapidDetails('mailto:feedback@rafiq-arabic.com', v.vapid_public, v.vapid_private);
  return webpush;
}
// true = sent; 'gone' = the subscription has expired (the browser dropped it)
async function push(row, m) {
  const wp = await pusher();
  if (!wp) throw new Error('web push is not available (web-push package or keys missing)');
  try {
    await wp.sendNotification(row.push, JSON.stringify({ title: m.title, body: m.reviews ? `${m.line} ${m.reviews}` : m.line, url: '/dashboard.html' }),
      { TTL: 4 * 3600, urgency: 'normal' });
    return true;
  } catch (e) {
    if (e.statusCode === 404 || e.statusCode === 410) return 'gone';
    throw e;
  }
}

async function remind(row, today, localDate, log) {
  const m = message(row, today), done = [];
  if (row.by_email && row.email) {
    try { await email(row, m); done.push('email'); } catch (e) { log(`email FAILED (${e.message})`); }
  }
  if (row.push) {
    try {
      const r = await push(row, m);
      if (r === 'gone') { await sql(`update public.reminders set push = null, enabled = by_email where user_id = ${q(row.user_id)}`); log('push subscription expired, removed'); }
      else done.push('push');
    } catch (e) { log(`push FAILED (${e.message})`); }
  }
  if (localDate) await sql(`update public.reminders set last_sent = ${q(localDate)} where user_id = ${q(row.user_id)}`);
  return done;
}

if (require.main === module) (async () => {
  const [cmd, arg] = process.argv.slice(2);
  if (cmd === 'self-test') return selfTest();
  if (!TOKEN) { console.error('SUPABASE_ACCESS_TOKEN is needed'); process.exit(1); }
  if (cmd === 'setup') return setup();
  if (!KEY) { console.error('RESEND_API_KEY is needed'); process.exit(1); }
  const today = utcDay(), now = new Date();

  if (cmd === 'test') {
    if (!UUID.test(arg || '')) { console.error('give one account id (uuid)'); process.exit(1); }
    const [row] = await rows(`r.user_id = ${q(arg)}`);
    if (!row) { console.error('that account has no reminder settings'); process.exit(1); }
    const done = await remind(row, today, null, s => console.log(`${row.user_id}  ${s}`));
    return console.log(`${row.user_id}  ${mask(row.email)}  sent: ${done.join(' + ') || 'nothing'}`);
  }
  if (cmd !== 'run' && cmd !== 'preview') { console.error('use: setup | run | preview | test <account-id>'); process.exit(1); }

  const all = await rows(`r.enabled and u.email_confirmed_at is not null`);
  let sent = 0, met = 0, failed = 0;
  for (const row of all) {
    const what = decide(row, now);
    if (!what) continue;
    const who = `${row.user_id}  ${mask(row.email)}`;
    const localDate = localNow(row.tz, now).date;
    if (what === 'done') {
      met++;
      if (cmd === 'run') await sql(`update public.reminders set last_sent = ${q(localDate)} where user_id = ${q(row.user_id)}`);
      console.log(`${who}  goal already met`);
      continue;
    }
    const via = [row.by_email && 'email', row.push && 'push'].filter(Boolean).join(' + ') || 'nothing';
    if (cmd === 'preview') { console.log(`would remind  ${who}  by ${via}  (${message(row, today).title})`); sent++; continue; }
    const done = await remind(row, today, localDate, s => console.log(`${who}  ${s}`));
    if (done.length) { sent++; console.log(`${who}  sent by ${done.join(' + ')}`); } else failed++;
    await new Promise(r => setTimeout(r, 600));   // Resend: 2 a second
  }
  console.log(`${all.length} with reminders on · ${sent} ${cmd === 'preview' ? 'due now' : 'reminded'} · ${met} had met their goal · ${failed} failed`);
  if (failed) process.exit(1);
})().catch(e => { console.error(e.message); process.exit(1); });

module.exports = { SETUP, rowsQuery, decide, message, streak, localNow, render };

/* node tools/send-reminders.js self-test — checks the timing and message rules, offline */
function selfTest() {
  const assert = require('assert');
  const at = iso => new Date(iso);
  // London in summer is UTC+1: 18:30 UTC is 19:30 there
  assert.deepStrictEqual(localNow('Europe/London', at('2026-09-27T18:30:00Z')), { date: '2026-09-27', hour: 19 });
  assert.deepStrictEqual(localNow('Not/AZone', at('2026-09-27T18:30:00Z')), { date: '2026-09-27', hour: 19 });
  const row = { tz: 'Europe/London', hour: 19, goal: 2, done_today: 0, last_sent: null };
  assert.strictEqual(decide(row, at('2026-09-27T17:59:00Z')), null);                  // 18:59 there: too early
  assert.strictEqual(decide(row, at('2026-09-27T18:05:00Z')), 'send');                // 19:05
  assert.strictEqual(decide(row, at('2026-09-27T20:10:00Z')), 'send');                // 21:10: a late run still sends
  assert.strictEqual(decide(row, at('2026-09-27T21:10:00Z')), null);                  // 22:10: too late
  assert.strictEqual(decide({ ...row, last_sent: '2026-09-27' }, at('2026-09-27T18:05:00Z')), null);   // once a day
  assert.strictEqual(decide({ ...row, done_today: 2 }, at('2026-09-27T18:05:00Z')), 'done');           // goal met
  assert.strictEqual(decide({ ...row, done_today: 1, goal: 1 }, at('2026-09-27T18:05:00Z')), 'done');
  assert.strictEqual(decide({ ...row, tz: 'Asia/Karachi' }, at('2026-09-27T14:05:00Z')), 'send');     // 19:05 in Karachi
  assert.strictEqual(streak(['2026-09-25', '2026-09-26'], '2026-09-27'), 2);         // today not done yet: counts from yesterday
  assert.strictEqual(streak(['2026-09-25', '2026-09-26', '2026-09-27'], '2026-09-27'), 3);
  assert.strictEqual(streak(['2026-09-24'], '2026-09-27'), 0);
  assert.strictEqual(streak(null, '2026-09-27'), 0);
  const m = message({ days: ['2026-09-25', '2026-09-26'], due: '12' }, '2026-09-27');
  assert.strictEqual(m.title, 'Keep your 2-day streak going');
  assert.strictEqual(m.reviews, '12 words and sentences are due for review.');
  assert.strictEqual(message({ days: [], due: 0 }, '2026-09-27').reviews, '');
  assert.strictEqual(message({ days: [], due: 1 }, '2026-09-27').reviews, '1 word or sentence is due for review.');
  console.log('self-test passed');
}
