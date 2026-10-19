# Caption for the time-words carousel (#268): "Today · Tomorrow · Yesterday · Now · After that. Can you say all 5 in Arabic?", one word per
# slide with the course's sentence (in shā' Allāh I'll visit you tomorrow; I'll do wudu now; the last slide asks "what do you do after Fajr?").
# Same test as questions_caption.py. Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/time_carousel_caption.py
# Result (19 Oct; comment / share / trust, target + revert x2): sentence 2.40 / 2.58 / 1.90 (chosen) · series 2.37 / 2.44 / 1.95 · fajr 2.21 / 2.51 / 1.93.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("An Instagram/TikTok photo carousel from a small account teaching the Arabic Muslims use. Slide 1: 'Today, Tomorrow, Yesterday, Now, "
       "After that. Can you say all 5 in Arabic?' Then one word per slide with an example sentence: الْيَوْمَ 'How's the weather today?', غَدًا "
       "'God willing, I'll visit you tomorrow', أَمْسِ 'The weather was cold yesterday', الآنَ 'I'll do wudu now', بَعْدَ ذَلِكَ 'After that I go to "
       "work' with 'what do you do after Fajr?'. Last slide: 'How many did you know? Comment /5'. Caption under it: ")
WHO = {"target": "a 27-year-old UK Muslim who prays but doesn't understand the Arabic", "revert": "a 31-year-old revert learning Arabic"}
T = " #learnarabic #arabic #arabicwords #muslim #islam"
C = {"fajr": "Bonus question on the last slide: what do you do after Fajr? Answer in Arabic if you can, starting with بَعْدَ ذَلِكَ 👇 Save this for later 📌" + T,
     "sentence": "Now put them together: can you say “I'll do wudu now” or “I'll visit you tomorrow” without looking? Comment it 👇 Save this 📌" + T,
     "series": "After who, what, where and when, here's WHEN in real life: 5 time words you'll use every day. How many did you know? Comment /5 👇 Save this 📌" + T}
Q = {"comment": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. How likely are they to comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "share": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. How likely are they to save or send it to a friend?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "trust": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. Does the caption feel honest and respectful rather than clickbait?", "criteria": ["Clickbait", "A bit", "Mostly honest", "Honest and interesting"]}}
jobs = [(k, w) for k in C for w in WHO for _ in range(2)]
with ThreadPoolExecutor(20) as ex: res = list(ex.map(lambda j: (j, ask({"ctx": CTX, "c": C[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
for k in C:
    s = {q: sum(a[q]["score"] for (kk, _), a in res if kk == k) / 4 for q in Q}
    print(f"{k:8} comment {s['comment']:.2f}  share {s['share']:.2f}  trust {s['trust']:.2f}  total {sum(s.values()):.2f}")
