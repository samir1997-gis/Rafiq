# Owner's talking-to-camera Jumuah reel: opener, hook and closing ask.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 40-second Instagram reel, a Muslim man talking to the camera on a Friday, plain edit with captions. He opens in Arabic, "
       "'الحَمْدُ لِلَّهِ الَّذِي بَلَّغَنا جُمُعَةً أُخْرى' (praise be to Allah who let us reach another Jumuʿah), then three things to do on Jumuʿah, each with "
       "an authentic benefit: pray Jumuʿah (it wipes out the minor sins between one Jumuʿah and the next), send salawat on the Prophet ﷺ (it is presented to him), "
       "read Surah al-Kahf (a light between the two Fridays). ")
WHO = {"scroller": "a 22-year-old UK Muslim scrolling on a Friday morning", "busy": "a 36-year-old working dad who often misses the Friday sunnahs",
       "revert": "a 30-year-old revert learning about Jumuʿah"}
A = {"arabic then hook, ask salawat": "First 3 seconds: the Arabic line with on-screen text 'Don't let this Jumuʿah pass without these 3 things'. Ends: 'Send salawat on the Prophet ﷺ in the comments 👇'",
     "arabic then hook, ask which": "First 3 seconds: the Arabic line with on-screen text 'Don't let this Jumuʿah pass without these 3 things'. Ends: 'Which one will you do today? Comment 1, 2 or 3 👇'",
     "hook first, ask salawat": "First 3 seconds: 'Don't let this Jumuʿah pass without these 3 things', then the Arabic line. Ends: 'Send salawat on the Prophet ﷺ in the comments 👇'",
     "arabic then hook, ask share": "First 3 seconds: the Arabic line with on-screen text 'Don't let this Jumuʿah pass without these 3 things'. Ends: 'Send this to someone to remind them 🤍'"}
Q = {"stay": {"type": "score", "instructions": "`ctx` `h` Viewer: `who`. How likely are they to keep watching past the first 3 seconds?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "comment": {"type": "score", "instructions": "`ctx` `h` Viewer: `who`. How likely are they to comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "share": {"type": "score", "instructions": "`ctx` `h` Viewer: `who`. How likely are they to share it?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "sincere": {"type": "score", "instructions": "`ctx` `h` Viewer: `who`. How sincere and fitting does it feel?", "criteria": ["Off-putting", "A bit off", "Fitting", "Very fitting"]}}
jobs = [(k, w) for k in A for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": A[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / len(WHO) for q in Q}) for k in A]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:32}" + "".join(f"{q} {s[q]:.2f}  " for q in Q) + f"total {sum(s.values()):.2f}")
