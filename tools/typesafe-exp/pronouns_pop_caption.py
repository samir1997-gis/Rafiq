# Caption for the redone pronouns carousel (28 Oct 2026, #304): bright slides with drawings, I / you (m) / you (f) / he / she / we,
# one course sentence each, the end asks for a score. Reach first (brag-quiz/IDEAS.md, How we post).
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/pronouns_pop_caption.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("An 8-slide Instagram/TikTok carousel from Rafiq, a small account teaching the Arabic Muslims use. Bright colourful slides with drawings: "
       "I أَنا, you to a man أَنْتَ, you to a woman أَنْتِ, he هُوَ, she هِيَ, we نَحْنُ, each with a short sentence (a grandfather praying in the mosque, "
       "a grandmother reading Qur'an, we pray in the mosque); the note that you say 'we' in every prayer in نَعْبُدُ; last slide: how many did you know? Comment /6.")
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun", "learner": "a 34-year-old who has wanted to learn Arabic for years",
       "parent": "a 41-year-old Muslim parent who prays but doesn't understand the Arabic"}
T = "#learnarabic #arabic #arabicforbeginners #muslim #quran"
CAP = {"A_score": f"I, you, he, she, we in Arabic 👀 6 tiny words you'll hear in every surah. How many did you get? Comment your score /6 👇 {T}",
       "B_we": f"You already say one of these in every prayer 🤲 نَعْبُدُ: “WE worship”. Swipe for all 6: I, you, you, he, she, we. Score yourself /6 in the comments 👇 {T}",
       "C_two_yous": f"Arabic has TWO words for “you” 👀 one for a man, one for a woman. Swipe for all 6 and comment your score /6 👇 Save it 📌 {T}",
       "D_tag": f"The 6 smallest words in Arabic, and you'll find them all over the Qur'an ✨ Swipe, count your score, and tag someone learning with you 👇 {T}"}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "follow": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to follow the account?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "swipe": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to swipe through all the slides?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':12}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:12}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
