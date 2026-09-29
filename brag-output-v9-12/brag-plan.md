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

## Before posting
- v10 shows the AI tutor, and v9, v10 and v11 show Your salah. Post them only once both are live: the Claude key (#154), and the teacher's sign-off for Your salah (#98).
- The tutor's answers on screen are ones I wrote for the demo, matching what the tutor is told to do. Check them the next time a teacher reviews.

Build: `python3 brag-output-v9-12/build.py`, then `npx hyperframes check` and `npx hyperframes render -o ../brag.mp4` in each `brag-output-vN/composition`.
