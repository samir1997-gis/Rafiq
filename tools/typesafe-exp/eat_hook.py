# Spoken hook for g6-i-she (owner, 4 Nov 2026, #347): teach يَأْكُلُ he eats → آكُلُ I eat → تَأْكُلُ she eats, then a quiz on يَقْرَأُ he reads:
# I read? she reads? Callum's voice, the first word shouted and slammed on (FORMATS.md, the g4 standard).
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("The first line, shouted word first and on screen from frame 0, of a 40-second Instagram reel from a small account teaching the Arabic "
       "Muslims use. The reel teaches that one letter at the front of an Arabic verb says who is doing it: yakulu 'he eats', aakulu 'I eat' "
       "(alif at the front), takulu 'she eats' (ta at the front); then quizzes the viewer on a new verb, yaqra'u 'he reads': what's 'I read'? "
       "what's 'she reads'? with a 3-2-1 countdown each, and asks how many they got.")
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun", "learner": "a 34-year-old who has tried to learn Arabic before and given up", "revert": "a 30-year-old revert"}
CAP = {"one": "ONE letter tells you WHO is eating in Arabic!",
       "most": "MOST people learn Arabic for years before they spot this letter!",
       "nobody": "NOBODY told you Arabic hides 'I' and 'she' in one letter!",
       "only": "ONLY 1 in 10 get the second one right!"}
Q = {"stop": {"type": "score", "instructions": "`ctx` Opening line: `h`. Viewer: `who`. How likely are they to keep watching past the first 3 seconds?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "clear": {"type": "score", "instructions": "`ctx` Opening line: `h`. Viewer: `who`. Is it clear and intriguing rather than confusing?", "criteria": ["Confusing", "A bit unclear", "Clear", "Clear and intriguing"]},
     "fair": {"type": "score", "instructions": "`ctx` Opening line: `h`. Does the video pay off this line fairly, without overclaiming?", "criteria": ["Misleading", "Partly", "Mostly", "Fully"]}}
jobs = [(k, w) for k in CAP for w in WHO for _ in range(2)]
with ThreadPoolExecutor(24) as ex: res = list(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(a[q]["score"] for (kk, _), a in res if kk == k) / 6 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
