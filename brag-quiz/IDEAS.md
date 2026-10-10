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

## More ideas (not made yet)
- A word tree: a root grows like a vine, a word blooms on each branch (softer, for family or salah words).
- One word, many endings: كِتاب → my book, your book, his book as each ending slides in.
