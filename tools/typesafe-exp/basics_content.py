# The basics (#165): every teaching example correct, every pick with exactly one right answer and fair for the lesson.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/basics_content.py
from concurrent.futures import ThreadPoolExecutor
import json, subprocess, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from videos_v9 import ask, Q
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
src = open(os.path.join(ROOT, "basics-data.js"), encoding="utf8").read()
B = json.loads(subprocess.run(["node"], input=src + "\nprocess.stdout.write(JSON.stringify(BASICS))", capture_output=True, text=True, check=True).stdout)
LEARNER = "an adult UK beginner who has just learned the Arabic letters and vowel marks"
QT = {"right": {"type": "noul", "instructions": "A beginner lesson on Modern Standard Arabic, '`title`'. Heading: `h`. Examples: `pairs`. Explanation: `en`. Is everything correct?"},
      "clear": Q("A beginner lesson, '`title`': `h`. Examples: `pairs`. `en` Learner: `learner`. How clear is it?", ["Confusing", "OK", "Clear", "Crystal clear"])}
QD = {"only": {"type": "noul", "instructions": "Beginner Modern Standard Arabic quiz: `q` `shown` Options: `opts`. The app says `right` is the answer. Is `right` correct and every other option wrong?"},
      "fair": Q("Straight after a lesson on '`title`' (`taught`), a learner gets: `q` `shown` Options: `opts`. Learner: `learner`. How fair is it (only needs what was taught)?", ["Unfair", "OK", "Fair", "Very fair"])}
if __name__ == "__main__":
    T = [(l, t) for l in B for t in l["teach"]]
    D = [(l, d) for l in B for d in l["drills"]]
    taught = lambda l: " ".join(t["h"] + " (" + "; ".join(f"{a} = {e}" for a, e in t["pairs"]) + "): " + t["en"] for t in l["teach"])
    with ThreadPoolExecutor(8) as ex:
        rt = list(ex.map(lambda x: ask({"title": x[0]["title"], "h": x[1]["h"], "pairs": "; ".join(f"{a} = {e}" for a, e in x[1]["pairs"]), "en": x[1]["en"], "learner": LEARNER}, QT)["answers"], T))
        rd = list(ex.map(lambda x: ask({"title": x[0]["title"], "taught": taught(x[0]), "q": x[1][0], "shown": x[1][1], "opts": " / ".join(x[1][2]), "right": x[1][2][0], "learner": LEARNER}, QD)["answers"], D))
    print("teaching screens: right clear")
    for (l, t), a in zip(T, rt): print(f"  {a['right']['noul']:.2f} {a['clear']['score']:.2f}  {l['key']}: {t['h']}{'  <-- look' if a['right']['noul'] < 0.7 else ''}")
    print("picks: only fair")
    for (l, d), a in sorted(zip(D, rd), key=lambda x: x[1]["only"]["noul"]):
        print(f"  {a['only']['noul']:.2f} {a['fair']['score']:.2f}  {l['key']}: {d[0]} {d[1]} → {d[2][0]}{'  <-- look' if a['only']['noul'] < 0.7 or a['fair']['score'] < 1.5 else ''}")
