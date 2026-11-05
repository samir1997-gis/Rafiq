/* The tour of Rafiq (#348): shown once, after the first lesson and the two questions, and again from
   Settings → More. A spotlight on one thing at a time, a short note on what it's for, Next, and
   "Skip tour" at every step; nothing on the page can be pressed while it's open.
   Part 1, on Home, is all a learner needs for their 5–10 minutes a day: Continue, Your salah, reviews,
   Ask Rafiq, Progress and Settings. Then they choose: done, or "Show me more", which carries on through
   the Practise page (part 2: the extra practice, none of it required).
   localStorage rafiq_tour: 'home' = part 1 is waiting on Home, 'more' = part 2 is waiting on Practise.
   Moves ease (MOTION-STYLE): the spotlight springs to each place with a slight overshoot, the note eases in. */
(function(){
  const KEY = 'rafiq_tour';
  const get = () => { try{ return localStorage.getItem(KEY); }catch(_){ return null; } };
  const set = v => { try{ v ? localStorage.setItem(KEY, v) : localStorage.removeItem(KEY); }catch(_){} };
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const esc = t => String(t).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const shown = e => !!(e && e.getClientRects().length && getComputedStyle(e).visibility !== 'hidden');
  /* A section in the bottom bar on a phone, or in the top menu on a computer. */
  const tab = href => [...document.querySelectorAll(`.tabbar a[href="${href}"], .navlinks a[href="${href}"]`)].find(shown) || null;
  const q = sel => () => { const e = document.querySelector(sel); return shown(e) ? e : null; };

  const CSS = `
#tour{position:fixed;inset:0;z-index:1000}
#tour .t-block{position:absolute;inset:0}
#tour .t-spot{position:fixed;border-radius:14px;box-shadow:0 0 0 9999px rgba(10,16,18,.62);pointer-events:none;
  transition:top .46s cubic-bezier(.34,1.3,.64,1),left .46s cubic-bezier(.34,1.3,.64,1),width .46s cubic-bezier(.34,1.3,.64,1),height .46s cubic-bezier(.34,1.3,.64,1),opacity .3s ease-out}
#tour .t-spot::after{content:'';position:absolute;inset:-4px;border-radius:18px;border:2px solid var(--gold,#c9a227);opacity:.9}
#tour .t-spot.none{opacity:1;width:0!important;height:0!important}
#tour .t-spot.none::after{display:none}
#tour .t-tip{position:fixed;width:min(340px,calc(100vw - 24px));background:var(--card);color:var(--ink);border:1px solid var(--rule);border-radius:16px;
  padding:16px 16px 12px;box-shadow:0 18px 40px -12px rgba(0,0,0,.45);font-family:var(--la)}
#tour .t-tip.in{animation:t-in .36s cubic-bezier(.22,1,.36,1) both}
@keyframes t-in{from{opacity:0;transform:translateY(8px) scale(.98)}to{opacity:1;transform:none}}
#tour .t-k{font-family:var(--ut);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-soft)}
#tour h3{font-size:18px;font-weight:800;margin:4px 0 6px}
#tour p{font-size:14.5px;line-height:1.5;color:var(--ink-soft);margin:0}
#tour p b{color:var(--ink)}
#tour .t-row{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-top:14px}
#tour .t-skip{background:none;border:none;color:var(--ink-soft);font:600 13px var(--la);text-decoration:underline;cursor:pointer;padding:8px 2px}
#tour .t-btns{display:flex;gap:8px}
#tour .t-go{border:none;border-radius:999px;background:var(--verdigris);color:#fff;font:800 14px var(--la);padding:10px 18px;cursor:pointer;
  touch-action:manipulation;transition:transform var(--press,120ms) var(--ease-out,ease-out)}
#tour .t-go.ghost{background:var(--paper);color:var(--ink);border:1px solid var(--rule)}
#tour .t-go:active{transform:scale(.96)}
@media (prefers-reduced-motion:reduce){#tour .t-spot{transition:none}#tour .t-tip.in{animation:none}}`;

  function run(steps, onEnd){
    steps = steps.filter(s => !s.target || s.target());           // a stop whose thing isn't on this page is left out
    if(!steps.length) return onEnd && onEnd('done');
    const st = document.createElement('style'); st.textContent = CSS; document.head.appendChild(st);
    const root = document.createElement('div'); root.id = 'tour'; root.setAttribute('role', 'dialog'); root.setAttribute('aria-modal', 'true');
    root.innerHTML = '<div class="t-block"></div><div class="t-spot none"></div><div class="t-tip" aria-live="polite"></div>';
    document.body.appendChild(root);
    const spot = root.querySelector('.t-spot'), tip = root.querySelector('.t-tip');
    let i = 0, el = null;
    const end = how => { root.remove(); st.remove(); removeEventListener('resize', place); removeEventListener('scroll', place, true); onEnd && onEnd(how); };
    function place(){
      const W = innerWidth, H = innerHeight, tw = Math.min(340, W - 24);
      if(!el){                                                    // no target: the note in the middle, everything dimmed
        spot.classList.add('none'); spot.style.top = H/2 + 'px'; spot.style.left = W/2 + 'px';
        tip.style.left = (W - tw)/2 + 'px'; tip.style.top = Math.max(16, (H - tip.offsetHeight)/2) + 'px'; return;
      }
      spot.classList.remove('none');
      const r = el.getBoundingClientRect(), pad = 6;
      Object.assign(spot.style, {top: r.top - pad + 'px', left: r.left - pad + 'px', width: r.width + pad*2 + 'px', height: r.height + pad*2 + 'px'});
      const th = tip.offsetHeight, below = r.bottom + pad + 14, above = r.top - pad - 14 - th;
      const top = below + th <= H - 10 ? below : above >= 10 ? above : Math.max(10, H - th - 10);
      tip.style.top = top + 'px';
      tip.style.left = Math.min(Math.max(12, r.left + r.width/2 - tw/2), W - tw - 12) + 'px';
    }
    function paint(){
      const s = steps[i]; el = s.target ? s.target() : null;
      const last = i === steps.length - 1;
      tip.innerHTML = `<div class="t-k">${esc(s.k || `${i + 1} of ${steps.length}`)}</div><h3>${esc(s.title)}</h3><p>${s.text}</p>
        <div class="t-row">${s.noSkip ? '<span></span>' : '<button class="t-skip" type="button">Skip tour</button>'}<div class="t-btns">${
          (s.buttons || [{t: last ? 'Done' : 'Next', go: 'next'}]).map((b, j) => `<button class="t-go${b.ghost ? ' ghost' : ''}" type="button" data-j="${j}">${esc(b.t)}</button>`).join('')}</div></div>`;
      const sk = tip.querySelector('.t-skip'); if(sk) sk.onclick = () => end('skip');
      tip.querySelectorAll('.t-go').forEach(b => b.onclick = () => {
        const a = (s.buttons || [{go: 'next'}])[+b.dataset.j].go;
        if(a === 'next'){ if(last) return end('done'); i++; paint(); } else end(a);
      });
      tip.classList.remove('in'); void tip.offsetWidth; tip.classList.add('in');
      if(el){ el.scrollIntoView({block: 'center', behavior: still ? 'auto' : 'smooth'}); setTimeout(place, still ? 0 : 380); }
      place();
      const go = tip.querySelector('.t-go:last-child'); if(go) go.focus({preventScroll: true});
    }
    addEventListener('resize', place); addEventListener('scroll', place, true);
    paint();
  }

  /* Wait (up to 6 s) for the page to draw the thing the tour starts from. */
  const ready = (sel, then) => { const t0 = Date.now(), k = () => document.querySelector(sel) ? setTimeout(then, 250) : Date.now() - t0 < 6000 && setTimeout(k, 120); k(); };

  function home(){
    let name = ''; try{ name = (localStorage.getItem('bay_name') || '').trim().split(/\s+/)[0]; }catch(_){}
    const tutor = typeof TUTOR_ON !== 'undefined' && TUTOR_ON;
    run([
      {k: 'A quick tour', title: `Welcome to Rafiq${name ? ', ' + name : ''} 👋`,
       text: 'Let’s show you around in under a minute: just what you need for your daily <b>5 to 10 minutes</b>. You can skip any time.',
       buttons: [{t: 'Show me', go: 'next'}]},
      {target: q('#home .today-card .cont'), title: 'Your daily lesson',
       text: 'This is the only button you need each day: press <b>Continue</b>. Each step takes 5 to 10 minutes, and Rafiq picks what comes next: new words, a conversation, grammar or a review.'},
      {target: q('#home .sring'), title: 'Your salah',
       text: 'How much of your prayer you understand, word by word. Tap the ring to see the whole prayer, or <b>Next</b> to learn the next part.'},
      {target: q('#home .htiles .htile'), title: 'Reviews',
       text: 'Words come back just before you’d forget them. When some are due, the number shows here.'},
      tutor && {target: () => tab('tutor.html'), title: 'Ask Rafiq',
       text: 'Stuck on something? Ask Rafiq anything about Arabic or your lessons. After a wrong answer in a lesson, tap <b>Why?</b> to see what went wrong.'},
      {target: () => tab('progress.html'), title: 'Your progress',
       text: 'Your streak, the words you know, and how far you are through each unit.'},
      {target: () => tab('settings.html'), title: 'Settings',
       text: 'Change your <b>daily goal</b> and <b>reminder time</b>, the voice and how fast it speaks, tiles or typing for your answers, light or dark, and your plan.'},
      {k: 'That’s the essentials', title: 'You’re all set 🎉',
       text: 'Press <b>Continue</b> each day and you’re on track. Want to see the extra practice too? Spelling bee, verbs, real-life scenes and more. None of it is required.',
       noSkip: true, buttons: [{t: 'Show me more', go: 'more', ghost: true}, {t: 'Done', go: 'done'}]}
    ].filter(Boolean), how => {
      if(how === 'more'){ set('more'); location.href = 'practise.html'; } else set(null);
    });
  }

  function practise(){
    const row = h => q(`#picker .prow[href="${h}"]`);
    run([
      {target: () => tab('practise.html') || q('#picker .plist')(), k: 'Show me more', title: 'Practise',
       text: 'Extra practice for whenever you want more. Your daily lessons already cover everything: use these as much or as little as you like.'},
      {target: row('#salah'), title: 'Your salah practice',
       text: 'Pray along with each word lit up with its meaning, your 50 most-said words, and quick quizzes on the parts you’ve done.'},
      {target: row('session.html?focus=weak'), title: 'Weak-spots review',
       text: 'Exercises built from the mistakes <b>you</b> keep making, about 5 minutes.'},
      {target: row('#spelling'), title: 'Spelling bee',
       text: 'Hear a word or see its meaning, then type it in Arabic. The right letters pass; vowel marks earn a bonus.'},
      {target: row('#essentials'), title: 'Everyday essentials',
       text: 'Numbers, days, Hijri months, colours, telling the time and the body: a table to look things up, and a short drill for each.'},
      {target: row('#beyond'), title: 'Beyond the lessons',
       text: '21 verbs in every form, the words that join ideas together, and flashcards of every word you’ve met.'},
      {target: row('#scenes'), title: 'Real-life scenes',
       text: 'The airport, the doctor, the masjid, a restaurant, a taxi, a family visit: reply in your own words and get feedback.'},
      {target: row('#redo'), title: 'Redo a unit',
       text: 'A fresh round of a unit you’ve finished, good before moving on or to refresh an older one.'},
      {k: 'The end', title: 'That’s the tour',
       text: 'You can see it again any time from <b>Settings → More</b>.', noSkip: true,
       buttons: [{t: 'Back to Home', go: 'home'}]}
    ], how => { set(null); if(how === 'home') location.href = 'dashboard.html'; });
  }

  window.RafiqTour = {
    again(){ set('home'); location.href = 'dashboard.html'; },
    start(){                                                      // called by Home and Practise once they're drawn
      const t = get(), page = location.pathname.split('/').pop() || 'index.html';
      if(t === 'home' && page === 'dashboard.html') ready('#home .today-card .cont', home);
      if(t === 'more' && page === 'practise.html') ready('#picker .plist', practise);
    }
  };
  if(document.readyState === 'loading') addEventListener('DOMContentLoaded', () => RafiqTour.start()); else RafiqTour.start();
})();
