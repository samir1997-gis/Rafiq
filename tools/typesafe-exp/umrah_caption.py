# Caption for u1-umrah (owner, 8 Nov 2026): 5 Arabic sentences for Umrah, each said and explained.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 54-second Reel from Rafiq, a small account teaching the Arabic Muslims use. Hook: 'SAVE this before your Umrah: five Arabic sentences you'll actually use!' "
       "Five sentences one by one, each said in Arabic with its transliteration and meaning: I'm going to perform Umrah; which way to the Haram?; what time is Fajr?; "
       "where can I find a restaurant?; how much is this? Ends: which one will you use first? Comment below, and send this to someone going for Umrah.")
WHO = {"going": "a 28-year-old UK Muslim going for Umrah next month", "someday": "a 35-year-old UK Muslim hoping to go one day", "scroller": "a 22-year-old UK Muslim scrolling for fun"}
T = "#umrah #makkah #learnarabic #arabic #muslim"
CAP = {"save": f"Save this for your Umrah 🕋 5 Arabic sentences you'll actually use in Makkah. Which one will you use first? 👇 Send it to someone going soon {T}",
       "send": f"Going for Umrah soon? 🕋 Send this to whoever you're going with: 5 sentences for the Haram, Fajr, food and the shops 👇 {T}",
       "bikam": f"Bikam hādhā? How much is this? 🛍️ Plus 4 more Arabic sentences for your Umrah. Save it before you fly 🕋 {T}"}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "follow": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to follow the account?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "fair": {"type": "score", "instructions": "`ctx` Caption: `h`. Does the caption avoid giving the quiz answers away and avoid overclaiming?", "criteria": ["No", "Partly", "Mostly", "Fully"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
