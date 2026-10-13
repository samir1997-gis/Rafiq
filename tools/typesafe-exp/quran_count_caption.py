# Caption for q1-quran-count-v2 (13 Oct 2026): Rafiq's voice counts the Quran (6,236 verses, 77,000 words, 4,800 different ones,
# 100 words make up more than half, the top ten a quarter of every page), ends "start with a hundred words, at rafiq-arabic.com,
# free for a week". A site post (about 1 in 5), so the caption also has to earn the link click, not just the save.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/quran_count_caption.py
# Result (13 Oct; save / click / trust, target + revert x2): numbers 2.57 / 2.67 / 1.39 · question 2.46 / 2.71 / 1.12 ·
#   save 2.79 / 2.72 / 1.57 (chosen: best on all three) · short 2.50 / 2.64 / 1.49.
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A TikTok/Instagram Reel from a small account teaching the Arabic Muslims use. The video counts the Quran: 6,236 verses, "
       "77,000 words, but only about 4,800 different ones, and just 100 words make up more than half of it (words like مِنْ, اللَّه, قَالَ); "
       "the top ten are a quarter of every page. It ends: 'So start with a hundred words. At rafiq-arabic.com, free for a week.' Caption under it: ")
WHO = {"target": "a 27-year-old UK Muslim who prays but doesn't understand the Arabic", "revert": "a 31-year-old revert learning Arabic"}
C = {
 "numbers": "77,000 words in the Quran. Just 100 of them make up more than half 🤯 Start with those 100 and you'll recognise words on every page. Free for a week, link in bio. #quran #learnarabic #quranarabic #arabic #muslim",
 "question": "Think understanding the Quran is too hard? 📖 Just 100 words make up more than half of it. Which word do you think is #1? Comment it 👇 Learn those 100 free for a week, link in bio. #quran #learnarabic #quranarabic #arabic #muslim",
 "save": "Save this for the next time understanding the Quran feels impossible 📖 6,236 verses, 77,000 words, and just 100 of them make up more than half. Start with those, free for a week: link in bio. #quran #learnarabic #quranarabic #arabic #muslim",
 "short": "100 words = more than half the Quran 📖 Start there. Free for a week, link in bio. #quran #learnarabic #quranarabic #arabic #muslim",
}
Q = {"save": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. How likely are they to save or share it?",
              "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "click": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. How likely are they to tap the link in bio to try it?",
               "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "trust": {"type": "score", "instructions": "`ctx` `c` Viewer: `who`. Does the caption feel honest and interesting rather than clickbait or a hard sell?",
               "criteria": ["Clickbait", "A bit", "Mostly honest", "Honest and interesting"]}}
if __name__ == "__main__":
    jobs = [(k, w) for k in C for w in WHO for _ in range(2)]
    with ThreadPoolExecutor(20) as ex: res = list(ex.map(lambda j: (j, ask({"ctx": CTX, "c": C[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
    for k in C:
        s = {q: sum(a[q]["score"] for (kk, _), a in res if kk == k) / 4 for q in Q}
        print(f"{k:10} save {s['save']:.2f}  click {s['click']:.2f}  trust {s['trust']:.2f}  total {sum(s.values()):.2f}")
