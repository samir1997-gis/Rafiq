// Shared by the Rafiq Edge Functions: CORS, the admin client, who is calling,
// and sending email through Resend.
import { createClient, type SupabaseClient } from 'npm:@supabase/supabase-js@2';

export const SITE = 'https://rafiq-arabic.com';
const ORIGINS = [SITE, 'https://www.rafiq-arabic.com', 'http://localhost:8765'];

export function cors(req: Request): Record<string, string> {
  const o = req.headers.get('origin') || '';
  return {
    'Access-Control-Allow-Origin': ORIGINS.includes(o) ? o : SITE,
    'Access-Control-Allow-Headers': 'authorization, content-type, apikey, x-client-info',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Vary': 'Origin',
  };
}
export const json = (req: Request, body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { ...cors(req), 'Content-Type': 'application/json' } });

// The service key is provided to every Edge Function by Supabase; it never reaches the browser.
export const admin: SupabaseClient = createClient(
  Deno.env.get('SUPABASE_URL')!, Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!,
  { auth: { persistSession: false, autoRefreshToken: false } });

// The signed-in learner making this request, checked with Supabase (not just decoded).
export async function caller(req: Request) {
  const token = (req.headers.get('authorization') || '').replace(/^Bearer\s+/i, '');
  if (!token) return null;
  const { data, error } = await admin.auth.getUser(token);
  return error || !data.user ? null : data.user;
}

// Calls from the database (welcome email, daily reminders) carry this shared secret.
export const fromHook = (req: Request) => {
  const s = Deno.env.get('HOOK_SECRET');
  return !!s && req.headers.get('x-rafiq-hook') === s;
};

export async function sendEmail(to: string, subject: string, html: string, text: string, replyTo = 'support@rafiq-arabic.com') {
  const r = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${Deno.env.get('RESEND_API_KEY')}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ from: 'Rafiq <hello@contact.rafiq-arabic.com>', to: [to],
      reply_to: replyTo, subject, html, text }),
  });
  if (!r.ok) throw new Error(`email failed: ${r.status} ${(await r.text()).slice(0, 200)}`);
}
