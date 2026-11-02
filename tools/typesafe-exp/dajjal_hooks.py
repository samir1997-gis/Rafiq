# Hooks for the Dajjāl script (owner, 2 Nov 2026), two runs each. Round 1 ("give me a few stronger hooks") is in the script's history; round 2 is his own three.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/dajjal_hooks.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A talking-head Reel from Rafiq, an account teaching the Arabic Muslims use; a young British Muslim to camera, about the word Dajjāl: "
       "it comes from a root meaning to coat or gild (paint gold over something), there will be about thirty dajjāls, the greatest paints Hell to look "
       "like Paradise, kāfir is written between his eyes and every believer will read it. ")
WHO = {"young": "a 20-year-old UK Muslim who scrolls a lot", "practising": "a 30-year-old practising Muslim", "learner": "a 35-year-old learning Arabic for the Qur'an"}
H = {   # round 2 (owner, 2 Nov 2026): his three hooks, the "thirty" one worded as the hadith says (about thirty), and two takes on his third
     "more": "Did you know there's more than one Dajjāl? Let me explain.",
     "thirty": "The Prophet ﷺ spoke about thirty dajjāls, but most people only know about one.",
     "met": "Have you met the dajjāl in your life?",
     "met2": "There's probably a dajjāl in your life right now. Let me explain.",
     "met3": "You've already met a dajjāl. You just didn't know the word for it.",
     "combo": "Did you know there's more than one Dajjāl? The Prophet ﷺ spoke about thirty. Let me explain."}
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
