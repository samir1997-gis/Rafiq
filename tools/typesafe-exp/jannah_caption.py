# Caption for n4-jannah (22 Oct 2026, #281): the word tree, part 3. Hook "Why does JANNAH share the same root as the jinn?" over gardens,
# the night, a shield, a baby, the unseen and the jinn, hidden by leaves; al-Anʿām 6:76 (al-Husary) "when the night covered him": ج ن ن;
# جَنَّة and جِنّ bloom; your turn جُنَّة, 3-2-1, a shield; then why Jannah is called Jannah, with the ḥadīth qudsī (al-Bukhārī 3244). Ends
# "Send this to someone you want to meet in Jannah, and comment: what will you ask for first?", then the owner's end card.
# The caption repeats the hook question and gives no answer away (not "hidden"); share line included.
# Result (22 Oct 2026; comment / share / trust, 2 viewers x 2): question 2.43 / 2.37 / 1.76 (chosen: repeats the hook) · letters 2.41 / 2.38 / 1.79 · shield 2.37 / 2.31 / 1.81.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/jannah_caption.py
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A TikTok/Instagram Reel from a small account teaching the Arabic Muslims use. A voice asks 'Why does Jannah share the same root as the "
       "jinn?' over little labels (gardens, the night, a shield, a baby, the unseen, the jinn) that leaves grow over; a Qur'an verse about Prophet "
       "Ibrahim, 'when the night covered him', gives the root's meaning; Jannah and jinn grow on a tree from it; a quiz word turns out to mean "
       "'a shield'; then why Paradise is called Jannah, with the hadith 'what no eye has seen, no ear has heard'. Ends: 'Send this to someone "
       "you want to meet in Jannah, and comment: what will you ask for first?' Caption under it: ")
C = {
 "question": "Why does Jannah share the same root as the jinn? 🤔 The answer is in a verse about Prophet Ibrahim, and it changes how you hear the word Jannah 🤍 Send this to someone you want to meet in Jannah 👇 #learnarabic #arabic #arabicroots #quran #jannah",
 "letters": "Jannah and jinn: the same three letters, ج ن ن. Why? 🌴 Stay for the hadith at the end. Send this to someone you want to meet in Jannah 🤍 #learnarabic #arabic #arabicroots #quran #jannah",
 "shield": "Why does Jannah share a root with the jinn? One root links Paradise, the jinn and a shield 🛡️ Send this to someone you want to meet in Jannah, and comment what you'll ask for first 👇 #learnarabic #arabic #arabicroots #quran #jannah",
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
