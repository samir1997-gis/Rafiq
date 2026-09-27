/* report.js — "Report a problem" and contacting support.

   RafiqReport.open({kind, context})   a sheet over the current page (a lesson
                                       isn't lost), e.g. from the ⚑ button
   RafiqReport.mount(el, {kind})       the same form inside a page (help.html)

   On lesson pages (.lhead in learn.html, .sess-head in session.html) a ⚑ button
   is added; it attaches what's on screen (the question and what was typed) so
   we can see exactly what went wrong. Messages go to the `support` Edge
   Function: saved in Supabase and emailed to support@rafiq-arabic.com, with
   Reply going to the learner. Needs auth.js (SUPABASE_URL, SUPABASE_KEY, sb). */
(function(){
  const KINDS = [
    ['answer','A question or answer is wrong'], ['bug','Something isn’t working'], ['billing','My plan or a payment'],
    ['account','My account'], ['idea','An idea'], ['other','Something else'],
  ];
  const esc = t => String(t).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

  const css = document.createElement('style');
  css.textContent = `
.rp-flag{flex:0 0 auto;width:40px;height:40px;border-radius:50%;border:1px solid var(--rule);background:var(--card);color:var(--ink-soft);
  font-size:16px;display:flex;align-items:center;justify-content:center;cursor:pointer;touch-action:manipulation;transition:transform var(--press,.12s) var(--ease-out,ease-out)}
.rp-flag:active{transform:scale(.92)}
.rp-scrim{position:fixed;inset:0;z-index:400;background:rgba(0,0,0,.38);opacity:0;transition:opacity .22s ease}
.rp-scrim.on{opacity:1}
.rp-sheet{position:fixed;left:0;right:0;bottom:0;z-index:401;max-width:560px;margin:0 auto;max-height:92vh;overflow:auto;
  background:var(--paper);border-radius:16px 16px 0 0;box-shadow:0 -10px 40px -12px rgba(0,0,0,.4);
  padding:10px 20px calc(20px + env(safe-area-inset-bottom));transform:translateY(100%);transition:transform .34s var(--ease-out,cubic-bezier(.16,1,.3,1))}
.rp-sheet.on{transform:none}
.rp-grab{width:40px;height:5px;border-radius:3px;background:var(--rule);margin:0 auto 12px}
.rp-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:4px}
.rp-head h2{font-size:20px;font-weight:700;letter-spacing:-.01em;margin:0}
.rp-x{border:0;background:none;font-size:15px;color:var(--verdigris);cursor:pointer;padding:10px 0 10px 12px;font-family:var(--la)}
.rp-sub{font-size:14px;color:var(--ink-soft);margin:0 0 14px;line-height:1.5}
.rp-kinds{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:14px}
.rp-kinds button{border:1px solid var(--rule);background:var(--card);color:var(--ink);border-radius:999px;padding:8px 13px;min-height:38px;
  font-family:var(--la);font-size:13.5px;cursor:pointer;touch-action:manipulation;transition:transform var(--press,.12s) var(--ease-out,ease-out),background .15s}
.rp-kinds button:active{transform:scale(.95)}
.rp-kinds button.on{background:var(--verdigris);border-color:var(--verdigris);color:var(--paper);font-weight:700}
.rp-f label{display:block;font-size:12px;color:var(--ink-soft);margin:0 0 5px}
.rp-f textarea,.rp-f input[type=email]{width:100%;border:1px solid var(--rule);border-radius:8px;background:var(--card);color:var(--ink);
  font-family:var(--la);font-size:16px;padding:10px 12px;margin-bottom:12px}
.rp-f textarea{min-height:110px;resize:vertical;line-height:1.45}
.rp-f textarea:focus,.rp-f input:focus{outline:none;border-color:var(--verdigris)}
.rp-f .rp-ctx{display:flex;gap:10px;align-items:flex-start;font-size:13px;color:var(--ink-soft);margin:0 0 14px;line-height:1.45}
.rp-ctx input{margin-top:3px;accent-color:var(--verdigris);width:18px;height:18px;flex:0 0 auto}
.rp-ctx q{display:block;color:var(--ink);font-style:normal;quotes:none;margin-top:2px;max-height:3.2em;overflow:hidden}
.rp-f .btn{width:100%;min-height:48px}
.rp-msg{font-size:14px;margin-top:10px;min-height:20px;text-align:center;color:var(--rubric)}
.rp-hp{position:absolute;left:-9999px;width:1px;height:1px;opacity:0}
.rp-done{text-align:center;padding:18px 0 8px}
.rp-done .ic{width:56px;height:56px;border-radius:50%;margin:0 auto 12px;display:grid;place-items:center;font-size:26px;
  background:color-mix(in srgb,var(--verdigris) 15%,var(--card));color:var(--verdigris)}
.rp-done h3{font-size:19px;margin:0 0 6px}
.rp-done p{font-size:14.5px;color:var(--ink-soft);margin:0 0 16px;line-height:1.5}
@media (prefers-reduced-motion:reduce){.rp-sheet{transition:opacity .2s ease;transform:none;opacity:0}.rp-sheet.on{opacity:1}}`;
  document.head.appendChild(css);

  async function token(){
    try{ const { data } = await sb.auth.getSession(); return data && data.session ? data.session : null; }catch(_){ return null; }
  }
  async function send(payload){
    const s = await token();
    try{
      const r = await fetch(`${SUPABASE_URL}/functions/v1/support`, { method:'POST',
        headers: Object.assign({ 'Content-Type':'application/json', apikey:SUPABASE_KEY }, s ? { Authorization:`Bearer ${s.access_token}` } : {}),
        body: JSON.stringify(payload) });
      return await r.json().catch(() => ({ error:'server' }));
    }catch(_){ return { error:'offline' }; }
  }

  // what's on screen in a lesson: the card's text plus anything typed
  function snapshot(){
    const root = document.querySelector('#stage, #panel, main');
    if(!root) return '';
    const typed = [...root.querySelectorAll('input:not([type=checkbox]):not([type=radio]), textarea')].map(i => i.value.trim()).filter(Boolean);
    const text = (root.innerText || '').replace(/[ \t]+/g,' ').replace(/\n{2,}/g,'\n').trim();
    return (text + (typed.length ? '\n\nTyped: ' + typed.join(' | ') : '')).slice(0, 2500);
  }

  /* The form. opts: kind, context, onDone(), inSheet */
  async function mount(el, opts = {}){
    const s = await token();
    let kind = opts.kind || 'bug';
    const ctx = opts.context || '';
    el.innerHTML = `<div class="rp-f">
      <div class="rp-kinds" role="group" aria-label="What is it about?">${KINDS.map(([k, t]) => `<button type="button" data-k="${k}">${t}</button>`).join('')}</div>
      <label for="rpMsg">What happened?</label>
      <textarea id="rpMsg" placeholder="${kind==='answer' ? 'e.g. I wrote the right answer but it was marked wrong' : 'Tell us in your own words'}"></textarea>
      ${s ? '' : `<label for="rpEmail">Your email, so we can reply</label><input id="rpEmail" type="email" autocomplete="email" placeholder="you@example.com">`}
      <input class="rp-hp" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
      ${ctx ? `<label class="rp-ctx"><input type="checkbox" id="rpCtx" checked><span>Include what’s on my screen<q>${esc(ctx.slice(0, 160))}</q></span></label>` : ''}
      <button class="btn" type="button" id="rpSend">Send</button>
      <div class="rp-msg" id="rpErr" role="alert"></div></div>`;
    const paint = () => el.querySelectorAll('[data-k]').forEach(b => b.classList.toggle('on', b.dataset.k === kind));
    el.querySelectorAll('[data-k]').forEach(b => b.onclick = () => { kind = b.dataset.k; paint(); });
    paint();
    const go = el.querySelector('#rpSend'), err = el.querySelector('#rpErr');
    go.onclick = async () => {
      const message = el.querySelector('#rpMsg').value.trim();
      const email = s ? '' : (el.querySelector('#rpEmail').value || '').trim();
      if(message.length < 3){ err.textContent = 'Please tell us a little about it.'; el.querySelector('#rpMsg').focus(); return; }
      if(!s && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)){ err.textContent = 'Please add your email so we can reply.'; return; }
      go.disabled = true; go.textContent = 'Sending…'; err.textContent = '';
      const r = await send({ kind, message, email, website: el.querySelector('.rp-hp').value,
        page: location.pathname.split('/').pop() + location.search, context: ctx && el.querySelector('#rpCtx') && el.querySelector('#rpCtx').checked ? ctx : '' });
      if(r && r.ok){
        el.innerHTML = `<div class="rp-done" role="status"><div class="ic" aria-hidden="true">✓</div><h3>Thank you</h3>
          <p>We’ve got it${r.id ? ` (#${r.id})` : ''}. A real person reads every message, and if you asked something we’ll reply by email${s && s.user && s.user.email ? ` to ${esc(s.user.email)}` : ''}.</p>
          ${opts.inSheet ? '<button class="btn" type="button" id="rpBack">Back to the lesson</button>' : ''}</div>`;
        const back = el.querySelector('#rpBack'); if(back) back.onclick = () => opts.onDone && opts.onDone();
        return;
      }
      go.disabled = false; go.textContent = 'Send';
      err.textContent = r && r.error === 'too_many' ? 'You’ve sent a lot just now. Please try again in an hour, or email support@rafiq-arabic.com.'
        : r && r.error === 'offline' ? 'You seem to be offline. Check your connection and try again.'
        : 'That didn’t send. Please try again, or email support@rafiq-arabic.com.';
    };
  }

  let open_ = null;
  function open(opts = {}){
    if(open_) return;
    const scrim = document.createElement('div'); scrim.className = 'rp-scrim';
    const sheet = document.createElement('div'); sheet.className = 'rp-sheet';
    sheet.setAttribute('role','dialog'); sheet.setAttribute('aria-modal','true'); sheet.setAttribute('aria-labelledby','rpTitle');
    sheet.innerHTML = `<div class="rp-grab" aria-hidden="true"></div><div class="rp-head"><h2 id="rpTitle">Report a problem</h2>
      <button class="rp-x" type="button">Close</button></div>
      <p class="rp-sub">Thanks for helping make Rafiq better. Tell us what went wrong and we’ll look into it.</p><div class="rp-body"></div>`;
    document.body.append(scrim, sheet);
    const last = document.activeElement;
    const close = () => {
      scrim.classList.remove('on'); sheet.classList.remove('on');
      setTimeout(() => { scrim.remove(); sheet.remove(); open_ = null; if(last && last.focus) last.focus(); }, 300);
      document.removeEventListener('keydown', key);
    };
    const key = e => { if(e.key === 'Escape') close(); };
    document.addEventListener('keydown', key);
    scrim.onclick = close; sheet.querySelector('.rp-x').onclick = close;
    mount(sheet.querySelector('.rp-body'), Object.assign({}, opts, { inSheet:true, onDone:close }));
    requestAnimationFrame(() => { scrim.classList.add('on'); sheet.classList.add('on'); });
    setTimeout(() => { const t = sheet.querySelector('textarea'); if(t) t.focus({ preventScroll:true }); }, 360);
    open_ = { close };
  }

  // the ⚑ button on lesson pages
  function addFlag(){
    const head = document.querySelector('.lhead, .sess-head');
    if(!head || head.querySelector('.rp-flag')) return;
    const b = document.createElement('button');
    b.type = 'button'; b.className = 'rp-flag'; b.textContent = '⚑';
    b.title = 'Report a problem'; b.setAttribute('aria-label', 'Report a problem with this question');
    b.onclick = () => open({ kind:'answer', context: snapshot() });
    head.appendChild(b);
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', addFlag); else addFlag();

  window.RafiqReport = { open, mount, snapshot };
})();
