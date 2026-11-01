# Urdu doctor (#313), per platform (1 Nov 2026): YouTube Shorts titles and TikTok captions. Instagram's is urdu_doctor_caption.py (A_score).
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/urdu_doctor_platforms.py
exec(open("tools/typesafe-exp/urdu_doctor_caption.py").read().split("WHO =")[0])
CTX = CTX.replace("'HUNDREDS of Arabic words... if you speak Urdu, you already know them, and nobody tells you!'", "'If you speak Urdu, you already know HUNDREDS of Arabic words!'")
WHO = {"urdu": "a 24-year-old British Pakistani Muslim who speaks Urdu at home", "learner": "a 33-year-old Urdu speaker who wants to understand the Qur'an",
       "teen": "a 19-year-old Pakistani Muslim scrolling on their phone"}
CAP = {"YT_hundreds": "If You Speak Urdu, You Already Know HUNDREDS of Arabic Words 🤯 #shorts",
       "YT_doctor": "Urdu Speakers Already Know These 6 Arabic Words 🩺 #shorts",
       "YT_same": "Urdu and Arabic Use the SAME Words 😳 #urdu #arabic",
       "TT_score": "If you speak Urdu, you already know more Arabic than you think 👀 How many did you get? /6 👇 #urdu #arabic #learnarabic #desi #pakistani #muslimtiktok",
       "TT_tag": "Tag someone who speaks Urdu 👇 they've been speaking Arabic this whole time 😅 #urdu #arabic #learnarabic #desi #pakistani #muslimtiktok",
       "TT_next": "Mareez, tabeeb, dawa, ilaaj… it's all Arabic 🩺 Where should we go next? 👇 #urdu #arabic #learnarabic #desi #pakistani #muslimtiktok"}
Q = {"stop": {"type": "score", "instructions": "`ctx` Text under/over the video: `h`. Viewer: `who`. How likely are they to stop and watch?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "engage": {"type": "score", "instructions": "`ctx` Text under/over the video: `h`. Viewer: `who`. How likely are they to comment, share or save?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "follow": {"type": "score", "instructions": "`ctx` Text under/over the video: `h`. Viewer: `who`. How likely are they to follow or subscribe?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':12}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: (x[0][:2], -sum(x[1].values()))): print(f"{k:12}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
