# Thumbnail headline for the long Aḥad video on YouTube (owner, 9 Nov 2026: "His only word… is boring and bland… make it emotionally
# triggering… give more context, like why a slave from Abyssinia said ahad"). The image: his serious face cut out on the left, the gold أَحَد
# over a boulder in the desert on the right; the headline sits above the Arabic. Which line gets the click, and is fair to the video?
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A YouTube thumbnail for a 3.5-minute video from Rafiq, a small account teaching the Arabic Muslims use. Image: the presenter's serious face "
       "cut out on the left; the Arabic word ahad huge in gold over a desert scene with a boulder. The video tells how Bilal, a black slave from Abyssinia, "
       "was laid on burning sand in Makkah with a boulder on his chest and told to deny Muhammad and worship idols, and answered with one word, ahad; "
       "why ahad and not wahid; how it is the whole of tawhid; his freedom, the adhan on the Ka'bah, his footsteps in Jannah.")
WHO = {"scroller": "a 22-year-old UK Muslim browsing YouTube", "seerah": "a 30-year-old who loves seerah stories", "learner": "a 34-year-old learning Arabic"}
CAP = {"crushed": "THEY CRUSHED HIS CHEST. HE SAID ONE WORD.", "tortured": "TORTURED TO SAY 2 WORDS. HE SAID 1.",
       "slave": "WHY A TORTURED SLAVE KEPT SAYING THIS", "couldnt": "THE WORD THEY COULDN'T CRUSH OUT OF HIM",
       "boulder": "A BOULDER ON HIS CHEST. HE SAID THIS.", "only": "HIS ONLY WORD"}
Q = {"click": {"type": "score", "instructions": "`ctx` Thumbnail headline: `h`. Viewer: `who`. How likely are they to click the video?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "curious": {"type": "score", "instructions": "`ctx` Thumbnail headline: `h`. Viewer: `who`. How strongly does it make them want to know the story?", "criteria": ["Not at all", "A little", "Quite", "Very"]},
     "fair": {"type": "score", "instructions": "`ctx` Thumbnail headline: `h`. Is it true to the video, respectful of the story, not misleading clickbait?", "criteria": ["No", "Partly", "Mostly", "Fully"]}}
jobs = [(k, w) for k in CAP for w in WHO for _ in range(2)]
with ThreadPoolExecutor(24) as ex: res = list(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(a[q]["score"] for (kk, _), a in res if kk == k) / 6 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}   {CAP[k]}")
