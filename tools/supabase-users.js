/* supabase-users.js — list recent accounts, or delete chosen ones (Management API,
   secret SUPABASE_ACCESS_TOKEN). Run by the "Supabase users" GitHub Action.
   The repo is public, so Action logs are public: emails are always masked.

     node tools/supabase-users.js list [days]      accounts created in the last N days (default 3)
     node tools/supabase-users.js billing-test     billing rows with Stripe details (read only)
     node tools/supabase-users.js billing-check    each billing row next to what Stripe itself says (needs STRIPE_SECRET_KEY; read only)
     node tools/supabase-users.js billing-clear-test CLEAR-TEST-BILLING   empty them, when going live (#70)
     node tools/supabase-users.js active [days]    how many people studied each day, last N days (default 14; read only)
     node tools/supabase-users.js sources [days]   where people who joined in the last N days came from (default 30; read only)
     node tools/supabase-users.js visits [days]    website visits from Cloudflare Web Analytics: by day, referrer, country, page, device
                                                   (default 7; needs CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID; read only)
     node tools/supabase-users.js make-admin id    let this account open the owner dashboard (admin.html)
     node tools/supabase-users.js delete id1,id2   delete these accounts (max 5) and their rows
     node tools/supabase-users.js reset-preview    who a beta reset would wipe (changes nothing)
     node tools/supabase-users.js reset RESET-BETA wipe progress + onboarding answers for them
     node tools/supabase-users.js signout SIGN-OUT-ALL  end every session on every device
                                                   (with SIGN_IN_AGAIN_BEFORE in auth.js)

   The beta reset keeps accounts that were created or onboarded today (UK time):
   they've already seen the current app. For everyone else it deletes their rows
   in every table with a user_id (progress, profile = onboarding answers, …)
   except 'settings', whose migrated_v2 flag stops old browser data re-importing. */
const REF = 'gaajfahtrbdybjuunfhe';
const TOKEN = process.env.SUPABASE_ACCESS_TOKEN;
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/;

async function sql(query) {
  const r = await fetch(`https://api.supabase.com/v1/projects/${REF}/database/query`, {
    method: 'POST', headers: { Authorization: `Bearer ${TOKEN}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ query }) });
  const t = await r.text();
  if (!r.ok) { console.error(`query failed: ${r.status} ${t.slice(0, 300)}`); process.exit(1); }
  return JSON.parse(t);
}
// yo***7+te***@gm***.com
const mask = e => { const [u, d = ''] = String(e || '').split('@'); const [dn, ...tld] = d.split('.');
  const m = s => s.length <= 2 ? s[0] + '*' : s.slice(0, 2) + '***' + s.slice(-1);
  return u.split('+').map(m).join('+') + '@' + m(dn || '') + (tld.length ? '.' + tld.join('.') : ''); };

// public tables with a user_id column (progress etc.), so a deleted account leaves nothing behind
async function userTables() {
  return (await sql(`select table_name from information_schema.columns
                     where table_schema='public' and column_name='user_id'`)).map(r => r.table_name);
}

(async () => {
  if (!TOKEN) { console.error('SUPABASE_ACCESS_TOKEN is not set'); process.exit(1); }
  const [cmd, arg] = process.argv.slice(2);
  if (cmd === 'list') {
    const days = Math.max(1, Math.min(60, parseInt(arg, 10) || 3));
    const tables = await userTables();
    const rows = await sql(`select id, email, created_at, email_confirmed_at, last_sign_in_at from auth.users
                            where created_at > now() - interval '${days} days' order by created_at`);
    const total = (await sql('select count(*)::int as n from auth.users'))[0].n;
    console.log(`${total} accounts in total; ${rows.length} created in the last ${days} day(s):`);
    for (const u of rows) {
      let n = 0;
      for (const t of tables) n += (await sql(`select count(*)::int as n from public."${t}" where user_id='${u.id}'`))[0].n;
      console.log(`${u.id}  ${mask(u.email)}  created ${u.created_at.slice(0, 16)}  ` +
                  `confirmed ${u.email_confirmed_at ? 'yes' : 'no'}  last sign-in ${(u.last_sign_in_at || '—').slice(0, 16)}  rows ${n}`);
    }
    return;
  }
  if (cmd === 'active') {
    // who's actually studying: an 's:<YYYY-MM-DD>' progress row is a day someone finished a lesson step,
    // a review or a scene (UTC dates, written by the app). Counts only, plus masked emails.
    const days = Math.max(1, Math.min(60, parseInt(arg, 10) || 14));
    const total = (await sql('select count(*)::int as n from auth.users'))[0].n;
    const perDay = await sql(`select substr(item_id, 3) as day, count(distinct user_id)::int as n from public.item_progress
                              where item_id like 's:%' and substr(item_id, 3) >= to_char(current_date - ${days - 1}, 'YYYY-MM-DD')
                              group by 1 order by 1`);
    const within = async d => (await sql(`select count(distinct user_id)::int as n from public.item_progress where item_id like 's:%'
                              and substr(item_id, 3) >= to_char(current_date - ${d - 1}, 'YYYY-MM-DD')`))[0].n;
    const signedIn = (await sql(`select count(*)::int as n from auth.users where last_sign_in_at > now() - interval '7 days'`))[0].n;
    console.log(`${total} accounts. Studied today: ${await within(1)} · last 7 days: ${await within(7)} · last 30 days: ${await within(30)}` +
                ` · signed in during the last 7 days: ${signedIn}`);
    console.log(`\nPeople who studied, each day (UTC), last ${days} days:`);
    const n = Object.fromEntries(perDay.map(r => [r.day, r.n]));
    for (let i = days - 1; i >= 0; i--) { const d = new Date(Date.now() - i * 864e5).toISOString().slice(0, 10); console.log(`${d}  ${n[d] || 0}`); }
    const people = await sql(`select u.email, count(*)::int as days, max(substr(p.item_id, 3)) as last, min(u.created_at)::date::text as joined
                              from public.item_progress p join auth.users u on u.id = p.user_id
                              where p.item_id like 's:%' and substr(p.item_id, 3) >= to_char(current_date - ${days - 1}, 'YYYY-MM-DD')
                              group by u.email order by days desc, last desc`);
    console.log(`\n${people.length} people studied in the last ${days} days:`);
    people.forEach(p => console.log(`${mask(p.email)}  studied on ${p.days} day(s), last ${p.last}, joined ${p.joined}`));
    return;
  }
  if (cmd === 'sources') {
    // which post or ad brings people who sign up, study and pay (#186): private.funnel_by_source in backend.sql
    const days = Math.max(1, Math.min(365, parseInt(arg, 10) || 30));
    const rows = await sql(`select * from private.funnel_by_source(${days})`);
    console.log(`People who joined in the last ${days} days, by where they first came from:`);
    console.log('source (campaign)                     joined  1st lesson  next day  chose plan  paying');
    for (const r of rows) console.log(`${(r.source + (r.campaign ? ` (${r.campaign})` : '')).slice(0, 36).padEnd(38)}${String(r.joined).padStart(6)}` +
      `${String(r.first_lesson).padStart(12)}${String(r.back_next_day).padStart(10)}${String(r.chose_plan).padStart(12)}${String(r.paying).padStart(8)}`);
    console.log("\n'unknown' = joined before this was tracked (2 Oct 2026). Tag links: rafiq-arabic.com/?utm_source=tiktok&utm_campaign=meet-rafiq");
    // and by whether they did the landing page's taster first (#207)
    const t = await sql(`select * from private.funnel_by_taster(${days})`);
    console.log('\nBy the landing page taster (done / started / no):');
    console.log('taster      joined  1st lesson  next day  chose plan  paying');
    for (const r of t) console.log(`${r.taster.padEnd(10)}${String(r.joined).padStart(8)}${String(r.first_lesson).padStart(12)}${String(r.back_next_day).padStart(10)}` +
      `${String(r.chose_plan).padStart(12)}${String(r.paying).padStart(8)}`);
    return;
  }
  if (cmd === 'visits') {
    // the same numbers the owner dashboard shows (#189): Cloudflare's GraphQL API, Web Analytics (RUM) page loads
    const days = Math.max(1, Math.min(30, parseInt(arg, 10) || 7));
    const CF = process.env.CLOUDFLARE_API_TOKEN, ACC = process.env.CLOUDFLARE_ACCOUNT_ID;
    if (!CF || !ACC) { console.error('CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID are needed (GitHub secrets)'); process.exit(1); }
    const by = d => `rumPageloadEventsAdaptiveGroups(limit: 15, filter: $f, orderBy: [sum_visits_DESC]) { count sum { visits } dimensions { ${d} } }`;
    const query = `query($acc: string, $f: AccountRumPageloadEventsAdaptiveGroupsFilter_InputObject) { viewer { accounts(filter: {accountTag: $acc}) {
      total: rumPageloadEventsAdaptiveGroups(limit: 1, filter: $f) { count sum { visits } }
      days: rumPageloadEventsAdaptiveGroups(limit: 31, filter: $f, orderBy: [date_ASC]) { count sum { visits } dimensions { date } }
      refs: ${by('refererHost')} countries: ${by('countryName')} devices: ${by('deviceType')}
      paths: rumPageloadEventsAdaptiveGroups(limit: 15, filter: $f, orderBy: [count_DESC]) { count sum { visits } dimensions { requestPath } } } } }`;
    const f = { datetime_geq: new Date(Date.now() - days * 864e5).toISOString(), datetime_leq: new Date().toISOString() };
    const r = await fetch('https://api.cloudflare.com/client/v4/graphql', { method: 'POST',
      headers: { Authorization: `Bearer ${CF}`, 'Content-Type': 'application/json' }, body: JSON.stringify({ query, variables: { acc: ACC, f } }) });
    const j = await r.json();
    if (!r.ok || j.errors) { console.error('Cloudflare:', r.status, JSON.stringify(j.errors || j).slice(0, 500)); process.exit(1); }
    const a = j.data.viewer.accounts[0], t = a.total[0] || { count: 0, sum: { visits: 0 } };
    console.log(`Last ${days} days: ${t.sum.visits} visits, ${t.count} page views\n`);
    console.log('Per day:'); a.days.forEach(x => console.log(`  ${x.dimensions.date}  ${String(x.sum.visits).padStart(4)} visits  ${String(x.count).padStart(4)} views`));
    for (const [k, name, d] of [['refs', 'Where they came from', 'refererHost'], ['countries', 'Countries', 'countryName'], ['paths', 'Pages', 'requestPath'], ['devices', 'Devices', 'deviceType']]) {
      // a page reached from another page is part of the same visit, so pages are counted by page views (a visit counts only where it starts)
      console.log(`\n${name}${k === 'paths' ? ' (page views)' : ''}:`);
      a[k].forEach(x => console.log(`  ${String(k === 'paths' ? x.count : x.sum.visits).padStart(4)}  ${x.dimensions[d] || '(direct / none)'}`));
    }
    return;
  }
  if (cmd === 'make-admin') {
    if (!UUID.test(arg || '')) { console.error('give the account id (from the list command)'); process.exit(1); }
    const r = await sql(`update auth.users set raw_app_meta_data = coalesce(raw_app_meta_data, '{}'::jsonb) || '{"admin": true}'
                         where id = '${arg}' returning email`);
    console.log(r.length ? `${mask(r[0].email)} can now open admin.html (sign out and in again)` : 'no such account');
    return;
  }
  if (cmd === 'billing-check') {
    // Rafiq's copy of each plan next to Stripe's own record (#191): does a cancelled plan show as cancelled?
    const KEY = process.env.STRIPE_SECRET_KEY;
    if (!KEY) { console.error('STRIPE_SECRET_KEY is needed'); process.exit(1); }
    const day = t => t ? new Date(typeof t === 'number' ? t * 1000 : t).toISOString().slice(0, 16).replace('T', ' ') : '—';   // UTC, to the minute
    const rows = await sql(`select b.user_id, u.email, b.plan, b.status, b.cancel_at_period_end, b.current_period_end, b.updated_at,
                              b.stripe_customer_id, b.stripe_subscription_id from public.billing b join auth.users u on u.id = b.user_id
                            where b.stripe_customer_id is not null order by u.email`);
    for (const r of rows) {
      console.log(`\n${mask(r.email)}`);
      console.log(`  Rafiq:  plan ${r.plan || '—'}, status ${r.status || '—'}, cancels at period end ${r.cancel_at_period_end ? 'yes' : 'no'}, ` +
                  `period ends ${day(r.current_period_end)}, last updated ${day(r.updated_at)}`);
      const res = await fetch(`https://api.stripe.com/v1/subscriptions?customer=${r.stripe_customer_id}&status=all&limit=10`, { headers: { Authorization: `Bearer ${KEY}` } });
      const j = await res.json();
      if (!res.ok) { console.log(`  Stripe: couldn't read (${j.error && j.error.message})`); continue; }
      if (!j.data.length) console.log('  Stripe: no subscriptions');
      for (const x of j.data) {
        const it = x.items.data[0] || {};
        console.log(`  Stripe: ${x.id === r.stripe_subscription_id ? '(this one) ' : ''}${(it.price && it.price.lookup_key) || '?'}, status ${x.status}` +
                    `${x.cancel_at_period_end || x.cancel_at ? `, set to cancel on ${day(x.cancel_at || it.current_period_end || x.current_period_end)}` : ''}` +
                    `${x.canceled_at ? `, cancelled ${day(x.canceled_at)}` : ''}${x.ended_at ? `, ended ${day(x.ended_at)}` : ''}${x.trial_end ? `, trial ends ${day(x.trial_end)}` : ''}`);
      }
    }
    return;
  }
  if (cmd === 'billing-test' || cmd === 'billing-clear-test') {
    // Going live (#70): billing rows still carrying Stripe *test-mode* details (customer, subscription,
    // plan) would point the live checkout at customers that don't exist there. billing-test lists them;
    // billing-clear-test CLEAR-TEST-BILLING empties those fields. The free-week dates are kept.
    const rows = await sql(`select b.user_id, u.email, b.plan, b.status, b.stripe_customer_id is not null as has_customer
                            from public.billing b join auth.users u on u.id = b.user_id
                            where b.stripe_customer_id is not null or b.stripe_subscription_id is not null or b.plan is not null or b.status is not null`);
    console.log(`${rows.length} billing row(s) with Stripe details:`);
    rows.forEach(r => console.log(`${r.user_id}  ${mask(r.email)}  plan ${r.plan || '—'}  status ${r.status || '—'}  customer ${r.has_customer ? 'yes' : 'no'}`));
    if (cmd === 'billing-test') return;
    if (arg !== 'CLEAR-TEST-BILLING') { console.error('to clear them, the arg must be CLEAR-TEST-BILLING'); process.exit(1); }
    const r = await sql(`with d as (update public.billing set plan = null, status = null, interval = null, current_period_end = null,
                           cancel_at_period_end = false, stripe_customer_id = null, stripe_subscription_id = null, updated_at = now()
                         where stripe_customer_id is not null or stripe_subscription_id is not null or plan is not null or status is not null
                         returning 1) select count(*)::int as n from d`);
    console.log(`${r[0].n} billing row(s) cleared; free-week dates kept`);
    return;
  }
  if (cmd === 'delete') {
    const ids = String(arg || '').split(',').map(s => s.trim()).filter(Boolean);
    if (!ids.length || ids.length > 5 || !ids.every(i => UUID.test(i))) { console.error('give 1-5 account ids (uuids), comma-separated'); process.exit(1); }
    const list = ids.map(i => `'${i}'`).join(',');
    const found = await sql(`select id, email from auth.users where id in (${list})`);
    if (found.length !== ids.length) { console.error(`only ${found.length} of ${ids.length} ids exist; nothing deleted`); process.exit(1); }
    for (const t of await userTables()) {
      const r = await sql(`with d as (delete from public."${t}" where user_id in (${list}) returning 1) select count(*)::int as n from d`);
      if (r[0].n) console.log(`${t}: ${r[0].n} rows deleted`);
    }
    await sql(`delete from auth.users where id in (${list})`);
    found.forEach(u => console.log(`deleted ${u.id}  ${mask(u.email)}`));
    return;
  }
  if (cmd === 'reset-preview' || cmd === 'reset') {
    if (cmd === 'reset' && arg !== 'RESET-BETA') { console.error('to wipe, the second input must be RESET-BETA'); process.exit(1); }
    const tables = (await userTables()).filter(t => t !== 'settings');
    const today = `(date_trunc('day', now() at time zone 'Europe/London') at time zone 'Europe/London')`;
    const pcols = (await sql(`select column_name from information_schema.columns
                              where table_schema='public' and table_name='profiles'`)).map(r => r.column_name);
    const pAt = pcols.includes('created_at') ? 'coalesce(p.created_at, p.updated_at)' : 'p.updated_at';
    const rows = await sql(`select u.id, u.email, u.created_at, ${pAt} as onboarded_at, p.onboarded,
                              (u.created_at >= ${today} or coalesce(${pAt} >= ${today}, false)) as keep
                            from auth.users u left join public.profiles p on p.user_id = u.id order by u.created_at`);
    console.log(`Today (UK) starts ${(await sql(`select ${today} as t`))[0].t}. Tables wiped: ${tables.join(', ')}`);
    const wipe = [];
    for (const u of rows) {
      let n = 0;
      for (const t of tables) n += (await sql(`select count(*)::int as n from public."${t}" where user_id='${u.id}'`))[0].n;
      console.log(`${u.keep ? 'KEEP ' : 'RESET'}  ${u.id}  ${mask(u.email)}  created ${String(u.created_at).slice(0, 16)}  ` +
                  `onboarded ${u.onboarded_at ? String(u.onboarded_at).slice(0, 16) : 'no'}  rows ${n}`);
      if (!u.keep) wipe.push(u);
    }
    console.log(`${wipe.length} to reset, ${rows.length - wipe.length} kept`);
    if (cmd === 'reset-preview' || !wipe.length) return;
    const list = wipe.map(u => `'${u.id}'`).join(',');
    for (const t of tables) {
      const r = await sql(`with d as (delete from public."${t}" where user_id in (${list}) returning 1) select count(*)::int as n from d`);
      console.log(`${t}: ${r[0].n} rows deleted`);
    }
    console.log('reset done');
    return;
  }
  if (cmd === 'signout') {
    if (arg !== 'SIGN-OUT-ALL') { console.error('to sign everyone out, the second input must be SIGN-OUT-ALL'); process.exit(1); }
    const r = await sql(`with d as (delete from auth.sessions returning 1) select count(*)::int as n from d`);
    const t = await sql(`with d as (delete from auth.refresh_tokens returning 1) select count(*)::int as n from d`);
    console.log(`${r[0].n} sessions and ${t[0].n} refresh tokens ended; everyone signs in again`);
    return;
  }
  console.error('use: list [days] | active [days] | billing-test | billing-clear-test CLEAR-TEST-BILLING | delete id1,id2 | reset-preview | reset RESET-BETA | signout SIGN-OUT-ALL'); process.exit(1);
})();
