# Ask Rafiq's permission screen (Apple 5.1.2(i), #351): clear, honest, and does it put people off asking?
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A one-time screen in Rafiq, an app teaching the Arabic Muslims use, shown before a learner's first question to Ask Rafiq, its AI tutor. "
       "Apple requires apps to ask permission before sending personal data to a third-party AI.")
WHO = {"new": "a 26-year-old UK Muslim learner", "wary": "a 45-year-old learner wary of AI and data", "parent": "a 38-year-old parent"}
CAP = {"now": "Before you ask. Ask Rafiq's answers are written by Claude, an AI made by Anthropic. To answer, your question is sent to Anthropic, with what Rafiq needs to fit the answer to you: your current unit's words, the kinds of mistakes you often make and, for Why?, what's on your screen. Your name and email are never sent, and Anthropic doesn't use any of it to train its AI. More in our Privacy policy. [Not now] [OK, ask Rafiq]"}
Q = {"clear": {"type": "score", "instructions": "`ctx` Screen: `h`. Viewer: `who`. Do they understand what is shared and with whom?", "criteria": ["No", "Partly", "Mostly", "Fully"]},
     "trust": {"type": "score", "instructions": "`ctx` Screen: `h`. Viewer: `who`. Does it feel honest and reassuring?", "criteria": ["No", "A little", "Yes", "Very"]},
     "go": {"type": "score", "instructions": "`ctx` Screen: `h`. Viewer: `who`. How likely are they to tap OK and ask?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(6) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
for w in WHO: print(w, {q: r[("now", w)][q]["score"] for q in Q})
