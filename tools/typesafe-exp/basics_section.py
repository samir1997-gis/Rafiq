# "The basics" (#165): a section between the letters and unit 1. Order of lessons, and how many picks per lesson.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/basics_section.py
from concurrent.futures import ThreadPoolExecutor
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from videos_v9 import ask, Q
LEARNER = "an adult UK Muslim who has just learned to read the Arabic letters and vowel marks, before starting unit 1 (greetings)"
ORDERS = {
 "A": "masculine/feminine → I, you, he, she → 'the' and 'a' (sun and moon letters) → one and many (plurals, we/they) → my, your, his, her → this, and describing words",
 "B": "I, you, he, she → masculine/feminine → 'the' and 'a' → this, and describing words → my, your, his, her → one and many",
 "C": "'the' and 'a' → masculine/feminine → I, you, he, she → this, and describing words → one and many → my, your, his, her",
}
PICKS = {n: f"each lesson is 1-2 teaching screens then {n} quick picks on single words and two- or three-word sentences, with missed ones coming back at the end" for n in (6, 10, 15)}
QO = {"build": Q("A short section teaching the building blocks of Arabic grammar in this order: `o`. Learner: `learner`. How well does each lesson build on the one before?", ["Badly", "OK", "Well", "Very well"])}
QP = {"stick": Q("A beginner Arabic lesson: `p`. Learner: `learner`. How well does the idea stick?", ["Badly", "OK", "Well", "Very well"]),
      "tire":  Q("A beginner Arabic lesson: `p`. Learner: `learner`. How likely are they to get bored or tired before the end?", ["Unlikely", "Maybe", "Likely", "Very likely"])}
if __name__ == "__main__":
    with ThreadPoolExecutor(6) as ex:
        ro = dict(zip(ORDERS, ex.map(lambda o: ask({"o": o, "learner": LEARNER}, QO)["answers"], ORDERS.values())))
        rp = dict(zip(PICKS, ex.map(lambda p: ask({"p": p, "learner": LEARNER}, QP)["answers"], PICKS.values())))
    for k, a in ro.items(): print(f"order {k}: {a['build']['score']:.2f}  {ORDERS[k]}")
    for k, a in rp.items(): print(f"{k:>2} picks: stick {a['stick']['score']:.2f} tire {a['tire']['score']:.2f}")
