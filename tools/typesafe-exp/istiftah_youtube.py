# YouTube Shorts title for the duʿāʾ al-istiftāḥ video (owner, 9 Nov 2026).
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = {"dua": ("A Short from Rafiq, a small account teaching the Arabic Muslims use: 'Have you ever seen the imam do this before? I always wondered what the imam "
               "was reciting between Allahu akbar and al-Fatiha... it's dua al-istiftah, the opening supplication, part of the Sunnah, and it's easy to learn.' "
               "Then the Rafiq app: subhanaka Allahumma wa bihamdik... with its meaning and recitation, then word by word.")}
WHO = {"scroller": "a 22-year-old UK Muslim scrolling Shorts", "learner": "a 34-year-old learning Arabic", "masjid": "a 40-year-old who prays at the masjid"}
CAP = {"dua": {"d1": "What the Imam Says Before al-Fatiha #shorts", "d2": "The Du'a Most People Skip in Salah #shorts", "d3": "Learn the Opening Du'a of Salah (Du'a al-Istiftah) #shorts"}}
Q = {"click": {"type": "score", "instructions": "`ctx` YouTube Shorts title: `h`. Viewer: `who`. How likely are they to stop and watch?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "watch": {"type": "score", "instructions": "`ctx` YouTube Shorts title: `h`. Viewer: `who`. How likely are they to watch to the end?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "trust": {"type": "score", "instructions": "`ctx` YouTube Shorts title: `h`. Viewer: `who`. How accurate and sincere does it feel (not clickbait)?", "criteria": ["No", "A bit", "Mostly", "Yes"]}}
jobs = [(v, k, w) for v in CAP for k in CAP[v] for w in WHO]
with ThreadPoolExecutor(18) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX[j[0]], "h": CAP[j[0]][j[1]], "who": WHO[j[2]]}, Q)["answers"]), jobs))
for v in CAP:
    rows = [(k, {q: sum(r[(v, k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP[v]]
    for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(v, k, {q: round(x, 2) for q, x in s.items()}, round(sum(s.values()), 2), CAP[v][k])
