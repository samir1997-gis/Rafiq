# Should Rafiq have a free tier? (owner, 10 Oct 2026) More sign-ups, and more people paying in the end?
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("Rafiq is a new web app teaching the Arabic of the Quran and the daily prayer, and everyday Arabic, to adult beginners (mostly UK Muslims, some non-Muslims), "
       "used on phones. Plans: Essentials £6.99/month or £49.99/year; Complete £11.99/month or £79.99/year (adds an AI conversation partner, unlimited answer checks, "
       "real-life scenes, weak-spots review). Its strongest hook is 'Your salah': the most-said words of the prayer, word by word. ")
O = {"A today: free week then pick a plan": "No card. 7 days of everything; then lessons ask for a plan, progress and streak stay visible.",
     "B free week, then free plan forever": "No card. 7 days of everything; then a free plan forever: 'Your salah' most-said words, one new lesson a day, and reviews of words learned. A plan unlocks all lessons and features.",
     "C free plan from day one, no trial": "No card. A free plan forever from day one (the 'Your salah' most-said words, one new lesson a day, reviews); upgrade any time.",
     "D generous free, pay for extras": "No card. Free forever for all lessons and reviews; only the AI conversation partner, real-life scenes and unlimited answer checks need a plan."}
WHO = {"masjid": "a UK Muslim parent who found Rafiq through the masjid WhatsApp group, careful with money and wary of subscriptions",
       "keen": "a motivated 28-year-old who wants to understand the Quran and would study daily",
       "student": "a 20-year-old university student with little money",
       "revert": "a 30-year-old revert learning to pray, who has tried free apps before",
       "reddit": "a non-Muslim on r/learn_arabic, sceptical of new apps and AI, comparing with free resources"}
Q = {"signup": {"type": "score", "instructions": "`ctx` Set-up: `o`. Person: `who`. How likely are they to create an account?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "pay1": {"type": "score", "instructions": "`ctx` Set-up: `o`. Person: `who`. How likely are they to pay within their first month?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "pay3": {"type": "score", "instructions": "`ctx` Set-up: `o`. Person: `who`. How likely are they to be paying 3 months from now?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "share": {"type": "score", "instructions": "`ctx` Set-up: `o`. Person: `who`. How likely are they to recommend it to friends or family?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]}}
jobs = [(k, w) for k in O for w in WHO]
with ThreadPoolExecutor(20) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "o": O[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':40}" + "".join(f"{q:>8}" for q in Q))
for k in O: print(f"{k:40}" + "".join(f"{sum(r[(k, w)][q]['score'] for w in WHO) / len(WHO):8.2f}" for q in Q))
print("\npaying in 3 months, by person:")
for k in O: print(f"  {k:40}" + "  ".join(f"{w} {r[(k, w)]['pay3']['score']}" for w in WHO))
