// quran — licensed Quran recitation for Your salah, from the Quran Foundation API (#135):
//   {verses: ["1:1", "112:1", …]} → {verses: {"1:1": {url, segments}}, credit}
// segments are word timings, [word position (from 1), start ms, end ms], for the
// word-by-word highlight. Signed-in learners only. Nothing is stored: QF's terms
// allow at most a week of caching, and the browser only keeps it for the page.
// Needs the function secrets QF_CLIENT_ID and QF_CLIENT_SECRET (Developer Console);
// QF_RECITATION_ID picks the reciter (default 12, Mahmoud Khalil al-Husary, Muallim: the slow
// teaching recitation, with a pause after each verse to repeat it).
import { caller, cors as siteCors, json as siteJson } from '../_shared/common.ts';

// Also answers the branch preview (raw.githack.com) so Salah can be tried before it's
// on the live site. Only this function: it hands out recitation links and nothing else.
const PREVIEW = 'https://raw.githack.com';
const cors = (req: Request) => req.headers.get('origin') === PREVIEW
  ? { ...siteCors(req), 'Access-Control-Allow-Origin': PREVIEW } : siteCors(req);
const json = (req: Request, body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { ...cors(req), 'Content-Type': 'application/json' } });

const ID = Deno.env.get('QF_CLIENT_ID') || '', SECRET = Deno.env.get('QF_CLIENT_SECRET') || '';
const RECITATION = Deno.env.get('QF_RECITATION_ID') || '12';
// QF issues production or pre-production keys; the right one is found on first use.
const ENVS = {
  production: { auth: 'https://oauth2.quran.foundation', api: 'https://apis.quran.foundation/content/api/v4' },
  prelive: { auth: 'https://prelive-oauth2.quran.foundation', api: 'https://apis-prelive.quran.foundation/content/api/v4' },
};
type Env = keyof typeof ENVS;
let env: Env = Deno.env.get('QF_ENV') === 'prelive' ? 'prelive' : 'production';
const AUDIO = 'https://verses.quran.foundation/';
const CREDIT = 'Recitation: Quran Foundation (Quran.com)';

let token = '', expires = 0;                 // one access token per instance, renewed before its hour is up
async function tokenFrom(e: Env) {
  return await fetch(`${ENVS[e].auth}/oauth2/token`, {
    method: 'POST',
    headers: { Authorization: 'Basic ' + btoa(`${ID}:${SECRET}`), 'Content-Type': 'application/x-www-form-urlencoded' },
    body: 'grant_type=client_credentials&scope=content' });
}
async function accessToken() {
  if (token && Date.now() < expires) return token;
  let r = await tokenFrom(env);
  if (r.status === 401 || r.status === 400) {                 // keys from the other environment?
    const other: Env = env === 'production' ? 'prelive' : 'production';
    const r2 = await tokenFrom(other);
    if (r2.ok) { env = other; r = r2; }
  }
  if (!r.ok) throw new Error(`token ${r.status}`);
  const t = await r.json();
  token = t.access_token; expires = Date.now() + (Number(t.expires_in || 3600) - 300) * 1000;
  return token;
}

async function verse(key: string, recitation = RECITATION) {
  const t = await accessToken();                              // first: it settles which environment
  const r = await fetch(`${ENVS[env].api}/recitations/${recitation}/by_ayah/${key}?fields=segments,url&segments=true`,
    { headers: { 'x-auth-token': t, 'x-client-id': ID } });
  if (!r.ok) throw new Error(`${key} ${r.status}`);
  const f = ((await r.json()).audio_files || [])[0];
  if (!f || !f.url) return null;
  const url = /^https?:/.test(f.url) ? f.url : f.url.startsWith('//') ? 'https:' + f.url : AUDIO + f.url;
  return { url, segments: Array.isArray(f.segments) ? f.segments : [] };
}

const verseKeys = (v: unknown) => [...new Set((Array.isArray(v) ? v : [])
  .map(String).filter((k: string) => /^\d{1,3}:\d{1,3}$/.test(k)))].slice(0, 60) as string[];

/* Health check, no sign-in: {check: true, verses?: [...]} says whether the keys work and,
   per verse, whether QF returns audio and word timings (the public audio link and the
   timings only; no Quran text). At most once every 10 minutes per list of verses. */
const checked = new Map<string, { at: number, result: Record<string, unknown> }>();
async function health(list: string[], recitation = RECITATION) {
  const keys = (list.length ? list : ['1:1']).slice(0, 60), id = recitation + ':' + keys.join(',');
  const c = checked.get(id);
  if (c && Date.now() - c.at < 600_000) return c.result;
  const verses: Record<string, unknown> = {}, todo = [...keys];
  await Promise.all([0, 1, 2].map(async () => {
    for (let k = todo.shift(); k; k = todo.shift()) {
      try { verses[k] = await verse(k, recitation); } catch (e) { verses[k] = { error: String(e) }; }
    }
  }));
  const result = { ok: Object.values(verses).some(v => v && !(v as { error?: string }).error), env, recitation, verses };
  checked.set(id, { at: Date.now(), result });
  return result;
}

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: cors(req) });
  if (req.method !== 'POST') return json(req, { error: 'method' }, 405);
  if (!ID || !SECRET) return json(req, { error: 'not_configured' }, 503);
  const body = await req.json().catch(() => ({}));
  if (body.check) return json(req, await health(verseKeys(body.verses), /^\d{1,3}$/.test(String(body.recitation)) ? String(body.recitation) : RECITATION));       // no sign-in: says only whether QF answers
  if (!(await caller(req))) return json(req, { error: 'signin' }, 401);
  const keys = verseKeys(body.verses);
  // three at a time, so a whole prayer's verses don't trip QF's rate limit; a verse
  // that still fails is left out (the app reads it along silently) rather than all
  const out: Record<string, unknown> = {}, todo = [...keys];
  let failed = 0;
  await Promise.all([0, 1, 2].map(async () => {
    for (let k = todo.shift(); k; k = todo.shift()) {
      try { out[k] = await verse(k); }
      catch (e) { failed++; console.error(k, String(e)); }
    }
  }));
  if (failed && failed === keys.length) return json(req, { error: 'upstream' }, 502);
  return json(req, { verses: out, credit: CREDIT });
});
