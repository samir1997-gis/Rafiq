# Caption for the he → she (ة) pop carousel (8 Nov 2026, #354).
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 9-slide Instagram carousel from Rafiq, a small account teaching the Arabic Muslims use, bright colours and drawings: 'He to she in Arabic: just "
       "one letter'. mu'allim/mu'allima teacher, talib/taliba student (taalibaat), tabib/tabiba doctor (said -t before another word), muhandis/muhandisa "
       "engineer, kabir/kabira big (the car is a she), jadid/jadida new (the bag is a she), watch out: umm mum is feminine with no taa marbuta, also bint, "
       "shams. Last slide: how many did you know? Comment /7.")
WHO = {"scroller": "a 21-year-old UK Muslim", "learner": "a 32-year-old learning Arabic", "parent": "a 40-year-old mum learning with her daughter"}
T = "#learnarabic #arabic #arabicgrammar #muslim #arabicforbeginners"
CAP = {"letter": f"One letter turns 'he' into 'she' in Arabic 👀 Teacher, student, doctor... and even your car. Swipe 👇 How many did you know? /7 {T}",
       "car": f"In Arabic, your car is a 'she' 🚗 Swipe for the one-letter rule (and the words that break it) 👇 {T}",
       "save": f"He → she in Arabic: add ة. Save this 📌 and send it to someone learning with you {T}"}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "follow": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to follow the account?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "watch": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to swipe to the last slide?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
