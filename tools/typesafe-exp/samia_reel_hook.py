# Hook line for the owner's talking-head reel on سَمِعَ اللَّهُ لِمَنْ حَمِدَهُ / رَبَّنا وَلَكَ الْحَمْدُ (said 17 times a day, about 1 in 15 words of a 4-rakah prayer).
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("The first line spoken (over a fast flicker of clips) in a 45-second Instagram reel by a Muslim who teaches Arabic for prayer. "
       "The reel then explains سَمِعَ اللَّهُ لِمَنْ حَمِدَهُ ('Allah hears the one who praises Him') and رَبَّنا وَلَكَ الْحَمْدُ ('Our Lord, and to You belongs all praise'), "
       "said each time you rise from bowing: 17 times a day, about 1 in every 15 words of a four-rakah prayer.")
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun", "learner": "a 34-year-old who has tried to learn Arabic before and given up", "revert": "a 30-year-old revert learning to pray"}
CAP = {"A": "You say this sentence 17 times a day. Do you know what it means?",
       "B": "There's a sentence you say every time you rise from ruku, and most of us have no idea what it means.",
       "C": "1 in every 15 words of your salah is in these two lines.",
       "D": "Every time you stand up from ruku, you're having a conversation. Here's what's being said."}
Q = {"stop": {"type": "score", "instructions": "`ctx` Opening line: `h`. Viewer: `who`. How likely are they to keep watching past the first 3 seconds?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "respect": {"type": "score", "instructions": "`ctx` Opening line: `h`. Viewer: `who`. How respectful and sincere does it feel for a topic about prayer?", "criteria": ["Disrespectful", "A bit flippant", "Respectful", "Very respectful and sincere"]},
     "accurate": {"type": "score", "instructions": "`ctx` Opening line: `h`. How accurate and not misleading is it, given the facts in the context?", "criteria": ["Misleading", "Somewhat misleading", "Accurate", "Fully accurate"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
