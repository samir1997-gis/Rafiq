// What the "thank you for subscribing" email needs from a Stripe subscription (#178): the plan,
// monthly or yearly, the price, and when the first payment is taken. Reads older and newer API
// shapes (newer ones keep the period on the item). No imports, so tests/emails.py can run it.
export type SubInfo = { plan: 'essentials' | 'complete' | null; interval: 'month' | 'year'; pence: number; firstCharge: Date | null };

// deno-lint-ignore no-explicit-any
export function subInfo(sub: any): SubInfo {
  const price = sub?.items?.data?.[0]?.price || {};
  const key = String(price.lookup_key || '');
  return {
    plan: key.includes('complete') ? 'complete' : key.includes('essentials') ? 'essentials' : null,
    interval: price.recurring?.interval === 'year' ? 'year' : 'month',
    pence: price.unit_amount ?? 0,
    // still in the free week: the first payment waits for it to end; otherwise it's taken today (null)
    firstCharge: sub?.status === 'trialing' && sub?.trial_end ? new Date(sub.trial_end * 1000) : null,
  };
}
