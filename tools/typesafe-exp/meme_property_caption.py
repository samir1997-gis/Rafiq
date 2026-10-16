# Caption for the owner's stitch of the "This ain't no state property, this is private property, hit the road dude" meme,
# translated into Arabic for fun (16 Oct 2026). Pure content: a laugh plus one useful phrase, a comment ask, no app.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/meme_property_caption.py
# Result (16 Oct; comment / share / fit, target + revert x2): next 2.10 / 1.73 / 2.46 · phrase 2.17 / 1.72 / 2.42 (chosen: a phrase
#   to keep and the meme ask) · tag 2.00 / 2.00 / 2.24. All three close.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A TikTok/Instagram Reel from a small account teaching the Arabic Muslims use. The creator stitches a famous meme (a man saying "
       "'This ain't no state property, this is private property, hit the road dude!') and says it back in Arabic, just for fun. Caption under it: ")
WHO = {"target": "a 27-year-old UK Muslim who prays but doesn't understand the Arabic", "revert": "a 31-year-old revert learning Arabic"}
C = {
 "next": "Hit the road, dude… but make it Arabic 😂 Which meme should I translate next? Comment it 👇 #learnarabic #arabic #arabicmemes #muslim #funny",
 "phrase": "Learn this one for your next argument 😂 مِلْكِيَّة خاصَّة (milkiyya khāṣṣa) = private property. Which meme should I do next? 👇 #learnarabic #arabic #arabicmemes #muslim #funny",
 "tag": "Tag the friend who says this when you sit in their seat 😂 مِلْكِيَّة خاصَّة = private property 🚫 #learnarabic #arabic #arabicmemes #muslim #funny",
}
Q = {"comment": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. How likely are they to comment?",
                 "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "share": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. How likely are they to send it to a friend?",
               "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "fit": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. Does it feel fun and natural for this account, not cringe?",
             "criteria": ["Cringe", "A bit off", "Fine", "Fun and natural"]}}
if __name__ == "__main__":
    jobs = [(k, w) for k in C for w in WHO for _ in range(2)]
    with ThreadPoolExecutor(20) as ex: res = list(ex.map(lambda j: (j, ask({"ctx": CTX, "c": C[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
    for k in C:
        s = {q: sum(a[q]["score"] for (kk, _), a in res if kk == k) / 4 for q in Q}
        print(f"{k:7} comment {s['comment']:.2f}  share {s['share']:.2f}  fit {s['fit']:.2f}  total {sum(s.values()):.2f}")
