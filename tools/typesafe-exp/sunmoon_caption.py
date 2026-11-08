# Caption for the sun and moon letters pop carousel (8 Nov 2026, #354).
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 10-slide Instagram carousel from Rafiq, a small account teaching the Arabic Muslims use, bright colours and drawings: 'When do you NOT say "
       "the L in al-?' ash-shams (91:1, sun letter, silent L), al-qamar (91:2, moon letter), as-salamu 'alaykum, al-kitab (2:2), ar-Rahman ar-Rahim (1:3), "
       "al-hamdu (1:2), an-nur (2:257), al-bayt (106:3); the 14 sun letters listed. Last slide: how many did you know? Comment /8.")
WHO = {"scroller": "a 21-year-old UK Muslim", "learner": "a 32-year-old learning Arabic", "parent": "a 40-year-old mum teaching her kids to read Qur'an"}
T = "#learnarabic #arabic #tajweed #quran #arabicforbeginners"
CAP = {"salam": f"Why is it 'as-salāmu ʿalaykum' and not 'al-salām'? ☀️ Sun letters swallow the L. Swipe for the rule 👇 {T}",
       "fatiha": f"al-ḥamdu but ar-Raḥmān? 🌙☀️ The one rule behind the L of 'al-'. How many did you know? Comment /8 👇 {T}",
       "save": f"Sun letters vs moon letters, with examples you already say every day ☀️🌙 Save this 📌 and send it to someone learning to read Qur'an {T}"}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "follow": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to follow the account?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "watch": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to swipe to the last slide?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
