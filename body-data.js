/* body-data.js — the words of the body explorer (Practise → Everyday essentials →
   The body; body.js draws it). One entry per word:
     { id, ar, en, tr, level, parent, svgZoneId, audioId }
   - level   0 the whole body, 1 its regions, 2 a region's parts, 3 the organs inside
   - parent  the entry this word belongs to (its zoomed-in view shows it)
   - svgZoneId  the tappable shape in body.js's drawing; the drawing never names a word,
             so words can be edited here without touching it
   - vocab   where the word is already in vocab-data.js, its id there: ar is taken from
             it, with ال, so both spell it the same (an entry giving two forms, like
             "the tooth / teeth", keeps its own ar; tests/body_explorer.py checks it
             contains the vocab form)
   - audioId filled in by BODY_RESOLVE: the clip audio/<audioId>.mp3, recorded from
             `say` (both forms of a pair, with a comma) by tools/build-manifest.js
   ALL OF THIS ARABIC IS PROVISIONAL: a teacher checks the words and vowel marks before
   it goes live (#206). Shown with the definite article, as a labelled diagram reads. */
const BODY_WORDS = [
  { id:'body',      ar:'الجِسْم',              en:'the body',              tr:'al-jism',        level:0, parent:null,     svgZoneId:'z-body' },

  // Level 1: the whole body
  { id:'head',      vocab:508,                 en:'the head',              tr:'ar-raʾs',        level:1, parent:'body',   svgZoneId:'z-head' },
  { id:'neck',      ar:'الرَّقَبة',             en:'the neck',              tr:'ar-raqaba',      level:1, parent:'body',   svgZoneId:'z-neck' },
  { id:'torso',     ar:'الجِذْع',              en:'the torso / trunk',     tr:'al-jidhʿ',       level:1, parent:'body',   svgZoneId:'z-torso' },
  { id:'arm',       vocab:652,                 en:'the arm',               tr:'adh-dhirāʿ',     level:1, parent:'body',   svgZoneId:'z-arm' },
  { id:'hand',      vocab:752,                 en:'the hand',              tr:'al-yad',         level:1, parent:'body',   svgZoneId:'z-hand' },
  { id:'back',      ar:'الظَّهْر',             en:'the back',              tr:'aẓ-ẓahr',        level:1, parent:'body',   svgZoneId:'z-back' },
  { id:'leg',       ar:'السّاق',               en:'the leg',               tr:'as-sāq',         level:1, parent:'body',   svgZoneId:'z-leg' },
  { id:'foot',      ar:'القَدَم',              en:'the foot',              tr:'al-qadam',       level:1, parent:'body',   svgZoneId:'z-foot' },

  // Level 2: the head
  { id:'eye',       ar:'العَيْن',              en:'the eye',               tr:'al-ʿayn',        level:2, parent:'head',   svgZoneId:'z-eye' },
  { id:'nose',      vocab:551,                 en:'the nose',              tr:'al-anf',         level:2, parent:'head',   svgZoneId:'z-nose' },
  { id:'mouth',     ar:'الفَم',                en:'the mouth',             tr:'al-fam',         level:2, parent:'head',   svgZoneId:'z-mouth' },
  { id:'ear',       vocab:543,                 en:'the ear',               tr:'al-udhun',       level:2, parent:'head',   svgZoneId:'z-ear' },
  { id:'hair',      ar:'الشَّعْر',             en:'the hair',              tr:'ash-shaʿr',      level:2, parent:'head',   svgZoneId:'z-hair' },
  { id:'forehead',  ar:'الجَبِين',             en:'the forehead',          tr:'al-jabīn',       level:2, parent:'head',   svgZoneId:'z-forehead' },
  { id:'cheek',     ar:'الخَدّ',               en:'the cheek',             tr:'al-khadd',       level:2, parent:'head',   svgZoneId:'z-cheek' },
  { id:'chin',      ar:'الذَّقْن',             en:'the chin',              tr:'adh-dhaqn',      level:2, parent:'head',   svgZoneId:'z-chin' },
  { id:'lip',       ar:'الشَّفة',              en:'the lip',               tr:'ash-shafa',      level:2, parent:'head',   svgZoneId:'z-lip' },
  { id:'teeth',     ar:'السِّنّ / الأَسْنان', vocab:548, en:'the tooth / teeth', tr:'as-sinn / al-asnān', level:2, parent:'head', svgZoneId:'z-teeth' },
  { id:'tongue',    vocab:734,                 en:'the tongue',            tr:'al-lisān',       level:2, parent:'head',   svgZoneId:'z-tongue' },
  { id:'eyebrow',   ar:'الحاجِب',              en:'the eyebrow',           tr:'al-ḥājib',       level:2, parent:'head',   svgZoneId:'z-eyebrow' },

  // Level 2: the arm and hand
  { id:'shoulder',  ar:'الكَتِف',              en:'the shoulder',          tr:'al-katif',       level:2, parent:'arm',    svgZoneId:'z-shoulder' },
  { id:'upperarm',  ar:'العَضُد',              en:'the upper arm',         tr:'al-ʿaḍud',       level:2, parent:'arm',    svgZoneId:'z-upperarm' },
  { id:'elbow',     ar:'الكوع / المِرْفَق',    en:'the elbow',             tr:'al-kūʿ / al-mirfaq', level:2, parent:'arm', svgZoneId:'z-elbow' },
  { id:'forearm',   ar:'السّاعِد',             en:'the forearm',           tr:'as-sāʿid',       level:2, parent:'arm',    svgZoneId:'z-forearm' },
  { id:'wrist',     ar:'المِعْصَم',            en:'the wrist',             tr:'al-miʿṣam',      level:2, parent:'arm',    svgZoneId:'z-wrist' },
  { id:'palm',      ar:'الكَفّ',               en:'the palm',              tr:'al-kaff',        level:2, parent:'hand',   svgZoneId:'z-palm' },
  { id:'fingers',   ar:'الإِصْبَع / الأَصابِع', en:'the finger / fingers', tr:'al-iṣbaʿ / al-aṣābiʿ', level:2, parent:'hand', svgZoneId:'z-fingers' },
  { id:'thumb',     ar:'الإِبْهام',            en:'the thumb',             tr:'al-ibhām',       level:2, parent:'hand',   svgZoneId:'z-thumb' },
  { id:'nail',      ar:'الظُّفْر',             en:'the nail',              tr:'aẓ-ẓufr',        level:2, parent:'hand',   svgZoneId:'z-nail' },

  // Level 2: the leg and foot
  { id:'thigh',     ar:'الفَخِذ',              en:'the thigh',             tr:'al-fakhidh',     level:2, parent:'leg',    svgZoneId:'z-thigh' },
  { id:'knee',      ar:'الرُّكْبة',            en:'the knee',              tr:'ar-rukba',       level:2, parent:'leg',    svgZoneId:'z-knee' },
  { id:'shin',      ar:'السّاق',               en:'the shin / lower leg',  tr:'as-sāq',         level:2, parent:'leg',    svgZoneId:'z-shin' },
  { id:'ankle',     ar:'الكاحِل',              en:'the ankle',             tr:'al-kāḥil',       level:2, parent:'foot',   svgZoneId:'z-ankle' },
  { id:'heel',      ar:'الكَعْب',              en:'the heel',              tr:'al-kaʿb',        level:2, parent:'foot',   svgZoneId:'z-heel' },
  { id:'toe',       ar:'أُصْبُع القَدَم',      en:'the toe',               tr:'uṣbuʿ al-qadam', level:2, parent:'foot',   svgZoneId:'z-toe' },

  // Level 2: the torso
  { id:'chest',     vocab:564,                 en:'the chest',             tr:'aṣ-ṣadr',        level:2, parent:'torso',  svgZoneId:'z-chest' },
  { id:'belly',     ar:'البَطْن',              en:'the belly / abdomen',   tr:'al-baṭn',        level:2, parent:'torso',  svgZoneId:'z-belly' },
  { id:'waist',     ar:'الخاصِرة',             en:'the waist / side',      tr:'al-khāṣira',     level:2, parent:'torso',  svgZoneId:'z-waist' },
  { id:'navel',     ar:'السُّرّة',             en:'the navel',             tr:'as-surra',       level:2, parent:'torso',  svgZoneId:'z-navel' },
  { id:'inside',    ar:'الأَعْضاء الدّاخِلِيّة', en:'the internal organs', tr:'al-aʿḍāʾ ad-dākhiliyya', level:2, parent:'torso', svgZoneId:'z-inside' },

  // Level 3: inside (the common organs only)
  { id:'heart',     vocab:574,                 en:'the heart',             tr:'al-qalb',        level:3, parent:'inside', svgZoneId:'z-heart' },
  { id:'lungs',     ar:'الرِّئة / الرِّئَتان', en:'the lung / lungs',      tr:'ar-riʾa / ar-riʾatān', level:3, parent:'inside', svgZoneId:'z-lungs' },
  { id:'stomach',   ar:'المَعِدة',             en:'the stomach',           tr:'al-maʿida',      level:3, parent:'inside', svgZoneId:'z-stomach' },
  { id:'liver',     ar:'الكَبِد',              en:'the liver',             tr:'al-kabid',       level:3, parent:'inside', svgZoneId:'z-liver' },
  { id:'kidneys',   ar:'الكُلْيَة / الكُلْيَتان', vocab:575, en:'the kidney / kidneys', tr:'al-kulya / al-kulyatān', level:3, parent:'inside', svgZoneId:'z-kidneys' },
  { id:'intestines',ar:'الأَمْعاء',            en:'the intestines',        tr:'al-amʿāʾ',       level:3, parent:'inside', svgZoneId:'z-intestines' },
  { id:'brain',     ar:'الدِّماغ / المُخّ',    en:'the brain',             tr:'ad-dimāgh / al-mukhkh', level:3, parent:'inside', svgZoneId:'z-brain' },
];

/* Fills in ar (from vocab-data.js where linked), say (what's spoken) and audioId.
   Used by body.js and tools/build-manifest.js, so the page and the recordings agree. */
function BODY_RESOLVE(vocab){
  const byId = new Map((vocab || []).map(v => [v.id, v]));
  const SUN = 'تثدذرزسشصضطظلن';
  // ال + the word: a sun letter doubles (shadda after its vowel, as the rest of the site writes it)
  const withAl = w => {
    const m = w.match(/^(.)([ً-ِْ]?)(.*)$/);
    return SUN.includes(m[1]) ? 'ال' + m[1] + m[2] + 'ّ' + m[3] : 'ال' + w;
  };
  const aid = s => { let h = 5381; for(let i = 0; i < s.length; i++) h = ((h * 33) ^ s.charCodeAt(i)) >>> 0; return h.toString(36); };   // audio.js
  BODY_WORDS.forEach(w => {
    const v = w.vocab && byId.get(w.vocab);
    w.vocabAr = v ? withAl(v.ar.split(' / ')[0].trim()) : null;
    if(!w.ar && w.vocabAr) w.ar = w.vocabAr;
    if(!w.ar) return;
    w.say = w.ar.replace(/ \/ /g, '، ');
    w.audioId = aid(w.say);
  });
  return BODY_WORDS;
}
