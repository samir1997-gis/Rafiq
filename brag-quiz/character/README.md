# Rafiq, the character (#230)

The logo tile, alive: no face. It shows feeling through motion, through the ر on it (which reshapes with its mood)
and through its red dot (which glows in time with its voice). Two small rounded hands; the word it teaches comes
out of it on a card and goes back the same way. Rafiq's own colours, light and dark.

**Why this one (TypeSafe, `tools/typesafe-exp/rafiq_character.py` and `_r2.py`, 0-3 averaged over five viewers):**
- Round 1, six ideas: the faceless tile won (9.36), ahead of the ر as a little figure (8.77), a cartoon teacher (7.76),
  the tile with eyes (7.42), a lantern (7.39) and a camel (5.22). The practising viewer who avoids pictures of faces:
  faceless tile 2.81 of 3, cartoon teacher 0.02.
- Round 2, making it likeable without a face: mood-shaped ر + word cards + small hands won (10.74, from 9.33);
  religiously still fine (2.46).
- Voice: "a calm, warm young British Muslim man, like a kind older brother" (brand fit 2.90); a cheeky voice scored 0.26.
  The ElevenLabs voice already on the account, `rafiq-voice` (Ywuz3KyW2N5pqKNpwcCL), is used.

**States:** idle, salam, talking, listening, thinking, teaching, well done, not quite (`rafiq.html`, `rafiq(state)`).
**Motion (apple-design skill):** springs, critically damped unless the motion has momentum (the hop, the wave, landing);
the card comes out of the tile and returns into it; the dot glows on the same frame as the voice.

**Files:** `rafiq.html` (the character, the sheet, the demo), `lines.json` + `voice/` (spoken by the ElevenLabs workflow),
`sheet.py`, `demo.py`, `segs.json` (the voice's loudness per frame, which drives the dot).
