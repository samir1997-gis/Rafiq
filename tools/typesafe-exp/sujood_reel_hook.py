# Hook line for the owner's talking-head reel on sujood (17 Oct 2026): سُبْحانَ رَبِّيَ الْأَعْلى (said about 100 times a day) and,
# sitting between the two prostrations, رَبِّ اغْفِرْ لِي وَارْحَمْنِي. Same test as samia_reel_hook.py.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("The first line spoken (over a fast flicker of clips) in a 40-second Instagram reel by a Muslim who teaches Arabic for prayer. "
       "The reel then explains سُبْحانَ رَبِّيَ الْأَعْلى ('Glory be to my Lord, the Most High'), said in prostration with your forehead on the floor, "
       "about 100 times a day; الأعلى shares a root with عَلِيّ and تَعالى; then رَبِّ اغْفِرْ لِي وَارْحَمْنِي said sitting between the two prostrations "
       "(اغفر: same root as astaghfirullah; ارحم: same root as ar-Rahman).")
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun", "learner": "a 34-year-old who has tried to learn Arabic before and given up", "revert": "a 30-year-old revert learning to pray"}
CAP = {"A": "When your head is at its lowest, you call Allah the Most High.",
       "B": "You say this over 100 times a day with your forehead on the floor. Do you know what it means?",
       "C": "The lowest you ever go in salah is where you say the highest words.",
       "D": "Every time you go down into sujood, here's what you're actually saying."}
Q = {"stop": {"type": "score", "instructions": "`ctx` Opening line: `h`. Viewer: `who`. How likely are they to keep watching past the first 3 seconds?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "respect": {"type": "score", "instructions": "`ctx` Opening line: `h`. Viewer: `who`. How respectful and sincere does it feel for a topic about prayer?", "criteria": ["Disrespectful", "A bit flippant", "Respectful", "Very respectful and sincere"]},
     "accurate": {"type": "score", "instructions": "`ctx` Opening line: `h`. How accurate and not misleading is it, given the facts in the context?", "criteria": ["Misleading", "Somewhat misleading", "Accurate", "Fully accurate"]}}
jobs = [(k, w) for k in CAP for w in WHO for _ in range(2)]
with ThreadPoolExecutor(24) as ex: res = list(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(a[q]["score"] for (kk, _), a in res if kk == k) / 6 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
