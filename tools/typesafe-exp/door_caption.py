# Caption for the door reel (brag-quiz/out/door/door.mp4, #291), posted as a trial reel (non-followers first): the caption starts a
# conversation, the video's end card carries the sign-up.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/door_caption.py
# Result (25 Oct 2026; comment / share / trust, 2 viewers x 3): D3 2.10 / 2.06 / 1.09 (chosen) · D1 2.07 / 2.12 / 0.94 · D2 2.13 / 2.02 / 0.84.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("An Instagram/TikTok Reel from a small account teaching the Arabic of salah: 8 s of a gold key flying at a keyhole with a FRAMES "
       "TO UNLOCK counter; it never arrives. A calm narrator: 'You just watched a key for seven seconds, a key that doesn't exist, and you're "
       "still here, waiting for it to turn.' Then a giant arched door with a tiny person scratching at its foot: 'Every salah, every ayah, "
       "you've only scratched the surface, never knowing how deep it goes. You can open it if you're ready: it's as simple as learning the "
       "language it speaks, Arabic.' The key turns, the door opens onto light. Ends: 'tell me in the comments: what's the first thing you'd "
       "want to understand?' Caption under it: ")
C = {
 "D1": "Be honest, you waited for it to turn 😅 What's the first thing you'd want to understand: your salah, the Qur'an, or your du'a? 👇 Send this to someone still scratching at the door 🤍 #learnarabic #arabic #salah #quran #muslim",
 "D2": "You've prayed thousands of times. How much of it have you actually understood? 🤍 The door's been there the whole time. What would you want to understand first? 👇 #learnarabic #salah #arabic #quran #muslim",
 "D3": "7 seconds on a key that doesn't exist… imagine giving that to the words you say 17 times a day 🗝️ What would you understand first? 👇 #learnarabic #arabic #salah #muslim #islam",
}
WHO = {"target": "a 27-year-old UK Muslim who prays but doesn't understand the Arabic", "revert": "a 31-year-old revert learning Arabic"}
Q = {"comment": {"type": "score", "instructions": "`ctx` `c` Viewer: `who` (doesn't follow the account). How likely are they to comment?",
                 "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "share": {"type": "score", "instructions": "`ctx` `c` Viewer: `who` (doesn't follow the account). How likely are they to send it to someone or save it?",
               "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "trust": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. Does the caption feel genuine rather than an ad or clickbait?",
               "criteria": ["Ad / clickbait", "A bit", "Mostly genuine", "Genuine"]}}
if __name__ == "__main__":
    jobs = [(k, w) for k in C for w in WHO for _ in range(3)]
    with ThreadPoolExecutor(18) as ex: res = list(ex.map(lambda j: (j, ask({"ctx": CTX, "c": C[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
    for k in C:
        s = {q: sum(a[q]["score"] for (kk, _), a in res if kk == k) / 6 for q in Q}
        print(f"{k} comment {s['comment']:.2f}  share {s['share']:.2f}  trust {s['trust']:.2f}  total {sum(s.values()):.2f}")
