# Primary text + headline for the breaking-news image ad (#266). Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/ad_news_caption.py
# Result (19 Oct 2026; stop / click / respect, 3 viewers x 2): C 2.72 / 2.62 / 1.85 (chosen) · A 2.74 / 2.59 / 1.65 · B 2.70 / 2.58 / 1.37.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A paid Instagram/Facebook image ad. The image is a breaking-news front page: 'BREAKING NEWS · Rafiq is now live: the app that teaches you "
       "every word you say in salah', a photo of a man in sujood, 'Five times a day, millions pray in a language they don't understand', "
       "bullets: every word of the prayer plus 10 short surahs, 5 minutes a day, free for 7 days, no card. Button: Learn more. Ad text: ")
WHO = {"scroller": "a 24-year-old UK Muslim who prays but doesn't know Arabic", "learner": "a 35-year-old who tried to learn Arabic before and gave up", "revert": "a 29-year-old revert learning to pray"}
CAP = {"A": "You've prayed thousands of times. Do you know what you're saying? 🤲 Rafiq teaches you every word of your salah, from Allahu akbar to the salam, plus 10 short surahs. 5 minutes a day. Try it free for 7 days, no card needed. || Understand every word of your salah",
       "B": "BREAKING: You can now understand your own prayer 🗞️ Rafiq takes you through every word you say in salah, one 5-minute part a day. Start with the 5 words that make up a third of your prayer. Free for 7 days, no card. || Rafiq is now live: free for 7 days",
       "C": "Subhana rabbiyal a'la. You say it in every sujood. Now find out what it means, and every other word of your prayer 🤍 Rafiq: 5 minutes a day, free for 7 days, no card. || Know what you're saying in salah"}
Q = {"stop": {"type": "score", "instructions": "`ctx` `h` Viewer: `who`. How likely are they to stop and read it?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "click": {"type": "score", "instructions": "`ctx` `h` Viewer: `who`. How likely are they to tap Learn more?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "respect": {"type": "score", "instructions": "`ctx` `h` Viewer: `who`. How respectful and trustworthy does it feel for an ad about prayer?", "criteria": ["Not at all", "A bit", "Mostly", "Very"]}}
jobs = [(k, w) for k in CAP for w in WHO for _ in range(2)]
with ThreadPoolExecutor(18) as ex: r = list(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]].replace(" || ", " Headline: "), "who": WHO[j[1]]}, Q)["answers"]), jobs))
rows = [(k, {q: sum(a[q]["score"] for (kk, _), a in r if kk == k) / (2 * len(WHO)) for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(k, " ".join(f"{q} {s[q]:.2f}" for q in Q), f"total {sum(s.values()):.2f}")
