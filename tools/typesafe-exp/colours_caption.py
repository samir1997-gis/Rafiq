# Caption for the colours carousel (21 Oct 2026, #272): slide 1 "Red Blue Green Yellow White Black · Can you say all 6 in Arabic?", then one
# colour per slide in its two forms (أَحْمَر / حَمْراء for feminine words) with the course's own sentences; notes: the Green Dome (الْقُبَّةُ
# الْخَضْراءُ), al-Baqarah 2:69 (بَقَرَةٌ صَفْراءُ), the Black Stone (الْحَجَرُ الْأَسْوَدُ). Ends "How many did you know? Comment /6".
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/colours_caption.py
# Result: not run yet (no TYPE_SAFE_KEY in the session that wrote it; #262).
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("An Instagram/TikTok photo carousel from a small account teaching the Arabic Muslims use. Slide 1: 'Red Blue Green Yellow White Black. "
       "Can you say all 6 in Arabic?' Then one colour per slide, in its two forms (one for feminine words), with everyday example sentences and "
       "notes: the Green Dome in Madinah, the yellow cow in Surat al-Baqarah, the Black Stone of the Kaaba. Last slide: 'How many did you know? "
       "Comment /6'. Caption under it: ")
WHO = {"target": "a 27-year-old UK Muslim who prays but doesn't understand the Arabic", "revert": "a 31-year-old revert learning Arabic"}
C = {
 "twist": "Every colour in Arabic has a second form, and you've heard one of them in Madinah 🕌 How many of the 6 did you know? 👇 #learnarabic #arabic #arabiccolours #arabicforbeginners #muslim",
 "cow": "Slide 5: the cow in Surat al-Baqarah had a colour, and now you can say it 🐄 How many did you know? 👇 Save this 📌 #learnarabic #arabic #arabiccolours #quran #muslim",
 "plain": "6 colours, 2 forms each. Comment your score out of 6 👇 Send it to someone learning Arabic with you #learnarabic #arabic #arabiccolours #arabicforbeginners #muslim",
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
