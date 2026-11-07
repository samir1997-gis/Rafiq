# Spoken hook for g7-we (owner, 7 Nov 2026: "another concept… like turning something from I to we"): teach يَأْكُلُ he eats →
# آكُلُ I eat → نَأْكُلُ we eat (nūn at the front), then quiz on the two verbs of al-Fātiḥah: يَعْبُدُ he worships → we worship? (نَعْبُدُ),
# يَسْتَعِينُ he seeks help → we seek help? (نَسْتَعِينُ). Callum's voice, the first word shouted and slammed on (FORMATS.md, the g4 standard).
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("The first line, shouted word first and on screen from frame 0, of a 45-second Instagram reel from a small account teaching the Arabic "
       "Muslims use. The reel teaches that one letter at the front of an Arabic verb says who is doing it: yakulu 'he eats', aakulu 'I eat' "
       "(alif at the front), nakulu 'we eat' (nun at the front); then quizzes the viewer on the two verbs of al-Fatihah: ya'budu 'he worships': "
       "what's 'we worship'? (na'budu), yasta'inu 'he seeks help': what's 'we seek help'? (nasta'in), with a 3-2-1 countdown each; the answers "
       "are the words of iyyaka na'budu wa iyyaka nasta'in, said in every rak'ah; it asks how many they got.")
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun", "learner": "a 34-year-old who has tried to learn Arabic before and given up", "revert": "a 30-year-old revert"}
CAP = {"most": "MOST people learn Arabic for years before they notice this trick!",
       "every": "EVERY rak'ah, you say 'we' twice without knowing it!",
       "one": "ONE letter turns 'I' into 'WE' in Arabic!",
       "seventeen": "SEVENTEEN times a day you say this letter in al-Fātiḥah!"}
Q = {"stop": {"type": "score", "instructions": "`ctx` Opening line: `h`. Viewer: `who`. How likely are they to keep watching past the first 3 seconds?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "clear": {"type": "score", "instructions": "`ctx` Opening line: `h`. Viewer: `who`. Is it clear and intriguing rather than confusing?", "criteria": ["Confusing", "A bit unclear", "Clear", "Clear and intriguing"]},
     "fair": {"type": "score", "instructions": "`ctx` Opening line: `h`. Does the video pay off this line fairly, without overclaiming?", "criteria": ["Misleading", "Partly", "Mostly", "Fully"]}}
jobs = [(k, w) for k in CAP for w in WHO for _ in range(2)]
with ThreadPoolExecutor(24) as ex: res = list(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(a[q]["score"] for (kk, _), a in res if kk == k) / 6 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
