# Caption for h6-zero (2 Nov 2026, #319): the story of a word, drawn over Baghdad at night, numbers drifting in the sky.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/zero_caption.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 57-second Reel from Rafiq, a small account teaching the Arabic Muslims use, drawn over Baghdad at night: 'Zero comes from an Arabic word, and so does the "
       "word for a secret code.' sifr = empty; when Indian numbers reached Baghdad the sign for nothing was called sifr. In 1202 Fibonacci took it to Italy as "
       "zephirum, which shrank to zefiro and then zero. A second road: cifra, then cipher, which meant zero, then any number, then a secret code. Your turn: the "
       "same letters in al-Baqarah 2:69, a ___ cow: empty, zero or yellow? 3-2-1: YELLOW, a bright yellow cow. Ask: what's your favourite number? zero doesn't count.")
WHO = {"student": "a 19-year-old UK Muslim studying maths", "learner": "a 32-year-old learning Arabic", "scroller": "a 24-year-old UK Muslim scrolling at night"}
T = "#learnarabic #arabic #maths #history #quran"
CAP = {"number": f"What's your favourite number? Zero doesn't count 😅 It's Arabic, and so is the word cipher. Did you get the cow? 👇 {T}",
       "question": f"Why is it called ZERO? It's from the Arabic sifr: empty 🌙 Then it took a second road and became 'cipher'. Comment your favourite number 👇 {T}",
       "send": f"Send this to your maths teacher 🧮 Zero and cipher both come from one Arabic word, and the same letters give you a yellow cow in al-Baqarah 👇 {T}"}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "follow": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to follow the account?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "watch": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to watch to the end?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
