# Why a1-adhan did less than j1-jumuah (same format), and what a v2 should change (owner, 11 Oct 2026).
# Instagram day 1: adhan 515 views, 33% hold, 4.7 s watched, 3 shares; Jumuah 1,433 views, 38%, 6.6 s, 73 shares. TikTok 265 vs 717.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/adhan_fix.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
from concurrent.futures import ThreadPoolExecutor
BASE = "An 18-25 second reel from Rafiq, a small Arabic-learning account, explaining one Arabic word through its three-letter root."
V = {"jumuah": "Posted on a Friday morning. 'Why is Friday called al-Jumuʿah?' The root ج م ع = to gather, so: 'The day of gathering.' Then 'Once you see it, it's everywhere': jamʿ (combining the prayers) and jāmiʿa (a university). Your turn: what does jamīʿ mean? 3-2-1: all. 'Send this to who you're going to Jumuʿah with.'",
     "adhan_v1": "Posted on a Saturday evening. 'Why is the call to prayer called the adhān?' The root أ ذ ن = 'the root of hearing' (no answer given yet). Then straight to: 'Your turn: what's an udhun?' 3-2-1: an ear. 'The adhān is the call made for your ears.' 'Send this to whoever wakes you up for Fajr.' Caption: 'The answer is right next to your eyes 👂'.",
     "adhan_v2": "Posted at Fajr time. 'You hear it five times a day. Why is it called the adhān?' The root أ ذ ن: an udhun is an ear, so the adhān is the announcement made to your ears. Then 'once you see it, it's everywhere': the muʾadhdhin (the man who calls it; English took this word as 'muezzin') and idhn (permission, as in 'by Allah's leave'). Your turn: what does istaʾdhana mean? 3-2-1: he asked permission (to be heard). 'Send this to whoever wakes you up for Fajr.' Caption does not give the answer away."}
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun", "learner": "a 34-year-old who has wanted to learn Arabic for years",
       "student": "someone already learning Arabic at a weekend madrasa"}
Q = {"aha": {"type": "score", "instructions": "`b` `v` Viewer: `who`. How surprising and satisfying is the 'aha' for them?", "criteria": ["None", "Weak", "Good", "Strong"]},
     "finish": {"type": "score", "instructions": "`b` `v` Viewer: `who`. How likely are they to watch to the end?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "share": {"type": "score", "instructions": "`b` `v` Viewer: `who`. How likely are they to send it to someone?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]}}
jobs = [(k, w) for k in V for w in WHO]
with ThreadPoolExecutor(9) as ex: r = dict(ex.map(lambda j: (j, ask({"b": BASE, "v": V[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
for k in V: print(f"{k:10}", *(f"{q} {sum(r[(k, w)][q]['score'] for w in WHO) / 3:.2f}" for q in Q))
