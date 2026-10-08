# How we post (the owner's rule, checked with TypeSafe: tools/typesafe-exp/reach_strategy.py)

Posts are for reach and engagement first; follows bring people to the site over time.
- **About 4 posts in 5 are pure content**: a quiz, a fact, something fun. The caption asks for a comment, a share
  ("send it to someone who'd get 0/3") or a follow ("follow for a new Arabic quiz every week"). No app, no link.
- **About 1 in 5 shows the app** and says "free week, link in bio".
- TypeSafe, 0-3 averaged over three viewers: this mix grows the accounts about twice as much as every post ending on
  the link (1.19 vs 0.51) and is trusted more (1.51 vs 0.99), for the same sign-ups (0.25 vs 0.24).

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
