# Caption for m2-barik (17 Oct 2026). Adds to the video, never repeats it or the shouted hook.
# Result (17 Oct; comment / share / trust, 2 viewers x 2): baby 2.37 / 2.67 / 2.83 (chosen) · next 2.39 / 2.60 / 2.83 · both 2.39 / 2.61 / 2.67.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 58-second Instagram reel from a small account teaching the Arabic Muslims use. Hook: 'Do you KNOW the difference between mashallah "
       "and Allahumma barik?' It breaks down ما شاءَ اللهُ, plays al-Kahf 18:39 (a man told to say it over his own garden), then shows the Prophet "
       "taught praying for blessing, اللَّهُمَّ بارِكْ, over someone else's blessing (Ibn Majah 3509), the root of barakah and Eid Mubarak, and a test: "
       "'Look, my new baby!' → both. Caption under it: ")
WHO = {"target": "a 27-year-old UK Muslim who says mashallah daily but doesn't know Arabic", "revert": "a 31-year-old revert learning Arabic"}
C = {
 "baby": "Save this for the next baby announcement in the family group chat 👶🤍 Which one do you usually say? 👇 Send this to someone who says mashallah every day #mashallah #barakallah #learnarabic #arabic #muslim #islam",
 "both": "Most of us only say one of them. From today, say both 🤍 Which phrase should I break down next? 👇 Send this to someone who says mashallah every day #mashallah #barakallah #learnarabic #arabic #muslim #islam",
 "next": "Which phrase you say every day should I break down next? 👇 Send this to someone who says mashallah every day 🤍 #mashallah #barakallah #learnarabic #arabic #muslim #islam",
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
