# The Drive-folder videos, recreated in the proven formats (#246)

The owner's folder held 14 files. Each was checked against `FORMATS.md` and `IDEAS.md`:
- Five are rebuilt below.
- The rest are skipped:
  - **p4-hamd:** a second ح م د video; `r2-muhammad` is the one.
  - **p2-ana:** the same "أَ = I" aha as v3 Ashrabu.
  - **i4-ta-marbuta:** `g2-female` covers ة.
  - **m08-day1, m05-typing, brag, Rafiq-ad:** no proven format.
  - **r2-muhammad:** already in the root format.

| Video | From | Format (builder) | Length | Loudness |
|---|---|---|---|---|
| `out/r3-akbar/r3-akbar.mp4` | p1-akbar | root, like j1 (`root_video`) | 25.5 s | -16.6 LUFS |
| `out/r4-insha/r4-insha.mp4` | p5-insha | root, like j1 (`root_video`) | 25.5 s | -16.9 LUFS |
| `out/g4-past-i/g4-past-i.mp4` | v1-go + v2-write | word-change quiz, like v3 (`change`) | 23.8 s | -16.5 LUFS |
| `out/w8-subhana-azim/w8-subhana-azim.mp4` | t2-subhana | word by word, like s3 / f1 (`wbw`) | 12.1 s | -16.3 LUFS |
| `out/q3-sujood/q3-sujood.mp4` | q3-sujood | salah word quiz (`build_quiz.py`), only re-levelled (was -28.8) | 17.0 s | -16.3 LUFS |

## Checklist
- **Format:** each copies its format's layout and order; only the words changed.
  - **One change, applied to every root and word-change video:** the hook and its Arabic word are now on screen from frame 0, so the cover is the question, not a blank fade-in.
- **Sound:** the fountain bed is under every video.
- **Every Arabic word is voiced:** with the app's recordings, plus تَكْبِير, كِبار and مَشِيئَة in the Rafiq voice (`voice/recreate-lines.json`, spoken by the ElevenLabs workflow).
- **Loudness:** about -16 LUFS. The true peak sits at -0.8 dBFS, so the three longer ones land 0.5-0.9 LU under -16.
- **Preview sheets checked:** no overlapping text or missing glyphs. In r4, ما شاءَ اللهُ is kept on one line.
- **Length:** 15-26 s, except **w8 at 12.1 s**. The word-by-word format is that length (f1-sujood 11.4 s, w5 11.5 s, s3 13.9 s).
- **Captions:** they repeat the hook, don't give the answer, and include a share line. Checking them with TypeSafe is still to do (no key in this session): `TYPE_SAFE_KEY=... python3 tools/typesafe-exp/recreate_captions.py`.
- **Teacher, please glance at:**
  - أَكْبَرُ as "greater than everything"
  - كِبار "grown-ups"
  - تَكْبِير "saying Allāhu akbar"
  - ش ي ء "to will", with شَيْء "a thing" from the same root
  - مَشِيئَة "will"

## When to post
- **w8 and q3:** near a prayer time (Asr or Maghrib). They pair with f1-sujood (post w8 after it: f1 asks "what do you say in rukūʿ?").
- **r3-akbar:** Friday after Jumuʿah, or any evening.
- **r4-insha:** any evening.
- **g4-past-i:** a weekday evening, around 7-8 pm UK.

All five are pure content (no link), keeping the 4-in-5 rule.

## Captions (option A of each; option B is in `tools/typesafe-exp/recreate_captions.py`)

**r3-akbar**: What does akbar in Allāhu akbar really mean? 🤍 Three letters, k-b-r, and you'll start seeing them everywhere, even in the takbīr. Try the last word before the 3 👇 Send this to whoever you pray with 🤍 #salah #allahuakbar #learnarabic #arabic #muslim #islam

**r4-insha**: What does in shā' Allāh actually say? 🤲 Three letters, sh-y-', and they're in mā shā' Allāh too. Guess the last word before the 3 👇 Send this to someone who says in shā' Allāh every day 🤍 #inshallah #mashallah #learnarabic #arabic #muslim #islam

**g4-past-i**: If kataba is “he wrote”, what's “I wrote”? ✍️ Three choices, 3 seconds. Then the same trick with “he went” 👇 0, 1 or 2? Send this to your Arabic study buddy. #learnarabic #arabic #arabicverbs #arabicgrammar #studyarabic

**w8-subhana-azim**: You say this every time you bow in rukūʿ. Do you know every word? 🤲 Subḥāna rabbiyal-ʿaẓīm, word by word. What do you say in sujūd instead? Comment it 👇 Send it to someone you pray with. #salah #ruku #learnarabic #arabic #muslim #islam

**q3-sujood**: In rukūʿ you say subḥāna rabbiyal-ʿaẓīm. What do you say in sujūd? 🤲 You've got 5 seconds 👇 Send this to someone you pray with. #salah #sujood #learnarabic #arabic #muslim #islam
