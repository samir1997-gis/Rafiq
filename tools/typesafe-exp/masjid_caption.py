# Caption and title for the t1-masjid teaching video (#218). Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/masjid_caption.py
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
CTX = ("A 26-second TikTok from Rafiq (Arabic for UK Muslim beginners): مَـ at the start of a word often means 'the place of'. مَسْجِد is the place of "
       "السُّجُود (prostration); then مَدْرَسَة (place of studying, school), مَكْتَبَة (place of books, library), مَطْعَم (place of food, restaurant), root letters "
       "coloured. It ends 'Your turn': مَطْبَخ, a 3-2-1 countdown, then the answer (kitchen, the place of cooking).")
C = {
 "C0_his": "Why is a mosque called a masjid? 🕌 Once you see this pattern you'll spot it everywhere. Did you get the last one before the answer? #learnarabic #arabic #masjid #islam #muslim",
 "C1_meaning": "Masjid literally means “the place of sujood” 🕌\n\nمَـ at the start of a word often means “the place of”: school, library, restaurant… Did you guess the last one before the answer? Tell us below 👇\n\nUnderstand the words of your deen → rafiq-arabic.com\n\n#learnarabic #arabic #masjid #islam #muslim",
 "C2_reflect": "Every time you walk into the masjid, its name tells you why you're there: مَسْجِد, the place of sujood 🤲\n\nOne small pattern, مَـ = “the place of”, and suddenly school, library and restaurant make sense too. Did you get the last one?\n\nLearn the words you say → rafiq-arabic.com\n\n#learnarabic #arabic #masjid #islam #muslim",
}
T = {"T1": "Why is a mosque called a masjid?", "T2": "Masjid means “the place of sujood”", "T3": "One Arabic pattern: مَـ = “the place of”"}
WHO = {"beginner": "a UK Muslim who can't read Arabic, scrolling TikTok", "some": "a UK Muslim who reads Quran letters but doesn't understand them", "parent": "a busy Muslim parent on Instagram"}
QC = {"engage": {"type": "score", "instructions": "`ctx` Caption: `c`. Viewer: `who`. How likely are they to watch to the end and comment their guess?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
      "visit": {"type": "score", "instructions": "`ctx` Caption: `c`. Viewer: `who`. How likely are they to visit the site?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
      "respect": {"type": "score", "instructions": "`ctx` Caption: `c`. Viewer: `who`. How respectful and sincere does it feel?", "criteria": ["Not at all", "A little", "Fairly", "Very"]}}
QT = {"stop": {"type": "score", "instructions": "`ctx` Post title: `c`. Viewer: `who`. How likely are they to stop and watch?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
      "clear": {"type": "score", "instructions": "`ctx` Post title: `c`. Viewer: `who`. How clear is what the video is about?", "criteria": ["Unclear", "Somewhat", "Clear", "Very clear"]}}
def run(opts, qs, title):
    jobs = [(k, w) for k in opts for w in WHO]
    with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "c": opts[j[0]], "who": WHO[j[1]]}, qs)["answers"]), jobs))
    print(f"\n{title}\n{'':12}" + "".join(f"{q:>9}" for q in qs))
    for k in sorted(opts, key=lambda k: -sum(r[(k, w)][q]['score'] for w in WHO for q in qs)):
        print(f"{k:12}" + "".join(f"{sum(r[(k, w)][q]['score'] for w in WHO) / 3:9.2f}" for q in qs))
run(C, QC, "Captions"); run(T, QT, "Titles")
