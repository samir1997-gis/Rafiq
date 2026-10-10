---
name: edit-reel
description: Edit a talking-head video the owner sends (a Drive link or an upload) into a finished Rafiq reel with the owner's approved template. Use whenever the owner sends footage to edit, asks for a reel or a video edit, or says "edit this".
---

# Edit a reel (the owner's approved method, 8 Oct 2026)

Every talking-head clip goes through `brag-quiz/reels/template/reel.py`. Read `brag-quiz/reels/template/README.md`
and `brag-quiz/VIDEO-STYLE.md` first. Don't change the method unless the owner asks; their feedback is already built in.

1. Work in a folder outside the repo (e.g. `/tmp/reel-NAME`). Run `fetch` (Drive id) or copy the upload to `clip.mp4`.
2. Run `words`, then `cut`. Check the cut transcript: no word clipped, re-takes removed.
3. Run `base`, then `plan`, then fill in `config.json` from the transcript:
   - **Hook:** a flicker at 0 (2-3 s, under the first line), titled with the hook. Also one at the end, and one at
     every camera-angle change.
   - **Titles behind the head:** one per section of the script.
   - **Steps:** for counting or building phrases ("these · three · things").
   - **Punches:** the 6-9 biggest moments, with the gold pops on the words that matter (drop fillers).
   - **Split frame:** one, if the script has a list or a "how".
4. Run `zoom`, `masks`, `layers` and `mix`. Check stills at the hook, each title, the steps and the end, and
   measure the loudness: about -14.5 LUFS, true peak under -0.5 dBFS.
5. Send the reel to the owner with a short note, and write a caption by the posting rule in `brag-quiz/IDEAS.md`.
   Check the caption with TypeSafe.

The approved result is `reels/3-things` v5 (`config-v4.json`, rendered with the current template).
