# Why the speed-reading reel (m09-speed) underperformed on TikTok, and which changes would make it spread (owner, 11 Oct 2026).
# The posted version: frame 0 = instruction text + an empty bar; first word at 1.5 s; silent but for each word's voice; a thin
# timer bar; "SPEED x1.0 → x3.3" in small type; 5 easy words (door, pen, tea, sea, car); a new bright striped colour per word.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/speed_read_fix.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
from concurrent.futures import ThreadPoolExecutor
BASE = "A 17-second TikTok from Rafiq, a small Arabic-learning account: a speed-reading challenge, read each Arabic word before the timer runs out."
V = {"0_posted": "As posted: the first frame is the instruction 'Read it before the timer, it gets faster' and an empty bar; the first word appears at 1.5 s; no sound except each word read aloud after the timer; a thin timer bar; speed shown as small 'x1.0'..'x3.3'; five easy words (door, pen, tea, sea, car); a different bright striped background for every word.",
     "1_urgency": "Same words, but the first word is already on screen in frame 0 with a big 3-2-1 countdown, a loud ticking clock that speeds up, a buzzer when time runs out, the screen flashing red in the last half second, and the speed shown big ('LEVEL 3: x2').",
     "2_ladder": "A difficulty ladder: the first frame says 'Only fluent readers pass level 5'; level 1 is a 3-letter word, then longer words, level 5 is a full phrase from the salah; ticking clock, buzzer, big level number; the viewer is asked to comment the level they reached.",
     "3_salah": "Words you say in salah (Allahu akbar, subhana, rabbiyal, al-azim, sami'a): 'Can you read your own salah at speed?' in the first frame with the first word already showing; ticking clock and buzzer; ends 'Comment the level you reached'.",
     "4_brand": "Same as 1_urgency but on Rafiq's calm cream/paper background with dark ink text and red accents, instead of bright colours changing every word.",
     "5_duel": "Two players on split screen race to read each word (a friend vs the viewer); ticking clock; whoever's slower gets a red X; 'Tag someone you'd beat'."}
WHO = {"scroller": "a 21-year-old UK Muslim who can read some Arabic, scrolling TikTok fast", "beginner": "a 30-year-old just starting to learn the Arabic letters",
       "reader": "someone who reads Arabic fluently from madrasa"}
Q = {"stop": {"type": "score", "instructions": "`b` `v` Viewer: `who`. How likely are they to stop scrolling in the first 2 seconds?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "finish": {"type": "score", "instructions": "`b` `v` Viewer: `who`. How likely are they to watch to the end (or replay it)?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "spread": {"type": "score", "instructions": "`b` `v` Viewer: `who`. How likely are they to comment, duet/stitch or send it to a friend?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]}}
jobs = [(k, w) for k in V for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"b": BASE, "v": V[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':12}" + "".join(f"{q:>8}" for q in Q) + "   total   (beginner stop)")
for k in V:
    s = {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}
    print(f"{k:12}" + "".join(f"{s[q]:8.2f}" for q in Q) + f"   {sum(s.values()):.2f}   ({r[(k, 'beginner')]['stop']['score']})")

# Round 2: combine the winners, and settle the colours.
V2 = {"6_salah_ladder": "Words you say in salah as a 5-level ladder (level 1 أَكْبَرُ, then سُبْحانَ, رَبِّيَ الْعَظِيمِ, سَمِعَ اللَّهُ لِمَنْ حَمِدَهُ, level 5 the full tashahhud opening); frame 0: 'Can you read your own salah at speed?' with level 1 already showing; 3-2-1 countdown, ticking that speeds up, buzzer, red flash at the end of each timer; big 'LEVEL 3'; ends 'Comment the level you reached'.",
      "7_same_bright": "Same as 6 with a new bright striped colour for every level (red, green, purple, orange, black).",
      "8_same_dark": "Same as 6 on one dark background throughout that turns redder as the levels get faster."}
jobs = [(k, w) for k in V2 for w in WHO]
with ThreadPoolExecutor(12) as ex: r2 = dict(ex.map(lambda j: (j, ask({"b": BASE, "v": V2[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
for k in V2:
    s = {q: sum(r2[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}
    print(f"{k:14}" + "".join(f"{s[q]:8.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
