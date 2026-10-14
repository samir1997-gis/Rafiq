# Caption for l1-ladder (14 Oct 2026): the difficulty ladder. The owner, stitched under it, asks seven questions that get harder
# (far, near, cold, hot, fat, thin, then the opposite of أَمِين "trustworthy"), a rail drops 90% → 5% "still in". Ends "How far did you
# get? Comment your score". The caption adds to the reel (owner, 13 Oct), states no percentage as data, gives no answers away.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/ladder_caption.py
# Result (14 Oct; comment / share / trust, target + revert x2): score 2.31 / 1.99 / 1.80 · boss 2.38 / 1.67 / 1.58 ·
#   honest 2.36 / 1.66 / 2.31 (chosen: best total, most trusted) · challenge 2.40 / 1.78 / 0.68.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A TikTok/Instagram Reel from a small account teaching the Arabic Muslims use. The creator asks seven Arabic questions that get "
       "harder each round (far, near, cold, hot, fat, thin, then a tough final one: the opposite of 'trustworthy'), while a rail on the "
       "side drops from 90% to 5% 'still in'. Ends: 'How far did you get? Comment your score.' Caption under it: ")
WHO = {"target": "a 27-year-old UK Muslim who prays but doesn't understand the Arabic", "revert": "a 31-year-old revert learning Arabic"}
C = {
 "score": "How far did you get? Drop your score out of 7 👇 No pausing, no Google 😅 Send it to the friend who says their Arabic is good. #learnarabic #arabic #arabicquiz #arabicwords #muslim",
 "boss": "Rounds 1–6 are words you'd meet in your first year. Round 7 is the one that catches people 😈 What did you get? 👇 #learnarabic #arabic #arabicquiz #arabicwords #muslim",
 "honest": "Each round really is harder: the words go from beginner to advanced on a research word list (Kelly, CEFR A1 → C1) 📈 How far did you get? 👇 #learnarabic #arabic #arabicquiz #arabicwords #muslim",
 "challenge": "Bet you can't get 7/7 👀 Comment your score and tag someone to beat it 👇 #learnarabic #arabic #arabicquiz #arabicwords #muslim",
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
