# v2: neutral greeting (some learners are not Muslim). Thank-you + feedback email to new users who have been studying regularly. Conditional vs up-front gift of 2 extra weeks.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A personal email from the founder of Rafiq (a small new web app that teaches the Arabic of the Quran and the daily prayer, "
       "with a free week, then a paid plan) to someone who signed up in the last week and has studied on several days. Email: ")
WHO = {"student": "a 24-year-old UK Muslim student who has used the app on 4 days this week",
       "nonmuslim": "a 29-year-old non-Muslim learning Arabic for travel and work, used it on 4 days",
       "parent": "a 38-year-old working mum learning Arabic for her prayer, used it on 3 days",
       "revert": "a 30-year-old revert who uses it most days"}
BASE = ("Subject: A quick thank you from Rafiq\n\nHi {name},\n\nI'm {founder}, and I made Rafiq. I noticed you've been coming back to practise "
        "this week, and I just wanted to say thank you. It genuinely means a lot this early on.\n\nCould I ask a small favour? Just hit reply and tell me how you're "
        "finding it: what you like, what's confusing, anything you wish it did. Even one line helps.\n\n{gift}\n\nThanks again,\n{founder}")
CAP = {"if-feedback": BASE.replace("{gift}", "As a thank you, if you send me your thoughts, I'll add two extra weeks of Rafiq Complete to your account, free."),
       "up-front": BASE.replace("{gift}", "And as a thank you for being one of our first learners, I've already added two extra weeks of Rafiq Complete to your account, free. No strings attached."),
}
Q = {"reply": {"type": "score", "instructions": "`ctx` `h` Reader: `who`. How likely are they to reply with feedback?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "genuine": {"type": "score", "instructions": "`ctx` `h` Reader: `who`. How personal and genuine does it feel (not like marketing)?", "criteria": ["Pure marketing", "Mostly marketing", "Mostly personal", "Very personal and genuine"]},
     "goodwill": {"type": "score", "instructions": "`ctx` `h` Reader: `who`. How much warmer do they feel towards Rafiq after reading it?", "criteria": ["Colder", "No change", "A bit warmer", "Much warmer"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':12}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / len(WHO) for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:12}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
