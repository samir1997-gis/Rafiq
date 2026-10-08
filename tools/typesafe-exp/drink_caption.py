# Caption for the أَشْرَبُ verb quiz video (v3-drink): "I drink" → "we drink"? then "I drank" → "we drank"? A pure-content post (no link).
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 24-second Arabic verb quiz reel: 'If أَشْرَبُ is \"I drink\", what's \"we drink\"?' with 3 options and a countdown, the answer نَشْرَبُ "
       "and the rule (أَ → نَ); then 'If شَرِبْتُ is \"I drank\", what's \"we drank\"?' answer شَرِبْنا (ـتُ → ـنا). Ends: 'Spot the pattern once, use it on every verb'.")
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun", "learner": "a 34-year-old who has tried to learn Arabic before and given up", "revert": "a 30-year-old revert learning to pray"}
CAP = {"A": "If أَشْرَبُ is “I drink”… what's “we drink”? 🤔 Then try the past tense 👀 Comment your answer before the reveal 👇 Follow for a new Arabic quiz every week. #learnarabic #arabic #arabicverbs #studyarabic #muslim",
       "B": "One letter turns “I drink” into “we drink” in Arabic. Can you spot it? 👇 Send this to someone learning Arabic 📩 #learnarabic #arabic #arabicverbs #studyarabic #muslim",
       "C": "Arabic verb quiz ☕ أَشْرَبُ = I drink. So what's “we drink”? And “we drank”? Pause and drop your answers below 👇 Spot the pattern once, use it on every verb. #learnarabic #arabic #arabicverbs #studyarabic #muslim"}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "follow": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to follow the account?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "clear": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How clear and inviting is the caption?", "criteria": ["Confusing", "Unclear", "Clear", "Very clear and inviting"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
