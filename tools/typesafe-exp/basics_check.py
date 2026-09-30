# First-lesson basics (#163): the new and changed cards, their quick checks, and the reading rules.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/basics_check.py
from concurrent.futures import ThreadPoolExecutor
import json, subprocess, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from videos_v9 import ask, Q
from teach_cards import QC, QB, LEARNER

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
def js(file, name):
    src = open(os.path.join(ROOT, file), encoding="utf8").read()
    return json.loads(subprocess.run(["node"], input=src + f"\nprocess.stdout.write(JSON.stringify({name}))", capture_output=True, text=True, check=True, cwd=ROOT).stdout)
EXTRA, RULES = js("drills-data.js", "EXTRA"), js("alphabet-data.js", "READING_RULES")
CARDS = [(n, g) for n in ("01", "02", "03") for g in EXTRA[n]["grammar"] if g.get("check")]
QK = {"only": {"type": "noul", "instructions": "A quick check in a beginner Modern Standard Arabic app. Question: `q` Options: `opts`. The app marks `right` as the answer. Is `right` correct, and is every other option wrong?"},
      "fair": Q("A quick check straight after a card teaching `h`. Question: `q` Options: `opts`. Learner: `learner`. How fair is it (tests what the card taught, no trick)?", ["Unfair", "OK", "Fair", "Very fair"])}
QR = {"right": {"type": "noul", "instructions": "A reading rule for Modern Standard Arabic, taught to beginners: `title`: `what` Examples: `ex`. Is it correct?"},
      "clear": Q("A reading rule taught to `learner` after the vowel marks: `title`: `what` Examples: `ex`. How clear is it?", ["Confusing", "OK", "Clear", "Crystal clear"]),
      "only": {"type": "noul", "instructions": "A quick check: `q` Options: `opts`. The app marks `right` as the answer. Is `right` correct, and is every other option wrong?"}}

if __name__ == "__main__":
    with ThreadPoolExecutor(8) as ex:
        rc = list(ex.map(lambda c: ask({"h": c[1]["h"], "ar": c[1]["ar"], "tr": c[1].get("tr", ""), "en": c[1]["en"], "learner": LEARNER}, QC)["answers"], CARDS))
        rb = list(ex.map(lambda c: ask({"h": c[1]["h"], "bad": c[1]["bad"][0], "note": c[1]["bad"][1], "learner": LEARNER}, QB)["answers"], CARDS))
        rk = list(ex.map(lambda c: ask({"h": c[1]["h"], "q": c[1]["check"][0], "opts": " / ".join(c[1]["check"][1]), "right": c[1]["check"][1][c[1]["check"][2]], "learner": LEARNER}, QK)["answers"], CARDS))
        rr = list(ex.map(lambda r: ask({"title": r[0], "what": r[1], "ex": "; ".join(f"{e[0]} = {e[1]} ({e[2]})" for e in r[2]), "q": r[3][0], "opts": " / ".join(r[3][1]), "right": r[3][1][r[3][2]], "learner": LEARNER}, QR)["answers"], RULES))
    print("unit  clear right | mistake: wrong fix helps | check: only fair | card")
    for (n, g), c, b, k in zip(CARDS, rc, rb, rk):
        low = min(c["right"]["noul"], b["wrong"]["noul"], b["fix"]["noul"], k["only"]["noul"]) < 0.7
        print(f"{n}   {c['clear']['score']:.2f}  {c['right']['noul']:.2f} |          {b['wrong']['noul']:.2f}  {b['fix']['noul']:.2f}  {b['helps']['score']:.2f} |        {k['only']['noul']:.2f}  {k['fair']['score']:.2f} | {g['h']}{' <-- look' if low else ''}")
    print("\nreading rule                          right clear only")
    for r, a in zip(RULES, rr):
        print(f"{r[0]:<36}  {a['right']['noul']:.2f}  {a['clear']['score']:.2f}  {a['only']['noul']:.2f}{' <-- look' if min(a['right']['noul'], a['only']['noul']) < 0.7 else ''}")
