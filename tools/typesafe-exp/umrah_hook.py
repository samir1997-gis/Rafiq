# Spoken hook for u1-umrah (owner, 8 Nov 2026: "5 essential sentences you should know if you're going to do Umrah", on screen one by one with the
# voiceover): I'm going to perform Umrah · which way to al-Masjid al-Ḥarām? · what time is Fajr? · where can I find a restaurant? · how much is this?
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("The first line, shouted word first and on screen from frame 0, of a 60-second Instagram reel from a small account teaching the Arabic Muslims use. "
       "It teaches 5 Arabic sentences for Umrah, one by one, each said in Arabic and explained: I'm going to perform Umrah; which way to al-Masjid al-Haram?; "
       "what time is Fajr?; where can I find a restaurant?; how much is this? It ends: which one will you use first? and send it to someone going for Umrah.")
WHO = {"going": "a 28-year-old UK Muslim going for Umrah next month", "someday": "a 35-year-old UK Muslim hoping to go for Umrah one day", "scroller": "a 22-year-old UK Muslim scrolling for fun"}
CAP = {"going": "GOING for Umrah? Learn these 5 Arabic sentences before you fly!",
       "dont": "DON'T go to Umrah without these 5 Arabic sentences!",
       "most": "MOST pilgrims can't say these 5 sentences in Makkah!",
       "save": "SAVE this before your Umrah: 5 Arabic sentences you'll actually use!"}
Q = {"stop": {"type": "score", "instructions": "`ctx` Opening line: `h`. Viewer: `who`. How likely are they to keep watching past the first 3 seconds?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "save": {"type": "score", "instructions": "`ctx` Opening line: `h`. Viewer: `who`. How likely are they to save or share the video?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "fair": {"type": "score", "instructions": "`ctx` Opening line: `h`. Does the video pay off this line fairly, without overclaiming or putting people down?", "criteria": ["Misleading", "Partly", "Mostly", "Fully"]}}
jobs = [(k, w) for k in CAP for w in WHO for _ in range(2)]
with ThreadPoolExecutor(24) as ex: res = list(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(a[q]["score"] for (kk, _), a in res if kk == k) / 6 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
