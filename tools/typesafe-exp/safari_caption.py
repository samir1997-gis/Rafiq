# Caption for h5-safari (2 Nov 2026, #317): the story of a word, drawn over a road across the savanna from night to full morning.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/safari_caption.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 64-second Reel from Rafiq, a small account teaching the Arabic Muslims use, drawn over a road across the savanna that goes from night to sunrise: "
       "'Safari comes from Arabic, and it's named after what a journey reveals about you.' safar = a journey; Swahili took it from Arab traders on the East "
       "African coast, English took it from Swahili in the 1800s. The root s-f-r means to uncover, like the dawn (al-Muddaththir 74:34). The old dictionaries "
       "(Lisan al-Arab) say a journey is called safar because it uncovers people's faces and their character: travel with someone and you'll find out who they "
       "really are. Your turn: 'wujuhun yawma'idhin musfirah' ('Abasa 80:38), some faces that Day will be travelling, covered or shining? 3-2-1: SHINING. "
       "Ask: who would you go on a journey with? Tag them in the comments.")
WHO = {"traveller": "a 27-year-old UK Muslim who loves travelling with friends", "learner": "a 32-year-old learning Arabic", "scroller": "a 20-year-old UK Muslim scrolling at lunch"}
T = "#learnarabic #arabic #safari #travel #quran"
CAP = {"tag": f"Tag the one person you'd go on a journey with 🧳 In Arabic, a journey is safar, because it shows who people really are. Did you get the 3-2-1? 👇 {T}",
       "question": f"Why is it called a safari? 🦒 It's Arabic, and the old dictionaries say a journey is named for what it reveals about you. Who would you travel with? 👇 {T}",
       "reveal": f"Travel with someone and you'll find out who they really are 😅 That's literally where the word safari comes from. Tag your travel partner 👇 {T}",
       "quran": f"Safari, safar, and the faces that will be musfirah on the Day of Judgement ☀️ One Arabic root: to uncover. Who would you take on a journey? Tag them 👇 {T}"}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "follow": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to follow the account?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "watch": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to watch to the end?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
