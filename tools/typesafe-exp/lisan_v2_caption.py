# Caption for h3-lisan v2 (28 Oct 2026, #303): the drawn dusk desert, the worm bursting out on "the UNSEEN", Hafez of Shiraz.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/lisan_v2_caption.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 55-second Reel from Rafiq, a small account teaching the Arabic Muslims use, on a drawn dusk desert with two moons: 'Everyone in Dune "
       "chants Lisan al-Gaib... but what does it actually mean in Arabic?' Lisan = tongue/language (the Qur'an came down in a clear Arabic tongue, 26:195); "
       "your turn: al-ghayb from the first page of al-Baqarah, the desert / the unseen / the future, 3-2-1, a sandworm bursts out on 'the UNSEEN'; "
       "so: the tongue of the unseen; Frank Herbert didn't invent it, the Persian poet Hafez (d. 1390) was already called Lisan al-Ghayb. Ask: Muad'Dib or Usul next?")
WHO = {"dune": "a 25-year-old Muslim Dune fan", "learner": "a 32-year-old learning Arabic", "scroller": "a 20-year-old UK Muslim scrolling for fun"}
T = "#dune #duneparttwo #learnarabic #arabic #lisanalgaib"
CAP = {"question": f"Everyone chants Lisan al-Gaib… but what does it actually mean in Arabic? 🏜️ Guess before the 3-2-1, then tell me: Muad'Dib or Usul next? 👇 {T}",
       "fact": f"Lisan al-Gaib is real Arabic, and it's older than Dune 🏜️ Did you know which part is from the Qur'an? Comment 👇 Send this to your Dune friend {T}",
       "hafez": f"Frank Herbert didn't invent “Lisan al-Gaib” 👀 A poet in Shiraz was called it 500 years before Dune. And the word ghayb is on the first page of al-Baqarah 🏜️ Muad'Dib or Usul next? 👇 {T}",
       "tag": f"The tongue of the… 🐛🏜️ What Lisan al-Gaib really means in Arabic (it's in the Qur'an). Tag the friend who quotes Dune all day 👇 {T}"}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "follow": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to follow the account?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "watch": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to watch to the end?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
