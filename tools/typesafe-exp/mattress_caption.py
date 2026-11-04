# Caption for h9-mattress (4 Nov 2026, #340): the story of a word, drawn over rooftops at night under the moon.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/mattress_caption.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A Reel from Rafiq, a small account teaching the Arabic Muslims use, drawn over rooftops at night: 'Every night, you fall asleep on an Arabic "
       "word... and you don't even know it.' matrah = something thrown down, a cushion you throw on the floor to sit or sleep on. Its root t-r-h means to "
       "throw; the ma at the front is the ma of masjid, 'the place of': the place you throw yourself down. Sicily passed it to Italian as materasso, French "
       "made it materas, and by the 1300s English was sleeping on a mattress. Your turn: the same root in surah Yusuf (12:9), when his brothers plotted: "
       "itrahoohu. Hide him, sell him or throw him? 3-2-1: THROW. Ask: what do you say before you sleep? Comment it.")
WHO = {"sleeper": "a 24-year-old UK Muslim who scrolls in bed at night", "learner": "a 32-year-old learning Arabic", "parent": "a 38-year-old UK Muslim mum"}
T = "#learnarabic #arabic #etymology #quran #surahyusuf"
CAP = {"dua": f"What do you say before you sleep? 🌙 Comment it 👇 Your mattress is an Arabic word, and its root is in surah Yusuf. Did you get the 3-2-1? {T}",
       "fact": f"Your mattress is an Arabic word 🛏️ maṭraḥ: the place you throw yourself down. Same root as a verse in surah Yusuf. What do you say before you sleep? 👇 {T}",
       "share": f"Send this to the person who's always asleep 😴 Their mattress is an Arabic word: maṭraḥ, 'the thing thrown down'. What do you say before you sleep? 👇 {T}"}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "follow": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to follow the account?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "watch": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to watch to the end?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
