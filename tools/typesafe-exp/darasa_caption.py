# Caption for the collaborator's "to study" (darasa) carousel, reach first (brag-quiz/IDEAS.md, How we post).
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/darasa_caption.py
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
CTX = ("A 9-slide Instagram/TikTok carousel from Rafiq, a small Arabic-learning account: the verb darasa 'to study', one slide per person "
       "(adrusu I study, tadrusu you study (m), tadrusina you study (f), yadrusu he studies, tadrusu she studies, nadrusu we study), the changing letter in red, "
       "a slide with all six, and a last slide with the site.")
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun", "learner": "a 34-year-old who has wanted to learn Arabic for years",
       "student": "someone already learning Arabic at a weekend madrasa"}
CAP = {"A_collab": "“To study” in Arabic, from I to we 📚 One verb, six people: adrusu, tadrusu, tadrusīna, yadrusu, tadrusu, nadrusu. Watch the red: the front letter tells you who. Swipe to the end for all six on one slide. Learn with Rafiq, link in bio (free for a week). #learnarabic #arabic #arabicgrammar #arabicverbs #studyarabic",
       "B_save": "One Arabic verb, six people 📚 Watch the red letter: it tells you who's studying. Save this for later 📌 and tell me 👇 which one is the odd one out? #learnarabic #arabic #arabicgrammar #arabicverbs #studyarabic",
       "C_madrasa": "You know madrasa (a place of study). Now meet the verb behind it: darasa, to study 📚 Swipe to see how it changes for I, you, he, she and we. Save it 📌 #learnarabic #arabic #arabicgrammar #arabicverbs #studyarabic",
       "D_trick": "The front letter tells you who 👀 adrusu, I study · nadrusu, we study. Swipe for all six, then save it 📌 Which form surprised you? 👇 #learnarabic #arabic #arabicgrammar #arabicverbs #studyarabic"}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "follow": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to follow the account?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "content": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How much does it feel like content rather than an ad?", "criteria": ["Pure ad", "Mostly ad", "Mostly content", "Pure content"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
