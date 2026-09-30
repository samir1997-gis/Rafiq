# Every sentence a learner can build in "Say it yourself", units 1-3 (#164): correct Arabic, and the English right?
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/say_own_check.py
from concurrent.futures import ThreadPoolExecutor
import json, subprocess, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from videos_v9 import ask
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
src = open(os.path.join(ROOT, "drills-data.js"), encoding="utf8").read()
E = json.loads(subprocess.run(["node"], input=src + "\nprocess.stdout.write(JSON.stringify(EXTRA))", capture_output=True, text=True, check=True, cwd=ROOT).stdout)
items = []
for n in ("01", "02", "03"):
    for t in E[n]["say"]:
        for f in t["frames"]:
            if t.get("ask"):
                items.append((n, f"{f['o'][f['a']]} → {f['q']}", f"Q&A: someone asks {f['o'][f['a']]} and the answer is {f['q']} ({f['qen']})"))
                continue
            for o in f["o"]:
                pat = f["ar"] if isinstance(f["ar"], str) else f["ar"][o[2] if len(o) > 2 else "m"]
                line = o[0] if pat == "___" else pat.replace("___", o[0])
                eng = o[1] if pat == "___" else f["en"].replace("…", o[1]).replace("My home", "My " + ("flat" if pat.startswith("شَقَّتِي") else "house"))
                items.append((n, line, f"{line} = {eng}"))
QS = {"ok": {"type": "noul", "instructions": "Modern Standard Arabic for beginners: `s`. Is the Arabic correct (vowels and endings included) and does it mean what the English says?"}}
if __name__ == "__main__":
    with ThreadPoolExecutor(8) as ex:
        r = list(ex.map(lambda it: ask({"s": it[2]}, QS)["answers"], items))
    for (n, line, _), a in sorted(zip(items, r), key=lambda x: x[1]["ok"]["noul"]):
        print(f"{n}  {a['ok']['noul']:.2f}  {line}{'  <-- look' if a['ok']['noul'] < 0.7 else ''}")
