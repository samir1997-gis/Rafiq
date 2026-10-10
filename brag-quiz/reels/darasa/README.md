# Darasa reel (the owner's Osmo Pocket 3 clip), how it was made

Source: the owner's 2:26 recording (Google Drive); not committed. Output: a 37 s reel.

1. `edl.py`: the best take of each line (the repeats and slips dropped), silences over 0.4 s cut (faster-whisper words + ffmpeg silencedetect) → `chunks.json`.
2. `base.py`: each piece cut on its own (seeking keeps memory low), cropped so the DJI watermark is gone, light grade, then the punch-in zooms from `zoom.py`; 1.4 s held at the end for the end card.
3. `sfx.py`: whoosh, swish, ping, ding, bell, boom, pop, tick, riser, synthesised (numpy/scipy), so nothing needs a licence.
4. `overlay.html` + `render.py`: the motion graphics, drawn per frame in Chromium (Playwright) as transparent PNGs:
   hook sticker, "WORD" and "HE" bubbles at the raised hand, CHANGE letters cycling the six colours, the class banner,
   a person tracker (أنا … نحن) that lights up, a card per person (prefix letter in its colour; tadrusīna and the "she" card
   drawn in as the hand sweeps), WE burst, the six-row summary, end card; Luckiest Guy captions with coloured word boxes.
5. `mix.py`: the effects ducked under the voice (sidechain), loudness about -14 LUFS, composited.

For a new clip: transcribe, pick the takes in `edl.py`, look at the gestures (frame sheets), set the times in `overlay.html` and `mix.py`.

## Version A (the one the owner chose)
`overlay_light.html` is the reel in Rafiq's own colours (paper, ink, verdigris, rubric; Karla and IBM Plex Sans Arabic; the changing letter always red), with calmer motion.
`mix_light.py` uses the owner's own sound effects (his recording, split into 11 sounds, not committed), at about half the earlier volume and ducked under the voice.
