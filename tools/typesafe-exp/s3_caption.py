# Caption for 'Salah word by word #3': سَمِعَ اللَّهُ لِمَنْ حَمِدَهُ, word by word, ending "What do you reply? Comment it". Reach first.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 15-second TikTok/Instagram video from Rafiq, a small Arabic-learning account: 'You say this every time you rise from rukuu', "
       "سَمِعَ اللَّهُ لِمَنْ حَمِدَهُ word by word (hears, Allah, the one who, praises Him), 'Allah hears the one who praises Him', then 'What do you reply? Comment it'. Part 3 of a series 'Salah word by word'.")
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun", "parent": "a 38-year-old practising mum who wants to understand her salah", "revert": "a 30-year-old revert learning to pray"}
CAP = {"A": "You say it every time you rise from rukūʿ… but do you know what it means? 🤲 Allah hears the one who praises Him. So what do you reply? Comment it 👇 Follow for #4 #salah #learnarabic #arabic #muslim #islam",
       "B": "Next time you rise from rukūʿ, you'll know Who is listening 🤲 سَمِعَ اللَّهُ لِمَنْ حَمِدَهُ, “Allah hears the one who praises Him.” What do you say back? 👇 Salah word by word, part 3. Follow for the next one. #salah #learnarabic #arabic #muslim #islam",
       "C": "Salah word by word #3 🕌 سَمِعَ اللَّهُ لِمَنْ حَمِدَهُ. Comment the reply 👇 #salah #learnarabic #arabic #muslim #islam"}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "follow": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to follow the account?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "content": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How much does it feel like content rather than an ad?", "criteria": ["Pure ad", "Mostly ad", "Mostly content", "Pure content"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
