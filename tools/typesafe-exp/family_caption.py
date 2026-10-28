# Caption for the family-words carousel (28 Oct 2026, #305): the pop style from #304 (bright slides, doodles, faceless drawn scenes), six
# words (mum, dad, brother, sister, grandpa, grandma) with the course's own sentences and a note each (al-Bukhārī 5971, Maryam 19:42,
# al-Ḥujurāt 49:10, أَخ → أُخْت, عَمّ / خال, جَدّ → جَدَّة); ends "How many did you know? Comment /6". Pure content, no app pitch.
# Not run yet: no TYPE_SAFE_KEY in the session that made it (#262).
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/family_caption.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("An Instagram/TikTok photo carousel from a small account teaching the Arabic Muslims use: bright drawn slides, one family word each "
       "(mum, dad, brother, sister, grandpa, grandma) with a sentence from everyday Muslim family life and a note (the hadith 'your mother, "
       "then your mother, then your mother', 'the believers are brothers'). Ends: 'How many did you know? Comment /6'. Caption under it: ")
C = {
 "score": "Can you say all 6 family words in Arabic? 👀 Swipe, count your score and comment it /6 👇 Save it for later 📌 #learnarabic #arabic #arabicforbeginners #arabicvocabulary #muslimfamily",
 "share": "Mum, Dad, Brother, Sister, Grandpa, Grandma… in Arabic 👨‍👩‍👧‍👦 How many did you know? Send this to the family member you'd teach first 🤍 #learnarabic #arabic #arabicforbeginners #arabicvocabulary #muslimfamily",
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
