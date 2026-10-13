# Ten TikToks: words of the day, the app, verbs from I to we (#222)

Five videos (1080x1920, the app's reading voice only, about -16 LUFS) and five carousels (1080x1350, TikTok photo mode).
Built by `brag-quiz/build_social.py` (its header has the commands).

| # | Piece | Type | File(s) |
|---|---|---|---|
| 1 | Word of the day: شُكْراً | Video, 21s | `brag-quiz/out/w1-shukran/w1-shukran.mp4` |
| 2 | Word of the day: صَدِيق / صَدِيقَة | Carousel, 5 slides | `brag-social/c1-sadiq/` |
| 3 | Word of the day: رِحْلَة | Carousel, 4 slides | `brag-social/c2-rihla/` |
| 4 | The app in 20 seconds | Video, 20s | `brag-quiz/out/a1-tour/a1-tour.mp4` |
| 5 | Your salah, word by word | Carousel, 4 slides | `brag-social/c3-salah/` |
| 6 | What's inside Rafiq | Carousel, 5 slides | `brag-social/c4-inside/` |
| 7 | "To go", I to we (present) | Video, 31s | `brag-quiz/out/v1-go/v1-go.mp4` |
| 8 | "To write", I to we (past) | Video, 30s | `brag-quiz/out/v2-write/v2-write.mp4` |
| 9 | Quiz: "I drink" → "we drink"? | Video, 24s | `brag-quiz/out/v3-drink/v3-drink.mp4` |
| 10 | "To study", one slide per person | Carousel, 9 slides | `brag-social/c5-study/` |

A good order to post: alternate the types, e.g. 7, 2, 4, 9, 5, 1, 10, 6, 8, 3.

## Where everything comes from

- **Words, phrases and meanings:**
  - `vocab-data.js`:
    - شُكْراً 110, عَفْواً 184
    - صَدِيق 26, صَدِيقَة 27
    - رِحْلَة 406, رِحْلَة سَعِيدَة 478
  - `drills-data.js` (the phrases, with their English):
    - "شُكْراً جَزِيلاً." Thank you very much.
    - "شُكْراً يا أُمِّي." Thank you, mother.
    - "مَعَ السَّلامَةِ يا صَدِيقِي." Goodbye, my friend.
- **Verb forms:** `toolkit-data.js` `VERBS` (ذَهَبَ present, كَتَبَ past, دَرَسَ present, شَرِبَ). The builder checks that every coloured split puts back together into the app's own form, and that every form it says has a recording.
- **Screens:** `brag-social/screens/`, taken from the app running locally with a test account (`tests/startup_speed.py`'s fake sign-in), Complete plan.
  - No progress was made up, so screens that would show "0 day streak" (Home, Progress) aren't used.
  - The test account's email is hidden on the Your words screen.
- **App facts:**
  - "56%" and "five words at a time" are from the Your salah screens.
  - "21 verbs" is from the Verb forms page.
  - Weak-spots review and Real-life scenes carry the COMPLETE badge in the app.
- **Worth a glance from the teacher (explanations written for these, not from the data):**
  - صَدِيق "for a man or a boy" / صَدِيقَة "for a woman or a girl".
  - "the ي on the end means my".
  - "only the first letter changes" (present).
  - "only the ending changes" (past).
  - "'He wrote' has no ending; that's the form the dictionary gives you".
  - "'you go' and 'she goes' are the same word" (true in the data: both تَذْهَبُ).

Not checked with TypeSafe (no key in this session): check the captions with it before posting (CLAUDE.md).

## Titles and descriptions

All end on "link in bio": put rafiq-arabic.com/tt in the TikTok bio.

**1 · w1-shukran**: *The first Arabic word you should learn 🙏*
Shukran, thank you. Then level it up: shukran jazīlan, thank you very much. And when someone thanks you: ʿafwan, you're welcome. Save it and use it today 📌 A new word every day with Rafiq, link in bio (free for a week). #learnarabic #arabic #arabicwordoftheday #arabicforbeginners #shukran

**2 · c1-sadiq**: *Word of the day: friend 🤝*
Ṣadīq for a man, ṣadīqa for a woman. Add one letter and it's feminine. And when you leave: maʿa s-salāma yā ṣadīqī, goodbye, my friend. Tag a friend 👇 Learn a word a day with Rafiq, link in bio (free for a week). #learnarabic #arabic #arabicwordoftheday #friends #arabicforbeginners

**3 · c2-rihla**: *Word of the day for travellers ✈️*
Riḥla means a journey, a trip. Know someone who's travelling? Wish them riḥla saʿīda, have a good trip 🧳 A new word every day with Rafiq, link in bio (free for a week). #learnarabic #arabic #arabicwordoftheday #travel #arabicforbeginners

**4 · a1-tour**: *The app I use to learn Arabic, in 20 seconds 📱*
Short lessons where every word has audio, your salah word by word, every verb from I to we, review, a spelling bee and real-life scenes. Free for a week, no card: link in bio. #learnarabic #arabic #arabicapp #islam #muslim #studywithme

**5 · c3-salah**: *Do you know what you're saying in your salah? 🕌*
Rafiq shows every word of your prayer: what it means and how often you say it. The 20 words you say most are about 56% of a four-rakʿah prayer, so that's where it starts, five words at a time. Link in bio (free for a week). #salah #learnarabic #arabic #islam #muslim #prayer

**6 · c4-inside**: *What's inside an Arabic learning app 👀*
Short lessons with audio, 21 verbs in every form, weak-spots review, a spelling bee, real-life scenes, and your words coming back just before you'd forget them. Some of it is in the Complete plan; you can try everything free for a week: link in bio. #learnarabic #arabic #arabicapp #languagelearning #studytips

**7 · v1-go**: *How an Arabic verb changes from "I" to "we" 🤯*
Dhahaba, to go. In the present only the first letter changes: adhhabu "I go", nadhhabu "we go". And "you go" and "she goes" are the same word! Did you know? 👇 Every verb, every form with Rafiq, link in bio (free for a week). #learnarabic #arabic #arabicgrammar #arabicverbs #arabicforbeginners

**8 · v2-write**: *"I wrote" vs "we wrote" in Arabic ✍️*
In the past tense, only the ending changes: katabtu, I wrote · katabnā, we wrote. And "he wrote", kataba, has no ending at all. Save this one 📌 Every verb, every form with Rafiq, link in bio (free for a week). #learnarabic #arabic #arabicgrammar #arabicverbs #arabicforbeginners

**9 · v3-drink**: *If this means "I drink"… can you say "we drink"? 🥤*
Two quick verb questions, 3 seconds each. Got both? Comment 👇 Spot the pattern once and it works on every verb like it. Learn with Rafiq, link in bio (free for a week). #learnarabic #arabic #arabicquiz #arabicverbs #quiz

**10 · c5-study**: *"To study" in Arabic, from I to we 📚*
One verb, six people: adrusu, tadrusu, tadrusīna, yadrusu, tadrusu, nadrusu. Watch the red: the front letter tells you who. Swipe to the end for all six on one slide. Learn with Rafiq, link in bio (free for a week). #learnarabic #arabic #arabicgrammar #arabicverbs #studyarabic
