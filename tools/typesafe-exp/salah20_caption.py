# Caption for the salah 20-words reel (13 Oct 2026). The owner on camera: picture the grave, the barzakh, the Day of Judgement
# (50,000 years, the sun overhead); the very first thing you're asked about is your salah. Content with it? If not: understand it.
# Just 20 words make up more than half of what you say in salah. Ends: "drop a comment and I will DM you".
# The caption adds to the reel instead of repeating it (owner, 13 Oct), and gives the commenters one word to type.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/salah20_caption.py
# Result (13 Oct; comment / share / trust, target + revert x2): hadith 2.79 / 2.51 / 1.35 (chosen; quoted as in Tirmidhi 413) ·
#   keyword 2.76 / 2.37 / 0.78 · personal 2.69 / 2.57 / 1.03 · question 2.75 / 2.40 / 1.06.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A Reel from a small account teaching the Arabic Muslims use. A young Muslim man on camera: picture waking up in the grave, "
       "the Day of Judgement lasting 50,000 years, the sun overhead; the very first thing you're asked about is your salah. Are you content "
       "with it? If not, try to understand the words: just 20 words make up more than half of what you say in salah. Start with those 20. "
       "He ends: 'drop a comment down below and I will DM you.' Caption under it: ")
WHO = {"target": "a 27-year-old UK Muslim who prays but doesn't understand the Arabic", "revert": "a 31-year-old revert learning Arabic"}
C = {
 "hadith": "“The first deed a servant will be held accountable for on the Day of Resurrection is his salah.” (Tirmidhi 413) 🤍 Comment 20 and I'll send you the 20 words. #salah #learnarabic #quranarabic #muslim #islam",
 "keyword": "Comment “20” and I'll DM you the 20 words that make up more than half of your salah 🤍 #salah #learnarabic #quranarabic #muslim #islam",
 "personal": "I prayed for 26 years without understanding a word. These 20 changed that 🤍 Comment “20” and I'll send them to you. #salah #learnarabic #quranarabic #muslim #islam",
 "question": "When did you last feel present in your salah? 🤍 Comment “20” and I'll send you the 20 words to start with. #salah #learnarabic #quranarabic #muslim #islam",
}
Q = {"comment": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. How likely are they to comment?",
                 "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "share": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. How likely are they to send it to a friend or save it?",
               "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "trust": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. Does the caption feel sincere and respectful of the topic rather than clickbait or a sales pitch?",
               "criteria": ["Clickbait", "A bit", "Mostly sincere", "Sincere"]}}
if __name__ == "__main__":
    jobs = [(k, w) for k in C for w in WHO for _ in range(2)]
    with ThreadPoolExecutor(20) as ex: res = list(ex.map(lambda j: (j, ask({"ctx": CTX, "c": C[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
    for k in C:
        s = {q: sum(a[q]["score"] for (kk, _), a in res if kk == k) / 4 for q in Q}
        print(f"{k:10} comment {s['comment']:.2f}  share {s['share']:.2f}  trust {s['trust']:.2f}  total {sum(s.values()):.2f}")
