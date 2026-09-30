# "Say it yourself" in units 1-3 (#164): free writing is too hard this early. What should it be?
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/say_it_early.py
from concurrent.futures import ThreadPoolExecutor
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from videos_v9 import ask, Q

LEARNER = "an adult UK beginner in unit 1 of an Arabic app, who has met about 40 words and phrases and a few grammar points"
WAYS = {
 "free":    "type three sentences introducing yourself in Arabic from scratch (what the app does now)",
 "frames":  "build your own introduction one sentence at a time: each sentence has one gap, and you pick the word that's true for you (أَنا ___: student, teacher, engineer, in the male or female form; أَنا مِنْ ___: a country), then say the finished sentences aloud with the audio",
 "repeat":  "hear a model introduction, then say each sentence aloud after it",
 "tiles":   "rebuild the model introduction from word tiles, then say it aloud",
}
QS = {"can":  Q("Task in a beginner Arabic app: `w`. Learner: `learner`. How likely are they to manage it without getting stuck?", ["Unlikely", "Maybe", "Likely", "Very likely"]),
      "own":  Q("Task in a beginner Arabic app: `w`. Learner: `learner`. How much does it feel like saying something true about themselves?", ["Not at all", "A little", "Clearly", "A lot"]),
      "learn": Q("Task in a beginner Arabic app: `w`. Learner: `learner`. How much does it build real speaking ability?", ["Not at all", "A little", "Clearly", "A lot"])}

if __name__ == "__main__":
    with ThreadPoolExecutor(4) as ex:
        r = dict(zip(WAYS, ex.map(lambda w: ask({"w": w, "learner": LEARNER}, QS)["answers"], WAYS.values())))
    print("way      can   own  learn  total")
    for k, a in sorted(r.items(), key=lambda x: -sum(x[1][q]["score"] for q in QS)):
        print(f"{k:<8} {a['can']['score']:.2f}  {a['own']['score']:.2f}  {a['learn']['score']:.2f}  {sum(a[q]['score'] for q in QS):.2f}")
