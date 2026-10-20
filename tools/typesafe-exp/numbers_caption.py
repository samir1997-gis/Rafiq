# Caption for the numbers carousel (20 Oct 2026): slide 1 "1 2 3 … 10 · Can you count to 10 in Arabic?", then one number per slide with
# the course's own example sentence and a salah link (Fajr رَكْعَتانِ, Maghrib 3, Dhuhr/ʿAsr/ʿIshāʾ 4, five prayers, al-Fātiḥah's 7
# verses), أَحَد in al-Ikhlāṣ, 3–10 working backwards, Arabic numerals ١٢٣. Ends "How many did you know? Comment /10". The caption adds to it.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/numbers_caption.py
# Result: not run yet (no TYPE_SAFE_KEY in the session that wrote it; #262).
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("An Instagram/TikTok photo carousel from a small account teaching the Arabic Muslims use. Slide 1: '1 2 3 4 5 6 7 8 9 10. Can you "
       "count to 10 in Arabic?' Then one number per slide with an everyday example sentence and a note linking it to the prayer (Fajr is two "
       "rak'ahs, Maghrib three, Dhuhr, Asr and Isha four, five prayers a day, al-Fatiha has seven verses), plus that the digits we write are "
       "called Arabic numerals. Last slide: 'How many did you know? Comment /10'. Caption under it: ")
WHO = {"target": "a 27-year-old UK Muslim who prays but doesn't understand the Arabic", "revert": "a 31-year-old revert learning Arabic"}
C = {
 "salah": "You already pray with these numbers every day: 2, 4, 4, 3 and 4 🤲 How many of the 10 did you know? 👇 Save this for later 📌 #learnarabic #arabic #arabicnumbers #salah #muslim",
 "two": "Slide 3 is the one that surprises people: Arabic doesn't need the number for “two” 👀 How many did you know? 👇 #learnarabic #arabic #arabicnumbers #arabicforbeginners #muslim",
 "kids": "Counting to 10 is the first thing kids learn in any language. Can you do it in the language of your salah? 👇 Send this to someone learning with you #learnarabic #arabic #arabicnumbers #muslim #islam",
 "plain": "1 to 10 in Arabic, with a sentence for each. Comment your score out of 10 👇 #learnarabic #arabic #arabicnumbers #arabicforbeginners #muslim",
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
        print(f"{k:9} comment {s['comment']:.2f}  share {s['share']:.2f}  trust {s['trust']:.2f}  total {sum(s.values()):.2f}")
