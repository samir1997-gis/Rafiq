# h1-algebra in a new format (owner, 27 Oct 2026: "more graphics, simpler script but more detailed… dynamic graphics showing what's being
# described"): the same story with al-Khwarizmi's own worked example drawn (x^2 + 10x = 39 by completing the square).
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/algebra_v2_script.py
# Result (27 Oct 2026; finish / clear / share, 2 viewers x 3): A 2.65 / 2.60 / 2.49.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 55-second Instagram/TikTok Reel from a small account teaching the Arabic Muslims use. Calm narrator, full-screen animated "
       "illustrations of each line (a bone cracking and being set, Baghdad, a square being completed, a word morphing). Script: ")
S = {
 "A": "Algebra is named after an Arabic word for setting broken bones. The word is al-jabr: putting broken pieces back together. About twelve "
      "hundred years ago, in Baghdad, a scholar called al-Khwarizmi wrote a book on solving problems this way. Here's his own example. A square, "
      "plus ten of its sides, makes thirty-nine. Split the ten into two fives, and put them on two sides. Now one corner is missing: five by five, "
      "twenty-five. Fill it in, and you've got a perfect square: thirty-nine plus twenty-five, sixty-four. Its side is eight. Take away the five, "
      "and the answer is three. When Europe translated his book into Latin, al-jabr became algebra. In Spain, a bone-setter was even called an "
      "algebrista. And his own name, al-Khwarizmi, became the word algorithm. Your turn. Between the two sujood, the Prophet, peace be upon him, "
      "asked: wajburni. What does it mean? And mend me. Set right whatever is broken in me. What do you say between the two sujood? Comment below!",
}
WHO = {"target": "a 24-year-old UK Muslim who hated maths at school", "learner": "a 30-year-old learning Arabic"}
Q = {"finish": {"type": "score", "instructions": "`ctx` `s` Viewer: `who`. How likely are they to watch to the end?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "clear": {"type": "score", "instructions": "`ctx` `s` Viewer: `who`. Is it simple to follow, including the maths part?", "criteria": ["Confusing", "A bit", "Mostly clear", "Clear"]},
     "share": {"type": "score", "instructions": "`ctx` `s` Viewer: `who`. How likely are they to share or save it?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]}}
if __name__ == "__main__":
    jobs = [(k, w) for k in S for w in WHO for _ in range(3)]
    with ThreadPoolExecutor(12) as ex: res = list(ex.map(lambda j: (j, ask({"ctx": CTX, "s": S[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
    for k in S:
        s = {q: sum(a[q]["score"] for (kk, _), a in res if kk == k) / 6 for q in Q}
        print(f"{k} finish {s['finish']:.2f}  clear {s['clear']:.2f}  share {s['share']:.2f}")
