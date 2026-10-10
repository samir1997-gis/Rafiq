# Captions for the 10 Oct batch in the owner's three formats (word by word, one root, the word-change quiz): w5-w7, g1-g3, r2.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/batch3_captions.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
from concurrent.futures import ThreadPoolExecutor
V = {"w5": "رَبَّنا وَلَكَ الْحَمْدُ shown, then word by word: Our Lord / and to You / all praise; ends 'What does the imam say just before it? Comment it'",
     "w6": "السَّلامُ عَلَيْكُمْ وَرَحْمَةُ اللَّهِ, the salam that ends the prayer, word by word; ends 'Right side first, or left? Comment it'",
     "w7": "التَّحِيّاتُ لِلَّهِ وَالصَّلَواتُ وَالطَّيِّباتُ from the tashahhud, word by word; ends 'What's the next line? Comment it'",
     "g1": "quiz: if كِتاب is a book, what's 'books'? then if صَدِيق is a friend, what's 'friends'? 3-2-1 each, answers كُتُب and أَصْدِقاء",
     "g2": "quiz: if مُعَلِّم is a male teacher, what's a female teacher? then beautiful for him → for her; the answer adds ة",
     "g3": "quiz: if يَشْرَبُ is 'he drinks', what's 'he drank'? then 'we drink' → 'we drank' (شَرِبْنا); a follow-up to an earlier 'I drink / we drink' quiz",
     "r2": "why the Prophet is named Muhammad: root ح م د = praise, the same root as al-hamdu lillah and sami'a Allahu liman hamidah; your turn: Ahmad = the most praised, his other name in the Quran (61:6); ends 'Send this to a Muhammad or an Ahmad you know'"}
CAP = {"w5": ["You say it every time you stand from rukūʿ: Rabbanā wa lakal-ḥamd 🤲 Now you know every word. What does the imam say just before it? Comment it 👇 #salah #learnarabic #arabic #muslim #islam",
              "Rabbanā wa lakal-ḥamd, word by word 🤲 Our Lord · and to You · all praise. Save it for your next salah 📌 Comment what the imam says just before it 👇 #salah #learnarabic #arabic #muslim #islam"],
       "w6": ["The last thing you say in every prayer, word by word 🤍 As-salāmu ʿalaykum wa raḥmatullāh. Right side first, or left? Comment it 👇 #salah #learnarabic #arabic #muslim #islam",
              "You end every prayer with this. Do you know every word? 🤍 Save it 📌 and send it to someone you pray with. #salah #learnarabic #arabic #muslim #islam"],
       "w7": ["At-taḥiyyātu lillāh, word by word 🤲 You say it every time you sit in salah. What's the next line? Comment it 👇 #salah #tashahhud #learnarabic #arabic #muslim",
              "You say this every time you sit in salah. Now you'll know what it means 🤲 Save it for your next prayer 📌 #salah #tashahhud #learnarabic #arabic #muslim"],
       "g1": ["One book is kitāb. So what's “books”? 📚 Arabic doesn't just add an S. Answer before the 3 👇 How many did you get? #learnarabic #arabic #arabicgrammar #arabicforbeginners #muslim",
              "Arabic plurals are a puzzle 📚 kitāb → ? · ṣadīq → ? Pause and drop your answers 👇 Send it to someone who'd get 0/2 😅 #learnarabic #arabic #arabicgrammar #arabicforbeginners #muslim"],
       "g2": ["He's a muʿallim. So what's she? 👩‍🏫 One letter does it. Answer before the 3 👇 How many did you get? #learnarabic #arabic #arabicgrammar #arabicforbeginners #muslim",
              "Turn it from him to her in Arabic 👩‍🏫 muʿallim → ? · jamīl → ? Drop your answers 👇 Send it to someone learning with you. #learnarabic #arabic #arabicgrammar #arabicforbeginners #muslim"],
       "g3": ["You got “we drink”. Now: “he drank” and “we drank”? ☕ Pause and drop your answers 👇 How many did you get? #learnarabic #arabic #arabicverbs #studyarabic #muslim",
              "Ashrabu, part 2 ☕ yashrabu is “he drinks”. So what's “he drank”? Answer before the 3 👇 Send it to whoever got part 1 wrong 😅 #learnarabic #arabic #arabicverbs #studyarabic #muslim"],
       "r2": ["Why is the Prophet ﷺ named Muhammad? 🤍 Three letters, ح م د: praise. You say them in every prayer. Send this to a Muhammad or an Ahmad you know 🤍 #learnarabic #arabic #muslim #islam #seerah",
              "Muhammad, Ahmad, al-ḥamdu lillāh, ḥamidah: one root 🤍 Did you know they were connected? Comment 👇 #learnarabic #arabic #muslim #islam #seerah"]}
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun", "learner": "a 34-year-old who has wanted to learn Arabic for years",
       "student": "someone already learning Arabic at a weekend madrasa"}
Q = {"engage": {"type": "score", "instructions": "A reel from Rafiq, a small Arabic-learning account: `v`. Caption: `h`. Viewer: `who`. How likely are they to comment, save or share?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]}}
jobs = [(v, k, w) for v in CAP for k in range(2) for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"v": V[j[0]], "h": CAP[j[0]][j[1]], "who": WHO[j[2]]}, Q)["answers"]), jobs))
for v in CAP: print(v, *(f"{'AB'[k]} {sum(r[(v, k, w)]['engage']['score'] for w in WHO) / 3:.2f}" for k in range(2)))
