# Caption for the q5-numbers quiz (count to 5 in Arabic, then "which number?" twice): original (link) vs reach-first (follow).
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = "A short reel: one to five in Arabic with the digits and audio (wāḥid, ithnān, thalātha, arbaʿa, khamsa), then two rounds of 'which number did you hear?'."
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun", "learner": "a 34-year-old who has tried to learn Arabic before and given up",
       "nonmuslim": "a 29-year-old non-Muslim curious about Arabic"}
T = " #learnarabic #arabic #arabicnumbers #arabicforbeginners #languagelearning"
CAP = {"original": "Count to 5 in Arabic, then test yourself 🔢 Wāḥid, ithnān, thalātha, arbaʿa, khamsa. Then two quick rounds: which number did you hear? Did you get both? 👇 Learn numbers, times and dates with Rafiq, link in bio (free for a week)." + T,
       "follow": "Count to 5 in Arabic, then test yourself 🔢 Wāḥid, ithnān, thalātha, arbaʿa, khamsa. Then two quick rounds: which number did you hear? Did you get both? 👇 Follow for a new Arabic quiz every week." + T}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to comment, save or share?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "follow": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to follow the account?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "content": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How much does it feel like content rather than an ad?", "criteria": ["Pure ad", "Mostly ad", "Mostly content", "Pure content"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / len(WHO) for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
