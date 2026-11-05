# The landing page's Ask Rafiq section (#154, #210): which headline makes a visitor want the AI tutor, and trust it?
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A section on the home page of Rafiq, an app teaching the Arabic Muslims use. Under the headline: 'Ask anything about Arabic or your lessons, "
       "any time, and get a clear answer built on Rafiq's teacher-checked course. Got a question wrong? Tap Why? and Rafiq explains exactly what happened.' "
       "Next to it, a sample chat about hadha / hadhihi. It's part of the Complete plan.")
WHO = {"new": "a 26-year-old UK Muslim who has never studied Arabic", "stuck": "a 35-year-old who gave up on Arabic before because no one could answer their questions", "parent": "a 40-year-old parent"}
CAP = {"stuck": "Stuck? Just ask.", "tutor": "Your own Arabic tutor, any time", "why": "Never wonder “why?” again", "ask": "Ask Rafiq anything about Arabic"}
Q = {"want": {"type": "score", "instructions": "`ctx` Headline: `h`. Viewer: `who`. How much does it make them want to try it?", "criteria": ["Not at all", "A little", "Yes", "Very much"]},
     "trust": {"type": "score", "instructions": "`ctx` Headline: `h`. Viewer: `who`. Does it feel honest, not overpromising?", "criteria": ["No", "Partly", "Mostly", "Yes"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':8}" + "".join(f"{q:>8}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:8}" + "".join(f"{s[q]:8.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
