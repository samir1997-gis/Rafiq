# Caption for the little-words carousel (30 Oct 2026, #308): and / but / with / in / from / to in the pop style (#304), the course's own
# sentences (study Arabic and history; coffee but don't drink it; football with friends; tea at home; where are you from?; Friday, going to
# the mosque?) and a note each (1:5, لَكِنْ / لَكِنَّ, 2:153, 2:201, the taʿawwudh's مِنَ, 2:156). Ends "How many did you know? Comment /6".
# Not run yet: no TYPE_SAFE_KEY in the session that made it (#262).
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/little_caption.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("An Instagram/TikTok photo carousel from a small account teaching the Arabic Muslims use: bright drawn slides, one small word each "
       "(and, but, with, in, from, to) with an everyday sentence and a note tying it to a line they say in salah or know from the Qur'an. "
       "Ends: 'How many did you know? Comment /6'. Caption under it: ")
C = {
 "score": "6 tiny words you'll find in almost every Arabic sentence 👀 Can you say them all? Swipe, count, and comment your score /6 👇 Save it for later 📌 #learnarabic #arabic #arabicforbeginners #arabicvocabulary #muslim",
 "prayer": "You already say 3 of these in every prayer 🤲 And, but, with, in, from, to… in Arabic. How many did you know? Comment /6 👇 #learnarabic #arabic #arabicforbeginners #salah #arabicvocabulary",
}
WHO = {"target": "a 27-year-old UK Muslim who prays but doesn't understand the Arabic", "revert": "a 31-year-old revert learning Arabic"}
Q = {"comment": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. How likely are they to comment?",
                 "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "share": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. How likely are they to send it to someone?",
               "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "save": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. How likely are they to save it?",
              "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]}}
if __name__ == "__main__":
    jobs = [(k, w) for k in C for w in WHO for _ in range(2)]
    with ThreadPoolExecutor(20) as ex: res = list(ex.map(lambda j: (j, ask({"ctx": CTX, "c": C[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
    for k in C:
        s = {q: sum(a[q]["score"] for (kk, _), a in res if kk == k) / 4 for q in Q}
        print(f"{k:8} comment {s['comment']:.2f}  share {s['share']:.2f}  save {s['save']:.2f}  total {sum(s.values()):.2f}")
