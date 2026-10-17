# Caption for m1-mashallah (17 Oct 2026). The caption adds to the video, never repeats it or the shouted hook.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/mashallah_caption.py
# Result (17 Oct; comment / share / trust, 2 viewers x 2): next 2.35 / 2.49 / 2.85 (chosen) · baby 2.31 / 2.50 / 2.68 · friend 2.21 / 2.33 / 2.61.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 60-second Instagram reel from a small account teaching the Arabic Muslims use. Hook: 'MOST people don't know mashallah is in the "
       "PAST tense!' It breaks down ما شاءَ اللهُ ('what Allah has willed'), says it's for good that's already there and the future takes in shā' "
       "Allāh, shows the root (will, a thing), plays al-Kahf 18:39 recited, then a test: 'See you at Jumuʿah tomorrow!': mashallah or inshallah? "
       "Caption under it: ")
WHO = {"target": "a 27-year-old UK Muslim who says mashallah daily but doesn't know Arabic", "revert": "a 31-year-old revert learning Arabic"}
C = {
 "baby": "Next time someone shows you their new baby, new job or exam results, you'll know exactly what you're saying 🤍 Did you get the test right? 👇 Send this to someone who says mashallah every day #mashallah #inshallah #learnarabic #arabic #muslim #islam",
 "friend": "Did you get the test right? Be honest 👇 Then send this to the friend who says mashallah about tomorrow 😅 #mashallah #inshallah #learnarabic #arabic #muslim #islam",
 "next": "Which phrase you say every day should I break down next? 👇 Send this to someone who says mashallah every day 🤍 #mashallah #inshallah #learnarabic #arabic #muslim #islam",
}
Q = {"comment": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. How likely are they to comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "share": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. How likely are they to save or send it to a friend?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "trust": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. Does the caption add something rather than repeat the video, and feel warm, not preachy?", "criteria": ["No", "A bit", "Mostly", "Yes"]}}
if __name__ == "__main__":
    jobs = [(k, w) for k in C for w in WHO for _ in range(2)]
    with ThreadPoolExecutor(20) as ex: res = list(ex.map(lambda j: (j, ask({"ctx": CTX, "c": C[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
    for k in C:
        s = {q: sum(a[q]["score"] for (kk, _), a in res if kk == k) / 4 for q in Q}
        print(f"{k:8} comment {s['comment']:.2f}  share {s['share']:.2f}  trust {s['trust']:.2f}  total {sum(s.values()):.2f}")
