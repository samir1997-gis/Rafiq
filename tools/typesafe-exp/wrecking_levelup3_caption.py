# Captions for the wrecking-ball reel (wrecking-brian-v3, #288) and level-up ad version 3 ("forces conspiring against you", #273),
# both posted as trial reels (shown to non-followers first), so the caption leads with the idea, not the pitch.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/wrecking_levelup3_caption.py
# Result (24 Oct 2026; comment / share / trust, 2 viewers x 2): wrecking W1 1.79 / 1.75 / 0.51 (chosen) · W2 1.61 / 1.88 / 0.11 · W3 1.58 / 1.69 / 0.06;
# level-up L2 1.78 / 1.58 / 1.06 (chosen) · L1 1.64 / 1.42 / 0.25 · L3 1.36 / 1.58 / 0.25. Anything with a link or "Arabic is the key" read as an ad.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = {
 "W": ("An Instagram Reel from a small account teaching the Arabic Muslims use: 8 seconds of a wrecking ball swinging at a brick wall with a "
       "FRAMES TO IMPACT counter; it never hits. A calm narrator: 'You just watched a wrecking ball for seven seconds... a wrecking ball that was "
       "never there. If you can watch that, you can watch this for another fifteen. Arabic is the key to unlocking your religion: every word of "
       "your salah, the Qur'an in the language it came down in, your du'a finally understood. Without Arabic it's like reading a book in the dark. "
       "So unlock it. RafiqArabic.com.' Caption under it: "),
 "L": ("An Instagram Reel: a young British Muslim founder talks to camera: 'There are forces conspiring against you to take you from your deen. "
       "The sooner we realise, the better. It's not enough to be passive Muslims anymore; we have to level up, invest in ourselves. The easiest "
       "way is Arabic: the Qur'an came down in Arabic.' His app is shown on a phone; 'less than a coffee a month'; 'Are you ready? RafiqArabic.com'. "
       "Caption under it: "),
}
C = {
 "W1": ("W", "You watched a wall not get hit for 8 seconds 😅 Now imagine giving that attention to the words you say in salah. Arabic is the key 🗝️ How long did you watch before you realised? 👇 #learnarabic #arabic #salah #muslim #islam"),
 "W2": ("W", "Admit it, you waited for it to hit 😅 Every word of your salah, the Qur'an, your du'a: it's all behind one door, and Arabic is the key 🗝️ Send this to someone who'd still be waiting 👇 #learnarabic #arabic #salah #quran #muslim"),
 "W3": ("W", "Reading the Qur'an without Arabic is like reading a book in the dark 📖 Unlock it, 5 minutes a day: rafiqarabic.com (free for 7 days). Did you wait for the ball? 👇 #learnarabic #arabic #quran #salah #muslim"),
 "L1": ("L", "It's not enough to be a passive Muslim anymore 🤍 The Qur'an came down in Arabic, so that's where levelling up starts. Are you ready? Comment 'ready' 👇 #muslim #deen #learnarabic #arabic #islam"),
 "L2": ("L", "There's a lot pulling you away from your deen. What's pulling you back? 🤍 For me it was learning the Arabic of my salah, 5 minutes a day. What's yours? 👇 #muslim #deen #learnarabic #salah #islam"),
 "L3": ("L", "Be honest: are you levelling up, or just getting through the day? 🤲 Invest in your deen: learn the words you pray, free for 7 days at rafiqarabic.com. #muslim #deen #learnarabic #salah #islam"),
}
WHO = {"target": "a 27-year-old UK Muslim who prays but doesn't understand the Arabic", "revert": "a 31-year-old revert learning Arabic"}
Q = {"comment": {"type": "score", "instructions": "`ctx` `c` Viewer: `who` (doesn't follow the account). How likely are they to comment?",
                 "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "share": {"type": "score", "instructions": "`ctx` `c` Viewer: `who` (doesn't follow the account). How likely are they to send it to someone or save it?",
               "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "trust": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. Does the caption feel genuine rather than an ad or clickbait?",
               "criteria": ["Ad / clickbait", "A bit", "Mostly genuine", "Genuine"]}}
if __name__ == "__main__":
    jobs = [(k, w) for k in C for w in WHO for _ in range(2)]
    with ThreadPoolExecutor(24) as ex: res = list(ex.map(lambda j: (j, ask({"ctx": CTX[C[j[0]][0]], "c": C[j[0]][1], "who": WHO[j[1]]}, Q)["answers"]), jobs))
    for k in C:
        s = {q: sum(a[q]["score"] for (kk, _), a in res if kk == k) / 4 for q in Q}
        print(f"{k:4} comment {s['comment']:.2f}  share {s['share']:.2f}  trust {s['trust']:.2f}  total {sum(s.values()):.2f}")
