// quran — the Quran for Your salah from the Quran Foundation API (#135, #147): the licensed
// recitation, the official translation and the word-by-word meanings.
//   {verses: ["1:1", "112:1", …]} → {verses: {"1:1": {url, segments, translation, words}}, credit}
// segments are word timings, [first word from 0, word after last, start ms, end ms], for the
// word-by-word highlight; words are the English meaning of each word, in order. Signed-in learners only. Nothing is stored: QF's terms
// allow at most a week of caching, and the browser only keeps it for the page.
// Needs the function secrets QF_CLIENT_ID and QF_CLIENT_SECRET (Developer Console);
// QF_RECITATION_ID picks the reciter (default 12, Mahmoud Khalil al-Husary, Muallim: the slow
// teaching recitation, with a pause after each verse to repeat it). QF_TRANSLATION_ID picks
// the translation (default 20, Saheeh International).
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
const TRANSLATION = Deno.env.get('QF_TRANSLATION_ID') || '20';
const TRANSLATORS: Record<string, string> = { '20': 'Saheeh International', '85': 'M.A.S. Abdel Haleem', '84': 'T. Usmani', '19': 'M. Pickthall', '22': 'A. Yusuf Ali' };
// QF issues production or pre-production keys; the right one is found on first use.
const ENVS = {
  production: { auth: 'https://oauth2.quran.foundation', api: 'https://apis.quran.foundation/content/api/v4' },
  prelive: { auth: 'https://prelive-oauth2.quran.foundation', api: 'https://apis-prelive.quran.foundation/content/api/v4' },
};
type Env = keyof typeof ENVS;
let env: Env = Deno.env.get('QF_ENV') === 'prelive' ? 'prelive' : 'production';
const AUDIO = 'https://verses.quran.foundation/';
const CREDIT = `Recitation and translation (${TRANSLATORS[TRANSLATION] || 'Quran Foundation'}; word by word: Quran.com) from the Quran Foundation`;

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

/* Every verse of one surah that we need, in one call: recitation with word timings, the
   translation (footnote markers left out) and each word's meaning. */
async function surah(ch: string, recitation = RECITATION) {
  const t = await accessToken();                              // first: it settles which environment
  const q = `words=true&word_fields=text_uthmani&translations=${TRANSLATION}&audio=${recitation}&per_page=50`;
  const r = await fetch(`${ENVS[env].api}/verses/by_chapter/${ch}?${q}`, { headers: { 'x-auth-token': t, 'x-client-id': ID } });
  if (!r.ok) throw new Error(`surah ${ch} ${r.status}`);
  const out: Record<string, unknown> = {};
  for (const v of (await r.json()).verses || []) {
    const a = v.audio || {}, url = String(a.url || '');
    out[v.verse_key] = {
      url: !url ? null : /^https?:/.test(url) ? url : url.startsWith('//') ? 'https:' + url : AUDIO + url,
      segments: Array.isArray(a.segments) ? a.segments : [],
      translation: String(((v.translations || [])[0] || {}).text || '').replace(/<sup[^>]*>.*?<\/sup>/g, '').replace(/<[^>]+>/g, '').trim() || null,
      // each word's text too, so the app can match QF's words to its own (the Uthmani script
      // sometimes joins two words: يَٰٓأَيُّهَا is يا + أيها)
      words: (v.words || []).filter((w: { char_type_name: string }) => w.char_type_name === 'word')
        .map((w: { text_uthmani?: string, translation?: { text?: string } }) => ({ t: w.text_uthmani || '', en: (w.translation && w.translation.text) || '' })),
    };
  }
  return out;
}
/* The verses asked for, fetched a surah at a time (three at once); a surah that fails is
   left out, so its verses are read along with our own meanings rather than all failing. */
async function versesFor(keys: string[], recitation = RECITATION) {
  const chapters = [...new Set(keys.map(k => k.split(':')[0]))], out: Record<string, unknown> = {};
  let failed = 0;
  await Promise.all([0, 1, 2].map(async () => {
    for (let ch = chapters.shift(); ch; ch = chapters.shift()) {
      try { const got = await surah(ch, recitation); keys.forEach(k => { if (got[k]) out[k] = got[k]; }); }
      catch (e) { failed++; console.error(String(e)); }
    }
  }));
  return { out, failed };
}

const verseKeys = (v: unknown) => [...new Set((Array.isArray(v) ? v : [])
  .map(String).filter((k: string) => /^\d{1,3}:\d{1,3}$/.test(k)))].slice(0, 60) as string[];

/* Health check, no sign-in: {check: true, verses?: [...]} says whether the keys work and,
   per verse, whether QF returns audio, word timings, a translation and word meanings (the
   public audio link, the timings, and each word's Arabic to check the matching; no translation). At most once every 10 minutes per list of verses. */
const checked = new Map<string, { at: number, result: Record<string, unknown> }>();
async function health(list: string[], recitation = RECITATION) {
  const keys = (list.length ? list : ['1:1']).slice(0, 60), id = recitation + ':' + keys.join(',');
  const c = checked.get(id);
  if (c && Date.now() - c.at < 600_000) return c.result;
  const { out } = await versesFor(keys, recitation);
  const verses: Record<string, unknown> = {};
  keys.forEach(k => { const v = out[k] as { url: string, segments: unknown[], translation: string | null, words: { t: string, en: string }[] } | undefined;
    verses[k] = v ? { url: v.url, segments: v.segments, has_translation: !!v.translation, words: v.words.map(w => ({ t: w.t, has_en: !!w.en })) } : { error: 'missing' }; });
  const result = { ok: Object.keys(out).length > 0, env, recitation, translation: TRANSLATION, verses };
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
  const { out, failed } = await versesFor(keys);
  if (failed && !Object.keys(out).length) return json(req, { error: 'upstream' }, 502);
  return json(req, { verses: out, credit: CREDIT });
});
