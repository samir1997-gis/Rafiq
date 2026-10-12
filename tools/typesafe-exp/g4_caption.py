# Caption for the remade g4-past-i (12 Oct 2026: spoken hook "MOST people learn Arabic for years before they notice this trick!",
# two 3-2-1 rounds, كَتَبَ → I wrote, ذَهَبَ → I went, ends "How many did you get? Zero, one, or two? Comment down below!").
# The caption must not give the answer (ـتُ) away, repeats the hook, asks for the comment and a share.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/g4_caption.py
# Result (12 Oct; comment / share / trust, target + revert x2): old 2.23 / 1.66 / 1.64 · new (MOST hook in the caption) 2.08 / 1.84 / 0.67 ·
#   plain_ask 2.09 / 1.93 / 1.30 (chosen: the video's own ask, best shares) · new_short 2.06 / 1.92 / 0.62. The bold hook works spoken, not written.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A TikTok/Instagram Reel from a small account teaching the Arabic Muslims use. The video: a voice says 'MOST people learn Arabic "
       "for years before they notice this trick!', then two quick quizzes (if كَتَبَ is 'he wrote', what's 'I wrote'? then 'I went'), "
       "a 3-2-1 each, the answer, and 'How many did you get? Zero, one, or two? Comment down below!'. Caption under it: ")
WHO = {"target": "a 27-year-old UK Muslim who prays but doesn't understand the Arabic", "revert": "a 31-year-old revert learning Arabic"}
C = {
 "old": "Arabic verb quiz ✍️ كَتَبَ = he wrote. So what's “I wrote”? And “I went”? Pause and drop your answers below 👇 Spot the pattern once, use it on every verb. #learnarabic #arabic #arabicverbs #studyarabic #muslim",
 "new": "MOST people learn Arabic for years before they notice this trick 👀 كَتَبَ = he wrote. So what's “I wrote”? And “I went”? How many did you get: 0, 1 or 2? Comment below 👇 and send this to your Arabic study buddy. #learnarabic #arabic #arabicverbs #studyarabic #muslim",
 "plain_ask": "Arabic verb quiz ✍️ كَتَبَ = he wrote. So what's “I wrote”? And “I went”? How many did you get: 0, 1 or 2? Comment below 👇 Spot the pattern once, use it on every verb. Send this to your Arabic study buddy. #learnarabic #arabic #arabicverbs #studyarabic #muslim",
 "new_short": "MOST people miss this trick for years 👀 If كَتَبَ is “he wrote”, what's “I wrote”? 0, 1 or 2? Comment below 👇 Send it to your Arabic study buddy. #learnarabic #arabic #arabicverbs #studyarabic #muslim",
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
