# Home layout (owner, 4 Nov 2026, #339: "way too convoluted"): the current Home against the three options in design/home-options and
# the owner's mix (B's Today list with A's salah bar on top). Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/home_layout.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("The home screen of Rafiq, a phone web app that teaches UK Muslims the Arabic of the Qur'an and salah. The learner has 100 words, a 0-day "
       "streak, 0 of 2 steps done today and 116 words due for review. Under the greeting and today's lesson card (Unit 3, Meet 5 new words, Continue), it shows: ")
L = {"current": "a 'Your salah' card (42 of 238 words, Continue button); a streak tile (0, 'freeze back after 2 more goal days') next to a goal ring tile "
                "(0/2 steps); three tiles (100 words learned, 1 mastered, 2/12 units); a 'Next goal: 3 days' card with a paragraph about the spacing effect; "
                "a 'Get a daily reminder' card with a paragraph and two buttons; a '116 to review from your lessons · Review →' strip. Eight separate boxes.",
     "A_onecard": "inside the lesson card under Continue, one row: 🔥 0 day streak | 0/2 today's steps | 100 words; then a green bar '116 words to review, "
                  "recall them now so they stick →'; a slim 'Your salah · 42 of 238 words' row with a progress bar; one line of text '1 mastered · 2 of 12 "
                  "units · next goal: 3-day streak'; a small 'Get a daily reminder · Set up' row.",
     "B_list": "a 'TODAY' grouped list like iPhone Settings: Review (red badge 116) ›, Daily goal 0 of 2 steps, Streak 0 days; then a 'YOUR PROGRESS' "
               "list: Your salah 42/238 words ›, Words 100 learned · 1 mastered, Units 2 of 12 ›; a small line about reminders.",
     "C_ring": "the lesson card moved down: first a big ring '0/2 steps today', three chips (🔥 0 streak, 📚 100 words, 🧭 2/12 units), then the lesson "
               "and Continue, then two tiles: '116 to review →' and '42/238 salah words' with bars.",
     "D_mix": "a slim 'Your salah · 42 of 238 words' row with a progress bar; then a 'TODAY' grouped list like iPhone Settings: 🔁 Review (red badge "
              "116) ›, 🎯 Daily goal 0 of 2 steps, 🔥 Streak 0 days; then one line '100 words learned · 1 mastered · 2 of 12 units'; a small 'Get a "
              "daily reminder · Set up' row.",
     "D2_hints": "a slim 'Your salah · 42 of 238 words' row with a progress bar; then a 'TODAY' grouped list like iPhone Settings: 🔁 Review (red badge "
                 "116) ›, 🎯 Daily goal 0 of 2 steps with a small progress bar, 🔥 Streak 0 days · 'finish today's 2 steps to start one'; then one line "
                 "'100 words learned · 1 mastered · 2 of 12 units'; a small 'Get a daily reminder · Set up' row.",
     "D3_reviewbar": "a slim 'Your salah · 42 of 238 words' row with a progress bar; a green bar '116 words to review, recall them now so they stick →'; "
                     "then a 'TODAY' grouped list like iPhone Settings: 🎯 Daily goal 0 of 2 steps, 🔥 Streak 0 days; then one line "
                     "'100 words learned · 1 mastered · 2 of 12 units'; a small 'Get a daily reminder · Set up' row."}
WHO = {"new": "a 24-year-old UK Muslim in their first week on Rafiq", "busy": "a 37-year-old parent who opens it for 5 minutes at night",
       "keen": "a 29-year-old learner who studies every day and likes seeing progress"}
Q = {"clear": {"type": "score", "instructions": "`ctx``l` User: `who`. How clear is it what to do next?", "criteria": ["Not clear", "Somewhat", "Clear", "Very clear"]},
     "calm": {"type": "score", "instructions": "`ctx``l` User: `who`. How calm and uncluttered does it feel?", "criteria": ["Cluttered", "A bit busy", "Calm", "Very calm"]},
     "back": {"type": "score", "instructions": "`ctx``l` User: `who`. How much does it make them want to come back tomorrow?", "criteria": ["Not at all", "A little", "Quite a lot", "A lot"]}}
jobs = [(k, w) for k in L for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "l": L[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':12}" + "".join(f"{q:>8}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in L]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:12}" + "".join(f"{s[q]:8.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
