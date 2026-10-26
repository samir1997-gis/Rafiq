# The chalkboard ad (owner, 26 Oct 2026): how Rafiq makes studying Arabic easy and how soon you improve, chalk drawn on a board as
# Callum explains. Claims kept to what the site and app state: 5-10 minutes a day; week one = the 20 words you say most in salah
# (over half of a four-rak'ah prayer before the surah, salah-data.js); every word of the salah + 10 short surahs; 785 words,
# 36 conversations, 12 units; reviews just before you'd forget; 7 days free, no card.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/chalkboard_ad.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
# Result (26 Oct 2026; stop / trust, 2 viewers x 3): ten 2.20 / 2.19 (chosen) · never 2.20 / 2.01 · years 2.27 / 1.68 · half 2.45 / 1.20 (reads as an exaggerated claim).
CTX = ("The first 3 seconds of a 35-second Instagram/TikTok ad for Rafiq, an app that teaches the Arabic of your salah: chalk writing "
       "appears on a blackboard as a narrator speaks (the first word shouted). The ad goes on to say 10 minutes a day, week one = the 20 "
       "words you say most in salah (over half of a four-rak'ah prayer), reviews before you forget, 7 days free. Hook: ")
H = {
 "years": "YEARS. That's how long most people think it takes to understand Arabic.",
 "half": "HALF of your salah. That's how much you'll understand after one week.",
 "ten": "TEN minutes a day. That's all it takes to start understanding your salah.",
 "never": "NOBODY tells you this about learning Arabic: you don't start with grammar.",
}
WHO = {"target": "a 24-year-old UK Muslim who prays but doesn't understand the Arabic", "quit": "a 33-year-old who started Arabic twice and quit"}
Q = {"stop": {"type": "score", "instructions": "`ctx` `h` Viewer: `who`. How likely are they to keep watching past 3 seconds?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "trust": {"type": "score", "instructions": "`ctx` `h` Viewer: `who`. Does it sound believable rather than an exaggerated ad claim?", "criteria": ["Exaggerated", "A bit", "Mostly believable", "Believable"]}}
if __name__ == "__main__":
    jobs = [(k, w) for k in H for w in WHO for _ in range(3)]
    with ThreadPoolExecutor(20) as ex: res = list(ex.map(lambda j: (j, ask({"ctx": CTX, "h": H[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
    for k in sorted(H, key=lambda k: -sum(a[q]["score"] for (kk, _), a in res if kk == k for q in Q)):
        s = {q: sum(a[q]["score"] for (kk, _), a in res if kk == k) / 6 for q in Q}
        print(f"{k:6} stop {s['stop']:.2f}  trust {s['trust']:.2f}  total {sum(s.values()):.2f}")
