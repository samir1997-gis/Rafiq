# Hook for the strangers carousel (Sahih Muslim 145, the root غ ر ب). Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/ghurabaa_hook.py
# Result (19 Oct; swipe / share / respect, target + revert x2): root 8.06 · maghrib 8.04 (used: question hooks hold best) · tuba 8.03.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("Slide 1 of an Instagram photo carousel from a small account teaching the Arabic Muslims use. The carousel goes on to the hadith "
       "'Islam began as something strange and will return to being strange as it began, so glad tidings to the strangers' (Muslim 145) word by "
       "word, then the root غ ر ب (going away, the sun setting): غَرَبَ the sun set, الْمَغْرِب the sunset prayer / the west, غَرِيب stranger, غُرَباء strangers. "
       "Slide 1 says: ")
WHO = {"target": "a 27-year-old UK Muslim who prays but doesn't understand the Arabic", "revert": "a 31-year-old revert learning Arabic"}
H = {"maghrib": "What does a stranger have to do with Maghrib? 🌅 (غَرِيب · الْمَغْرِب)",
     "root": "“Stranger” and Maghrib come from the SAME Arabic root 🌅",
     "tuba": "“Glad tidings to the strangers.” Do you know what غَرِيب really means?"}
Q = {"swipe": {"type": "score", "instructions": "`ctx` `h` Viewer: `who`. How likely are they to swipe to the next slide?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "share": {"type": "score", "instructions": "`ctx` `h` Viewer: `who`. How likely are they to save or send the carousel?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "respect": {"type": "score", "instructions": "`ctx` `h` Viewer: `who`. How respectful is it for a post about a hadith?", "criteria": ["Not at all", "A bit", "Mostly", "Very"]}}
jobs = [(k, w) for k in H for w in WHO for _ in range(2)]
with ThreadPoolExecutor(12) as ex: res = list(ex.map(lambda j: (j, ask({"ctx": CTX, "h": H[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
for k in H:
    s = {q: sum(a[q]["score"] for (kk, _), a in res if kk == k) / 4 for q in Q}
    print(f"{k:8}", "  ".join(f"{q} {s[q]:.2f}" for q in Q), f" total {sum(s.values()):.2f}")
