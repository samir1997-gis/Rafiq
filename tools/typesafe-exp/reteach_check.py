# After "The basics" (#165): which "How it works" cards in the journey reteach what the basics already teach? (#166)
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/reteach_check.py
from concurrent.futures import ThreadPoolExecutor
import json, subprocess, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from videos_v9 import ask
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
js = lambda f, n: json.loads(subprocess.run(["node"], input=open(os.path.join(ROOT, f), encoding="utf8").read() + f"\nprocess.stdout.write(JSON.stringify({n}))", capture_output=True, text=True, check=True).stdout)
B, E = js("basics-data.js", "BASICS"), js("drills-data.js", "EXTRA")
BASICS = " | ".join(f"{t['h']}: {t['en']}" for l in B for t in l["teach"])
CARDS = [(n, g) for n in sorted(E) for g in E[n].get("grammar", [])]
QS = {"same": {"type": "noul", "instructions": "A learner has already finished a section that taught exactly this: `basics`. Later a lesson card says: `h`. `en` Example: `ar`. Does the card mainly teach again something that section already taught (rather than something new)?"},
      "new":  {"type": "noul", "instructions": "A learner already knows: `basics`. A later card says: `h`. `en` Does it also teach something new that they don't know yet?"}}
if __name__ == "__main__":
    with ThreadPoolExecutor(8) as ex:
        r = list(ex.map(lambda c: ask({"basics": BASICS, "h": c[1]["h"], "en": c[1]["en"], "ar": c[1]["ar"]}, QS)["answers"], CARDS))
    print("unit  same  new  card")
    for (n, g), a in zip(CARDS, r):
        flag = "  <-- reteaches" if a["same"]["noul"] >= 0.6 else ""
        print(f"{n}    {a['same']['noul']:.2f}  {a['new']['noul']:.2f}  {g['h']}{flag}")
