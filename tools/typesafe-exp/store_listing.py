# App Store / Google Play name and subtitle for Rafiq (#352): which pair makes the right person tap "Get"?
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("An App Store search result. Rafiq is an app teaching Modern Standard Arabic to Muslims in the UK: short daily lessons from the "
       "first letter, every word of the salah explained, audio, spaced review, an AI tutor. Name and subtitle (30 characters each) are what show.")
WHO = {"salah": "a 28-year-old UK Muslim who wants to understand what they say in salah", "learner": "a 35-year-old who wants to learn Arabic properly",
       "revert": "a 30-year-old revert searching the App Store for Arabic"}
CAP = {"a": "Rafiq: Learn Arabic & Salah — Understand every word you pray",
       "b": "Rafiq: Learn Arabic for Salah — Daily lessons from the 1st letter",
       "c": "Rafiq – Arabic for Muslims — Understand every word you pray",
       "d": "Rafiq: Learn Arabic — Understand your salah, word by word"}
Q = {"tap": {"type": "score", "instructions": "`ctx` Name — subtitle: `h`. Viewer: `who`. How likely are they to tap to see more?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "clear": {"type": "score", "instructions": "`ctx` Name — subtitle: `h`. Is it clear what the app does and who it's for?", "criteria": ["No", "Partly", "Mostly", "Fully"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(k, {q: round(v, 2) for q, v in s.items()}, round(sum(s.values()), 2), CAP[k])
