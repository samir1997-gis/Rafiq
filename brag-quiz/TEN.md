# Ten more TikToks (#219)

Ten vertical videos (1080x1920): five quizzes and five that teach one thing. **The only sound is the app's reading voice**:
no fountain, no taps or chimes, no music. That leaves room to add a TikTok sound under them in the app if you want one.
Built by `brag-quiz/build_ten.py` (its header has the commands), in the same look as the earlier quiz and teaching videos.
Every Arabic word is said with the app's own recording, and all ten are levelled to about -16 LUFS.

| Video | Type | What happens | Why people engage |
|---|---|---|---|
| `q1-guess-food` | Quiz | Three food words (خُبْز, تَمْر, حَلِيب), three meanings each, a 3-2-1, then the answer | "Can you get 3 out of 3?" Scores go in the comments. |
| `q2-loanwords` | Quiz | سُكَّر, قَهْوَة, زَرافة, صِفْر: guess the English word each one became (sugar, coffee, giraffe, zero) | Surprise, and "I already know Arabic". |
| `q3-listen` | Quiz, sound on | Hear an animal's name (twice), pick the picture: horse, lion, cat | Makes people turn the sound on and watch to the end. |
| `q4-salah-where` | Quiz | When in the prayer do you say this? Rising, rukūʿ, sujūd (the last two differ by one word) | Most people say these daily without knowing which is which by meaning. |
| `q5-numbers` | Teach + quiz | One to five with the digits, then "which number is it?" twice | An easy win for beginners. |
| `i1-salam-reply` | Teach | How to answer السَّلامُ عَلَيْكُم, then كَيْفَ حالُكَ / حالُكِ (one vowel for a man or a woman), then الحَمْدُ لِلَّهِ | Useful straight away; easy to save and share. |
| `i2-sun-letters` | Teach + quiz | Why it's ash-shams, not al-shams: the 14 sun letters, then "sun or moon?" twice | A real reading "aha". |
| `i3-days` | Teach | Sunday to Thursday are "day one" to "day five"; Friday is the day of gathering; and Saturday | A fact people repeat to friends. |
| `i4-ta-marbuta` | Teach | ة turns him into her: جَدّ → جَدَّة, ابْن → ابْنَة, والِد → والِدَة; but أَخ → أُخْت | A pattern you can spot at once. |
| `i5-salah-words` | Teach | Three things you say in every prayer, word by word: اللَّهُ أَكْبَرُ, سَمِعَ اللَّهُ لِمَنْ حَمِدَهُ, رَبَّنا وَلَكَ الْحَمْدُ | Understanding your own prayer. |

## Where every fact comes from

- **Words, meanings and transliterations:** `vocab-data.js`.
  - q1: 169, 166, 168, plus tea, fish and water as the wrong answers.
  - q2: 331, 190, 686, 373.
  - q3: 714, 736, 710, 720, 671, 172.
  - q5: 34–38.
  - i1: 1, 2, 3, 4, 6.
  - i2: 520, 121, 119, 122.
  - i3: 780, 781, 120, 782, 121, 122, 119 and the numbers 35–38.
  - i4: 52/53, 47/48, 56/57, 32/33.
- **Prayer phrases and their word-by-word meanings:** `salah-data.js` (takbīr, rukūʿ, rising, sujūd). These are the prayer's own words, never the Quran, which the app's voice never says.
- **Not from the app's data** (general knowledge, worth a glance from the teacher):
  - **q2:** that these English words came from Arabic.
    - sugar, from *sukkar*, via Latin and French
    - coffee, from *qahwa*, via Turkish
    - giraffe, from *zarāfa*, via Italian
    - zero, from *ṣifr*, via Italian

    These are the usual dictionary etymologies (e.g. Merriam-Webster).
  - **q5:** the Eastern Arabic digits ١ ٢ ٣ ٤ ٥.
  - **i1:** "only the last vowel changes" (-ka to a man, -ki to a woman).
  - **i2:**
    - The 14 sun letters: ت ث د ذ ر ز س ش ص ض ط ظ ل ن.
    - The ل of ال isn't said before them, and the next letter is doubled.
  - **i3:**
    - The days are named from the numbers: أَحَد "one" is shown but not said, because the app has no recording of it on its own.
    - الجُمُعَة is from ج م ع, "to gather".
  - **i4:**
    - ة at the end of a word is "usually feminine".
    - أُخْت ends in ت.

## Titles and descriptions to post with them

Each ends on "link in bio" because links in TikTok descriptions can't be tapped.

**q1-guess-food**: *Can you guess these 3 Arabic words? 🍞*
Three everyday Arabic words, three choices each, and 3 seconds to answer ⏱️ No pressure 😅 Comment your score 👇 1, 2 or 3 out of 3? Learn the Arabic you'll actually use with Rafiq, link in bio (free for a week). #learnarabic #arabic #arabicquiz #quiz #arabicwords #languagelearning

**q2-loanwords**: *You already speak Arabic (you just don't know it) ☕*
Sugar, coffee, giraffe and zero all came into English from Arabic: sukkar, qahwa, zarāfa and ṣifr. How many did you guess before the timer ran out? 👇 Which one surprised you most? Learn Arabic with Rafiq, link in bio (free for a week). #learnarabic #arabic #etymology #languages #didyouknow #arabicwords

**q3-listen**: *Sound on 🔊 Which animal is it?*
You'll hear an animal's name in Arabic. Pick the right one before the timer ends 🐴🦁🐱 3 out of 3? Tell me in the comments 👇 Every word in Rafiq is said by a real voice. Link in bio (free for a week). #learnarabic #arabic #arabicquiz #listening #arabicwords #quiz

**q4-salah-where**: *You say these in every prayer, but when? 🕌*
Three phrases you say in every salah. Do you know which part of the prayer each one belongs to? Careful: the last two differ by just one word 👀 How many did you get? 👇 Understand every word of your salah with Rafiq, link in bio (free for a week). #salah #learnarabic #arabic #islam #muslim #prayer #namaz

**q5-numbers**: *Count to 5 in Arabic, then test yourself 🔢*
Wāḥid, ithnān, thalātha, arbaʿa, khamsa. Then two quick rounds: which number did you hear? Did you get both? 👇 Learn numbers, times and dates with Rafiq, link in bio (free for a week). #learnarabic #arabic #arabicnumbers #arabicforbeginners #languagelearning

**i1-salam-reply**: *How to answer "as-salāmu ʿalaykum" 👋*
Someone greets you with salam. What do you say back? And did you know "how are you?" changes by one vowel for a man or a woman? Kayfa ḥāluka / kayfa ḥāluki. Save this for later 📌 Say it right from day one with Rafiq, link in bio (free for a week). #learnarabic #arabic #salam #islam #muslim #arabicforbeginners

**i2-sun-letters**: *Why "ash-shams" and not "al-shams"? ☀️🌙*
Before 14 Arabic letters, the "sun letters", the L in "al-" disappears and the next letter doubles. That's why it's as-salām, not al-salām. Did you get sun or moon right at the end? 👇 Read Arabic the way it's said with Rafiq, link in bio (free for a week). #learnarabic #arabic #arabicreading #sunletters #tajweed #arabicforbeginners

**i3-days**: *Arabic days of the week are just numbers 🤯*
Sunday is "day one", Monday "day two", all the way to Thursday, "day five". Friday is different: al-jumuʿa, the day of gathering 🕌 Did you know this? 👇 Learn the words behind the words with Rafiq, link in bio (free for a week). #learnarabic #arabic #languagefacts #didyouknow #jummah #arabicwords

**i4-ta-marbuta**: *One letter turns "he" into "she" in Arabic ✨*
Add ة to the end of a word and it's usually feminine: grandfather → grandmother, son → daughter, father → mother. But watch out for brother → sister 👀 Spot the pattern and learn faster with Rafiq, link in bio (free for a week). #learnarabic #arabic #arabicgrammar #arabicforbeginners #languagelearning

**i5-salah-words**: *What you're really saying in every prayer 🤲*
Allāhu akbar. Samiʿa llāhu liman ḥamidah. Rabbanā wa laka l-ḥamd. You say them every day. Here's what each word means. Which one did you not know? 👇 Understand every word of your salah with Rafiq, link in bio (free for a week). #salah #learnarabic #arabic #islam #muslim #prayer #quranwords

Bio link for TikTok: rafiq-arabic.com/tt (tags visits as TikTok in the funnel).

Not checked with TypeSafe (no key in this session): check the captions with it before posting (CLAUDE.md).
