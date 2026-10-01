# The learner's name in Arabic (#169): is each spelling the standard, correctly vowelled Arabic for those English spellings?
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/names_check.py
from concurrent.futures import ThreadPoolExecutor
import json, subprocess, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from videos_v9 import ask
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
src = open(os.path.join(ROOT, "basics-data.js"), encoding="utf8").read()
N = json.loads(subprocess.run(["node"], input=src + "\nprocess.stdout.write(JSON.stringify(BASICS_NAMES))", capture_output=True, text=True, check=True).stdout)
by = {}
for en, ar in N.items(): by.setdefault(ar, []).append(en)
Q = {"ok": {"type": "noul", "instructions": "A Muslim first name written in English as `en`. Is `ar` its standard Arabic spelling, with correct vowel marks?"},
     "same": {"type": "noul", "instructions": "Are all of these English spellings the same name: `en`?"}}
if __name__ == "__main__":
    items = list(by.items())
    with ThreadPoolExecutor(8) as ex:
        r = list(ex.map(lambda it: ask({"ar": it[0], "en": " / ".join(it[1])}, Q)["answers"], items))
    for (ar, ens), a in sorted(zip(items, r), key=lambda x: x[1]["ok"]["noul"]):
        if a["ok"]["noul"] < 0.75 or a["same"]["noul"] < 0.75:
            print(f"{a['ok']['noul']:.2f} {a['same']['noul']:.2f}  {ar}  {' / '.join(ens)}")
    print(f"{sum(1 for a in r if a['ok']['noul'] >= 0.75 and a['same']['noul'] >= 0.75)} of {len(r)} fine")
