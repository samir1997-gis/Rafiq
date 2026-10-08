# How Rafiq videos look (the owner's rule, 7 Oct 2026)

Every video we generate or edit follows this. The reference is a reel by @kalylsfilms ("my 3 go-to edits"):
clean, crisp, vibrant, slick and elegant. Not busy: the effects come in short bursts between calm talking shots.

## The look
- **Grade:** rich colour, deep blacks, warm skin, slightly cool shadows, gentle vignette, a little sharpening.
  Starting point (ffmpeg): `eq=contrast=1.1:saturation=1.12:gamma=1.08,curves=r='0/0 0.3/0.31 0.7/0.74 1/1':g='0/0.01 0.3/0.31 0.7/0.71 1/0.99':b='0/0.05 0.3/0.32 0.7/0.68 1/0.95',vibrance=intensity=0.2,unsharp=5:5:0.45,vignette=PI/6`.
  Footage shot in D-Log M needs a stronger lift first. Never darken faces.
- **Colours:** Rafiq's own: rubric red (#C8372D on video, #B4322A in the app), gold (#E9B949), paper (#F1ECE0), ink (#17262B), verdigris (#2E7263).

## Type (fonts in `brag-quiz/fonts/`, all open licence)
- **Titles:** Anton (tall, narrow capitals), big, in red or gold, stacked in two or three lines of different sizes.
- **Arabic titles:** IBM Plex Sans Arabic bold, huge, the key letter in red.
- **Script accent** over a title, sparingly (one word).
- **Captions:** Instrument Serif, small and elegant, white with a soft shadow, mid-frame, two or three words at a time.
  No big bubbly caption boxes.
- Karla stays the app's font; videos use the above.

## The three signature edits
1. **Text behind the person (masking):** the title sits between the background and the speaker, so the head covers
   part of it. Cut the person out per frame with rembg (`u2net_human_seg`), layers: graded background, title, graded person.
2. **Split frame:** for a few seconds the screen splits into three stacked strips of B-roll (mixing black-and-white
   and colour), the caption across them.
3. **Flicker in a frame:** a quick burst of clips flickering inside a bold red (rubric) border, a title over it. The hook.

## The edit
- Best takes only; silences and repeats cut; picture and sound cut to whole frames (see `reels/darasa/base.py`).
- Long, steady talking shots; gentle punch-ins on key words; effects in short bursts.
- Sound: a crisp effect on every visual change, heard over the voice, not ducked (rules below); loudness about -14 LUFS.
- Rafiq the character (`character/`) can answer beside the speaker or full screen.
- Captions follow the posting rule in `IDEAS.md` (reach first).

## Asking the owner to film
Sit low in the frame with about a third of the frame free above the head (for the titles); one soft light on the face
from the side; a darker room with a warm lamp behind; the DJI Mic; 4K, 24 or 30 fps, exposure locked on the face.
Plus 5-10 B-roll clips of 2-3 seconds (Quran pages, writing Arabic, prayer mat, masjid, the app on a phone).

## Learned on the first one (reels/3-things, 8 Oct 2026)
- **Cutting pauses:** cut only true silence (ffmpeg `silencedetect` at -40 dB, 0.4 s or more) and leave a 0.12 s breath
  either side. Tighter settings (-35 dB) clip the owner's soft word endings ("daily", "recall", the last sentence).
  Check every cut by transcribing it before rendering.
- **Titles behind the head:** with this framing the big title's top is about 240 px down, so the hair overlaps the
  bottom of the letters; higher up there's no depth.
- **Split frame over app footage:** the app is light, so dim the strips and put the caption on the darker middle
  (black-and-white) strip; hide the caption during the flicker (its title says it).
- **B-roll** until the owner films some: the app's own screen recordings in `brag-output-v9-12/clips/`.
- The DJI watermark: `delogo=x=90:y=600:w=780:h=110` on the 2160×3840 Osmo footage.
- **Audio:** the owner's recordings come in very quiet (about -37 LUFS). Never just compress and boost: that lifts the room
  hiss with the voice. Clean first (`highpass=80, lowpass=13000, afftdn=nr=18:nf=-66, agate` gentle, light compressor),
  measure, then one fixed gain to about -14 LUFS and a limiter (`reels/3-things/mix2.py`). Tell the owner to raise the
  DJI Mic's gain / check it's paired, so there's less to fix.
- **Emphasis (the owner's rule):** where he stresses a word, show it: the word pops in the caption in Anton, gold,
  larger; on the biggest moments the scene (him + the title) punches in about 10%, holds through the word and eases
  back. Find stressed words by loudness against the words around them, then keep the ones that matter to the script.
  Keep titles narrow enough to survive the punch-in (about 240 px for long words).
- **Sound effects (learned from the owner's reference breakdown, `reels/template/sfx_rules.py`):** every visual change
  gets a short, crisp sound that's heard, never pushed under the voice (no ducking), and never the same sound twice
  in a row (each moment rotates through the reference sounds and the owner's n01-n11):
  title lands → shutter / pop · text line → tap / tick · stressed word → tap / tick / ping / click · punch-in → swoosh ·
  stepped zoom → a hit on every step, the last heaviest, with a low boom · big transition → charge landing on the cut + boom,
  swooshes as the strips slide in · flicker → flash + whoosh, a flicker sound on every clip switch, swoosh + shutter on the
  wipe out · "RAFIQ" → sparkle + ding.
  Level each sound by its loudest 50 ms, not its peak: clicks and shutters are spiky, so a peak target leaves them 10-20 dB
  under the voice (v3's mistake). Targets: hits -16, swooshes -14, taps and flickers -19 dBFS against a voice at about -17.
- **The flicker is the hook (owner, 8 Oct 2026):** open every reel with it (the first 2-3 s, under the first line), and use it
  again at the end and wherever the camera angle changes. A new clip every 8 frames inside the red frame, each switch a
  white flash and one frame flicking back to the last clip; the speaker's own footage (tight, black-and-white, medium crops)
  mixed with app screens, which alone all look alike; the caption keeps running over it; it ends on a circle wipe.
- **Stepped zoom (owner):** when a phrase counts or builds ("these · three · things", "every · single · day"), zoom in one
  level (7%) on each word, with a sound on each, then ease back.

## The template: any new clip
`brag-quiz/reels/template/` does all of the above. See its README.
