# Jumuah video (formula, like t1-masjid): Friday = الجُمُعَة from ج م ع "to gather"; جَمْع, جامِعَة; your turn جَمِيع = all.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 25-second reel posted on a Friday: 'Why is Friday called الجُمُعَة?' The root ج م ع means to gather, the day of gathering. The same letters in "
       "جَمْع (combining the prayers) and جامِعَة (a university). Your turn: what does جَمِيع mean? 3-2-1, answer: all. ")
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun on a Friday morning", "learner": "a 34-year-old who has tried to learn Arabic before and given up",
       "revert": "a 30-year-old revert learning to pray"}
A = {"where praying": "It ends: 'Where are you praying Jumuʿah today? 👇'",
     "did you get it": "It ends: 'Did you get it before the 3? 👇'",
     "send to": "It ends: 'Send this to who you're going to Jumuʿah with 🤍'"}
Q = {"comment": {"type": "score", "instructions": "`ctx` `h` Viewer: `who`. How likely are they to comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "share": {"type": "score", "instructions": "`ctx` `h` Viewer: `who`. How likely are they to share or send it?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "fit": {"type": "score", "instructions": "`ctx` `h` Viewer: `who`. How fitting and sincere does it feel for Jumuʿah?", "criteria": ["Off-putting", "A bit off", "Fitting", "Very fitting"]}}
jobs = [(k, w) for k in A for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": A[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / len(WHO) for q in Q}) for k in A]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:16}" + "".join(f"{q} {s[q]:.2f}  " for q in Q) + f"total {sum(s.values()):.2f}")
