# Short quiz videos for regular posting (#197): which format, and which salah words?
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/salah_quizzes.py
from concurrent.futures import ThreadPoolExecutor
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from videos_v9 import ask, Q, VIEWERS
BASE = ("A 12-15 second vertical TikTok/Reel from Rafiq (an Arabic app for UK Muslims), no face, in the app's calm cream design, "
        "with a native Arabic voice saying the word and a soft tick for each second of the countdown. It ends with rafiq-arabic.com. ")
FORMATS = {
 "meaning":   "On screen: 'What does this word in your salah mean?' The Arabic word, voiced. Four English options. 5, 4, 3, 2, 1. The right one lights up, with one line on where you say it.",
 "frequency": "On screen: 'You say this word 36 times in every four-rakah prayer. What does it mean?' The Arabic word, voiced. Four English options. 5, 4, 3, 2, 1. The answer lights up.",
 "reverse":   "On screen: 'Which of these means \"my Lord\"?' Four Arabic options that look alike (رَبِّ, رَبُّنا, رَبِّيَ, الرَّبّ), each voiced. 5, 4, 3, 2, 1. The answer, and why: the ـِي on the end means 'my'.",
 "pair":      "On screen: 'In ruku you say سُبْحانَ رَبِّيَ الْعَظِيمِ. What do you say in sujood?' Two Arabic options. 5, 4, 3, 2, 1. The answer: الْأَعْلى, the Most High, and the meanings of both.",
 "finish":    "On screen: 'Finish the line: سَمِعَ اللَّهُ لِمَنْ ...' Three Arabic options. 5, 4, 3, 2, 1. The answer, voiced, and the meaning: Allah hears the one who praises Him.",
 "rapid":     "On screen: '3 salah words in 15 seconds. Keep score.' Three Arabic words in a row, each with two options and 3 seconds; answers after each. 'Comment your score.'",
 "trap":      "On screen: 'Most people get this wrong.' سَمِعَ: does it mean 'sees', 'hears', 'knows' or 'loves'? 5, 4, 3, 2, 1. 'Hears.' Allah hears the one who praises Him.",
}
QS = {"watch": Q("Viewer: `viewer`. Video: `v` How likely are they to watch it to the end?", ["Scroll past", "Watch a bit", "Most of it", "To the end"]),
      "engage": Q("Viewer: `viewer`. Video: `v` How likely are they to comment their answer, share, save or replay it?", ["Unlikely", "Maybe", "Likely", "Very likely"]),
      "try": Q("Viewer: `viewer`. Video: `v` How likely are they to visit the app's website?", ["Unlikely", "Maybe", "Likely", "Very likely"]),
      "respect": Q("Viewer: `viewer`. Video: `v` How respectful and fitting is it for content about the prayer?", ["Off-putting", "A bit flippant", "Fine", "Respectful and fitting"])}
if __name__ == "__main__":
    runs = [(k, v) for k in FORMATS for v in VIEWERS for _ in range(2)]
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(lambda r: ask({"viewer": VIEWERS[r[1]], "v": BASE + FORMATS[r[0]]}, QS)["answers"], runs))
    print("format      watch  engage try   respect")
    for k in FORMATS:
        rs = [a for (n, _), a in zip(runs, res) if n == k]
        print(f"{k:<11} " + "  ".join(f"{sum(a[q]['score'] for a in rs)/len(rs):.2f}" for q in QS))

# Results (2 Oct 2026), 5 viewers x 2 runs — watch / comment-share / visit / respectful:
#   meaning 2.40/1.79/1.70/2.67, frequency 2.44/1.88/1.61/2.44, reverse 2.47/1.90/1.65/2.61, pair 2.44/1.87/1.67/2.58,
#   finish 2.35/1.86/1.58/2.67, rapid 2.21/1.91/1.52/1.80 (flippant: dropped), trap 2.51/1.82/1.64/2.49.
# Built first: meaning (sami'a), reverse (rabbana: "my Lord" would have two right answers, rabbi and rabbiya), pair (ruku/sujood).
