# Caption for the departure board (25 Oct 2026, #293): a new format with no voice and no reused audio. A split-flap board at night asks
# "Why is dhikr hiding in the Arabic word for ticket?"; ذ ك ر = to remember, tadhkira literally means "a reminder"; your turn ذاكِرَة
# (memory, prayer mat or station?) with 3-2-1 flipping on the board; فَاذْكُرُونِي أَذْكُرْكُمْ (2:152); "What dhikr do you say the most?
# Comment it". The caption repeats the hook question and gives no answer away (no "memory" in it).
# Not run yet: no TYPE_SAFE_KEY in the session that made it (#262).
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/board_caption.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A TikTok/Instagram Reel from a small account teaching the Arabic Muslims use. No voiceover: the whole video is a train station "
       "departure board whose letters flip and clatter. It asks 'Why is dhikr hiding in the Arabic word for ticket?', shows the same three "
       "letters mean 'to remember' and that the word for ticket literally means 'a reminder', then a quiz (what does a third word from the "
       "same letters mean: memory, prayer mat or station?) with a 3-2-1 on the board, then the verse 'Remember Me, and I will remember you' "
       "(2:152). Ends: 'What dhikr do you say the most? Comment it' and 'send this to the friend who always reminds you'. Caption under it: ")
C = {
 "question": "Why is dhikr hiding inside the Arabic word for ticket? 🎟️ Guess the last one before the board hits 1, then tell me: what dhikr do you say the most? Comment it 👇 #learnarabic #arabic #arabicroots #dhikr #muslimtiktok",
 "remind": "Dhikr is hiding inside the Arabic word for ticket 🎟️ Send this to the friend who always reminds you 🤍 Did you get the last one before the 3-2-1? #learnarabic #arabic #arabicroots #dhikr #muslimtiktok",
 "sound": "Sound on 🔊 Why is dhikr hiding in the Arabic word for ticket? 🚉 What dhikr do you say most? Comment it 👇 #learnarabic #arabic #dhikr #arabicroots #satisfying",
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
