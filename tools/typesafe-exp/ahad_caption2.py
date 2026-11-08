# Captions for the Aḥad videos (7 Nov 2026, #315; 8 Nov: a new set for the re-cut that opens on "deny Muḥammad"): Bilāl under the rock saying "aḥad", why that word, and why it is tawḥīd.
# Two endings: "comment SALAH for a starter pack" (the 90 s and 60 s footsteps versions) and "sign up" (the full and the 60 s deny versions).
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/ahad_caption.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
STORY = ("A Reel from Rafiq, a small account teaching the Arabic Muslims use, a young man talking to camera with motion graphics: Bilāl, a slave in Makkah, "
         "is laid on burning sand with a boulder on his chest and told to deny Muḥammad ﷺ and worship al-Lāt and al-ʿUzzā. His one word in reply: aḥad. "
         "Why aḥad and not wāḥid: wāḥid is a number (one, then two), aḥad is the One with no second, the word that leaves no room for any partner; it is "
         "the whole of tawḥīd in one word, the very thing they wanted him to deny. ")
CTX = {"comment": STORY + "It ends: if you want to learn the words you say in your salah, comment SALAH and I'll send you a starter pack.",
       "signup": STORY + "It ends: if you want to learn the words you say in your salah, sign up to rafiq-arabic.com."}
WHO = {"student": "a 20-year-old UK Muslim student", "learner": "a 32-year-old learning Arabic", "scroller": "a 24-year-old UK Muslim scrolling at night"}
T = "#bilal #seerah #tawhid #learnarabic #islam"
CAP = {"comment": {
    "deny": f"They told him: deny Muḥammad ﷺ. He had a boulder on his chest and one word in reply 🪨☝️ Do you know what it means? Comment SALAH for the starter pack 👇 {T}",
    "word": f"Not wāḥid. Aḥad. One letter of difference, and it's the whole of tawḥīd ☝️ Comment SALAH and I'll send you the starter pack 👇 {T}",
    "you": f"You say this word every time you read al-Ikhlāṣ. Bilāl said it with a boulder on his chest 🤍 Comment SALAH for the starter pack 👇 {T}"}}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "follow": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to follow the account?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "trust": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How much do they trust the account after reading it?", "criteria": ["Not at all", "A little", "Quite a lot", "Completely"]}}
for end in CAP:  # (comment ending only)
    jobs = [(k, w) for k in CAP[end] for w in WHO]
    with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX[end], "h": CAP[end][j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
    print(f"\n{end:10}" + "".join(f"{q:>9}" for q in Q) + "   total")
    rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP[end]]
    for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
