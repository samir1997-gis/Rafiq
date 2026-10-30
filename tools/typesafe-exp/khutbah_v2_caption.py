# Caption for h4-khutbah v2 (30 Oct 2026, #310): a drawn Friday city at dusk, the imam and the suitor, khutbah vs khitbah.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/khutbah_v2_caption.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 62-second Reel from Rafiq, a small account teaching the Arabic Muslims use, posted on a Friday, drawn over a city of domes and minarets at dusk: "
       "'The imam giving your Friday khutbah and your fiance have the same name in Arabic': khatib. Both come from khataba, to address (the imam addresses "
       "the people, a suitor addresses a family). khutbah (damma) = sermon, khitbah (kasra) = proposal, one small mark apart. Your turn: a phrase from "
       "al-Baqarah 2:235, sermon or proposal? 3-2-1: a PROPOSAL, the kasra gives it away. Ask: listen closely at Jumu'ah, send it to someone getting married, did you spot it?")
WHO = {"engaged": "a 26-year-old UK Muslim who just got engaged", "learner": "a 32-year-old learning Arabic", "scroller": "a 20-year-old UK Muslim scrolling on a Friday"}
T = "#jummah #khutbah #learnarabic #arabic #muslimwedding"
CAP = {"question": f"Your imam and your fiancé have the same name in Arabic 👀 One tiny mark tells the khutbah from the proposal. Did you spot it before the 3-2-1? 👇 {T}",
       "send": f"Send this to the friend who's getting married 💍 In Arabic, the imam on the minbar and their fiancé are both khatib. Sermon or proposal: did you spot it? 👇 {T}",
       "friday": f"Listen closely at Jumu'ah today 🕌 Khutbah = sermon, khitbah = proposal, and it's one small mark under the first letter. It's even in al-Baqarah 👇 Did you spot it? {T}",
       "mark": f"One dot of a vowel between a sermon and a proposal 😅 Khutbah or khitbah? Watch the first letter, then comment if you got it 👇 {T}"}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "follow": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to follow the account?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "watch": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to watch to the end?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
