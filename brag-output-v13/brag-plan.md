# v13: Meet Rafiq, fast cut (#183)

v12 sped up after the owner's note: "Pick up the pace, it's still so slow and boring." 43s → 26s.
- Sara 15% quicker (atempo, same pitch); 0.1s between lines (was 0.5).
- The app demos play while she speaks, instead of a still frame until her line ends; app sounds under her a little louder (0.6) so the native voice is still heard.
- Quick cuts (0.12s), the designed scenes animated 1.6× faster, captions that pop in, a push on the phone at each cut.
- No tutor line: the tutor is hidden at launch (#154). The review gaps are the current ones (1 day → 1 week → 1 month → 4 months).

Build: `python3 brag-output-v9-12/build.py v13`, then `npx hyperframes check` and `npx hyperframes render -o ../brag.mp4` in `brag-output-v13/composition` (settings: `FAST` in build.py).
