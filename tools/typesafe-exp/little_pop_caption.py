# Caption for the little-words carousel in the pop look (30 Oct 2026, #308/#304): and, but, with, in, from, to, one course sentence each and an
# ayah or du'a they're in; the end asks for a score. Reach first (brag-quiz/IDEAS.md, How we post).
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/little_pop_caption.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("An 8-slide Instagram/TikTok carousel from Rafiq, a small account teaching the Arabic Muslims use. Bright colourful slides with drawings. Cover: "
       "'And, But, With, In, From, To: can you say all 6 in Arabic?' Then wa وَ (you say it in every prayer: iyyaka na'budu wa iyyaka nasta'in), lakin لَكِنْ, "
       "ma'a مَعَ (inna Allaha ma'a as-sabirin, 2:153), fi فِي (rabbana atina fi d-dunya hasanah, 2:201), min مِنْ (a'udhu billahi mina sh-shaytan), "
       "ila إِلى (inna lillahi wa inna ilayhi raji'un, 2:156), each with a short everyday sentence; last slide: how many did you know? Comment /6.")
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun", "learner": "a 34-year-old who has wanted to learn Arabic for years",
       "parent": "a 41-year-old Muslim parent who prays but doesn't understand the Arabic"}
T = "#learnarabic #arabic #arabicforbeginners #muslim #quran"
CAP = {"A_score": f"And, but, with, in, from, to 👀 6 tiny Arabic words you'll hear in every surah. How many could you say? Comment your score /6 👇 {T}",
       "B_prayer": f"You already say 3 of these every day without realising 🤲 “wa” in al-Fātiḥah, “min” in a'ūdhu billāh, “ilā” in innā lillāh… Swipe for all 6 and comment your score /6 👇 {T}",
       "C_quran": f"Learn these 6 and you'll start spotting them all over the Qur'an ✨ And, but, with, in, from, to. Swipe, count your score, comment /6 👇 Save it 📌 {T}",
       "D_tag": f"The smallest words do the most work 👀 6 Arabic words for and, but, with, in, from, to. Swipe, score yourself /6, and tag someone learning with you 👇 {T}"}
exec("Q =" + open("tools/typesafe-exp/pronouns_pop_caption.py").read().split("Q =")[1])
