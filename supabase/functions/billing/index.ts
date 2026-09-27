// billing — for the signed-in learner:
//   {action:'checkout', plan:'essentials'|'complete', interval:'month'|'year'} → {url} (Stripe Checkout)
//   {action:'portal'}  → {url}  (Stripe's page for card details and invoices)
//   {action:'cancel'}  → stops at the end of the period already paid for
//   {action:'resume'}  → undoes a cancel before that date
import { admin, caller, cors, json, SITE } from '../_shared/common.ts';
import { stripe, lookupKey, sync } from '../_shared/stripe.ts';

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: cors(req) });
  const user = await caller(req);
  if (!user) return json(req, { error: 'signin' }, 401);
  if (!stripe) return json(req, { error: 'not_ready' }, 503);
  const body = await req.json().catch(() => ({}));
  const { data: b } = await admin.from('billing').select('*').eq('user_id', user.id).maybeSingle();
  if (!b) return json(req, { error: 'no_account' }, 404);

  try {
    if (body.action === 'checkout') {
      if (!['essentials', 'complete'].includes(body.plan) || !['month', 'year'].includes(body.interval))
        return json(req, { error: 'bad_plan' }, 400);
      if (b.stripe_subscription_id && ['active', 'trialing', 'past_due'].includes(b.status))
        return json(req, { error: 'already_subscribed' }, 409);
      const prices = await stripe.prices.list({ lookup_keys: [lookupKey(body.plan, body.interval)], active: true });
      if (!prices.data.length) return json(req, { error: 'not_ready' }, 503);
      let customer = b.stripe_customer_id as string | null;
      if (!customer) {
        customer = (await stripe.customers.create({ email: user.email, metadata: { user_id: user.id } })).id;
        await admin.from('billing').update({ stripe_customer_id: customer }).eq('user_id', user.id);
      }
      // Paying during the free week doesn't cut it short: the first charge waits
      // until the week ends (Stripe needs that to be at least 2 days away).
      const trialEnd = new Date(b.trial_ends_at).getTime();
      const keepTrial = trialEnd - Date.now() > 49 * 3600_000;
      const session = await stripe.checkout.sessions.create({
        mode: 'subscription', customer, client_reference_id: user.id,
        line_items: [{ price: prices.data[0].id, quantity: 1 }],
        subscription_data: { metadata: { user_id: user.id }, ...(keepTrial ? { trial_end: Math.floor(trialEnd / 1000) } : {}) },
        allow_promotion_codes: true,
        success_url: `${SITE}/settings.html?plan=done`,
        cancel_url: `${SITE}/plans.html`,
      });
      return json(req, { url: session.url });
    }
    if (body.action === 'portal') {
      if (!b.stripe_customer_id) return json(req, { error: 'no_subscription' }, 404);
      const s = await stripe.billingPortal.sessions.create({ customer: b.stripe_customer_id, return_url: `${SITE}/settings.html` });
      return json(req, { url: s.url });
    }
    if (body.action === 'cancel' || body.action === 'resume') {
      if (!b.stripe_subscription_id) return json(req, { error: 'no_subscription' }, 404);
      const sub = await stripe.subscriptions.update(b.stripe_subscription_id, { cancel_at_period_end: body.action === 'cancel' });
      await sync(sub);
      return json(req, { ok: true, cancel_at_period_end: sub.cancel_at_period_end });
    }
    return json(req, { error: 'unknown' }, 400);
  } catch (e) {
    console.error(e);
    return json(req, { error: 'stripe', message: String((e as Error).message || e).slice(0, 200) }, 502);
  }
});
