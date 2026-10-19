# Caption for the finished sujood reel (#263). Like the ruku reel it ends on "sign up to rafiq-arabic.com" and "which part next?",
# so it's a 1-in-5 site post. Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/sujood_reel_caption.py
# Result (19 Oct 2026; engage / visit / respect, 3 viewers x 2): A 2.19 / 1.96 / 2.65 (chosen) · C 2.11 / 1.93 / 2.28 · B 2.14 / 1.96 / 2.11.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 91-second Instagram reel by a Muslim who teaches the Arabic of the prayer. Hook: 'When your head is at its lowest, you call Allah "
       "the Most High.' سُبْحانَ رَبِّيَ الْأَعْلى word by word (glory be, my Lord, the Most High), then رَبِّ اغْفِرْ لِي وَارْحَمْنِي sitting between the two "
       "prostrations; over 100 times a day, 43,000 a year; the hadith 'the closest a servant is to his Lord is in sujood, so make lots of du'a' "
       "(Sahih Muslim 482). Ends: sign up to rafiq-arabic.com, and 'which part of the salah should I explain next?'")
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun", "learner": "a 34-year-old who has tried to learn Arabic before and given up", "revert": "a 30-year-old revert learning to pray"}
T = " #salah #sujood #learnarabic #arabic #muslim"
CAP = {"A": "Your head at its lowest, and you call Him the Most High 🤍 Next time you're in sujood, you'll know every word. Which part of the salah should I explain next? 👇 Learn every word you say in salah: free week, link in bio." + T,
       "B": "Over 100 times a day you say this in sujood. Did you know what it meant? Be honest 👇 Send this to someone you pray with 🤍 Learn every word of your salah, free for a week: link in bio." + T,
       "C": "The closest you are to Allah is in sujood, so make lots of du'a (Muslim 482). Now you'll know what you're saying there 🤲 Which part of the salah next? 👇 Free week, link in bio." + T}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "visit": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to tap the link in bio?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "respect": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How respectful and sincere does it feel for a post about prayer?", "criteria": ["Disrespectful", "A bit flippant", "Respectful", "Very respectful and sincere"]}}
jobs = [(k, w) for k in CAP for w in WHO for _ in range(2)]
with ThreadPoolExecutor(18) as ex: r = list(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':4}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(a[q]["score"] for (kk, _), a in r if kk == k) / (2 * len(WHO)) for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:4}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
