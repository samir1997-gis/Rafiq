# Founder video (17 Nov 2026, #393, #386): which opening line makes a visitor on the landing page keep watching and tap "Start lesson 1"?
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 25-second video of the founder of Rafiq talking to camera, on Rafiq's landing page, above the button to start a free first lesson. "
       "Rafiq is a small app that teaches Muslims the Arabic of their salah and the Qur'an, word by word, in short daily lessons. "
       "After the opening line he says why he built it and that the first lesson takes two minutes and is free.")
WHO = {"revert": "a 27-year-old revert who prays but doesn't understand the Arabic", "born": "a 35-year-old born Muslim who learnt to read Qur'an as a child without the meaning",
       "parent": "a 40-year-old Muslim dad who has tried Arabic apps before and given up"}
H = {"years": "I prayed for years without understanding a single word I was saying.",
     "every": "Every day, five times a day, I was saying words I didn't understand.",
     "question": "Do you know what you're actually saying in your salah?",
     "khushu": "I wanted khushūʿ in my salah, and I realised I couldn't have it without knowing what I was saying.",
     "rukuh": "Subḥāna rabbiya l-ʿaẓīm. I said it thousands of times before I knew what it meant."}
Q = {"watch": {"type": "score", "instructions": "`ctx` The opening line: `h`. Viewer: `who`. How likely are they to keep watching past the first line?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "trust": {"type": "score", "instructions": "`ctx` The opening line: `h`. Viewer: `who`. Does the founder come across as sincere and someone like them?", "criteria": ["No", "Partly", "Mostly", "Fully"]},
     "act": {"type": "score", "instructions": "`ctx` The opening line: `h`. Viewer: `who`. How likely are they to tap to start the free first lesson by the end?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]}}
jobs = [(k, w) for k in H for w in WHO]
with ThreadPoolExecutor(15) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": H[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in H]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
