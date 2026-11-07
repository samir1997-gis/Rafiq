# YouTube titles for the Aḥad videos (#315): the full version (the owner's own edit, v4) and the Shorts (90 s, 60 s footsteps, 60 s deny).
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
STORY = ("A video from Rafiq, a small account teaching the Arabic Muslims use: Bilal, a slave in Makkah, laid on burning sand with a boulder on his chest "
         "and told to deny Muhammad and worship al-Lat and al-Uzza, answers with one word: ahad. Why ahad and not wahid: wahid is a number (one, then two), "
         "ahad is the One with no second; it leaves no room for any partner; the whole of tawhid in one word, the very thing they wanted him to deny. ")
CTX = {"full": STORY + "The full 2.5-minute version, talking to camera with graphics, also covers al-Ikhlas and Bilal giving the adhan on the Ka'bah.",
       "short": STORY + "A 60-90 second Short."}
WHO = {"scroller": "a 22-year-old UK Muslim scrolling YouTube", "learner": "a 34-year-old learning Arabic", "seerah": "a 30-year-old who loves seerah stories"}
CAP = {"full": {"f1": "Why Bilal Said “Ahad” (Not “Wahid”)", "f2": "The One Word Bilal Said Under the Rock: Ahad", "f3": "Ahad: The Whole of Tawhid in One Word (the Story of Bilal)"},
       "short": {"s1": "Why Bilal Said “Ahad” Under the Rock #shorts", "s2": "One Word Under a Boulder: Ahad #shorts", "s3": "Why “Ahad” and Not “Wahid”? #shorts"}}
Q = {"click": {"type": "score", "instructions": "`ctx` YouTube title: `h`. Viewer: `who`. How likely are they to click and watch?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "watch": {"type": "score", "instructions": "`ctx` YouTube title: `h`. Viewer: `who`. How likely are they to watch to the end?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "trust": {"type": "score", "instructions": "`ctx` YouTube title: `h`. Viewer: `who`. How accurate and sincere does it feel (not clickbait)?", "criteria": ["No", "A bit", "Mostly", "Yes"]}}
jobs = [(v, k, w) for v in CAP for k in CAP[v] for w in WHO]
with ThreadPoolExecutor(18) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX[j[0]], "h": CAP[j[0]][j[1]], "who": WHO[j[2]]}, Q)["answers"]), jobs))
for v in CAP:
    rows = [(k, {q: sum(r[(v, k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP[v]]
    for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(v, k, {q: round(x, 2) for q, x in s.items()}, round(sum(s.values()), 2), CAP[v][k])
