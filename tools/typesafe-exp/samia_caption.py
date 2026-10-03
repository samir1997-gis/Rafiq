# Caption and title for the سَمِعَ ("hears") quiz post (brag-quiz q1-samia / s1-samia). Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/samia_caption.py
from concurrent.futures import ThreadPoolExecutor
import json, os, time, urllib.request
KEY = os.environ.get("TYPESAFE_API_KEY") or os.environ["TYPE_SAFE_KEY"]
def ask(state, qs):
    body = json.dumps({"state": state, "model": "jev-latest", "questions": qs}).encode()
    for a in range(5):
        try:
            r = urllib.request.Request("https://api.typesafe.ai/v1/systemone", body, {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
            with urllib.request.urlopen(r, timeout=60) as f: return json.load(f)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504, 529) and a < 4: time.sleep(2 ** a); continue
            raise
CTX = ("A TikTok/Instagram quiz post from Rafiq (Arabic for UK Muslim beginners): 'What does this word in your salah mean?' سَمِعَ with options sees / hears / "
       "knows / forgives; the answer is 'hears', from سَمِعَ اللَّهُ لِمَنْ حَمِدَهُ, 'Allah hears the one who praises Him', said rising from ruku.")
C = {
 "C1_reflect": "You say it every time you rise from ruku: سَمِعَ اللَّهُ لِمَنْ حَمِدَهُ\n\nBut do you know what سَمِعَ means? Guess before you swipe 👇\n\n“Allah hears the one who praises Him.” Next time you rise, you'll know Who is listening. 🤲\n\nUnderstand every word of your salah → rafiq-arabic.com\n\n#salah #learnarabic #arabic #muslim #islam",
 "C2_quiz":    "Quick salah quiz 🕌 What does سَمِعَ mean? Sees, hears, knows or forgives? Comment your answer, then swipe 👇\n\nIt's from سَمِعَ اللَّهُ لِمَنْ حَمِدَهُ, said rising from ruku.\n\nUnderstand every word of your salah → rafiq-arabic.com\n\n#salah #learnarabic #arabic #muslim #islam",
 "C3_short":   "سَمِعَ: you say it in every rakʿah. Do you know what it means? 👇\n\nUnderstand every word of your salah → rafiq-arabic.com\n\n#salah #learnarabic #arabic #muslim #islam",
}
T = {"T1": "You say this in every rakʿah. What does it mean?", "T2": "What does سَمِعَ mean in your salah?", "T3": "The word you say rising from ruku",
     "T4": "Do you know what you're saying in salah?"}
WHO = {"beginner": "a UK Muslim who prays but can't read Arabic, scrolling TikTok", "some": "a UK Muslim who reads Quran letters but doesn't understand them", "parent": "a busy Muslim parent on Instagram"}
QC = {"engage": {"type": "score", "instructions": "`ctx` Caption: `c`. Viewer: `who`. How likely are they to swipe, answer or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
      "visit": {"type": "score", "instructions": "`ctx` Caption: `c`. Viewer: `who`. How likely are they to visit the site?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
      "respect": {"type": "score", "instructions": "`ctx` Caption: `c`. Viewer: `who`. How respectful and sincere does it feel about the prayer?", "criteria": ["Not at all", "A little", "Fairly", "Very"]}}
QT = {"stop": {"type": "score", "instructions": "`ctx` Post title: `c`. Viewer: `who`. How likely are they to stop and look?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
      "clear": {"type": "score", "instructions": "`ctx` Post title: `c`. Viewer: `who`. How clear is what the post is about?", "criteria": ["Unclear", "Somewhat", "Clear", "Very clear"]}}
def run(opts, qs, title):
    jobs = [(k, w) for k in opts for w in WHO]
    with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "c": opts[j[0]], "who": WHO[j[1]]}, qs)["answers"]), jobs))
    print(f"\n{title}\n{'':12}" + "".join(f"{q:>9}" for q in qs))
    for k in sorted(opts, key=lambda k: -sum(r[(k, w)][q]['score'] for w in WHO for q in qs)):
        print(f"{k:12}" + "".join(f"{sum(r[(k, w)][q]['score'] for w in WHO) / 3:9.2f}" for q in qs))
run(C, QC, "Captions"); run(T, QT, "Titles")
