# Should a right answer on a multiple-choice question move on by itself, and how?
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/auto_advance.py
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
APP = ("Rafiq, an Arabic learning web app on phones. Multiple-choice questions: pick the meaning of an Arabic word, pick a letter "
       "by its sound, pick the word that fits a gap in a sentence. When you tap an option it turns green (right) or red (wrong, and the "
       "right one turns green), a sound plays, and the Arabic word or sentence is spoken aloud by a recorded voice (1-3 seconds). "
       "In review sessions, fill-the-gap answers also show a one-line explanation and an English translation.")
WHO = ["an adult complete beginner on a phone", "a busy parent doing 5 minutes a day", "an impatient 16-year-old", "a careful learner who likes to read every explanation"]
OPTS = {
 "now":        "Today: after any answer, a Next button appears and they must tap it to go on.",
 "fixed":      "After a RIGHT answer, the app moves on by itself 0.9 seconds after the tap (the audio may be cut off). After a wrong answer, a Next button appears.",
 "after_audio":"After a RIGHT answer, the app waits for the spoken word to finish, then moves on by itself about half a second later. Tapping anywhere moves on sooner. After a wrong answer, a Next button appears so they can look at the right answer.",
 "after_audio_not_explained": "Like the previous one, but only for simple picks (word meaning, letter by sound). Where there is an explanation and translation to read (fill-the-gap in reviews), a right answer still shows Next.",
 "all":        "After ANY answer (right or wrong), the app moves on by itself after 1.5 seconds.",
}
Q = {"flow": {"type": "score", "instructions": "App: `app`. Behaviour: `opt`. For `who`, how smooth and satisfying does answering feel?",
              "criteria": ["Clunky", "OK", "Smooth", "Very smooth"]},
     "learn": {"type": "score", "instructions": "App: `app`. Behaviour: `opt`. For `who`, how well do they still hear and take in the right answer?",
               "criteria": ["Poorly", "Somewhat", "Well", "Very well"]},
     "annoy": {"type": "score", "instructions": "App: `app`. Behaviour: `opt`. How likely is `who` to feel rushed, lose their place, or be annoyed?",
               "criteria": ["Not likely", "A little", "Quite", "Very"]}}
jobs = [(k, w) for k in OPTS for w in WHO]
def run(j):
    k, w = j
    a = ask({"app": APP, "opt": OPTS[k], "who": w}, Q)["answers"]
    return j, (a['flow']['score'], a['learn']['score'], a['annoy']['score'])
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(run, jobs))
rows = []
for k in OPTS:
    f, l, n = (sum(r[(k, w)][i] for w in WHO) / len(WHO) for i in range(3))
    rows.append((f + l - n, f, l, n, k))
print("value = flow + learning - annoyance")
for v, f, l, n, k in sorted(rows, reverse=True): print(f"{v:5.2f}  flow {f:.2f}  learning {l:.2f}  annoyance {n:.2f}  {k}")
