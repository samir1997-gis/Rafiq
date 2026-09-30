# Review that grows with progress (#158): how often a recap, how long, and the unit test's pass mark.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/review_progress.py
from concurrent.futures import ThreadPoolExecutor
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from videos_v9 import ask, Q

LEARNER = "an adult UK Muslim beginner learning Modern Standard Arabic on a phone app, lessons of about 5 minutes, often doing 2-6 lessons in one sitting"
RECAPS = [(every, size) for every in (1, 2, 3) for size in (5, 6, 8, 10)]
QR = {"learn": Q("In a beginner Arabic app, after every `every` lesson(s) the learner gets a recap: `size` words from earlier lessons (the ones due for review first), each a quick multiple-choice question, before the next new lesson. Learner: `learner`. How much does this help them remember the words a week later?", ["Not at all", "A little", "Clearly", "A lot"]),
      "annoy": Q("In a beginner Arabic app, after every `every` lesson(s) the learner has to do a recap of `size` quick word questions before the next lesson. Learner: `learner`. How much does it get in the way or feel like a chore?", ["Not at all", "A little", "Clearly", "A lot"])}
TESTS = [(n, mark) for n in (12, 18, 25) for mark in (70, 80, 90)]
QT = {"fair": Q("At the end of each unit of a beginner Arabic app there is a test of `n` questions (word meanings, hear a word and pick it, fill the gap in a sentence). Pass mark `mark`%. Below that, the learner reviews the questions they missed before they can retake it, and the next unit opens only after a pass. Learner: `learner`. How fair and motivating is this?", ["Not at all", "A little", "Clearly", "A lot"]),
      "catches": Q("A unit test in a beginner Arabic app: `n` questions, pass mark `mark`%. How well does it catch a learner who hasn't really learned the unit yet, before they move on?", ["Not at all", "A little", "Clearly", "A lot"]),
      "quit": Q("A unit test in a beginner Arabic app: `n` questions, pass mark `mark`%; failing means reviewing mistakes and retaking it before the next unit opens. Learner: `learner`. How likely are they to give up on the app because of it?", ["Not at all", "A little", "Clearly", "Very"])}

if __name__ == "__main__":
    with ThreadPoolExecutor(8) as ex:
        rr = list(ex.map(lambda r: ask({"every": r[0], "size": r[1], "learner": LEARNER}, QR)["answers"], RECAPS))
        rt = list(ex.map(lambda t: ask({"n": t[0], "mark": t[1], "learner": LEARNER}, QT)["answers"], TESTS))
    print("recap: every size | learn annoy  learn-annoy")
    for (e, s), a in sorted(zip(RECAPS, rr), key=lambda x: -(x[1]["learn"]["score"] - x[1]["annoy"]["score"])):
        print(f"       {e}     {s:>2}   | {a['learn']['score']:.2f}  {a['annoy']['score']:.2f}   {a['learn']['score'] - a['annoy']['score']:+.2f}")
    print("\ntest: questions mark | fair catches quit  fair+catches-quit")
    for (n, m), a in sorted(zip(TESTS, rt), key=lambda x: -(x[1]["fair"]["score"] + x[1]["catches"]["score"] - x[1]["quit"]["score"])):
        print(f"      {n:>2}        {m}%  | {a['fair']['score']:.2f} {a['catches']['score']:.2f}    {a['quit']['score']:.2f}  {a['fair']['score'] + a['catches']['score'] - a['quit']['score']:+.2f}")
