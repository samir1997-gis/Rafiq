# The faster start (#348): is the first lesson's and the tour's wording clear and encouraging for a brand-new learner?
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("Rafiq is an app teaching the Arabic Muslims use. Straight after confirming their email, a new learner does a 2-minute first lesson "
       "(say hello: as-salamu alaykum; 'my name': ismi; their own name in Arabic; build 'as-salamu alaykum, ismi <name>' from tiles), sees "
       "'Well done', answers two questions, then gets a tour of the app they can skip at every step.")
WHO = {"new": "a 26-year-old UK Muslim who has never studied Arabic", "busy": "a 41-year-old busy parent with 10 minutes a day", "revert": "a 30-year-old revert"}
CAP = {"well": "Well done, Samir! You just introduced yourself in Arabic. 2 new words in your reviews. 1 step done today.",
       "well2": "Well done, Samir! You just introduced yourself in Arabic. You've learnt 2 words: we'll bring them back so they stick. That's your first lesson done today ✅",
       "well3": "Well done, Samir! You just introduced yourself in Arabic: your first 2 Arabic words, learnt. We'll remind you of them so they stick.",
       "tour1": "Welcome to Rafiq, Samir 👋 Here's a quick look around. If you just want your 5 to 10 minutes a day, the next few stops are all you need.",
       "tour2": "Welcome to Rafiq, Samir 👋 A quick tour: 6 stops, about a minute. They show you everything you need for your 5 to 10 minutes a day.",
       "tour3": "Welcome to Rafiq, Samir 👋 Let's show you around in under a minute: just what you need for your daily 5 to 10 minutes. You can skip any time."}
Q = {"clear": {"type": "score", "instructions": "`ctx` Screen text: `h`. Viewer: `who`. Is it clear what it means and what to do?", "criteria": ["Confusing", "A bit unclear", "Clear", "Very clear"]},
     "warm": {"type": "score", "instructions": "`ctx` Screen text: `h`. Viewer: `who`. Does it feel encouraging and make them want to carry on?", "criteria": ["No", "A little", "Yes", "Very much"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(15) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':8}" + "".join(f"{q:>8}" for q in Q))
for k in CAP: print(f"{k:8}" + "".join(f"{sum(r[(k, w)][q]['score'] for w in WHO) / 3:8.2f}" for q in Q))
