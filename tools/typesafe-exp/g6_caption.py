# Caption for g6-i-she (owner, 4 Nov 2026, #347): teach he eats / I eat / she eats, then a quiz on يَقْرَأُ (I read? she reads?).
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 58-second Reel from Rafiq, a small account teaching the Arabic Muslims use. Hook: 'ONE letter tells you WHO is eating in Arabic!' "
       "It teaches yakulu he eats, aakulu I eat (alif at the front), takulu she eats (ta at the front), then quizzes a new verb, yaqra'u he reads: "
       "what's 'I read'? what's 'she reads'? 3-2-1 each. Ends: how many did you get? Zero, one or two? Comment below.")
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun", "learner": "a 34-year-old learning Arabic", "parent": "a 38-year-old UK Muslim mum"}
T = "#learnarabic #arabic #arabicgrammar #quran #muslim"
CAP = {"score": f"One letter tells you who's eating 🍽️ Learn it, then try the quiz: did you get 0, 1 or 2? 👇 Send this to your Arabic study buddy {T}",
       "who": f"Who's eating? In Arabic, ONE letter tells you 👀 Can you do it with 'read'? Comment your score 👇 Send this to your study buddy {T}",
       "quran": f"Learn this one letter and you'll start hearing it all through the Qur'an 📖 Quiz at the end: 0, 1 or 2? 👇 Send this to your study buddy {T}"}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "follow": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to follow the account?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "fair": {"type": "score", "instructions": "`ctx` Caption: `h`. Does the caption avoid giving the quiz answers away and avoid overclaiming?", "criteria": ["No", "Partly", "Mostly", "Fully"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
