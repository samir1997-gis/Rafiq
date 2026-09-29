/* progress.js — one progress store for all four sections, kept in Supabase.
   Loaded after auth.js, which provides `sb` and `currentUserId()`.

     await Progress.init()          pull this user's rows (once per page)
     Progress.get(id)               {box, due, seen} or null
     Progress.isDue(id)             due today or earlier
     Progress.grade(id, quality)    'again' | 'good' | 'easy' — schedules and saves
     Progress.dueIds(prefix)        ids due now, optionally 'v:' / 'd:' / 'f:' / 'c:'
     Progress.stats(prefix)         {due, learning, known, started}
     Progress.newPerDayKey          shared settings key

   Ids are namespaced so one table serves everything:
     v:412            vocabulary word
     d:03|cloze|2     sentence drill
     f:قال|past       verb pattern (verb + tense, not each pronoun)
     c:لِأَنَّ          connector

   Writes are batched and flushed shortly after you answer, so a fast session
   makes one request rather than twenty. A local mirror exists only so the app
   still works with no signal; Supabase is the source of truth on load.        */
(function(){
  const MIRROR='rafiq_progress_mirror';      // offline cache, not the master copy
  const QUEUE ='rafiq_progress_queue';       // writes that have not reached the server

  /* Reviews are scheduled by FSRS (fsrs.js, loaded before this file): it learns
     how well each item is remembered and picks the next gap from that. The
     per-item memory state lives in r.fsrs. `box` is still kept, derived from the
     gap, because pages read it: 0 new, 1 missed last time, 4+ known.
     The fixed gaps below are the fallback if fsrs.js is missing, and the seed
     for items reviewed before FSRS existed. */
  const GAPS={
    v:[0,1,2,4,8,16],
    d:[0,1,3,7,21,60],
    f:[0,1,3,7,21,60],
    c:[0,1,3,7,21,60]
  };
  const ns   = id => (id.split(':')[0] || 'd');
  const gaps = id => GAPS[ns(id)] || GAPS.d;

  const todayISO = () => new Date().toISOString().slice(0,10);
  const addDays  = n => { const d=new Date(); d.setDate(d.getDate()+n); return d.toISOString().slice(0,10); };

  let mem   = {};        // id -> {box, due, seen, at}  (at: when it was last saved)
  let dirty = new Set();
  let ready = false;
  let timer = null;
  let hasFsrsCol = true; // false until the fsrs column exists (supabase/sql/backend.sql)

  const readLS  = (k,d) => { try{ return JSON.parse(localStorage.getItem(k)) || d }catch(_){ return d } };
  const writeLS = (k,v) => { try{ localStorage.setItem(k, JSON.stringify(v)) }catch(_){} };

  async function init(){
    if(ready) return mem;
    mem = readLS(MIRROR, {});                       // show something immediately
    if(typeof sb!=='undefined' && sb){
      const uid = await currentUserId();
      if(uid){
        let { data, error } = await sb.from('item_progress')
          .select('item_id, box, due, seen, updated_at, fsrs').eq('user_id', uid);
        if(error){                                   // table without the fsrs column yet
          hasFsrsCol = false;
          ({ data, error } = await sb.from('item_progress').select('item_id, box, due, seen, updated_at').eq('user_id', uid));
        }
        if(error)                                    // older table without the timestamp
          ({ data, error } = await sb.from('item_progress').select('item_id, box, due, seen').eq('user_id', uid));
        if(error){ console.warn('[progress] load failed:', error.message); }
        else{
          mem = {};
          (data||[]).forEach(r => { mem[r.item_id] = {box:r.box, due:r.due, seen:r.seen, at:r.updated_at||null,
                                                      ...(r.fsrs ? {fsrs:r.fsrs} : {})}; });
          writeLS(MIRROR, mem);
        }
        await flushQueue(uid);                      // anything written while offline
        await migrateLegacy(uid);
      }
    }
    ready = true;
    return mem;
  }

  const get    = id => mem[id] || null;
  const isDue  = id => { const r=mem[id]; return !!(r && r.box>0 && r.due && r.due<=todayISO()); };
  const isNew  = id => !mem[id] || !mem[id].box;

  function dueIds(prefix){
    const t=todayISO();
    return Object.keys(mem).filter(id =>
      (!prefix || id.startsWith(prefix)) && mem[id].box>0 && mem[id].due && mem[id].due<=t);
  }
  function stats(prefix){
    const t=todayISO(); let due=0, learning=0, known=0, started=0;
    Object.keys(mem).forEach(id=>{
      if(prefix && !id.startsWith(prefix)) return;
      const r=mem[id]; if(!r || !r.box) return;
      started++;
      if(r.due && r.due<=t) due++;
      if(r.box>=4) known++; else learning++;
    });
    return {due, learning, known, started};
  }

  /* Exposure only — used by the self-study drills. Records that you have worked
     an item so the unit can show coverage, without putting it into any schedule.
     A row that has only ever been touched keeps box 0, so nothing reschedules. */
  function touch(id){
    const r = mem[id] || {box:0, due:null, seen:0};
    r.seen = (r.seen||0)+1;
    r.at = new Date().toISOString();
    mem[id]=r;
    writeLS(MIRROR, mem);
    dirty.add(id);
    schedule();
    return r;
  }
  /* Ids with any activity, optionally only those starting with a prefix. */
  const ids = prefix => Object.keys(mem).filter(id => (!prefix || id.startsWith(prefix)) && mem[id].seen>0);
  const seenCount = prefix =>
    Object.keys(mem).filter(id => (!prefix || id.startsWith(prefix)) && mem[id].seen>0).length;
  const hasSeen = id => !!(mem[id] && mem[id].seen>0);

  const F = window.FSRS;
  const scheduler = F && F.fsrs(F.generatorParameters({ enable_short_term:false }));   // whole days only
  const RATING = F && { again:F.Rating.Again, good:F.Rating.Good, easy:F.Rating.Easy };

  /* The saved FSRS state, or one seeded from the old box for items reviewed
     before FSRS: stability = that box's gap, average difficulty. */
  function cardOf(r, id){
    if(r.fsrs) return {
      due:new Date(r.due||Date.now()), stability:r.fsrs.s, difficulty:r.fsrs.d,
      elapsed_days:0, scheduled_days:0, learning_steps:0,
      reps:r.fsrs.n||0, lapses:r.fsrs.l||0, state:r.fsrs.st,
      last_review:r.fsrs.lr ? new Date(r.fsrs.lr) : undefined };
    if(!r.box) return F.createEmptyCard(new Date());
    const gap = gaps(id)[Math.min(r.box, gaps(id).length-1)] || 1;
    const due = r.due ? new Date(r.due) : new Date();
    return { due, stability:gap, difficulty:5, elapsed_days:0, scheduled_days:gap, learning_steps:0,
             reps:r.box, lapses:0, state:F.State.Review,
             last_review:new Date(due.getTime() - gap*86400000) };
  }
  const boxFor = days => days<=3 ? 2 : days<=7 ? 3 : days<=15 ? 4 : 5;

  function grade(id, quality){
    const g = gaps(id);
    const r = mem[id] || {box:0, due:null, seen:0};
    if(scheduler){
      const now  = new Date();
      const card = scheduler.next(cardOf(r, id), now, RATING[quality] || RATING.good).card;
      const days = Math.max(1, Math.round((card.due - now) / 86400000));
      r.box  = quality==='again' ? 1 : boxFor(days);
      r.due  = addDays(days);
      r.fsrs = { s:+card.stability.toFixed(3), d:+card.difficulty.toFixed(3), st:card.state,
                 n:card.reps, l:card.lapses, lr:now.toISOString() };
    } else {
      if(quality==='again')      r.box = 1;                         // back to the start, still scheduled
      else if(quality==='easy')  r.box = Math.min(g.length-1, Math.max(1,r.box)+2);
      else                       r.box = Math.min(g.length-1, Math.max(1,r.box)+1);
      r.due  = addDays(g[r.box]);
    }
    r.seen = (r.seen||0)+1;
    r.at   = new Date().toISOString();
    mem[id]=r;
    writeLS(MIRROR, mem);
    dirty.add(id);
    schedule();
    return r;
  }

  function schedule(){
    if(timer) clearTimeout(timer);
    timer = setTimeout(()=>{ flush(); }, 900);      // batch a burst of answers
  }

  async function flush(){
    if(!dirty.size) return;
    const ids=[...dirty]; dirty.clear();
    const rows = ids.map(id => ({
      item_id:id, box:mem[id].box, due:mem[id].due, seen:mem[id].seen,
      updated_at:new Date().toISOString(),
      ...(mem[id].fsrs ? {fsrs:mem[id].fsrs} : {})
    }));
    if(typeof sb==='undefined' || !sb){ queueRows(rows); return; }
    const uid = await currentUserId();
    if(!uid){ queueRows(rows); return; }
    const error = await upsert(uid, rows);
    if(error){ console.warn('[progress] save failed:', error.message); queueRows(rows); }
  }

  /* Save rows; leaves out the fsrs field while the column doesn't exist, so
     answers still save (the state is kept in the local mirror meanwhile). */
  async function upsert(uid, rows){
    const send = rs => sb.from('item_progress')
      .upsert(rs.map(r=>({user_id:uid, ...r})), { onConflict:'user_id,item_id' });
    if(hasFsrsCol){
      const { error } = await send(rows);
      if(!error || !/fsrs/.test(error.message||'')) return error;
      hasFsrsCol = false;
    }
    const { error } = await send(rows.map(({fsrs, ...r}) => r));
    return error;
  }

  function queueRows(rows){
    const q = readLS(QUEUE, []);
    writeLS(QUEUE, q.concat(rows));
  }
  async function flushQueue(uid){
    const q = readLS(QUEUE, []);
    if(!q.length || !sb || !uid) return;
    const error = await upsert(uid, q);
    if(!error) writeLS(QUEUE, []);
  }

  /* One-time import of the two old localStorage stores, per account. */
  async function migrateLegacy(uid){
    if(!sb || !uid) return;
    let done=false;
    try{
      const { data } = await sb.from('settings').select('migrated_v2').eq('user_id',uid).maybeSingle();
      done = !!(data && data.migrated_v2);
    }catch(_){}
    if(done) return;

    const rows=[];
    const vp = readLS('bay_vocab_progress_v1', null);
    if(vp) Object.keys(vp).forEach(wid=>{
      const r=vp[wid];
      if(!r || !r.box) return;                        // never-started words add nothing
      rows.push({item_id:'v:'+wid, box:r.box, seen:r.seen||1,
                 due: r.due==null ? null : new Date(r.due*86400000).toISOString().slice(0,10)});
    });
    const dp = readLS('bay_drills_progress_v1', null);
    if(dp && dp.items) Object.keys(dp.items).forEach(k=>{
      const r=dp.items[k];
      if(!r || !r.box) return;
      rows.push({item_id:'d:'+k, box:r.box, due:r.due||null, seen:r.seen||1});
    });

    if(rows.length){
      const { error } = await sb.from('item_progress')
        .upsert(rows.map(r=>({user_id:uid, ...r, updated_at:new Date().toISOString()})),
                { onConflict:'user_id,item_id' });
      if(error){ console.warn('[progress] migration failed:', error.message); return; }
      rows.forEach(r=>{ mem[r.item_id]={box:r.box, due:r.due, seen:r.seen}; });
      writeLS(MIRROR, mem);
      console.log('[progress] imported '+rows.length+' items from the old stores');
    }
    try{
      await sb.from('settings').upsert({user_id:uid, migrated_v2:true,
        updated_at:new Date().toISOString()}, {onConflict:'user_id'});
    }catch(_){}
  }

  // don't lose the last few answers when the page goes away
  window.addEventListener('pagehide', ()=>{ flush(); });
  document.addEventListener('visibilitychange', ()=>{ if(document.hidden) flush(); });

  window.Progress = { init, get, isDue, isNew, dueIds, stats, grade, touch, hasSeen, seenCount, ids,
                      flush, todayISO, ns, GAPS };
})();
