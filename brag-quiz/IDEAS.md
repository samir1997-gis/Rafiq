# How we post (the owner's rule, checked with TypeSafe: tools/typesafe-exp/reach_strategy.py)

Posts are for reach and engagement first; follows bring people to the site over time.
- **About 4 posts in 5 are pure content**: a quiz, a fact, something fun. The caption asks for a comment, a share
  ("send it to someone who'd get 0/3") or a follow ("follow for a new Arabic quiz every week"). No app, no link.
- **About 1 in 5 shows the app** and says "free week, link in bio".
- TypeSafe, 0-3 averaged over three viewers: this mix grows the accounts about twice as much as every post ending on
  the link (1.19 vs 0.51) and is trusted more (1.51 vs 0.99), for the same sign-ups (0.25 vs 0.24).

**When to post (Metricool, @rafiqarabic, best times for 22–28 Oct 2026, UK time):** 10:00 is the peak every day; weekdays beat
weekends about 2 to 1 (Fri 10:00 the best slot of the week, then Wed and Thu; 18:00 the second peak). Post at 10:00 on weekdays.
**Trial reels (the level-up ad, #273):** don't post the ten at once (near-copies compete and can read as repeated content); post
one version a day as a pair, the edited one at 10:00 and the plain one at 10:30, as Instagram trial reels (non-followers only,
so the ads don't fill the grid): Thu 23 v1 · Fri 24 v2 · Mon 27 v3 · Tue 28 v4 · Wed 29 v5. Judge on hold and watch time;
share the winner to the profile afterwards.

## What our best videos do (owner's top three on Instagram, analysed 8 Oct 2026)

The winners: `s3-samiallahu` (rising from ruku, word by word), `t1-masjid` (why a mosque is a مَسْجِد) and `v3-drink`
(أَشْرَبُ "I drink", what's "we drink"?), all on `claude/teach-videos`. Compared with the 23 others in the same set:

1. **The hook is a question about something they already say or know but never understood.** "Why is a mosque called a
   masjid?" · "You say this every time you rise from ruku" · "If this is 'I drink'…". The quieter ones open with a
   statistic ("You say this word 36 times"), a product problem ("Learnt a word yesterday? It's fading") or a plain topic
   ("Count to five in Arabic").
2. **One "aha" pattern that makes the viewer feel clever and want to share it.** مَـ = "the place of" (masjid, madrasa,
   maktaba, matʿam), أَ → نَ for "I → we", the line taken apart word by word. Numbers alone (36 times, 56%) interest but
   don't give them something to use or tell a friend.
3. **The viewer plays along.** A 3-2-1 countdown before the answer (v3, the masjid "your turn" round), or a comment
   everyone can answer: s3 ends "What do you reply? Comment it 👇", and every Muslim knows the reply. Weaker asks need
   effort or are yes/no ("Which line should I do next?", "Did you know it was 22?").
4. **Short, with the payoff at the end:** 14-26 s, the answer revealed last, so people watch to the end and loop.
5. **It's content, not an ad.** The app card comes after the payoff, for two seconds, or not at all. The videos that
   explain the app (the forgetting curve, the 56% chart) are the quiet ones.

**The formula for the next ones:** a familiar word or moment from the prayer or daily life, asked as a question in the
first second · one pattern that unlocks several words · a "your turn" round with a 3-second countdown · end on a
comment anyone can answer · 15-25 s · app card last, or none (4 posts in 5).

**The three formats to keep making (owner, 10 Oct 2026; this is what's getting traction):**
1. **A salah line, word by word.** The line they say, then each word with its meaning (s3-samiallahu, f1-sujood). `build_series.build`.
2. **One important word traced to its root**, with the everyday words that share it (Jumuʿah → جامِعَة university), posted
   on the day it matters (Jumuʿah on a Friday). `j1`, `a1`, `r2` in `build_formula.py`.
3. **The word-change quiz**, more than "what does this mean": if this is X, what's the we / she / past / plural form?
   (v3-drink Ashrabu). `change()` in `build_formula.py`.
Made 10 Oct: `w5-rabbana`, `w6-salam`, `w7-tahiyyat` · `r2-muhammad` · `g1-plural`, `g2-female`, `g3-past`
(captions: `tools/typesafe-exp/batch3_captions.py`).

**Instagram, all 18 reels 1-10 Oct (Metricool, 10 Oct 2026).** Judged on rates, not raw views: early posts had fewer
followers, 8-9 Oct ones are still growing. Hold = still watching at 3 s; per 1,000 people reached.
- Question hooks about a word they already know hold best: Jumuʿah 39%, the سَمِعَ quiz 39%, Ashrabu 37%, masjid 35%.
  Topic/statement openers hold less: "Count to five" 30%, loanwords 23%, the forgetting-curve promo 16%.
- A share ask in the caption works: Jumuʿah ("Send this to who you're going to Jumuʿah with") 67 shares/1k, the rest 3-14.
- Saves come from "pattern you can reuse" videos: Ashrabu 18/1k, masjid 18, sujood 15, days 15. Promos 0-5.
- Short quizzes loop: the 17 s سَمِعَ quiz averaged 19 s watched (116%). 25-37 s videos are watched 15-25%, the 73 s ruku reel 13%.
- Vague captions ("Did you know? 🧐🤨", "You say this in salah every single time…") waste the hook; say the question.
- Six covers are the end card (logo + link), which reads as an ad on the grid: pick the question frame as the cover.

**Made from these findings (10 Oct 2026):** `q4-azim` (الْعَظِيمِ), `q5-ighfir` (اغْفِرْ), `q6-tahiyyat` (التَّحِيّاتُ): the 15-18 s
salah word quiz with a 5-second countdown, the format people replay (`build_quiz.py`); `a1-adhan` (why the adhān: أ ذ ن, your turn
أُذُن = ear, a Fajr share ask; `build_formula.py`). Captions: `tools/typesafe-exp/batch2_captions.py`.

**Recreated in the proven formats (11 Oct 2026, `build_formula.py`, notes in RECREATED.md):** `r3-akbar` (root ك ب ر; your turn كِبار),
`r4-insha` (root ش ي ء; your turn شَيْء), `g4-past-i` (word change: he wrote/went → I wrote/went, ـتُ), `w8-subhana-azim` (the rukūʿ line
word by word), `q3-sujood` re-levelled. These replace p1-akbar, p5-insha, v1-go, v2-write and t2-subhana.

**Made in the formula (10 Oct 2026, `build_formula2.py`, captions in FORMULA2.md):** `p1-akbar` (why akbar, not kabīr: أَفْعَل; your turn عَلِيّ),
`p2-ana` (the أَ of أَشْهَدُ = I; your turn أَكْتُبُ; the app post), `p3-li` (the li of lillāh; your turn لِي), `p4-hamd` (Muhammad, Ahmad,
al-ḥamdu share ح م د; your turn مَحْمُود; tag ask), `p5-insha` (in shā' Allāh word by word; your turn ما شاءَ اللهُ). Hook big on frame 0 for the cover.

**Made in the formula (8 Oct 2026, `build_formula.py`):** `f1-sujood` (سُبْحانَ رَبِّيَ الْأَعْلى; ends "What do you say in rukūʿ
instead? Comment it"), `f2-root` (school, teacher, to study share د ر س; your turn: كِتاب), `f3-she-eats` (يَأْكُلُ → تَأْكُلُ,
أَكَلَ → أَكَلَتْ, with أَكَلْتُ as the trap). Captions checked with TypeSafe (`tools/typesafe-exp/formula_batch1_captions.py`).

# Quiz backlog (#198)

The owner asked to keep these for later: "I might ask you to generate them soon". Each becomes one entry in
`quizzes.json` (video: `python3 build_quiz.py <id>`) or in `stills.json` (images: `python3 build_stills.py <id>`).
All have the app's native audio (`audio-manifest.json`, bucket `salah`); meanings are from `salah-data.js`.

| Idea | Word / question | Answer | Distractors | Said in |
|---|---|---|---|---|
| What does this word mean? | اغْفِرْ | forgive | guide, bless, protect | رَبِّ اغْفِرْ لِي, between the two sujood |
| What does this word mean? | الْعَظِيمِ | the Magnificent | the Most High, the Merciful, the Greatest | ruku |
| What does this word mean? | الْأَعْلى | the Most High | the Magnificent, the First, the Greatest | sujood |
| What does this word mean? | التَّحِيّاتُ | all greetings | all praise, all prayers, all blessings | tashahhud |
| What does this word mean? | أَشْهَدُ | I bear witness | I believe, I know, I promise | tashahhud |
| Which word means "forgive"? | اغْفِرْ / ارْحَمْ / اهْدِ | اغْفِرْ | (check the others with the teacher first) | between the sujood |
| You say this 36 times in every four-rakah prayer | سُبْحانَ | Glory be to | Praise be to, Thanks be to, Peace be upon | ruku and sujood |
| Finish the line | سَمِعَ اللَّهُ لِمَنْ … | حَمِدَهُ | رَبَّنا, الْعَظِيمِ | rising from ruku |

Avoid: "which means my Lord?" (رَبِّ and رَبِّيَ both do), and rapid-fire "comment your score" (TypeSafe: flippant, 1.80/3 respect).
Already made: videos سَمِعَ (q1), رَبَّنا (q2), ruku → sujood (q3); stills سَمِعَ, اغْفِرْ, الْعَظِيمِ, التَّحِيّاتُ, أَشْهَدُ (stills/).
Also made since (don't repeat the format without a twist): the salah word-by-word series s1-s3 (`build_series.py`: اللَّهُ أَكْبَرُ,
سُبْحانَ رَبِّيَ الْعَظِيمِ, سَمِعَ اللَّهُ لِمَنْ حَمِدَهُ), f1-f2 (`build_fresh.py`), x1-x2 (`build_wild.py`), m01-m10 (`build_mix.py`); see FRESH.md, WILD.md, MIX.md.

**Made 17 Oct 2026 (`build_formula.py`):** `m2-barik` (mashallah vs Allahumma barik: 18:39 said over your own garden; the barakah
dua for someone else's blessing, Ibn Mājah 3509; root ب ر ك; a "new baby" test, answer both; hook `tools/typesafe-exp/barik_hook.py`).
**Don't post** `m1-mashallah`, which it replaces: its "past tense, so for the past" point is wrong (إِنْ شاءَ اللهُ is the same form).
Also  (mashallah redone in the standard, 62 s: Callum explains, Rafiq and al-Husary's
18:39 for the Arabic; word by word, past tense vs إِنْ شاءَ اللهُ, the root ش ي ء, a "mashallah or inshallah?" test. Hook and caption
tested: `tools/typesafe-exp/mashallah_hook.py`, `mashallah_caption.py`). The longest generated video so far: compare its watch time.

**Made 13–14 Oct 2026 (`build_formula.py`):** `n1-jannah` (root series part 3, ج ن ن: Jannah, jinn, majnūn; your turn جَنِين; the owner
stitches himself under it); `l1-ladder` (the difficulty ladder, owner approved: one page that slides up, a % rail on the left, 90% → 5%,
words ordered by the Kelly list's CEFR levels (ssharoff.github.io/kelly): far/near A1, cold A2, hot/fat/thin B1, final boss خائِن C1;
Kelly ranks by corpus frequency, so everyday shop words like رَخِيص come out "C2": sanity-check those by hand). The ladder's
percentages are a game device, never stated as data.

**Made 15 Oct 2026 (`build_formula.py`):** `g5-endings` (#261), "one word, many endings" made as a word-change quiz in the g4
standard: hook "NOBODY tells you Arabic has no word for 'my'!", then اسْمِي "my name" → his name (ـهُ) and بَيْتُكَ "your house" →
her house (ـها, the trap is ـهُ). More endings (our, their, your f.) are left for a part 2.

**Made 18 Oct 2026 (`build_formula.py`, #264; owner: "be more creative"), both in the standard:** `n2-rahma` (the word tree, root
series part 4: hook "FAMILY is hiding inside a word you say in every prayer!" over family names that leaves grow over; al-Fātiḥah 1:3
(al-Husary); ر ح م drops into the soil as a seed, a trunk grows, رَحْمَة and رَحِمَهُ اللهُ bloom with a word counter; the tree pulls back
for "your turn": رَحِم, 3-2-1, the womb; al-Bukhārī 5988, "the womb takes its name from ar-Raḥmān"; 44 s) and `d1-din` (hook
"SEVENTEEN times a day… do you know what this word MEANS?" over the day's prayers ticking up to 17 rakʿahs; al-Fātiḥah 1:4 (al-Husary);
"you know دِين as religion, but here?" 3-2-1: repayment, Ibn Kathīr on 1:4 from Ibn ʿAbbās; a year of squares filling, 17 → 6,205;
42 s). Captions: `tools/typesafe-exp/rahma_caption.py`, `din_caption.py` (not run yet: no TypeSafe key). Word timings from
`brag-quiz/align_words.py` (pocketsphinx), as huggingface.co was blocked.

**Made 18 Oct 2026 (`build_formula.py`, #265; owner asked for it after n2-rahma):** `f4-family` (the family tree: hook "TWO words for
'aunty' in Arabic, and one's like your MUM!" over the family popping in; the tree in Arabic, dad's side green, mum's side gold; the camera
zooms into عَمَّة (dad's sister) and pans to خالَة (mum's sister); fun fact: Ḥamza's daughter went to her khala, "the maternal aunt is in
the place of the mother" (al-Bukhārī 2699); your turn: mum's brother, 3-2-1, خال; ask: tag your khala; 45 s). Caption candidates:
`tools/typesafe-exp/family_caption.py` (not run yet). Next in this format: zoom into grandpa/grandma, or عَمّ and its root.

**Made 21 Oct 2026 (`build_formula.py`, #272):** `n3-ilm` (the word tree, part 2, now `word_tree()` shared with n2-rahma: hook "The WORLD is a sign, and you say it in every prayer!" over the sun, moon, stars, mountains, sea and trees tagged "a sign"; al-Fātiḥah 1:2 (al-Husary); ع ل م grows عِلْم and مُعَلِّم; your turn عَلامَة, 3-2-1, a sign; Ibn Kathīr on 1:2, ʿālam from ʿalāma; then the owner's end card (`brag-quiz/out/endcard/endcard-cream.mp4`); 50.5 s). Caption candidates: `tools/typesafe-exp/ilm_caption.py` (not run yet).

**Made 22 Oct 2026 (`build_formula.py`, #281):** `n4-jannah` (the word tree, part 3, the owner's hook "Why does JANNAH share the same root as the jinn?" over gardens, the night, a shield, a baby, the unseen and the jinn, hidden by leaves on "same root"; al-Anʿām 6:76 (al-Husary) "when the night covered him": ج ن ن = to cover; جَنَّة (a garden so thick its trees cover the ground) and جِنّ (hidden from our eyes) bloom; your turn جُنَّة, 3-2-1, a SHIELD; why Jannah: hidden from you for now, Ibn Fāris (Maqāyīs) and the ḥadīth qudsī "what no eye has seen…" (al-Bukhārī 3244); ask: send it to someone you want to meet in Jannah, what will you ask for first?; then the owner's end card; 70.8 s). Replaces `n1-jannah` (old format). Caption: `tools/typesafe-exp/jannah_caption.py` ("question").

**Made 23 Oct 2026 (`build_formula.py`):** `l2-jumuah` (the difficulty ladder #2, Jumuʿah edition, for the owner to stitch under himself, 3 s to answer each: غُسْل 90% → جَماعَة 70% → عِطْر 45% → لِباس 20% → the final boss أَنْصِتْ "be quiet and listen!" 1% (al-Bukhārī 934, Muslim 851); hadith for each word in the owner's notes: ghusl al-Bukhārī 877, congregation al-Bukhārī 645, perfume al-Bukhārī 880 / al-Nasāʾī 3939, best clothes Abū Dāwūd 343; ask: send it to who you're going to Jumuʿah with; 49 s). Percentages are a game device, not data.

**Made 23 Oct 2026 (`brag-quiz/reels/wrecking/build.py`):** `wrecking` (the owner's pick, in the style of @aperturemotion's "a wrecking ball that was never there": 8 s of a wrecking ball swinging at a rubric brick wall with ر on it, a FRAMES TO IMPACT counter, no voice; it freezes, a calm narrator says the reference's line with a soft chuckle, the scene turns to a blueprint; then ours: "watch this for another fifteen", Arabic is the key (a gold key, a door onto light: salah, the Qur'an (Yūsuf 12:2), du'a), without it a book in the dark, "unlock it, RafiqArabic.com", the owner's end card; 48 s). Owner's notes: all Brian; v3 (`wrecking-brian-v3.mp4`, 47.7 s, 24 Oct) times the swing on the reference: FRAMES TO IMPACT falls from 204 by ~12% every quarter second (fast, then a crawl to 006), the ball rushes in from the left edge and covers most of the way at once, then creeps to just short of the wall, while the camera zooms in steadily. v4 (`wrecking-brian-v4.mp4`): the pivot is up beyond the wall, so the chain is diagonal at the stop and the ball still looks like it's mid-swing. Sounds made for it: `sfx/soft/drone.wav`, `shimmer.wav`, `darkhum.wav`.

**Made 24 Oct 2026 (`build_formula.py`, #290):** `n5-salah` (the word tree, part 4, root series part 6: ص ل و. Hook "You do it FIVE times a day… but what does salah really mean?" over the five prayers, counted 1 to 5 with a click each as FIVE lands; حَيَّ عَلَى الصَّلاةِ from the adhān in Rafiq's voice; الصَّلاة and مُصَلَّى bloom (the app's recordings); your turn فَلْيُصَلِّ (ṣalāh, duʿāʾ or eat?), 3-2-1, make DUʿĀʾ: a fasting guest is told to "pray" for his host, Muslim 1431, and al-Tirmidhī 780 adds "meaning duʿāʾ"; "every ṣalāh is a duʿāʾ"; ask: who do you make duʿāʾ for first, send this to them; then the owner's end card; 67 s). **No Qur'an recitation in it**, on purpose: TikTok kept m2-barik off the For You feed as "unoriginal" (#289), and reused recitation audio is one suspect, so compare how this one is treated. Caption candidates: `tools/typesafe-exp/salah_caption.py` (not run yet: no TypeSafe key).

## More ideas (not made yet)
- Root series part 7: another word tree (`word_tree()` in `build_formula.py`), e.g. ح م د (al-ḥamd, Muḥammad, Aḥmad, Maḥmūd), done twice
  already in older formats (p4-hamd, r2-muhammad), so only with a new angle; or ذ ك ر (dhikr, tadhkira, dhakar).

## Ramadan countdown (parked by the owner, 4 Oct 2026, to come back to)

Facts: Ramadan 1448 expected to start about 8 Feb 2027 (moon-dependent: say "in shā' Allāh"/"expected"); on 4 Oct that's 127 days.
The salah from the opening takbīr to the salām, incl. al-Fātiḥah, has **93 different words** (salah-data.js); with the 10 short
surahs about 240. 93 words < the days left: "less than one a day". Full salah is in Complete: from 4 Oct, 4 payments of £11.99
before Ramadan = £47.96 (~38p/day); yearly £79.99 covers Ramadan.

TypeSafe (tools/typesafe-exp/ramadan_angle.py): **don't lead with the price**. "£47.96 until Ramadan" scored 0.95/3 sincere
(0.69 with a viewer wary of businesses using Ramadan). Best: a free daily series, "one word of your salah a day until
Ramadan" (believable 2.69, share 1.79), or the single post "127 days. 93 words. Less than one a day." Even the best reach
only ~1.5/3 sincere, so keep the tone humble and the sale soft.

Options: (1) one countdown post; (2) a daily template, "Day N · X days to Ramadan", one salah word with its audio and where
it's said, built from salah-data.js like build_stills.py.

## Fun / meme formats (5 Oct 2026, owner: "a bit more fun and silly")

`build_pov.py` makes POV photo carousels (big text, one big emoji per slide, end card). Made: `pov-salah`, `pov-imam`.
Rule: the punchline is a fact from the app (20 words you say most ≈ 56% of the prayer), never a made-up "I understand 60%"
testimonial (TypeSafe preferred the fact on every score; UK ad rules want testimonials to be real).

TypeSafe ranking of other fun formats (tools/typesafe-exp/fun_content.py; viral / respect / fit, 0–3):
1. POV: the imam recites a surah you learned 🥹 (2.62 / 2.93 / 1.70) **made**
2. POV: finished salah, didn't understand (2.12 / 2.43 / 2.39) **made**
3. "My Arabic, day 1 vs day 60" (2.35 / 2.60 / 1.95)
4. "Me nodding along to the Arabic in the khutbah" 🙂 vs after 20 words 🤯 (2.34 / 2.72 / 1.50)
5. "You say this 17 times a day" (al-Fātiḥah, 17 rakʿahs) (1.92 / 2.14 / 2.33)
Weaker: younger sibling corrects your Arabic; guess the word from the emoji; "green flag in a spouse"; "what your mum means
by in shā' Allāh" (respect 1.37: avoid jokes on religious phrases); loanwords (fit 0.83).

**Word-set carousels (19 Oct 2026, `build_word_carousels.py`).** The question-words carousel did best of the carousels (owner: "people
like the simple ones they can relate to"), so five more in the same format, words and sentences from the course: `pronouns`
(I/you/he/she/we, "we" in نَعْبُدُ), `time` (today/tomorrow/yesterday/now/after that), `here-this` (here/there/this m/f),
`feelings` (happy/hungry/ill/busy), `yes-no` (yes/no/of course/OK). Drive: "Rafiq videos" → one "Carousel - …" folder each.
Next in the series, if they work: "and/but/with/in", family words (to go with f4-family).
**Made 21 Oct 2026:** `colours` (`build_word_carousels.py colours`, #272): six colours in both forms (أَحْمَر / حَمْراء), the course's own sentences, the Green Dome, al-Baqarah 2:69, the Black Stone; a swatch on each slide and the cover's words in their own colours. Caption candidates: `tools/typesafe-exp/colours_caption.py` (not run yet).
**Made 20 Oct 2026:** `numbers` (1–10, `build_word_carousels.py numbers`): the course's own words and sentences, a salah link on 2/3/4/5/7 (Fajr رَكْعَتانِ, Maghrib 3, Dhuhr/ʿAsr/ʿIshāʾ 4, five prayers, al-Fātiḥah's 7 verses), أَحَد in al-Ikhlāṣ, the dual for two, 3–10 working backwards, Arabic numerals ١٢٣. Caption candidates: `tools/typesafe-exp/numbers_caption.py` (not run yet).
**Made 19 Oct 2026:** `ghurabaa` carousel (`build_ghurabaa_carousel.py`): the strangers hadith (Muslim 145) word by word, the root غ ر ب
(Maghrib and stranger are family), Bukhari 6416. Drive: "Carousel - Strangers (ghurabaa)". Teacher to check the glosses.
