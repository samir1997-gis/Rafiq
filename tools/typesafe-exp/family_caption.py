# Caption for f4-family (18 Oct 2026, #265): the family tree. Hook "TWO words for 'aunty' in Arabic, and one's like your MUM!"; the tree
# in Arabic; the camera zooms into dad's sister (عَمَّة) and mum's sister (خالَة); the fun fact: Ḥamza's daughter went to her khala, "the
# maternal aunt is in the place of the mother" (al-Bukhārī 2699); your turn: mum's brother, 3-2-1, خال. Ends "Tag your khala in the
# comments, and tell her she's basically your mum!". The caption adds to the video and gives no answer away.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/family_caption.py
# Result: not run yet (no TYPE_SAFE_KEY in the session that wrote it; #262).
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A TikTok/Instagram Reel from a small account teaching the Arabic Muslims use. A voice says 'Two words for aunty in Arabic, and one's "
       "like your mum!' over a family popping in; a family tree in Arabic, dad's side and mum's side; the camera zooms into dad's sister "
       "(amma) and mum's sister (khala); the story of Hamza's daughter given to her khala, with the hadith 'the maternal aunt is in the place "
       "of the mother'; then a 3-2-1 quiz on what to call mum's brother. Ends: 'Tag your khala in the comments, and tell her she's basically "
       "your mum!' Caption under it: ")
C = {
 "uncle": "Uncles too: dad's side and mum's side get different words. Did you get the last one? Tag your khala 👇 #learnarabic #arabic #arabicwords #family #muslim",
 "grandma": "Grandma and grandpa are the same on both sides: جَدَّة and جَدّ 👵🏽👴🏽 Only the aunts and uncles split. Tag your khala 👇 #learnarabic #arabic #arabicwords #family #muslim",
 "story": "Three men wanted to raise Ḥamza's daughter. She went to her khala 🤍 Tag yours below 👇 #learnarabic #arabic #hadith #family #muslim",
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
