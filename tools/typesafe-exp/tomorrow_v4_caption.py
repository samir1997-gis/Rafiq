# Caption for tomorrow-people V4, "Ya Allah, send us back." (30 Oct 2026): the owner talking to camera, the as-Sajdah 32:12 ayah card,
# "too late", the clock the shayatin wind down, "the grave is full of people who said we'll start tomorrow", comment NOW for a starter pack.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/tomorrow_v4_caption.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("An 86-second talking-head Reel from Rafiq (an Arabic-learning account for Muslims): 'There will be people thrown into Jahannam who will say: "
       "Ya Allah, give us another chance, send us back, this time we will worship You' (ayah card, as-Sajdah 32:12: 'Our Lord, we have seen and heard, "
       "so send us back; we will do good'); but it'll be too late. That's the problem with being a tomorrow person: tomorrow isn't guaranteed, and the "
       "shayatin keep winding down your clock until tomorrow never comes. The grave is full of people who said 'we will start tomorrow'. Start today: "
       "comment NOW and I'll send you a starter pack.")
WHO = {"young": "a 22-year-old UK Muslim who keeps putting off praying", "learner": "a 34-year-old who wants to learn Arabic for the Qur'an",
       "parent": "a 41-year-old Muslim parent"}
T = "#islam #muslim #reminder #quran #learnarabic"
CAP = {"B1": f"“Send us back, we'll do good” (as-Sajdah 32:12) 😔 One day people will beg for the chance you have right now. Don't be a tomorrow person. Comment NOW for a starter pack 👇 {T}",
       "B2": f"The grave is full of people who said “I'll start tomorrow” 🕰️ Tomorrow isn't promised. What have you been putting off? Comment NOW and I'll send you a starter pack 👇 {T}",
       "B3": f"Reminder to self first 🤍 They'll ask to be sent back, and it'll be too late. Today it isn't. Start today: comment NOW for a free starter pack 👇 {T}",
       "B4": f"Shaytan doesn't need you to say no. He just needs you to say “tomorrow” 🕰️ Start today: comment NOW and I'll send you a starter pack 👇 {T}"}
exec("Q =" + open("tools/typesafe-exp/tomorrow_sun_caption.py").read().split("Q =")[1])
