# Still-image salah quizzes (#197): which format of post?
from concurrent.futures import ThreadPoolExecutor
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from videos_v9 import ask, Q, VIEWERS
BASE = "An Instagram post from Rafiq (an Arabic app for UK Muslims), in its calm cream design: 'What does this word in your salah mean?' اغْفِرْ, with four options (guide, forgive, bless, protect). "
FORMATS = {"carousel": "Slide 1 is the question with 'Swipe for the answer →'. Slide 2: the answer, forgive, with رَبِّ اغْفِرْ لِي 'My Lord, forgive me', said between the two sujood, and rafiq-arabic.com.",
           "single_comment": "One image. Caption: 'Answer in the comments.' The answer is pinned as a comment.",
           "single_answer": "One image with the answer shown small at the bottom: forgive, said between the two sujood."}
QS = {"stop": Q("Viewer: `viewer`. Post: `p` How likely are they to stop scrolling and look at it?", ["Scroll past", "Glance", "Look", "Stop and engage"]),
      "engage": Q("Viewer: `viewer`. Post: `p` How likely are they to swipe, comment, save or share?", ["Unlikely", "Maybe", "Likely", "Very likely"]),
      "learn": Q("Viewer: `viewer`. Post: `p` How likely are they to come away knowing the word's meaning?", ["Unlikely", "Maybe", "Likely", "Very likely"])}
if __name__ == "__main__":
    runs = [(k, v) for k in FORMATS for v in VIEWERS for _ in range(2)]
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(lambda r: ask({"viewer": VIEWERS[r[1]], "p": BASE + FORMATS[r[0]]}, QS)["answers"], runs))
    for k in FORMATS:
        rs = [a for (n, _), a in zip(runs, res) if n == k]
        print(f"{k:<15}" + "  ".join(f"{q} {sum(a[q]['score'] for a in rs)/len(rs):.2f}" for q in QS))

# Results (2 Oct 2026), 5 viewers x 2 runs — stop / swipe-comment-save / learn the word:
#   two-slide carousel ("Swipe for the answer") 2.46/2.19/2.88; one image, answer in comments 2.31/1.84/2.70;
#   one image, answer at the bottom 2.36/1.85/2.63. Built: carousels (brag-quiz/build_stills.py).
