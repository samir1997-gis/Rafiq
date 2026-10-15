# Caption for g5-endings (15 Oct 2026, #261): the word-change quiz in the g4 standard. Callum's hook "NOBODY tells you Arabic has no
# word for 'my'!", then two rounds: اسْمِي "my name" → what's "his name"?, and بَيْتُكَ "your house" → what's "her house"? (the
# ـهُ / ـها trap), 3-2-1 each. Ends "How many did you get? Zero, one, or two? Comment down below!". The caption adds to the video
# (owner, 13 Oct), doesn't repeat the shouted hook, and gives no answer away.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/g5_caption.py
# Result: not run yet (no TYPE_SAFE_KEY in the session that wrote it).
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A TikTok/Instagram Reel from a small account teaching the Arabic Muslims use. A voice says 'Nobody tells you Arabic has no word "
       "for my!', then a two-question quiz: if this Arabic word means 'my name', what's 'his name'?; if this one means 'your house', "
       "what's 'her house'? Three choices and a 3-2-1 countdown each, then the answer. Ends: 'How many did you get? Zero, one, or two? "
       "Comment down below!' Caption under it: ")
WHO = {"target": "a 27-year-old UK Muslim who prays but doesn't understand the Arabic", "revert": "a 31-year-old revert learning Arabic"}
C = {
 "salah": "You already say one of these endings in every prayer: رَبِّي, “my Lord” 🤲 How many did you get? 👇 Send this to someone you pray with. #learnarabic #arabic #arabicgrammar #salah #muslim",
 "family": "There’s a whole family of these endings (my, your, his, her, our…) and two of them sound almost the same 👀 How many did you get? 👇 Send this to your Arabic study buddy. #learnarabic #arabic #arabicgrammar #arabicforbeginners #muslim",
 "names": "Asking a man his name is ismuka, a woman ismuki: one vowel decides it 👀 How many did you get? 👇 Send this to your Arabic study buddy. #learnarabic #arabic #arabicgrammar #arabicforbeginners #muslim",
 "plain": "Two questions, three seconds each. Zero, one or two? 👇 Send it to your Arabic study buddy. #learnarabic #arabic #arabicquiz #arabicgrammar #muslim",
}
Q = {"comment": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. How likely are they to comment their score?",
                 "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "share": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. How likely are they to send it to a friend?",
               "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "trust": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. Does the caption feel honest and interesting rather than clickbait?",
               "criteria": ["Clickbait", "A bit", "Mostly honest", "Honest and interesting"]}}
if __name__ == "__main__":
    jobs = [(k, w) for k in C for w in WHO for _ in range(2)]
    with ThreadPoolExecutor(20) as ex: res = list(ex.map(lambda j: (j, ask({"ctx": CTX, "c": C[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
    for k in C:
        s = {q: sum(a[q]["score"] for (kk, _), a in res if kk == k) / 4 for q in Q}
        print(f"{k:10} comment {s['comment']:.2f}  share {s['share']:.2f}  trust {s['trust']:.2f}  total {sum(s.values()):.2f}")
