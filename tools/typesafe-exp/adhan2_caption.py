# Caption for a2-adhan (11 Oct 2026): the Jumuah caption's shape, and nothing that gives the answer away.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/adhan2_caption.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
from concurrent.futures import ThreadPoolExecutor
CTX = ("A 25-second reel from Rafiq: why the call to prayer is called the adhān (root أ ذ ن, the ear: the announcement made to your ears), "
       "then the muʾadhdhin (English 'muezzin') and idhn (permission), your turn istaʾdhana = he asked permission; ends 'Send this to whoever wakes you up for Fajr'.")
CAP = {"A_jumuah_shape": "Why is the call to prayer called the adhān? 🕌 Three letters, أ ذ ن. Once you see them, they're everywhere. Send this to whoever wakes you up for Fajr 🤍 #adhan #fajr #learnarabic #arabic #muslim",
       "B_muezzin": "You hear it five times a day. But why is it called the adhān? 🕌 And what does it have to do with the word “muezzin”? Send this to whoever wakes you up for Fajr 🤍 #adhan #fajr #learnarabic #arabic #muslim"}
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun", "learner": "a 34-year-old who has wanted to learn Arabic for years",
       "student": "someone already learning Arabic at a weekend madrasa"}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to watch, comment or share?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "spoil": {"type": "score", "instructions": "`ctx` Caption: `h`. Does the caption give away the video's answer before they watch?", "criteria": ["Not at all", "A little", "Mostly", "Completely"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(6) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
for k in CAP: print(k, *(f"{q} {sum(r[(k, w)][q]['score'] for w in WHO) / 3:.2f}" for q in Q))
