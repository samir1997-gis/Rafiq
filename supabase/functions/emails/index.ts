// emails — called only by the database (x-rafiq-hook secret):
//   {kind:'welcome', user_id}   when an address is confirmed (trigger on auth.users)
//   {kind:'trial_reminders'}    daily at 09:00 UTC (pg_cron): "2 days left" and "last day"
// Each email is sent at most once per account (billing.*_sent_at).
import { admin, fromHook, sendEmail } from '../_shared/common.ts';
import { welcome, trialSoon, trialLast, text } from '../_shared/emails.ts';

const PAYING = ['active', 'trialing', 'past_due'];
const H = 3600_000;

async function account(id: string) {
  const { data } = await admin.auth.admin.getUserById(id);
  const u = data?.user;
  return u && u.email && u.email_confirmed_at ? { email: u.email, name: (u.user_metadata?.name as string) || null } : null;
}
async function send(to: string, m: { subject: string; html: string }) { await sendEmail(to, m.subject, m.html, text(m.html)); }

Deno.serve(async (req) => {
  if (req.method !== 'POST' || !fromHook(req)) return new Response('no', { status: 403 });
  const body = await req.json().catch(() => ({}));

  if (body.kind === 'welcome' && body.user_id) {
    const { data: b } = await admin.from('billing').select('*').eq('user_id', body.user_id).maybeSingle();
    if (!b || b.welcome_sent_at) return new Response('skip');
    const a = await account(body.user_id);
    if (!a) return new Response('skip');
    // mark first, so a retry can never send it twice
    await admin.from('billing').update({ welcome_sent_at: new Date().toISOString() }).eq('user_id', body.user_id);
    await send(a.email, welcome(a.name, new Date(b.trial_ends_at)));
    return new Response('sent');
  }

  if (body.kind === 'trial_reminders') {
    const now = Date.now(), iso = (ms: number) => new Date(ms).toISOString();
    const { data: rows } = await admin.from('billing').select('*')
      .gt('trial_ends_at', iso(now)).lte('trial_ends_at', iso(now + 48 * H));
    let n = 0;
    for (const b of rows || []) {
      if (b.plan && PAYING.includes(b.status)) continue;          // already subscribed
      const left = new Date(b.trial_ends_at).getTime() - now;
      const col = left <= 24 * H ? 'trial_last_sent_at' : 'trial_soon_sent_at';
      if (b[col]) continue;
      const a = await account(b.user_id);
      if (!a) continue;
      await admin.from('billing').update({ [col]: iso(now) }).eq('user_id', b.user_id);
      await send(a.email, left <= 24 * H ? trialLast(a.name) : trialSoon(a.name, new Date(b.trial_ends_at)));
      n++;
    }
    return new Response(`sent ${n}`);
  }
  return new Response('unknown', { status: 400 });
});
