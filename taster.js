/* taster.js — the landing page's one-minute taster (#207): four easy words, two
   everyday ones and two from the prayer, each one Arabic word and three meanings
   to pick from. An answer shows the right meaning and says the word (a prayer
   word also shows the phrase it's said in); a wrong pick just shows the right
   one, nothing red. It never gets harder and has no score: it ends on "you just
   learned 4 words" and the free week.
   The words and their recordings are the app's own (vocab-data.js, salah-data.js,
   audio.js), loaded once the page itself has. Prayer words come only from the
   prayer's own phrases, never the Quran, which the app's voice never says.
   Doing it is noted in rafiq_src (source.js), which is saved with a new account,
   so the funnel can compare sign-ups who did the taster with those who didn't.
   Motion: each word slides in from the right and out to the left (the way the
   dots go), answers respond on press, and nothing below the word jumps when the
   answer appears. With reduced motion, a short cross-fade instead. */
(function(){
  const VOCAB_POOL = [90, 194, 150, 627, 692];  // house, water, book, door, pen (vocab-data.js ids)
  // said in every prayer, in its own phrases (salah-data.js: part id, word, when it's said)
  const SALAH_POOL = [['takbir', 'أَكْبَرُ', 'in the opening takbir'], ['ruku', 'سُبْحانَ', 'when bowing'], ['ruku', 'رَبِّيَ', 'when bowing'],
                      ['ruku', 'الْعَظِيمِ', 'when bowing'], ['sujud', 'الْأَعْلى', 'in prostration'], ['rising', 'الْحَمْدُ', 'when rising from bowing']];   // short phrases only, so the card never grows
  const box = document.getElementById('taster');
  if(!box) return;
  const card = box.querySelector('.tst-card');
  const esc = t => String(t).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const shuffle = a => { const b = a.slice(); for(let i = b.length - 1; i > 0; i--){ const j = Math.floor(Math.random() * (i + 1)); [b[i], b[j]] = [b[j], b[i]]; } return b; };
  const say = (t, el, after) => { if(window.RQ) RQ.speak(t, el, after); else if(after) after(); };
  const calm = () => matchMedia('(prefers-reduced-motion: reduce)').matches;
  const EASE = 'cubic-bezier(.16,1,.3,1)';      // the site's settle curve (--ease-out)

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
    Promise.all([typeof VOCAB === 'undefined' ? load('vocab-data.js') : 0, typeof SALAH === 'undefined' ? load('salah-data.js') : 0,
                 window.RQ ? 0 : load('audio.js')]).then(() => {
      const everyday = typeof VOCAB === 'undefined' ? [] : VOCAB_POOL.map(id => VOCAB.find(v => v.id === id)).filter(Boolean)
        .map(v => ({ key: 'v' + v.id, ar: v.ar, en: v.en }));
      const prayer = typeof SALAH === 'undefined' ? [] : SALAH_POOL.map(([pid, ar, when]) => {
        const p = SALAH.parts.find(x => x.id === pid), line = p && p.lines.find(l => !l.ref && l.words.some(w => w.ar === ar));
        const w = line && line.words.find(x => x.ar === ar);
        return w && { key: 's' + pid + ar, ar, en: w.en, salah: true, when, line };
      }).filter(Boolean);
      if(everyday.length < 3 || prayer.length < 3){ box.hidden = true; return; }   // offline and never cached
      const e = shuffle(everyday), s = shuffle(prayer);
      run([e[0], s[0], e[1], s[1]], { everyday, prayer });
    });
  }
  // after the page itself has loaded, so it never slows the first screen
  const soon = () => (window.requestIdleCallback || setTimeout)(start, { timeout: 1500 });
  if(document.readyState === 'complete') soon(); else addEventListener('load', soon);

  /* Swap what the card shows: the old slides out to the left, the new in from the right. */
  function show(html, bind){
    const old = card.querySelector('.tst-pane');
    const put = () => {
      card.innerHTML = `<div class="tst-pane">${html}</div>`;
      const pane = card.firstElementChild; bind(pane);
      if(old && pane.animate) pane.animate(calm() ? [{ opacity: 0 }, { opacity: 1 }]
        : [{ opacity: 0, transform: 'translateX(28px)' }, { opacity: 1, transform: 'none' }], { duration: calm() ? 160 : 380, easing: EASE });
    };
    if(!old || !old.animate) return put();
    old.style.pointerEvents = 'none';
    old.animate(calm() ? [{ opacity: 1 }, { opacity: 0 }] : [{ opacity: 1, transform: 'none' }, { opacity: 0, transform: 'translateX(-28px)' }],
      { duration: calm() ? 120 : 170, easing: 'cubic-bezier(.4,0,1,1)', fill: 'forwards' }).onfinish = put;
  }

  function run(words, pools){
    let k = 0;
    const dots = i => `<span class="tst-dots" aria-hidden="true">${words.map((_, j) => `<i class="${j < i ? 'did' : j === i ? 'now' : ''}"></i>`).join('')}</span>`;
    const ask = () => {
      const w = words[k], pool = w.salah ? pools.prayer : pools.everyday;
      const others = shuffle(pool.filter(x => x.key !== w.key && x.en !== w.en));
      const opts = shuffle([w].concat(others.slice(0, 2)));
      const from = w.salah ? `<p class="tst-from"><span class="lab">You say it ${esc(w.when)}</span>
          <span class="ar" lang="ar" dir="rtl">${w.line.words.map(x => x.ar === w.ar ? `<b>${esc(x.ar)}</b>` : esc(x.ar)).join(' ')}</span>
          <span class="en">${esc(w.line.en)}</span></p>` : '';
      show(`<div class="tst-top"><span>Word ${k + 1} of ${words.length}</span>${dots(k)}</div>
        <p class="tst-tag">${w.salah ? '🕌 From your prayer' : 'An everyday word'}</p>
        <button type="button" class="tst-word" lang="ar" dir="rtl" aria-label="Hear it: ${esc(w.ar)}">${esc(w.ar)}<span class="tst-hear" aria-hidden="true">🔊</span></button>
        <p class="tst-q">What does it mean?</p>
        <div class="tst-opts">${opts.map(o => `<button type="button" class="tst-opt" data-key="${esc(o.key)}">${esc(o.en)}</button>`).join('')}</div>
        <div class="tst-after"><p class="tst-say" aria-live="polite"></p>${from}
          <button type="button" class="btn tst-next">${k + 1 < words.length ? 'Next word →' : 'See what you learned →'}</button></div>`, pane => {
        const word = pane.querySelector('.tst-word'), next = pane.querySelector('.tst-next'), msg = pane.querySelector('.tst-say'), after = pane.querySelector('.tst-after');
        word.onclick = () => say(w.ar, word);
        let done = false, moved = false;
        const go = () => { if(moved) return; moved = true; k++; k < words.length ? ask() : end(); };
        next.onclick = go;
        pane.querySelectorAll('.tst-opt').forEach(b => b.onclick = () => {
          if(done) return; done = true;
          if(k === 0) note('started');
          const right = b.dataset.key === w.key;
          pane.querySelectorAll('.tst-opt').forEach(o => { o.disabled = true; if(o.dataset.key === w.key) o.classList.add('right'); else o.classList.add('quiet'); });
          if(!right) b.classList.add('picked');
          const r = pane.querySelector('.tst-opt.right');
          if(right && r.animate && !calm()) r.animate([{ transform: 'scale(1)' }, { transform: 'scale(1.03)' }, { transform: 'scale(1)' }], { duration: 320, easing: EASE });
          msg.textContent = right ? '✓ Nice!' : 'It’s this one. Now you know it!';
          msg.className = 'tst-say ' + (right ? 'yes' : 'soft');
          after.classList.add('on');                   // its room was kept, so nothing moves
          // the word is said with the reveal; a right answer moves on by itself once it's been heard
          say(w.ar, word, () => { if(right) setTimeout(() => { if(next.isConnected) go(); }, w.salah ? 1600 : 700); });
        });
      });
    };
    const end = () => {
      note('done');
      const n = words.filter(w => w.salah).length;
      show(`<div class="tst-end">
        <div class="tst-big" aria-hidden="true">🎉</div>
        <h3>You just learned ${words.length} Arabic words in under a minute${n ? `, including ${n} you say in every prayer` : ''}.</h3>
        <div class="tst-learned">${words.map(w => `<button type="button" class="tst-chip" data-ar="${esc(w.ar)}">${w.salah ? '<i aria-hidden="true">🕌</i>' : ''}<span lang="ar" dir="rtl">${esc(w.ar)}</span> ${esc(w.en)}</button>`).join('')}</div>
        <p class="tst-month">Imagine what you’d know in a month.</p>
        <a class="btn tst-go" href="login.html?mode=signup">Keep the momentum going →</a>
        <p class="tst-free">7 days free, no card.</p></div>`, pane => {
        pane.querySelectorAll('.tst-chip').forEach(c => c.onclick = () => say(c.dataset.ar, c));
        // the pieces settle in one after another
        if(!calm() && pane.animate) [...pane.querySelector('.tst-end').children].forEach((el, i) =>
          el.animate([{ opacity: 0, transform: 'translateY(10px)' }, { opacity: 1, transform: 'none' }], { duration: 420, delay: 120 + i * 70, easing: EASE, fill: 'backwards' }));
      });
    };
    ask();
  }
})();
