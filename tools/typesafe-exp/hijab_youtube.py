# YouTube Shorts title for the owner's hijab video, v1 full cut (31 Oct 2026, #307): which title gets the click and the watch-through.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/hijab_youtube.py
exec(open("tools/typesafe-exp/hijab_video_caption.py").read().split("WHO =")[0])
WHO = {"search": "a 23-year-old Muslim who searched 'hijab meaning in Quran' on YouTube", "hijabi": "a 23-year-old UK hijabi swiping YouTube Shorts",
       "curious": "a 30-year-old non-Muslim who's curious, swiping YouTube Shorts"}
CAP = {"meaning": "What Does Hijab ACTUALLY Mean in the Qur'an? 🤯 #shorts",
       "word": "The Qur'an Doesn't Use “Hijab” for the Headscarf 👀 #hijab",
       "ban": "They Want to Ban the Hijab… But Do They Know What It Means? #shorts",
       "places": "Hijab in the Qur'an Isn't What You Think: 4 Ayahs 📖 #hijab"}
Q = {"click": {"type": "score", "instructions": "`ctx` YouTube Shorts title: `h`. Viewer: `who`. How likely are they to stop and watch?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "watch": {"type": "score", "instructions": "`ctx` YouTube Shorts title: `h`. Viewer: `who`. How likely are they to watch to the end?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "trust": {"type": "score", "instructions": "`ctx` YouTube Shorts title: `h`. Viewer: `who`. How sincere and respectful does it feel (not clickbait or misleading)?", "criteria": ["No", "A bit", "Mostly", "Yes"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
