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
  const LIVE = true;   // on in this branch for testing: set back to false (or get the teacher's sign-off) before merging into main
  /* The licensed recitation comes from the Quran Foundation API through our own
     function (supabase/functions/quran, #135): one file per verse, with word timings.
     Kept in memory for the page only, since QF's terms allow no more than a week of
     caching. Until that function has its QF keys, or offline, Quran parts stay
     silent read-alongs. */
  const recited = {};            // "112:1" -> {url, segments} | null (asked, none)
  let credit = '', lastError = '';   // why the last request brought nothing: 'signin', 'offline', …

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
  /* Plans (#125, chosen with TypeSafe: pricing_revenue.py): the most-said words are in
     every plan, as a taster; the rest (every part of the prayer, the surahs, Pray along,
     the drills) is Complete. The free week is Complete, so everyone tries it all. */
  const complete = () => !window.RafiqPlan || RafiqPlan.isComplete();
  const open = p => !!p && (p.kind === 'common' || complete());
  const done = id => !!(P() && P().hasSeen('sp:' + id));
  const next = () => parts().find(p => !done(p.id)) || null;
  const stateOf = p => done(p.id) ? 'done' : !open(p) ? 'plan' : (next() === p ? 'next' : 'locked');
  // no punctuation, and the shadda always before its vowel (the Quran text writes it after)
  const bare = s => String(s).replace(/[۝؟?!.،,:؛﴿﴾0-9٠-٩]/g, '').replace(/([\u064B-\u0650\u0652])\u0651/g, '\u0651$1').trim();
  const wid = w => 'sw:' + bare(w.ar);
  const known = w => !!(P() && !P().isNew(wid(w)));

  const allWords = p => p.lines.reduce((a, l) => a.concat(l.words), []);
  // distinct words (by their written form) in a part, or in the whole prayer
  function distinct(ws){ const m = new Map(); ws.forEach(w => { const k = wid(w); if(!m.has(k)) m.set(k, w); }); return [...m.values()]; }
  /* How often each word is said in a normal 4-rakah prayer (#124): takbir 22 times,
     Al-Fatiha, bowing and rising 4 (the tasbih of bowing 3 times each, of prostration
     3 times in each of 8 prostrations; 'my Lord, forgive me' once between each pair),
     tashahhud and salam twice, salawat once. A number per line where lines differ.
     Surahs vary, so they aren't counted. The teacher checks these numbers too. */
  const REPS = { takbir:22, opening:1, refuge:1, fatiha1:4, fatiha2:4, ruku:12, rising:4, sujud:[24,4], tashahhud:2, salawat:1, taslim:2 };
  const FREQ = {};
  SALAH.parts.forEach(p => { const r = REPS[p.id]; if(r) p.lines.forEach((l, i) => { const n = Array.isArray(r) ? (r[i] || 0) : r;
    l.words.forEach(w => { const k = 'sw:' + bare(w.ar); FREQ[k] = (FREQ[k] || 0) + n; }); }); });
  const freq = w => FREQ[wid(w)] || 0;
  // words said in the prayer's own phrases (not the Quran): these may be voiced
  // (and how the prayer spells them, which is what was recorded: the Quran text orders the marks differently)
  const VOICED = new Map(); SALAH.parts.forEach(p => { if(p.group === 'prayer' && !/^fatiha/.test(p.id)) allWords(p).forEach(w => { if(!VOICED.has(wid(w))) VOICED.set(wid(w), w.ar); }); });
  const voiced = w => VOICED.has(wid(w));
  const sayAr = w => VOICED.get(wid(w)) || w.ar;

  /* "Your most-said words": the 20 words said most (over half of everything said in
     the prayer), chosen with TypeSafe (salah_learning.py) to get people going, as
     four small parts of 5 (salah_opener_size.py: easiest to take in). Word by word +
     a short check, no whole line to recite. */
  if(!SALAH.parts.some(p => p.kind === 'common')){
    const top = distinct(SALAH.parts.filter(p => REPS[p.id]).reduce((a, p) => a.concat(allWords(p)), []))
      .filter(w => w.root).sort((a, b) => freq(b) - freq(a)).slice(0, 20);
    const all = Object.values(FREQ).reduce((a, n) => a + n, 0), pct = ws => Math.round(100 * ws.reduce((a, w) => a + freq(w), 0) / all);
    const sets = []; for(let i = 0; i < top.length; i += 5) sets.push(top.slice(i, i + 5));
    SALAH.parts.unshift(...sets.map((ws, i) => ({ id: 'common' + (i + 1), group: 'start', kind: 'common',
      title: `Most-said words ${i * 5 + 1}–${i * 5 + ws.length}`, ar_title: 'أَكْثَرُ الْكَلِماتِ',
      what: i === 0 ? `The 20 words you say most are about ${pct(top)}% of everything you say in a four-rakah prayer. These first 5 alone are ${pct(ws)}%.`
                    : `These 5 are another ${pct(ws)}% of what you say in a four-rakah prayer.`,
      lines: [{ ar: '', en: '', words: ws }] })));
  }
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

  /* Recitation for a Quran line ("112:1"): {url, segments}, or null. */
  const recitation = line => (line && line.ref && recited[line.ref]) || null;
  /* True while some of these lines haven't been asked for yet. */
  const needsRecitation = lines => lines.some(l => l.ref && !(l.ref in recited));
  /* Which of our words each of QF's words covers: [[first, after last], …] in QF's order,
     or null if they can't be matched. Compared by consonants only, so vowel marks and the
     Uthmani script's spellings (ٱ, مَٰلِكِ for مالك) don't count as differences. */
  const skel = t => String(t).replace(/[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED\u0640]/g, '').replace(/[اأإآٱىيوءئؤ]/g, '');
  function matchWords(line, qf){
    if(!Array.isArray(qf) || !qf.length || typeof qf[0] !== 'object') return null;
    const map = []; let j = 0;
    for(const q of qf){
      const want = skel(q.t), start = j; let got = '';
      do { if(j >= line.words.length) return null; got += skel(line.words[j].ar); j++; } while(got.length < want.length);
      if(got !== want) return null;
      map.push([start, j]);
    }
    return j === line.words.length ? map : null;
  }
  /* Every Quran line of the track: they're all asked for in one go, so the official
     meanings are the same everywhere (lessons, checks, review, drills, the map). */
  const quranLines = () => parts().reduce((a, p) => a.concat(p.lines.filter(l => l.ref)), []);
  /* The Quran's meanings come from the official translation and Quran.com's word-by-word
     English (#147), replacing our drafts while the page is open; the drafts stay in
     salah-data.js only as the fallback when that can't be reached. */
  let official = false;
  function useOfficial(line, v){
    if(!v) return;
    if(v.translation) line.en = v.translation;
    // a QF word that is one of ours gets QF's meaning; where QF joins two of ours
    // (يَٰٓأَيُّهَا) ours keep their separate meanings ("O", "you")
    const map = matchWords(line, v.words);
    if(map) map.forEach(([a, b], q) => { if(b - a === 1 && v.words[q].en) line.words[a].en = v.words[q].en; });
    official = true;
  }
  const ready = () => needsRecitation(quranLines()) ? loadRecitation() : Promise.resolve();
  async function loadRecitation(){
    const lines = quranLines();
    const keys = [...new Set(lines.map(l => l.ref).filter(k => k && !(k in recited)))];
    if(!keys.length) return;
    let r = null;
    try{ if(window.RafiqPlan && RafiqPlan.call) r = await RafiqPlan.call('quran', { verses:keys }); }catch(_){}
    // remember a verse only when the server answered for it; a failed request is
    // asked again next time a part opens, not silent for the rest of the visit
    if(r && r.verses){
      keys.forEach(k => { recited[k] = r.verses[k] || null; });
      lines.forEach(l => useOfficial(l, recited[l.ref]));
    }
    else keys.forEach(k => { recited[k] = null; setTimeout(() => { delete recited[k]; }, 30000); });
    if(r && r.credit) credit = r.credit;
    lastError = r && r.verses ? '' : ((r && r.error) || 'offline');
  }
  /* When each word of a line is said: [[startMs, endMs] per word] or null.
     Quran: the recitation's timings, QF's [position from 1, start, end] or quran-align's
     [first word from 0, word after last, start, end] (#140). Prayer phrases: measured
     from our own recording (salah-timings.js, tools/align-salah.js). */
  function timings(line){
    if(!line) return null;
    if(!line.ref){
      const id = window.RQ && RQ.clipId && RQ.clipId(line.ar);
      const t = id && typeof SALAH_TIMINGS !== 'undefined' && SALAH_TIMINGS[id];
      return t && t.length === line.words.length ? t : null;
    }
    const r = recitation(line), segs = r && r.segments;
    if(!segs || !segs.length) return null;
    // timings count QF's words; turn them into ours (يَٰٓأَيُّهَا is one QF word, two of ours)
    const map = matchWords(line, r.words) || line.words.map((_, i) => [i, i + 1]);
    const n = line.words.length, owner = new Array(n).fill(-1);
    const groups = segs.map((s, g) => {
      const [a, b, t0, t1] = s.length >= 4 ? [s[0], s[1], s[2], s[3]] : [s[0] - 1, s[0], s[1], s[2]];
      for(let q = Math.max(0, a); q < b && q < map.length; q++)
        for(let k = map[q][0]; k < map[q][1] && k < n; k++) owner[k] = g;
      return { t0, t1, words: [] };
    });
    /* A word the timings leave out (109:1 has 3 timed of 4) shares the time of the
       word before it (or after, at the start); a time covering several words is
       split between them by length. */
    for(let k = 0; k < n; k++){
      let g = owner[k];
      for(let j = k - 1; g < 0 && j >= 0; j--) g = owner[j];
      for(let j = k + 1; g < 0 && j < n; j++) g = owner[j];
      if(g < 0) return null;
      groups[g].words.push(k);
    }
    const len = k => line.words[k].ar.replace(/[\u064b-\u0652\u0670\u0640]/g, '').length + 1;
    const out = new Array(n);
    groups.forEach(({ t0, t1, words }) => {
      const total = words.reduce((x, k) => x + len(k), 0); let at = t0;
      words.sort((x, y) => x - y).forEach(k => { const e = at + (t1 - t0) * len(k) / total; out[k] = [Math.round(at), Math.round(e)]; at = e; });
    });
    return out;
  }

  /* The Home card: its Continue goes straight into the next part; the card opens the overview. */
  function cardHTML(){
    const n = next(), c = counts();
    if(n && !open(n)) return `<div class="salah-card"><a class="sc-open" href="salah.html" aria-label="Your salah: open the overview">
        <span class="sc-ic" aria-hidden="true">🕌</span><span class="sc-tx"><b>Your salah</b><span>Your 20 most-said words ✓ · the whole prayer is in Complete</span></span></a>
      <a class="sc-go" href="plans.html">See Complete</a></div>`;
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
    const list = opts.prayerOnly ? parts().filter(p => p.group === 'prayer') : parts().filter(p => p.kind !== 'common');
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
    if(!official) ready().then(() => { if(official) el.querySelector('.smap').outerHTML = mapHTML(opts); });   // official meanings once loaded
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

  window.RafiqSalah = { enabled, LIVE, complete, open, parts, part, isQuran, done, next, stateOf, words, counts, wid, known, freq, voiced, sayAr,
    courseWords, courseKnown, bridgeFor, recitation, needsRecitation, loadRecitation, ready, officialMeanings:()=>official, timings, credit:()=>credit, recitationError:()=>lastError, cardHTML, styles, mapHTML, mountMap, finishPart, due, wordById, esc };
})();
