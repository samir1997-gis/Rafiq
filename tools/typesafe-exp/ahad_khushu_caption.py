# Caption for the Aḥad video with the khushūʿ hook on the front (12 Nov 2026): "Before you pray another salah without khushūʿ, did you know this?"
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A Reel from Rafiq, a small account teaching the Arabic Muslims use. It opens with the presenter: 'Before you pray another salah without khushu, "
       "did you know this?' Then: Bilal, a slave in Makkah, dragged out, laid on burning sand with a boulder on his chest, told to deny Muhammad, answers "
       "with one word, ahad; why ahad and not wahid (the One with no second); the word you say in Surat al-Ikhlas; the whole of tawhid in one word.")
WHO = {"scroller": "a 22-year-old UK Muslim scrolling", "learner": "a 34-year-old learning Arabic", "sister": "a 27-year-old UK Muslim woman"}
T = "#khushu #bilal #tawhid #surahikhlas #learnarabic"
CAP = {"know": f"Khushūʿ starts with knowing what you're saying ☝️ Bilāl said aḥad with a boulder on his chest. You say it in al-Ikhlāṣ. Do you know what it means? 👇 {T}",
       "next": f"Next time you recite قُلْ هُوَ اللَّهُ أَحَدٌ, think of Bilāl on the burning sand ☝️ One word, and he wouldn't let it go. Save this for before your next salah. {T}",
       "feel": f"You can't feel what you don't understand. Aḥad isn't just 'one': it's the One with no second, the word Bilāl held on to under a boulder ☝️ Comment AHAD if you'll think of him next salah 👇 {T}"}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "fair": {"type": "score", "instructions": "`ctx` Caption: `h`. Is it accurate and sincere, paying off the hook without overclaiming?", "criteria": ["No", "Partly", "Mostly", "Fully"]}}
jobs = [(k, w) for k in CAP for w in WHO for _ in range(2)]
with ThreadPoolExecutor(18) as ex: r = list(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
for k in CAP:
    s = {q: round(sum(a[q]["score"] for (kk, _), a in r if kk == k) / 6, 2) for q in Q}
    print(k, s, round(sum(s.values()), 2))
