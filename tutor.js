/* tutor.js — the AI tutor (#127), Rafiq Complete.

   RafiqTutor.ask(mode, messages, context, onText)
       asks the `tutor` Edge Function; onText(sofar) is called as the answer
       streams in; the first time on a device it asks permission to send to Anthropic. Resolves to {text} or {error: 'consent'|'signin'|'plan'|'limit'|
       'not_configured'|'offline'|'server'}.
   RafiqTutor.learner(question)
       what the tutor should know for the Tutor tab: the learner's unit, its
       words and grammar notes, recurring mistakes, and the salah lines (with
       the official Quran translation) when the question is about the prayer.
   RafiqTutor.html(text)   the answer as safe HTML (**bold**, *italic*, "- " lists, Arabic runs)

   On lesson pages (.lhead in learn.html, .sess-head in session.html) a "Why?"
   button appears beside ⚑ after a wrong answer, never while a question is
   open, and explains the mistake from what's on screen. Needs auth.js, plan.js
   and report.js (the sheet's look, the screen snapshot, reporting an answer). */
(function(){
  const esc = t => String(t).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const AR = /[؀-ۿݐ-ݿﭐ-﷿ﹰ-﻿]+(?:[\s،؛؟.!]*[؀-ۿݐ-ݿﭐ-﷿ﹰ-﻿]+)*/g;

  const css = document.createElement('style');
  css.textContent = `
.tu-ans{line-height:1.6;font-size:16px}
.tu-ans p{margin:0 0 .7em;unicode-bidi:plaintext}
.tu-ans p:last-child{margin-bottom:0}
.tu-ans ul{margin:0 0 .7em;padding-left:1.2em}
.tu-ans bdi{font-family:var(--ar);font-size:1.18em;line-height:1.5}
.tu-why{flex:0 0 auto;height:40px;border-radius:999px;border:0;background:var(--gold);color:var(--ink);padding:0 14px;
  font-family:var(--la);font-size:15px;font-weight:700;cursor:pointer;touch-action:manipulation;animation:tu-in .35s var(--ease-out,ease-out)}
.tu-why:active{transform:scale(.94)}
@keyframes tu-in{from{opacity:0;transform:scale(.7)}to{opacity:1;transform:none}}
.tu-foot{display:flex;gap:10px;align-items:center;justify-content:space-between;margin-top:16px;flex-wrap:wrap}
.tu-foot .rp-x{padding:10px 0}
.tu-dots::after{content:'…';animation:tu-blink 1s steps(2) infinite}
@keyframes tu-blink{50%{opacity:.2}}
@media (prefers-reduced-motion:reduce){.tu-why{animation:none}}`;
  document.head.appendChild(css);

  /* The answer as HTML: paragraphs, "- " lists, **bold**, and Arabic in its own font and direction. */
  function html(text){
    const inline = s => esc(s).replace(/\*\*(.+?)\*\*/g, '<b>$1</b>').replace(/\*([^*\s][^*]*?)\*/g, '<i>$1</i>').replace(AR, m => `<bdi lang="ar" dir="rtl">${m}</bdi>`);
    return String(text).trim().split(/\n{2,}/).map(block => {
      const lines = block.split('\n');
      if(lines.every(l => /^\s*[-•]\s/.test(l))) return '<ul>' + lines.map(l => `<li>${inline(l.replace(/^\s*[-•]\s/, ''))}</li>`).join('') + '</ul>';
      return '<p>' + lines.map(inline).join('<br>') + '</p>';
    }).join('');
  }

  /* Permission before anything goes to Anthropic (Apple 5.1.2(i), #351): asked once on this device, before the first
     question from the chat, Home's card or Why?. Resolves true once allowed. */
  const OK_KEY = 'rafiq_ai_ok';
  function allowed(){
    try{ if(localStorage.getItem(OK_KEY) === '1') return Promise.resolve(true); }catch(_){}
    return new Promise(done => {
      if(!document.getElementById('aiok-css')){ const st = document.createElement('style'); st.id = 'aiok-css'; st.textContent = `
#aiok{position:fixed;inset:0;z-index:2000;display:flex;align-items:center;justify-content:center;padding:16px;background:rgba(10,16,18,.55);
  animation:aiok-fade .25s ease-out both}
#aiok .box{width:min(420px,100%);background:var(--card);color:var(--ink);border:1px solid var(--rule);border-radius:18px;padding:20px 20px 16px;
  box-shadow:0 24px 50px -16px rgba(0,0,0,.5);font-family:var(--la);animation:aiok-in .38s cubic-bezier(.34,1.3,.64,1) both}
#aiok h2{font-size:19px;font-weight:800;margin:0 0 8px}#aiok p{font-size:14.5px;line-height:1.55;color:var(--ink-soft);margin:0 0 10px}#aiok b{color:var(--ink)}
#aiok a{color:var(--verdigris)}#aiok .row{display:flex;justify-content:flex-end;gap:10px;margin-top:14px}
#aiok button{border-radius:999px;font:800 14px var(--la);padding:10px 18px;cursor:pointer;border:1px solid var(--rule);background:var(--paper);color:var(--ink)}
#aiok button.yes{background:var(--verdigris);border-color:var(--verdigris);color:#fff}
@keyframes aiok-fade{from{opacity:0}}@keyframes aiok-in{from{opacity:0;transform:translateY(10px) scale(.97)}}
@media (prefers-reduced-motion:reduce){#aiok,#aiok .box{animation:none}}`; document.head.appendChild(st); }
      const m = document.createElement('div'); m.id = 'aiok'; m.setAttribute('role', 'dialog'); m.setAttribute('aria-modal', 'true'); m.setAttribute('aria-labelledby', 'aiokT');
      m.innerHTML = `<div class="box"><h2 id="aiokT">Before you ask</h2>
        <p>Ask Rafiq’s answers are written by <b>Claude, an AI made by Anthropic</b>. To answer, your question is sent to Anthropic,
          with what Rafiq needs to fit the answer to you: your current unit’s words, the kinds of mistakes you often make and,
          for <b>Why?</b>, what’s on your screen.</p>
        <p><b>Your name and email are never sent</b>, and Anthropic doesn’t use any of it to train its AI.
          More in our <a href="privacy.html#tutor" target="_blank" rel="noopener">Privacy policy</a>.</p>
        <div class="row"><button type="button" class="no">Not now</button><button type="button" class="yes">OK, ask Rafiq</button></div></div>`;
      document.body.appendChild(m);
      const end = ok => { if(ok) try{ localStorage.setItem(OK_KEY, '1'); }catch(_){} m.remove(); done(ok); };
      m.querySelector('.yes').onclick = () => end(true); m.querySelector('.no').onclick = () => end(false);
      m.querySelector('.yes').focus();
    });
  }

  async function ask(mode, messages, context, onText){
    if(!(await allowed())) return { error:'consent' };
    let token = null;
    try{ const { data } = await sb.auth.getSession(); token = data && data.session && data.session.access_token; }catch(_){}
    if(!token) return { error:'signin' };
    let r;
    try{
      r = await fetch(`${SUPABASE_URL}/functions/v1/tutor`, { method:'POST',
        headers:{ 'Content-Type':'application/json', Authorization:`Bearer ${token}`, apikey:SUPABASE_KEY },
        body: JSON.stringify({ mode, messages, context }) });
    }catch(_){ return { error:'offline' }; }
    if(!r.ok || !r.body){
      const j = await r.json().catch(() => ({}));
      return { error: j.error || 'server' };
    }
    const reader = r.body.getReader(), dec = new TextDecoder();
    let text = '';
    try{
      for(;;){
        const { value, done } = await reader.read();
        if(done) break;
        text += dec.decode(value, { stream:true });
        if(onText) onText(text);
      }
    }catch(_){ if(!text) return { error:'offline' }; }
    return text.trim() ? { text } : { error:'server' };
  }

  const WHY_NOT = {
    consent:'Ask Rafiq needs your OK before it sends a question. Ask again whenever you’re ready.',
    signin:'Please sign in again to ask Rafiq.',
    plan:'Ask Rafiq is part of Rafiq Complete.',
    limit:'You’ve asked Rafiq 20 questions today, the most for one day. It’ll be back tomorrow.',
    not_configured:'Ask Rafiq isn’t switched on yet. Please try again soon.',
    offline:'You seem to be offline. Check your connection and try again.',
    server:'Rafiq couldn’t answer just now. Please try again in a moment.',
  };
  const problem = e => WHY_NOT[e] || WHY_NOT.server;

  /* ---- what the tutor knows about the learner (Tutor tab) ---- */
  const bare = s => String(s).replace(/[ً-ٰٟۖ-ۭـ]/g, '').replace(/[أإآٱ]/g, 'ا');
  const SALAH_Q = /\b(salah|salat|prayer|pray|praying|surah?|fatiha|ikhlas|quran|qur'?an|verse|ayah?|takbir|ruku|sujud|tashahhud|tahiyyat|du'?a|allahu|subhan|ameen|amin|wudu)\b/i;
  function aboutSalah(q){
    if(!window.RafiqSalah || !RafiqSalah.enabled() || !RafiqSalah.parts) return false;
    if(SALAH_Q.test(q)) return true;
    // or two or more Arabic words in a row from the prayer (one word alone, like هَذا, is too common)
    const runs = bare(q).match(/[ء-ي]+(?:\s+[ء-ي]+)+/g) || [];
    if(!runs.length) return false;
    const all = bare(lines().map(l => l.ar).join(' '));
    return runs.some(r => all.includes(r));
  }
  const lines = () => RafiqSalah.parts().flatMap(p => p.lines).filter(l => l.ar);
  async function salahLines(){
    // the official Quran translation replaces our drafts once loaded (salah.js); a few seconds at most
    try{ await Promise.race([RafiqSalah.ready(), new Promise(r => setTimeout(r, 4000))]); }catch(_){}
    const official = RafiqSalah.officialMeanings && RafiqSalah.officialMeanings();
    return `The words of the prayer as taught in Your salah. Lines with a verse reference are Quran${official ? ', with the official Saheeh International translation' : ''}:\n` +
      RafiqSalah.parts().filter(p => p.lines.some(l => l.ar)).map(p => `${p.title}:\n` +
        p.lines.filter(l => l.ar).map(l => `${l.ar} = ${l.en}${l.ref ? ` (${l.ref})` : ''}`).join('\n')).join('\n');
  }
  async function learner(question){
    const out = [];
    if(window.RafiqPath){
      const { unit } = RafiqPath.next(), units = RafiqPath.units();
      const done = units.filter(u => u !== unit && RafiqPath.unitDone(u)).map(u => `${u.n} ${u.en}`);
      out.push(`Current unit: ${unit.n} ${unit.en} (${unit.ar}).` + (done.length ? ` Units finished: ${done.join(', ')}.` : ' No units finished yet.'));
      const words = unit.alpha ? [] : RafiqPath.wordsOf(unit);
      if(words.length) out.push('Words in this unit:\n' + words.map(w => `${w.ar} = ${w.en}`).join('\n'));
      // the notes are in drills-data.js's EXTRA (lesson pages copy them onto the unit)
      // the basics (#165): its lessons' teaching screens are the notes
      const notes = unit.alpha ? [] : unit.basics ? BASICS.flatMap(l => l.teach.map(t => ({h:t.h, ar:t.pairs.map(p => p[0]).join(' · '), tr:t.pairs.map(p => p[1]).join(' · '), en:t.en})))
        : ((RafiqPath.unitData(unit.n) || {}).grammar || (typeof EXTRA !== 'undefined' && EXTRA[unit.n] && EXTRA[unit.n].grammar) || []);
      if(notes.length) out.push('How it works (grammar notes) in this unit:\n' +
        notes.map(g => `- ${g.h || g.t}: ${(g.ar || '').replace(/=/g, ' ')}${g.tr ? ` (${g.tr})` : ''}. ${g.en}`).join('\n'));
    }
    if(window.RafiqMistakes){
      const c = RafiqMistakes.counts(), top = Object.entries(c).filter(([, n]) => n > 0).sort((a, b) => b[1] - a[1]);
      if(top.length) out.push('Mistakes they made this week: ' + top.map(([k, n]) => `${RafiqMistakes.HELP[k].title} (${n})`).join('; ') + '.');
    }
    if(aboutSalah(question)) out.push(await salahLines());
    return out.join('\n\n');
  }

  /* ---- "Why?" after a wrong answer, on lesson pages ---- */
  const screen = () => window.RafiqReport ? RafiqReport.snapshot() : '';
  const firstLine = () => screen().split('\n').find(l => l.trim().length > 2) || '';
  let why = null, watch = null;
  function hideWhy(){ if(why){ why.remove(); why = null; } if(watch){ watch.disconnect(); watch = null; } }
  function showWhy(){
    hideWhy();
    if(typeof TUTOR_ON === 'undefined' || !TUTOR_ON) return;   // auth.js
    const head = document.querySelector('.lhead, .sess-head');
    if(!head || !window.RafiqPlan || !RafiqPlan.isComplete()) return;
    why = document.createElement('button');
    why.type = 'button'; why.className = 'tu-why'; why.textContent = 'Why?';
    why.setAttribute('aria-label', 'Why was that wrong? Ask Rafiq');
    why.onclick = openWhy;
    const flag = head.querySelector('.rp-flag');
    flag ? head.insertBefore(why, flag) : head.appendChild(why);
    // gone once the next question is on screen
    const q = firstLine(), root = document.querySelector('#stage, #panel, main');
    if(root && q){ watch = new MutationObserver(() => { if(!screen().includes(q)) hideWhy(); }); watch.observe(root, { childList:true, subtree:true, characterData:true }); }
  }
  function openWhy(){
    const shot = screen();
    const scrim = document.createElement('div'); scrim.className = 'rp-scrim';
    const sheet = document.createElement('div'); sheet.className = 'rp-sheet';
    sheet.setAttribute('role','dialog'); sheet.setAttribute('aria-modal','true'); sheet.setAttribute('aria-labelledby','tuTitle');
    sheet.innerHTML = `<div class="rp-grab" aria-hidden="true"></div><div class="rp-head"><h2 id="tuTitle">Why?</h2>
      <button class="rp-x" type="button">Close</button></div>
      <div class="tu-ans" aria-live="polite"><p class="rp-sub tu-dots">Your tutor is looking at the question</p></div>
      <div class="tu-foot" hidden><button class="btn" type="button" id="tuOk">Got it</button>
        <button class="rp-x" type="button" id="tuReport">Report this answer</button></div>`;
    document.body.append(scrim, sheet);
    const close = () => {
      scrim.classList.remove('on'); sheet.classList.remove('on');
      setTimeout(() => { scrim.remove(); sheet.remove(); }, 300);
      document.removeEventListener('keydown', key);
    };
    const key = e => { if(e.key === 'Escape') close(); };
    document.addEventListener('keydown', key);
    scrim.onclick = close; sheet.querySelector('.rp-x').onclick = close; sheet.querySelector('#tuOk').onclick = close;
    requestAnimationFrame(() => { scrim.classList.add('on'); sheet.classList.add('on'); });
    const box = sheet.querySelector('.tu-ans'), foot = sheet.querySelector('.tu-foot');
    const page = (document.title || '').replace(/\s*—\s*Rafiq$/, '');
    ask('why', [{ role:'user', content:'Why was my answer wrong?' }], `${page}\n\n${shot}`, t => { box.innerHTML = html(t); }).then(r => {
      if(r.error){ box.innerHTML = `<p>${esc(problem(r.error))}</p>`; foot.hidden = false; sheet.querySelector('#tuReport').hidden = true; return; }
      box.innerHTML = html(r.text); foot.hidden = false;
      sheet.querySelector('#tuReport').onclick = () => { close(); setTimeout(() =>
        RafiqReport.open({ kind:'answer', context:`Tutor's "Why?" answer:\n${r.text}\n\nOn screen:\n${shot}`.slice(0, 2900) }), 320); };
    });
  }
  // every checked answer goes through RafiqSound.answer (sounds.js); a wrong one brings up "Why?"
  function hook(){
    if(!window.RafiqSound || RafiqSound._tutor) return;
    const answer = RafiqSound.answer;
    RafiqSound.answer = ok => { hideWhy(); if(!ok) setTimeout(showWhy, 350); return answer(ok); };
    RafiqSound._tutor = true;
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', hook); else hook();

  window.RafiqTutor = { ask, learner, html, problem };
})();
