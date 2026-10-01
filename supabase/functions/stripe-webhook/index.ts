// stripe-webhook — Stripe tells us when a subscription starts, changes or ends, and when a payment
// goes through. Registered by tools/stripe-setup.js, which also stores STRIPE_WEBHOOK_SECRET.
// Emails (#178): "thank you for subscribing" when checkout completes, and "payment received" for each
// later charge. Each is sent once: the billing row records which subscription or invoice it was for,
// so a repeated event sends nothing.
import Stripe from 'npm:stripe@17';
import { stripe, sync } from '../_shared/stripe.ts';
import { admin, sendEmail } from '../_shared/common.ts';
import { subscribed, paymentReceived, text } from '../_shared/emails.ts';
import { subInfo } from '../_shared/sub-info.ts';

const SECRET = Deno.env.get('STRIPE_WEBHOOK_SECRET');
const crypto = Stripe.createSubtleCryptoProvider();

async function account(id: string) {
  const { data } = await admin.auth.admin.getUserById(id);
  const u = data?.user;
  return u && u.email ? { email: u.email, name: (u.user_metadata?.name as string) || null } : null;
}
// Mark the email as sent for this id, unless it already was. Returns the account, or null to skip.
async function claim(col: string, id: string, by: string, value: string) {
  const { data } = await admin.from('billing').update({ [col]: id }).eq(by, value)
    .or(`${col}.is.null,${col}.neq.${id}`).select('user_id, plan, interval');
  return data?.[0] || null;
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
      if (uid && i.plan && await claim('subscribed_email_sub', sub.id, 'user_id', uid)) {
        const a = await account(uid);
        if (a) await send(a.email, subscribed(a.name, i.plan, i.interval, i.pence, i.firstCharge));
      }
    }
  } else if (event.type === 'invoice.paid') {
    // deno-lint-ignore no-explicit-any
    const inv = event.data.object as any;
    // a charge at sign-up is confirmed by the "thank you" email; a free week's £0 invoice isn't a payment
    if (inv.amount_paid > 0 && inv.billing_reason !== 'subscription_create') {
      const customer = typeof inv.customer === 'string' ? inv.customer : inv.customer?.id;
      const b = customer && await claim('paid_email_invoice', inv.id, 'stripe_customer_id', customer);
      if (b && b.plan) {
        const a = await account(b.user_id);
        const end = inv.lines?.data?.[0]?.period?.end;
        if (a) await send(a.email, paymentReceived(a.name, b.plan, inv.amount_paid, end ? new Date(end * 1000) : null, inv.hosted_invoice_url || null));
      }
    }
  }
  return new Response('ok');
});
