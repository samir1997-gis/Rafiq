# Caption for the finished rising-from-ruku reel (#233). The owner ended it on "sign up to rafiqarabic.com", so it's a 1-in-5 site post.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 73-second Instagram reel by a Muslim who teaches the Arabic of the prayer: every time you stand up from ruku you're having a conversation; "
       "سَمِعَ اللَّهُ لِمَنْ حَمِدَهُ (Allah hears the one who praises Him) word by word, then you answer رَبَّنا وَلَكَ الْحَمْدُ; the two lines are 7 words, 1 in 15 of the words "
       "of a four-rakah prayer, said 17 times a day, over 6,000 a year; even the name Muhammad means the praised one. Ends: sign up to rafiq-arabic.com.")
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun", "learner": "a 34-year-old who has tried to learn Arabic before and given up", "revert": "a 30-year-old revert learning to pray"}
T = " #salah #learnarabic #arabic #quranarabic #muslim"
CAP = {"A": "You say this 17 times a day. Now you'll know what it means 🤲 Save it for your next salah. Learn every word you say in salah: free week, link in bio." + T,
       "B": "Every time you rise from ruku, you're in a conversation. Sami'a Allahu liman hamidah… Rabbana wa lakal hamd. Send this to someone who prays 🤍 Learn every word of your salah, free for a week: link in bio." + T,
       "C": "7 words. 17 times a day. 1 in every 15 words of your prayer. Do you know what they mean? Learn every word you say in salah with Rafiq, free week, link in bio." + T}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "visit": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to tap the link in bio?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "respect": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How respectful and sincere does it feel for a post about prayer?", "criteria": ["Disrespectful", "A bit flippant", "Respectful", "Very respectful and sincere"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / len(WHO) for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
