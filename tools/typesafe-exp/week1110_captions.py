# The 15 captions for 10–16 Nov 2026 (#355), from brag-quiz/schedule/2026-11-10.json: each scored as it stands (one caption a post).
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/week1110_captions.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
import json
P = json.load(open("brag-quiz/schedule/2026-11-10.json"))
WHO = {"scroller": "a 21-year-old UK Muslim", "learner": "a 32-year-old learning Arabic", "parent": "a 40-year-old UK Muslim parent"}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "follow": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to follow the account?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]}}
jobs = [(k, w) for k in range(len(P)) for w in WHO]
ctx = lambda p: f"A TikTok post from Rafiq, a small account teaching the Arabic Muslims use: {p['kind']}, {p['what']}."
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": ctx(P[j[0]]), "h": P[j[0]]["caption"], "who": WHO[j[1]]}, Q)["answers"]), jobs))
for k, p in enumerate(P): print(f"{p['id']:12}" + "".join(f"{sum(r[(k, w)][q]['score'] for w in WHO) / 3:9.2f}" for q in Q))
