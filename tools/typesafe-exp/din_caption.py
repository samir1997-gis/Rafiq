# Caption for d1-din (18 Oct 2026, #264): seventeen times a day. Hook "SEVENTEEN times a day... do you know what this word MEANS?" over the
# day's prayers clicking up to 17 rakʿahs; al-Fātiḥah 1:4; "you know دِين as religion, but here?" 3-2-1: repayment (Ibn Kathīr, from Ibn
# ʿAbbās); 6,205 times a year. Ends "Did you know this one? Comment yes or no below". The caption adds and gives no answer away.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/din_caption.py
# Result: not run yet (no TYPE_SAFE_KEY in the session that wrote it; #262).
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A TikTok/Instagram Reel from a small account teaching the Arabic Muslims use. A voice shouts 'Seventeen times a day... do you know "
       "what this word means?' over the day's five prayers ticking up to 17 rak'ahs; al-Fatiha's 'Master of the Day of ...'; 'you know deen "
       "as religion, but here?', a 3-2-1 quiz, the answer with Ibn Kathir's tafsir, then 17 a day becomes 6,205 a year. Ends: 'Did you know "
       "this one? Comment yes or no below.' Caption under it: ")
C = {
 "count": "Fajr 2, Dhuhr 4, ʿAsr 4, Maghrib 3, ʿIshāʾ 4. That's 17 before you count a single sunnah 🤲 Did you know this one? 👇 Send this to someone you pray with. #learnarabic #quran #alfatiha #salah #muslim",
 "notice": "Most of us learned the translation once and never looked at the word again 👀 Yes or no? 👇 Send this to someone you pray with. #learnarabic #quran #alfatiha #salah #muslim",
 "pray": "Next time you pray, listen for it in the fourth line 🤲 Did you know this one? 👇 #learnarabic #quran #alfatiha #salah #muslim",
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
