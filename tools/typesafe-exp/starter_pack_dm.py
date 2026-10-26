# The DM sent to everyone who comments NOW on the tomorrow-people reels (owner, 26 Oct 2026, #292): what Rafiq is, how it brings you
# closer to your deen, the free trial with no strings, then the 20 most common words of salah (the owner's own list, pasted after).
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/starter_pack_dm.py
# Result (26 Oct 2026; click / trust / read, 2 readers x 3): B 2.03 / 1.36 / 2.51 (chosen: the words first, then Rafiq) · A 1.99 / 1.47 / 2.22 · C 1.98 / 1.12 / 2.45.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("An Instagram DM sent automatically to someone who commented NOW under a reel about 'the tomorrow people' (people who keep saying "
       "they'll start praying properly / learning Arabic tomorrow). They were promised a free starter pack: the 20 most common words of "
       "salah, which follow this message. The message: ")
M = {
 "A": "Assalamu alaykum 🤍 JazakAllahu khayran for commenting, here's your starter pack.\n\nQuick intro: I built Rafiq because for 26 years I prayed without understanding a word of my salah. Rafiq teaches you the Arabic of your salah, word by word, in about 5 minutes a day. Pray along with the meaning on screen, and every day a few more words click.\n\nIt's free for 7 days, no card needed, so nothing to cancel: rafiq-arabic.com\n\nStart with these 20 words. They make up a big part of every prayer 👇",
 "B": "Assalamu alaykum 🤍 You said NOW, so let's start now.\n\nHere are the 20 words you say most in salah 👇 Learn these and your next prayer already feels different.\n\nIf you want to keep going, that's what Rafiq is for: the Arabic of your salah, word by word, 5 minutes a day, until you understand everything you say to Allah. Try it free for 7 days, no card, no strings: rafiq-arabic.com\n\nMay Allah make it easy for you 🤲",
 "C": "Assalamu alaykum! Thanks for commenting 🤍\n\nRafiq is an app that teaches you to understand your salah: the Arabic you actually pray, one word at a time, 5 minutes a day. When you know what you're saying, your prayer stops being words you recite and becomes a conversation with Allah.\n\nTry it free for 7 days, no card details, nothing to cancel: rafiq-arabic.com\n\nAnd as promised, the 20 most common words in salah 👇",
}
WHO = {"target": "a 24-year-old UK Muslim who prays on and off and commented NOW", "learner": "a 30-year-old who keeps meaning to learn Arabic and commented NOW"}
Q = {"click": {"type": "score", "instructions": "`ctx` `m` Reader: `who`. How likely are they to tap the link and try Rafiq?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "trust": {"type": "score", "instructions": "`ctx` `m` Reader: `who`. Does it feel genuine and respectful rather than a sales pitch?", "criteria": ["Pushy pitch", "A bit salesy", "Mostly genuine", "Genuine"]},
     "read": {"type": "score", "instructions": "`ctx` `m` Reader: `who`. How likely are they to read it to the end and look at the 20 words?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]}}
if __name__ == "__main__":
    jobs = [(k, w) for k in M for w in WHO for _ in range(3)]
    with ThreadPoolExecutor(18) as ex: res = list(ex.map(lambda j: (j, ask({"ctx": CTX, "m": M[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
    for k in M:
        s = {q: sum(a[q]["score"] for (kk, _), a in res if kk == k) / 6 for q in Q}
        print(f"{k} click {s['click']:.2f}  trust {s['trust']:.2f}  read {s['read']:.2f}  total {sum(s.values()):.2f}")
