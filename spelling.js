/* spelling.js — Spelling bee: type a word you've met, in Arabic, from its sound
   or its meaning. Mounted by practise.html#spelling.
   Needs vocab-data.js (VOCAB), path-data.js (PIC), path.js (RafiqPath),
   progress.js (Progress); uses audio.js (RQ), sounds.js and arkb.js when present.

   Letters must be right to pass; matching vowel marks earn a bonus. Alef forms
   and a final ة/ه or ى/ي get one hint and another try instead of a wrong. */
(function(){
  const ROUND = 10, MIN_WORDS = 4, BEST_KEY = 'rafiq_spelling_best';
  const MARK = /[ً-ْٰ]/, LETTER = /[ء-ي]/;

  const esc = t => String(t).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const letters = s => (s||'').replace(/ٱ/g,'ا').split('').filter(c => LETTER.test(c) && c !== 'ـ').join('');
  const unifyAlef = s => s.replace(/[أإآ]/g,'ا');
  const unifyEnd  = s => s.replace(/ة$/,'ه').replace(/ى$/,'ي');

  // letters with their marks, marks sorted so shadda+fatha and fatha+shadda compare equal
  function vowelled(s){
    const out = []; let cur = null;
    for(const c of (s||'').replace(/ٱ/g,'ا')){
      if(MARK.test(c)){ if(cur) cur.m.push(c); }
      else if(LETTER.test(c) && c !== 'ـ'){ cur = {b:c, m:[]}; out.push(cur); }
    }
    return out.map(x => x.b + x.m.sort().join('')).join('');
  }
  const hasMarks = s => [...(s||'')].some(c => MARK.test(c));

  function lcsMask(a, b){
    const n=a.length, m=b.length, dp=Array.from({length:n+1},()=>new Array(m+1).fill(0));
    for(let i=1;i<=n;i++) for(let j=1;j<=m;j++) dp[i][j] = a[i-1]===b[j-1] ? dp[i-1][j-1]+1 : Math.max(dp[i-1][j],dp[i][j-1]);
    const ma=new Array(n).fill(false), mb=new Array(m).fill(false); let i=n, j=m;
    while(i>0 && j>0){ if(a[i-1]===b[j-1]){ ma[i-1]=mb[j-1]=true; i--; j--; } else if(dp[i-1][j]>=dp[i][j-1]) i--; else j--; }
    return [ma, mb];
  }
  // wrap each letter (with the marks that follow it) in ok/no by its position in the mask
  function paint(s, mask){
    let k = -1, html = '', open = false;
    for(const c of s.replace(/ٱ/g,'ا')){
      if(LETTER.test(c) && c !== 'ـ'){
        if(open) html += '</span>';
        k++; html += `<span class="${mask[k]?'ok':'no'}">${esc(c)}`; open = true;
      } else html += esc(c);
    }
    return html + (open ? '</span>' : '');
  }

  // single words only: a phrase isn't a spelling test
  function pool(){
    const met = window.RafiqPath ? RafiqPath.metWords() : new Set();
    return VOCAB.filter(w => met.has(w.id) && w.ar.replace(/[؟?!.,،]/g,'').trim().split(/\s+/).length === 1);
  }
  function best(){ try{ return JSON.parse(localStorage.getItem(BEST_KEY)) || null; }catch(_){ return null; } }
  function saveBest(score, total){ try{ localStorage.setItem(BEST_KEY, JSON.stringify({score, total})); }catch(_){} }
  const shuffle = a => { for(let i=a.length-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); [a[i],a[j]]=[a[j],a[i]]; } return a; };
  const canHear = () => !!(window.RQ && RQ.available());
  const say = (t, el) => { if(window.RQ) RQ.speak(t, el); };
  const sound = ok => { if(window.RafiqSound) RafiqSound.answer(ok); };

  function mount(el){
    const words = pool();
    if(words.length < MIN_WORDS){
      el.innerHTML = `<div class="sb-card"><p class="sb-empty">The spelling bee uses words you've met in your lessons.
        Finish a few more <b>Meet new words</b> steps on your path (you need ${MIN_WORDS} single words; you have ${words.length}),
        then come back.</p><a class="btn" href="dashboard.html">Go to your path</a></div>`;
      return;
    }
    // words due for review first, then the rest, each group shuffled
    const due = shuffle(words.filter(w => Progress.isDue('v:'+w.id)));
    const rest = shuffle(words.filter(w => !Progress.isDue('v:'+w.id)));
    // only words that were due count as a review: extra rounds are free practice,
    // so replaying can't push words weeks ahead, and a slip on a word that isn't
    // due doesn't send it back to the start of the schedule
    const dueIds = new Set(due.map(w => w.id));
    const queue = due.concat(rest).slice(0, ROUND).map((w, i) => ({w, i, retry:false, review: dueIds.has(w.id)}));
    const total = queue.length, missed = [], marks = new Array(total).fill('');
    let pos = 0, score = 0, bonus = 0, turn = Math.random() < .5 ? 0 : 1;
    // on a phone, focusing the input pops the OS keyboard over the word just shown; let them tap when ready
    const autoFocus = matchMedia('(hover:hover) and (pointer:fine)').matches;
    const bar = cur => `<div class="sb-bar" role="progressbar" aria-label="Round progress" aria-valuemin="0" aria-valuemax="${total}" aria-valuenow="${marks.filter(Boolean).length}">`+
      marks.map((m, i) => `<span class="${m}${i === cur ? ' cur' : ''}"></span>`).join('') + '</div>';

    function ask(){
      if(pos >= queue.length) return finish();
      const item = queue[pos], w = item.w;
      item.near = false;
      const mode = (turn++ % 2 === 0 && canHear()) ? 'hear' : 'see';
      const pic = (typeof PIC !== 'undefined' && PIC[w.id]) || '';
      const prompt = mode === 'hear'
        ? `<button class="sb-listen" type="button" aria-label="Play the word again">🔊</button>
           <div class="sb-how">Listen, then type the word in Arabic</div>
           <div class="sb-links"><a class="sb-hint" role="button" data-act="en">Show the English</a> · <a class="sb-hint" role="button" data-act="give">Show me the answer</a></div>
           <div class="sb-en" hidden>${esc(w.en)}</div>`
        : `${pic ? `<div class="sb-pic">${pic}</div>` : ''}<div class="sb-en">${esc(w.en)}</div>
           <div class="sb-how">Type this word in Arabic</div>
           <div class="sb-links"><a class="sb-hint" role="button" data-act="give">Show me the answer</a></div>`;
      const n = queue.slice(0, pos+1).filter(x => !x.retry).length;
      // Check sits beside the input and messages above it: on wide screens the
      // on-screen keyboard opens just below the input and would cover them
      el.innerHTML = `<div class="sb-top"><span>${item.retry ? 'One you missed' : `Word ${n} of ${total}`}</span><span>Score <b>${score}</b></span></div>
        ${bar(item.i)}
        <div class="sb-card sb-in">
          <div class="sb-prompt">${prompt}</div>
          <div class="sb-msgline" aria-live="polite"></div>
          <div class="ansrow"><input class="ar-in" dir="rtl" autocomplete="off" autocapitalize="off" spellcheck="false" placeholder="اكْتُبْ هُنا" aria-label="Your spelling">
            <button class="btn" type="button" data-act="check">Check</button></div>
          <div class="sb-out" aria-live="polite"></div>
        </div>`;
      const inp = el.querySelector('input'), out = el.querySelector('.sb-out'), msg = el.querySelector('.sb-msgline');
      if(mode === 'hear'){
        const b = el.querySelector('.sb-listen');
        b.onclick = () => say(w.ar, b); say(w.ar, b);
        const en = el.querySelector('[data-act="en"]');
        en.onclick = () => { el.querySelector('.sb-prompt .sb-en').hidden = false; en.nextSibling.remove(); en.remove(); };
      }
      let answered = false;
      const check = give => {
        if(answered) return next();
        const typed = give ? '' : inp.value.trim();
        if(!give && !letters(typed)){ msg.innerHTML = '<p class="sb-msg">Type the word first — or tap “Show me the answer”.</p>'; inp.focus(); return; }
        const t = letters(typed), target = letters(w.ar);
        const ok = t === target;
        if(!ok && !give && !item.near){
          const hint = unifyAlef(t) === unifyAlef(target) ? 'Check the hamza on the alef: أ, إ, آ or plain ا?'
            : unifyEnd(t) === unifyEnd(target) ? (/[ةه]$/.test(target) ? 'Check the last letter: ة or ه?' : 'Check the last letter: ى or ي?')
            : unifyEnd(unifyAlef(t)) === unifyEnd(unifyAlef(target)) ? 'Check the alef and the last letter.' : '';
          if(hint){ item.near = true; inp.classList.add('is-near');
            msg.innerHTML = `<p class="sb-msg sb-near sb-in">Nearly! ${hint} Try again.</p>`; inp.focus(); return; }
        }
        answered = true;
        msg.innerHTML = '';
        el.querySelector('.sb-links').remove();
        const full = ok && hasMarks(typed) && vowelled(typed) === vowelled(w.ar);
        // colour, shake and sound land on the same frame; a voluntary "show me" isn't an error, so it stays quiet
        inp.classList.remove('is-near');
        if(!give){ inp.classList.add(ok ? 'is-ok' : 'is-no'); sound(ok); }
        if(!item.retry){
          marks[item.i] = ok ? 'ok' : 'no';
          const seg = el.querySelectorAll('.sb-bar span')[item.i]; if(seg) seg.className = marks[item.i] + ' cur';
          if(item.review) Progress.grade('v:'+w.id, ok ? 'good' : 'again');
          if(ok){ score++; if(full) bonus++; }
          else { missed.push(w); queue.splice(Math.min(queue.length, pos+3), 0, {w, i:item.i, retry:true}); }
        }
        let html, answer = esc(w.ar);
        if(ok){
          html = `<p class="sb-verdict ok">✓ Correct${full ? ' <span class="sb-full">fully vowelled ✓</span>' : ''}</p>`;
        } else {
          const [mt, mw] = lcsMask([...t], [...target]);
          html = `<p class="sb-verdict no">${give ? 'Here it is' : 'Not quite'}</p>` +
            (t ? `<div class="sb-row"><span class="sb-lab">You wrote</span><span class="sb-ar">${paint(typed, mt)}</span></div>` : '');
          if(t) answer = paint(w.ar, mw);                  // letters you missed shown in red
        }
        html += `<div class="sb-row"><span class="sb-lab">${ok ? 'With vowels' : 'Answer'}</span>
          <button class="sb-word sb-ar" type="button" aria-label="Play">${answer} 🔊</button><span class="sb-gloss">${esc(w.en)}</span></div>`;
        if(!ok) html += `<p class="sb-note">${item.retry ? 'You’ll meet it again in review.' : 'This one comes back later in the round.'}</p>`;
        out.innerHTML = `<div class="sb-in">${html}</div>`;
        el.querySelector('.sb-top b').textContent = score;
        const wb = out.querySelector('.sb-word'); wb.onclick = () => say(w.ar, wb);
        inp.blur(); inp.disabled = true;   // disabled, not readOnly: a tap must not reopen the keyboard
        const nb = el.querySelector('[data-act="check"]'); nb.textContent = pos+1 >= queue.length ? 'See results' : 'Next'; nb.focus();
      };
      const next = () => { pos++; ask(); };
      el.querySelector('[data-act="check"]').onclick = () => check(false);
      el.querySelector('[data-act="give"]').onclick = () => check(true);
      inp.addEventListener('keydown', e => { if(e.key === 'Enter'){ e.preventDefault(); check(false); } });
      inp.addEventListener('input', () => inp.classList.remove('is-near'));
      if(mode === 'see' && autoFocus) inp.focus();
    }

    function finish(){
      const prev = best(), isBest = !prev || score > prev.score;
      if(isBest) saveBest(score, total);
      el.innerHTML = `${bar(-1)}<div class="sb-card sb-end sb-in">
        <div class="sb-big">${score} / ${total}</div>
        <div class="sb-how">right first time${bonus ? ` · <b>${bonus}</b> fully vowelled` : ''}</div>
        <p class="sb-best">${isBest && prev ? '🎉 New best!' : prev ? `Your best: ${prev.score} / ${prev.total}` : 'Your first round — beat it next time.'}</p>
        ${missed.length ? `<div class="sb-miss"><div class="sb-lab">To practise</div>${missed.map(w =>
          `<div class="sb-row"><button class="sb-word" type="button" data-ar="${esc(w.ar)}">${esc(w.ar)} 🔊</button><span class="sb-gloss">${esc(w.en)}</span></div>`).join('')}</div>` : ''}
        <div class="sb-actions"><button class="btn" type="button" data-act="again">Another round</button>
          <a class="btn ghost" href="#">Back to Practise</a></div></div>`;
      el.querySelectorAll('.sb-miss .sb-word').forEach(b => b.onclick = () => say(b.dataset.ar, b));
      el.querySelector('[data-act="again"]').onclick = () => mount(el);
      const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
      scrollTo({ top: 0, behavior: still ? 'auto' : 'smooth' });
    }
    ask();
  }

  window.RafiqSpelling = { mount, pool, best, letters, vowelled };
})();
