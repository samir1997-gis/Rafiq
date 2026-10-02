# v15: "Which of these means brother?" (#188)

A background for the owner to film over on green screen: the app asks "Which of these means brother?" with four options
(أَخِي, أُخْت, أَخ, إِخْوَة), counts down 5 to 1, marks أَخِي wrong ("my brother"), then أَخ right with the native audio, shows the rule
(the ـِي on the end means "my"), and ends on rafiq-arabic.com. 1080x1920, 15s. Everything sits in the top half so the owner can float in the bottom half.

Timing is a first guess for rehearsing; it gets matched to the owner's voice once the footage is in.
Script check: `tools/typesafe-exp/brother_quiz_ad.py` (the friendly script scored best on every measure).
Render: `npx hyperframes render -o ../brag.mp4` in `brag-output-v15/composition`.
