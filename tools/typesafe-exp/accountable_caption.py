# Caption for the owner's "first thing you're asked about" talking reel (10 Oct 2026).
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/accountable_caption.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
from concurrent.futures import ThreadPoolExecutor
CTX = ("A 45-second talking-head reel by a young British Muslim from Rafiq, a small Arabic-learning account: picture the Day of Judgement, "
       "the first thing you're asked about is your salah (Tirmidhi 413); are you content with yours? Understanding its words makes it more "
       "meaningful, and 20 words are more than half of what you say in salah.")
CAP = {"A_question": "If you stood before Allah today, would you be happy with your salah? 🤲 The first thing you'll be asked about is your prayer. Understanding it starts with just 20 words. Save this for your next salah 📌 #salah #muslim #islam #learnarabic #dayofjudgement",
       "B_share": "The first thing you'll be asked about on the Day of Judgement is your salah 🤍 Are you content with yours? Send this to someone you pray with, and start with the 20 words 📌 #salah #muslim #islam #learnarabic #reminder",
       "C_link": "The first thing you'll be asked about is your salah. 20 words make up more than half of it 🤲 Learn them free: link in bio. #salah #muslim #islam #learnarabic #reminder"}
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun", "learner": "a 34-year-old who has wanted to learn Arabic for years",
       "imam": "a careful, knowledgeable Muslim who dislikes clickbait about religion"}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "trust": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. Does it feel sincere rather than an ad or clickbait?", "criteria": ["No", "Somewhat", "Mostly", "Yes"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(9) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
for k in CAP: print(k, *(f"{q} {sum(r[(k, w)][q]['score'] for w in WHO) / 3:.2f}" for q in Q))
