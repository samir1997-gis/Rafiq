#!/usr/bin/env node
/* Builds path-data.js — which words each unit of the learning path teaches.
   Run:  node tools/build-path.js   (after changing vocab-data.js or drills-data.js)

   A word belongs to the first unit whose own conversations and drills use it.
   Units are then topped up from the matching vocabulary topic, up to CAP words,
   so no lesson asks for too much at once. Everything left over stays in the
   Words section as extra practice, outside the path.

   LATE words were added to a unit after it was full and after learners had
   finished it: they go after the unit's CAP words, in their own "New words"
   step, and the unit records where they start (lateFrom) so path.js doesn't
   pull back learners who have already moved past it.

   Pictures (PIC) are kept from the previous path-data.js; they are chosen by
   tools/typesafe-exp/pick_pictures.py.                                        */
const fs = require('fs'), path = require('path'), root = path.join(__dirname, '..');
const CAP = 40;
// vocabulary topic → the unit it belongs with (topics not listed stay extra)
const TOPIC_UNIT = { '01':'01', '08':'02', '10':'03', '06':'04', '09':'05', '07':'06',
                     '14':'07', '15':'09', '12':'10', '13':'11' };
// unit → word ids added late (issue #61: the days and numbers missing from the lessons)
const LATE = { '03': [780, 781, 782, 35, 783] };        // Sunday, Monday, Wednesday, two, six
const lateIds = new Set(Object.values(LATE).flat());
// words spelt like another word with a different meaning: placed by their topic, not by spelling, so
// ما 'what' in unit 1 doesn't bring in ما 'not (past)', nor لا 'no' the لا of 'not' and 'don't'
const BY_TOPIC_ONLY = new Set([127, 163, 213]);
// words taught in the basics section (#168, basics-data.js), before unit 1: never placed in a unit
const BASICS_ONLY = new Set([784, 785, 786, 787, 788, 789, 790, 791, 792, 793, 794]);   // اسْم name, لُغَة language; #277: hello … word
// unit → words it starts with (#156, teach first): unit 1 opens with ten single words, before the
// greeting phrases, so its first lesson is words a beginner can hold on to (I, you, he, she, this…)
const FIRST = { '01': [15, 16, 17, 18, 19, 20, 21, 26, 30, 28] };      // أَنا أَنْتَ أَنْتِ هُوَ هِيَ هَذا هَذِهِ صَدِيق مُدَرِّس طالِبَة
/* Units whose words are listed here in full, in the order they're taught (lessons of 5), instead of being worked out
   from their sentences. A listed word is placed before anything else, so it must not be one an earlier unit teaches.
   04: listed to keep the words its learners already have. Unit 03's later exercises use لَيْسَ (418), so the rule below
       would now drop it from unit 04 and bring in فُلوس (695) in its place.
   13 to 16 (#344): written after the path, each with its own 40 words. */
const LISTED = {
  '04': [132, 142, 137, 138, 139, 152, 217, 762, 268, 293, 724, 175, 148, 181, 551, 140, 416, 540, 144, 143, 235, 146, 147, 292, 336, 679, 141, 210, 418, 496, 155, 207, 208, 211, 528, 727, 765, 243, 523, 637],
  '13': [795, 718, 796, 797, 798, 522, 799, 800, 747, 801, 802, 803, 804, 805, 806, 636, 177, 807, 158, 244, 808, 809, 635, 810, 811, 812, 585, 813, 728, 814, 603, 815, 816, 817, 533, 407, 587, 53, 713, 818],
  '14': [819, 820, 508, 821, 822, 519, 823, 824, 563, 825, 641, 826, 543, 827, 548, 752, 652, 564, 828, 829, 830, 831, 832, 561, 574, 577, 570, 573, 565, 578, 833, 768, 296, 834, 835, 579, 553, 130, 560, 836],
  '15': [837, 838, 839, 840, 618, 841, 842, 238, 364, 843, 844, 845, 846, 770, 847, 848, 599, 232, 391, 849, 402, 470, 476, 490, 477, 483, 488, 850, 851, 72, 475, 852, 634, 466, 853, 382, 354, 615, 504, 467],
  '16': [854, 855, 856, 720, 629, 614, 857, 858, 357, 601, 859, 860, 861, 862, 863, 864, 107, 865, 866, 486, 867, 868, 869, 870, 871, 204, 227, 281, 485, 228, 645, 697, 746, 872, 873, 874, 875, 136, 127, 572],
};

function load(file, names) {
  let src = fs.readFileSync(path.join(root, file), 'utf8');
  names.forEach(n => { src = src.replace(new RegExp('const\\s+' + n + '\\s*=', 'g'), 'globalThis.' + n + '='); });
  eval(src);
}
load('drills-data.js', ['DATA', 'EXTRA']);
load('vocab-data.js', ['VOCAB']);
Object.keys(EXTRA).forEach(k => { const u = DATA.find(x => x.n === k); if (u) Object.assign(u, EXTRA[k]); });

const norm = t => (t || '').replace(/[ً-ْٰـ]/g, '').replace(/[أإآٱ]/g, 'ا')
  .replace(/ى/g, 'ي').replace(/ة/g, 'ه').replace(/[^ء-ي\s]/g, ' ').replace(/\s+/g, ' ').trim();
const bare = w => w.replace(/^(و|ف|ب|ل|ك)?(ال)?/, '');          // drop clitics and the article
function unitWords(u) {
  const out = [];
  const walk = x => typeof x === 'string' ? out.push(x) : Array.isArray(x) ? x.forEach(walk)
                  : (x && typeof x === 'object') ? Object.values(x).forEach(walk) : 0;
  [u.convos, u.ladders, u.subs, u.builds, u.transforms, u.cloze, u.fix, u.prompts].forEach(walk);
  return new Set(norm(out.join(' ')).split(' ').map(bare));
}
const used = DATA.map(unitWords);
// a verb entry "ذَهَبَ / يَذْهَبُ" matches if either form is used
const forms = w => w.ar.split('/').map(f => norm(f).split(' ').map(bare).filter(Boolean)).filter(f => f.length);

const byUnit = DATA.map(() => []), placed = new Set();
Object.entries(LISTED).forEach(([n, ids]) => {
  const i = DATA.findIndex(x => x.n === n);
  if (i < 0) return;
  ids.forEach(id => {
    if (!VOCAB.some(w => w.id === id) || placed.has(id)) throw new Error(`unit ${n}: word ${id} is not in the word list, or is listed twice`);
    byUnit[i].push(id); placed.add(id);
  });
});
VOCAB.forEach(w => {
  if (placed.has(w.id) || lateIds.has(w.id) || BY_TOPIC_ONLY.has(w.id) || BASICS_ONLY.has(w.id)) return;
  const i = used.findIndex(set => forms(w).some(f => f.every(t => set.has(t))));
  if (i >= 0 && byUnit[i].length < CAP) { byUnit[i].push(w.id); placed.add(w.id); }
});
VOCAB.forEach(w => {
  if (placed.has(w.id) || lateIds.has(w.id) || BASICS_ONLY.has(w.id)) return;
  const u = TOPIC_UNIT[w.unit.slice(0, 2)], i = DATA.findIndex(x => x.n === u);
  if (i >= 0 && byUnit[i].length < CAP) { byUnit[i].push(w.id); placed.add(w.id); }
});

let PIC = {};
try { load('path-data.js', ['PATH', 'PIC']); PIC = globalThis.PIC || {}; } catch (_) {}

const PATH = DATA.map((u, i) => {
  const first = (FIRST[u.n] || []).filter(id => byUnit[i].includes(id));
  const p = { n: u.n, ar: u.ar, en: u.en, words: first.concat(byUnit[i].filter(id => !first.includes(id))) };
  const late = (LATE[u.n] || []).filter(id => VOCAB.some(w => w.id === id));
  if (late.length) {
    // late words need a batch (path.js BATCH = 10) of their own, so the steps learners
    // already finished keep exactly the words they had
    if (p.words.length % 10) throw new Error(`unit ${u.n}: late words need a full last batch (has ${p.words.length})`);
    p.lateFrom = p.words.length; p.words.push(...late); late.forEach(id => placed.add(id));
  }
  return p;
});
fs.writeFileSync(path.join(root, 'path-data.js'),
  '/* Generated by tools/build-path.js — do not edit by hand.\n' +
  '   PATH: the units of the learning path and the word ids each one teaches.\n' +
  '   PIC:  word id → picture (emoji) for the "meet" step. */\n' +
  'const PATH = ' + JSON.stringify(PATH) + ';\n' +
  'const PIC = ' + JSON.stringify(PIC) + ';\n');

PATH.forEach(p => console.log(p.n, p.en.padEnd(26), p.words.length, 'words'));
console.log('in the path:', placed.size, '| extra practice only:', VOCAB.length - placed.size);
