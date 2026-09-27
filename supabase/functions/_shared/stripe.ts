import Stripe from 'npm:stripe@17';
import { admin } from './common.ts';

const KEY = Deno.env.get('STRIPE_SECRET_KEY');
export const stripe = KEY ? new Stripe(KEY, { httpClient: Stripe.createFetchHttpClient() }) : null;

// Prices are found by lookup key, set by tools/stripe-setup.js: rafiq_<plan>_<monthly|yearly>
export const lookupKey = (plan: string, interval: string) => `rafiq_${plan}_${interval === 'year' ? 'yearly' : 'monthly'}`;
const planOf = (key?: string | null) => key?.includes('complete') ? 'complete' : key?.includes('essentials') ? 'essentials' : null;
const ENDED = ['canceled', 'incomplete_expired', 'unpaid'];

// Copy a Stripe subscription onto the account's billing row.
export async function sync(sub: Stripe.Subscription) {
  const customer = typeof sub.customer === 'string' ? sub.customer : sub.customer.id;
  let uid = sub.metadata?.user_id as string | undefined;
  if (!uid) {
    const { data } = await admin.from('billing').select('user_id').eq('stripe_customer_id', customer).maybeSingle();
    uid = data?.user_id;
  }
  if (!uid) return console.warn('subscription with no account', sub.id);
  const item = sub.items.data[0];
  // newer API versions keep the period on the item
  const end = (item as unknown as { current_period_end?: number }).current_period_end
    ?? (sub as unknown as { current_period_end?: number }).current_period_end;
  const ended = ENDED.includes(sub.status);
  await admin.from('billing').update({
    plan: ended ? null : planOf(item?.price?.lookup_key),
    status: sub.status,
    interval: item?.price?.recurring?.interval ?? null,
    current_period_end: end ? new Date(end * 1000).toISOString() : null,
    cancel_at_period_end: !!sub.cancel_at_period_end,
    stripe_customer_id: customer,
    stripe_subscription_id: ended ? null : sub.id,
    updated_at: new Date().toISOString(),
  }).eq('user_id', uid);
}
