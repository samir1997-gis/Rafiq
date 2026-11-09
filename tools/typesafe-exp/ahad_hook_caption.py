# Caption for the Aḥad video with the owner's hook stitched on the front (9 Nov 2026): "Do not pray another salah until you know this fact",
# then Bilāl under the boulder saying aḥad, why aḥad not wāḥid, al-Ikhlāṣ, tawḥīd. Owner: "make it relevant to the hook".
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A Reel from Rafiq, a small account teaching the Arabic Muslims use. It opens with the presenter: 'Do not pray another salah until you know this fact.' "
       "Then the story: Bilal, a slave in Makkah, a boulder on his chest, told to deny Muhammad, answers with one word, ahad; why ahad and not wahid; "
       "the word that opens and closes Surat al-Ikhlas; the whole of tawhid in one word. Ends: comment SALAH for a starter pack.")
WHO = {"scroller": "a 22-year-old UK Muslim scrolling", "learner": "a 34-year-old learning Arabic", "seerah": "a 30-year-old who loves seerah stories"}
T = "#bilal #tawhid #surahikhlas #learnarabic #islam"
CAP = {"ikhlas": f"Don't recite Sūrat al-Ikhlāṣ in your next salah until you know what aḥad really means ☝️ Bilāl said it with a boulder on his chest. Comment SALAH for the starter pack 👇 {T}",
       "pray": f"Before your next salah: the word you say in al-Ikhlāṣ is the same word Bilāl said under a boulder ☝️ Here's why it's so powerful. Comment SALAH 👇 {T}",
       "fact": f"The fact: aḥad is not just 'one' ☝️ It's the word Bilāl held on to under a boulder, and you say it in al-Ikhlāṣ. Comment SALAH for the starter pack 👇 {T}"}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "follow": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to follow the account?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "fair": {"type": "score", "instructions": "`ctx` Caption: `h`. Does the caption avoid giving the quiz answers away and avoid overclaiming?", "criteria": ["No", "Partly", "Mostly", "Fully"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
