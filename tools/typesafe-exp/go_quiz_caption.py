# Caption for v1-go-quiz (11 Oct 2026): "If this is 'I go' (أَذْهَبُ), what's 'we go'?" then "he goes" → "she goes"; Ashrabu's caption shape.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/go_quiz_caption.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
from concurrent.futures import ThreadPoolExecutor
CTX = ("A 24-second Arabic verb quiz from Rafiq: if أَذْهَبُ is 'I go', what's 'we go'? (نَذْهَبُ) then if يَذْهَبُ is 'he goes', what's 'she goes'? "
       "(تَذْهَبُ); 3-2-1 before each answer, the rule shown after; ends 'How many did you get? 0, 1 or 2?'")
CAP = {"A_ashrabu": "Arabic verb quiz 🚶 أَذْهَبُ = I go. So what's “we go”? And “she goes”? Pause and drop your answers below 👇 Spot the pattern once, use it on every verb. #learnarabic #arabic #arabicverbs #studyarabic #muslim",
       "B_share": "If “I go” is adhhabu, what's “we go”? 🚶 One letter changes. Answer before the 3 👇 and send it to someone learning Arabic with you. #learnarabic #arabic #arabicverbs #studyarabic #muslim"}
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun", "learner": "a 34-year-old who has wanted to learn Arabic for years",
       "student": "someone already learning Arabic at a weekend madrasa"}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to comment, save or share?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "spoil": {"type": "score", "instructions": "`ctx` Caption: `h`. Does the caption give away the answers?", "criteria": ["Not at all", "A little", "Mostly", "Completely"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(6) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
for k in CAP: print(k, *(f"{q} {sum(r[(k, w)][q]['score'] for w in WHO) / 3:.2f}" for q in Q))
