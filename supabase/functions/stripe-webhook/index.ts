// stripe-webhook — Stripe tells us when a subscription starts, changes or ends.
// Registered by tools/stripe-setup.js, which also stores STRIPE_WEBHOOK_SECRET.
// Email (#178): "thank you for subscribing" when checkout completes, sent once per subscription (the
// billing row records which one it was for, so a repeated event sends nothing). Payments themselves
// get Stripe's own receipt.
import Stripe from 'npm:stripe@17';
import { stripe, sync } from '../_shared/stripe.ts';
import { admin, sendEmail } from '../_shared/common.ts';
import { subscribed, text } from '../_shared/emails.ts';
import { subInfo } from '../_shared/sub-info.ts';

const SECRET = Deno.env.get('STRIPE_WEBHOOK_SECRET');
const crypto = Stripe.createSubtleCryptoProvider();

async function account(id: string) {
  const { data } = await admin.auth.admin.getUserById(id);
  const u = data?.user;
  return u && u.email ? { email: u.email, name: (u.user_metadata?.name as string) || null } : null;
}
// Mark the email as sent for this subscription; false if it already was.
async function firstTime(uid: string, subId: string) {
  const { data } = await admin.from('billing').update({ subscribed_email_sub: subId }).eq('user_id', uid)
    .or(`subscribed_email_sub.is.null,subscribed_email_sub.neq.${subId}`).select('user_id');
  return !!data?.length;
}
async function send(to: string, m: { subject: string; html: string }) {
  try { await sendEmail(to, m.subject, m.html, text(m.html)); } catch (e) { console.error(e); }   // never fail the webhook over an email
}

Deno.serve(async (req) => {
  if (!stripe || !SECRET) return new Response('not ready', { status: 503 });
  const raw = await req.text();
  let event: Stripe.Event;
  try {
    event = await stripe.webhooks.constructEventAsync(raw, req.headers.get('stripe-signature') || '', SECRET, undefined, crypto);
  } catch { return new Response('bad signature', { status: 400 }); }

  if (event.type.startsWith('customer.subscription.')) {
    await sync(event.data.object as Stripe.Subscription);
  } else if (event.type === 'checkout.session.completed') {
    const s = event.data.object as Stripe.Checkout.Session;
    if (s.subscription) {
      const sub = await stripe.subscriptions.retrieve(String(s.subscription));
      await sync(sub);
      const uid = (sub.metadata?.user_id as string) || s.client_reference_id;
      const i = subInfo(sub);
      if (uid && i.plan && await firstTime(uid, sub.id)) {
        const a = await account(uid);
        if (a) await send(a.email, subscribed(a.name, i.plan, i.interval, i.pence, i.firstCharge));
      }
    }
  }
  return new Response('ok');
});
