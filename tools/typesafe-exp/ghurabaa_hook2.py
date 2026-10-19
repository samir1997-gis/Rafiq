# Owner's hook for the strangers carousel v2: "ISLAM IS SO STRANGE!" alone, or with a line that points to the hadith.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/ghurabaa_hook2.py
# Result (19 Oct; 3 viewers x 2): alone swipe 2.26 respect 1.62 · with the line swipe 2.33 respect 2.10 (used).
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("Slide 1 of an Instagram photo carousel from a small Muslim account teaching Arabic. The next slides: the hadith 'Islam began as something "
       "strange and will return to being strange as it began, so glad tidings to the strangers' (Muslim 145), the word غُرَباء, its root, and "
       "'Be in this world as if you were a stranger'. Slide 1 says: ")
WHO = {"target": "a 27-year-old UK Muslim who prays but doesn't understand the Arabic", "revert": "a 31-year-old revert learning Arabic", "scroller": "a 22-year-old Muslim scrolling fast"}
H = {"alone": "ISLAM IS SO STRANGE!", "line": "ISLAM IS SO STRANGE! (smaller, under it:) …and the Prophet ﷺ said it would be."}
Q = {"swipe": {"type": "score", "instructions": "`ctx` `h` Viewer: `who`. How likely are they to swipe to the next slide?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "respect": {"type": "score", "instructions": "`ctx` `h` Viewer: `who`. Before swiping, does slide 1 alone feel respectful to Islam?", "criteria": ["No, it reads as mocking", "Unsure", "Mostly", "Yes"]}}
jobs = [(k, w) for k in H for w in WHO for _ in range(2)]
with ThreadPoolExecutor(12) as ex: res = list(ex.map(lambda j: (j, ask({"ctx": CTX, "h": H[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
for k in H:
    s = {q: sum(a[q]["score"] for (kk, _), a in res if kk == k) / 6 for q in Q}
    print(f"{k:6}", "  ".join(f"{q} {s[q]:.2f}" for q in Q))
