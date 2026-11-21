# Hook for a tawakkul vs tawākul reel (21 Nov 2026): one sound turns trust in Allah into laziness; the camel hadith (al-Tirmidhī 2517).
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 50-second Reel from Rafiq, a small account teaching the Arabic Muslims use, in its usual style: a spoken hook with one word shouted, "
       "words on screen one at a time. It shows tawakkul (trusting Allah after doing your part, Qur'an 65:3) and tawaakul (idle dependence, leaving it "
       "to others and doing nothing): same root, one sound changes (a doubled k versus a long aa). The camel hadith: 'Tie it, and trust' (al-Tirmidhi 2517). "
       "A quiz: three short scenes, tawakkul or tawaakul? 3-2-1 each. Ends: which one are you this week? Comment.")
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun", "learner": "a 34-year-old learning Arabic", "parent": "a 40-year-old UK Muslim mum"}
H = {"one_sound": "ONE sound turns trusting Allah into being LAZY.",
     "camel": "Should you tie your camel, or trust Allah? The Prophet ﷺ gave a two-word answer.",
     "fake": "Half the people saying 'I've got tawakkul' actually mean a DIFFERENT word.",
     "exam": "You didn't revise and said 'I'll put my trust in Allah'? Arabic has a word for that, and it's NOT tawakkul."}
Q = {"watch": {"type": "score", "instructions": "`ctx` The hook: `h`. Viewer: `who`. How likely are they to keep watching past the first three seconds?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "respect": {"type": "score", "instructions": "`ctx` The hook: `h`. Viewer: `who`. How respectful is it of the religion?", "criteria": ["Disrespectful", "Somewhat flippant", "Respectful", "Very respectful"]},
     "engage": {"type": "score", "instructions": "`ctx` The hook: `h`. Viewer: `who`. How likely are they to comment, save or share by the end?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]}}
jobs = [(k, w) for k in H for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": H[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in H]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
