# h2-coffee in the new format (owner, 27 Oct 2026, #300: "do the same for the h2 coffee" as h1-algebra #298): a simpler script with more
# detail, every line drawn (the cup turning into a wine glass, the dictionary, Yemen at night, the route on a map, the ship).
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/coffee_v2_script.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 50-second Instagram/TikTok Reel from a small account teaching the Arabic Muslims use. Calm narrator, full-screen animated "
       "illustrations of each line (a coffee cup turning into a wine glass, an old dictionary, Yemen at night, a route drawn on a map, a ship). Script: ")
TAIL = ("Your turn. A masjid is the place of sujood. So what's this? Maqha. A coffee pot, a cafe, or a coffee bean? 3, 2, 1. A cafe! "
        "The place of qahwa. So every coffee you order is a little bit of Arabic. How do you take yours? Comment below!")
S = {
 "A": "The Arabic word for coffee used to mean... wine. Qahwa. Old Arabic dictionaries say it meant wine because it takes away your appetite. "
      "Then, in the fourteen-hundreds, Sufis in Yemen drank a dark brew made from coffee beans, to stay awake for their night prayers. And they "
      "gave it the old name: qahwa. From Yemen it travelled to Makkah and Cairo, then to Istanbul, where it became kahve. Ships carried it to "
      "Europe. The Dutch said koffie, and by 1582, English had a new word: coffee. " + TAIL,
 "B": "The Arabic word for coffee used to mean... wine. Qahwa. Old Arabic dictionaries say it meant wine because it takes away your appetite. "
      "In the fourteen-hundreds, Sufis in Yemen drank coffee to stay awake for their night prayers, and called it qahwa. It travelled to Makkah, "
      "Cairo and Istanbul, where it became kahve. The Dutch said koffie, and by 1582, English had: coffee. " + TAIL,
}
WHO = {"target": "a 24-year-old UK Muslim who drinks coffee every day", "learner": "a 30-year-old learning Arabic"}
Q = {"finish": {"type": "score", "instructions": "`ctx` `s` Viewer: `who`. How likely are they to watch to the end?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "clear": {"type": "score", "instructions": "`ctx` `s` Viewer: `who`. Is it simple to follow?", "criteria": ["Confusing", "A bit", "Mostly clear", "Clear"]},
     "share": {"type": "score", "instructions": "`ctx` `s` Viewer: `who`. How likely are they to share or save it?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]}}
if __name__ == "__main__":
    jobs = [(k, w) for k in S for w in WHO for _ in range(3)]
    with ThreadPoolExecutor(12) as ex: res = list(ex.map(lambda j: (j, ask({"ctx": CTX, "s": S[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
    for k in S:
        s = {q: sum(a[q]["score"] for (kk, _), a in res if kk == k) / 6 for q in Q}
        print(f"{k} finish {s['finish']:.2f}  clear {s['clear']:.2f}  share {s['share']:.2f}")
