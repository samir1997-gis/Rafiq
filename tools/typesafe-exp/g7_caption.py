# Caption for g7-we (owner, 7 Nov 2026): teach he eats / I eat / we eat, then a quiz on al-Fātiḥah's two verbs and the āyah.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 72-second Reel from Rafiq, a small account teaching the Arabic Muslims use. Hook: 'EVERY rak'ah, you say we twice without knowing it!' "
       "It teaches yakulu he eats, aakulu I eat (alif at the front), nakulu we eat (nun at the front), then quizzes ya'budu he worships: what's "
       "'we worship'? and yasta'inu he seeks help: what's 'we seek help'? 3-2-1 each; then al-Fatihah 1:5 is recited, iyyaka na'budu wa iyyaka "
       "nasta'in, the two nun lit: not I, WE, the whole ummah together. Ends: how many did you get? Zero, one or two? Comment below.")
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun", "learner": "a 34-year-old learning Arabic", "parent": "a 38-year-old UK Muslim mum"}
T = "#learnarabic #arabic #fatiha #salah #muslim"
CAP = {"rakah": f"You say 'we' twice in every rak'ah 🤲 One letter, ن, and the whole ummah is in it. Did you get 0, 1 or 2? 👇 Send this to someone you pray with {T}",
       "fatiha": f"Iyyāka naʿbudu wa iyyāka nastaʿīn: not 'I'. WE. Learn the one letter that says it, then try the quiz 👇 Send this to someone you pray with {T}",
       "score": f"One letter turns 'I' into 'we' in Arabic, and you say it in al-Fātiḥah every day. 0, 1 or 2? Comment your score 👇 {T}"}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "follow": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to follow the account?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "fair": {"type": "score", "instructions": "`ctx` Caption: `h`. Does the caption avoid giving the quiz answers away and avoid overclaiming?", "criteria": ["No", "Partly", "Mostly", "Fully"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
