# YouTube Shorts title for h4-khutbah v2 (30 Oct 2026, #310): which title gets the click and the watch-through.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/khutbah_youtube.py
exec(open("tools/typesafe-exp/khutbah_v2_caption.py").read().split("WHO =")[0])
WHO = {"search": "a 24-year-old Muslim who searched 'khutbah meaning' on YouTube", "learner": "a 32-year-old learning Arabic browsing Shorts",
       "scroller": "a 19-year-old UK Muslim swiping YouTube Shorts on a Friday"}
CAP = {"same": "Your Imam and Your Fiancé Have the SAME Name in Arabic 🤯 #shorts",
       "mark": "Khutbah vs Khitbah: One Tiny Mark Changes Everything 😳 #arabic",
       "quiz": "Sermon or Proposal? Only Arabic Learners Get This 👀 #learnarabic",
       "word": "The Arabic Word for Imam AND Fiancé 💍🕌 Khatib Explained #shorts"}
Q = {"click": {"type": "score", "instructions": "`ctx` YouTube Shorts title: `h`. Viewer: `who`. How likely are they to stop and watch?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "watch": {"type": "score", "instructions": "`ctx` YouTube Shorts title: `h`. Viewer: `who`. How likely are they to watch to the end and loop?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "engage": {"type": "score", "instructions": "`ctx` YouTube Shorts title: `h`. Viewer: `who`. How likely are they to like, comment or subscribe?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
