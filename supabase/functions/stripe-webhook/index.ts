// stripe-webhook — Stripe tells us when a subscription starts, changes or ends.
// Registered by tools/stripe-setup.js, which also stores STRIPE_WEBHOOK_SECRET.
import Stripe from 'npm:stripe@17';
import { stripe, sync } from '../_shared/stripe.ts';

const SECRET = Deno.env.get('STRIPE_WEBHOOK_SECRET');
const crypto = Stripe.createSubtleCryptoProvider();

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
    if (s.subscription) await sync(await stripe.subscriptions.retrieve(String(s.subscription)));
  }
  return new Response('ok');
});
