// quran — licensed Quran recitation for Your salah, from the Quran Foundation API (#135):
//   {verses: ["1:1", "112:1", …]} → {verses: {"1:1": {url, segments}}, credit}
// segments are word timings, [word position (from 1), start ms, end ms], for the
// word-by-word highlight. Signed-in learners only. Nothing is stored: QF's terms
// allow at most a week of caching, and the browser only keeps it for the page.
// Needs the function secrets QF_CLIENT_ID and QF_CLIENT_SECRET (Developer Console);
// QF_RECITATION_ID picks the reciter (default 7, Mishari Rashid al-Afasy).
import { caller, cors, json } from '../_shared/common.ts';

const ID = Deno.env.get('QF_CLIENT_ID') || '', SECRET = Deno.env.get('QF_CLIENT_SECRET') || '';
const RECITATION = Deno.env.get('QF_RECITATION_ID') || '7';
const PRELIVE = Deno.env.get('QF_ENV') === 'prelive';
const AUTH = PRELIVE ? 'https://prelive-oauth2.quran.foundation' : 'https://oauth2.quran.foundation';
const API = (PRELIVE ? 'https://apis-prelive.quran.foundation' : 'https://apis.quran.foundation') + '/content/api/v4';
const AUDIO = 'https://verses.quran.foundation/';
const CREDIT = 'Recitation: Quran Foundation (Quran.com)';

let token = '', expires = 0;                 // one access token per instance, renewed before its hour is up
async function accessToken() {
  if (token && Date.now() < expires) return token;
  const r = await fetch(`${AUTH}/oauth2/token`, {
    method: 'POST',
    headers: { Authorization: 'Basic ' + btoa(`${ID}:${SECRET}`), 'Content-Type': 'application/x-www-form-urlencoded' },
    body: 'grant_type=client_credentials&scope=content' });
  if (!r.ok) throw new Error(`token ${r.status}`);
  const t = await r.json();
  token = t.access_token; expires = Date.now() + (Number(t.expires_in || 3600) - 300) * 1000;
  return token;
}

async function verse(key: string) {
  const r = await fetch(`${API}/recitations/${RECITATION}/by_ayah/${key}?fields=segments,url&segments=true`,
    { headers: { 'x-auth-token': await accessToken(), 'x-client-id': ID } });
  if (!r.ok) throw new Error(`${key} ${r.status}`);
  const f = ((await r.json()).audio_files || [])[0];
  if (!f || !f.url) return null;
  const url = /^https?:/.test(f.url) ? f.url : f.url.startsWith('//') ? 'https:' + f.url : AUDIO + f.url;
  return { url, segments: Array.isArray(f.segments) ? f.segments : [] };
}

/* Health check: fetches 1:1 at most every 10 minutes, and says whether the keys and
   word timings work. Shows no content. */
let checked: { at: number, result: Record<string, unknown> } | null = null;
async function health() {
  if (checked && Date.now() - checked.at < 600_000) return checked.result;
  let result: Record<string, unknown>;
  try {
    const v = await verse('1:1');
    result = { ok: !!v, env: PRELIVE ? 'prelive' : 'production', recitation: RECITATION,
               timings: !!(v && v.segments.length), audio_host: v ? new URL(v.url).host : null };
  } catch (e) { result = { ok: false, env: PRELIVE ? 'prelive' : 'production', error: String(e) }; }
  checked = { at: Date.now(), result };
  return result;
}

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: cors(req) });
  if (req.method !== 'POST') return json(req, { error: 'method' }, 405);
  if (!ID || !SECRET) return json(req, { error: 'not_configured' }, 503);
  const body = await req.json().catch(() => ({}));
  if (body.check) return json(req, await health());       // no sign-in: says only whether QF answers
  if (!(await caller(req))) return json(req, { error: 'signin' }, 401);
  const keys = [...new Set((Array.isArray(body.verses) ? body.verses : [])
    .map(String).filter((k: string) => /^\d{1,3}:\d{1,3}$/.test(k)))].slice(0, 40) as string[];
  const out: Record<string, unknown> = {};
  try {
    await Promise.all(keys.map(async k => { out[k] = await verse(k); }));
  } catch (e) { console.error(e); return json(req, { error: 'upstream' }, 502); }
  return json(req, { verses: out, credit: CREDIT });
});
