/* teach.js — teach first (#156), for the units in RafiqPath.teaches (1-3).

   RafiqTeach.parts(ar)          a phrase taken apart: [[word, meaning], ...], or null.
                                 Shown under a phrase when it's met, so a greeting
                                 isn't just a sound to copy.
   RafiqTeach.taught(unitN)      the words a learner has been taught by that unit's
                                 Practise step: every word of the unit and the units
                                 before it, the examples on their grammar cards, plus a
                                 few little words used everywhere.
   RafiqTeach.coverage(text, k)  the share of the words in `text` that are in k (0-1),
                                 allowing for و/ال/بِ/لِ on the front, ‘my’/‘your’ endings,
                                 and present and past verb forms.
   Needs vocab-data.js (VOCAB) and path-data.js (PATH). */
(function(){
  // the greeting phrases of unit 1, word by word (checked in REVIEW.md with the rest of the Arabic)
  const PARTS = {
    'السَّلامُ عَلَيْكُم':     [['السَّلامُ','peace'],['عَلَيْكُم','(be) upon you']],
    'وَعَلَيْكُمُ السَّلام':   [['وَ','and'],['عَلَيْكُمُ','upon you'],['السَّلام','peace']],
    'كَيْفَ حالُكَ':          [['كَيْفَ','how'],['حالُكَ','your state (to a man)']],
    'كَيْفَ حالُكِ':          [['كَيْفَ','how'],['حالُكِ','your state (to a woman)']],
    'الحَمْدُ لِلَّهِ':        [['الحَمْدُ','praise'],['لِلَّهِ','(be) to Allah']],
    'أَهْلاً وَسَهْلاً':       [['أَهْلاً','(you’re among) family'],['وَسَهْلاً','and (on) easy ground']],
    'مَعَ السَّلامَةِ':        [['مَعَ','with'],['السَّلامَةِ','safety']],
    'ما اسْمُكَ؟':            [['ما','what (is)'],['اسْمُكَ','your name (to a man)']],
    'ما اسْمُكِ؟':            [['ما','what (is)'],['اسْمُكِ','your name (to a woman)']],
    'ما جِنْسِيَّتُكَ؟':       [['ما','what (is)'],['جِنْسِيَّتُكَ','your nationality (to a man)']],
    'ما جِنْسِيَّتُكِ؟':       [['ما','what (is)'],['جِنْسِيَّتُكِ','your nationality (to a woman)']],
    'مِنْ أَيْنَ؟':            [['مِنْ','from'],['أَيْنَ','where']],
    'ما شاءَ اللهُ':          [['ما','what'],['شاءَ','(has) willed'],['اللهُ','Allah']],
    'إِلى أَيْنَ':            [['إِلى','to'],['أَيْنَ','where']],
  };
  const parts = ar => PARTS[String(ar).trim()] || null;

  // Arabic letters only, without vowel marks; alif forms, ى and ة made the same
  const norm = t => String(t || '').replace(/[ً-ٰٟـ]/g, '').replace(/[أإآٱ]/g, 'ا')
    .replace(/ى/g, 'ي').replace(/ة/g, 'ه').replace(/[^ء-ي\s]/g, ' ');
  // the forms a word can be recognised by: without و/ف, بِ/لِ/كَ, ال, ‘my/your/his’ endings, plural and verb endings,
  // or a present-tense prefix (أَ/تَ/يَ/نَ)
  function stems(t){
    const out = new Set([t]);
    const a = t.replace(/^(و|ف)/, ''), b = a.replace(/^(ب|ل|ك)/, ''), c = b.replace(/^ال/, '');
    [a, b, c].forEach(x => [x, x.replace(/(ي|ك|ه|ها|نا|كم|هم|كن|هن|ني)$/, '')].forEach(y => {
      out.add(y); out.add(y.replace(/(ون|ين|ان|ات|وا|تم|ت|ه)$/, ''));
      if(y.length > 3){ const v = y.replace(/^[اتين]/, ''); out.add(v); out.add(v.replace(/(ون|ين|ان|وا)$/, '')); }
    }));
    return [...out].filter(x => x.length > 1);
  }
  // little words used everywhere, which the lessons use from the start
  const LITTLE = 'في من الي علي عن مع هل ما و يا هذا هذه انا انت هو هي نحن هم ان لا نعم';

  const byId = (() => { const m = new Map(); (typeof VOCAB !== 'undefined' ? VOCAB : []).forEach(w => m.set(w.id, w)); return m; })();
  function taught(unitN){
    const k = new Set(norm(LITTLE).split(/\s+/));
    const units = typeof PATH !== 'undefined' ? PATH : [];
    const add = ar => norm(ar).split(/[\s/]+/).filter(Boolean).forEach(t => stems(t).forEach(x => k.add(x)));
    for(const p of units){
      p.words.forEach(id => { const w = byId.get(id); if(w) add(w.ar); });
      // the examples on the unit's grammar cards are taught too (#163: عِنْدِي, كَبِيرَة)
      ((typeof EXTRA !== 'undefined' && EXTRA[p.n] && EXTRA[p.n].grammar) || []).forEach(g => add(g.ar));
      if(p.n === unitN) break;
    }
    return k;
  }
  function coverage(text, k){
    const t = norm(text).split(/\s+/).filter(Boolean);
    return t.length ? t.filter(x => stems(x).some(y => k.has(y))).length / t.length : 1;
  }

  window.RafiqTeach = { parts, taught, coverage };
})();
