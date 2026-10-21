# Primary text + headline for the level-up video ad (#273). Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/ad_levelup_caption.py
# Result (21 Oct 2026; stop / click / respect, 3 viewers x 2): C 2.49 / 2.22 / 1.95 (chosen) · B 2.51 / 2.24 / 1.82 · A 2.40 / 2.18 / 1.81.
# Only the 7-day free trial is promised here: the video's 30-day refund differs from the terms (14 days), the owner decides that.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A paid Instagram/Facebook video ad: the founder, a young British Muslim, talks to camera: 'It's not enough to be passive Muslims anymore. "
       "We have to level up, invest in ourselves and our deen. The easiest way is studying Arabic: the Quran came down in Arabic.' The app is shown on a "
       "phone (salah words, pray along); 'one month costs about the same as a cup of coffee'; 'sign up to RafiqArabic.com, 7-day free trial, no card'. Ad text: ")
WHO = {"scroller": "a 24-year-old UK Muslim who prays but doesn't know Arabic", "learner": "a 35-year-old who tried to learn Arabic before and gave up", "parent": "a 40-year-old Muslim parent in London who feels the kids are drifting from the deen"}
CAP = {"A": "It's not enough to be a passive Muslim anymore. The Quran came down in Arabic, so that's where levelling up starts 🤍 Rafiq teaches you the Arabic of your salah in 5 minutes a day. Free for 7 days, no card. || Level up your deen",
       "B": "The odds are stacked against Muslims in the West. Don't just get through the day: invest in your deen. Learn the words of your salah with Rafiq, 5 minutes a day. 7-day free trial, no card needed. || Level up as a Muslim",
       "C": "Imagine understanding every word you say to Allah in salah 🤲 That's what levelling up looks like. Rafiq: 5 minutes a day, the words you actually pray. Try it free for 7 days, no card. || Start your 7-day free trial"}
Q = {"stop": {"type": "score", "instructions": "`ctx` `h` Viewer: `who`. How likely are they to stop and read it?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "click": {"type": "score", "instructions": "`ctx` `h` Viewer: `who`. How likely are they to tap Learn more?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "respect": {"type": "score", "instructions": "`ctx` `h` Viewer: `who`. How respectful and trustworthy does it feel for an ad about the deen?", "criteria": ["Not at all", "A bit", "Mostly", "Very"]}}
jobs = [(k, w) for k in CAP for w in WHO for _ in range(2)]
with ThreadPoolExecutor(18) as ex: r = list(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]].replace(" || ", " Headline: "), "who": WHO[j[1]]}, Q)["answers"]), jobs))
rows = [(k, {q: sum(a[q]["score"] for (kk, _), a in r if kk == k) / (2 * len(WHO)) for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(k, " ".join(f"{q} {s[q]:.2f}" for q in Q), f"total {sum(s.values()):.2f}")
