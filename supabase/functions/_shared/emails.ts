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
    p('Each day, Home shows one <b>Continue</b> button. It takes you to the next step: the letters, then the basics (by the end you can introduce yourself in Arabic), then the units, with new words, conversations, short grammar notes and practice. Five to ten minutes a day is plenty.') +
    h('Your salah') +
    p('On Home you’ll also find <b>Your salah</b>: what every word of the prayer means, starting with the words you say most, plus ten short surahs. Pray along line by line, and the meanings stay with you.') +
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

// the two plans, as on the Plans page
const PLANS = `<ul style="margin:0 0 20px;padding-left:20px"><li><b>Essentials</b> £6.99 a month or £49.99 a year: the whole course, reviews, audio and practice, and the 20 words you say most in salah</li>` +
  `<li><b>Complete</b> £11.99 a month or £79.99 a year: everything, plus <b>Your salah</b> in full (every word of the prayer and 10 short surahs, with Pray along), the conversation partner, unlimited smart checks, real-life scenes and the weak-spots review</li></ul>`;

export function trialSoon(name: string | null | undefined, trialEnds: Date) {
  return { subject: 'Your free week of Rafiq ends in 2 days', html: frame(
    `<p style="margin:0 0 14px">${hi(name)}</p>` +
    p(`Your free week ends on <b>${endDay(trialEnds)}</b>. To keep learning after that, choose a plan. It takes a minute, and you can cancel any time.`) +
    h('Two plans') +
    PLANS +
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

// the day after the free week ends (#177): once, not paying
export function trialEnded(name: string | null | undefined) {
  return { subject: 'Your free week of Rafiq has ended', html: frame(
    `<p style="margin:0 0 14px">${hi(name)}</p>` +
    p('Your free week has ended. Everything you’ve learned is saved: your words, your progress and your streak are waiting where you left them.') +
    p('To carry on with your lessons and your salah, choose a plan. It takes a minute, and you can cancel any time.') +
    PLANS +
    btn('Choose a plan', `${SITE}/plans.html`) +
    p('Not happy after paying? Cancel within 14 days of your first payment and you’ll be refunded in full, automatically.') + p(support) +
    `<p style="margin:0 0 22px">The Rafiq team</p>`) };
}

// Subscribing (#178). Plans renew until cancelled; yearly is one payment a year.
const NAMES = { essentials: 'Rafiq Essentials', complete: 'Rafiq Complete' } as const;
const money = (pence: number) => `£${(pence / 100).toFixed(2)}`;
const every = (interval: string) => interval === 'year' ? 'year' : 'month';

// as soon as someone subscribes, whenever that is
export function subscribed(name: string | null | undefined, plan: 'essentials' | 'complete', interval: string, pence: number, firstCharge: Date | null) {
  const per = every(interval), when = firstCharge
    ? `Your first payment of <b>${money(pence)}</b> will be taken on <b>${endDay(firstCharge)}</b>, when your free week ends. Until then, everything stays free.`
    : `Your first payment of <b>${money(pence)}</b> has been taken today.`;
  return { subject: `Thank you for subscribing to ${NAMES[plan]}`, html: frame(
    `<p style="margin:0 0 14px">${hi(name)}</p>` +
    p(`Thank you for subscribing to <b>${NAMES[plan]}</b>. JazakAllahu khayran for supporting Rafiq.`) +
    h('Your plan') +
    `<ul style="margin:0 0 20px;padding-left:20px"><li><b>${NAMES[plan]}</b>, paid ${per === 'year' ? 'yearly' : 'monthly'}</li>` +
    `<li><b>${money(pence)}</b> a ${per}, renewing every ${per} until you cancel</li></ul>` +
    p(when) +
    p(`You can cancel any time in <b>Settings → Your plan</b>, and nothing more will be charged. Not happy? Cancel within 14 days of this first payment and you’ll be refunded in full, automatically.`) +
    btn('Continue learning', `${SITE}/login.html`) + p(support) +
    `<p style="margin:0 0 22px">The Rafiq team</p>`) };
}

// When someone cancels (#182): 'free' in the free week, 'refund' within 14 days (refunded, ended now),
// 'keep' otherwise (runs to the end of the period). askRefund: the automatic refund didn't go through.
export function cancelled(name: string | null | undefined, plan: 'essentials' | 'complete', kind: 'free' | 'refund' | 'keep',
                          o: { until?: Date | null; pence?: number; askRefund?: boolean } = {}) {
  const body = kind === 'free'
    ? p(`You’ve cancelled <b>${NAMES[plan]}</b> during your free week, so <b>you won’t be charged</b>.`) +
      (o.until ? p(`You can keep using everything until <b>${endDay(o.until)}</b>, when your free week ends.`) : '')
    : kind === 'refund'
    ? p(`You’ve cancelled <b>${NAMES[plan]}</b>, and because it was within 14 days of your payment, we’ve <b>refunded ${money(o.pence || 0)}</b> in full. It usually shows on your statement within 5–10 working days.`) +
      p('Your plan has ended. Your progress, words and streak are saved if you ever come back.')
    : p(`You’ve cancelled <b>${NAMES[plan]}</b>. Nothing more will be charged.`) +
      (o.until ? p(`You keep everything until <b>${endDay(o.until)}</b>, the end of the period you’ve paid for.`) : '') +
      (o.askRefund ? p('If you’d like a refund, just reply to this email and we’ll sort it out.') : '');
  const again = kind === 'refund'
    ? p(`Changed your mind? You can choose a plan again any time.`) + btn('See the plans', `${SITE}/plans.html`)
    : p(`Changed your mind? You can resume any time before then in <b>Settings → Your plan</b>.`) + btn('Open Settings', `${SITE}/settings.html`);
  return { subject: `You’ve cancelled ${NAMES[plan]}`, html: frame(
    `<p style="margin:0 0 14px">${hi(name)}</p>` + body + again +
    p('We’d love to know why you cancelled: just reply to this email. It really helps.') + p(support) +
    `<p style="margin:0 0 22px">The Rafiq team</p>`) };
}
