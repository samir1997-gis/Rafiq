// stripe-webhook — Stripe tells us when a subscription starts, changes or ends.
// Registered by tools/stripe-setup.js, which also stores STRIPE_WEBHOOK_SECRET.
// Email (#178): "thank you for subscribing" when checkout completes, sent once per subscription (the
// billing row records which one it was for, so a repeated event sends nothing). Payments themselves
// get Stripe's own receipt.
// Cancelling (#182), in Settings or in Stripe's Manage billing: within 14 days of the first payment (or
// a yearly one) it's refunded automatically and the plan ends now; then a "you've cancelled" email.
import Stripe from 'npm:stripe@17';
import { stripe, sync } from '../_shared/stripe.ts';
import { admin, sendEmail } from '../_shared/common.ts';
import { subscribed, cancelled, text } from '../_shared/emails.ts';
import { subInfo, onCancel } from '../_shared/sub-info.ts';

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
// Once per cancellation: the billing row records which one the email was for.
async function firstCancel(customer: string, key: string) {
  const { data } = await admin.from('billing').update({ cancel_email_for: key }).eq('stripe_customer_id', customer)
    .or(`cancel_email_for.is.null,cancel_email_for.neq.${key}`).select('user_id');
  return data?.[0]?.user_id as string | undefined;
}
async function onCancelled(sub: Stripe.Subscription) {
  const customer = typeof sub.customer === 'string' ? sub.customer : sub.customer.id;
  const uid = await firstCancel(customer, `${sub.id}:${sub.canceled_at ?? sub.cancel_at ?? ''}`);
  const i = subInfo(sub);
  if (!uid || !i.plan) return;
  // the key needs Invoices: Read and Refunds: Write; without them, the email still goes and offers a refund by reply
  const paid = await stripe!.invoices.list({ subscription: sub.id, status: 'paid', limit: 24 }).then(r => r.data, e => { console.error(e); return null; });
  const d = paid ? onCancel(sub, paid) : { kind: sub.status === 'trialing' ? 'free' as const : 'keep' as const, invoices: [], pence: 0 };
  const item = sub.items.data[0] as unknown as { current_period_end?: number };
  const end = item?.current_period_end ?? (sub as unknown as { current_period_end?: number }).current_period_end;
  let kind = d.kind, askRefund = !paid && d.kind === 'keep';
  if (kind === 'refund') {
    try {
      for (const inv of d.invoices)
        await stripe!.refunds.create(inv.payment_intent ? { payment_intent: String(inv.payment_intent) } : { charge: String(inv.charge) },
                                     { idempotencyKey: `rafiq-refund-${inv.id}` });
      await stripe!.subscriptions.cancel(sub.id);   // ends now; the 'deleted' event updates the billing row
    } catch (e) { console.error('refund failed', e); kind = 'keep'; askRefund = true; }
  }
  const a = await account(uid);
  if (a) await send(a.email, cancelled(a.name, i.plan, kind, {
    until: kind === 'free' ? (sub.trial_end ? new Date(sub.trial_end * 1000) : null) : end ? new Date(end * 1000) : null,
    pence: d.pence, askRefund }));
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
    const sub = event.data.object as Stripe.Subscription;
    await sync(sub);
    // just cancelled: it now ends at the period's end, and before this event it didn't
    const before = (event.data as { previous_attributes?: { cancel_at_period_end?: boolean; cancel_at?: number | null } }).previous_attributes;
    if (event.type === 'customer.subscription.updated' && before && (sub.cancel_at_period_end || sub.cancel_at)
        && (before.cancel_at_period_end === false || before.cancel_at === null)) await onCancelled(sub);
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
