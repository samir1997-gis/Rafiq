# Caption for tomorrow-people V3, "The sun has risen from the west. It's too late." (29 Oct 2026): the owner talking to camera,
# the hadith card (Muslim 2703), at-taswīf from sawfa, al-Ḥijr 15:3 recited and highlighted, "start today", comment NOW for a starter pack.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/tomorrow_sun_caption.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 78-second talking-head Reel from Rafiq (an Arabic-learning account for Muslims): 'The sun has risen from the west: it's too late. The doors of "
       "repentance have been shut. Believing now will not benefit anyone' (hadith card, Muslim 2703); there's an Arabic word for putting it off, at-taswif, "
       "from sawfa, 'I will, later'; Allah describes these people in Surah al-Hijr 15:3 (recited, each phrase lit up: let them eat and enjoy, distracted by "
       "false hope, they will come to know); don't say you'll start tomorrow, start today; comment NOW and I'll send you a starter pack.")
WHO = {"young": "a 22-year-old UK Muslim who keeps putting off praying", "learner": "a 34-year-old who wants to learn Arabic for the Qur'an",
       "parent": "a 41-year-old Muslim parent"}
T = "#islam #muslim #reminder #quran #learnarabic"
CAP = {"S1": f"One day the sun will rise from the west, and the door will shut 🌅 Until then it's open. There's even an Arabic word for “I'll do it later”: at-taswīf. Comment NOW for a starter pack 👇 {T}",
       "S2": f"“Sawfa”: I will, later. Allah uses it in al-Ḥijr 15:3: فَسَوْفَ يَعْلَمُونَ, they will come to know 😔 Don't be a tomorrow person. Comment NOW and I'll send you a starter pack 👇 {T}",
       "S3": f"Reminder to self first 🤍 The sun rising from the west is the day it's too late (Muslim 2703). Today it isn't. Start today: comment NOW for a free starter pack 👇 {T}",
       "S4": f"What are you putting off until tomorrow? 🌅 Tomorrow isn't promised. Comment NOW and I'll send you a starter pack to begin today 👇 {T}"}
Q = {"comment": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to comment NOW?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "share": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to share or save it?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "trust": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How sincere and trustworthy does it feel (not clickbait)?", "criteria": ["Clickbait", "A bit", "Mostly sincere", "Sincere"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':6}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:6}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
