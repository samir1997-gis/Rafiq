# The English in units 13-16 (#344, #371), checked with TypeSafe: the grammar cards (clear and correct for a beginner), every line of the
# conversations and the speaking prompts (does the English match the Arabic), the ladders, the word meanings, and the fix/cloze notes.
# python3 tools/typesafe-exp/units_13_16.py DATA.json   (DATA.json: the content as extracted from drills-data.js and vocab-data.js)
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
import sys
D = json.load(open(sys.argv[1]))
APP = "Rafiq, an app teaching Modern Standard Arabic to adult beginners (many of them Muslims in the UK), on a phone. "
QG = {"clear": {"type": "score", "instructions": APP + "A grammar card. Heading: `h`. Example: `ar` (`tr`). Explanation: `en`. Is the explanation clear to a beginner?", "criteria": ["No", "Partly", "Mostly", "Fully"]},
      "right": {"type": "score", "instructions": APP + "A grammar card. Heading: `h`. Example: `ar` (`tr`). Explanation: `en`. Is it accurate Arabic grammar, with the example translated correctly?", "criteria": ["No", "Partly", "Mostly", "Fully"]},
      "check": {"type": "score", "instructions": APP + "A quick check after the card: question `q`, options `o`, the right one `a`, the note `n`. Is the question clear and the marked answer the only right one?", "criteria": ["No", "Partly", "Mostly", "Fully"]}}
QT = {"match": {"type": "score", "instructions": APP + "Arabic: `ar`. The English the learner sees: `en`. Is the English an accurate, natural translation of the Arabic?", "criteria": ["No", "Partly", "Mostly", "Fully"]}}
jobs = []
for g in D["grammar"]:
    c = g.get("check") or ["", [], 0, ""]
    st = {"h": g["h"], "ar": g["ar"], "tr": g["tr"], "en": g["en"], "q": c[0], "o": " / ".join(c[1]), "a": c[1][c[2]] if c[1] else "", "n": c[3]}
    jobs += [(g["id"], st, QG, n) for n in range(2)]
for x in D["lines"] + D["prompts"] + D["ladders"] + D["vocab"]:
    jobs.append((x["id"], {"ar": x["ar"], "en": x["en"]}, QT, 0))
for x in D["prompts"]:
    jobs.append((x["id"] + "m", {"ar": x["model"], "en": x["men"]}, QT, 0))
with ThreadPoolExecutor(24) as ex: res = list(ex.map(lambda j: (j[0], j[1], ask(j[1], j[2])["answers"]), jobs))
by = {}
for i, st, a in res: by.setdefault(i, (st, []))[1].append(a)
flag = []
for i, (st, ans) in by.items():
    sc = {q: sum(a[q]["score"] for a in ans) / len(ans) for q in ans[0]}
    low = min(sc.values())
    if low < 2: flag.append((low, i, sc, st, [a[q].get("reason", "") for a in ans for q in a][:2]))
print(len(by), "items checked;", len(flag), "under 2 of 3 on some question")
for low, i, sc, st, why in sorted(flag, key=lambda x: x[0]):
    print(f"\n{i} {({k: round(v, 2) for k, v in sc.items()})}\n  {json.dumps(st, ensure_ascii=False)[:400]}")
# Results (13 Nov 2026): 293 items, 16 under 2. Rewritten: the 'nearest' card (1.73 -> fine), الَّذِي/الَّتِي (1.79 -> 2.0), before/after
# (1.64 -> 2.14), 'the little one', 'in the holidays'. The fox ladder stays passive (1.63; its steps must follow the Arabic order, and
# every other wording scored lower). Not changed: 16g3 (no quick check, so 'check' scored 0), and lines at 1.8-1.99 judged fine.
