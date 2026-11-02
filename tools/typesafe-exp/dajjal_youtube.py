# YouTube Shorts title for the owner's Dajjāl video (2 Nov 2026, #316): which title gets the click and the watch-through.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/dajjal_youtube.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 2-minute talking-head Reel from Rafiq (an Arabic-learning account for Muslims), a young British Muslim on his sofa. It opens with several "
       "copies of him in the room: 'Did you know there's more than one Dajjāl?' The word comes from d-j-l, to coat or cover: the Arabs used it for "
       "coating a sick camel in tar to hide what was underneath, and for painting gold over something cheap. A dajjāl is a master liar, a manipulator, "
       "so there could be hundreds among us; the Prophet ﷺ said about thirty would come claiming prophethood; the greatest is al-Masīḥ ad-Dajjāl, whose "
       "Paradise is the Fire; kāfir is written between his eyes and every believer will read it, even one who can't read: it's about faith; the first "
       "ten ayahs of al-Kahf protect you. Ends: send this to someone. ")
WHO = {"young": "a 21-year-old UK Muslim who scrolls a lot", "practising": "a 30-year-old practising Muslim", "parent": "a 42-year-old Muslim parent"}
CAP = {"more": "There’s More Than One Dajjāl 👀 #shorts",
       "thirty": "The Prophet ﷺ Warned of 30 Dajjāls #shorts",
       "means": "What “Dajjāl” Actually Means in Arabic #shorts",
       "met": "Have You Met a Dajjāl? (The Word Explained) #shorts"}
Q = {"click": {"type": "score", "instructions": "`ctx` YouTube Shorts title: `h`. Viewer: `who`. How likely are they to stop and watch?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "watch": {"type": "score", "instructions": "`ctx` YouTube Shorts title: `h`. Viewer: `who`. How likely are they to watch to the end?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "trust": {"type": "score", "instructions": "`ctx` YouTube Shorts title: `h`. Viewer: `who`. How sincere and respectful does it feel (not clickbait or misleading)?", "criteria": ["No", "A bit", "Mostly", "Yes"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':8}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:8}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
