/* path.js — the learning path: which step comes next, what's unlocked, streaks.
   Needs path-data.js (PATH, PIC), drills-data.js (DATA), vocab-data.js (VOCAB)
   and progress.js (Progress, already init()ed).

   A unit is a short run of steps, each about 5–10 minutes:
     meet 10 words → hear the conversation → how it works (grammar) →
     meet the next 10 → practise → … → have the conversation → say it yourself →
     the unit test (pass it to open the next unit)
   Steps are stored in the shared progress store as 'p:<unit>|<step>', so the
   path follows the learner across devices. A unit skipped by the placement
   check is stored as 'p:<unit>|placed'. Each day with any finished step or
   session is 's:<yyyy-mm-dd>', which gives the streak and the daily goal. */
(function(){
  const BATCH = 10;          // words met per step
  // units that teach before they ask (#156): words first, practice only from what's been taught
  const TEACH = new Set(['01', '02', '03']);
  // steps (or sessions) a day to meet the daily goal; set at sign-up from minutes a day
  const GOAL  = (() => { try{ const g=parseInt(localStorage.getItem('rafiq_goal'),10); return g>0 ? g : 2; }catch(_){ return 2; } })();

  /* Unit 0, the reading starter, comes first for everyone; readers skip it
     with one tap or through placement. It exists only if alphabet-data.js is
     loaded on the page. */
  const ALPHA = typeof ALPHABET_GROUPS !== 'undefined'
    ? [{n:'00', ar:'الْحُرُوفُ', en:'Reading Arabic', words:[], alpha:true}] : [];
  const UNITS = ALPHA.concat(PATH);
  const units = () => UNITS;
  const unitData = n => DATA.find(u => u.n === n);
  /* Announced, not built yet: shown after the last unit on Home and on the
     pricing page. Update as units ship (and move them into the path). */
  const COMING = [
    {ar:'السَّفَرُ',              en:'Travel & directions',    d:'Airports, hotels, asking the way'},
    {ar:'الصِّحَّةُ',              en:'Health & the body',      d:'At the doctor, how you feel'},
    {ar:'رَمَضانُ وَالْعِيدُ',      en:'Ramadan & Eid',          d:'Fasting, iftar, Eid visits'},
    {ar:'الْحِكاياتُ',             en:'Telling stories',        d:'What happened — the past tense in use'},
  ];
  const wordById = (() => { const m = new Map(); VOCAB.forEach(w => m.set(w.id, w)); return id => m.get(id); })();

  function steps(p){
    if(p.alpha) return ALPHABET_GROUPS.map((g,i) => ({key:'letters'+(i+1), kind:'letters', group:i,
        title:g.title.replace(/^Letters \d+: /,'Letters: '), mins:5}))
      .concat([{key:'vowels', kind:'vowels', title:'The vowel marks', mins:5},
               {key:'hear', kind:'hearing', title:'Listening test', mins:6}]);
    const nb = Math.ceil(p.words.length / BATCH), out = [];
    // "Meet 10 new words & phrases": chosen with TypeSafe (tools/typesafe-exp/step_label.py, #116);
    // "New words 4 of 4" read like four words. The count and "& phrases" follow the set itself.
    const words = i => {
      const set = p.words.slice(i*BATCH, (i+1)*BATCH).map(wordById).filter(Boolean);
      const n = set.length, phrases = set.some(w => /\s/.test(w.ar.trim()));
      return {key:'words'+(i+1), kind:'words', batch:i, mins: 5,
        title: `Meet ${n} new ${n === 1 ? (phrases ? 'phrase' : 'word') : (phrases ? 'words & phrases' : 'words')}`};
    };
    const listen   = {key:'listen',   kind:'listen',   title:'Hear the conversation', mins:4};
    const grammar  = {key:'grammar',  kind:'grammar',  title:'How it works',          mins:5};
    const practise = {key:'practise', kind:'practise', title:'Practise',              mins:8};
    if(TEACH.has(p.n)){
      /* Teach first (#156): words before sentences. Two lessons of words, then how it
         works, the rest of the words, practice made from what's been taught, and the
         conversation last, when most of its words are known. The step keys are the
         same as before, so progress already saved still counts. */
      out.push(words(0));
      if(nb>1) out.push(words(1));
      out.push(grammar);
      for(let i=2;i<nb;i++) out.push(words(i));
      out.push(practise, listen);
    } else {
      out.push(words(0), listen, grammar);
      for(let i=1;i<nb;i++){
        out.push(words(i));
        if(i===1) out.push(practise);
      }
      if(nb<2) out.push(practise);
    }
    out.push({key:'chat',     kind:'chat',     title:'Have the conversation', mins:6});
    out.push({key:'speak',    kind:'speak',    title:'Say it yourself',       mins:6});
    // the unit test (#158): the next unit opens once it's passed
    out.push({key:'test',     kind:'test',     title:'Unit test',             mins:6});
    return out;
  }
  const sid = (n, key) => 'p:' + n + '|' + key;
  const stepDone = (n, key) => Progress.hasSeen(sid(n, key));
  const placed = n => Progress.hasSeen(sid(n, 'placed'));
  /* The listening test was added after some learners had finished the reading
     starter and moved on to unit 1; it stays open to them but doesn't pull them back. */
  const movedOn = () => UNITS.some(u => !u.alpha && (placed(u.n) || steps(u).some(s => stepDone(u.n, s.key))));
  /* The same goes for words added to a unit after it was written (lateFrom in
     path-data.js, e.g. the missing days of the week): their step stays open to
     learners who are already past the unit, but doesn't pull them back. */
  const late = (p, s) => p.lateFrom != null && s.kind === 'words' && s.batch * BATCH >= p.lateFrom;
  const movedPast = p => { const i = UNITS.indexOf(p);
    return UNITS.slice(i + 1).some(u => placed(u.n) || steps(u).some(s => stepDone(u.n, s.key))); };
  // the unit test came later too (#158): learners already past a unit aren't sent back for it
  function unitDone(p){
    return placed(p.n) || steps(p).every(s => stepDone(p.n, s.key)
      || (p.alpha && s.key === 'hear' && movedOn()) || ((late(p, s) || s.kind === 'test') && movedPast(p)));
  }
  // a finished unit with a late step still to do (Home can point it out)
  const lateLeft = p => !placed(p.n) && steps(p).some(s => late(p, s) && !stepDone(p.n, s.key));

  /* The unit you're on: the first one not finished. Everything before it is
     done; everything after is "coming up" but still openable. */
  function currentIndex(){
    const i = UNITS.findIndex(p => !unitDone(p));
    return i < 0 ? UNITS.length - 1 : i;
  }
  function next(){
    const i = currentIndex(), p = UNITS[i];
    const s = steps(p).find(s => !stepDone(p.n, s.key)) || null;
    return {unit:p, index:i, step:s, finishedAll: i === UNITS.length-1 && unitDone(p)};
  }
  /* Locks: a unit opens once every unit before it is done (or skipped by
     placement); inside the current unit, steps open in order. Anything
     finished can always be revisited. The Practise area is never locked. */
  const unitIndex = n => UNITS.findIndex(p => p.n === n);
  const unitOpen = n => { const i = unitIndex(n); return i >= 0 && i <= currentIndex(); };
  function stepOpen(n, key){
    const i = unitIndex(n); if(i < 0) return false;
    const cur = currentIndex();
    if(i < cur) return true;
    if(i > cur) return false;
    const p = UNITS[i], first = steps(p).find(s => !stepDone(p.n, s.key));
    return stepDone(n, key) || (first && first.key === key);
  }
  // units whose material sessions may use (the reading starter has none)
  const reached = () => UNITS.slice(0, currentIndex() + 1).filter(p => !p.alpha);

  /* What review may draw on: only what the learner has actually done on the
     path — words they've met in lessons (from units reached) and sentence
     exercises they've already practised there. Nothing from the Practise area
     (verbs, joining words) and nothing they haven't seen yet. */
  function reviewScope(){
    const units = reached();
    return { units: new Set(units.map(p => p.n)), wordIds: metWords() };
  }
  /* Words met on the path: every word in a finished "New words" step. Words
     practised only in the Practise area don't count, nor do units skipped by
     placement. */
  function metWords(){
    const out = new Set();
    UNITS.forEach(p => { if(p.alpha) return;
      steps(p).forEach(s => { if(s.kind==='words' && stepDone(p.n, s.key)) wordsOf(p, s.batch).forEach(w => out.add(w.id)); }); });
    return out;
  }
  const inScope = (id, sc) => id.startsWith('v:') ? sc.wordIds.has(+id.slice(2))
                            : id.startsWith('d:') ? sc.units.has(id.slice(2, 4)) : false;
  /* Items in scope that are due for review today (for the Home nudge). */
  function reviewDue(){ const sc = reviewScope(); return Progress.dueIds().filter(id => inScope(id, sc)).length; }
  /* Anything learned at all (so review isn't offered before the first lesson). */
  function hasLearned(){ const sc = reviewScope();
    return VOCAB.some(w => sc.wordIds.has(w.id) && !Progress.isNew('v:' + w.id)); }

  function complete(n, key){
    // a step keeps the date it was first finished; revisiting it only counts the day
    if(!stepDone(n, key)){ Progress.touch(sid(n, key)); if(n !== '00' && key !== 'test') lessonsSinceRecap(1); }
    markDay();
  }
  /* Recaps (#158): review that grows with progress. Every RECAP lessons finished, the
     next lesson starts with a short recap of words from earlier lessons, so two units
     in a day bring back far more than one. Kept on the device. */
  const RECAP = 2;
  function lessonsSinceRecap(add){
    let n = 0; try{ n = parseInt(localStorage.getItem('rafiq_recap'), 10) || 0; }catch(_){}
    if(add != null){ n = add ? n + add : 0; try{ localStorage.setItem('rafiq_recap', String(n)); }catch(_){} }
    return n;
  }
  const recapDue = () => lessonsSinceRecap() >= RECAP;
  const recapDone = () => lessonsSinceRecap(0);
  function place(uptoIndex){          // placement: skip units before this one (index into units())
    UNITS.slice(0, uptoIndex).forEach(p => { if(!unitDone(p)) Progress.touch(sid(p.n, 'placed')); });
  }
  const skipReading = () => { if(ALPHA.length && !unitDone(ALPHA[0])) Progress.touch(sid('00','placed')); };

  const iso = d => d.toISOString().slice(0,10);
  function markDay(){ Progress.touch('s:' + iso(new Date())); }
  // one 'w:<date>' row per day; its count is the number of new words met that day
  function wordMet(){ Progress.touch('w:' + iso(new Date())); }
  /* The last 7 days: days active, steps and sessions finished, new words met. */
  function week(){
    let days=0, steps=0, words=0;
    for(let k=0;k<7;k++){
      const d=new Date(); d.setDate(d.getDate()-k); const day=iso(d);
      const s=Progress.get('s:'+day), w=Progress.get('w:'+day);
      if(s && s.seen){ days++; steps+=s.seen; }
      if(w && w.seen) words+=w.seen;
    }
    return {days, steps, words};
  }
  /* Daily counts. Two sources, and each day takes the larger:
     - counters, one row per day: 'w:<date>' new words met, 'e:<date>'
       sentence exercises done ('s:<date>' is steps and sessions);
     - when things were saved: a finished "New words" step adds its words on
       the day it was finished, and a sentence exercise counts on the day it
       was last practised. This covers everything done before the counters
       existed. */
  const dayKey = k => { const d=new Date(); d.setDate(d.getDate()-k); return iso(d); };
  const countOn = (pre, day) => { const r=Progress.get(pre+day); return r && r.seen || 0; };
  const dayOf = at => at ? iso(new Date(at)) : null;
  function savedByDay(){
    const words={}, sentences={};
    UNITS.forEach(p => { if(p.alpha) return;
      steps(p).forEach(s => { if(s.kind!=='words') return;
        const r=Progress.get(sid(p.n, s.key)), d=r && r.seen && dayOf(r.at);
        if(d) words[d]=(words[d]||0)+wordsOf(p, s.batch).length; }); });
    Progress.ids('d:').forEach(id => { const d=dayOf(Progress.get(id).at); if(d) sentences[d]=(sentences[d]||0)+1; });
    return {words, sentences};
  }
  const wordsOn = (day, sv) => Math.max(countOn('w:',day), sv.words[day]||0);
  const sentencesOn = (day, sv) => Math.max(countOn('e:',day), sv.sentences[day]||0);
  function sentenceDone(){ Progress.touch('e:' + iso(new Date())); }
  /* Totals for the last `days` days (1 = today): words, sentences, steps, days active. */
  function period(days){
    const sv=savedByDay(), t={words:0, sentences:0, steps:0, days:0};
    for(let k=0;k<days;k++){ const d=dayKey(k);
      t.words+=wordsOn(d,sv); t.sentences+=sentencesOn(d,sv);
      const st=countOn('s:',d); t.steps+=st; if(st) t.days++; }
    return t;
  }
  /* New words per day for the last `days` days, oldest first. */
  const wordsByDay = days => { const sv=savedByDay();
    return Array.from({length:days}, (_,i) => { const d=dayKey(days-1-i); return {day:d, words:wordsOn(d,sv), active:countOn('s:',d)>0}; }); };
  /* Today's new words against your usual: the median of the days in the last
     four weeks you met any (needs 3 such days), and your best day this year. */
  function wordsReport(){
    const sv=savedByDay(), today=wordsOn(dayKey(0),sv);
    const recent=[]; for(let k=1;k<=28;k++){ const n=wordsOn(dayKey(k),sv); if(n) recent.push(n); }
    recent.sort((a,b)=>a-b);
    const usual = recent.length>=3 ? recent[Math.floor(recent.length/2)] : null;
    let best=0; for(let k=1;k<=365;k++) best=Math.max(best, wordsOn(dayKey(k),sv));
    return { today, usual, best, aboveUsual: usual!=null && today>usual, record: best>=10 && today>best };
  }
  function bestStreak(){
    let best=0, run=0;
    for(let k=400;k>=0;k--){ if(countOn('s:',dayKey(k))){ run++; best=Math.max(best,run); } else if(k>0) run=0; }
    return Math.max(best, streak());
  }
  function doneToday(){ const r = Progress.get('s:' + iso(new Date())); return r ? r.seen : 0; }
  /* Streak goals. Each says what the research behind daily, spaced practice
     suggests is happening by then — no invented percentages. Sources: the
     spacing effect (Cepeda et al., 2006, review of 254 studies), the testing
     effect (Roediger & Karpicke, 2006), habit formation (Lally et al., 2010). */
  const STREAK_GOALS = [
    {days:3,   why:'Your first words come back for review. Recalling a word after a gap makes it fade more slowly — the spacing effect, one of the most replicated findings in memory research.'},
    {days:7,   why:'The words from your first day will have come back twice. Spreading practice over days beats cramming the same time into one sitting.'},
    {days:14,  why:'Pulling a word from memory strengthens it more than re-reading it — the testing effect. Two weeks of daily recall adds up.'},
    {days:30,  why:'Your earliest words are on long review gaps by now — a sign they\'re settling into long-term memory.'},
    {days:66,  why:'66 days was the average time for a daily habit to start feeling automatic in a well-known habit study (Lally et al., 2010).'},
    {days:100, why:'A hundred days of Arabic. By now it\'s simply part of your day.'},
  ];
  /* {next, left, from, why} for the goal you're working towards, and the goal
     reached today if the streak has just hit one. */
  function streakGoal(n){
    const next = STREAK_GOALS.find(g => g.days > n) || null;
    const prev = [...STREAK_GOALS].reverse().find(g => g.days <= n);
    return { next, left: next ? next.days - n : 0, from: prev ? prev.days : 0,
             reached: STREAK_GOALS.find(g => g.days === n) || null };
  }
  function streak(){
    const d = new Date(); let n = 0;
    if(!Progress.hasSeen('s:' + iso(d))) d.setDate(d.getDate()-1);   // today not done yet: count from yesterday
    while(Progress.hasSeen('s:' + iso(d))){ n++; d.setDate(d.getDate()-1); }
    return n;
  }

  /* How "Say this in Arabic" is answered: word tiles in units 1–3, tiles with
     a piece or two that don't belong in units 4–6, typing from unit 7. Per
     learner, per unit: 5 tile answers right first time in a row moves that unit
     on a stage; typing that goes badly (under 5 of the last 10 right) brings it
     back a stage. Settings can fix it to tiles or typing. Kept on the device. */
  const ANSWER_STYLES=['tiles','mixed','type'];
  const answerPref = () => { try{ const v=localStorage.getItem('rafiq_answer_style'); return v==='tiles'||v==='type' ? v : 'auto'; }catch(_){ return 'auto'; } };
  const answerState = () => { try{ return JSON.parse(localStorage.getItem('rafiq_answer'))||{}; }catch(_){ return {}; } };
  const saveAnswerState = s => { try{ localStorage.setItem('rafiq_answer', JSON.stringify(s)); }catch(_){} };
  function answerStyle(n){
    const pref=answerPref();
    if(pref!=='auto') return pref;
    const u=+n, base = u<=3 ? 0 : u<=6 ? 1 : 2, shift=(answerState().shift||{})[n]||0;
    return ANSWER_STYLES[Math.max(0, Math.min(2, base+shift))];
  }
  /* After each "Say this in Arabic": style is how it was answered, ok whether
     it was right first time. Returns 'up' or 'down' when the unit's stage moves. */
  function answered(n, style, ok){
    const s=answerState(); s.shift=s.shift||{}; s.run=s.run||{}; s.typed=s.typed||{};
    let moved=null;
    if(style==='type'){
      const t=(s.typed[n]||[]).concat(ok?1:0).slice(-10); s.typed[n]=t;
      if(t.length===10 && t.reduce((a,b)=>a+b,0)<5 && answerStyle(n)==='type'){ s.shift[n]=(s.shift[n]||0)-1; s.typed[n]=[]; moved='down'; }
    } else {
      s.run[n] = ok ? (s.run[n]||0)+1 : 0;
      if(s.run[n]>=5 && answerStyle(n)!=='type'){ s.shift[n]=(s.shift[n]||0)+1; s.run[n]=0; moved='up'; }
    }
    saveAnswerState(s);
    return answerPref()==='auto' ? moved : null;
  }

  function wordsOf(p, batch){
    const ids = batch == null ? p.words : p.words.slice(batch*BATCH, (batch+1)*BATCH);
    return ids.map(wordById).filter(Boolean);
  }

  window.RafiqPath = { recapDue, recapDone, teaches: n => TEACH.has(n), lateLeft, reviewScope, metWords, sentenceDone, period, wordsByDay, wordsReport, bestStreak, reviewDue, hasLearned, COMING, STREAK_GOALS, streakGoal, BATCH, GOAL, units, skipReading, unitOpen, stepOpen, steps, stepDone, unitDone, placed, currentIndex, next, reached,
                       complete, place, markDay, wordMet, week, doneToday, streak, wordsOf, unitData, wordById,
                       answerStyle, answered, answerPref };
})();
