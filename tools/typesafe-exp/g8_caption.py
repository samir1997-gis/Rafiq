# Caption for g8-you (8 Nov 2026, #354): teach he eats / you eat (to a man) / you eat (to a woman), then a quiz on drink and go.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 64-second Reel from Rafiq, a small account teaching the Arabic Muslims use. Hook: 'MOST people learn Arabic for years before they notice "
       "this trick!' It teaches ya'kulu he eats, ta'kulu you eat (to a man: taa at the front; it's also 'she eats', the sentence tells you which), "
       "ta'kuleena you eat (to a woman: taa at the front and -eena at the end), then quizzes yashrabu he drinks: what's 'you drink', to a man? and "
       "yadh-habu he goes: what's 'you go', to a woman? 3-2-1 each. Ends: how many did you get? Zero, one or two? Comment below.")
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun", "learner": "a 34-year-old learning Arabic", "parent": "a 38-year-old UK Muslim mum"}
T = "#learnarabic #arabic #arabicgrammar #muslim #arabicforbeginners"
CAP = {"woman": f"In Arabic, 'you' changes when you're talking to a woman 👀 One letter at the front, two at the end. Did you get 0, 1 or 2? 👇 {T}",
       "buddy": f"Learn the 'you' trick in 60 seconds, then try the quiz 👇 Send this to your Arabic study buddy {T}",
       "score": f"Talking to a man or a woman? Arabic tells you in the verb. 0, 1 or 2? Comment your score 👇 {T}"}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "follow": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to follow the account?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "fair": {"type": "score", "instructions": "`ctx` Caption: `h`. Does the caption avoid giving the quiz answers away and avoid overclaiming?", "criteria": ["No", "Partly", "Mostly", "Fully"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
