// support — "Report a problem" and the contact page (help.html):
//   {kind, message, page?, context?, email?} → {ok}
// Saves the message in `reports` and emails it to support@, with Reply going
// straight to the learner. Works signed in (the account's email is used) or
// signed out (they give an email), with a small limit per hour.
import { admin, caller, cors, json, sendEmail } from '../_shared/common.ts';

const KINDS: Record<string, string> = {
  answer: 'Something’s wrong with a question or answer', bug: 'Something isn’t working',
  billing: 'My plan or a payment', account: 'My account', idea: 'An idea', other: 'Something else',
};
const esc = (s: string) => s.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]!));
const clip = (s: unknown, n: number) => String(s ?? '').slice(0, n);

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: cors(req) });
  if (req.method !== 'POST') return json(req, { error: 'method' }, 405);
  const body = await req.json().catch(() => ({}));
  if (body.website) return json(req, { ok: true });                    // hidden field: only bots fill it in
  const user = await caller(req);
  const email = (user?.email || clip(body.email, 200)).trim();
  const message = clip(body.message, 4000).trim();
  const kind = KINDS[body.kind] ? body.kind : 'other';
  if (message.length < 3) return json(req, { error: 'message' }, 400);
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return json(req, { error: 'email' }, 400);

  const hourAgo = new Date(Date.now() - 3600_000).toISOString();
  const { count } = await admin.from('reports').select('id', { count: 'exact', head: true })
    .gte('created_at', hourAgo).eq(user ? 'user_id' : 'email', user ? user.id : email);
  if ((count || 0) >= 8) return json(req, { error: 'too_many' }, 429);

  const row = { user_id: user?.id ?? null, email, kind, message, page: clip(body.page, 300),
    context: clip(body.context, 3000), user_agent: clip(req.headers.get('user-agent'), 300) };
  const { data, error } = await admin.from('reports').insert(row).select('id').single();
  if (error) { console.error(error); return json(req, { error: 'server' }, 500); }

  const html = `<div style="font-family:Helvetica,Arial,sans-serif;font-size:15px;line-height:1.5;color:#17262B">
    <p style="margin:0 0 4px"><b>${esc(KINDS[kind])}</b> · report #${data.id}</p>
    <p style="margin:0 0 14px;color:#5C6B6E">From ${esc(email)}${user ? ` (account ${user.id})` : ' (not signed in)'} · ${esc(row.page || '—')}</p>
    <div style="white-space:pre-wrap;border-left:3px solid #2E7263;padding:4px 12px;margin:0 0 14px">${esc(message)}</div>
    ${row.context ? `<p style="margin:0 0 4px;color:#5C6B6E">On their screen:</p><div style="white-space:pre-wrap;font-size:13px;background:#F1ECE0;padding:10px 12px;border-radius:4px">${esc(row.context)}</div>` : ''}
    <p style="margin:14px 0 0;font-size:12px;color:#5C6B6E">${esc(row.user_agent || '')}</p></div>`;
  const text = `${KINDS[kind]} · report #${data.id}\nFrom ${email} · ${row.page}\n\n${message}\n\nOn their screen:\n${row.context}`;
  try { await sendEmail('support@rafiq-arabic.com', `[Rafiq] ${KINDS[kind]}: ${message.slice(0, 50)}`, html, text, email); }
  catch (e) { console.error(e); }                                        // it's saved either way
  return json(req, { ok: true, id: data.id });
});
