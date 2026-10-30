# Caption for the owner's hijab video (30 Oct 2026, #307): the pile-on, then "Hijab, everybody has an opinion…", the word in the Qur'an
# (7:46, 38:32, 19:17, 42:51), khimār for the covering (24:31), men lower your gaze first (24:30), the barrier, banned, a dua for our sisters.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/hijab_video_caption.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A Reel from Rafiq (an Arabic-learning account for Muslims). It opens on an animation: a woman shouts 'We need to ban the hijab!' and a crowd shouts "
       "'hijab' at a hijabi under a spotlight; then the presenter: 'Hijab, everybody has an opinion. But most people don't know: when the Qur'an tells women "
       "to cover it uses a different word (khimar, 24:31). The word hijab is in the Qur'an in a much bigger context': the barrier between Paradise and the "
       "Fire (7:46), the sun hiding behind the hijab (38:32), Maryam's screen (19:17), Allah speaking to Musa from behind a hijab (42:51); before the women, "
       "the men are told to lower their gaze (24:30), the first hijab; it's a covering, a protection, a barrier from evil; it's being banned left, right and "
       "centre; may Allah protect our sisters; the hijab will be a covering for you on the Day of Judgement. Every ayah on screen in Arabic and English.")
WHO = {"hijabi": "a 23-year-old UK hijabi", "brother": "a 28-year-old Muslim man", "curious": "a 30-year-old non-Muslim who's curious"}
T = "#hijab #islam #muslim #quran #learnarabic"
CAP = {"H1": f"Everyone has an opinion on the hijab… but do you know what the word actually means? 🤍 It's in the Qur'an, and not where you'd think. Which ayah surprised you? 👇 {T}",
       "H2": f"The Qur'an uses a different word when it tells women to cover 👀 So where does “hijab” come from? Watch to the end, and send this to a sister 🤍 {T}",
       "H3": f"Before Allah speaks to women about covering, He speaks to the men: lower your gaze (24:30) 🤍 The word hijab means so much more than a scarf. Did you know? 👇 {T}",
       "H4": f"To every sister being told to take it off: your hijab is a barrier, a protection, a covering 🤍 May Allah protect you. Share this with her 👇 {T}"}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "watch": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to watch to the end?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "trust": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How sincere and respectful does it feel (not clickbait or preachy)?", "criteria": ["No", "A bit", "Mostly", "Yes"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':6}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:6}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
