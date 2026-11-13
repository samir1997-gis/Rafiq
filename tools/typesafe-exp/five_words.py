# "5 words everyone should know" (owner, 13 Nov 2026): the five small words that are 1 in 10 words of the Qur'an (counted on the text: min 3,195,
# la 1,626, fi 1,221, alladhina 984, ala 710 = 7,736 of 78,245, 9.9%, a lower bound: with wa/fa in front, not with suffixes). Hook and script check.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("The spoken first line, on screen from frame 0, of a 50-second Reel from Rafiq, a small account teaching the Arabic Muslims use. The video shows five "
       "small Arabic words (min 'from', la 'no', fi 'in', alladhina 'those who', ala 'on/over') that together are about 1 in every 10 words of the Quran, each with "
       "a line people already say (al-Falaq, the shahada, an-Nasr, al-Fatiha), then a quiz on the fifth.")
WHO = {"scroller": "a 22-year-old UK Muslim scrolling", "learner": "a 34-year-old learning Arabic", "revert": "a 30-year-old revert to Islam"}
CAP0 = {"five": "FIVE tiny words make up one in every ten words of the Qur'an.", "quran": "These five tiny words make up one in every ten words of the QUR'AN!",
       "know": "Learn these FIVE words and one in every ten words of the Qur'an makes sense."}
# round 1: five 4.14 (fair 1.63), quran 4.03, know 3.95. Round 2: a counted number instead of a ratio
CAP = {"7700": "Over 7,700 words in the Qur'an are just FIVE tiny words.", "five": CAP0["five"], "tenth": "FIVE tiny words. Together, they're about a tenth of the whole Qur'an."}
CTX += " The counts are from the Quran text: 7,736 of its 78,245 words, and more if you count them with endings attached."
Q = {"stop": {"type": "score", "instructions": "`ctx` Line: `h`. Viewer: `who`. How likely are they to stop scrolling and keep watching?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "fair": {"type": "score", "instructions": "`ctx` Line: `h`. Is it accurate and paid off fairly (not overclaiming)?", "criteria": ["No", "Partly", "Mostly", "Fully"]}}
jobs = [(k, w) for k in CAP for w in WHO for _ in range(2)]
with ThreadPoolExecutor(18) as ex: r = list(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
for k in CAP:
    s = {q: round(sum(a[q]["score"] for (kk, _), a in r if kk == k) / 6, 2) for q in Q}
    print(k, s, round(sum(s.values()), 2))
