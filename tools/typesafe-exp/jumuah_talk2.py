# Jumuah talking reel v2: each step said in Arabic then English. 7 steps in the order of the day vs 5 vs the original 3.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
WHO = {"scroller": "a 22-year-old UK Muslim scrolling on a Friday morning", "busy": "a 36-year-old working dad who often misses the Friday sunnahs",
       "revert": "a 30-year-old revert learning about Jumuʿah"}
BASE = ("An Instagram reel, a Muslim man talking to the camera on a Friday, plain edit with captions. He opens in Arabic (praise be to Allah who let us reach "
        "another Jumuʿah), then a checklist; each step he says first as a short Arabic sentence, then in English, some with a quick authentic benefit. ")
V = {"7 in order of the day (55 s)": "Hook on screen: 'Your Jumuʿah checklist, in order'. Steps: ghusl, trim your nails, best clothes and perfume, go early, "
        "send salawat a lot, read Surah al-Kahf, make duʿa in the last hour. Ends: 'Send this to someone to remind them 🤍'",
     "5 (40 s)": "Hook on screen: 'Don't let this Jumuʿah pass without these 5 things'. Steps: ghusl, best clothes and perfume, go early, send salawat a lot, "
        "read Surah al-Kahf. Ends: 'Send this to someone to remind them 🤍'",
     "3 (30 s)": "Hook on screen: 'Don't let this Jumuʿah pass without these 3 things'. Steps: pray Jumuʿah, salawat, Surah al-Kahf. Ends: 'Send this to someone to remind them 🤍'"}
Q = {"finish": {"type": "score", "instructions": "`ctx` `h` Viewer: `who`. How likely are they to watch to the end?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "save": {"type": "score", "instructions": "`ctx` `h` Viewer: `who`. How likely are they to save or share it?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "learn": {"type": "score", "instructions": "`ctx` `h` Viewer: `who`. How much do they feel they learned something useful?", "criteria": ["Nothing", "A little", "Something useful", "A lot"]}}
jobs = [(k, w) for k in V for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": BASE, "h": V[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / len(WHO) for q in Q}) for k in V]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:30}" + "".join(f"{q} {s[q]:.2f}  " for q in Q) + f"total {sum(s.values()):.2f}")
