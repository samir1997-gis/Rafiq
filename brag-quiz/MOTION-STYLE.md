# Motion graphics: how generated videos move (the owner's rule, 12 Oct 2026)

Approved on `q1-quran-count-v2` (`brag-quiz/reels/quran-count/build2.py`, the reference implementation: copy its helpers).
Learned from a reference reel the owner sent (a kinetic-type brand piece). **Take the style, never the colours or the exact
shapes**: our palette and our own graphics, always.

## The rules
1. **The voice drives everything.** A voiceover (since 12 Oct 2026: **Callum** `N2lVS1w4EtoT3dr4eOWO` for the English, the Rafiq voice `Ywuz3KyW2N5pqKNpwcCL` only for the Arabic; see "The standard for EVERY video" in FORMATS.md; one short line per beat in
   `brag-quiz/voice/<video>-lines.json`, spoken with the "ElevenLabs voices" workflow). Every move lands on the word that's
   said: take the word timings from the audio (faster-whisper, `timings()` in build2.py), never guess them.
2. **Something moves every half second to second.** Nothing sits still for more than about 1.5 s.
3. **One idea on screen at a time.** The old one leaves (up, with a fade) before the next arrives.
4. **The hook is still on frame 0** (it's the cover), whole and readable; its words lift as they're said.

## The moves (helpers in build2.py)
| Move | When to use it | Helper |
|---|---|---|
| **Page moves up**: the scenes sit down one tall page, the camera scrolls, motion blur on the way | a new section | `cam(scene, t)` |
| **Whip sideways**, motion-blurred | a quick change of thought, or setup → answer | `cam(scene, t)` with a scene to the right |
| **Blur-zoom in**: a word flies in big and blurred, then settles | words appearing one by one | `zoomin(sel, t)` |
| **Keyword glow**: the word turns teal (or gold, or red for "hard") with a soft halo and a small bump | the key word in a line | `glow(sel, t, colour)` |
| **Drawn underline / hand-drawn circle** in gold | the phrase that matters most (one per scene) | `draw(svg path, t)` |
| **Counter that rolls up and pops** | every number | `counter(sel, to, t)` |
| **Pills**: filled teal and outlined ink in turn, sliding in from alternate sides, stacking | lists, pairs, contrasts | `pop(sel, t, from-side)` |
| **Highlighter sweep** in gold behind a phrase | the answer to a question | the `.hl` scaleX tween |
| **Typewriter, then whip to the answer**, circled | the ending's payoff | the `#tw` tween + `cam()` |
| **Soft rings drifting** in the corners | the whole video, very faint | `.orb` |

## Look
- **Colours:** paper `#F1ECE0` background, ink `#17262B` text, verdigris `#2E7263` for emphasis and filled pills, gold
  `#A8842C` / `#E9B949` for numbers, circles and highlights, rubric red `#B4322A` rarely (one word like "hard?").
- **Type:** Karla bold for the words, Instrument Serif italic for the accent word in a line ("verses", "of them",
  "words."), IBM Plex Sans Arabic for Arabic.
- **Our own shapes**, e.g. the verses as dots in the eight-pointed star (۞), not the reference's grids or icons.
- **Ending** high on the screen (clear of the apps' captions): the site pill, "Free for a week · no card needed", the share ask.

## Sound
The voice, the fountain bed underneath (`build_teach.py`'s crossfaded loop, volume 0.1), a soft swoosh on each camera move
and a click on each pill or pop. Level to -16 LUFS. Everything in `FORMATS.md`'s checklist still applies.
