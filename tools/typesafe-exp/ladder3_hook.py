# Spoken hook for l3-quran (owner, 8 Nov 2026: "another rendition of the weekly Arabic quiz, with words getting progressively harder",
# the normal cream background): the difficulty ladder with five Qur'an words, rabb → yawm → qulub → yatafakkarun → sundus (the final boss).
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("The first line, shouted word first and on screen from frame 0, of a 50-second Instagram reel from a small account teaching the Arabic Muslims use. "
       "A difficulty ladder of five words from the Qur'an, each harder than the last, a rail showing the share of people still in (90% down to 3%), "
       "a 3-2-1 for each: how do you say 'Lord' (rabb); yawm (day); qulub (hearts); yatafakkarun (they reflect); the final boss sundus (fine silk, al-Kahf 18:31). "
       "It ends: how far did you get? Comment your level.")
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun", "learner": "a 34-year-old learning Arabic", "quran": "a 30-year-old who reads the Qur'an in Arabic without understanding it"}
CAP = {"only": "ONLY 3% get the last one right! How far can you get?",
       "most": "MOST people can't get past level 3 of this Qur'an quiz!",
       "five": "FIVE words from the Qur'an, each one harder. How far can you get?"}
Q = {"stop": {"type": "score", "instructions": "`ctx` Opening line: `h`. Viewer: `who`. How likely are they to keep watching past the first 3 seconds?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "play": {"type": "score", "instructions": "`ctx` Opening line: `h`. Viewer: `who`. How likely are they to play along and comment their score?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "fair": {"type": "score", "instructions": "`ctx` Opening line: `h`. Does the video pay off this line fairly, without overclaiming?", "criteria": ["Misleading", "Partly", "Mostly", "Fully"]}}
jobs = [(k, w) for k in CAP for w in WHO for _ in range(2)]
with ThreadPoolExecutor(24) as ex: res = list(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(a[q]["score"] for (kk, _), a in res if kk == k) / 6 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
