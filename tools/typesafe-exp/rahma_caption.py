# Caption for n2-rahma (18 Oct 2026, #264): the word tree. Hook "FAMILY is hiding inside a word you say in every prayer!", al-Fātiḥah 1:3,
# the root ر ح م grows into رَحْمَة and رَحِمَهُ اللهُ, then "your turn": رَحِم, 3-2-1, the womb; al-Bukhārī 5988. Ends "Who in your family
# needs a call from you today? Comment below". The caption adds to the video and gives no answer away.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/rahma_caption.py
# Result: not run yet (no TYPE_SAFE_KEY in the session that wrote it; #262).
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A TikTok/Instagram Reel from a small account teaching the Arabic Muslims use. A voice says 'Family is hiding inside a word you say in "
       "every prayer!', then al-Fatiha's 'ar-Rahman ar-Rahim', whose three root letters (mercy) grow into a tree: mercy, 'may Allah have mercy "
       "on him', and a last word to guess with a 3-2-1, which turns out to be the word for the womb, with the hadith that the womb takes its "
       "name from ar-Rahman. Ends: 'Who in your family needs a call from you today? Comment below.' Caption under it: ")
C = {
 "bismillah": "Every Bismillah has this root in it twice 🌱 Who came to mind? Comment below 👇 and send this to them. #learnarabic #arabic #arabicroots #quran #muslim",
 "ties": "Keeping family ties is called صِلَة الرَّحِم in Arabic, and now you know why 🤍 Who are you calling today? 👇 #learnarabic #arabic #arabicroots #family #muslim",
 "tree": "Three letters, one meaning, and a whole family tree grows out of them 🌳 Did you get the last one? 👇 Send it to someone you love. #learnarabic #arabic #arabicroots #quran #muslim",
}
WHO = {"target": "a 27-year-old UK Muslim who prays but doesn't understand the Arabic", "revert": "a 31-year-old revert learning Arabic"}
Q = {"comment": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. How likely are they to comment?",
                 "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "share": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. How likely are they to send it to someone?",
               "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "trust": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. Does the caption feel honest and interesting rather than clickbait?",
               "criteria": ["Clickbait", "A bit", "Mostly honest", "Honest and interesting"]}}
if __name__ == "__main__":
    jobs = [(k, w) for k in C for w in WHO for _ in range(2)]
    with ThreadPoolExecutor(20) as ex: res = list(ex.map(lambda j: (j, ask({"ctx": CTX, "c": C[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
    for k in C:
        s = {q: sum(a[q]["score"] for (kk, _), a in res if kk == k) / 4 for q in Q}
        print(f"{k:10} comment {s['comment']:.2f}  share {s['share']:.2f}  trust {s['trust']:.2f}  total {sum(s.values()):.2f}")
