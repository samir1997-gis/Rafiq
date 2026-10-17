# Result (17 Oct; keep watching / respectful / pays off, 3 viewers x 2): past 7.76 (chosen) · actually 7.22 · wrong 6.00 · nobody 5.12.
# Spoken hook for m1-mashallah (owner, 17 Oct 2026: redo the mashallah video in the standard; Callum explains, Rafiq says the Arabic).
# The video: ما شاءَ اللهُ word by word ("what Allah has willed"), شاءَ is past tense so it's for good you see, the future is
# إِنْ شاءَ اللهُ; the root ش ي ء (مَشِيئَة, شَيْء); al-Kahf 18:39; a quick "mashallah or inshallah?" test with 3-2-1.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("The first line of a 35-second Instagram reel from a small account teaching the Arabic Muslims use, shouted word first, "
       "on screen from frame 0. The reel then breaks down ما شاءَ اللهُ word by word ('what Allah has willed'), explains the verb is past tense "
       "so it's said for something good that's already there, while the future takes in shā' Allāh; shows the root (will, thing); quotes "
       "Surah al-Kahf 18:39 where it's taught; ends with a quick test: 'See you at Jumuʿah tomorrow': mashallah or inshallah?")
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun", "learner": "a 34-year-old who has tried to learn Arabic before and given up", "revert": "a 30-year-old revert learning to pray"}
CAP = {"wrong": "MOST people say mashallah in the WRONG place!",
       "actually": "Do you ACTUALLY know what mashallah means?",
       "past": "MOST people don't know mashallah is in the PAST tense!",
       "nobody": "NOBODY tells you when NOT to say mashallah!"}
Q = {"stop": {"type": "score", "instructions": "`ctx` Opening line: `h`. Viewer: `who`. How likely are they to keep watching past the first 3 seconds?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "respect": {"type": "score", "instructions": "`ctx` Opening line: `h`. Viewer: `who`. Does it feel respectful about a religious phrase rather than mocking people?", "criteria": ["Disrespectful", "A bit preachy or mocking", "Respectful", "Respectful and intriguing"]},
     "accurate": {"type": "score", "instructions": "`ctx` Opening line: `h`. Does the video pay off this line, so it doesn't feel like a cheat?", "criteria": ["Cheat", "Partly", "Mostly", "Fully"]}}
jobs = [(k, w) for k in CAP for w in WHO for _ in range(2)]
with ThreadPoolExecutor(24) as ex: res = list(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(a[q]["score"] for (kk, _), a in res if kk == k) / 6 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
