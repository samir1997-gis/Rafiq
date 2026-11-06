# Caption for the Islamic months pop carousel (6 Nov 2026, #353).
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/months_caption.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 12-slide Instagram carousel from Rafiq, a small account teaching the Arabic Muslims use, bright colours and drawings: 'What the Islamic months "
       "actually mean'. Muharram = sacred (9:36), Safar = empty (it's said homes stood empty; same letters as zero), Rabi' = spring, Jumada = to freeze, Rajab = "
       "to honour (al-Bukhari 4662), Sha'ban = to branch out (49:13), Ramadan = scorching heat (the only month named in the Qur'an, 2:185), Shawwal = Eid "
       "(six days, Muslim 1164), Dhul-Qa'dah = to sit, Dhul-Hijjah = pilgrimage (22:27). Last slide: how many did you know? Comment /10.")
WHO = {"scroller": "a 21-year-old UK Muslim", "learner": "a 32-year-old learning Arabic", "parent": "a 40-year-old mum teaching her kids"}
T = "#learnarabic #arabic #ramadan #islamiccalendar #muslim"
CAP = {"ramadan": f"Ramadan means 'scorching heat' 🔥 Swipe for what all 12 Islamic months mean. How many did you know? Comment /10 👇 {T}",
       "send": f"Send this to someone who thinks Safar is just 'month 2' 😅 Every Islamic month's name means something. Swipe 👇 {T}",
       "score": f"What the Islamic months actually mean 🌙 Swipe and comment your score /10 👇 Save it 📌 {T}"}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "follow": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to follow the account?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "watch": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to swipe to the last slide?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
