# Script for the door reel (owner, 24 Oct 2026): the @motiontheory "bullet that doesn't exist" format with a key flying at a keyhole,
# then a giant arched door with a tiny person scratching at its foot; the key finally turns on "Arabic". Narrator: Brian.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/door_script.py
# Result (24 Oct 2026; finish / comment / clear, 2 viewers x 3): A 2.42 / 2.48 / 2.71 (chosen) · B 2.39 / 2.50 / 2.69.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("An Instagram/TikTok Reel from a small account teaching the Arabic of salah. 0-8 s: no voice, a gold key flies at a keyhole, a "
       "FRAMES TO UNLOCK counter falls from 204 to 006, it never arrives. Then a calm narrator (with a soft chuckle) says this script while the "
       "camera pulls back to a giant arched door with a tiny person scratching at its foot; at the end the key turns and the door opens onto "
       "light. Script: ")
S = {
 "A": ["You just watched a key for seven seconds... a key that doesn't exist.", "And you're still here... waiting for it to turn.",
       "So if you can watch that for seven seconds... you can watch this for another fifteen.",
       "This is you. At the foot of a door you've been scratching at your whole life.",
       "You hear it in every salah. Every ayah. But you've only ever scratched the surface... never knowing how deep it goes.",
       "You can open it, if you're ready. And it's as simple as learning the language it speaks: Arabic.",
       "Start today at RafiqArabic.com... and tell me in the comments: what's the first thing you'd want to understand?"],
 "B": ["You just watched a key for seven seconds... a key that doesn't exist.", "And you're still here... waiting for it to turn.",
       "So if you can watch that for seven seconds... you can watch this for another fifteen.",
       "This is you. Scratching at the surface of a door your whole life.",
       "Every salah you've prayed. Every ayah you've heard. It's all behind this door... and you never knew how deep it goes.",
       "You can open it, if you're ready. It's as simple as learning Arabic.",
       "Start today at RafiqArabic.com... and tell me in the comments: which part of your salah do you want to understand first?"],
}
WHO = {"target": "a 27-year-old UK Muslim who prays but doesn't understand the Arabic", "revert": "a 31-year-old revert learning Arabic"}
Q = {"finish": {"type": "score", "instructions": "`ctx` `s` Viewer: `who` (doesn't follow the account). How likely are they to watch to the end?",
                "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "comment": {"type": "score", "instructions": "`ctx` `s` Viewer: `who`. How likely are they to comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "clear": {"type": "score", "instructions": "`ctx` `s` Viewer: `who`. Is the door metaphor clear and moving rather than confusing or preachy?",
               "criteria": ["Confusing", "A bit", "Mostly clear", "Clear and moving"]}}
if __name__ == "__main__":
    jobs = [(k, w) for k in S for w in WHO for _ in range(3)]
    with ThreadPoolExecutor(12) as ex: res = list(ex.map(lambda j: (j, ask({"ctx": CTX, "s": " ".join(S[j[0]]), "who": WHO[j[1]]}, Q)["answers"]), jobs))
    for k in S:
        s = {q: sum(a[q]["score"] for (kk, _), a in res if kk == k) / 6 for q in Q}
        print(f"{k} finish {s['finish']:.2f}  comment {s['comment']:.2f}  clear {s['clear']:.2f}  total {sum(s.values()):.2f}")
