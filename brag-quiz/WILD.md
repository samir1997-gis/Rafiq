# Two high-energy TikToks (#237)

Built by `brag-quiz/build_wild.py` (its header has the commands). 1080x1920, the app's reading voice only, levelled to about -16 LUFS.

| Video | Length | What happens |
|---|---|---|
| `out/x1-machine/x1-machine.mp4` | 24s | **The Arabic word machine.** A slot machine with blinking bulbs. Pull the lever and three reels blur-spin, then land on the root د ر س one by one. A pattern reel spins: "he did it" → دَرَسَ, "a place for it" → مَدْرَسَة, "someone who does it" → مُدَرِّس. Each word drops into the tray with sunburst rays and confetti, is said, then flies down onto a shelf. Twist: "Now swap the root 🔄". The reels land on ك ت ب, the pattern stays "a place for it", and out comes مَكْتَبَة, library (the big jackpot). |
| `out/x2-dots/x2-dots.mp4` | 23s | **Dots are power-ups.** An arcade game on a dark grid, with a level counter, score and XP bar. One shape, ٮ. Level banners sweep in, then glowing dots drop from the sky and bounce into place, with screen shake, a flash, sparks and +100. One dot below makes ب (بَيْت), two on top make ت (تَمْر), three on top make ث (ثَلاثَة). Boss level is a shell game: ب ت ث flip face down and shuffle, then "Where's ت? 👀", 3-2-1, and the reveal for +500. |

## Where it comes from

- **x1:** مَدْرَسَة school (`vocab-data.js` 149), مُدَرِّس teacher (30), مَكْتَبَة library (279). دَرَسَ "he studied" is from `toolkit-data.js` VERBS.
- **x2:** the letters, their sounds ("b" as in bed…) and the words بَيْت, تَمْر, ثَلاثَة are from `alphabet-data.js` (Letters 1).
- **The dots are measured, not drawn by eye:** the builder draws ٮ and each letter in the app's Arabic font, finds where each letter's dots sit, and drops the power-ups exactly there.
- **Worth a glance from the teacher (written for the video, not from the data):**
  - The pattern labels: "he did it" (the past), "a place for it" (ma-…-a), "someone who does it" (mu-…).
  - "root د ر س · studying" and "root ك ت ب · writing".
  - That مَكْتَبَة is "a place for" ك ت ب.

Not checked with TypeSafe (no key in this session): check the captions with it before posting (CLAUDE.md).

## Titles and descriptions

**x1-machine**: *Arabic has a word machine 🎰*
Put in 3 letters (a root), pick a pattern, and out comes a word. D-R-S: darasa he studied, madrasa school, mudarris teacher. Then swap the root to K-T-B with the same "place" pattern… maktaba, library 🤯 Which root should I spin next? 👇 Learn how Arabic really works with Rafiq, link in bio (free for a week). #learnarabic #arabic #arabicgrammar #languagelearning #didyouknow #arabicroots

**x2-dots**: *Arabic speedrun: 1 shape + dots = 3 letters 🎮*
Same shape, different dots: one below is bā' (bayt, house), two on top tā' (tamr, dates), three on top thā' (thalātha, three). Then the boss level: can you keep your eye on tā'? 👀 Found it? Comment 👇 Read Arabic from zero with Rafiq, link in bio (free for a week). #learnarabic #arabic #arabicalphabet #arabicforbeginners #gaming #challenge
