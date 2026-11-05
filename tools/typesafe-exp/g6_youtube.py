# YouTube Shorts title for g6-i-she (5 Nov 2026, #347): which title gets the click and the watch-through.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 58-second Short from Rafiq, a small account teaching the Arabic Muslims use. Hook: 'MOST people learn Arabic for years before they notice this "
       "trick!' It teaches one letter at the front of a verb: yakulu he eats, aakulu I eat (alif), takulu she eats (ta; also 'you' to a man), then quizzes "
       "yaqra'u he reads: what's 'I read'? what's 'she reads'? 3-2-1 each. Ends: how many did you get? Zero, one or two?")
WHO = {"scroller": "a 22-year-old UK Muslim scrolling Shorts", "learner": "a 34-year-old learning Arabic", "revert": "a 30-year-old revert"}
CAP = {"trick": "The Arabic Trick Most Learners Miss for Years #shorts",
       "letter": "One Letter Changes Who Is Doing It in Arabic #shorts",
       "quiz": "Can You Say “She Reads” in Arabic? Quick Quiz #shorts",
       "eat": "I Eat, She Eats: The Easiest Arabic Verb Trick #shorts"}
Q = {"click": {"type": "score", "instructions": "`ctx` YouTube Shorts title: `h`. Viewer: `who`. How likely are they to stop and watch?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "watch": {"type": "score", "instructions": "`ctx` YouTube Shorts title: `h`. Viewer: `who`. How likely are they to watch to the end?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "trust": {"type": "score", "instructions": "`ctx` YouTube Shorts title: `h`. Viewer: `who`. How sincere and accurate does it feel (not clickbait or misleading)?", "criteria": ["No", "A bit", "Mostly", "Yes"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
