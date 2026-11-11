# YouTube title for h11-jamil (#356): beautiful and camel from the same root ج م ل (11 Nov 2026).
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 70-second YouTube Short from Rafiq, a small account teaching the Arabic Muslims use: jamil (beautiful) and jamal (camel) are built from the same "
       "three letters j-m-l; camels were beauty and wealth to the Arabs, as the Quran says of livestock (16:6); jumla, a sentence, from the same root; "
       "a quiz on the hadith 'Allah is jamil and loves al-jamal' (Muslim 91): camels or beauty?")
WHO = {"scroller": "a 22-year-old UK Muslim scrolling YouTube", "learner": "a 34-year-old learning Arabic", "curious": "a 28-year-old curious about languages"}
CAP = {"t1": "In Arabic, 'Beautiful' and 'Camel' Are the Same Word?! #shorts", "t2": "Why Arabic Uses the Same Letters for Beautiful and Camel 🐪 #shorts",
       "t3": "Beautiful = Camel? The Arabic Root That Explains It #shorts"}
Q = {"click": {"type": "score", "instructions": "`ctx` YouTube title: `h`. Viewer: `who`. How likely are they to watch it to the end?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "trust": {"type": "score", "instructions": "`ctx` YouTube title: `h`. Viewer: `who`. Is it accurate, and does the video pay it off fairly?", "criteria": ["No", "A bit", "Mostly", "Yes"]}}
jobs = [(k, w) for k in CAP for w in WHO for _ in range(2)]
with ThreadPoolExecutor(18) as ex: r = list(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
for k in CAP:
    s = {q: round(sum(a[q]["score"] for (kk, _), a in r if kk == k) / 6, 2) for q in Q}
    print(k, s, round(sum(s.values()), 2), CAP[k])
