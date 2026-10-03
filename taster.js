/* taster.js — the landing page's one-minute taster (#207): four easy words, each
   one Arabic word and three meanings to pick from. An answer shows the right
   meaning and says the word; a wrong pick just shows the right one, nothing red.
   It never gets harder and has no score: it ends on "you just learned 4 words"
   and the free week.
   The words and their recordings are the app's own (vocab-data.js, audio.js),
   loaded once the page itself has. Doing it is noted in
   rafiq_src (source.js), which is saved with a new account, so the funnel can
   compare sign-ups who did the taster with those who didn't. */
(function(){
  const POOL = [90, 194, 150, 627, 692];        // house, water, book, door, pen (vocab-data.js ids)
  const N = 4;
  const box = document.getElementById('taster');
  if(!box) return;
  const card = box.querySelector('.tst-card');
  const esc = t => String(t).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const shuffle = a => { const b = a.slice(); for(let i = b.length - 1; i > 0; i--){ const j = Math.floor(Math.random() * (i + 1)); [b[i], b[j]] = [b[j], b[i]]; } return b; };
  const say = (t, el, after) => { if(window.RQ) RQ.speak(t, el, after); else if(after) after(); };

  // noted with where they came from (source.js): 'started', then 'done'
  function note(state){
    try{
      const s = JSON.parse(localStorage.getItem('rafiq_src') || 'null'); if(!s || s.taster === 'done') return;
      s.taster = state; localStorage.setItem('rafiq_src', JSON.stringify(s));
    }catch(_){}
  }

  const load = src => new Promise(res => { const s = document.createElement('script'); s.src = src; s.onload = s.onerror = res; document.head.appendChild(s); });
  let started = false;
  function start(){
    if(started) return; started = true;
    Promise.all([typeof VOCAB === 'undefined' ? load('vocab-data.js') : 0, window.RQ ? 0 : load('audio.js')]).then(() => {
      if(typeof VOCAB === 'undefined'){ box.hidden = true; return; }   // offline and never cached
      const pool = POOL.map(id => VOCAB.find(v => v.id === id)).filter(Boolean);
      if(pool.length < 3){ box.hidden = true; return; }
      run(shuffle(pool).slice(0, Math.min(N, pool.length)), pool);
    });
  }
  // after the page itself has loaded, so it never slows the first screen
  const soon = () => (window.requestIdleCallback || setTimeout)(start, { timeout: 1500 });
  if(document.readyState === 'complete') soon(); else addEventListener('load', soon);

  function run(words, pool){
    let k = 0;
    const ask = () => {
      const w = words[k];
      const opts = shuffle([w].concat(shuffle(pool.filter(x => x !== w)).slice(0, 2)));
      card.innerHTML = `<div class="tst-top"><span>Word ${k + 1} of ${words.length}</span>
          <span class="tst-dots" aria-hidden="true">${words.map((_, i) => `<i class="${i < k ? 'did' : i === k ? 'now' : ''}"></i>`).join('')}</span></div>
        <button type="button" class="tst-word" lang="ar" dir="rtl" aria-label="Hear it: ${esc(w.ar)}">${esc(w.ar)}<span class="tst-hear" aria-hidden="true">🔊</span></button>
        <p class="tst-q">What does it mean?</p>
        <div class="tst-opts">${opts.map(o => `<button type="button" class="tst-opt" data-id="${o.id}">${esc(o.en)}</button>`).join('')}</div>
        <p class="tst-say" aria-live="polite"></p>
        <button type="button" class="btn tst-next" hidden>${k + 1 < words.length ? 'Next word →' : 'See what you learned →'}</button>`;
      const word = card.querySelector('.tst-word'), next = card.querySelector('.tst-next'), msg = card.querySelector('.tst-say');
      word.onclick = () => say(w.ar, word);
      let done = false, moved = false;
      const go = () => { if(moved) return; moved = true; k++; k < words.length ? ask() : end(); };
      next.onclick = go;
      card.querySelectorAll('.tst-opt').forEach(b => b.onclick = () => {
        if(done) return; done = true;
        if(k === 0) note('started');
        const right = +b.dataset.id === w.id;
        card.querySelectorAll('.tst-opt').forEach(o => { o.disabled = true; if(+o.dataset.id === w.id) o.classList.add('right'); });
        if(!right) b.classList.add('picked');
        msg.textContent = right ? '✓ Nice!' : 'It’s this one. Now you know it!';
        msg.className = 'tst-say ' + (right ? 'yes' : 'soft');
        next.hidden = false;
        // the word is said either way; a right answer moves on by itself once it's been heard
        say(w.ar, word, () => { if(right) setTimeout(() => { if(next.isConnected) go(); }, 700); });
      });
    };
    const end = () => {
      note('done');
      card.innerHTML = `<div class="tst-end">
        <div class="tst-big" aria-hidden="true">🎉</div>
        <h3>You just learned ${words.length} Arabic words in under a minute.</h3>
        <div class="tst-learned">${words.map(w => `<button type="button" class="tst-chip" data-ar="${esc(w.ar)}"><span lang="ar" dir="rtl">${esc(w.ar)}</span> ${esc(w.en)}</button>`).join('')}</div>
        <p class="tst-month">Imagine what you’d know in a month.</p>
        <a class="btn tst-go" href="login.html?mode=signup">Keep the momentum going →</a>
        <p class="tst-free">7 days free, no card.</p></div>`;
      card.querySelectorAll('.tst-chip').forEach(c => c.onclick = () => say(c.dataset.ar, c));
    };
    ask();
  }
})();
