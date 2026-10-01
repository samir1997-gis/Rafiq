/* plan.js — subscriptions and the free week.

     Essentials  £6.99/month or £49.99/year
       the whole course, all practice, audio and review, and
       ESSENTIALS_CHECKS smart checks a day (a judgment by the TypeSafe Worker);
       past that, checks fall back to ordinary matching.
     Complete    £11.99/month or £79.99/year
       everything in Essentials, plus unlimited smart checks, the
       conversation partner, real-life scenes, the weak-spots review,
       speaking feedback, the mistake focus and first access to new units.

   Every account starts with a free week of Complete, no card needed (chosen with
   TypeSafe: tools/typesafe-exp/trial_model.py). Then lessons ask for a plan, but
   Home, Progress and the word list stay open, so nothing feels lost.

   The account's row in Supabase's `billing` table is the truth (written only by
   the server: supabase/functions). It's cached in localStorage so pages can
   decide straight away, and refreshed on every page.

   BETA = true gives everyone Complete and never asks anyone to pay. Set it to
   false at launch, once Stripe is set up (README → "Taking payments"). */
(function(){
  const BETA = true;
  const ESSENTIALS_CHECKS = 25;
  const PRICES = {
    essentials: { monthly:'£6.99',  yearly:'£49.99' },
    complete:   { monthly:'£11.99', yearly:'£79.99' },
  };
  const PAYING = ['active','trialing','past_due'];
  const CACHE = 'rafiq_billing';
  const KEY = 'rafiq_checks';
  const DAY = 86400000;
  const today = () => new Date().toISOString().slice(0,10);
  const read = () => { try{ const r=JSON.parse(localStorage.getItem(KEY)||'{}'); return r.day===today() ? r : {day:today(), n:0}; }catch(_){ return {day:today(), n:0}; } };

  let row = (() => { try{ return JSON.parse(localStorage.getItem(CACHE)||'null'); }catch(_){ return null; } })();

  /* Where the account stands:
       kind 'paid'  — a subscription (plan, interval, periodEnd, cancelAtPeriodEnd)
            'trial' — in the free week (daysLeft, trialEndsAt)
            'ended' — free week over, no plan
            'unknown' — not loaded yet (treated as allowed) */
  function state(){
    if(!row) return {kind:'unknown'};
    const s = { plan:row.plan, status:row.status, interval:row.interval, trialEndsAt:row.trial_ends_at ? new Date(row.trial_ends_at) : null,
                periodEnd:row.current_period_end ? new Date(row.current_period_end) : null, cancelAtPeriodEnd:!!row.cancel_at_period_end,
                hasCustomer:!!row.stripe_customer_id };
    if(row.plan && PAYING.includes(row.status)) return {...s, kind:'paid'};
    const left = s.trialEndsAt ? s.trialEndsAt - Date.now() : -1;
    if(left > 0) return {...s, kind:'trial', daysLeft:Math.ceil(left / DAY)};
    return {...s, kind:'ended'};
  }

  /* 'complete' | 'essentials' | null (must choose a plan) */
  function tier(){
    if(BETA) return 'complete';
    try{ const t=localStorage.getItem('rafiq_plan'); if(t==='complete'||t==='essentials') return t; }catch(_){}   // testing only
    const s = state();
    return s.kind==='paid' ? s.plan : s.kind==='ended' ? null : 'complete';
  }
  const isComplete = () => tier()==='complete';
  const checksLeft = () => isComplete() ? Infinity : tier() ? Math.max(0, ESSENTIALS_CHECKS - read().n) : 0;

  /* Fetch this account's billing row (needs auth.js). Resolves to state(). */
  /* Local-first (#171): with a saved copy, resolve straight away and refresh behind it
     ('rafiq:plan' when it changes); without one, wait for the server. */
  let loading = null;
  const CHECKED = 'rafiq_billing_checked';   // the server has answered at least once on this device
  function load(){
    let known = !!row; try{ known = known || !!localStorage.getItem(CHECKED); }catch(_){}
    if(known) { fetchRow(); return Promise.resolve(state()); }
    return fetchRow();
  }
  function fetchRow(){
    if(loading) return loading;
    const before = JSON.stringify(row);
    loading = (async () => {
      if(typeof sb==='undefined' || !sb || typeof currentUserId!=='function') return state();
      const uid = await currentUserId(); if(!uid) return state();
      const { data, error } = await sb.from('billing').select('*').eq('user_id', uid).maybeSingle();
      if(!error){
        row = data || null;
        try{ row ? localStorage.setItem(CACHE, JSON.stringify(row)) : localStorage.removeItem(CACHE); localStorage.setItem(CHECKED, '1'); }catch(_){}
        if(JSON.stringify(row) !== before) try{ window.dispatchEvent(new Event('rafiq:plan')); }catch(_){}
      }
      return state();
    })().finally(() => { loading = null; });   // shares one request between callers, then fetches fresh next time
    return loading;
  }

  /* Server actions (supabase/functions): billing checkout/portal/cancel/resume, account delete. */
  async function call(fn, body){
    const { data } = await sb.auth.getSession();
    const token = data && data.session && data.session.access_token;
    if(!token) return { error:'signin' };
    try{
      const r = await fetch(`${SUPABASE_URL}/functions/v1/${fn}`, { method:'POST',
        headers:{ 'Content-Type':'application/json', Authorization:`Bearer ${token}`, apikey:SUPABASE_KEY },
        body: JSON.stringify(body) });
      return await r.json().catch(() => ({ error:'server' }));
    }catch(_){ return { error:'offline' }; }
  }

  /* Called by judge.js before each smart check. false = no check this time. */
  function useCheck(){
    if(isComplete()) return true;
    if(!tier()) return false;
    const r = read();
    if(r.n >= ESSENTIALS_CHECKS){ notice(); return false; }
    r.n++; try{ localStorage.setItem(KEY, JSON.stringify(r)); }catch(_){}
    return true;
  }

  /* Lesson and practice pages call this: once the free week is over without a
     plan, go to the plans page. Home, Progress, the word list and Settings don't. */
  function requirePlan(){
    if(BETA) return true;
    const go = () => { if(!tier()) location.replace('plans.html'); };
    go(); load().then(go); addEventListener('rafiq:plan', go);   // the saved plan first, the server's when it comes (#171)
    return !!tier();
  }

  let shown = false;
  function notice(){
    if(shown || typeof document==='undefined') return; shown = true;
    const d = document.createElement('div');
    d.setAttribute('role','status');
    d.style.cssText = 'position:fixed;left:12px;right:12px;bottom:calc(76px + env(safe-area-inset-bottom));z-index:300;'+
      'background:var(--card);border:1px solid var(--gold);border-radius:12px;padding:12px 14px;font-size:14px;'+
      'box-shadow:0 8px 24px -10px rgba(0,0,0,.35);max-width:520px;margin:0 auto';
    d.innerHTML = `You've used today's ${ESSENTIALS_CHECKS} smart checks, so answers are now matched word by word. `+
      `<a href="plans.html">Rafiq Complete</a> gives unlimited checking. <button type="button" style="float:right;border:0;background:none;font-size:16px;cursor:pointer" aria-label="Close">✕</button>`;
    d.querySelector('button').onclick = () => d.remove();
    document.body.appendChild(d);
  }
  const dateText = d => d ? d.toLocaleDateString('en-GB', { day:'numeric', month:'long', year: d.getFullYear()!==new Date().getFullYear() ? 'numeric' : undefined }) : '';
  window.RafiqPlan = { BETA, ESSENTIALS_CHECKS, PRICES, tier, isComplete, checksLeft, useCheck, requirePlan, state, load, call, dateText };
})();
