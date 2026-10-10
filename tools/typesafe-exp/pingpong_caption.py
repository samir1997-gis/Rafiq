# Caption for the "ping pong of opposites" video (a word served, its opposite returned), reach first (brag-quiz/IDEAS.md, How we post).
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/pingpong_caption.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
from concurrent.futures import ThreadPoolExecutor
CTX = ("A short TikTok/Reels video from Rafiq, a small Arabic-learning account: a simulated game of ping pong where each shot serves an Arabic word "
       "and the return is its opposite (big / small, hot / cold and so on), rally after rally.")
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun", "learner": "a 34-year-old who has wanted to learn Arabic for years",
       "student": "someone already learning Arabic at a weekend madrasa"}
CAP = {"A_rally": "Arabic ping pong 🏓 Every word gets returned with its opposite. Say the return before it lands. How many rallies did you win? 👇 #learnarabic #arabic #arabicwords #arabicvocabulary #arabicforbeginners",
       "B_serve": "I serve, you return 🏓 Can you hit back the opposite in Arabic before the ball lands? Drop your score in the comments 👇 #learnarabic #arabic #arabicwords #arabicvocabulary #arabicforbeginners",
       "C_next": "Arabic opposites, ping pong style 🏓 Your serve: comment a word and I'll return its opposite in Arabic 👇 #learnarabic #arabic #arabicwords #arabicvocabulary #arabicforbeginners",
       "D_tag": "Arabic ping pong 🏓 Play it with a friend: one says the word, the other returns the opposite. Tag who you're playing 👇 #learnarabic #arabic #arabicwords #arabicvocabulary #arabicforbeginners"}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "follow": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to follow the account?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "content": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How much does it feel like content rather than an ad?", "criteria": ["Pure ad", "Mostly ad", "Mostly content", "Pure content"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
