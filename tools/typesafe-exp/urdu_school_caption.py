# Caption for h7-urdu-school (2 Nov 2026, #320): If you speak Urdu, you already know these Arabic words, part 2, in the classroom.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/urdu_school_caption.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 62-second Reel from Rafiq, a small account teaching the Arabic Muslims use. Hook, shouted: 'HUNDREDS of Arabic words... if you speak Urdu, you already "
       "know them.' Part 2 of a series (part 1 was at the doctor's). A drawn classroom: talib (student, Urdu talib-e-ilm), ilm (knowledge), kitab (book), qalam (pen), "
       "hisab (maths), imtihan (exam), each with its Urdu spelling and a counter; the first verses of the Qur'an mention the pen, al-Alaq 96:4. Ask: how many did you get? "
       "Comment your score and say where we should go next.")
WHO = {"urdu": "a 22-year-old British Pakistani who speaks Urdu at home", "parent": "a 38-year-old Urdu-speaking mum whose kids learn Arabic", "learner": "a 30-year-old learning Arabic"}
T = "#urdu #learnarabic #arabic #pakistani #desi"
CAP = {"score": f"If you speak Urdu, you already know these 6 Arabic words 📚 How many did you get? Comment your score, and tell us where to go next 👇 {T}",
       "part2": f"Part 2: the classroom ✏️ Kitab, qalam, ilm, imtihaan... all Arabic! Part 1 was the doctor's. Where should we go next? 👇 {T}",
       "tag": f"Tag the Urdu speaker who thinks they don't know any Arabic 😅 Six words from the classroom, and the first verses of the Qur'an mention one of them 👇 {T}"}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "follow": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to follow the account?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "watch": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to watch to the end?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
