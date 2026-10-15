# Caption for the question-words carousel (15 Oct 2026): slide 1 "Who? What? Where? When? Why? How? How many? Can you say all 7
# in Arabic?", then one word per slide with an example (مَنْ رَبُّكَ؟ "the first question in the grave", ما/ماذا, the mosque, Jumuʿah,
# why study Arabic, how are you, how many rakʿahs in Fajr), ends "How many did you know? Comment /7". The caption adds to it.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/questions_caption.py
# Result (15 Oct; comment / share / trust, target + revert x2): grave 2.13 / 2.21 / 1.65 · fajr 2.10 / 2.49 / 1.79 (chosen) ·
#   plain 2.14 / 2.24 / 1.61 · twist 2.07 / 2.10 / 1.68.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("An Instagram/TikTok photo carousel from a small account teaching the Arabic Muslims use. Slide 1: 'Who? What? Where? When? Why? "
       "How? How many? Can you say all 7 in Arabic?' Then one question word per slide with an example sentence (who: مَنْ رَبُّكَ؟ 'Who is "
       "your Lord?', the first question in the grave; what has two words, ما and ماذا; where is the mosque; when is Jumuʿah; how many "
       "rakʿahs in Fajr). Last slide: 'How many did you know? Comment /7'. Caption under it: ")
WHO = {"target": "a 27-year-old UK Muslim who prays but doesn't understand the Arabic", "revert": "a 31-year-old revert learning Arabic"}
C = {
 "grave": "The very first question you'll be asked in the grave starts with one of these words 🤍 How many of the 7 did you know? 👇 #learnarabic #arabic #arabicwords #muslim #islam",
 "fajr": "Bonus question on the last slide: how many rakʿahs are in Fajr? Answer it in Arabic if you can 👇 Save this for later 📌 #learnarabic #arabic #arabicwords #muslim #islam",
 "plain": "7 question words that unlock every Arabic conversation. How many did you know? Comment your score 👇 #learnarabic #arabic #arabicwords #muslim #islam",
 "twist": "Arabic has two words for “what” and most learners mix them up (slide 3) 👀 How many of the 7 did you know? 👇 #learnarabic #arabic #arabicwords #muslim #islam",
}
Q = {"comment": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. How likely are they to comment?",
                 "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "share": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. How likely are they to save or send it to a friend?",
               "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "trust": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. Does the caption feel honest and respectful rather than clickbait?",
               "criteria": ["Clickbait", "A bit", "Mostly honest", "Honest and interesting"]}}
if __name__ == "__main__":
    jobs = [(k, w) for k in C for w in WHO for _ in range(2)]
    with ThreadPoolExecutor(20) as ex: res = list(ex.map(lambda j: (j, ask({"ctx": CTX, "c": C[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
    for k in C:
        s = {q: sum(a[q]["score"] for (kk, _), a in res if kk == k) / 4 for q in Q}
        print(f"{k:8} comment {s['comment']:.2f}  share {s['share']:.2f}  trust {s['trust']:.2f}  total {sum(s.values()):.2f}")
