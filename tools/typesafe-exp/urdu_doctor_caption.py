# Caption for "If you speak Urdu, you already know these Arabic words: at the doctor's" (1 Nov 2026, #313).
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/urdu_doctor_caption.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 59-second Reel from Rafiq, a small account teaching the Arabic Muslims use: 'HUNDREDS of Arabic words... if you speak Urdu, you already know "
       "them, and nobody tells you!' A drawn clinic: the patient marid (Urdu mareez), the doctor tabib (tabeeb), medicine dawa, treatment ilaj (ilaaj), "
       "health sihha (sehat), the cure shifa, each with its Urdu spelling and a counter of the words you already know; then Ibrahim in the Qur'an, "
       "ash-Shu'ara 26:80 'and when I am ill, it is He who cures me'; ask: how many did you get, comment your score, where should we go next?")
WHO = {"urdu": "a 24-year-old British Pakistani Muslim who speaks Urdu at home", "learner": "a 33-year-old Urdu speaker who wants to understand the Qur'an",
       "parent": "a 45-year-old Muslim mum who speaks Urdu"}
T = "#urdu #learnarabic #arabic #pakistani #muslim"
CAP = {"A_score": f"If you speak Urdu, you already know more Arabic than you think 👀 Mareez, tabeeb, dawa, ilaaj… How many did you get? Comment your score /6 👇 {T}",
       "B_next": f"Urdu speakers, you've been speaking Arabic this whole time 😅 6 words from the doctor's. Where should we go next: the kitchen, the classroom or the mosque? 👇 {T}",
       "C_quran": f"Shifa, the cure, comes from Allah 🤲 And if you speak Urdu, you already know the Arabic for it. 6 words you didn't know you knew. Comment your score 👇 {T}",
       "D_tag": f"Tag someone who speaks Urdu 👇 They already know hundreds of Arabic words and nobody told them. Start with these 6 from the doctor's 🩺 {T}"}
exec("Q =" + open("tools/typesafe-exp/pronouns_pop_caption.py").read().split("Q =")[1].replace("swipe through all the slides", "watch to the end"))
