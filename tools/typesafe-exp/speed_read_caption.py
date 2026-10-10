# Caption for m09-speed (the owner's speed-reading reel, 10 Oct 2026): باب, قَلَم, شاي, بَحْر, سَيّارَة, the timer faster each time
# (x1.0 to x3.3); ends "How many did you read in time? 5/5 = 🔥".
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/speed_read_caption.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
from concurrent.futures import ThreadPoolExecutor
CTX = ("A 17-second reel from Rafiq, a small Arabic-learning account: 'Read it before the timer, it gets faster'. Five Arabic words "
       "(door, pen, tea, sea, car), each with a shrinking timer bar, speed x1.0 up to x3.3, the meaning shown after; it ends 'How many did you read in time? 5/5 = fire'.")
CAP = {"A_score": "How many did you read before the timer? 📖⏱️ It gets faster every word. Drop your score out of 5 👇 #learnarabic #arabic #readarabic #arabicforbeginners #muslim",
       "B_challenge": "Arabic speed reading 🔥 bāb → sayyāra, and the timer gets faster every word. Comment your score /5 👇 and send it to a friend who thinks they can beat you 😅 #learnarabic #arabic #readarabic #arabicforbeginners #muslim",
       "C_level": "Can you read Arabic faster than the timer? ⏱️ Most people lose it on word 4. Comment your score 👇 #learnarabic #arabic #readarabic #arabicforbeginners #muslim"}
WHO = {"scroller": "a 22-year-old UK Muslim who can read a little Arabic, scrolling for fun", "learner": "a 34-year-old beginner learning to read Arabic",
       "student": "someone who reads Arabic well from madrasa"}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to comment their score or share it?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(9) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
for k in CAP: print(k, f"{sum(r[(k, w)]['engage']['score'] for w in WHO) / 3:.2f}")
