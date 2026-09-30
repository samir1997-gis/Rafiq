# The basics with a goal sentence (#168): each lesson adds a piece of
# "السَّلامُ عَلَيْكُمْ، اسْمِي …، وَأَنا طالِبُ اللُّغَةِ الْعَرَبِيَّةِ" — against the section as it is now.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/basics_goal.py
from concurrent.futures import ThreadPoolExecutor
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from videos_v9 import ask
from simpler_overall import QS, LEARNER, AFTER, V_SPLIT
GOAL = ("After learning the letters and vowel marks, the learner does 'The basics'. It opens with a goal: by the end you'll say "
        "'السَّلامُ عَلَيْكُمْ، اسْمِي … وَأَنا طالِبُ اللُّغَةِ الْعَرَبِيَّةِ' (Peace be upon you, my name is …, and I'm a student of the Arabic language). "
        "Six short lessons, each teaching one building block and adding a piece of that sentence at the end: 'the' and sun letters (السَّلامُ عَلَيْكُمْ); "
        "'my' endings (اسْمِي, my name); I/you/he/she with no word for 'is' (وَأَنا طالِبٌ); masculine and feminine, with هَذا/هَذِهِ (طالِبَةٌ for a woman); "
        "'of' as two nouns side by side, and describing words (طالِبُ اللُّغَةِ الْعَرَبِيَّةِ: the sentence is complete); then one and many, with a bonus: "
        "نَحْنُ طُلّابُ اللُّغَةِ الْعَرَبِيَّةِ. Each lesson is 1-2 teaching screens then 8 quick picks on single words and short phrases, and ends with 'your sentence so far', "
        "heard and said aloud. An 18-question check at the end, then unit 1. Units now focus on vocabulary and using it.")
if __name__ == "__main__":
    V = {"now": AFTER, "greetings first": V_SPLIT, "goal sentence": GOAL}
    runs = [(k, v) for k, v in V.items() for _ in range(3)]
    with ThreadPoolExecutor(9) as ex:
        res = list(ex.map(lambda r: ask({"v": r[1], "learner": LEARNER}, QS)["answers"], runs))
    print("                  simple overload sticks stay slow")
    for k in V:
        a = {q: sum(x[q]["score"] for (n, _), x in zip(runs, res) if n == k) / 3 for q in QS}
        print(f"{k:<17} {a['simple']:.2f}   {a['load']:.2f}    {a['sticks']:.2f}  {a['stay']:.2f} {a['slow']:.2f}")
