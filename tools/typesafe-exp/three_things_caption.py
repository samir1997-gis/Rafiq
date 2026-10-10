# Caption for the owner's reel "3 things to learn Arabic" (a tutor, immerse, daily recall in 5-10 minute bursts; ends on Rafiq).
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 56-second talking-head reel by the founder of Rafiq (an Arabic-learning web app): 'If you want to learn Arabic, do these 3 things: "
       "1) study with a tutor or an institution, 2) immerse yourself, use every word you learn, listen to podcasts, 3) practise daily, recall what you learned, "
       "in 5-10 minute bursts every day, which is exactly what Rafiq is designed to do.' Cinematic edit with big titles.")
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun", "learner": "a 34-year-old who has tried to learn Arabic before and given up", "revert": "a 30-year-old revert learning to pray"}
CAP = {"A": "3 things that actually work if you want to learn Arabic 📚 Which one are you missing? 👇 Save this for later. #learnarabic #arabic #studyarabic #muslim #islam",
       "B": "Tried learning Arabic and gave up? Do these 3 things 📚 Number 3 is the one most people skip. Save this 📌 #learnarabic #arabic #studyarabic #muslim #islam",
       "C": "If you want to learn Arabic, do these 3 things 📚 Rafiq does number 3 for you: 5-10 minutes a day, free for a week, link in bio. #learnarabic #arabic #studyarabic #muslim #islam"}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "follow": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to follow the account?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "content": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How much does it feel like content rather than an ad?", "criteria": ["Pure ad", "Mostly ad", "Mostly content", "Pure content"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
