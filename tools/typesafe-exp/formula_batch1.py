# Hooks and closing asks for three new videos in the winning formula (brag-quiz/IDEAS.md, "What our best videos do").
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun", "learner": "a 34-year-old who has tried to learn Arabic before and given up",
       "revert": "a 30-year-old revert learning to pray"}
V = {
 "sujood": ("A 15-second reel: the Arabic phrase سُبْحانَ رَبِّيَ الْأَعْلى shown and said, then word by word (Glory be to · my Lord · the Most High), then a question.",
   {"hook A + ask ruku": "Hook: 'You say this every time your forehead touches the ground'. Ends: 'What do you say in rukūʿ instead? Comment it 👇'",
    "hook B + ask ruku": "Hook: 'You say this 24 times in every four-rakʿah prayer'. Ends: 'What do you say in rukūʿ instead? Comment it 👇'",
    "hook A + ask next": "Hook: 'You say this every time your forehead touches the ground'. Ends: 'Which line should I break down next? 👇'"}),
 "root": ("A 25-second reel about Arabic roots: school (مَدْرَسَة), teacher (مُدَرِّس) and to study (دَرَسَ) share the letters د ر س. Then 'your turn': كَتَبَ = to write, so what is a كِتاب? 3-2-1 countdown, answer: a book.",
   {"why alike + did you get it": "Hook: 'Why do school and teacher look alike in Arabic?'. Ends: 'Got it before the 3? Comment ✅ 👇'",
    "3 words 1 root + did you get it": "Hook: 'School, teacher, to study: one Arabic root'. Ends: 'Got it before the 3? Comment ✅ 👇'",
    "why alike + what word next": "Hook: 'Why do school and teacher look alike in Arabic?'. Ends: 'Which word's root should I show next? 👇'"}),
 "verb": ("A 23-second quiz reel with 3-2-1 countdowns: 'If يَأْكُلُ is he eats, what's she eats?' (answer تَأْكُلُ, the change ي → ت), then 'If أَكَلَ is he ate, what's she ate?' (answer أَكَلَتْ, add تْ; the trap أَكَلْتُ is I ate).",
   {"he-she + score": "Ends: 'How many did you get? 0, 1 or 2? 👇'",
    "he-she + trap": "Ends: 'Did the second one catch you out? 👇'"})}
Q = {"stop": {"type": "score", "instructions": "`ctx` `h` Viewer: `who`. How likely are they to watch to the end?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "comment": {"type": "score", "instructions": "`ctx` `h` Viewer: `who`. How likely are they to comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "share": {"type": "score", "instructions": "`ctx` `h` Viewer: `who`. How likely are they to share or save it?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]}}
jobs = [(v, k, w) for v in V for k in V[v][1] for w in WHO]
with ThreadPoolExecutor(16) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": V[j[0]][0], "h": V[j[0]][1][j[1]], "who": WHO[j[2]]}, Q)["answers"]), jobs))
for v in V:
    print(v); rows = [(k, {q: sum(r[(v, k, w)][q]["score"] for w in WHO) / len(WHO) for q in Q}) for k in V[v][1]]
    for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"  {k:34}" + "".join(f"{q} {s[q]:.2f}  " for q in Q) + f"total {sum(s.values()):.2f}")
