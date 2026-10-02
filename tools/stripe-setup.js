/* stripe-setup.js — create what Rafiq needs in Stripe, then hand the keys to Supabase.
   Run by the "Stripe setup" GitHub Action; needs STRIPE_SECRET_KEY (test or live) and
   SUPABASE_ACCESS_TOKEN. Safe to run again: products and prices are found by lookup key.

   - Products Essentials and Complete, with four GBP prices (lookup keys rafiq_<plan>_<monthly|yearly>)
   - A customer portal: update card, see invoices, cancel at the end of the period
   - A webhook to the stripe-webhook function; its signing secret goes to Supabase
   - STRIPE_SECRET_KEY and STRIPE_WEBHOOK_SECRET stored as Supabase function secrets */
const REF = 'gaajfahtrbdybjuunfhe';
const KEY = process.env.STRIPE_SECRET_KEY, TOKEN = process.env.SUPABASE_ACCESS_TOKEN;
const HOOK_URL = `https://${REF}.supabase.co/functions/v1/stripe-webhook`;
const PLANS = {
  essentials: { name: 'Rafiq Essentials', desc: 'The whole course, reviews, audio and practice.', monthly: 699, yearly: 4999 },
  complete:   { name: 'Rafiq Complete', desc: 'Everything, plus the conversation partner, unlimited smart checks, real-life scenes and the weak-spots review.', monthly: 1199, yearly: 7999 },
};
const EVENTS = ['checkout.session.completed', 'customer.subscription.created', 'customer.subscription.updated', 'customer.subscription.deleted',
  'charge.refunded'];   // a refund made by hand in Stripe ends the plan (#193)

// Stripe's API takes form encoding; nested keys like a[b][0]=c
function form(obj, pre = '', out = []) {
  for (const [k, v] of Object.entries(obj)) {
    const key = pre ? `${pre}[${k}]` : k;
    if (v && typeof v === 'object') form(v, key, out);
    else if (v !== undefined) out.push(`${encodeURIComponent(key)}=${encodeURIComponent(v)}`);
  }
  return out.join('&');
}
async function stripe(method, url, body) {
  const r = await fetch('https://api.stripe.com/v1' + url, { method,
    headers: { Authorization: `Bearer ${KEY}`, 'Content-Type': 'application/x-www-form-urlencoded' },
    body: body ? form(body) : undefined });
  const j = await r.json();
  if (!r.ok) { console.error(`Stripe ${method} ${url}: ${j.error && j.error.message}`); process.exit(1); }
  return j;
}

(async () => {
  if (!KEY) { console.error('STRIPE_SECRET_KEY is not set: add it under GitHub → Settings → Secrets and variables → Actions'); process.exit(1); }
  if (!TOKEN) { console.error('SUPABASE_ACCESS_TOKEN is not set'); process.exit(1); }
  console.log(`Stripe mode: ${KEY.startsWith('sk_live') || KEY.startsWith('rk_live') ? 'LIVE' : 'test'}`);

  for (const [plan, p] of Object.entries(PLANS)) {
    const keys = ['monthly', 'yearly'].map(i => `rafiq_${plan}_${i}`);
    const found = (await stripe('GET', `/prices?active=true&${keys.map(k => 'lookup_keys[]=' + k).join('&')}`)).data;
    let product = found[0] && found[0].product;
    if (!product) product = (await stripe('POST', '/products', { name: p.name, description: p.desc, metadata: { rafiq_plan: plan } })).id;
    for (const i of ['monthly', 'yearly']) {
      const k = `rafiq_${plan}_${i}`, have = found.find(x => x.lookup_key === k);
      if (have && have.unit_amount === p[i]) { console.log(`price ${k}: exists (£${(p[i] / 100).toFixed(2)})`); continue; }
      await stripe('POST', '/prices', { product, currency: 'gbp', unit_amount: p[i], lookup_key: k, transfer_lookup_key: 'true',
        recurring: { interval: i === 'yearly' ? 'year' : 'month' }, tax_behavior: 'inclusive' });
      console.log(`price ${k}: created (£${(p[i] / 100).toFixed(2)})`);
    }
  }

  const products = (await stripe('GET', '/products?active=true&limit=100')).data.filter(x => x.metadata && x.metadata.rafiq_plan);
  const portalProducts = [];
  for (const pr of products) {
    const prices = (await stripe('GET', `/prices?active=true&product=${pr.id}`)).data.filter(x => (x.lookup_key || '').startsWith('rafiq_'));
    portalProducts.push({ product: pr.id, prices: prices.map(x => x.id) });
  }
  const portal = {
    business_profile: { headline: 'Manage your Rafiq plan', privacy_policy_url: 'https://rafiq-arabic.com/privacy.html', terms_of_service_url: 'https://rafiq-arabic.com/terms.html' },
    features: {
      payment_method_update: { enabled: 'true' }, invoice_history: { enabled: 'true' },
      customer_update: { enabled: 'true', allowed_updates: { 0: 'email' } },
      subscription_cancel: { enabled: 'true', mode: 'at_period_end' },
      // changing plan in the free week keeps the free week (Stripe's default ends it and charges at once, #180)
      subscription_update: { enabled: 'true', default_allowed_updates: { 0: 'price' }, proration_behavior: 'create_prorations', trial_update_behavior: 'continue_trial',
        products: Object.fromEntries(portalProducts.map((x, n) => [n, { product: x.product, prices: Object.fromEntries(x.prices.map((id, m) => [m, id])) }])) },
    },
    default_return_url: 'https://rafiq-arabic.com/settings.html',
  };
  const configs = (await stripe('GET', '/billing_portal/configurations?is_default=true')).data;
  if (configs.length) await stripe('POST', `/billing_portal/configurations/${configs[0].id}`, portal);
  else await stripe('POST', '/billing_portal/configurations', portal);
  console.log('customer portal: set (card, invoices, switch plan keeping the free week, cancel at period end)');

  // the signing secret is only shown when an endpoint is created, so replace ours each run
  for (const w of (await stripe('GET', '/webhook_endpoints?limit=100')).data)
    if (w.url === HOOK_URL) await stripe('DELETE', `/webhook_endpoints/${w.id}`);
  const hook = await stripe('POST', '/webhook_endpoints', { url: HOOK_URL, enabled_events: Object.fromEntries(EVENTS.map((e, n) => [n, e])),
    description: 'Rafiq: keep each account’s plan up to date' });
  console.log('webhook: created →', HOOK_URL);

  const r = await fetch(`https://api.supabase.com/v1/projects/${REF}/secrets`, { method: 'POST',
    headers: { Authorization: `Bearer ${TOKEN}`, 'Content-Type': 'application/json' },
    body: JSON.stringify([{ name: 'STRIPE_SECRET_KEY', value: KEY }, { name: 'STRIPE_WEBHOOK_SECRET', value: hook.secret }]) });
  if (!r.ok) { console.error(`Supabase secrets failed: ${r.status} ${(await r.text()).slice(0, 300)}`); process.exit(1); }
  console.log('Supabase: STRIPE_SECRET_KEY and STRIPE_WEBHOOK_SECRET stored');
})();
