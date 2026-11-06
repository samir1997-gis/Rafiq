# YouTube Shorts titles for zero (h6-zero, #319) and mattress (h9-mattress, #340): which gets the click and the watch-through?
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = {"zero": ("A Short from Rafiq, a small account teaching the Arabic Muslims use: zero comes from the Arabic sifr (empty); Fibonacci took it to Italy "
                "in 1202 as zephirum, then zefiro, zero; sifr also became cipher, a secret code. Quiz: the same letters in al-Baqarah 2:69 mean yellow."),
       "mattress": ("A Short from Rafiq, a small account teaching the Arabic Muslims use: mattress comes from the Arabic matrah, the place you throw yourself "
                    "down (root t-r-h, to throw; ma = the place of, as in masjid); via Sicily, Italian materasso, French materas, English by the 1300s. "
                    "Quiz: the same root in surah Yusuf 12:9, 'throw him'.")}
WHO = {"scroller": "a 22-year-old UK Muslim scrolling Shorts", "learner": "a 34-year-old learning Arabic", "curious": "a 30-year-old who loves word origins"}
CAP = {"zero": {"z1": "Zero Is an Arabic Word #shorts", "z2": "Why Is It Called ZERO? (It’s Arabic) #shorts", "z3": "The Arabic Word Behind Zero and Cipher #shorts"},
       "mattress": {"m1": "Your Mattress Is an Arabic Word #shorts", "m2": "Why Is It Called a Mattress? (It’s Arabic) #shorts", "m3": "You Sleep on an Arabic Word Every Night #shorts"}}
Q = {"click": {"type": "score", "instructions": "`ctx` YouTube Shorts title: `h`. Viewer: `who`. How likely are they to stop and watch?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "watch": {"type": "score", "instructions": "`ctx` YouTube Shorts title: `h`. Viewer: `who`. How likely are they to watch to the end?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "trust": {"type": "score", "instructions": "`ctx` YouTube Shorts title: `h`. Viewer: `who`. How accurate and sincere does it feel (not clickbait)?", "criteria": ["No", "A bit", "Mostly", "Yes"]}}
jobs = [(v, k, w) for v in CAP for k in CAP[v] for w in WHO]
with ThreadPoolExecutor(18) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX[j[0]], "h": CAP[j[0]][j[1]], "who": WHO[j[2]]}, Q)["answers"]), jobs))
for v in CAP:
    rows = [(k, {q: sum(r[(v, k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP[v]]
    for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(v, k, {q: round(x, 2) for q, x in s.items()}, round(sum(s.values()), 2), CAP[v][k])
