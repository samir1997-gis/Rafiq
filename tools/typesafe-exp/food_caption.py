# Caption for the food & drink pop carousel (2 Nov 2026, #321).
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/food_caption.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("An 8-slide Instagram carousel from Rafiq, a small account teaching the Arabic Muslims use, bright colours and drawings: 'Can you order all 6 in Arabic?' "
       "water maa', bread khubz, dates tamr, tea shaay, milk haleeb, coffee qahwa, each with a sentence from the course and a note (we made every living thing from water 21:30; "
       "in Egypt bread is 'aysh, life; breaking the fast with dates, Abu Dawud 2356; shaay and chai from Chinese cha, tea from te; the Qur'an says laban 16:66; qahwa to coffee). "
       "Last slide: how many did you know? Comment /6.")
WHO = {"foodie": "a 25-year-old UK Muslim who loves cafes", "learner": "a 32-year-old learning Arabic", "parent": "a 40-year-old mum teaching her kids Arabic words"}
T = "#learnarabic #arabic #arabicwords #food #halal"
CAP = {"score": f"Can you order all 6 in Arabic? ☕ Swipe and count your score, then comment it 👇 Save it for your next trip 📌 {T}",
       "teaorcoffee": f"Shaay or qahwa? ☕ 6 food & drink words in Arabic, with the Sunnah of dates at iftar. Tea or coffee: comment 👇 {T}",
       "send": f"Send this to the friend who always orders for you 😅 Water, bread, dates, tea, milk and coffee in Arabic. How many did you know? 👇 {T}"}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "follow": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to follow the account?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "watch": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to swipe to the last slide?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
