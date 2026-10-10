# Captions for the three formula videos (f1-sujood, f2-root, f3-she-eats): content-first with a follow/comment ask.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun", "learner": "a 34-year-old who has tried to learn Arabic before and given up",
       "revert": "a 30-year-old revert learning to pray"}
C = {"f1-sujood": ("A 12-second reel: 'You say this every time you go into sujūd', سُبْحانَ رَبِّيَ الْأَعْلى word by word.",
       ["You say this in every sujūd. Now you'll know what it means 🤍 What do you say in rukūʿ? Comment it 👇 Follow for your salah, word by word. #salah #sujood #learnarabic #arabic #muslim",
        "Glory be to my Lord, the Most High. Say it with meaning in your next sujūd 🤍 Comment what you say in rukūʿ 👇 #salah #sujood #learnarabic #arabic #muslim"]),
     "f2-root": ("A 23-second reel: school, teacher and to study share one Arabic root, د ر س; then 'your turn: what is a كِتاب?' with a countdown.",
       ["Why do school and teacher look alike in Arabic? One root 🤯 Did you get the last one before the 3? Tell me which word to break down next 👇 #learnarabic #arabic #arabicroots #arabicforbeginners #quranarabic",
        "3 words, 1 root 🤯 Once you see Arabic roots, you can't unsee them. Which word should I break down next? 👇 #learnarabic #arabic #arabicroots #arabicforbeginners #quranarabic"]),
     "f3-she-eats": ("A 24-second quiz reel with countdowns: he eats → she eats, he ate → she ate in Arabic.",
       ["He eats → she eats. He ate → she ate. Can you spot the change before the 3? How many did you get? 👇 Follow for a new Arabic quiz every week. #learnarabic #arabic #arabicverbs #arabicforbeginners #languagelearning",
        "One letter turns 'he' into 'she' in Arabic 👀 Two rounds, three seconds each. 0, 1 or 2? 👇 #learnarabic #arabic #arabicverbs #arabicforbeginners #languagelearning"])}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to comment, save or share?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "follow": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to follow?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "respect": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How sincere and fitting does it feel?", "criteria": ["Off-putting", "A bit off", "Fitting", "Very fitting"]}}
jobs = [(v, i, w) for v in C for i in range(2) for w in WHO]
with ThreadPoolExecutor(16) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": C[j[0]][0], "h": C[j[0]][1][j[1]], "who": WHO[j[2]]}, Q)["answers"]), jobs))
for v in C:
    for i in range(2): print(v, "AB"[i], " ".join(f"{q} {sum(r[(v, i, w)][q]['score'] for w in WHO) / len(WHO):.2f}" for q in Q), "total", round(sum(r[(v, i, w)][q]['score'] for w in WHO for q in Q) / len(WHO), 2))
