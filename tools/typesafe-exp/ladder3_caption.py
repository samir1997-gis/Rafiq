# Caption for l3-quran (owner, 8 Nov 2026): the difficulty ladder, five words from the Qur'an, each harder.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 62-second Reel from Rafiq, a small account teaching the Arabic Muslims use. Hook: 'FIVE words from the Qur'an, each one harder. How far can you get?' "
       "A ladder with a rail of the share still in (90% to 3%), a 3-2-1 each: how do you say Lord (rabb); yawm (day); qulub (hearts); yatafakkarun (they reflect); "
       "the final boss sundus (fine green silk, al-Kahf 18:31). Ends: how far did you get? Comment your level.")
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun", "learner": "a 34-year-old learning Arabic", "quran": "a 30-year-old who reads the Qur'an in Arabic without understanding it"}
T = "#quran #learnarabic #arabic #quiz #muslim"
CAP = {"level": f"5 words from the Qur'an, each one harder 📖 What level did you reach? Comment it 👇 Send this to your Qur'an study buddy {T}",
       "boss": f"Level 5 is the final boss 😈 Most people stop at level 3. How far did you get? 👇 {T}",
       "quran": f"You've read these words in the Qur'an. Do you know what they mean? 📖 Comment your level 👇 {T}"}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "follow": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to follow the account?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "fair": {"type": "score", "instructions": "`ctx` Caption: `h`. Does the caption avoid giving the quiz answers away and avoid overclaiming?", "criteria": ["No", "Partly", "Mostly", "Fully"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
