/* salah.js — "Your salah": understand every word of the prayer (#38).

   Design, all chosen with TypeSafe (tools/typesafe-exp/salah_design.py):
   - a "Your salah" card on Home under the daily path, also reachable from
     Practise; its Continue goes straight into the next part, tapping the card
     opens the overview (salah.html): the prayer in order, the map, Review
   - one part is about 5 minutes, words first: Listen · Word by word (with a
     course word from the same root) · Check · Put it together · Follow along
     (learn.html?salah=<part>), then the words join spaced review
   - its own progress: it never counts towards (or gets in the way of) the
     main course's daily goal
   - bridge cards in lessons ("You'll hear this in your salah") and the map on
     Progress

   Content (salah-data.js) awaits a teacher's sign-off, so the whole feature is
   OFF until LIVE is set to true. To preview it on one device, open any page with
   ?salah_preview=1 (and ?salah_preview=0 to hide it again).

   Audio rule: prayer phrases may use the app's recorded voice; Quran (Al-Fatiha
   and the surahs) only ever a licensed human recitation, never a generated or
   device voice. Until RECITATION is set, Quran parts are silent read-alongs.

   Needs salah-data.js (SALAH) and progress.js (Progress); vocab-data.js (VOCAB)
   for the links to course words. */
(function(){
  const LIVE = false;
  /* A licensed recitation, one file per verse: RECITATION + '001001.mp3' (surah,
     verse, three digits each), e.g. files placed in audio/quran/. null = none yet. */
  const RECITATION = null;

  function enabled(){
    if(LIVE) return true;
    try{
      const q = new URLSearchParams(location.search).get('salah_preview');
      if(q === '1') localStorage.setItem('rafiq_salah_preview', '1');
      if(q === '0') localStorage.removeItem('rafiq_salah_preview');
      return localStorage.getItem('rafiq_salah_preview') === '1';
    }catch(_){ return false; }
  }
  if(typeof SALAH === 'undefined') { window.RafiqSalah = { enabled: () => false }; return; }

  const esc = t => String(t).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const parts = () => SALAH.parts;
  const part = id => SALAH.parts.find(p => p.id === id) || null;
  const isQuran = p => p.group === 'surah' || /^fatiha/.test(p.id);
  const P = () => window.Progress;

  /* Progress: a part is done once finished (sp:<id>); each word is reviewed as sw:<word>. */
  const done = id => !!(P() && P().hasSeen('sp:' + id));
  const next = () => parts().find(p => !done(p.id)) || null;
  const stateOf = p => done(p.id) ? 'done' : (next() === p ? 'next' : 'locked');
  const bare = s => String(s).replace(/[۝؟?!.،,:؛﴿﴾0-9٠-٩]/g, '').trim();
  const wid = w => 'sw:' + bare(w.ar);
  const known = w => !!(P() && !P().isNew(wid(w)));

  const allWords = p => p.lines.reduce((a, l) => a.concat(l.words), []);
  // distinct words (by their written form) in a part, or in the whole prayer
  function distinct(ws){ const m = new Map(); ws.forEach(w => { const k = wid(w); if(!m.has(k)) m.set(k, w); }); return [...m.values()]; }
  const words = p => distinct(p ? allWords(p) : parts().reduce((a, x) => a.concat(allWords(x)), []));
  const counts = p => { const ws = words(p); return { known: ws.filter(known).length, total: ws.length }; };

  /* Links to the main course: SALAH.links maps a course word id to its roots;
     SALAH.where maps a root to where it's said: [partId, line, word]. */
  const byRoot = (() => { const m = {}; Object.entries(SALAH.links || {}).forEach(([id, roots]) => roots.forEach(r => (m[r] = m[r] || []).push(+id))); return m; })();
  function courseWords(root){
    if(!root || typeof VOCAB === 'undefined') return [];
    const ids = byRoot[root] || [];
    return VOCAB.filter(v => ids.includes(v.id));
  }
  const courseKnown = v => !!(P() && !P().isNew('v:' + v.id));
  /* For a course word: where its root is said in the prayer (prayer parts first). */
  function bridgeFor(vocabId){
    const roots = (SALAH.links || {})[vocabId] || [];
    for(const group of ['prayer', 'surah']) for(const r of roots){
      for(const [pid, li, wi] of (SALAH.where || {})[r] || []){
        const p = part(pid); if(!p || p.group !== group) continue;
        const line = p.lines[li]; if(!line || !line.words[wi]) continue;
        return { part: p, line, word: line.words[wi], index: wi, root: r };
      }
    }
    return null;
  }

  /* Recitation for a Quran line ("112:1"), or null. */
  function recitation(line){
    if(!RECITATION || !line.ref) return null;
    const [s, a] = line.ref.split(':').map(Number);
    return RECITATION + String(s).padStart(3, '0') + String(a).padStart(3, '0') + '.mp3';
  }

  /* The Home card: its Continue goes straight into the next part; the card opens the overview. */
  function cardHTML(){
    const n = next(), c = counts();
    const sub = n ? `${esc(n.title)} · ${c.known} of ${c.total} words understood` : `Every part done · ${c.known} of ${c.total} words understood`;
    return `<div class="salah-card"><a class="sc-open" href="salah.html" aria-label="Your salah: open the overview">
        <span class="sc-ic" aria-hidden="true">🕌</span><span class="sc-tx"><b>Your salah</b><span>${sub}</span></span></a>
      <a class="sc-go" href="${n ? 'learn.html?salah=' + n.id : 'learn.html?salah=review'}">${n ? 'Continue' : 'Review'}</a></div>`;
  }
  const CARD_CSS = `.salah-card{display:flex;align-items:center;gap:12px;background:var(--card);border:1px solid var(--rule);border-radius:14px;padding:14px 14px 14px 16px;margin:0 0 14px}
.salah-card .sc-open{flex:1;display:flex;align-items:center;gap:12px;color:var(--ink);text-decoration:none;min-width:0}
.salah-card .sc-ic{font-size:26px;flex:0 0 auto}
.salah-card .sc-tx{display:flex;flex-direction:column;min-width:0}
.salah-card .sc-tx b{font-size:16px}
.salah-card .sc-tx span{font-size:13px;color:var(--ink-soft);line-height:1.4}
.salah-card .sc-go{flex:0 0 auto;background:var(--verdigris);color:var(--paper);text-decoration:none;font-weight:700;font-size:14px;border-radius:999px;padding:10px 16px;min-height:40px;display:flex;align-items:center}
.smap{display:grid;gap:12px}
.smap .sp{background:var(--card);border:1px solid var(--rule);border-radius:12px;padding:12px 14px}
.smap .sp h4{margin:0 0 6px;font-size:14px;display:flex;justify-content:space-between;gap:8px}
.smap .sp h4 span{color:var(--ink-soft);font-weight:400;font-size:12.5px}
.smap .sl{font-family:var(--ar);direction:rtl;font-size:21px;line-height:2}
.smap .w{color:var(--ink-soft);opacity:.55;cursor:pointer;border-radius:6px;padding:0 2px}
.smap .w.k{color:var(--ink);opacity:1;background:color-mix(in srgb,var(--verdigris) 16%,transparent)}
.smap .w.r{opacity:.9;border-bottom:2px dotted var(--gold)}
.smap .key{font-size:12.5px;color:var(--ink-soft);display:flex;gap:14px;flex-wrap:wrap;margin:0 0 4px}
.smap .key i{font-style:normal;padding:0 4px;border-radius:4px}
.smap .key .k{background:color-mix(in srgb,var(--verdigris) 16%,transparent);color:var(--ink)}
.smap .key .r{border-bottom:2px dotted var(--gold)}
.smap .tip{font-size:13.5px;color:var(--ink);min-height:20px}`;
  function styles(){
    if(document.getElementById('salah-css')) return;
    const s = document.createElement('style'); s.id = 'salah-css'; s.textContent = CARD_CSS; document.head.appendChild(s);
  }

  /* The "Your salah" map: the prayer in order, words you understand lit up; a word
     whose root you know from the course is underlined. Tap a word for its meaning. */
  function mapHTML(opts = {}){
    const learnedRoots = new Set();
    if(typeof VOCAB !== 'undefined') Object.entries(SALAH.links || {}).forEach(([id, roots]) => { if(courseKnown({id: +id})) roots.forEach(r => learnedRoots.add(r)); });
    const list = opts.prayerOnly ? parts().filter(p => p.group === 'prayer') : parts();
    return `<div class="smap"><div class="key"><span><i class="k">word</i> you understand</span><span><i class="r">word</i> its root is in your course words</span></div>
      <div class="tip" aria-live="polite">Tap a word for its meaning.</div>` +
      list.map(p => { const c = counts(p);
        return `<div class="sp"><h4>${esc(p.title)}<span>${c.known} of ${c.total}</span></h4>` +
          p.lines.map(l => `<div class="sl">${l.words.map(w =>
            `<span class="w${known(w) ? ' k' : w.root && learnedRoots.has(w.root) ? ' r' : ''}" data-en="${esc(w.en)}" data-ar="${esc(w.ar)}">${esc(w.ar)}</span>`).join(' ')}</div>`).join('') +
          `</div>`; }).join('') + `</div>`;
  }
  function mountMap(el, opts){
    styles(); el.innerHTML = mapHTML(opts);
    const tip = el.querySelector('.tip');
    el.addEventListener('click', e => { const w = e.target.closest('.w'); if(w) tip.innerHTML = `<b dir="rtl" style="font-family:var(--ar)">${esc(w.dataset.ar)}</b> · ${esc(w.dataset.en)}`; });
  }

  /* After a part: its words count as met, so they join review. */
  function finishPart(p){
    if(!P()) return;
    words(p).forEach(w => { if(P().isNew(wid(w))) P().grade(wid(w), 'good'); });
    P().touch('sp:' + p.id);
  }
  const due = () => P() ? P().dueIds('sw:') : [];
  // meaning of a reviewed word id (its first appearance)
  const wordById = id => { for(const p of parts()) for(const w of allWords(p)) if(wid(w) === id) return w; return null; };

  window.RafiqSalah = { enabled, LIVE, parts, part, isQuran, done, next, stateOf, words, counts, wid, known,
    courseWords, courseKnown, bridgeFor, recitation, cardHTML, styles, mapHTML, mountMap, finishPart, due, wordById, esc };
})();
