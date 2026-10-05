// admin-stats — the owner dashboard (admin.html, #189): {days} → website visits from Cloudflare Web Analytics
// (per day, where from, countries, pages, devices) and sign-ups by where people came from (private.funnel_by_source).
// Only accounts with app_metadata.admin (set by the Supabase users workflow's make-admin; learners can't set it).
import { admin, caller, cors, json } from '../_shared/common.ts';

const CF = Deno.env.get('CLOUDFLARE_API_TOKEN'), ACC = Deno.env.get('CLOUDFLARE_ACCOUNT_ID');
const by = (d: string) => `rumPageloadEventsAdaptiveGroups(limit: 15, filter: $f, orderBy: [sum_visits_DESC]) { count sum { visits } dimensions { ${d} } }`;
const QUERY = `query($acc: string, $f: AccountRumPageloadEventsAdaptiveGroupsFilter_InputObject) { viewer { accounts(filter: {accountTag: $acc}) {
  total: rumPageloadEventsAdaptiveGroups(limit: 1, filter: $f) { count sum { visits } }
  days: rumPageloadEventsAdaptiveGroups(limit: 31, filter: $f, orderBy: [date_ASC]) { count sum { visits } dimensions { date } }
  refs: ${by('refererHost')} countries: ${by('countryName')} devices: ${by('deviceType')}
  paths: rumPageloadEventsAdaptiveGroups(limit: 15, filter: $f, orderBy: [count_DESC]) { count sum { visits } dimensions { requestPath } } } } }`;   // pages by views: a visit counts only where it starts

type Row = { count: number; sum: { visits: number }; dimensions: Record<string, string> };
const rows = (xs: Row[], d: string) => xs.map(x => ({ name: x.dimensions[d] || '', visits: x.sum.visits, views: x.count }));

async function visits(days: number) {
  if (!CF || !ACC) return { error: 'no_cloudflare' };
  // only the real site: test copies (raw.githack.com previews, localhost) were counted before the pages stopped reporting from them
  // "Today" is since midnight (UTC, as the per-day chart and the sign-ups count it), not the last 24 hours
  const from = days === 1 ? new Date(new Date().toISOString().slice(0, 10) + 'T00:00:00Z') : new Date(Date.now() - days * 864e5);
  const f = { datetime_geq: from.toISOString(), datetime_leq: new Date().toISOString(), requestHost: 'rafiq-arabic.com' };
  const r = await fetch('https://api.cloudflare.com/client/v4/graphql', { method: 'POST',
    headers: { Authorization: `Bearer ${CF}`, 'Content-Type': 'application/json' }, body: JSON.stringify({ query: QUERY, variables: { acc: ACC, f } }) });
  const j = await r.json().catch(() => ({}));
  if (!r.ok || j.errors || !j.data) { console.error('cloudflare', r.status, JSON.stringify(j.errors || j).slice(0, 300)); return { error: 'cloudflare' }; }
  const a = j.data.viewer.accounts[0], t = a.total[0];
  return { visits: t?.sum.visits ?? 0, views: t?.count ?? 0, days: rows(a.days, 'date'),
    refs: rows(a.refs, 'refererHost'), countries: rows(a.countries, 'countryName'), paths: rows(a.paths, 'requestPath'), devices: rows(a.devices, 'deviceType') };
}

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: cors(req) });
  const user = await caller(req);
  if (!user || user.app_metadata?.admin !== true) return json(req, { error: 'not_admin' }, 403);
  const body = await req.json().catch(() => ({}));
  const days = Math.max(1, Math.min(30, parseInt(body.days, 10) || 7));
  const [web, src, acc] = await Promise.all([visits(days),
    admin.rpc('admin_funnel_by_source', { days }), admin.rpc('admin_account_count')]);
  if (src.error || acc.error) console.error(src.error || acc.error);
  return json(req, { days, web, sources: src.data ?? [], accounts: acc.data ?? null });
});
