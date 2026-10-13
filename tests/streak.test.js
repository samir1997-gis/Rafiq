/* Node check of the streak (path.js, #256): a day counts when the daily goal is met,
   one missed day is covered by a streak freeze, and a used freeze comes back after
   7 goal days in a row. Days before 14 Oct 2026 count with any finished step.
   Run: node tests/streak.test.js */
const fs = require('fs'), vm = require('vm'), assert = require('assert');
const NOW = new Date('2026-11-20T12:00:00Z').getTime();
class FakeDate extends Date { constructor(...a){ super(...(a.length ? a : [NOW])); } static now(){ return NOW; } }
const day = k => new Date(NOW - k * 86400000).toISOString().slice(0, 10);   // k days ago

/* steps[k] = steps finished k days ago (0 = today); goal 2 a day */
async function load(steps, extra = {}){
  const mirror = {};
  steps.forEach((n, k) => { if(n) mirror['s:' + day(k)] = { box: 0, due: null, seen: n }; });
  Object.entries(extra).forEach(([d, n]) => { mirror['s:' + d] = { box: 0, due: null, seen: n }; });
  const store = { rafiq_progress_mirror: JSON.stringify(mirror), rafiq_goal: '2' };
  const ctx = { console, Date: FakeDate, Math, JSON, Set, setTimeout: () => 0, clearTimeout(){},
    localStorage: { getItem: k => store[k] ?? null, setItem: (k, v) => { store[k] = v; } },
    addEventListener(){}, document: { addEventListener(){} }, PATH: [], DATA: [], VOCAB: [], PIC: {} };
  ctx.window = ctx; ctx.globalThis = ctx; ctx.self = ctx;
  vm.createContext(ctx);
  vm.runInContext(fs.readFileSync('progress.js', 'utf8'), ctx);
  await ctx.Progress.init();
  vm.runInContext(fs.readFileSync('path.js', 'utf8'), ctx);
  return ctx.RafiqPath;
}

(async () => {
  let R = await load([2, 2, 2]);                       // goal met today and the two days before
  assert.equal(R.streak(), 3);

  R = await load([1, 2, 2]);                           // today started but not met: counts to yesterday
  assert.equal(R.streak(), 2);

  R = await load([0, 1, 2, 2]);                        // yesterday short of the goal: the freeze covers it
  let s = R.streakState();
  assert.equal(s.days, 2); assert.equal(s.freezes, 0); assert.equal(s.frozen, day(1)); assert.equal(s.earn, 7);

  R = await load([0, 0, 0, 2, 2]);                     // two missed days in a row: the second breaks it
  assert.equal(R.streak(), 0);

  R = await load([2, 0, 2, 2]);                        // a covered day doesn't add to the count
  assert.equal(R.streak(), 3);

  R = await load([2, 0, 2, 0, 2]);                     // a second miss before the freeze is earned back breaks it:
  assert.equal(R.streak(), 1);                         // the streak starts again today

  // the freeze comes back after 7 goal days in a row, so a later miss is covered again
  R = await load([2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 2, 0, 2]);
  s = R.streakState();
  assert.equal(s.days, 16); assert.equal(s.freezes, 1, 'earned back');
  assert.equal(R.bestStreak(), 16);

  // before 14 Oct any finished step counted, so old streaks don't drop
  R = await load([2], { '2026-10-11': 1, '2026-10-12': 1, '2026-10-13': 1 });
  assert.equal(R.bestStreak(), 3);

  console.log('streak: all passed');
})();
