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

// When someone cancels (#182). Given the subscription and its paid invoices (newest first):
//   'free'   — in the free week: nothing was charged, nothing will be; it ends with the free week
//   'refund' — the first payment, or a yearly one, was within 14 days: refund it (with any plan-change
//              top-ups paid since) and end the plan now
//   'keep'   — otherwise: the plan runs to the end of the period paid for, then stops
// Monthly renewals after the first payment aren't refunded (the Terms, section 6), and the automatic refund
// is once per account: someone refunded before who subscribes again keeps the plan to the end instead.
const DAY = 86_400_000;
// deno-lint-ignore no-explicit-any
const paidAt = (inv: any) => (inv?.status_transitions?.paid_at ?? inv?.created ?? 0) * 1000;
// deno-lint-ignore no-explicit-any
export function onCancel(sub: any, paid: any[], now = Date.now(), refundedBefore = false): { kind: 'free' | 'refund' | 'keep'; invoices: any[]; pence: number } {
  if (sub?.status === 'trialing') return { kind: 'free', invoices: [], pence: 0 };
  if (refundedBefore) return { kind: 'keep', invoices: [], pence: 0 };
  const charged = (paid || []).filter(i => i.amount_paid > 0).sort((a, b) => paidAt(b) - paidAt(a));
  let periodic = charged.filter(i => i.billing_reason !== 'subscription_update');     // not plan-change top-ups
  if (!periodic.length) periodic = charged.slice(-1);   // a plan change that ended the free week was the first payment
  const anchor = periodic[0];
  const ok = anchor && now - paidAt(anchor) <= 14 * DAY && (periodic.length === 1 || subInfo(sub).interval === 'year');
  if (!ok) return { kind: 'keep', invoices: [], pence: 0 };
  const invoices = charged.filter(i => paidAt(i) >= paidAt(anchor));
  return { kind: 'refund', invoices, pence: invoices.reduce((n, i) => n + i.amount_paid, 0) };
}
