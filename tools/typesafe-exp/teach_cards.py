# Teach first (#156): are the new grammar cards clear and right, and is each crossed-out mistake really a mistake?
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/teach_cards.py
from concurrent.futures import ThreadPoolExecutor
import json, subprocess, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from videos_v9 import ask, Q

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
EXTRA = json.loads(subprocess.run(["node"], input=open(os.path.join(ROOT, "drills-data.js"), encoding="utf8").read() + "\nprocess.stdout.write(JSON.stringify(EXTRA))",
                                   capture_output=True, text=True, check=True, cwd=ROOT).stdout)
CARDS = [(n, g) for n in ("01", "02", "03") for g in EXTRA[n]["grammar"]]
NEW = {"Three endings: -u, -a, -i", "The past: the ending shows who", "Describing words copy the noun", "‘This is a house’ or ‘this house’?"}
LEARNER = "an adult UK beginner in Modern Standard Arabic, a few lessons in, who reads Arabic script slowly"

QC = {"clear": Q("A grammar card in a beginner Arabic app. Title: `h`. Examples: `ar` = `tr`. Explanation: `en`. Learner: `learner`. How clear is it?", ["Confusing", "OK", "Clear", "Crystal clear"]),
      "right": {"type": "noul", "instructions": "A grammar card teaching Modern Standard Arabic. Title: `h`. Examples: `ar` = `tr`. Explanation: `en`. Is everything it says, and every example, correct Modern Standard Arabic?"}}
QB = {"wrong": {"type": "noul", "instructions": "In Modern Standard Arabic, the learner wrote: `bad`. Is that a mistake (for the meaning intended on a card about `h`)?"},
      "fix": {"type": "noul", "instructions": "A card about `h` in a beginner Arabic app shows the mistake `bad` and says: `note`. Is the correction right and the note accurate?"},
      "helps": Q("A grammar card about `h` shows a common mistake crossed out: `bad`, with the note `note`. Learner: `learner`. How much does seeing it help them avoid the mistake?", ["Not at all", "A little", "Clearly", "A lot"])}

if __name__ == "__main__":
    with ThreadPoolExecutor(8) as ex:
        rc = list(ex.map(lambda c: ask({"h": c[1]["h"], "ar": c[1]["ar"], "tr": c[1].get("tr", ""), "en": c[1]["en"], "learner": LEARNER}, QC)["answers"], CARDS))
        rb = list(ex.map(lambda c: ask({"h": c[1]["h"], "bad": c[1]["bad"][0], "note": c[1]["bad"][1], "learner": LEARNER}, QB)["answers"], CARDS))
    print("unit  new  clear right | mistake: is-wrong fix-right helps | card")
    for (n, g), c, b in zip(CARDS, rc, rb):
        flag = " <-- look" if c["right"]["noul"] < 0.7 or b["wrong"]["noul"] < 0.7 or b["fix"]["noul"] < 0.7 else ""
        print(f"{n}    {'NEW' if g['h'] in NEW else '   '}  {c['clear']['score']:.2f}  {c['right']['noul']:.2f} |          {b['wrong']['noul']:.2f}      {b['fix']['noul']:.2f}   {b['helps']['score']:.2f} | {g['h']}{flag}")
