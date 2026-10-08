# Reel template

Turns one talking-head clip into a finished reel in the house style (`brag-quiz/VIDEO-STYLE.md`):
silences cut, grade, titles behind the speaker, gold pops and punch-ins on stressed words, a split frame, a flicker,
sound effects, and clean, loud-enough audio.

```
W=/tmp/reel-NAME                      # a working folder per video (big files: keep it out of the repo)
python3 reel.py $W fetch DRIVE_FILE_ID
python3 reel.py $W words              # read the transcript: what to keep, where the sections start
python3 reel.py $W cut                # check the printed transcript: no word clipped
python3 reel.py $W base
python3 reel.py $W plan               # draft config.json, then edit it (below)
python3 reel.py $W zoom
python3 reel.py $W masks              # slow: about a second a frame, only where titles sit
python3 reel.py $W layers             # slow: two screenshots a frame
python3 reel.py $W mix                # → $W/reel.mp4
```

## Filling in `config.json` after `plan`
Times are in the cut (`cutwords.json`).
- `titles`: `[start, end, "SMALL LINE", "BIG WORD", size px]`, one per section of the script (about 240 px for long words, 320 for short).
- `caps`: the third value of each word is `true` for a gold pop. `plan` guesses by loudness. Keep the words that matter to
  the script and drop fillers like "Number".
- `punch`: `[word start, word end]` for the single punch-ins, the 6 to 9 biggest moments (not inside a flicker).
- `split`: `[start, end]` for the three-strip app frame. Use `null` for none.
- `flicks`: `[[start, end, "TITLE", size], ...]`: the flicker. Always one at 0 as the hook (2-3 s, under the first line),
  usually one at the end, and one wherever the camera angle changes. Its clips are the speaker's own footage plus app screens.
- `steps`: `[[[word starts], end], ...]` where a phrase counts or builds ("these · three · things"): one zoom level per word.
- `sections`: `[[start, end], ...]` where each slow push restarts. This is usually each title.
- `broll`: which of the app's recordings (`brag-output-v9-12/clips/`) go in the split and the flicker.

After editing the titles or captions, rerun `masks`, `layers` and `mix`. Changing only the sound needs just `mix`.
Sound rules and levels live in `sfx_rules.py`.

Needs: ffmpeg, faster-whisper, rembg, numpy, Pillow, playwright (Chromium is preinstalled).
Example: `reels/3-things/` is the first reel made this way (v3).
