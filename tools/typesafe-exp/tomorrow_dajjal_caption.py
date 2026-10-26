# Caption for tomorrow-v2-dajjal (#292), posted as a trial reel: the hook "The Dajjal has come out. It's too late. The sun has risen
# from the west… the doors of repentance have been shut", then the tomorrow people, the grave, "start today", and "comment NOW and
# I'll send you a starter pack" (the 20 words of your salah). Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/tomorrow_dajjal_caption.py
# Result (26 Oct 2026; comment / share / trust, 2 viewers x 3): E3 1.45 / 1.90 / 1.61 (chosen) · E2 1.43 / 1.74 / 1.69 · E1 1.56 / 1.93 / 1.33 ·
# D2 1.59 / 1.90 / 0.24 (the starter-pack ask in the caption reads as comment bait; the video already asks for it).
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("An Instagram Reel by a young British Muslim: 'The Dajjal has come out: it's too late. The sun has risen from the west: it's too "
       "late. The doors of repentance have been shut.' (a door slams on screen, Sahih Muslim 158). Then a skit of 'I'll start tomorrow', "
       "'the grave is full of people who said we will start tomorrow', 'start today', and 'comment NOW and I'll send you a starter pack' "
       "(the 20 words of your salah). Caption under it: ")
C = {
 "D2": "How many times have you said “I’ll start tomorrow”? 😔 Be honest 👇 Comment NOW for the free starter pack (the 20 words of your salah) and send this to someone who needs it 🤍 #islam #muslim #salah #learnarabic #reminder",
 "E1": "A reminder for me before anyone else 🤍 Tomorrow isn’t promised. What’s the one thing you keep putting off? 👇 #islam #muslim #salah #reminder #learnarabic",
 "E2": "“I’ll start tomorrow” 😔 We’ve all said it. Today the door is still open, so start with one small step. What are you starting today? 👇 #islam #muslim #salah #reminder #learnarabic",
 "E3": "Reminder to self first 🤍 The door of repentance is open until the sun rises from the west (Muslim 2703). Don’t wait for tomorrow. What are you starting today? 👇 #islam #muslim #reminder #salah #learnarabic",
}
WHO = {"target": "a 24-year-old UK Muslim who prays on and off", "learner": "a 30-year-old who keeps meaning to learn Arabic"}
Q = {"comment": {"type": "score", "instructions": "`ctx` `c` Viewer: `who` (doesn't follow the account). How likely are they to comment?",
                 "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "share": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. How likely are they to send it to someone or save it?",
               "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "trust": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. Does the caption feel sincere rather than fear-mongering or an ad?",
               "criteria": ["Fear-mongering / ad", "A bit", "Mostly sincere", "Sincere"]}}
if __name__ == "__main__":
    jobs = [(k, w) for k in C for w in WHO for _ in range(3)]
    with ThreadPoolExecutor(18) as ex: res = list(ex.map(lambda j: (j, ask({"ctx": CTX, "c": C[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
    for k in C:
        s = {q: sum(a[q]["score"] for (kk, _), a in res if kk == k) / 6 for q in Q}
        print(f"{k} comment {s['comment']:.2f}  share {s['share']:.2f}  trust {s['trust']:.2f}  total {sum(s.values()):.2f}")
