# Caption for h10-magazine (6 Nov 2026, #353): the story of a word, drawn over an old market's storehouses at dusk.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/magazine_caption.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A Reel from Rafiq, a small account teaching the Arabic Muslims use, drawn over an old market at dusk: 'Every magazine you've ever read is named after "
       "an Arabic word... and it has nothing to do with reading.' makhazin = storehouses, where you keep the grain, the oil, the goods. Its root kh-z-n means to "
       "store away; put ma in front and you get makhzan, the place where you keep things. Italian magazzino, French magasin (still a shop in France), English "
       "magazine in the 1580s: a storehouse. In 1731 a London monthly called itself The Gentleman's Magazine: a storehouse of articles. Your turn: Yusuf to the "
       "king (12:55), put me in charge of the khaza'in of the land: the armies, the roads or the storehouses? 3-2-1: STOREHOUSES. Ask: which English word "
       "should we trace next? Comment it.")
WHO = {"scroller": "a 21-year-old UK Muslim", "learner": "a 32-year-old learning Arabic", "reader": "a 28-year-old who loves word origins"}
T = "#learnarabic #arabic #etymology #quran #surahyusuf"
CAP = {"next": f"Which English word should we trace back next? Comment it 👇 'Magazine' started as an Arabic word for storehouses, and it's in surah Yusuf. {T}",
       "fact": f"Magazine is an Arabic word 📰 makhāzin: storehouses. Yusuf asked to run them (12:55). Did you get the 3-2-1? 👇 {T}",
       "share": f"Send this to someone who still buys magazines 😅 The word is Arabic: makhāzin, storehouses. Which word next? 👇 {T}"}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "follow": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to follow the account?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "watch": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to watch to the end?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
