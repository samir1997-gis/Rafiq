# Caption for the "remember" carousel (owner, 8 Nov 2026): death comes on an ordinary day; only your deeds go with you (al-Bukhari 6514);
# make the effort while you have time: learn Arabic, connect with Allah; rafiq-arabic.com.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 4-slide Instagram carousel from Rafiq, a small account teaching the Arabic Muslims use. 1: over a drawn open grave, 'Remember: your death will come on an "
       "ordinary day, in the middle of unfinished plans, and the world will carry on without you.' 2: the only thing you'll take with you is your deeds, with the "
       "hadith 'three follow the dead: his family, wealth and deeds; two return and his deeds remain' (al-Bukhari 6514, Muslim 2960). 3: so make the effort while you "
       "still have time: learn Arabic, understand what you say to Allah, connect with Him. 4: kick-start your Arabic journey at rafiq-arabic.com, free for a week.")
WHO = {"scroller": "a 22-year-old UK Muslim scrolling at night", "learner": "a 34-year-old who has tried to learn Arabic before", "parent": "a 40-year-old UK Muslim dad"}
T = "#reminder #islam #death #learnarabic #muslim"
CAP = {"deeds": f"Your family and your wealth walk back home. Only your deeds stay with you 🤍 (al-Bukhārī 6514) Start today, while you still have time {T}",
       "time": f"An ordinary day, unfinished plans. Make the effort while you still have time 🤍 Learn the words you say to Allah: rafiq-arabic.com {T}",
       "share": f"Send this to someone you want to see in Jannah 🤍 Only our deeds go with us. Start today: learn what you say in your salah {T}"}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "follow": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to follow the account?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "fair": {"type": "score", "instructions": "`ctx` Caption: `h`. Does the caption avoid giving the quiz answers away and avoid overclaiming?", "criteria": ["No", "Partly", "Mostly", "Fully"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
