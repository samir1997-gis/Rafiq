# Hooks for "the tomorrow people" (owner's idea, 25 Oct 2026): a talking-head video, people who always say "I'll start tomorrow"
# (learning Arabic, praying, quitting smoking); the grave is full of them; after the Dajjal or the sun rising from the west it's too
# late (Muslim 158); the Arabic word for it, at-taswīf, from sawfa ("I will, later"). Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/tomorrow_hooks.py
# Result (25 Oct 2026; stop / feel, 2 viewers x 3): you 2.06 / 1.87 · word 2.10 / 1.67 · people 1.91 / 1.44 · grave 2.05 / 1.05 · late 1.77 / 0.99.
# The "too late" hooks stop people but read as fear-mongering on their own; they work as the turn in the middle, not the opener.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("The first 3 seconds of a talking-head Instagram/TikTok Reel by a young British Muslim (spoken and on screen). The video is about "
       "people who always say 'I'll start tomorrow' (praying, learning Arabic, quitting) and how tomorrow isn't promised. Hook: ")
H = {
 "people": "There's a group of people who will still be saying 'I'll start tomorrow' when the sun rises from the west.",
 "late": "The sun has just risen from the west. It's too late. And someone is still saying 'I'll start tomorrow'.",
 "grave": "The graveyard is full of people who said 'I'll start tomorrow'.",
 "word": "There's an Arabic word for people who always say 'I'll start tomorrow', and the Qur'an warns about it.",
 "you": "If you've said 'I'll start tomorrow' this week, you're one of the tomorrow people.",
}
WHO = {"target": "a 24-year-old UK Muslim who prays on and off", "learner": "a 30-year-old who keeps meaning to learn Arabic"}
Q = {"stop": {"type": "score", "instructions": "`ctx` `h` Viewer: `who` (doesn't follow the account). How likely are they to keep watching past 3 seconds?",
              "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "feel": {"type": "score", "instructions": "`ctx` `h` Viewer: `who`. Does it feel sincere and motivating rather than preachy or fear-mongering?",
              "criteria": ["Preachy", "A bit", "Mostly sincere", "Sincere and motivating"]}}
if __name__ == "__main__":
    jobs = [(k, w) for k in H for w in WHO for _ in range(3)]
    with ThreadPoolExecutor(20) as ex: res = list(ex.map(lambda j: (j, ask({"ctx": CTX, "h": H[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
    for k in sorted(H, key=lambda k: -sum(a[q]["score"] for (kk, _), a in res if kk == k for q in Q)):
        s = {q: sum(a[q]["score"] for (kk, _), a in res if kk == k) / 6 for q in Q}
        print(f"{k:7} stop {s['stop']:.2f}  feel {s['feel']:.2f}  total {sum(s.values()):.2f}")
