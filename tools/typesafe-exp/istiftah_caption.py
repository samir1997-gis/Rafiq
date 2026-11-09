# Caption for the duʿāʾ al-istiftāḥ video (owner, 9 Nov 2026): "Have you ever seen the imam do this before?" … the app: the duʿāʾ with its
# recording, then word by word.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 48-second Reel from Rafiq, a small account teaching the Arabic Muslims use. The presenter, in prayer: 'Have you ever seen the imam do this before? "
       "I always used to wonder what the imam was reciting between Allahu akbar and the Fatiha, then I realised it's part of the Sunnah: dua al-istiftah, "
       "the opening supplication, and it's really easy to learn. Have a look.' Then the Rafiq app full screen: the dua subhanaka Allahumma wa bihamdik... "
       "with its meaning and recitation, then word by word.")
WHO = {"scroller": "a 22-year-old UK Muslim scrolling", "learner": "a 34-year-old learning Arabic", "parent": "a 40-year-old UK Muslim who prays at the masjid"}
T = "#salah #sunnah #dua #learnarabic #muslim"
CAP = {"imam": f"What is the imam saying in that pause after Allahu akbar? 🤲 It's the opening du'a, and it takes a minute to learn. Save this for your next salah {T}",
       "silent": f"That silent moment before al-Fatiha has a du'a in it 🤲 Subhanaka Allahumma wa bihamdik... learn it word by word. Did you know it? 👇 {T}",
       "sunnah": f"A Sunnah most of us skip in every salah 🤲 The opening du'a, word by word. Comment 🤍 if you're learning it today {T}"}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "follow": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to follow the account?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "fair": {"type": "score", "instructions": "`ctx` Caption: `h`. Does the caption avoid giving the quiz answers away and avoid overclaiming?", "criteria": ["No", "Partly", "Mostly", "Fully"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
