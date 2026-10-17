# Spoken hook for m2-barik (owner, 17 Oct 2026): mashallah vs Allahumma barik. m1's "past tense" angle was wrong (إِنْ شاءَ اللهُ uses the
# same past form), so the video is now: ما شاءَ اللهُ word by word, al-Kahf 18:39 (said over your own blessing), then the Sunnah's
# barakah dua when you admire someone else's (Ibn Mājah 3509, Sahl ibn Ḥunayf), the root ب ر ك (بَرَكَة, مُبارَك), a "new baby" test.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("The first line, shouted word first and on screen from frame 0, of a 45-second Instagram reel from a small account teaching the Arabic "
       "Muslims use. The reel explains ما شاءَ اللهُ word by word and where it comes from (al-Kahf 18:39: a man told to say it about his own garden), "
       "then that when you admire someone else's blessing the Prophet taught praying for blessing, اللَّهُمَّ بارِكْ (Ibn Majah 3509), same root as "
       "barakah and mubarak, and ends with a test: 'your friend shows you their new baby: what do you say?' (answer: both).")
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun", "learner": "a 34-year-old who has tried to learn Arabic before and given up", "revert": "a 30-year-old revert"}
CAP = {"this": "MOST people say mashallah when they should say THIS!",
       "mix": "Mashallah or Allahumma barik? MOST people mix them up!",
       "half": "MOST people only say HALF of what the Sunnah teaches here!",
       "know": "Do you KNOW the difference between mashallah and Allahumma barik?"}
Q = {"stop": {"type": "score", "instructions": "`ctx` Opening line: `h`. Viewer: `who`. How likely are they to keep watching past the first 3 seconds?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "respect": {"type": "score", "instructions": "`ctx` Opening line: `h`. Viewer: `who`. Does it feel respectful rather than preachy or mocking about how people speak?", "criteria": ["Preachy or mocking", "A bit", "Respectful", "Respectful and intriguing"]},
     "fair": {"type": "score", "instructions": "`ctx` Opening line: `h`. Does the video pay off this line fairly, without overclaiming (e.g. implying mashallah is wrong)?", "criteria": ["Misleading", "Partly", "Mostly", "Fully"]}}
jobs = [(k, w) for k in CAP for w in WHO for _ in range(2)]
with ThreadPoolExecutor(24) as ex: res = list(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(a[q]["score"] for (kk, _), a in res if kk == k) / 6 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
