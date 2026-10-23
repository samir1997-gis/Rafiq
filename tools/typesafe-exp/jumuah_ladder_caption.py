# Caption for l2-jumuah (23 Oct 2026, #286): the difficulty ladder, Jumuʿah edition, the owner stitched under it: ghusl 90% →
# jamāʿah 70% → ʿiṭr (perfume) 45% → libās (clothes) 20% → the final boss anṣit "be quiet and listen!" 1%. Ends: "How far did you
# get? Comment your score; send this to who you're going to Jumuʿah with". The caption gives no answer away and has a share line.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/jumuah_ladder_caption.py
# Result (23 Oct 2026; comment / share / trust, 2 viewers x 2): sunnah 2.37 / 2.04 / 1.54 (chosen, reworded "comes from a Friday hadith": congregation and the khutbah silence are duties, not sunnahs) · ladder 2.28 / 2.06 / 1.42 · boss 2.40 / 2.09 / 0.93 (reads as clickbait).
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A TikTok/Instagram Reel from a small account teaching the Arabic Muslims use: a quiz for Friday (Jumu'ah), five Arabic words "
       "linked to Friday, each harder than the last, a 3-second countdown each, a rail showing '90% still in' dropping to '1%' for the "
       "final boss word. Ends: 'How far did you get? Comment your score, and send this to who you're going to Jumu'ah with.' Caption under it: ")
C = {
 "ladder": "Jumuʿah edition 🕌 Five Friday words, each one harder than the last. Only 1% get the final boss 😈 How far did you get? 👇 Send this to who you're going to Jumuʿah with 🤍 #jumuah #jummah #learnarabic #arabicquiz #muslim",
 "sunnah": "Every word in this quiz is a Friday sunnah 🕌 Can you get all five before the timer? Comment your score 👇 and send it to who you're going to Jumuʿah with 🤍 #jumuah #jummah #learnarabic #arabicquiz #muslim",
 "boss": "The last word is something the Prophet ﷺ warned us about during the khutbah 😳 Can you get there? Comment your score 👇 Send this to your Jumuʿah crew 🤍 #jumuah #jummah #learnarabic #arabicquiz #muslim",
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
