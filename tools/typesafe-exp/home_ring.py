# What Home's big ring should measure (owner, 4 Nov 2026, #339: "0 out of 2 steps is a bit useless… something more meaningful, like the
# percentage of the unit you've completed, or the percentage of words in your salah"). Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/home_ring.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("The home screen of Rafiq, a phone web app that teaches UK Muslims the Arabic of the Qur'an and salah. At the top, under the greeting, a big "
       "progress ring. The learner has 100 words, is on step 10 of 24 of Unit 3 (Housing), has done 2 of 12 units, understands 42 of the 238 words of "
       "their salah, and has 0 of 2 steps done today. The ring shows: ")
R = {"steps": "'0/2 steps today'.",
     "salah": "'18%: of your salah you understand' (42 of 238 words).",
     "salah_top": "'You understand 18% of your salah', with 'next: al-Fātiḥah's last line' under it.",
     "unit": "'42%: Unit 3, Housing' (step 10 of 24).",
     "course": "'17% of the course' (2 of 12 units).",
     "words": "'100 words: you know 100 Arabic words'."}
WHO = {"new": "a 24-year-old UK Muslim in their first week on Rafiq", "busy": "a 37-year-old parent who opens it for 5 minutes at night",
       "keen": "a 29-year-old learner who studies every day and likes seeing progress"}
Q = {"meaning": {"type": "score", "instructions": "`ctx``r` User: `who`. How meaningful is this number to them?", "criteria": ["Not at all", "A little", "Quite", "Very"]},
     "back": {"type": "score", "instructions": "`ctx``r` User: `who`. How much does it make them want to come back tomorrow?", "criteria": ["Not at all", "A little", "Quite a lot", "A lot"]},
     "next": {"type": "score", "instructions": "`ctx``r` User: `who`. How much does it make them want to do a lesson right now?", "criteria": ["Not at all", "A little", "Quite a lot", "A lot"]}}
jobs = [(k, w) for k in R for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "r": R[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':12}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in R]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:12}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
