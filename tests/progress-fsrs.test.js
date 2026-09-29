/* Node check of progress.js scheduling (FSRS + the box every page reads).
   Run: node tests/progress-fsrs.test.js */
const fs = require('fs'), vm = require('vm'), assert = require('assert');
function load(withFsrs, mirror){
  const store = mirror ? { rafiq_progress_mirror: JSON.stringify(mirror) } : {};
  const ctx = { console, Date, Math, JSON, setTimeout: () => 0, clearTimeout(){},
    localStorage: { getItem: k => store[k] ?? null, setItem: (k, v) => { store[k] = v; } },
    addEventListener(){}, document: { addEventListener(){} } };
  ctx.window = ctx; ctx.globalThis = ctx; ctx.self = ctx;
  vm.createContext(ctx);
  if(withFsrs) vm.runInContext(fs.readFileSync('fsrs.js', 'utf8'), ctx);
  vm.runInContext(fs.readFileSync('progress.js', 'utf8'), ctx);
  return ctx.Progress;
}
const days = iso => Math.round((new Date(iso) - new Date(new Date().toISOString().slice(0,10))) / 86400000);

let P = load(true);
let r = P.grade('v:1', 'good');
assert.equal(r.box, 2); assert.ok(days(r.due) >= 2 && days(r.due) <= 4, 'first good ~3 days');
assert.ok(r.fsrs && r.fsrs.s > 0 && r.fsrs.d > 0, 'fsrs state saved');
r = P.grade('v:1', 'again');
assert.equal(r.box, 1, 'missed = box 1'); assert.equal(days(r.due), 1);
r = P.grade('v:2', 'easy');
assert.ok(r.box >= 4, 'easy on a new word jumps to known');

// an item reviewed before FSRS (box 4, due today, no fsrs state) is seeded from its box
(async () => {
const today = new Date().toISOString().slice(0,10);
const legacy = load(true, { 'v:9': { box: 4, due: today, seen: 4 } });
await legacy.init();
assert.ok(legacy.isDue('v:9'));
const lr = legacy.grade('v:9', 'good');
assert.ok(days(lr.due) > 8, 'a remembered known word gets a longer gap, got ' + days(lr.due));
assert.ok(lr.box >= 4 && lr.fsrs, 'still known, now with fsrs state');

// without fsrs.js the old fixed boxes still work
P = load(false);
r = P.grade('d:1', 'good'); assert.equal(r.box, 2); assert.equal(days(r.due), 3);
assert.equal(r.fsrs, undefined);
console.log('progress-fsrs: all passed');
})().catch(e => { console.error(e); process.exit(1); });
