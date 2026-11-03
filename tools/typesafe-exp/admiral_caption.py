# Caption for h8-admiral (3 Nov 2026, #323): the story of a word, drawn over a sea at dusk with a fleet.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/admiral_caption.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 55-second Reel from Rafiq, a small account teaching the Arabic Muslims use, drawn over a sea at dusk: 'Every admiral in the navy has an Arabic "
       "title... they just don't know it.' amir = a commander, the one who gives the orders. In Norman Sicily in the 1100s the king's top commander ran his fleet "
       "and his title was Arabic: amir of amirs. Latin wrote it ammiratus, French amiral, English slipped in a D from 'admire': admiral. Your turn: its root means "
       "to command; Ya-Seen 36:82, amruhu: his ship, his army or his command? 3-2-1: COMMAND, 'His command is only to say: Be! and it is' (kun fayakun). "
       "Ask: who's the real amir of your house? comment it.")
WHO = {"family": "a 28-year-old UK Muslim who lives with family", "learner": "a 32-year-old learning Arabic", "scroller": "a 21-year-old UK Muslim scrolling at lunch"}
T = "#learnarabic #arabic #history #quran #kunfayakun"
CAP = {"amir": f"Who's the real amir of your house? 👑 Comment it 👇 Every admiral has an Arabic title, and it's in a verse you know by heart. Did you get the 3-2-1? {T}",
       "kun": f"Kun fayakun… and the same root gives you 'admiral' ⚓ An Arabic title that went from Sicily to the Royal Navy. Who's the amir of your house? 👇 {T}",
       "tag": f"Tag the person who's the boss of your house 😅 In Arabic that's the amir, and it's where the word admiral comes from 👇 {T}"}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "follow": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to follow the account?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "watch": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to watch to the end?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
