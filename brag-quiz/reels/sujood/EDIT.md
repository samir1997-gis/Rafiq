# Editing the sujood reel (18 Oct 2026, #263)

Footage (Drive, the owner's): `subhana.mp4` (1E7abPEJN55i1h_Ok6GsYnmS6_oFFJw3N, the talking head, already cut by him, 91 s)
and `DJI_20261018181326_0042_D.MP4` (1ksEtTdrGxpNARGlvUBoqXgdzDSaYkZhK, B-roll: sitting 2-8 s, down 9 s, sujood 10-14 s, up 15 s, sitting 16-20 s).

The owner's rules: **no cuts, no trims, the voice as recorded** (no cleaning, no gain). So `cut` is skipped (one chunk, the whole
clip) and the mix is `mix keepvoice`. Everything else is the template, in the ruku reel's style.

```
W=/tmp/reel-sujood; R=brag-quiz/reels/template/reel.py
cp subhana.mp4 $W/clip.mp4; python3 $R $W words
echo '[[0.0, 91.367]]' > $W/chunks.json; python3 $R $W base nologo      # no watermark on his export
# B-roll over the picture while he keeps talking (graded with template/grade.txt, 1404x2496):
#   7.68-13.14 sujood (B-roll 8.7 s on) · 34.78-39.18 sitting up (15.0 s on) · 70.32-74.38 sujood (10.0 s on)
# → overlay onto cut.mov's picture, audio copied (see the ffmpeg command in the session notes)
# flicker/split frames: broll/sujood (11 s, 3 s), broll/sit (3 s, 3 s), broll/sujoodcut (9 s, 6 s), broll/sitcut (15.2 s, 4.8 s)
python3 $R $W plan; (cd $W && python3 brag-quiz/reels/sujood/mkconfig.py)
python3 $R $W zoom; python3 $R $W masks; python3 $R $W layers; python3 $R $W mix keepvoice
```

## v2 (owner's notes, 18 Oct 2026)
- The sitting B-roll stops at 18.6 s in DJI_..._0042 (he reaches for his phone after): cutaway 34.78-38.38 from 15.0 s.
- Two slips fixed with his re-recording (Drive 1SciSENQqFuHFUE_SELk5xhFVY9GmWPNV, wider framing): "al-a'la" (fix 17.93-19.12 s)
  replaces 25.0-26.6, "ighfir li" (fix 28.40-29.53 s) replaces 41.85-43.15. Both fit the original gaps, so no timing moves.
  The re-recording's picture is cut in for those moments (lips match), graded and cropped 1/1.22; its sound is raised 2.3 dB
  to match his voice in the reel (speech RMS). Nothing else in the voice is touched.
- v3 (owner): the re-recording's picture didn't match (framing, light), so the original picture stays and only the two words' sound is swapped.
- v4 (owner): "the Most High" (5.58, 27.12, 33.48) is a zoom step and a hit per word with a boom under "High" (`steps`); the hadith
  he quotes gets a panel 69.0-74.4 with its Arabic, English and source (Sahih Muslim 482); frame 0 is no longer a white flash
  (template fix in layers.html: the opening flicker starts on the speaker).
- v5 (owner asked to check SFX sync): sounds were placed exactly (±25 ms) but on whisper's word times, up to 0.6 s off in the
  slow Arabic. Every word now sits on its forced-aligned start (`wordtimes.json`, torchaudio MMS_FA, 40 ms early), checked
  by plotting the voice at 18 key moments; captions hidden under a panel no longer tap (template `sfx_rules.py`).
- v6 (owner, 23 Oct 2026): 1.25x speed and 5% closer; the red flicker opening (0-2.6 s) replaced with hook idea 3, "one flash, one hit":
  his talking shot from subhana.mp4 (graded and pushed as the master), "AT YOUR" behind his head from frame 0, "LOWEST" slamming
  down on the word with one white flash and one boom (n03). His voice untouched (owner: don't raise the volume). `hook3.py`.
  The sujood B-roll (DJI_..._0042) is no longer on Drive (404), so hook idea 1 (a cold open on the sujood) needs it re-uploaded.
