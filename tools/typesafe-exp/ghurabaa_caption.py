# Caption for the strangers carousel (Muslim 145, root غ ر ب). Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/ghurabaa_caption.py
# Result (19 Oct; comment / share / trust, target + revert x2): home 2.33 / 2.50 / 2.90 (chosen) · tuba 2.28 / 2.67 / 2.71 · maghrib 2.30 / 2.62 / 2.64.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("An Instagram photo carousel from a small account teaching the Arabic Muslims use: 'What does a stranger have to do with Maghrib?'; the "
       "hadith 'Islam began as something strange… so glad tidings to the strangers' (Muslim 145) word by word; the root غ ر ب, to go away like the "
       "setting sun; its family (the sun set, Maghrib, west, stranger, being away from home, strangers); 'Be in this world as if you were a stranger or "
       "a traveller' (Bukhari 6416): our home is somewhere else. Ends: 'Did you know Maghrib and stranger were family?'. Caption under it: ")
WHO = {"target": "a 27-year-old UK Muslim who prays but doesn't understand the Arabic", "revert": "a 31-year-old revert learning Arabic"}
T = " #hadith #learnarabic #arabic #muslim #islam"
C = {"maghrib": "Next time you pray Maghrib, remember the word for the sunset and the word for a stranger come from the same place: going away 🌅 Did you know they were family? 👇 Send this to someone who feels like a stranger 🤍" + T,
     "tuba": "فَطُوبى لِلْغُرَباءِ: glad tidings to the strangers. If you've ever felt like you don't fit in for holding on to your deen, this one is for you 🤍 Save it 📌 and send it to someone who needs it." + T,
     "home": "A stranger is someone far from home. The Prophet ﷺ told us to live in this world like one, because our home is somewhere else 🤍 Which slide stayed with you? 👇" + T}
Q = {"comment": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. How likely are they to comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "share": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. How likely are they to save or send it to a friend?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "trust": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. Does the caption feel sincere and respectful for a post about a hadith?", "criteria": ["No", "A bit", "Mostly", "Yes"]}}
jobs = [(k, w) for k in C for w in WHO for _ in range(2)]
with ThreadPoolExecutor(12) as ex: res = list(ex.map(lambda j: (j, ask({"ctx": CTX, "c": C[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
for k in C:
    s = {q: sum(a[q]["score"] for (kk, _), a in res if kk == k) / 4 for q in Q}
    print(f"{k:8} comment {s['comment']:.2f}  share {s['share']:.2f}  trust {s['trust']:.2f}  total {sum(s.values()):.2f}")
