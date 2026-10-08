# Full script check for the rising-from-ruku reel (brag-quiz/reels/samia/SCRIPT.md), both endings.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
body = open("brag-quiz/reels/samia/SCRIPT.md").read().split("**7. Ending")[0]
CTX = "A 45-second Instagram reel script by a Muslim who teaches the Arabic of the prayer. Script: " + body
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun", "learner": "a 34-year-old who has tried to learn Arabic before and given up", "revert": "a 30-year-old revert learning to pray"}
CAP = {"A content": "So next time you rise from ruku, you'll know exactly what you're saying. Follow for more of the words you say in salah.",
       "B app": "Rafiq teaches you every word you say in salah. Free week, link in bio."}
Q = {"watch": {"type": "score", "instructions": "`ctx` Ending: `h`. Viewer: `who`. How likely are they to watch to the end?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "respect": {"type": "score", "instructions": "`ctx` Ending: `h`. Viewer: `who`. How respectful and sincere does it feel?", "criteria": ["Disrespectful", "A bit flippant", "Respectful", "Very respectful and sincere"]},
     "follow": {"type": "score", "instructions": "`ctx` Ending: `h`. Viewer: `who`. How likely are they to follow, save or share?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "clear": {"type": "score", "instructions": "`ctx` Ending: `h`. Viewer: `who`. How clear is the explanation?", "criteria": ["Confusing", "Unclear", "Clear", "Very clear"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q))
for k in CAP: print(f"{k:10}" + "".join(f"{sum(r[(k, w)][q]['score'] for w in WHO) / 3:9.2f}" for q in Q))
