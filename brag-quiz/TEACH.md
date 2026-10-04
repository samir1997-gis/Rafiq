# Teaching videos (#218)

Three vertical videos (1080x1920) that teach one real thing each and show what Rafiq does with it. Fully generated: no filming.
Built by `brag-quiz/build_teach.py` (see its header for the commands). Every Arabic word is said with the app's own recording.

| Video | Length | What it teaches | Engagement hook |
|---|---|---|---|
| `t1-masjid` | 26.2s | مَـ at the start of a word often means "the place of": مَسْجِد is the place of السُّجُودُ; then مَدْرَسَة, مَكْتَبَة, مَطْعَم | Ends on "Your turn": مَطْبَخ, a 3-2-1, then the answer. People guess in the comments. |
| `t2-subhana` | 26.7s | You say سُبْحانَ 36 times in a four-rakʿah prayer (12 in rukūʿ + 24 in sujūd), what it means word by word, and that the 20 words you say most are about 56% of the prayer | A number most people have never counted. |
| `t3-remember` | 22.0s | New words fade fast without review; Rafiq brings each one back just before you'd forget it, and the gap grows: 3 days → 2 weeks → 2 months → 6 months | "Learnt a new Arabic word yesterday? It's already fading." |

## Where every fact comes from

- **Words and recordings:** `vocab-data.js` (مَسْجِد, مَدْرَسَة, دَرَسَ, مَكْتَبَة, كِتاب, مَطْعَم, طَعام, مَطْبَخ), `salah-data.js` (السُّجُودُ, the rukūʿ and sujūd lines and their meanings). The root letters are coloured inside each word.
- **36:** `salah.js` counts each prayer phrase per four-rakʿah prayer (`REPS`: rukūʿ 12, sujūd 24, assuming each is said three times). The app shows the same number on the word card.
- **56%:** the app's own line on Most-said words 1–5: "The 20 words you say most are about 56% of everything you say in a four-rakah prayer."
- **The gaps:** `progress.js` + `fsrs.js`, simulated for a word answered right on each due day: 3, 14, 57, then 196 days. A missed word comes back sooner (the next day for a new word, longer for one you've known a while), so the video only says "sooner".
- **Glosses written for the video** (not from the data): "the place of studying / books / food / cooking", "the place of prostration". These are the usual explanation of the مَفْعَل pattern; worth a glance from the teacher.
- **The graph** is an illustration (labelled "not to scale"), not measured data.

## Captions to post with them

**t1-masjid:** Why is a mosque called a masjid? 🕌 Once you see this pattern you'll spot it everywhere. Did you get the last one before the answer? #learnarabic #arabic #masjid #islam #muslim

**t2-subhana:** You say سُبْحانَ 36 times in every four-rakʿah prayer. Do you know what it means? #salah #learnarabic #arabic #islam #muslim

**t3-remember:** Why new Arabic words disappear, and how to make them stay. #learnarabic #arabic #studytips #languagelearning

Bio link for TikTok: rafiq-arabic.com/tt (tags visits as TikTok in the funnel).

## The sound

The fountain from `brag-output-v6` under everything, the app's recordings for the Arabic, `tap.mp3` and `correct.mp3` on the
frame that causes them, no music. The fountain is a soft bed: still heard, 8-11 dB quieter than the first cut. After
rendering, `--level` sets t1 and t2 to about -16 LUFS (a normal TikTok loudness) and t3, which is mostly the fountain, to -25 so
its fountain is no louder than t1's; the words sit well above the bed. The earlier quiz videos are
much quieter (#217).

Silent copies (`out/<id>/<id>-silent.mp4`, same picture, no audio track) are there for posting with a sound picked in TikTok.

Not checked with TypeSafe (no key in this session): check the captions with it before posting (CLAUDE.md).
