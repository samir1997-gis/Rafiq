// store-webhook (#345): RevenueCat tells us about App Store and Google Play subscriptions; this keeps the account's
// billing row the same as Stripe's webhook does for the website, so every page reads the plan one way.
// RevenueCat → Project settings → Integrations → Webhooks: this function's URL, and as the Authorization header
// "Bearer <REVENUECAT_WEBHOOK_AUTH>" (the same value as the GitHub secret, set by tools/backend-deploy.js).
// No emails to the learner: Apple and Google send their own receipts and cancellation emails. The owner's
// alert (#312) goes to the Rafiq inbox for every new subscriber and cancellation, as for Stripe.
// Sandbox (test) purchases are ignored unless STORE_SANDBOX=1.
import { admin, sendEmail } from '../_shared/common.ts';
import { ownerAlert, text } from '../_shared/emails.ts';
import { fromEvent, live } from '../_shared/store.ts';

const AUTH = Deno.env.get('REVENUECAT_WEBHOOK_AUTH');
const OWNER = 'support@rafiq-arabic.com';
const same = (a: string, b: string) => { if (a.length !== b.length) return false; let d = 0; for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ b.charCodeAt(i); return d === 0; };

Deno.serve(async (req) => {
  if (!AUTH) return new Response('not ready', { status: 503 });
  if (!same(req.headers.get('authorization') || '', `Bearer ${AUTH}`)) return new Response('unauthorised', { status: 401 });
  const body = await req.json().catch(() => null);
  const e = body?.event;
  if (!e) return new Response('no event', { status: 400 });
  if (e.environment === 'SANDBOX' && Deno.env.get('STORE_SANDBOX') !== '1') return new Response('sandbox ignored');
  const r = fromEvent(e);
  if (r.skip) { console.log('skipped:', r.skip); return new Response('ok'); }

  const { data: b } = await admin.from('billing').select('source, status, stripe_subscription_id, store_event_at').eq('user_id', r.uid!).maybeSingle();
  if (!b) { console.warn('store event for an account with no billing row', r.uid); return new Response('ok'); }
  if (b.store_event_at && r.at! < b.store_event_at) { console.log('older than the last event applied'); return new Response('ok'); }
  const alsoStripe = b.source === 'stripe' && !!b.stripe_subscription_id && live(b.status);   // paying twice: tell the owner

  const { error } = await admin.from('billing').update(r.update!).eq('user_id', r.uid!);
  if (error) { console.error(error); return new Response('db error', { status: 500 }); }   // RevenueCat retries

  if (r.alert) {
    const { data } = await admin.auth.admin.getUserById(r.uid!);
    const u = data?.user;
    const { count } = await admin.from('item_progress').select('item_id', { count: 'exact', head: true }).eq('user_id', r.uid!).like('item_id', 's:%');
    const a = r.alert;
    const m = ownerAlert(a.event, { email: u?.email || r.uid!, joined: u?.created_at ? new Date(u.created_at) : null, studyDays: count || 0 },
                         a.plan, a.interval, a.pence, { firstCharge: a.firstCharge, kind: a.kind, until: a.until,
                         via: a.via + (alsoStripe && a.event === 'bought' ? ' ⚠️ They also have a website (Stripe) subscription: refund one.' : '') });
    try { await sendEmail(OWNER, m.subject, m.html, text(m.html)); } catch (x) { console.error(x); }
  }
  return new Response('ok');
});
