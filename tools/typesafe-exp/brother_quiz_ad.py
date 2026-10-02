# The "which of these means brother?" ad (#188): the owner's script vs small changes, before filming.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/brother_quiz_ad.py
from concurrent.futures import ThreadPoolExecutor
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from videos_v9 import ask, Q, VIEWERS
SHOW = ("A 12-second vertical video. A young British Muslim man floats over the Rafiq app (green screen). On screen: 'Which of these means brother?' "
        "and four Arabic options: أَخِي, أَخٌ, أُخْتٌ, إِخْوَةٌ, with a countdown. He says: ")
SCRIPTS = {
 "owner": "'Which of these means brother in Arabic? Five, four, three, two, one. If you said akhi, you're incorrect. The word for brother is akh. The ya is for possession: akhi means MY brother. If you got that wrong, go to rafiq-arabic.com now so you don't embarrass yourself again in the future.'",
 "softer_end": "'Which of these means brother in Arabic? Five, four, three, two, one. If you said akhi, you're incorrect. The word for brother is akh. The ya is for possession: akhi means MY brother. Got it wrong? Learn it properly, free for a week, at rafiq-arabic.com.'",
 "comment_end": "'Which of these means brother in Arabic? Five, four, three, two, one. If you said akhi, you're incorrect. The word for brother is akh. The ya is for possession: akhi means MY brother. Comment what you picked, and if you got it wrong, rafiq-arabic.com.'",
}
QS = {"watch": Q("Viewer: `viewer`. Video: `v` How likely are they to watch to the end?", ["Scroll past", "Watch a bit", "Most of it", "To the end"]),
      "try": Q("Viewer: `viewer`. Video: `v` How likely are they to visit the website after it?", ["Unlikely", "Maybe", "Likely", "Very likely"]),
      "off": Q("Viewer: `viewer`. Video: `v` How much does its tone put them off or feel condescending?", ["Not at all", "Slightly", "Noticeably", "A lot"]),
      "engage": Q("Viewer: `viewer`. Video: `v` How likely are they to comment, share or replay it?", ["Unlikely", "Maybe", "Likely", "Very likely"]),
      "clear": Q("Viewer: `viewer`. Video: `v` How clear is the lesson (brother vs my brother) to them?", ["Confusing", "Somewhat clear", "Clear", "Very clear"])}
if __name__ == "__main__":
    runs = [(k, v) for k in SCRIPTS for v in VIEWERS for _ in range(2)]
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(lambda r: ask({"viewer": VIEWERS[r[1]], "v": SHOW + SCRIPTS[r[0]]}, QS)["answers"], runs))
    print("script        watch  try   off   engage clear")
    for k in SCRIPTS:
        rs = [a for (n, _), a in zip(runs, res) if n == k]
        print(f"{k:<13} " + "  ".join(f"{sum(a[q]['score'] for a in rs)/len(rs):.2f}" for q in QS))

# Results (1 Oct 2026), 5 viewers x 2 runs; watch / visit site / tone puts off (lower is better) / comment-share / clear:
#   owner's script ("...so you don't embarrass yourself again")  1.76 / 1.09 / 2.79 / 0.88 / 2.39
#   softer ending ("Got it wrong? Learn it properly...")           2.02 / 1.36 / 2.14 / 1.26 / 2.39
#   comment ending ("Comment what you picked...")                  2.18 / 1.54 / 1.66 / 1.63 / 2.37
#   friendly ("Most people pick akhi, but akhi means MY brother... Comment what you picked, learn the rest free")
#                                                                  2.38 / 1.58 / 1.22 / 1.82 / 2.50  <- best on every measure
