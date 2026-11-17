# Caption for g12-will (17 Nov 2026, #393): the future with sa-: I understand → I will understand, then a quiz on play and sleep.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 60-second Reel from Rafiq, a small account teaching the Arabic Muslims use. Hook: 'MOST people learn Arabic for years before they notice "
       "this trick!' It teaches afhamu I understand, sa-afhamu I will understand, sa-yafhamu he will understand: put sa- on the front of a verb and it "
       "means 'will'. Then it quizzes nal'abu we play: what's 'we will play'? and yanamu he sleeps: what's 'he will sleep'? 3-2-1 each. "
       "Ends: how many did you get? Zero, one or two? Comment below.")
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun", "learner": "a 34-year-old learning Arabic", "parent": "a 38-year-old UK Muslim mum"}
T = "#learnarabic #arabic #arabicgrammar #muslim #arabicforbeginners"
CAP = {"syllable": f"One syllable puts any Arabic verb in the future ⏩ Learn it in 60 seconds, then try the quiz. 0, 1 or 2? 👇 {T}",
       "understand": f"'I understand' → 'I WILL understand' with one sound at the front. Try it on two more verbs 👇 Send this to your Arabic study buddy {T}",
       "future": f"The easiest rule in Arabic grammar? How to say 'will' 👀 Watch, then beat the 3-2-1. Comment your score 👇 {T}"}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "follow": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to follow the account?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "fair": {"type": "score", "instructions": "`ctx` Caption: `h`. Does the caption avoid giving the quiz answers away and avoid overclaiming?", "criteria": ["No", "Partly", "Mostly", "Fully"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
