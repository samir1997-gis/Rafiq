/* app-store.js — only inside the iPhone and Android app (#352). app/build-web.js adds it to the app's copies of
   plans.html and settings.html; the website never loads it, and it does nothing outside the app.

   Apple (3.1.1) and Google only allow their own in-app purchase for subscriptions bought in an app, so in the app:
   - Plans is the App Store / Google Play subscription screen, through RevenueCat (#345, #346): Essentials and
     Complete, yearly or monthly, at the store's own prices, the terms Apple asks for (3.1.2: renews automatically,
     how to cancel, Terms and Privacy), and Restore purchases. A purchase is tied to the Rafiq account (RevenueCat's
     app user id = the account id), and the store-webhook function writes it to the account's billing row.
     Until the store products and the RevenueCat keys exist, it shows the plans with "opening soon", never Stripe.
   - Settings never offers Stripe's own pages (Manage billing, Billing history) or Stripe actions: a plan bought on
     the website is just said to be managed there. */
(function(){
  const C = window.Capacitor;
  if(!(C && C.isNativePlatform && C.isNativePlatform())) return;
  const IOS = C.getPlatform && C.getPlatform() === 'ios';
  // RevenueCat's public SDK keys (appl_… and goog_…): safe to ship in an app. Filled in once RevenueCat is set up (#346).
  const KEYS = { ios: '', android: '' };
  const KEY = IOS ? KEYS.ios : KEYS.android;
  const STORE = IOS ? 'the App Store' : 'Google Play';
  const MANAGE = IOS ? 'https://apps.apple.com/account/subscriptions' : 'https://play.google.com/store/account/subscriptions';
  const page = location.pathname.split('/').pop() || 'dashboard.html';
  const esc = t => String(t).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const NAME = { essentials: 'Essentials', complete: 'Complete' };
  const open = url => { try{ if(C.Plugins.Browser) return C.Plugins.Browser.open({ url }); }catch(_){} location.href = url; };

  /* ---------------- Settings: no Stripe pages or actions in the app ---------------- */
  if(page === 'settings.html'){
    const STRIPE = /^(Cancel subscription|Manage billing|Billing history|Resume my plan)$/;
    const tidy = () => {
      const acts = document.getElementById('planActs'), info = document.getElementById('planInfo'), P = window.RafiqPlan;
      if(!acts || !P) return;
      const s = P.state();
      [...acts.children].forEach(b => { if(STRIPE.test(b.textContent.trim())) b.remove(); });
      if(s.kind === 'paid' && s.source === 'stripe' && info && !/rafiq-arabic\.com/.test(info.textContent))
        info.textContent += ' Bought on rafiq-arabic.com: change or cancel it there.';
      const box = document.getElementById('cancelBox'); if(box) box.hidden = true;
    };
    const watch = () => { const acts = document.getElementById('planActs'); if(!acts) return;
      new MutationObserver(tidy).observe(acts, { childList: true }); tidy(); };
    if(document.readyState === 'loading') addEventListener('DOMContentLoaded', watch); else watch();
    return;
  }
  if(page !== 'plans.html') return;

  /* ---------------- Plans: the store's subscription screen ---------------- */
  const P = window.RafiqPlan;
  const main = document.querySelector('main');
  const feats = {};                                           // each plan's list, as the page has it
  document.querySelectorAll('.card[data-plan]').forEach(c => { const ul = c.querySelector('ul'); feats[c.dataset.plan] = ul ? ul.innerHTML : ''; });
  ['.toggle', '.cards', '.fine', '#msg'].forEach(s => { const e = document.querySelector(s); if(e) e.remove(); });
  const st = document.createElement('style'); st.textContent = `
.sp-seg{display:flex;justify-content:center;margin:6px 0 16px}
.sp-seg .seg{display:inline-flex;background:var(--paper-deep);border-radius:999px;padding:4px}
.sp-seg button{border:0;background:none;border-radius:999px;padding:8px 18px;font:700 14px var(--la);color:var(--ink-soft);cursor:pointer}
.sp-seg button.on{background:var(--card);color:var(--ink);box-shadow:0 2px 8px -4px rgba(0,0,0,.3)}
.sp-cards{display:grid;gap:14px}
.sp-card{background:var(--card);border:1px solid var(--rule);border-radius:18px;padding:18px}
.sp-card.best{border:2px solid var(--verdigris)}
.sp-card h2{font-size:20px;margin:0 0 4px}.sp-price{font-size:26px;font-weight:800}.sp-price small{font-size:14px;font-weight:600;color:var(--ink-soft)}
.sp-per{font-size:13.5px;color:var(--ink-soft);margin-top:2px}.sp-trial{font-size:13.5px;font-weight:700;color:var(--verdigris);margin-top:4px}
.sp-card ul{list-style:none;padding:0;margin:12px 0 14px;display:grid;gap:7px;font-size:14px}
.sp-card li::before{content:'✓ ';color:var(--verdigris);font-weight:800}
.sp-card .btn{width:100%}.sp-msg{min-height:20px;margin:12px 0;font-size:14px;font-weight:600;color:var(--rubric);text-align:center}
.sp-restore{display:block;margin:4px auto 0;background:none;border:0;color:var(--verdigris);font:700 14px var(--la);text-decoration:underline;cursor:pointer;padding:10px}
.sp-fine{font-size:12.5px;line-height:1.55;color:var(--ink-soft);margin-top:14px}.sp-fine a{color:var(--ink-soft)}
@media (min-width:860px){.sp-cards{grid-template-columns:1fr 1fr}}`;
  document.head.appendChild(st);
  const box = document.createElement('div');
  box.innerHTML = `<div class="sp-seg"><div class="seg" role="group" aria-label="Billing period">
      <button type="button" data-i="year" class="on">Yearly</button><button type="button" data-i="month">Monthly</button></div></div>
    <div class="sp-cards">${['essentials', 'complete'].map(p => `<section class="sp-card${p === 'complete' ? ' best' : ''}" data-plan="${p}">
      <h2>${NAME[p]}</h2><div class="sp-price" data-price>…</div><div class="sp-per" data-per></div><div class="sp-trial" data-trial></div>
      <ul>${feats[p] || ''}</ul><button class="btn" type="button" data-buy>Choose ${NAME[p]}</button></section>`).join('')}</div>
    <div class="sp-msg" id="spMsg" role="alert"></div>
    <button class="sp-restore" type="button" id="spRestore">Restore purchases</button>
    <p class="sp-fine">${IOS
      ? 'Payment is charged to your Apple ID at confirmation of purchase. Your subscription renews automatically for the same period and price unless you cancel it at least 24 hours before the end of the current period; the renewal is charged within the 24 hours before the period ends. You can manage or cancel it any time in your App Store account settings (Settings → your name → Subscriptions).'
      : 'Payment is charged to your Google Play account. Your subscription renews automatically for the same period and price until you cancel it. You can manage or cancel it any time in Google Play (Payments & subscriptions → Subscriptions).'}
      If a free week is offered and you cancel before it ends, you won’t be charged.
      <br><a href="terms.html">Terms of use</a> · <a href="privacy.html">Privacy policy</a> · <a href="help.html?kind=billing">Get help</a></p>`;
  main.appendChild(box);
  const msg = t => { document.getElementById('spMsg').textContent = t || ''; };

  let interval = 'year', packs = {}, configured = null;
  const planOf = id => (/complete/.test(id) ? 'complete' : /essentials/.test(id) ? 'essentials' : null);
  const intervalOf = (id, pk) => (/year|annual/.test(id) || pk.packageType === 'ANNUAL' ? 'year' : 'month');
  function paint(){
    box.querySelectorAll('.sp-seg button').forEach(b => b.classList.toggle('on', b.dataset.i === interval));
    const s = P ? P.state() : {};
    box.querySelectorAll('.sp-card').forEach(c => {
      const pk = packs[c.dataset.plan + ':' + interval], pr = pk && pk.product;
      c.querySelector('[data-price]').innerHTML = pr ? `${esc(pr.priceString)} <small>/ ${interval}</small>` : (configured === false ? 'Opening soon' : '…');
      c.querySelector('[data-per]').textContent = pr && interval === 'year' && pr.pricePerMonthString ? `That’s ${pr.pricePerMonthString} a month` : '';
      const intro = pr && pr.introPrice;
      c.querySelector('[data-trial]').textContent = intro && intro.price === 0 ? 'Starts with a free week for new subscribers' : '';
      const cur = s.kind === 'paid' && s.plan === c.dataset.plan, b = c.querySelector('[data-buy]');
      b.textContent = cur ? 'Your plan' : `Choose ${NAME[c.dataset.plan]}`;
      b.disabled = !pr || (s.kind === 'paid');
    });
    const status = document.getElementById('status');
    if(status && s.kind === 'trial' && !s.team) status.innerHTML = `Your free week ends on <b>${P.dateText(s.trialEndsAt)}</b> (${s.daysLeft} day${s.daysLeft === 1 ? '' : 's'} left).`;   // the website's line about the first payment is Stripe's
    if(status && s.kind === 'paid') status.innerHTML = s.source === 'stripe'
      ? `You're on <b>${NAME[s.plan]}</b>, bought on rafiq-arabic.com: change or cancel it there.`
      : `You're on <b>${NAME[s.plan]}</b>, bought through ${s.source === 'apple' ? 'the App Store' : 'Google Play'}. <a href="#" id="spManage">Manage it</a>`;
    const m = document.getElementById('spManage'); if(m) m.onclick = e => { e.preventDefault(); open(MANAGE); };
  }
  box.querySelectorAll('.sp-seg button').forEach(b => b.onclick = () => { interval = b.dataset.i; paint(); });

  async function setup(){
    const R = C.Plugins && C.Plugins.Purchases, uid = typeof currentUserId === 'function' ? await currentUserId().catch(() => null) : null;
    if(!R || !KEY || !uid){ configured = false; paint(); return null; }
    try{
      await R.configure({ apiKey: KEY, appUserID: uid });       // purchases belong to this Rafiq account
      const o = await R.getOfferings(), cur = o && o.current;
      (cur ? cur.availablePackages : []).forEach(pk => { const id = pk.product.identifier, p = planOf(id); if(p) packs[p + ':' + intervalOf(id, pk)] = pk; });
      configured = Object.keys(packs).length > 0;
    }catch(_){ configured = false; }
    paint(); return configured ? R : null;
  }
  const ready = setup();

  // after a purchase or restore the store tells our server (store-webhook); wait for the plan to show up here
  async function settle(){
    for(let k = 0; k < 10; k++){ await new Promise(r => setTimeout(r, 2000)); await P.load().catch(() => {}); if(P.state().kind === 'paid') return true; }
    return false;
  }
  box.querySelectorAll('[data-buy]').forEach(b => b.onclick = async () => {
    const R = await ready, pk = packs[b.closest('.sp-card').dataset.plan + ':' + interval];
    if(!R || !pk) return;
    const label = b.textContent; b.disabled = true; b.textContent = `Opening ${STORE}…`; msg('');
    try{
      await R.purchasePackage({ aPackage: pk });
      b.textContent = 'Setting up your plan…';
      if(await settle()){ location.href = 'settings.html?plan=done'; return; }
      msg('Thank you! Your plan is being set up and will show in a moment.');
    }catch(e){
      if(!(e && (e.userCancelled || String(e.code) === '1'))) msg(`That didn’t go through. Please try again, or email support@rafiq-arabic.com.`);
    }
    b.disabled = false; b.textContent = label; paint();
  });
  document.getElementById('spRestore').onclick = async e => {
    const R = await ready, b = e.target;
    if(!R){ msg('Subscriptions in the app are opening soon.'); return; }
    b.disabled = true; b.textContent = 'Restoring…'; msg('');
    try{
      const r = await R.restorePurchases(), active = r && r.customerInfo && Object.keys(r.customerInfo.entitlements && r.customerInfo.entitlements.active || {}).length;
      if(active){ await settle(); paint(); msg(''); document.getElementById('status').scrollIntoView({ block: 'center' }); }
      else msg(`No subscription found for this ${IOS ? 'Apple ID' : 'Google account'}.`);
    }catch(_){ msg('Restoring didn’t work. Please try again.'); }
    b.disabled = false; b.textContent = 'Restore purchases';
  };
  if(P) P.load().then(paint).catch(() => {});
  paint();
})();
