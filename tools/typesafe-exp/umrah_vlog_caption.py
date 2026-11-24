# Caption for the owner's Umrah vlog (24 Nov 2026): he's been away on Umrah, so a different post: a small vlog with 5 Arabic sentences for Umrah.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("An Instagram Reel from Rafiq, a small account teaching the Arabic Muslims use. The creator has been away on Umrah and posted nothing for a while; "
       "this is a short vlog from the trip with 5 Arabic sentences to know before Umrah: how much to the hotel (taxi), where's the market, "
       "where's the nearest toilet, is there a restaurant nearby, what time is Maghrib.")
WHO = {"scroller": "a 25-year-old UK Muslim scrolling for fun", "planner": "a 32-year-old planning their first Umrah", "follower": "an existing follower who noticed the account went quiet"}
T = "#umrah #makkah #learnarabic #arabic #muslim #umrah2026"
CAP = {"warm": f"Been quiet for a bit… because I was in Makkah for Umrah 🕋🤍\n\nSo today's a little different: a mini Umrah vlog, with 5 Arabic sentences I actually needed out there 🚕🛍️🚻🍽️🕌\n\nSave it for your next trip 📌 and tag the person you're going with 👇\n\n{T}",
       "dua": f"Back from Umrah 🕋 and I've missed you all 🤍\n\nNo quiz today: just a little vlog from Makkah and the 5 Arabic sentences you'll use most when you go 🚕🛍️🚻🍽️🕌\n\nMay Allah invite every one of you to His House 🤲 Save this for when He does 📌\n\n{T}",
       "short": f"Away on Umrah 🕋, so here's something different: a mini vlog + 5 Arabic sentences you need before your next Umrah ✨\n\nWhich one would you use first? 👇\n\n{T}"}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "warmth": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How warm and genuine does it feel?", "criteria": ["Cold or salesy", "A bit flat", "Warm", "Very warm and genuine"]},
     "respect": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How respectful is it of Umrah?", "criteria": ["Disrespectful", "Somewhat flippant", "Respectful", "Very respectful"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
