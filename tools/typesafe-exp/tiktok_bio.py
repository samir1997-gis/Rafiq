# TikTok bio (max 80 characters; the link field is rafiq-arabic.com/tt). Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/tiktok_bio.py
# Result (20 Oct 2026; follow / tap / clear, 3 viewers x 2): know 2.68 / 2.70 / 2.90 (chosen) · salah 2.58 / 2.67 / 2.95 · quiz 2.55 / 2.67 / 2.96.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("The TikTok profile of a small account that posts short videos on the Arabic Muslims say: salah lines word by word, word roots, quizzes. "
       "The app it links to (rafiq-arabic.com) teaches every word of the salah and everyday Arabic, 5 minutes a day, free for 7 days. The bio says: ")
WHO = {"target": "a 24-year-old UK Muslim who prays but doesn't understand the Arabic, landing on the profile from one video",
       "revert": "a 30-year-old revert learning to pray", "learner": "a 34-year-old who tried to learn Arabic before and gave up"}
B = {"salah": "Understand every word you say in salah 🤲\nArabic, 5 mins a day · free week ↓",
     "know": "You say it 5 times a day. Now know what it means 🤍\nSalah Arabic, word by word ↓",
     "quiz": "Arabic for your salah & everyday life 🤲\nNew quiz every week · free week ↓"}
Q = {"follow": {"type": "score", "instructions": "`ctx` `h` Viewer: `who`. How likely are they to follow?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "tap": {"type": "score", "instructions": "`ctx` `h` Viewer: `who`. How likely are they to tap the link?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "clear": {"type": "score", "instructions": "`ctx` `h` Viewer: `who`. How clearly do they know what this account is for, in a glance?", "criteria": ["Not at all", "Vaguely", "Mostly", "Instantly"]}}
for k, v in B.items(): assert len(v) <= 80, (k, len(v))
jobs = [(k, w) for k in B for w in WHO for _ in range(2)]
with ThreadPoolExecutor(18) as ex: res = list(ex.map(lambda j: (j, ask({"ctx": CTX, "h": B[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
for k in B:
    s = {q: sum(a[q]["score"] for (kk, _), a in res if kk == k) / 6 for q in Q}
    print(f"{k:6} ({len(B[k])} chars)", "  ".join(f"{q} {s[q]:.2f}" for q in Q), f" total {sum(s.values()):.2f}")
