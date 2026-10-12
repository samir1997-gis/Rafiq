# Our video formats (the owner's rule, 11 Oct 2026: when a format works, copy it exactly)

Every generated video uses one of these, built by the named function. Don't redesign a format that works; change the words.

| Format | Copy this | Build with | Proof it works |
|---|---|---|---|
| **One word traced to its root** | `j1-jumuah` | `root_video()` in `build_formula.py` | Jumuʿah: 1,433 IG views, 73 shares, 38% hold (day 1) |
| **A salah line, word by word** | `s3-samiallahu`, `f1-sujood` | `wbw()` in `build_formula.py` (build_series with the bed on) | Sujood: 1,729 IG views; Sami'a: 1,301 |
| **Word-change quiz** (we / she / past / plural) | `v3-drink` (Ashrabu) | `change()` in `build_formula.py` | Ashrabu: 2,007 IG views, 31 saves |
| **Salah word quiz** (what does it mean, 5-second countdown) | `q1-samia` | `build_quiz.py` + `quizzes.json` | 19 s average watch on a 17 s video (replays) |

What didn't work, so don't make more without a new idea: timed challenges on everyday words on TikTok (speed reading x2,
"3 seconds to answer", the POV chat: all stalled at 260-300 views). The speed reel did fine on Instagram (1,990 views).

## The standard for EVERY video (owner, 12 Oct 2026; on trial, judged over a few videos, not the first)
Reference: **`g4-past-i`** (trial tracked in #254) (`g4()` → `change()` + `hook_in()` in `build_formula.py`). Every video we make from now on, of any
kind (quiz, root, salah line, data reel, carousel-to-video, edits where it fits), uses all of this; no video goes out without it.
1. **A spoken hook in Callum's voice** (`N2lVS1w4EtoT3dr4eOWO`): a bold, curiosity-first line the video pays off, on screen
   from frame 0. Rafiq's voice (`Ywuz3KyW2N5pqKNpwcCL`) only says the Arabic.
2. **One word stressed, hard.** Spoken shouted (ElevenLabs `eleven_v3`, `"[shouting] MOST!"`, `stability` 0), in capitals on
   screen, huge on frame 0, then it **slams** down on the voice: crash (`brag-quiz/sfx/crash.wav`), screen shake, shockwave
   rings, sparks, flash, squash (`marks` `"loud"` in `hook_in`). Other key words: red, or a gold hand-drawn circle with a flash.
3. **Words come on one at a time** as they're said (word timings from the audio, `words_at()`), swooshing in from alternating
   sides with blur and a soft swoosh; a whip with a swoosh between sections.
4. **The page is never still**: numbers that fit the line count up all over the background (`HOOK_NUMS`), and a counter or
   timer ring for the key number.
5. **A sound on every count**: a clear click (`brag-quiz/sfx/ref/click.wav`) on every tick of a timer or counter and on
   every countdown second (`count_down()`); the countdown stays **3-2-1**.
6. **Voiceover all the way through** (Callum): the question asked around the Arabic word, the rule, and a closing ask that
   invites a comment ("How many did you get? Zero, one, or two? Comment down below!"), **heard in full** before the end.
7. **Rafiq's voice level with Callum's**: the app's recordings go in with `say_up()` (about -19 LUFS), never plain `c.say()`.
8. **The hook page font is Fredoka** (round, bubbly; `brag-quiz/fonts/`), our colours always.
9. **Then the checklist below**, as always (frame 0, -16 LUFS, the bed, no silences, preview sheet, TypeSafe, share line).

## The root format, exactly (from j1-jumuah)
1. **0-6 s:** the hook question ("Why is Friday called الجُمُعَة?") with the big word on screen from the first frame; the root
   letters turn red; "ج م ع = to gather"; **the payoff line answers the hook by about 4 s** ("The day of gathering.").
2. **7-12 s:** "Once you see it, it's everywhere:" **two** related words, each with its meaning and a line on why it matters.
3. **12-20 s:** "Your turn": one more word, the root as a hint, 3-2-1, the answer, then a **"Send this to …" ask** that fits the moment.
4. End card. About 25 s. The fountain bed underneath.

## Before sending any video (the mistakes we've made)
- [ ] **It copies the format above**, not a variation (a1-adhan skipped the payoff and the second section and did a third as well).
- [ ] **The fountain bed is on.** It's one file, `brag-output-v6/composition/assets/sfx-gen/fountain.mp3`, added by
      `Comp` in `build_teach.py` (volume 0.1, looped to the video's length). **Never pass `bed=False`**:
      `build_series`, `build_ten` and `build_social` default to off, and `build_formula2`, `build_mix` and `build_wild`
      switch it off. Use `wbw()` / `change()` / `root_video()`, or `Comp(..., bed=True)` / `c.bed = True`. Check:
      no stretch of the finished video is silent (`ffmpeg -af silencedetect=n=-50dB:d=0.25` finds nothing).
- [ ] **Loudness about -16 LUFS** (`--level`, or loudnorm for `build_quiz.py` videos).
- [ ] **Every Arabic word is voiced**: the app's recording, or an ElevenLabs line in the Rafiq voice (`Ywuz3KyW2N5pqKNpwcCL`,
      `brag-quiz/voice/*-lines.json`, run the "ElevenLabs voices" workflow with `speak`).
- [ ] **A preview sheet checked** for overlapping text, missing glyphs (ﷺ needs the Arabic font; × isn't in Anton) and wrapping.
- [ ] **The caption never gives the answer away** (a1's "right next to your eyes 👂" did) and repeats the hook question.
- [ ] **A share line** on screen and in the caption ("Send this to …").
- [ ] **When to post**: tie it to its moment (Jumuʿah on Friday morning, the adhān at Fajr, Ramadan words in Ramadan).
- [ ] **Cover = the first frame** (the question), never the end card.
- [ ] **Frame 0 is never empty**: the question and the big word are on screen from the very first frame, nothing fades in from
      blank. Run `python3 brag-quiz/check_frame0.py <video>.mp4` on every video before it goes in the folder; it must say `ok`.
      (q4-azim opened blank and most TikTok viewers left at 0:01; on 12 Oct 12 of 23 scheduled videos did the same.)
- [ ] **Captions checked with TypeSafe** (`tools/typesafe-exp/`).
- [ ] **A spoken hook** (owner, 12 Oct 2026): a bold, curiosity-first opening line ("Most people learn Arabic for years before they
      notice this trick"), on screen from frame 0 and spoken in the hook voice, **Callum** (`N2lVS1w4EtoT3dr4eOWO`, ElevenLabs);
      the Rafiq voice stays for the Arabic. The line can tease, the video must pay it off. `change(..., hook=(words, marks, mp3))` (`hook_in`) in
      `build_formula.py` does it for the word-change quizzes.
- [ ] **Moves like `MOTION-STYLE.md`**: voice-led, every move on its word, our colours (never the reference's).
- [ ] **The last line is heard in full**: transcribe the last 7 s of the finished video (faster-whisper) and check every word of
      the closing ask is there (g4's "Comment down below!" was cut off on 12 Oct because the end card was shorter than the line).
- [ ] **A click on every countdown second** (`count_down()` in `build_formula.py`); the countdown stays 3-2-1.
