# Caption for the owner's own talking intro ("As someone who's studying Arabic to understand the Quran and the salah
# a little better...") in front of a short Arabic video. Reach first (brag-quiz/IDEAS.md, How we post).
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/intro_caption.py
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
CTX = ("A TikTok/Instagram video: a young British Muslim man talks to camera, 'As someone who's studying Arabic to understand the Quran "
       "and understand the salah a little bit better...', then a short Arabic learning clip follows. Posted by Rafiq, a small Arabic-learning app account.")
WHO = {"scroller": "a 22-year-old UK Muslim scrolling TikTok for fun", "learner": "a 34-year-old who has wanted to learn Arabic for years but never started",
       "revert": "a 28-year-old revert who prays but doesn't understand the words"}
CAP = {"A_journey": "Learning Arabic so my salah actually means something to me 🤲 Day by day, word by word. Are you learning too? Tell me where you're at 👇 #learnarabic #salah #quran #muslim #arabic",
       "B_question": "Do you understand what you say in your salah? I didn't. So I started learning Arabic, one word at a time 🤲 Follow along if you're on the same journey. #learnarabic #salah #quran #muslim #arabic",
       "C_together": "I'm learning Arabic to understand the Quran and my salah a little better. Learn with me? 🤝 Follow for a few words every week. #learnarabic #salah #quran #muslim #arabic",
       "D_with_link": "Learning Arabic to understand the Quran and my salah a little better 🤲 I built Rafiq to help: your salah, word by word. Free for a week, link in bio. #learnarabic #salah #quran #muslim"}
Q = {"comment": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to comment, share or save it?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "follow": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to follow the account?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "genuine": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How genuine and relatable does it feel (not an ad)?", "criteria": ["Not at all", "A little", "Fairly", "Very"]}}
jobs = [(k, w) for k in CAP for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CAP[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':12}" + "".join(f"{q:>9}" for q in Q) + "   total")
rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in CAP]
for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:12}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
