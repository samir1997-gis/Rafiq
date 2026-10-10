# Captions for the 10 Oct batch (q4-azim, q5-ighfir, q6-tahiyyat, a1-adhan), written to the Instagram findings in brag-quiz/IDEAS.md.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/batch2_captions.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
from concurrent.futures import ThreadPoolExecutor
V = {"q4": "a 16-second quiz: الْعَظِيمِ, which of four meanings, a 5-second countdown, answer 'the Magnificent' from سُبْحانَ رَبِّيَ الْعَظِيمِ said in ruku",
     "q5": "a 15-second quiz: اغْفِرْ, which of four meanings, a 5-second countdown, answer 'forgive' from رَبِّ اغْفِرْ لِي said between the two sujood",
     "q6": "an 18-second quiz: التَّحِيّاتُ, which of four meanings, a 5-second countdown, answer 'all greetings', the first words of the tashahhud",
     "a1": "an 18-second video: why the call to prayer is called the adhān: its root أ ذ ن is hearing, then 'your turn: what is an أُذُن?' with a 3-2-1, answer: an ear"}
CAP = {"q4": {"A": "What does al-ʿAẓīm mean? 🤔 You say it in every rukūʿ. Answer before the 5 runs out 👇 Save it for your next salah. #salah #learnarabic #arabic #muslim #islam",
              "B": "You say سُبْحانَ رَبِّيَ الْعَظِيمِ in every rukūʿ… but what does al-ʿAẓīm mean? Comment your answer before the reveal 👇 #salah #learnarabic #arabic #muslim #islam"},
       "q5": {"A": "What does ighfir mean? 🤲 You say it between the two sujood. Answer before the 5 runs out 👇 Save it for your next salah. #salah #learnarabic #arabic #muslim #islam",
              "B": "Rabbi-ghfir lī: you say it between the two sujood. Do you know what ighfir means? Comment before the reveal 👇 Send it to someone you pray with 🤍 #salah #learnarabic #arabic #muslim #islam"},
       "q6": {"A": "At-taḥiyyāt: the first word of the tashahhud. What does it mean? Answer before the 5 runs out 👇 Save it for your next salah. #salah #tashahhud #learnarabic #arabic #muslim",
              "B": "You sit and say at-taḥiyyātu lillāh in every prayer. What does at-taḥiyyāt mean? Comment before the reveal 👇 #salah #tashahhud #learnarabic #arabic #muslim"},
       "a1": {"A": "Why is the call to prayer called the adhān? 🕌 The answer is right next to your eyes 👂 Send this to whoever wakes you up for Fajr 🤍 #adhan #learnarabic #arabic #muslim #islam",
              "B": "Why is it called the adhān? Three letters, أ ذ ن, and one of them is on your head 👂 Did you get it before the 3? 👇 #adhan #learnarabic #arabic #muslim #islam"}}
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun", "learner": "a 34-year-old who has wanted to learn Arabic for years",
       "student": "someone already learning Arabic at a weekend madrasa"}
Q = {"engage": {"type": "score", "instructions": "A reel from Rafiq, a small Arabic-learning account: `v`. Caption: `h`. Viewer: `who`. How likely are they to comment, save or share?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "clear": {"type": "score", "instructions": "A reel from Rafiq: `v`. Caption: `h`. Is the caption accurate to the video and clear about the one thing to do?", "criteria": ["No", "Somewhat", "Mostly", "Yes"]}}
jobs = [(v, k, w) for v in CAP for k in CAP[v] for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"v": V[j[0]], "h": CAP[j[0]][j[1]], "who": WHO[j[2]]}, Q)["answers"]), jobs))
for v in CAP:
    for k in CAP[v]: print(v, k, *(f"{q} {sum(r[(v, k, w)][q]['score'] for w in WHO) / 3:.2f}" for q in Q))
