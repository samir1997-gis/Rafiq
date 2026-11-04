// The app stores (#345): what a RevenueCat event means for an account's billing row. Pure (no network), so
// tests/store_webhook.py runs it under Node. store-webhook applies the result.
// In the apps, RevenueCat's app user id is the Supabase account id (Purchases.logIn(user.id)).
// Product ids carry the plan and the period, as Stripe's lookup keys do: rafiq_complete_monthly, rafiq_essentials_yearly
// (Google's arrive as "<subscription>:<base plan>", e.g. rafiq_complete:yearly).
export type Plan = 'essentials' | 'complete';
export type Source = 'apple' | 'google';
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
const LIVE = ['active', 'trialing', 'past_due'];

export const planOf = (id?: string | null): Plan | null => !id ? null : /complete/i.test(id) ? 'complete' : /essentials/i.test(id) ? 'essentials' : null;
export const intervalOf = (id?: string | null) => /year|annual/i.test(id || '') ? 'year' : 'month';
export const sourceOf = (store?: string): Source | null => store === 'APP_STORE' || store === 'MAC_APP_STORE' ? 'apple' : store === 'PLAY_STORE' ? 'google' : null;
export const live = (status?: string | null) => LIVE.includes(status || '');
export const STORE_NAME = { apple: 'the App Store', google: 'Google Play' } as const;

// deno-lint-ignore no-explicit-any
type Ev = Record<string, any>;
export type Result = {
  skip?: string;
  uid?: string; at?: string; source?: Source;
  update?: Record<string, unknown>;
  alert?: { event: 'bought' | 'cancelled'; plan: Plan; interval: string; pence: number; firstCharge?: Date | null;
            kind?: 'free' | 'refund' | 'keep'; until?: Date | null; via: string };
};

export function accountOf(e: Ev): string | null {
  for (const id of [e.app_user_id, e.original_app_user_id, ...(e.aliases || [])]) if (typeof id === 'string' && UUID.test(id)) return id;
  return null;
}

export function fromEvent(e: Ev): Result {
  if (e.type === 'TEST') return { skip: 'test event' };
  const source = sourceOf(e.store);
  if (!source) return { skip: `not an app store (${e.store})` };
  const uid = accountOf(e);
  if (!uid) return { skip: 'no Rafiq account id' };
  const product = e.product_id as string, plan = planOf(product), interval = intervalOf(product);
  if (!plan) return { skip: `unknown product ${product}` };
  const ms = (x?: number | null) => typeof x === 'number' ? new Date(x).toISOString() : null;
  const end = ms(e.expiration_at_ms), trial = e.period_type === 'TRIAL';
  const at = ms(e.event_timestamp_ms) || new Date().toISOString();
  const base = { source, store_product: product, store_transaction_id: e.original_transaction_id ?? null, store_event_at: at,
                 interval, current_period_end: end, updated_at: new Date().toISOString() };
  const gbp = e.currency === 'GBP' && typeof e.price_in_purchased_currency === 'number';
  const pence = gbp ? Math.round(e.price_in_purchased_currency * 100) : 0;
  const via = `Through ${STORE_NAME[source]}${gbp || typeof e.price_in_purchased_currency !== 'number' ? '' : ` (${e.price_in_purchased_currency} ${e.currency})`}.`;
  const r = { uid, at, source };
  switch (e.type) {
    case 'INITIAL_PURCHASE':
      return { ...r, update: { ...base, plan, status: trial ? 'trialing' : 'active', cancel_at_period_end: false },
               alert: { event: 'bought', plan, interval, pence, firstCharge: trial && end ? new Date(end) : null, via } };
    case 'RENEWAL': case 'UNCANCELLATION': case 'SUBSCRIPTION_EXTENDED': case 'TEMPORARY_ENTITLEMENT_GRANT':
      return { ...r, update: { ...base, plan, status: trial ? 'trialing' : 'active', cancel_at_period_end: false } };
    case 'BILLING_ISSUE':
      return { ...r, update: { ...base, plan, status: 'past_due' } };
    case 'CANCELLATION':
      if (e.cancel_reason === 'CUSTOMER_SUPPORT')        // refunded by Apple or Google: the plan ends now
        return { ...r, update: { ...base, plan: null, status: 'canceled', cancel_at_period_end: false, current_period_end: at },
                 alert: { event: 'cancelled', plan, interval, pence, kind: 'refund', via } };
      return { ...r, update: { ...base, plan, status: trial ? 'trialing' : 'active', cancel_at_period_end: true },
               alert: { event: 'cancelled', plan, interval, pence, kind: trial ? 'free' : 'keep', until: end ? new Date(end) : null, via } };
    case 'EXPIRATION':
      return { ...r, update: { ...base, plan: null, status: 'canceled', cancel_at_period_end: false } };
    default:     // PRODUCT_CHANGE (the new plan arrives with the next RENEWAL), SUBSCRIPTION_PAUSED, TRANSFER, NON_RENEWING_PURCHASE
      return { skip: `not used: ${e.type}` };
  }
}
