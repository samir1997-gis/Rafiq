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
