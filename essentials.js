/* essentials.js — Practise → Everyday essentials: numbers, days, months, colours
   and telling the time. Each set is a table to look things up in (tap any Arabic
   to hear it) and a short drill: hear it or see the English, pick the answer.
   Needs essentials-data.js (ESSENTIALS) and progress.js; uses audio.js (RQ) and
   sounds.js when present. Answers are kept as 'e:<set>:<n>' so the drill can
   start with what was missed; they aren't part of Home's review.
   Mounted by practise.html#essentials. */
(function(){
  const ROUND = 10;
  const esc = t => String(t).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const shuffle = a => { const b=a.slice(); for(let i=b.length-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); [b[i],b[j]]=[b[j],b[i]]; } return b; };
  const say = (t, el) => { if(window.RQ) RQ.speak(t, el); };
  const canHear = () => !!(window.RQ && RQ.available());
  const sound = ok => { if(window.RafiqSound) RafiqSound.answer(ok); };
  const id = (s, i) => 'e:' + s.id + ':' + i;
  const P = () => window.Progress;
  const got = (s, i) => { const r = P() && P().get(id(s, i)); return r ? r.box : 0; };   // 0 new, 1 missed last time, 2+ known
  const known = s => s.items.filter((_, i) => got(s, i) >= 2).length;

  const css = document.createElement('style');
  css.textContent = `
.es-back{display:inline-block;margin:0 0 12px;font-size:14px;color:var(--verdigris);text-decoration:none;cursor:pointer;background:none;border:0;padding:0;font-family:var(--la)}
.es-note{font-size:14.5px;line-height:1.6;color:var(--ink-soft);margin:0 0 14px}
.es-note .ar{font-family:var(--ar);font-size:17px;color:var(--ink)}
.es-table{display:grid;gap:6px;margin-bottom:16px}
.es-row{display:flex;align-items:center;gap:10px;background:var(--card);border:1px solid var(--rule);border-radius:10px;padding:4px 12px}
.es-num{font-family:var(--ut);font-size:13px;color:var(--ink-soft);min-width:40px}
.es-en{flex:1;font-size:15px;color:var(--ink)}
.es-ar{font-family:var(--ar);font-size:22px;line-height:1.8;direction:rtl;background:none;border:0;color:var(--ink);cursor:pointer;padding:0 4px;
  border-radius:6px;touch-action:manipulation;transition:transform var(--press,120ms) var(--ease-out,ease-out)}
.es-ar:active{transform:scale(.95)}
.es-ar.speaking{color:var(--verdigris)}
.es-forms{display:flex;align-items:center}
.es-sep{color:var(--ink-soft);margin:0 4px}
.es-row.known{border-color:color-mix(in srgb,var(--verdigris) 45%,var(--rule))}
.es-q{background:var(--card);border:1px solid var(--rule);border-radius:10px;padding:20px;text-align:center}
.es-top{display:flex;justify-content:space-between;font-family:var(--ut);font-size:11px;letter-spacing:.08em;color:var(--ink-soft);margin:0 0 10px}
.es-prompt{font-size:22px;font-weight:600;margin:6px 0 4px}
.es-prompt .dig{display:block;font-size:13px;font-weight:400;color:var(--ink-soft);margin-top:4px}
.es-listen{font-size:32px;width:72px;height:72px;border-radius:50%;border:1px solid var(--verdigris);background:var(--paper);cursor:pointer;touch-action:manipulation}
.es-how{font-size:13.5px;color:var(--ink-soft);margin:8px 0 0}
.es-opts{display:grid;gap:8px;margin-top:16px}
.es-opt{min-height:50px;border:1px solid var(--rule);border-radius:10px;background:var(--paper);font-size:16px;color:var(--ink);cursor:pointer;padding:6px 12px;touch-action:manipulation}
.es-opt.ar{font-family:var(--ar);font-size:22px;line-height:1.7}
.es-opt.right{background:var(--verdigris);border-color:var(--verdigris);color:#fff}
.es-opt.wrong{background:var(--rubric);border-color:var(--rubric);color:#fff}
.es-reveal{margin-top:12px;font-size:14px;color:var(--ink-soft);min-height:20px}
.es-reveal .ar{font-family:var(--ar);font-size:20px;color:var(--ink)}
.es-actions{display:flex;gap:8px;margin-top:14px}
.es-actions .btn{flex:1;min-height:44px}
.es-big{font-size:40px;font-weight:700;color:var(--verdigris);font-variant-numeric:tabular-nums}
.es-miss{text-align:left;margin-top:14px;padding-top:12px;border-top:1px solid var(--rule)}`;
  document.head.appendChild(css);

  function menu(el){
    el.innerHTML = `<div class="qgrid">` + ESSENTIALS.map(s => {
      const k = known(s);
      return `<a class="qcard" href="#essentials" data-set="${s.id}">
        <div class="qa">${s.icon} ${esc(s.ar)}</div><div class="qt">${esc(s.t)}</div>
        <div class="qd">${s.items.length} ${s.id==='time'?'phrases':'words'} · tap to hear</div>
        <div class="qm">${k ? `<b>${k}</b> of ${s.items.length} known` : 'Table and a short drill'}</div></a>`; }).join('') + `</div>`;
    el.querySelectorAll('[data-set]').forEach(a => a.addEventListener('click', e => {
      e.preventDefault(); table(el, ESSENTIALS.find(s => s.id === a.dataset.set)); }));
  }

  // the note's Arabic in the right font
  const noteHTML = t => esc(t).replace(/([؀-ۿ][؀-ۿ\sً-ْٰ]*[؀-ۿً-ْ])/g, '<span class="ar">$1</span>');

  function table(el, s){
    const numbers = s.id === 'numbers' || s.id === 'ordinals', pair = s.id === 'colours';
    el.innerHTML = `<button class="es-back" type="button">‹ All essentials</button>
      <h2 style="margin:0 0 6px">${s.icon} ${esc(s.t)} <span style="font-family:var(--ar);font-weight:400;color:var(--ink-soft)">${esc(s.ar)}</span></h2>
      <p class="es-note">${noteHTML(s.note)}</p>
      <div class="es-table">${s.items.map((it, i) => `<div class="es-row${got(s,i)>=2?' known':''}">
        ${numbers ? `<span class="es-num">${esc(it[2])}</span>` : ''}
        <span class="es-en">${esc(it[1])}</span>
        <span class="es-forms" dir="rtl"><button class="es-ar" type="button" data-t="${esc(it[0])}">${esc(it[0])}</button>${pair ? `<span class="es-sep" aria-hidden="true">·</span><button class="es-ar" type="button" data-t="${esc(it[2])}" aria-label="feminine: ${esc(it[2])}">${esc(it[2])}</button>` : ''}</span>
      </div>`).join('')}</div>
      <div class="es-actions"><button class="btn" type="button" data-act="drill">Practise these</button></div>`;
    el.querySelector('.es-back').onclick = () => { menu(el); scrollTo(0, 0); };
    el.querySelectorAll('.es-ar').forEach(b => b.onclick = () => say(b.dataset.t, b));
    el.querySelector('[data-act="drill"]').onclick = () => drill(el, s);
    scrollTo(0, 0);
  }

  /* Ten questions: what was missed last time first, then what's new, then the rest.
     Each is either "hear it, pick the meaning" or "see the meaning, pick the Arabic". */
  function drill(el, s){
    const idx = s.items.map((_, i) => i);
    const order = shuffle(idx.filter(i => got(s,i) === 1)).concat(shuffle(idx.filter(i => got(s,i) === 0)), shuffle(idx.filter(i => got(s,i) >= 2)));
    const qs = order.slice(0, Math.min(ROUND, idx.length));
    const missed = []; let k = 0, score = 0, turn = Math.random() < .5 ? 0 : 1;
    const ask = () => {
      if(k >= qs.length) return end();
      const i = qs[k], it = s.items[i], hear = (turn++ % 2 === 0) && canHear();
      const others = shuffle(idx.filter(j => j !== i)).slice(0, 3);
      const opts = shuffle([i].concat(others));
      const digit = (s.id === 'numbers' || s.id === 'ordinals') ? `<span class="dig">${esc(it[2])}</span>` : '';
      el.innerHTML = `<button class="es-back" type="button">‹ ${esc(s.t)}</button>
        <div class="es-top"><span>${esc(s.t)} · ${k+1} of ${qs.length}</span><span>Score <b>${score}</b></span></div>
        <div class="es-q">${hear
          ? `<button class="es-listen" type="button" aria-label="Play again">🔊</button><p class="es-how">What does it mean?</p>`
          : `<div class="es-prompt">${esc(it[1])}${digit}</div><p class="es-how">Pick the Arabic</p>`}
          <div class="es-opts">${opts.map(j => `<button class="es-opt${hear?'':' ar'}" type="button" data-j="${j}">${esc(hear ? s.items[j][1] : s.items[j][0])}</button>`).join('')}</div>
          <div class="es-reveal" aria-live="polite"></div></div>
        <div class="es-actions"><button class="btn" type="button" data-act="next" disabled>Next</button></div>`;
      el.querySelector('.es-back').onclick = () => table(el, s);
      const next = el.querySelector('[data-act="next"]');
      if(hear){ const b = el.querySelector('.es-listen'); b.onclick = () => say(it[0], b); say(it[0], b); }
      let done = false;
      el.querySelectorAll('.es-opt').forEach(b => b.onclick = () => {
        if(done) return; done = true;
        const ok = +b.dataset.j === i;
        b.classList.add(ok ? 'right' : 'wrong');
        if(!ok) el.querySelector(`.es-opt[data-j="${i}"]`).classList.add('right');
        sound(ok); if(P()) P().grade(id(s, i), ok ? 'good' : 'again');
        if(ok) score++; else missed.push(it);
        const r = el.querySelector('.es-reveal');
        r.innerHTML = `<span class="ar">${esc(it[0])}</span> · ${esc(it[1])}`;
        next.disabled = false; next.textContent = k + 1 >= qs.length ? 'See results' : 'Next'; next.focus();
        // a right answer moves on by itself once the word's been said (see autoNext in learn.html)
        if(ok){
          let gone = false;
          const go = () => { if(gone || !next.isConnected) return;
            if(document.querySelector('.rp-sheet') || document.hidden) return setTimeout(go, 700);
            gone = true; next.click(); };
          if(!hear && window.RQ) RQ.speak(it[0], null, () => setTimeout(go, 500)); else setTimeout(go, 900);
          setTimeout(go, 6000);
        } else if(!hear) say(it[0], null);
      });
      next.onclick = () => { k++; ask(); };
    };
    const end = () => {
      el.innerHTML = `<div class="es-q"><div class="es-big">${score} / ${qs.length}</div>
        <p class="es-how">${score === qs.length ? 'All right first time.' : 'The ones you missed come first next time.'}</p>
        ${missed.length ? `<div class="es-miss">${missed.map(it => `<div class="es-row"><span class="es-en">${esc(it[1])}</span><button class="es-ar" type="button" data-t="${esc(it[0])}">${esc(it[0])}</button></div>`).join('')}</div>` : ''}</div>
        <div class="es-actions"><button class="btn" type="button" data-act="again">Another round</button>
          <button class="btn ghost" type="button" data-act="table">Back to the table</button></div>`;
      el.querySelectorAll('.es-ar').forEach(b => b.onclick = () => say(b.dataset.t, b));
      el.querySelector('[data-act="again"]').onclick = () => drill(el, s);
      el.querySelector('[data-act="table"]').onclick = () => table(el, s);
      scrollTo(0, 0);
    };
    ask();
  }

  window.RafiqEssentials = { mount: menu, known };
})();
