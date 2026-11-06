# Caption for the wudu body parts pop carousel (6 Nov 2026, #353).
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/wudu_caption.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 10-slide Instagram carousel from Rafiq, a small account teaching the Arabic Muslims use, bright colours and drawings: 'Can you do wudu in Arabic?' "
       "hands yad (aghsilu yadayya, I wash my hands), mouth fam, nose anf (an ENT doctor: a nose, ear and throat doctor), face wajh (5:6), elbow mirfaq (5:6), "
       "head ra's (wipe, don't wash, 5:6), ears udhun (same letters as adhan), feet rijl (5:6). Last slide: how many did you know? Comment /8.")
WHO = {"scroller": "a 21-year-old UK Muslim", "learner": "a 32-year-old learning Arabic", "parent": "a 40-year-old dad teaching his kids wudu"}
T = "#learnarabic #arabic #wudu #salah #muslim"
CAP = {"wudu": f"You do wudu five times a day... can you do it in Arabic? 💧 Swipe and comment your score /8 👇 {T}",
       "send": f"Send this to someone teaching their kids wudu 💧 Every step in Arabic, straight from al-Ma'idah 5:6. Save it 📌 {T}",
       "adhan": f"Your ear and the adhan share the same three letters 👂 Swipe for every wudu word in Arabic. How many did you know? 👇 {T}"}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "follow": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to follow the account?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "watch": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to swipe to the last slide?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
