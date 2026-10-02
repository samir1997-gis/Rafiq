/* backend-deploy.js — set up the server side in Supabase (Management API).
   Run by the "Backend deploy" GitHub Action, before it deploys supabase/functions.
   Needs SUPABASE_ACCESS_TOKEN and RESEND_API_KEY. Safe to run again.

   1. applies supabase/sql/backend.sql (billing table, free week, triggers, daily job)
   2. stores the function secrets: RESEND_API_KEY and a fresh HOOK_SECRET, the
      Quran Foundation client (QF_CLIENT_ID, QF_CLIENT_SECRET) and the Claude API key
      for the AI tutor (ANTHROPIC_API_KEY) when they're given
   3. tells the database where the emails function is, and the same HOOK_SECRET
   Secrets are never printed. */
const fs = require('fs'), path = require('path'), crypto = require('crypto');
const REF = 'gaajfahtrbdybjuunfhe';
const API = `https://api.supabase.com/v1/projects/${REF}`;
const TOKEN = process.env.SUPABASE_ACCESS_TOKEN;

async function call(method, url, body) {
  const r = await fetch(API + url, { method, headers: { Authorization: `Bearer ${TOKEN}`, 'Content-Type': 'application/json' },
                                     body: body ? JSON.stringify(body) : undefined });
  const t = await r.text();
  if (!r.ok) { console.error(`${method} ${url} failed: ${r.status} ${t.slice(0, 400)}`); process.exit(1); }
  return t ? JSON.parse(t) : {};
}
const sql = query => call('POST', '/database/query', { query });
const lit = s => `'${String(s).replace(/'/g, "''")}'`;

(async () => {
  if (!TOKEN) { console.error('SUPABASE_ACCESS_TOKEN is not set'); process.exit(1); }
  if (!process.env.RESEND_API_KEY) { console.error('RESEND_API_KEY is not set'); process.exit(1); }
  await sql(fs.readFileSync(path.join(__dirname, '..', 'supabase/sql/backend.sql'), 'utf8'));
  console.log('database: backend.sql applied');

  const hook = crypto.randomBytes(24).toString('hex');
  await call('POST', '/secrets', [{ name: 'RESEND_API_KEY', value: process.env.RESEND_API_KEY }, { name: 'HOOK_SECRET', value: hook }]);
  await sql(`insert into private.config (key, value) values
               ('emails_url', ${lit(`https://${REF}.supabase.co/functions/v1/emails`)}), ('hook_secret', ${lit(hook)})
             on conflict (key) do update set value = excluded.value`);
  console.log('secrets: RESEND_API_KEY, HOOK_SECRET set; database knows the emails function');
  if (process.env.QF_CLIENT_ID && process.env.QF_CLIENT_SECRET) {
    await call('POST', '/secrets', [{ name: 'QF_CLIENT_ID', value: process.env.QF_CLIENT_ID },
                                    { name: 'QF_CLIENT_SECRET', value: process.env.QF_CLIENT_SECRET }]);
    console.log('secrets: Quran Foundation client set');
    if (process.env.QF_RECITATION_ID) {                    // the reciter: a GitHub Actions variable (default 12, al-Husary Muallim)
      await call('POST', '/secrets', [{ name: 'QF_RECITATION_ID', value: process.env.QF_RECITATION_ID }]);
      console.log('secrets: reciter set to recitation ' + process.env.QF_RECITATION_ID);
    }
  } else console.log('secrets: no Quran Foundation client yet (Quran parts stay read-along)');
  if (process.env.CLOUDFLARE_API_TOKEN && process.env.CLOUDFLARE_ACCOUNT_ID) {   // the owner dashboard's visits (#189)
    await call('POST', '/secrets', [{ name: 'CLOUDFLARE_API_TOKEN', value: process.env.CLOUDFLARE_API_TOKEN },
                                    { name: 'CLOUDFLARE_ACCOUNT_ID', value: process.env.CLOUDFLARE_ACCOUNT_ID }]);
    console.log('secrets: Cloudflare Web Analytics (read only) set');
  } else console.log('secrets: no Cloudflare token yet (the dashboard shows sign-ups only)');
  if (process.env.ANTHROPIC_API_KEY) {
    await call('POST', '/secrets', [{ name: 'ANTHROPIC_API_KEY', value: process.env.ANTHROPIC_API_KEY }]);
    console.log('secrets: Claude API key set (AI tutor)');
  } else console.log('secrets: no Claude API key yet (the AI tutor says it isn\'t ready)');

  const n = await sql(`select count(*)::int as n, count(*) filter (where trial_ends_at > now())::int as trial from public.billing`);
  console.log(`billing rows: ${n[0].n} (${n[0].trial} in their free week)`);
})();
