// The emails Rafiq sends itself (sign-up confirmation and password reset are
// Supabase's, in supabase/email-templates). Same look as those.
import { SITE } from './common.ts';

const esc = (s: string) => s.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]!));
const hi = (name?: string | null) => {
  const n = (name || '').trim().split(/\s+/)[0];
  return n ? `Assalamu alaykum ${esc(n)},` : 'Assalamu alaykum,';
};
const h = (t: string) => `<p style="margin:0 0 6px;font-weight:bold">${t}</p>`;
const p = (t: string) => `<p style="margin:0 0 20px">${t}</p>`;
const btn = (label: string, href: string) =>
  `</td></tr><tr><td align="center" style="padding:0 22px 26px"><a href="${href}" style="display:inline-block;background:#2E7263;color:#F1ECE0;text-decoration:none;font-size:16px;padding:13px 28px;border-radius:3px">${label}</a></td></tr><tr><td style="padding:0 22px 0;font-size:16px;line-height:1.6">`;
const support = `Questions? Email <a href="mailto:support@rafiq-arabic.com" style="color:#2E7263">support@rafiq-arabic.com</a> and a real person will reply.`;

function frame(body: string) {
  return `<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#F1ECE0;padding:24px 10px;font-family:Helvetica,Arial,sans-serif;color:#17262B">
  <tr><td align="center">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:520px;background:#FFFFFF;border:1px solid #E2DACB;border-radius:6px">
      <tr><td style="padding:28px 22px 8px;text-align:center">
        <div style="display:inline-block;width:52px;height:52px;line-height:52px;border-radius:12px;background:#17262B;color:#F1ECE0;font-size:30px;font-family:serif">ر</div>
        <div style="font-size:30px;font-family:serif;margin-top:10px" dir="rtl">رَفِيق</div>
      </td></tr>
      <tr><td style="padding:8px 22px 8px;font-size:16px;line-height:1.6">${body}</td></tr>
    </table>
    <p style="font-size:12px;color:#5C6B6E;margin:16px 0 0">Rafiq · rafiq-arabic.com</p>
  </td></tr>
</table>`;
}
// a plain-text copy for mail apps that don't show HTML
export const text = (html: string) => html.replace(/<li>/g, '• ').replace(/<br>/g, '\n').replace(/<\/(p|li|ul|div|tr)>/g, '\n')
  .replace(/<a [^>]*href="(https[^"]+)"[^>]*>([^<]+)<\/a>/g, '$2: $1').replace(/<[^>]+>/g, '')
  .replace(/&amp;/g, '&').replace(/[ \t]+/g, ' ').replace(/\n\s*\n\s*/g, '\n\n').trim();

const endDay = (d: Date) => d.toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long', timeZone: 'Europe/London' });

export function welcome(name: string | null | undefined, trialEnds: Date) {
  return { subject: 'Welcome to Rafiq – here’s how to get started', html: frame(
    `<p style="margin:0 0 14px">${hi(name)}</p>` +
    p('Welcome to Rafiq. We’re glad you’re here. A few things will help you get the most from your first week.') +
    h('1. Watch the two short videos') +
    p(`<b>How Rafiq works</b> (79 seconds) shows your path, reviews, practice and feedback. The <b>one-minute film</b> shows why Rafiq helps words stick. Both are on the <a href="${SITE}/#how-section" style="color:#2E7263">Rafiq home page</a>, and they’ll save you a lot of guessing.`) +
    h('2. Just press Continue') +
    p('Each day, Home shows one <b>Continue</b> button. It takes you to the next step: new words, a conversation, a short grammar note or practice. Five to ten minutes a day is plenty.') +
    h('3. Let the reviews do their job') +
    p('Words come back for review just as you’re likely to forget them. Doing your reviews is what makes them stay. Missed a day? Just carry on.') +
    h('4. Explore Practise when you want more') +
    p('Verbs, joining words, a spelling bee, everyday essentials (numbers, days, months, colours) and real-life scenes are all in <b>Practise</b>.') +
    h('Your free week') +
    p(`You have every part of Rafiq free until <b>${endDay(trialEnds)}</b>. No card needed. Before it ends, you can choose a plan to keep going. Your progress is always kept.`) +
    btn('Continue learning', `${SITE}/login.html`) +
    p('Tip: add Rafiq to your phone’s home screen so it opens like an app.') +
    p(support) +
    `<p style="margin:0 0 22px">JazakAllahu khayran,<br>The Rafiq team</p>`) };
}

export function trialSoon(name: string | null | undefined, trialEnds: Date) {
  return { subject: 'Your free week of Rafiq ends in 2 days', html: frame(
    `<p style="margin:0 0 14px">${hi(name)}</p>` +
    p(`Your free week ends on <b>${endDay(trialEnds)}</b>. To keep learning after that, choose a plan. It takes a minute, and you can cancel any time.`) +
    h('Two plans') +
    `<ul style="margin:0 0 20px;padding-left:20px"><li><b>Essentials</b> £6.99 a month or £49.99 a year: the whole course, reviews, audio and practice</li>` +
    `<li><b>Complete</b> £11.99 a month or £79.99 a year: everything, plus the conversation partner, unlimited smart checks, real-life scenes and the weak-spots review</li></ul>` +
    btn('Choose a plan', `${SITE}/plans.html`) +
    p('Your progress, streak and words are kept whatever you decide.') + p(support) +
    `<p style="margin:0 0 22px">The Rafiq team</p>`) };
}

export function trialLast(name: string | null | undefined) {
  return { subject: 'Last day of your free week', html: frame(
    `<p style="margin:0 0 14px">${hi(name)}</p>` +
    p('Today is the last day of your free week. Choose a plan to carry on from where you are. Everything you’ve learned is saved.') +
    btn('Choose a plan', `${SITE}/plans.html`) + p(support) +
    `<p style="margin:0 0 22px">The Rafiq team</p>`) };
}
