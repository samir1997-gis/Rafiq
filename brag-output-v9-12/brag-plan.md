# Brag plan v9–v12: four vertical videos for the new features (#155)

## Why these four (TypeSafe, `tools/typesafe-exp/videos_v9.py`)
Eight ideas were scored for five viewers (a UK Muslim who prays, a revert, a parent, a madrasa student, a casual scroller) on watching to the end, trying Rafiq, wanting Complete, clarity and respect:
- **Your salah / Pray along** was the strongest to watch (2.56/3) and to try (2.30).
- **What's in Complete** did most to make viewers want to pay (2.43).
- **How Rafiq works** made viewers the most likely to try it (2.34).
- **The problem ad** (the owner's "Meet Rafiq") scored mid-table. The owner's opening, "Struggling to learn Arabic? Meet Rafiq.", was the weakest and most cheesy hook (1.34, cheesy 0.77). "Learnt Arabic words, then forgot them a week later?" was the strongest (2.07).
- **Not made:**
  - the AI tutor on its own (least clear, 1.26, and not live yet);
  - a series of five section shorts (clearer, but lower on watching).
- **Format:** vertical at 20–45s (2.60–2.63) beat landscape (0.70).

## The scripts (TypeSafe, `tools/typesafe-exp/videos_v9_scripts.py`)
Every line was checked for truth against the app's facts, clarity and cheesiness, and the weak ones were rewritten:
- "five minutes a day" became "a few minutes a day", because steps take 5–10 minutes (true 0.47 → 0.85).
- "Press Continue. That's it." became "Every day, just press Continue. رَفِيق knows what comes next."
- The tutor and Why? lines were merged, since the Complete video felt a bit long.
- Sheikh al-Husary isn't named and no Quran recitation is played. The Pray along shots use a prayer phrase in the app's own voice.

The review scene shows the app's real review gaps: a new word remembered each time comes back after 3 days, 2 weeks, 2 months and 6 months (fsrs.js with progress.js's settings), and a word you forget comes back tomorrow.

## Look and sound
- **Layout:** 1080x1920. The spoken line appears as a caption at the top, for viewers with the sound off. Below it, the real app sits in a phone frame that runs off the bottom of the frame so the text is readable. The screens were captured from the app at phone size (`shots/`).
- **Designed scenes:**
  - the three words of ruku with their meanings;
  - word cards that blur away;
  - Meet Rafiq;
  - the review gaps;
  - the ending, with rafiq-arabic.com.
- **Voice:** ElevenLabs, the same narrator (Sarah) and Rafiq voice as v7/v8 (`tools/v9-12-lines.json`).
- **Sound:** v6's fountain and birdsong, a pen stroke on the opening red ink line, and page turns and taps. No music.

## Storyboards (voice line → what's on screen)
**v9 Your salah (23.5s)**
1. "Imagine understanding every word of your salah." → سُبْحانَ رَبِّيَ الْعَظِيمِ, with each word's meaning appearing.
2. "It starts with the words you say most in every prayer." → Most-said words, word by word, then Pick the meaning.
3. "Then each part of the prayer, word by word." → Rising from bowing, then Your salah.
4. "And Pray along takes you through a whole prayer, lighting up each word as it's said." → Pray along, with the words lighting up (real frames).
5. "Your salah, in رَفِيق." / "Try it free for a week at rafiq-arabic.com." → the ending.

**v10 What's in Complete (26.6s)**: the Complete plan card → Pray along → the Tutor tab (a question and its answer) → a wrong answer, Why?, and the explanation → Real-life scenes and At the masjid → Practise, zooming in on the Weak-spots review → the ending.

**v11 How Rafiq works (43.3s)**: Home → Continue (tap) → the alphabet → a new word → the conversation → How it works → word tiles → the review gaps → Practise → Your salah → the ending.

**v12 Meet Rafiq (22.1s)**: three words blur away ("one week later…") → Meet Rafiq → a new word → the conversation → the review gaps → the ending.


## Second cut (owner feedback, 30 Sep 2026)
The first cut was too fast, showed too little of the features, cut screens off at the phone's edges, and the owner didn't like the narrator's voice. What changed:
- **Voice:** Sara (ElevenLabs jAAHNNqlbAX9iWjJPEtE), at speed 0.92 (`tools/v9-12-lines-sara.json`).
- **Pace:** about 1 second after every line. A demo that makes sounds (a word being said, a letter, a part of the prayer) plays after the line, so Sara never talks over the app. Any app sound under her voice is quieter. TypeSafe rated the scripts' pace 1.85–1.94 out of 2, where 2 means right; the first cut scored about 0.9 (`tools/typesafe-exp/videos_v13_scripts.py`).
- **Live:** `capture.py` drives the real app and saves a frame at every change with its real timing, plus the app's own sounds. On screen:
  - a tile sentence built and marked right;
  - a spelling bee word typed on the Arabic keyboard;
  - a question typed to the tutor, with the answer appearing;
  - a wrong answer, then Why?;
  - a reply typed in a real-life scene, then "Good reply";
  - the salah count growing from 24 to 138 of 238;
  - Pray along lighting up each word.
- **Features:** the ones TypeSafe found make people most want to pay (`videos_v13_features.py`: Pray along, the salah features, the tutor, weak spots, scenes). Also every part of Your salah and the spelling bee, which the owner asked for.
- **Phone:** always fully in frame. The only zoom is one gentle move onto a most-said word.

| Video | Length | Features shown working |
|---|---|---|
| v12 Meet Rafiq | 45s | new words, the most-said salah words, Pray along, the tutor, the review gaps |
| v9 Your salah | 63s | most-said words, the two drills, the parts, the tashahhud, the count growing, Pray along |
| v10 What's in Complete | 48s | Plans, Pray along, the tutor, Why?, a real-life scene reply, the weak-spots review |
| v11 How Rafiq works | 69s | Continue, the alphabet, new words, the conversation, a grammar note, tiles, the review gaps, the spelling bee, Your salah |

## Third cut (30 Sep 2026): the owner's notes on the second
- **Pace a little faster:** a 0.5s pause after each line (was 0.9), 0.2s after each demo (was 0.35), 0.7s before the first line (was 0.9). An "after" demo now starts as Sara's line ends, not 0.15s later. The idle stretches are trimmed: the quiz's wait before the first pick, and Pray along's long "Now repeat" at the end. Sara still speaks at 0.92, since re-recording at 0.97 wasn't needed. Lengths: v12 43s (was 45), v9 59s (63), v10 46s (48), v11 66s (69).
- **More background sound:** the fountain (22s) and birds (15s) used to stop partway through every video, which is where it went quiet. They now loop under the whole video, a little louder (0.2 and 0.15, were 0.12 and 0.08), over a soft low room tone (`ambience()` in build.py). The bed is about 5–6 dB louder on average and stays about 20 dB under Sara. Still no music.
- **The page fits the phone:** the most-said words shot (v9) no longer zooms in 1.3×, which had pushed the page past the phone's edges. It was the only zoomed shot.

## Before posting
- v10 shows the AI tutor, and v9, v10 and v11 show Your salah. Post them only once both are live: the Claude key (#154), and the teacher's sign-off for Your salah (#98).
- The tutor's answers on screen are ones I wrote for the demo, matching what the tutor is told to do. Check them the next time a teacher reviews.

Build: `python3 brag-output-v9-12/build.py`, then `npx hyperframes check` and `npx hyperframes render -o ../brag.mp4` in each `brag-output-vN/composition`.
