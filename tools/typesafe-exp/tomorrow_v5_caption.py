# Caption for tomorrow-people V5, "Shaytan's biggest ploy" (3 Nov 2026).
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/tomorrow_v5_caption.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("An 89-second talking-head Reel from Rafiq (an Arabic-learning account for Muslims): 'It's one of Shaytan's biggest ploys. Shaytan knows full "
       "well that tomorrow isn't guaranteed, and as long as he can keep delaying you, he knows he will win' (a clock whose hands get pushed back). A skit: "
       "'Just leave it, I'll start tomorrow': these are the tomorrow people. The Dajjal has come out: too late. The sun has risen from the west: too late; "
       "believing then won't benefit anyone (Muslim 158). They keep winding down your clock until tomorrow never comes. Don't waste the opportunity, start "
       "today: comment NOW and I'll send you a starter pack.")
WHO = {"young": "a 22-year-old UK Muslim who keeps putting off praying", "learner": "a 34-year-old who wants to learn Arabic for the Qur'an",
       "parent": "a 41-year-old Muslim parent"}
T = "#islam #muslim #reminder #quran #learnarabic"
CAP = {"self": f"Reminder to myself first 🤍 “I'll start tomorrow” is one of Shaytan's biggest plots. What have you been putting off? Comment NOW for a free starter pack 👇 {T}",
       "self2": f"Reminder to myself first 🤍 “I'll start tomorrow” is one of Shaytan's biggest plots, because tomorrow was never promised. What's the one thing you'll start today? Tell me below 👇 (comment NOW and I'll send you a free Arabic starter pack) {T}",
       "ayah": f"“No soul knows what it will earn tomorrow” (Luqmān 31:34) 🤍 “I'll start tomorrow” is one of Shaytan's biggest plots. Start today: comment NOW and I'll send you a free starter pack to begin learning the Qur'an's Arabic {T}",
       "honest": f"I've been a tomorrow person too 🤍 “I'll start tomorrow” is one of Shaytan's biggest plots. If you've been putting off learning the Qur'an's Arabic, comment NOW and I'll send you a free starter pack, in shā' Allāh {T}"}
exec("Q =" + open("tools/typesafe-exp/tomorrow_sun_caption.py").read().split("Q =")[1])
