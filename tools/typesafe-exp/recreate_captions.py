# Captions for the Drive-folder videos recreated in the proven formats (#246): r3-akbar, r4-insha, g4-past-i, w8-subhana-azim, q3-sujood.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/recreate_captions.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
from concurrent.futures import ThreadPoolExecutor
V = {"r3": "why Allahu akbar: أَكْبَرُ, root ك ب ر = big, great; payoff 'Greater than everything'; relatives كَبِير big and تَكْبِير the takbir; your turn: كِبار = grown-ups; ends 'Send this to whoever you pray with'",
     "r4": "what in sha' Allah actually says: شاءَ, root ش ي ء = to will; payoff 'If Allah wills'; relatives ما شاءَ اللهُ and مَشِيئَة (will); your turn: شَيْء = a thing; ends 'Send this to someone who says in sha' Allah every day'",
     "g4": "quiz: if كَتَبَ is 'he wrote', what's 'I wrote'? then 'he went' → 'I went'; 3-2-1 each, answers كَتَبْتُ and ذَهَبْتُ, rule: ـتُ on the end = I",
     "w8": "سُبْحانَ رَبِّيَ الْعَظِيمِ, said in every rukuʿ, word by word: Glory be to / my Lord / the Magnificent; ends 'What do you say in sujud instead? Comment it'",
     "q3": "salah quiz: in ruku you say subhana rabbiyal-azim; what do you say in sujud? three options, 5-second countdown, answer subhana rabbiyal-aʿla"}
CAP = {"r3": ["What does akbar in Allāhu akbar really mean? 🤍 Three letters, k-b-r, and you'll start seeing them everywhere, even in the takbīr. Try the last word before the 3 👇 Send this to whoever you pray with 🤍 #salah #allahuakbar #learnarabic #arabic #muslim #islam",
              "You say it to start every prayer. But what does akbar actually mean? 🤍 Watch to the end and guess the last word 👇 Send this to whoever you pray with. #salah #allahuakbar #learnarabic #arabic #muslim #islam"],
       "r4": ["What does in shā' Allāh actually say? 🤲 Three letters, sh-y-', and they're in mā shā' Allāh too. Guess the last word before the 3 👇 Send this to someone who says in shā' Allāh every day 🤍 #inshallah #mashallah #learnarabic #arabic #muslim #islam",
              "You say in shā' Allāh every day. Do you know what each word means? 🤲 Watch to the end and guess the last one 👇 Send this to someone who says it every day 🤍 #inshallah #mashallah #learnarabic #arabic #muslim #islam"],
       "g4": ["If kataba is “he wrote”, what's “I wrote”? ✍️ Three choices, 3 seconds. Then the same trick with “he went” 👇 0, 1 or 2? Send this to your Arabic study buddy. #learnarabic #arabic #arabicverbs #arabicgrammar #studyarabic",
              "He wrote → I wrote in Arabic? ✍️ One small ending does it. Pause and drop your answers 👇 Send this to someone learning with you. #learnarabic #arabic #arabicverbs #arabicgrammar #studyarabic"],
       "w8": ["You say this every time you bow in rukūʿ. Do you know every word? 🤲 Subḥāna rabbiyal-ʿaẓīm, word by word. What do you say in sujūd instead? Comment it 👇 Send it to someone you pray with. #salah #ruku #learnarabic #arabic #muslim #islam",
              "Subḥāna rabbiyal-ʿaẓīm, word by word 🤲 You say it in every rukūʿ. Save it for your next salah 📌 and comment what you say in sujūd 👇 #salah #ruku #learnarabic #arabic #muslim #islam"],
       "q3": ["In rukūʿ you say subḥāna rabbiyal-ʿaẓīm. What do you say in sujūd? 🤲 You've got 5 seconds 👇 Send this to someone you pray with. #salah #sujood #learnarabic #arabic #muslim #islam",
              "Rukūʿ and sujūd: almost the same words, one change. Can you spot it before the 5? 🤲 Send this to someone you pray with. #salah #sujood #learnarabic #arabic #muslim #islam"]}
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun", "learner": "a 34-year-old who has wanted to learn Arabic for years",
       "student": "someone already learning Arabic at a weekend madrasa"}
Q = {"engage": {"type": "score", "instructions": "A reel from Rafiq, a small Arabic-learning account: `v`. Caption: `h`. Viewer: `who`. How likely are they to comment, save or share?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]}}
jobs = [(v, k, w) for v in CAP for k in range(2) for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"v": V[j[0]], "h": CAP[j[0]][j[1]], "who": WHO[j[2]]}, Q)["answers"]), jobs))
for v in CAP: print(v, *(f"{'AB'[k]} {sum(r[(v, k, w)]['engage']['score'] for w in WHO) / 3:.2f}" for k in range(2)))
