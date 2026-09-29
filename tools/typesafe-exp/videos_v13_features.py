# Which features to show working in the next videos (#155): the ones that most make people want to pay.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/videos_v13_features.py
from concurrent.futures import ThreadPoolExecutor
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from videos_v9 import ask, FACTS, VIEWERS, Q, avg

FEATURES = {
 # Your salah
 "salah_mostsaid": "Your salah, most-said words: each word of the prayer with its meaning, how many times you say it in a four-rakah prayer, its root, and where it appears in your course",
 "salah_pick": "Your salah, Pick the meaning: a word from the prayer, pick its meaning from four",
 "salah_hear": "Your salah, Hear it, pick the word: hear a word of the prayer, pick it from four",
 "salah_part": "Your salah, a part of the prayer word by word (e.g. ruku, tashahhud, Al-Fatiha): listen, see each word with its meaning",
 "salah_progress": "Your salah progress: 'x of 238 words of your salah understood', growing as you learn",
 "pray_along": "Pray along: a whole prayer line by line, each word lighting up as it's said, then a pause to repeat",
 # practice
 "spelling_bee": "Spelling bee: hear an Arabic word, type it with the Arabic keyboard, get it checked letter by letter",
 "tiles": "Say this in Arabic: build a sentence from word tiles, which becomes typing later",
 "ai_check": "Type your own Arabic; the AI checks it and names the mistake, e.g. 'masculine and feminine must match'",
 "conversation": "Conversation partner: the other person speaks (native voice), you reply in your own words, and get feedback",
 "scenes": "Real-life scenes: the airport, the doctor, the masjid, a taxi: reply in your own words",
 "tutor": "AI tutor: ask anything about Arabic and get a clear answer built on your lessons",
 "why": "Why?: after a wrong answer, a tap explains the mistake",
 "weak_spots": "Weak-spots review: a session built from the mistakes you keep making",
 "alphabet": "Reading starter: tap a letter, hear it, three words with the letter in red",
 "listening_test": "Listening test: hear a word, pick its first letter from look-alike sounds",
 "meet_words": "Meet new words: a picture, the fully vowelled word, a native voice",
 "review": "Reviews scheduled by a memory model: each word comes back just before you'd forget it",
 "streak": "Daily goal and streak on Home",
}
QF = {
 "pay": Q("`facts` A short video shows this Rafiq feature working, live on a phone: `feature`. Viewer: `viewer`. How much does seeing it make them want to pay for Rafiq?", ["Not at all", "A little", "Somewhat", "A lot"]),
 "wow": Q("`facts` A short video shows this Rafiq feature working, live on a phone: `feature`. Viewer: `viewer`. How interesting is it to watch?", ["Dull", "OK", "Interesting", "Gripping"]),
 "different": Q("`facts` Feature: `feature`. Viewer: `viewer`. How clearly does it set Rafiq apart from Duolingo or a Quran app?", ["Not at all", "A little", "Clearly", "Very clearly"]),
}

if __name__ == "__main__":
    with ThreadPoolExecutor(8) as ex:
        jobs = [(f, v) for f in FEATURES for v in VIEWERS]
        r = dict(ex.map(lambda j: (j, ask({"facts": FACTS, "feature": FEATURES[j[0]], "viewer": VIEWERS[j[1]]}, QF)["answers"]), jobs))
    rows = []
    for f in FEATURES:
        rs = [r[(f, v)] for v in VIEWERS]
        rows.append((avg(rs, "pay") + avg(rs, "wow") / 2 + avg(rs, "different") / 2, f, avg(rs, "pay"), avg(rs, "wow"), avg(rs, "different")))
    print(f"{'feature':16} pay   watch  different")
    for _, f, p, w, d in sorted(rows, reverse=True): print(f"{f:16} {p:.2f}  {w:.2f}   {d:.2f}")
