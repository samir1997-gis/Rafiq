# Caption for the days of the week pop carousel (2 Nov 2026, #322).
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/days_caption.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 9-slide Instagram carousel from Rafiq, a small account teaching the Arabic Muslims use, bright colours and drawings: 'The Arabic week is... just numbers?' "
       "Sunday al-ahad = one, Monday al-ithnayn = two, Tuesday ath-thulathaa' = three, Wednesday al-arbi'aa' = four, Thursday al-khamees = five, then the pattern breaks: "
       "Friday al-jumu'ah = to gather (62:9), Saturday as-sabt = rest (78:9). Notes: the Prophet fasted Mondays (Muslim 1162) and Mondays and Thursdays (at-Tirmidhi 747). "
       "Last slide: how many did you know? Comment /7.")
WHO = {"scroller": "a 21-year-old UK Muslim", "learner": "a 32-year-old learning Arabic", "parent": "a 40-year-old dad teaching his kids"}
T = "#learnarabic #arabic #jummah #arabicwords #muslim"
CAP = {"numbers": f"The Arabic week is just numbers 🤯 Sunday is 'one', Monday 'two'... until Friday breaks the pattern. Did you know? 👇 {T}",
       "send": f"Send this to someone who didn't know Monday means 'two' in Arabic 😅 Swipe to Friday: that's where it gets good 👇 {T}",
       "score": f"How many Arabic days did you know? Swipe and comment your score /7 👇 Save it 📌 {T}"}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "follow": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to follow the account?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "watch": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to swipe to the last slide?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
