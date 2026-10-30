# Caption for the owner's weekly Arabic quiz (30 Oct 2026, #309): five words found all over the Qur'an (qala, kana, amanu, athath, ja'ala),
# him floating at the bottom, four options each, a countdown, the answer read out. Reach first (IDEAS.md, How we post).
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/quiz_1030_caption.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 50-second Reel from Rafiq (an Arabic-learning account for Muslims): 'STOP! It's time for your weekly Arabic quiz: words frequently mentioned "
       "in the Qur'an.' Five questions with four options and a countdown, the answer read out: which means 'he said' (qala), what does kana mean (he was), "
       "amanu (they believed), a tricky one, athath (furnishings, 16:80), which means 'he made' (ja'ala). Ends: how many did you get? Comment /5.")
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun", "learner": "a 34-year-old who has wanted to learn Arabic for years",
       "parent": "a 41-year-old Muslim parent who reads Qur'an but doesn't understand it"}
T = "#learnarabic #arabic #quran #arabicquiz #muslim"
CAP = {"Q1": f"5 words you'll find all over the Qur'an 📖 How many did you get? Comment your score /5 👇 {T}",
       "Q2": f"Weekly Arabic quiz ⏱️ Number 4 catches almost everyone 👀 Comment your score /5 and send it to someone who'd get 0 {T}",
       "Q3": f"You read these words every time you open the Qur'an… but do you know what they mean? 📖 Score yourself /5 👇 Follow for a new quiz every week {T}",
       "Q4": f"Can you beat 3/5? ⏱️ Five Qur'an words, one tricky one. Drop your score 👇 {T}"}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to comment, share or save?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "follow": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to follow the account?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "watch": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to watch to the end?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':6}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:6}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
