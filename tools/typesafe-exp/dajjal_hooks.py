# Stronger hooks for the Dajjāl script (owner, 2 Nov 2026: "give me a few stronger hooks"), tested against the current one (base), two runs each.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/dajjal_hooks.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A talking-head Reel from Rafiq, an account teaching the Arabic Muslims use; a young British Muslim to camera, about the word Dajjāl: "
       "it comes from a root meaning to coat or gild (paint gold over something), there will be about thirty dajjāls, the greatest paints Hell to look "
       "like Paradise, kāfir is written between his eyes and every believer will read it. ")
WHO = {"young": "a 20-year-old UK Muslim who scrolls a lot", "practising": "a 30-year-old practising Muslim", "learner": "a 35-year-old learning Arabic for the Qur'an"}
H = {"base": "\"Dajjāl\" isn't a name. It's a word, and it tells you exactly what he does.",
     "gold": "The Dajjāl isn't coming with horns. He's coming covered in gold.",
     "paradise": "The Dajjāl will show you Paradise. Don't walk in.",
     "read": "There's one Arabic word you'll be able to read on the Dajjāl's face, even if you can't read.",
     "fool": "The Dajjāl's name already tells you how he'll fool you.",
     "thirty": "The Prophet ﷺ warned us about thirty dajjāls. Most people only know about one.",
     "recognise": "You'll recognise the Dajjāl by one word. Do you know which?",
     "paint": "His name means \"the one who paints gold over things\". And that's exactly how he'll trick you.",
     "read2": "The Prophet ﷺ said every believer will read one word on the Dajjāl's forehead, even those who can't read.",
     "read3": "One Arabic word is written on the Dajjāl's face. The Prophet ﷺ said every believer will be able to read it.",
     "fool2": "The Prophet ﷺ told us how the Dajjāl will fool people, and it's hidden in his name."}
Q = {"stop": {"type": "score", "instructions": "`ctx` The first line said to camera: `s` Viewer: `who`, scrolling. How likely are they to stop and keep watching?",
              "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "fair": {"type": "score", "instructions": "`ctx` The first line said to camera: `s` Viewer: `who`. Does it feel sincere and respectful, not clickbait?",
              "criteria": ["No", "A bit", "Mostly", "Yes"]}}
jobs = [(k, w) for k in H for w in WHO for _ in range(2)]
with ThreadPoolExecutor(12) as ex: res = list(ex.map(lambda j: (j, ask({"ctx": CTX, "s": H[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
rows = []
for k in H:
    a = [x for (kk, _), x in res if kk == k]
    rows.append((k, sum(x["stop"]["score"] for x in a) / len(a), sum(x["fair"]["score"] for x in a) / len(a)))
for k, s, f in sorted(rows, key=lambda r: -r[1]): print(f"{k:10} stop {s:.2f}  fair {f:.2f} | {H[k]}")
