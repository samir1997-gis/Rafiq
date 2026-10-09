# Owner's talking reel: you can understand your salah without years of Arabic. Facts (salah-data.js + salah.js REPS, 4-rakah prayer
# without the surah): 425 words, 90 different; top 5 = 34%, top 20 = 56%.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 40-second Instagram reel, a Muslim man talking to the camera with the template edit (titles, captions, a word-wall graphic). Message: you don't need "
       "years of Arabic to start understanding your salah. A four-rakah prayer, without the surah you choose, is 425 words but only 90 different words; "
       "the 5 most common (subhana, rabbiya, Allah, al-aʿla, akbar) are a third of everything you say; the top 20 are more than half. Start with those. ")
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun", "learner": "a 34-year-old who has tried to learn Arabic before and given up",
       "revert": "a 30-year-old revert learning to pray"}
V = {"A did-you-know + follow": "Opens: 'Did you know you can start understanding your salah without spending years studying Arabic?' Ends: 'Follow, and I'll teach you those 20 words, one at a time.'",
     "B 425/90 + follow": "Opens: 'Your salah is 425 words. But only 90 different ones.' Ends: 'Follow, and I'll teach you those 20 words, one at a time.'",
     "C 5 words a third + follow": "Opens: '5 words make up a third of your salah.' Ends: 'Follow, and I'll teach you those 20 words, one at a time.'",
     "B 425/90 + app": "Opens: 'Your salah is 425 words. But only 90 different ones.' Ends: 'That's exactly how Rafiq teaches it: the most-said words first. Link in bio.'"}
Q = {"stay": {"type": "score", "instructions": "`ctx` `h` Viewer: `who`. How likely are they to keep watching past the first 3 seconds?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "hope": {"type": "score", "instructions": "`ctx` `h` Viewer: `who`. How much does it make them feel understanding their salah is within reach?", "criteria": ["Not at all", "A little", "Quite a lot", "Very much"]},
     "follow": {"type": "score", "instructions": "`ctx` `h` Viewer: `who`. How likely are they to follow, save or share?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "trust": {"type": "score", "instructions": "`ctx` `h` Viewer: `who`. How much do they trust it (not hype, not an ad)?", "criteria": ["Distrust", "Wary", "Trust", "Fully trust"]}}
jobs = [(k, w) for k in V for w in WHO]
with ThreadPoolExecutor(16) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": V[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / len(WHO) for q in Q}) for k in V]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:28}" + "".join(f"{q} {s[q]:.2f}  " for q in Q) + f"total {sum(s.values()):.2f}")
