# Caption for i4-she-quiz v2 (13 Oct 2026): Callum shouts "MOST of you will get the second one WRONG!", then two 3-2-1 rounds
# (جَدّ grandfather → grandmother? then أَخ brother → sister?), ends "How many did you get? Zero, one, or two? Comment down below!".
# The caption must not give the answers away (جَدَّة, and أُخْت not أَخَة).
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/i4_caption.py
# Result (13 Oct; comment / share / trust, target + revert x2). Round 1, captions that repeat the reel: plain_ask 2.07 / 1.85 / 1.44 ·
#   dare 2.19 / 1.90 / 0.79 · rule_tease 2.15 / 1.96 / 1.10. Owner: "the caption is literally repeating the reel", so round 2 adds
#   something the video doesn't say: plain_ask 2.11 / 1.84 / 1.42 · beyond 1.91 / 1.58 / 2.36 (chosen: best total, by far the most
#   trusted) · challenge 2.02 / 1.90 / 0.96 · save_tip 2.17 / 1.70 / 1.64.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A TikTok/Instagram Reel from a small account teaching the Arabic Muslims use. The video: a voice shouts 'MOST of you will get "
       "the second one WRONG!', then two quick quizzes (if جَدّ is 'grandfather', what's 'grandmother'? then if أَخ is 'brother', "
       "what's 'sister'?), a 3-2-1 each, the answer, and 'How many did you get? Zero, one, or two? Comment down below!'. Caption under it: ")
WHO = {"target": "a 27-year-old UK Muslim who prays but doesn't understand the Arabic", "revert": "a 31-year-old revert learning Arabic"}
C = {
 "plain_ask": "Arabic quiz: he or she? 👨👩 جَدّ = grandfather. So what's “grandmother”? And if أَخ = brother, what's “sister”? How many did you get: 0, 1 or 2? Comment below 👇 Send this to your Arabic study buddy. #learnarabic #arabic #arabicgrammar #studyarabic #muslim",
 "beyond": "That little ة on the end is everywhere once you see it: صَلاة, جَنَّة, رَحْمَة 🤍 Which other words with ة do you know? Comment one 👇 #learnarabic #arabic #arabicgrammar #studyarabic #muslim",
 "challenge": "Got both? Then try this one: if مُسْلِم is a Muslim man, what's a Muslim woman? 👀 Answer in the comments 👇 Send this to your Arabic study buddy. #learnarabic #arabic #arabicgrammar #studyarabic #muslim",
 "save_tip": "Save this: in Arabic, ة on the end usually means feminine. Usually 👀 The second one is why you can't trust it every time. What was your score? 👇 #learnarabic #arabic #arabicgrammar #studyarabic #muslim",
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
