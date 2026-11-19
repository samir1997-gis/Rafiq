# Caption for "Signs in the hills 2" (19 Nov 2026, #375): a 6-slide carousel of the owner's own photos from a night on Kinder Scout.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("An Instagram carousel from Rafiq, a small account teaching the Arabic Muslims use. Real photos from a camping trip on a mountain in England. "
       "Cover: 'One night on a mountain, 5 words from the Qur'an'. Each slide pairs a photo with one Qur'an word, its meaning and verse: "
       "a stream, al-ma' water (21:30, every living thing from water); a path, hawnan gently, humbly (25:63, the servants of the Most Merciful walk on the earth gently); "
       "clouds, sahab (24:43); the sunrise, ash-shams the sun (91:1); sleeping under a rock, nawm sleep (78:9, We made your sleep for rest). Last slide: follow and share.")
WHO = {"scroller": "a 24-year-old UK Muslim who likes hiking", "learner": "a 34-year-old learning Arabic", "parent": "a 40-year-old UK Muslim dad"}
T = "#quran #arabic #learnarabic #muslim #hiking #peakdistrict #nature"
CAP = {"sleep": f"We slept under a rock on Kinder Scout. These 5 Qur'an words wouldn't leave my head 🏔️ Which one hit you most? 👇 Save it for your next trip {T}",
       "walk": f"\"The servants of the Most Merciful walk on the earth gently\" (25:63). One night in the hills, five words from the Qur'an. Which is your favourite? 👇 {T}",
       "part2": f"Part 2 from the mountain ⛰️ Water, a gentle walk, clouds, the sun, sleep: 5 Qur'an words you've seen with your own eyes. Send it to who you'd camp with 👇 {T}"}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "follow": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to follow the account?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "fair": {"type": "score", "instructions": "`ctx` Caption: `h`. Is it accurate and respectful of the Qur'an, without overclaiming?", "criteria": ["No", "Partly", "Mostly", "Fully"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
