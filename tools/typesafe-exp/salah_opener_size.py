# How big should the "Your most-said words" opener be? (#124 follow-up)
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/salah_opener_size.py
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
APP = ("Rafiq's 'Your salah' track starts with the words said most in the prayer: the top 20 are about 56% of everything said in a 4-rakah "
       "prayer (the top 10 about 40%). A part shows words 5 per screen, each with meaning, root, 'you say this N times', then a quick "
       "'pick the meaning' check, and the words join spaced review. The main course meets 10 new words per step.")
WHO = ["a UK Muslim adult who prays daily but understands little", "a new Muslim who can't read Arabic yet", "a busy parent with 5 minutes", "a 16-year-old"]
OPTS = {
 "one20": "One part of all 20 words (4 screens of 5 words, then a check of 6).",
 "two10": "Two parts of 10 words each ('Your most-said words 1' and '2'), each 2 screens of 5 then a check of 5; the second part comes straight after the first on the path.",
 "two10_split": "Two parts of 10: the first 10 as the opener, the other 10 after the first real part of the prayer (the takbir), so words and prayer alternate.",
 "four5": "Four small parts of 5 words each, one screen then a check of 3.",
}
Q = {"digest": {"type": "score", "instructions": "`app` Option: `opt`. How easily can `who` take it in without feeling overloaded?", "criteria": ["Overloaded", "A lot", "Manageable", "Easy"]},
     "remember": {"type": "score", "instructions": "`app` Option: `opt`. How well will `who` remember the words a week later?", "criteria": ["Poorly", "Somewhat", "Well", "Very well"]},
     "progress": {"type": "score", "instructions": "`app` Option: `opt`. How strongly does `who` feel quick, motivating progress?", "criteria": ["Not at all", "A little", "Clearly", "Strongly"]}}
jobs = [(k, w) for k in OPTS for w in WHO]
def run(j):
    k, w = j
    a = ask({"app": APP, "opt": OPTS[k], "who": w}, Q)["answers"]
    return j, {q: a[q]['score'] for q in Q}
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(run, jobs))
avg = lambda k, q: sum(r[(k, w)][q] for w in WHO) / len(WHO)
for v, k in sorted(((sum(avg(k, q) for q in Q), k) for k in OPTS), reverse=True):
    print(f"{v:5.2f}  digest {avg(k,'digest'):.2f}  remember {avg(k,'remember'):.2f}  progress {avg(k,'progress'):.2f}  {k}")
