# How to make Rafiq videos (brief for a collaborator's Claude, 15 Oct 2026)

You're making short videos (TikTok / Instagram Reels) for Rafiq, an app that teaches Muslims the Arabic of their salah and
everyday Arabic. The owner has settled on ONE format that works. Make only that. Read this whole file, then the files it names,
before you build anything.

## 0. Setup
- Repo: `github.com/sal716eh-spec/Rafiq`. Work on the **`wip`** branch only. **Never commit or push to `main`** (it's the live site;
  the owner merges on set days).
- Read first, in this order: `CLAUDE.md` (project rules), `brag-quiz/FORMATS.md` (**"The standard for EVERY video"** and the
  checklist "Before sending any video"), `brag-quiz/MOTION-STYLE.md`, `brag-quiz/VIDEO-STYLE.md`, `brag-quiz/IDEAS.md` (how we
  post, what's made, what to avoid; make its unmade ideas first and add what you make to its "made" list).
- If `graphify` is installed, run `graphify update .` and use `graphify query "<question>"` to find things.
- Every piece of work gets a GitHub issue on the repo (labels `priority: before launch` / `next` / `later`); close it with what changed.

## 1. The format (copy it, change the words)
Reference video: **`g4-past-i`** = `g4()` in `brag-quiz/build_formula.py`. Every video has:
1. **A spoken clickbait hook in Callum's voice**, on screen from frame 0. It opens with ONE shouted word that **slams** onto the
   screen (crash, screen shake, shockwave, flash: the `"loud"` mark in `hook_in()`), then the promise. Vary the sentence, keep the
   shape: "MOST people learn Arabic for years before they notice this trick!", "MOST of you will get the second one WRONG!",
   "ONLY 1 in 10 get the last one", "NOBODY told you this about your salah".
2. **Words appear one at a time** as they're said (timings come from the audio), swooshing in from alternating sides.
3. **The page never stands still**: numbers count up in the background, a timer or counter ring for the key number
   (`hook_in` takes an optional `(label, count)`, e.g. `("YEARS", 7)`, `("QUESTIONS", 2)`).
4. **A click on every tick** of a timer, counter and the **3-2-1** countdown (never 5).
5. **Callum voices everything in English** (the questions, the rule, the ending); **Rafiq's voice says only the Arabic**, brought
   up to Callum's level with `say_up()`.
6. **The ending asks for a comment and is heard in full** ("How many did you get? Zero, one, or two? Comment down below!").
7. Hook page in **Fredoka**, our colours only, motion as in `MOTION-STYLE.md` (every move on its word, one continuous page per moment).

Next improvement to build into quizzes (issue #257): a **rehook at ~8 s** ("Only 1 in 10 get the second one right", slammed like
the hook), a second one after the first reveal, and a 1/2 → 2/2 counter. Viewers drop off around 10 s.

## 2. The video types (all in `brag-quiz/build_formula.py`; add a function, register it in `ALL`)
| Type | Copy | Function |
|---|---|---|
| Word-change quiz (if X is "he wrote", what's "I wrote"?) | `g4()`, `i4q()` | `change(..., hook=..., vo=...)` |
| Difficulty ladder (7 questions, 90% → 5% rail, owner stitches under it) | `l1()` | `ladder()` |
| One word traced to its root (weekly series, owner stitches under it) | `n1()` (Jannah), `j1()` | `root_video()` |
| A salah line word by word | `w8()` | `wbw()` |

- **Ladder difficulty must be real**: order words by the Kelly list's CEFR levels for Arabic (ssharoff.github.io/kelly,
  `ar_m3.xls`), sanity-checked by hand (it ranks by news frequency, so shop words like رَخِيص come out too hard).
- Stitch formats (`ladder`, `root_video`) keep everything in the **top ~1,150 px**: the owner films himself under it.
- **Talking-head footage** the owner sends: use the `edit-reel` skill (`.claude/skills/edit-reel/SKILL.md`, template
  `brag-quiz/reels/template/`): flicker hook, titles behind the head, kinetic captions, booms and crashes on key words.
  Latest reference: `brag-quiz/reels/salah-20/`.

## 3. Voices (ElevenLabs, through a GitHub Action; the key is a repo secret, never in code or chat)
1. Write a lines file, e.g. `brag-quiz/voice/<id>-lines.json`:
   ```json
   [{"file":"h1","voice":"N2lVS1w4EtoT3dr4eOWO","model":"eleven_v3","stability":0.0,
     "text":"[shouting] MOST! [normal] of you will get the second one... [shouting] WRONG!"},
    {"file":"q1a","voice":"N2lVS1w4EtoT3dr4eOWO","stability":0.35,"style":0.45,"speed":1.05,"text":"If this means 'grandfather'..."}]
   ```
   - **Callum** `N2lVS1w4EtoT3dr4eOWO`: the hook with `eleven_v3` + `[shouting]` tags, stability 0 (make 2-3 takes, keep the best);
     other lines stability 0.35, style 0.45, speed 1.05 (see `brag-quiz/voice/i4-vo-lines.json`).
   - **Rafiq** `Ywuz3KyW2N5pqKNpwcCL`: Arabic only. Use the app's own recordings where they exist (`audio-manifest.json`), new
     words via a lines file (stability 0.5-0.6, style 0-0.1, speed 0.9).
   - **Words ending in a doubled letter (ّ)**: ElevenLabs adds an "-a" (جَدّ came out "jadda"). Write the end with a sukun
     instead (جَدْ, حارْ, جِنْ) and **have the owner listen** before using it (issue #258).
2. Commit and push the lines file to `wip`, then run the **eleven-voices** workflow (Actions → eleven-voices → Run workflow, branch
   `wip`): command `speak`, args `brag-quiz/voice/<id>-lines.json|brag-quiz/voice/<id>|no`. It commits the mp3s back to `wip`; pull.

## 4. Build, render, check
```
python3 brag-quiz/build_formula.py <id>
cd brag-quiz/out/<id>/composition && npx -y hyperframes@0.8.153 render --crf 10 -o ../<id>.mp4 && cd -
python3 brag-quiz/build_formula.py <id> --level
```
Then, before sending (the full list is in FORMATS.md "Before sending any video"):
- `python3 brag-quiz/check_frame0.py <mp4>`: frame 0 must not be blank (it's the cover).
- Loudness about **-16 LUFS** for quizzes, peak under -1 dB. If hot: re-encode the audio through
  `aresample=192000,alimiter=limit=0.8:level=disabled:attack=0.5:release=50,aresample=48000`, AAC 256k, video copied.
- No silent gaps (`silencedetect=n=-50dB:d=0.25`), and **transcribe it** (faster-whisper) to prove every line, the ending
  especially, is heard in full.
- Look at frames from every section (a contact sheet) for overlaps and blank moments.

## 5. Sending and posting
- What you send must be **ready to post**: quizzes at `--crf 10`; anything over the 30 MB chat limit as HEVC two-pass
  (`-c:v libx265 -tag:v hvc1`), never an H.264 squeezed to fit. Full quality also to the owner's Drive:
  `python3 tools/drive-upload.py <file>` (needs `GDRIVE_*` in the environment) and send the link.
- **Caption**: test 3-4 options with TypeSafe (copy any `tools/typesafe-exp/*_caption.py`, e.g. `ladder_caption.py`), pick the
  best total. Rules learned: the caption **adds** to the video (a fact, a source, a related word), never repeats it; don't repeat
  the shouted hook in writing (it reads as clickbait); give the answers away nowhere; a share ask works ("send this to who
  you're going to Jumuʿah with" got 6x the shares); the ladder's percentages are a game, never stated as data.
- About 4 posts in 5 are pure content; 1 in 5 mentions the app (free week, no card needed, link in bio).
- Max 1-2 TikTok posts a day, never the same video twice.
- Commit the build function, the voices and the finished mp4 to `wip`, and add the video to `IDEAS.md`'s made list.
