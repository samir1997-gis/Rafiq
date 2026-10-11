# "We counted every word of the Quran" video (owner, 11 Oct 2026, after a viral frames.of.quran reel): which hook and ending?
# Facts (Quranic Arabic Corpus v0.4): 6,236 verses, 77,429 words, 4,831 different words (lemmas) from 1,642 roots;
# the 100 most common words are 54.8% of all words, the top 10 about a quarter.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/quran_count_video.py
# Result (11 Oct; hold/share/trust): 'Think understanding the Quran is too hard?' + 'Start with 100 words' + send ask 7.32 (used) ·
#   'We counted every word' + the same ending 7.23 · the rest 6.87-7.19. Trust is the low score everywhere, so the video shows its source.
# Caption (engage/spoil/trust): A_q 6.09 (used) · B_tell 5.34 (giving the numbers away leaves no reason to watch).
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = ("A 22-second vertical video (Instagram/TikTok) from Rafiq, a small Arabic-learning account, in the style of a viral Quran data reel: "
       "dark sky, a grid of 6,236 dots (one per verse), numbers counting up, no talking, soft background sound. It shows: 77,429 words; only 4,831 "
       "different ones; the 100 most common make up more than half of the Quran (the dots light up gold); the top 10 words with meanings. ")
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun", "learner": "a 34-year-old who has wanted to understand the Quran for years",
       "revert": "a 30-year-old revert learning to pray"}
OPEN = {"A_counted": "On screen from the first frame: 'We counted every word of the Quran.'",
        "B_hard": "On screen from the first frame: 'Think understanding the Quran is too hard?'",
        "C_100": "On screen from the first frame: '100 words make up more than half of the Quran.'"}
END = {"X_hard": "Ends: 'Think the Quran is too hard to understand? Start with 100 words.' then 'Send this to someone learning the Quran 🤍'",
       "Y_follow": "Ends: 'Start with 100 words. Follow, and learn them one a day.'",
       "Z_comment": "Ends: 'How many of the top 10 did you know? Comment 👇' then 'Send this to someone learning the Quran 🤍'"}
Q = {"hold": {"type": "score", "instructions": "`ctx` `o` Viewer: `who`. How likely are they to watch to the end?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "share": {"type": "score", "instructions": "`ctx` `o` `e` Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "trust": {"type": "score", "instructions": "`ctx` `o` `e` Viewer: `who`. Does it feel honest and accurate, not clickbait?", "criteria": ["Clickbait", "A bit misleading", "Mostly honest", "Honest"]}}
if __name__ == "__main__":
    jobs = [(o, n, w) for o in OPEN for n in END for w in WHO]
    with ThreadPoolExecutor(20) as ex: res = list(ex.map(lambda j: (j[:2], ask({"ctx": CTX, "o": OPEN[j[0]], "e": END[j[1]], "who": WHO[j[2]]}, Q)["answers"]), jobs))
    for o in OPEN:
        for n in END:
            s = {q: sum(a[q]["score"] for k, a in res if k == (o, n)) / len(WHO) for q in Q}
            print(f"{o:10} {n:10}" + "".join(f"{s[q]:7.2f}" for q in Q) + f"{sum(s.values()):8.2f}")

# Caption (hook B, ending X).
CAP = {"A_q": "Think understanding the Quran is too hard? We counted every word of it 👀 Watch the dots turn gold. Which of the top 10 did you already know? 👇 Send this to someone learning the Quran 🤍 #quran #learnarabic #arabic #muslim #islam #quranic",
       "B_tell": "Think understanding the Quran is too hard? 77,429 words, but just 100 of them are more than half. Start there 🤍 Send this to someone learning the Quran. #quran #learnarabic #arabic #muslim #islam #quranic"}
QC = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
      "spoil": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. Does the caption give away so much that there's no reason to watch?", "criteria": ["Gives it all away", "Gives a lot away", "A little", "Nothing, makes you watch"]},
      "trust": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. Does it feel honest and accurate, not clickbait?", "criteria": ["Clickbait", "A bit misleading", "Mostly honest", "Honest"]}}
if __name__ == "__main__":
    jobs = [(k, w) for k in CAP for w in WHO for _ in range(2)]
    with ThreadPoolExecutor(12) as ex: res = list(ex.map(lambda j: (j[0], ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, QC)["answers"]), jobs))
    for k in CAP:
        s = {q: sum(a[q]["score"] for kk, a in res if kk == k) / (2 * len(WHO)) for q in QC}
        print(f"{k:8}" + "".join(f"{s[q]:7.2f}" for q in QC) + f"{sum(s.values()):8.2f}")
