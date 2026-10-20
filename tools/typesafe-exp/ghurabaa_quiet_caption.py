# Caption for the voiceless strangers video (ghurabaa-quiet, 31 s, text only). Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/ghurabaa_quiet_caption.py
# Result (20 Oct 2026; comment / share / trust, target + revert x2): tuba 2.35 / 2.67 / 2.86 (chosen) · home 2.33 / 2.21 / 2.87 · maghrib 2.24 / 2.17 / 2.26.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 31-second TikTok/Instagram video with no voice, only text and soft sounds, from a small account teaching the Arabic Muslims use: "
       "'Islam is so strange… and the Prophet told us it would be'; the hadith (Muslim 145) typed in Arabic and English; the last word "
       "لِلْغُرَباءِ highlighted; it means strangers, one stranger غَرِيب, the root غ ر ب 'to go away, like the sun when it sets'; Maghrib, west and "
       "ghurba (far from home) from the same root; 'Be in this world as if you were a stranger or a traveller' (Bukhari 6416); ends "
       "'Are you one of the strangers? Comment below'. Caption under it: ")
WHO = {"target": "a 27-year-old UK Muslim who prays but doesn't understand the Arabic", "revert": "a 31-year-old revert learning Arabic"}
T = " #hadith #learnarabic #arabic #muslim #islam"
C = {"home": "A stranger is someone far from home. The Prophet ﷺ told us to live in this world like one, because our home is somewhere else 🤍 Are you one of the strangers? 👇" + T,
     "maghrib": "Every Maghrib, the sun goes away, and that's the same root as غَرِيب, the stranger 🌅 Watch it to the end, then tell me: are you one of the strangers? 👇" + T,
     "tuba": "فَطُوبى لِلْغُرَباءِ: glad tidings to the strangers 🤍 Save this for the days you feel like you don't fit in, and send it to someone who needs it." + T}
Q = {"comment": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. How likely are they to comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "share": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. How likely are they to save or send it to a friend?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "trust": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. Does the caption feel sincere and respectful for a post about a hadith?", "criteria": ["No", "A bit", "Mostly", "Yes"]}}
jobs = [(k, w) for k in C for w in WHO for _ in range(2)]
with ThreadPoolExecutor(12) as ex: res = list(ex.map(lambda j: (j, ask({"ctx": CTX, "c": C[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
for k in C:
    s = {q: sum(a[q]["score"] for (kk, _), a in res if kk == k) / 4 for q in Q}
    print(f"{k:8} comment {s['comment']:.2f}  share {s['share']:.2f}  trust {s['trust']:.2f}  total {sum(s.values()):.2f}")
