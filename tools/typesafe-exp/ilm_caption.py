# Caption for n3-ilm (21 Oct 2026, #272): the word tree, part 2. Hook "The WORLD is a sign, and you say it in every prayer!" over the sun,
# moon, stars, mountains, sea and trees, each tagged "a sign"; al-Fātiḥah 1:2 (al-Husary); ع ل م grows عِلْم and مُعَلِّم; your turn: عَلامَة,
# 3-2-1, a sign; Ibn Kathīr on 1:2 (ʿālam from ʿalāma). Ends "What sign of Allah did you notice today? Comment below", then the owner's
# end card. The caption adds to the video and gives no answer away.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/ilm_caption.py
# Result: not run yet (no TYPE_SAFE_KEY in the session that wrote it; #262).
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A TikTok/Instagram Reel from a small account teaching the Arabic Muslims use. A voice says 'The world is a sign, and you say it in every "
       "prayer!' over the sun, moon, stars, mountains, sea and trees; al-Fatiha's 'Lord of the worlds', whose root (to know) grows into a tree: "
       "knowledge, teacher, and a last word to guess with a 3-2-1, which turns out to mean 'a sign'; Ibn Kathir's tafsir that the world is named "
       "from 'sign' because it points to its Creator. Ends: 'What sign of Allah did you notice today? Comment below.' Caption under it: ")
C = {
 "seventeen": "Knowledge, a teacher and the whole world grow from one root, and you say it 17 times a day 🌍 What sign did you notice today? 👇 #learnarabic #arabic #arabicroots #quran #muslim",
 "sunset": "Next sunset you see, remember what Ibn Kathir said about the word for “world” 🌅 Comment the sign you noticed today 👇 #learnarabic #arabic #quran #tafsir #muslim",
 "plain": "One root, three letters: knowledge, teacher, and a word that changes how you hear al-Fātiḥah 🌳 Send this to someone you pray with #learnarabic #arabic #arabicroots #quran #muslim",
}
WHO = {"target": "a 27-year-old UK Muslim who prays but doesn't understand the Arabic", "revert": "a 31-year-old revert learning Arabic"}
Q = {"comment": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. How likely are they to comment?",
                 "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "share": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. How likely are they to send it to someone?",
               "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "trust": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. Does the caption feel honest and interesting rather than clickbait?",
               "criteria": ["Clickbait", "A bit", "Mostly honest", "Honest and interesting"]}}
if __name__ == "__main__":
    jobs = [(k, w) for k in C for w in WHO for _ in range(2)]
    with ThreadPoolExecutor(20) as ex: res = list(ex.map(lambda j: (j, ask({"ctx": CTX, "c": C[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
    for k in C:
        s = {q: sum(a[q]["score"] for (kk, _), a in res if kk == k) / 4 for q in Q}
        print(f"{k:10} comment {s['comment']:.2f}  share {s['share']:.2f}  trust {s['trust']:.2f}  total {sum(s.values()):.2f}")
