# Does the new start (letters -> The basics -> trimmed units) make learning simpler than before? (#167)
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/simpler_overall.py
from concurrent.futures import ThreadPoolExecutor
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from videos_v9 import ask, Q
LEARNER = "an adult UK Muslim beginner with no Arabic, learning on a phone a few minutes a day"
BEFORE = ("After learning the letters and vowel marks (and five reading rules: ة, ال, sun letters, joining, stopping), the learner goes straight into unit 1 (greetings). "
          "Unit 1's word lessons are followed by one 'How it works' step with 7 grammar cards in a row: no word for 'is', masculine and feminine, 'this' m/f, 'the' and 'a', "
          "nationalities, 'my' endings, question words, each with a quick check. Unit 2 then has 6 cards plus 3 more in a second step; unit 3 has 6 cards plus 4 more. "
          "Grammar is taught inside the topic units, alongside greetings, family and housing vocabulary.")
AFTER = ("After learning the letters and vowel marks (and three reading rules: ة, joining, stopping), the learner does 'The basics': six short lessons "
         "(the/a with sun and moon letters; masculine/feminine; I/you/he/she; this and describing words; plurals and we/they; my/your/his/her). "
         "Each is 1-2 teaching screens with examples, then 8 quick picks on single words and 2-3 word sentences (e.g. 'Make it feminine: طالِب', 'Which fits: أَنا مُدَرِّسٌ وَهِيَ ___'); "
         "missed picks come back; an 18-question check at the end. Then unit 1 (greetings), whose 'How it works' now has only 2 cards (nationalities, question words); "
         "unit 2 has 5 cards plus 3; unit 3 has 7. The units focus on vocabulary and using it.")
QS = {"simple":  Q("How a beginner Arabic app starts: `v` Learner: `learner`. How simple and easy to follow does it feel?", ["Confusing", "OK", "Simple", "Very simple"]),
      "load":    Q("How a beginner Arabic app starts: `v` Learner: `learner`. How overloaded do they feel at any one point?", ["Not at all", "A little", "Clearly", "Very"]),
      "sticks":  Q("How a beginner Arabic app starts: `v` Learner: `learner`. How well do the basics (gender, the, plurals, pronouns, my/your) stick?", ["Badly", "OK", "Well", "Very well"]),
      "stay":    Q("How a beginner Arabic app starts: `v` Learner: `learner`. How likely are they to still be using it after two weeks?", ["Unlikely", "Maybe", "Likely", "Very likely"]),
      "slow":    Q("How a beginner Arabic app starts: `v` Learner: `learner`. How much does it feel slow to get to real, useful Arabic (greetings, talking about yourself)?", ["Not at all", "A little", "Clearly", "Very"])}
if __name__ == "__main__":
    runs = [("before", BEFORE), ("after", AFTER)] * 3                    # 3 runs each, averaged
    with ThreadPoolExecutor(6) as ex:
        res = list(ex.map(lambda v: ask({"v": v[1], "learner": LEARNER}, QS)["answers"], runs))
    avg = {k: {q: sum(a[q]["score"] for (n, _), a in zip(runs, res) if n == k) / 3 for q in QS} for k in ("before", "after")}
    print("           simple  overload  sticks  stay  feels-slow")
    for k in ("before", "after"):
        a = avg[k]; print(f"{k:<10} {a['simple']:.2f}    {a['load']:.2f}      {a['sticks']:.2f}    {a['stay']:.2f}  {a['slow']:.2f}")

# Fixes for "feels slow" (the basics before any greetings):
V_SPLIT = AFTER.replace("does 'The basics': six short lessons", "learns the greetings first (unit 1's first word lesson: as-salamu alaykum, how are you, my name is), then does 'The basics': six short lessons")
V_HALF = AFTER.replace("does 'The basics': six short lessons", "does the first three lessons of 'The basics', then unit 1's greetings, then the other three basics lessons before unit 2. 'The basics' is six short lessons")
V_FRAME = AFTER.replace("missed picks come back;", "missed picks come back; every lesson ends with 'now you can say': a real sentence about yourself, like أَنا طالِبٌ وَهِيَ أُخْتِي;")

# Results (30 Sep 2026), averaged over 3 runs (simple / overload / sticks / stay / feels slow):
#   before (grammar inside units 1-3)    1.82 / 1.75 / 1.94 / 1.92 / 0.55
#   after (The basics, trimmed units)    1.80 / 0.91 / 2.30 / 2.00 / 1.50
#   greetings first, then the basics     1.85 / 1.02 / 2.19 / 2.08 / 0.82
#   basics split in two                  1.56 / 0.82 / 2.20 / 2.12 / 1.48
#   'now you can say' after each lesson  1.82 / 0.91 / 2.52 / 2.07 / 1.31
#   greetings first + 'now you can say'  1.85 / 1.06 / 2.41 / 2.17 / 0.63   <- best overall
