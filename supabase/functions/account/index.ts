// account — for the signed-in learner:
//   {action:'delete', confirm:'DELETE'} → cancels any subscription, removes every
//   row that belongs to the account, then deletes the account itself.
import { admin, caller, cors, json } from '../_shared/common.ts';
import { stripe } from '../_shared/stripe.ts';

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: cors(req) });
  const user = await caller(req);
  if (!user) return json(req, { error: 'signin' }, 401);
  const body = await req.json().catch(() => ({}));
  if (body.action !== 'delete' || body.confirm !== 'DELETE') return json(req, { error: 'confirm' }, 400);

  const { data: b } = await admin.from('billing').select('stripe_customer_id').eq('user_id', user.id).maybeSingle();
  if (b?.stripe_customer_id) {
    // deleting the customer cancels their subscription straight away and removes their details from Stripe
    if (!stripe) return json(req, { error: 'try_later' }, 503);
    try { await stripe.customers.del(b.stripe_customer_id); }
    catch (e) { if ((e as { statusCode?: number }).statusCode !== 404) { console.error(e); return json(req, { error: 'try_later' }, 502); } }
  }
  const { error: e1 } = await admin.rpc('delete_user_data', { uid: user.id });
  if (e1) { console.error(e1); return json(req, { error: 'try_later' }, 500); }
  const { error: e2 } = await admin.auth.admin.deleteUser(user.id);
  if (e2) { console.error(e2); return json(req, { error: 'try_later' }, 500); }
  return json(req, { ok: true });
});
