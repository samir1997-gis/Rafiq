/* supabase-auth.js — read or change the Supabase Auth settings (Management API).
   Run by the "Supabase auth settings" GitHub Action; needs the secrets
   SUPABASE_ACCESS_TOKEN (account → Access Tokens) and, for apply, RESEND_API_KEY.

     node tools/supabase-auth.js show
     node tools/supabase-auth.js apply            (CONFIRM=yes|no|keep, SENDER=…, TEMPLATES=dir)

   apply sets: site address + redirect addresses (added to what's there),
   Resend as the email sender, the branded templates in TEMPLATES (the
   subject is read from the comment on each file's first line), a higher
   email rate limit, passwords of at least 8 characters, 6-digit sign-in codes, and — only if CONFIRM=yes — "Confirm email". Secrets are
   never printed. */
const fs = require('fs'), path = require('path');
const REF = 'gaajfahtrbdybjuunfhe';                 // the Rafiq project (see auth.js)
const API = `https://api.supabase.com/v1/projects/${REF}/config/auth`;
const TOKEN = process.env.SUPABASE_ACCESS_TOKEN;
const SITE = 'https://rafiq-arabic.com';
const REDIRECTS = [`${SITE}/login.html`, `${SITE}/reset-password.html`, `${SITE}/**`];
const TEMPLATES = { confirmation: 'confirm-signup.html', recovery: 'reset-password.html', magic_link: 'sign-in-code.html' };

async function call(method, body) {
  const r = await fetch(API, { method, headers: { Authorization: `Bearer ${TOKEN}`, 'Content-Type': 'application/json' },
                               body: body ? JSON.stringify(body) : undefined });
  const t = await r.text();
  if (!r.ok) { console.error(`${method} failed: ${r.status} ${t.slice(0, 400)}`); process.exit(1); }
  return t ? JSON.parse(t) : {};
}

function summary(c) {
  const len = s => (s ? `${s.length} chars` : 'default');
  return {
    site_url: c.site_url, redirect_urls: c.uri_allow_list,
    confirm_email: c.mailer_autoconfirm === false ? 'ON (people must click the link)' : 'OFF (accounts work straight away)',
    email_sender: c.smtp_host ? `${c.smtp_sender_name || ''} <${c.smtp_admin_email}> via ${c.smtp_host}:${c.smtp_port}` : 'Supabase built-in (a few emails an hour)',
    emails_per_hour: c.rate_limit_email_sent, password_min_length: c.password_min_length,
    confirm_subject: c.mailer_subjects_confirmation, confirm_template: len(c.mailer_templates_confirmation_content),
    reset_subject: c.mailer_subjects_recovery, reset_template: len(c.mailer_templates_recovery_content),
    code_subject: c.mailer_subjects_magic_link, code_template: len(c.mailer_templates_magic_link_content),
    code_length: c.mailer_otp_length, code_expires_s: c.mailer_otp_exp,
  };
}

async function resendCheck(sender) {
  const key = process.env.RESEND_API_KEY;
  if (!key) return console.log('RESEND_API_KEY: not set');
  const r = await fetch('https://api.resend.com/domains', { headers: { Authorization: `Bearer ${key}` } });
  const j = await r.json().catch(() => ({}));
  if (!r.ok) return console.log(`RESEND_API_KEY: set (a sending-only key can't list domains: ${j.name || r.status})`);
  (j.data || []).forEach(d => console.log(`Resend domain: ${d.name} — ${d.status}${sender && sender.endsWith('@' + d.name) ? '  ← sender' : ''}`));
}

function template(dir, file) {
  const p = path.join(dir, file);
  if (!fs.existsSync(p)) return null;
  const html = fs.readFileSync(p, 'utf8');
  const m = html.match(/Subject:\s*([^>]+?)\s*-->/);
  return { subject: m && m[1], html: html.replace(/^<!--[\s\S]*?-->\s*/, '') };
}

(async () => {
  if (!TOKEN) { console.error('SUPABASE_ACCESS_TOKEN is not set'); process.exit(1); }
  const cmd = process.argv[2] || 'show';
  const now = await call('GET');
  const sender = process.env.SENDER || 'hello@contact.rafiq-arabic.com';
  if (cmd === 'show') { console.log(JSON.stringify(summary(now), null, 2)); await resendCheck(sender); return; }
  if (cmd !== 'apply') { console.error('use: show | apply'); process.exit(1); }

  const key = process.env.RESEND_API_KEY;
  if (!key) { console.error('RESEND_API_KEY is not set'); process.exit(1); }
  const urls = new Set((now.uri_allow_list || '').split(',').map(s => s.trim()).filter(Boolean));
  REDIRECTS.forEach(u => urls.add(u));
  const patch = {
    site_url: SITE, uri_allow_list: [...urls].join(','),
    external_email_enabled: true,
    smtp_host: 'smtp.resend.com', smtp_port: '465', smtp_user: 'resend', smtp_pass: key,
    smtp_admin_email: sender, smtp_sender_name: 'Rafiq',
    rate_limit_email_sent: Math.max(now.rate_limit_email_sent || 0, 100),
    password_min_length: Math.max(now.password_min_length || 0, 8),
    mailer_otp_length: 6,                            // sign-in codes (login.html): 6 digits
  };
  const dir = process.env.TEMPLATES || 'supabase/email-templates';
  for (const [kind, file] of Object.entries(TEMPLATES)) {
    const t = template(dir, file);
    if (!t) { console.log(`template ${file}: not found in ${dir}, left as it is`); continue; }
    patch[`mailer_templates_${kind}_content`] = t.html;
    if (t.subject) patch[`mailer_subjects_${kind}`] = t.subject;
  }
  const confirm = (process.env.CONFIRM || 'keep').toLowerCase();
  if (confirm === 'yes') patch.mailer_autoconfirm = false;
  if (confirm === 'no') patch.mailer_autoconfirm = true;

  console.log('Before:', JSON.stringify(summary(now), null, 2));
  const after = await call('PATCH', patch);
  console.log('After:', JSON.stringify(summary(after), null, 2));
  await resendCheck(sender);
})();
