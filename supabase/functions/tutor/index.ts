// tutor — the AI tutor (#127), for Complete learners:
//   {mode: 'chat'|'why', messages: [{role: 'user'|'assistant', content}], context} → the answer,
//   streamed as plain text. context is what the page knows: the learner's unit, its words and
//   grammar notes, their recurring mistakes, the salah lines, or (for 'why') what's on screen.
// Checks the learner is signed in and on Complete, keeps to a daily limit, asks Claude with the
// key kept here (the function secret ANTHROPIC_API_KEY), and logs each question, its answer and
// the tokens used in public.tutor_usage so costs and answers can be checked.
import { admin, caller, cors as siteCors } from '../_shared/common.ts';

// The branch preview (raw.githack.com) may call it too, as with the quran function.
const PREVIEW = 'https://raw.githack.com';
const cors = (req: Request) => req.headers.get('origin') === PREVIEW
  ? { ...siteCors(req), 'Access-Control-Allow-Origin': PREVIEW } : siteCors(req);
const json = (req: Request, body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { ...cors(req), 'Content-Type': 'application/json' } });

const BETA = true;               // as in plan.js: everyone has Complete until launch; set both to false together
const KEY = Deno.env.get('ANTHROPIC_API_KEY') || '';
const MODEL = 'claude-sonnet-5-5';
const DAILY = 20;                // questions a day, "Why?" included (#127: keeps the worst case near £3.30 a month)
const MAX_TOKENS = { chat: 800, why: 400 };

const PROMPT = `You are Rafiq's tutor. Rafiq (rafiq-arabic.com) teaches Modern Standard Arabic to Muslims in the UK. Most learners are adult beginners who want to understand their prayers and the Quran, and to speak everyday Arabic. Learners reach you in two ways:
- the Tutor tab, where they can ask anything about Arabic or the course;
- a "Why?" button after they get a question wrong in a lesson, where you're shown what was on their screen.

How to answer
- Plain, warm British English for a beginner. Explain a grammar term the first time you use it, e.g. "the idafa (two nouns side by side meaning 'the X of Y')".
- Keep it short: usually 2 to 6 sentences and never more than about 250 words. Give the answer first, then the reason, then one or two examples. No preamble and no "Great question".
- Write Arabic with full vowel marks, as the course does, with the English meaning next to it. Add transliteration only if the learner asks for it or says they can't read Arabic script yet.
- Teach Modern Standard Arabic, as the course does. If asked about a dialect, say briefly that Rafiq teaches MSA and how the two differ, without teaching the dialect.
- Build on what the learner has met: their current unit's words and grammar notes are given below. Prefer those words in your examples. Where your explanation matches a course note, use the course's wording and mention the note (e.g. "the How it works note on هَذا / هَذِهِ").
- Plain text only. Short lists starting with "- ", **bold** and *italic* are fine; no headings, tables or code blocks.
- If a question is unclear, ask one short question back rather than guessing.

Being right
- The course material below has been checked by a teacher. Treat it as correct and keep to it. If it seems to disagree with what you know, say what the course says and suggest the learner reports it with the ⚑ button.
- If you aren't sure, say so plainly and suggest asking a teacher. Never invent a word, a rule, a hadith, a verse or a reference.
- The Quran: use only the translation and word meanings given below (from the Quran Foundation: Saheeh International, and Quran.com's word by word). For a verse that isn't given, you may explain its words and grammar, but don't give your own translation of the whole verse: point to a published translation. Never give your own tafsir (commentary on what a verse means); suggest a teacher or a recognised tafsir.
- No religious rulings (fiqh), such as whether a prayer is valid or what to do after a mistake in salah: say kindly that it's a question for their imam or a teacher. You can explain what the Arabic of a prayer means.
- Stay on Arabic, the course and learning it. For anything else, say in one sentence that you're here for Arabic and offer to help with that.

"Why?" after a wrong answer
- You'll see the screen: the question, the choices or what the learner typed, and usually the right answer.
- Say what the right answer is and why, pointing at exactly what went wrong in theirs (a gender ending, the wrong person of the verb, two letters that sound alike, a word from the wrong unit…). If their answer was also acceptable, say so and suggest they report the question with the ⚑ button.
- End with one small tip to remember it. Keep it under about 100 words.`;

type Turn = { role: 'user' | 'assistant', content: string };
// The last few turns of the chat, starting and ending with the learner.
function turns(list: unknown): Turn[] {
  const out: Turn[] = (Array.isArray(list) ? list : []).slice(-10)
    .filter(m => m && (m.role === 'user' || m.role === 'assistant') && typeof m.content === 'string' && m.content.trim())
    .map(m => ({ role: m.role, content: m.content.slice(0, 2000) }));
  while (out.length && out[0].role !== 'user') out.shift();
  return out.length && out[out.length - 1].role === 'user' ? out : [];
}

async function complete(uid: string) {
  if (BETA) return true;
  const { data: b } = await admin.from('billing').select('plan, status, trial_ends_at').eq('user_id', uid).maybeSingle();
  if (!b) return false;
  if (b.plan && ['active', 'trialing', 'past_due'].includes(b.status)) return b.plan === 'complete';
  return new Date(b.trial_ends_at).getTime() > Date.now();          // the free week is Complete
}

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: cors(req) });
  if (req.method !== 'POST') return json(req, { error: 'method' }, 405);
  if (!KEY) return json(req, { error: 'not_configured' }, 503);
  const user = await caller(req);
  if (!user) return json(req, { error: 'signin' }, 401);
  if (!(await complete(user.id))) return json(req, { error: 'plan' }, 403);

  const body = await req.json().catch(() => ({}));
  const mode: 'chat' | 'why' = body.mode === 'why' ? 'why' : 'chat';
  const messages = turns(body.messages);
  if (!messages.length) return json(req, { error: 'message' }, 400);
  const context = String(body.context ?? '').slice(0, 12000);

  const today = new Date().toISOString().slice(0, 10) + 'T00:00:00Z';
  const { count } = await admin.from('tutor_usage').select('id', { count: 'exact', head: true })
    .eq('user_id', user.id).gte('created_at', today);
  if ((count || 0) >= DAILY) return json(req, { error: 'limit', limit: DAILY }, 429);

  const r = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: { 'x-api-key': KEY, 'anthropic-version': '2023-06-01', 'content-type': 'application/json' },
    body: JSON.stringify({
      model: MODEL, max_tokens: MAX_TOKENS[mode], stream: true, messages,
      // the fixed prompt is cached (a tenth of the price); the learner's context follows it
      system: [{ type: 'text', text: PROMPT, cache_control: { type: 'ephemeral' } },
               { type: 'text', text: (mode === 'why' ? 'On the learner\'s screen:\n' : 'About this learner:\n') + (context || '(nothing given)') }],
    }),
  });
  if (!r.ok || !r.body) { console.error('anthropic', r.status, (await r.text()).slice(0, 300)); return json(req, { error: 'upstream' }, 502); }

  // Claude streams server-sent events; pass on only the text, and log the usage at the end.
  const usage = { input_tokens: 0, output_tokens: 0, cache_read_tokens: 0, cache_write_tokens: 0 };
  let answer = '';
  const enc = new TextEncoder(), dec = new TextDecoder();
  const stream = new ReadableStream({
    async start(ctl) {
      const reader = r.body!.getReader(); let buf = '';
      try {
        for (;;) {
          const { value, done } = await reader.read();
          if (done) break;
          buf += dec.decode(value, { stream: true });
          let i;
          while ((i = buf.indexOf('\n')) >= 0) {
            const line = buf.slice(0, i).trim(); buf = buf.slice(i + 1);
            if (!line.startsWith('data:')) continue;
            const e = JSON.parse(line.slice(5));
            if (e.type === 'message_start') {
              const u = e.message.usage || {};
              usage.input_tokens = u.input_tokens || 0;
              usage.cache_read_tokens = u.cache_read_input_tokens || 0;
              usage.cache_write_tokens = u.cache_creation_input_tokens || 0;
            } else if (e.type === 'content_block_delta' && e.delta.type === 'text_delta') {
              answer += e.delta.text; ctl.enqueue(enc.encode(e.delta.text));
            } else if (e.type === 'message_delta' && e.usage) usage.output_tokens = e.usage.output_tokens || 0;
          }
        }
      } catch (err) { console.error('stream', err); }
      ctl.close();
      const { error } = await admin.from('tutor_usage').insert({ user_id: user.id, mode, model: MODEL, ...usage,
        question: messages[messages.length - 1].content, answer: answer.slice(0, 4000) });
      if (error) console.error('usage', error.message);
    },
  });
  return new Response(stream, { headers: { ...cors(req), 'Content-Type': 'text/plain; charset=utf-8', 'Cache-Control': 'no-store' } });
});
