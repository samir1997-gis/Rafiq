# Caption for n5-salah (24 Oct 2026, #290): the word tree, part 4. Hook "You do it FIVE times a day… but what does salah really mean?" over
# the five prayers counted 1 to 5; حَيَّ عَلَى الصَّلاةِ from the adhān; ص ل و grows الصَّلاة and مُصَلَّى; your turn فَلْيُصَلِّ (ṣalāh, duʿāʾ or
# eat?), 3-2-1, make duʿāʾ (Muslim 1431; al-Tirmidhī 780 "meaning duʿāʾ"). Ends "Comment below: who's the first person you make dua for?
# And send this to them", then the owner's end card. The caption repeats the hook question and gives no answer away (no "duʿāʾ" in it).
# Not run yet: no TYPE_SAFE_KEY in the session that made it (#262).
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/salah_caption.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A TikTok/Instagram Reel from a small account teaching the Arabic Muslims use. A voice asks 'You do it five times a day, but what does "
       "salah really mean?' over the five prayers counted 1 to 5; the adhan's 'come to prayer' shows the root of salah; the prayer and a "
       "place of prayer grow on a tree from it; then a quiz on a word from a hadith (a fasting guest is told to 'pray' for his host: does "
       "it mean salah, dua or eat?), 3-2-1, it means make dua; so every salah is a dua. Ends: 'Comment below: who's the first person you "
       "make dua for? And send this to them.' Caption under it: ")
C = {
 "question": "You do it five times a day… but what does ṣalāh really mean? 🤔 Play along with the 3-2-1, then send this to someone you always pray for 🤍 #learnarabic #arabic #arabicroots #salah #muslimtiktok",
 "guess": "Ṣalāh, duʿāʾ or eat? 👀 One word from a hadith changes how you see the prayer you do five times a day. What did you guess? Comment 👇 #learnarabic #arabic #salah #hadith #muslimtiktok",
 "adhan": "You hear it in every adhān, but what does ṣalāh really mean? 🕌 Stay for the 3-2-1, and send this to someone you never forget in your prayers 🤍 #learnarabic #arabic #arabicroots #salah #adhan",
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
