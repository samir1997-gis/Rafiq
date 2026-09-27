# What to call the "New words 4 of 4" step on Home and in the unit's step list (issue #116).
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/step_label.py
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
STEP = ("In an Arabic learning app, a lesson step where you meet 10 new items one at a time (picture, Arabic, transliteration, "
        "English meaning, recorded audio, say it aloud), then a quick 'pick the meaning' check. In unit 1 the items are a mix of "
        "single words and short phrases (e.g. 'peace be upon you', 'what's your name?', 'what God has willed'). Each unit has 4 of these "
        "steps spread among other steps (a conversation, grammar, practice). This is the 4th and last one of unit 1.")
WHERE = ("It is the big title on the Home screen card: 'UNIT 1 OF 12 · STEP 7 OF 9', the unit name in Arabic, then the title, "
         "then 'Greetings & introductions · about 5 minutes' and a Continue button. The same title appears in the unit's list of steps.")
WHO = ["an adult complete beginner", "a busy parent on a phone", "a 16-year-old", "an older learner who is not very techy"]
LABELS = {
 "now": "New words 4 of 4",
 "set": "New words: set 4 of 4",
 "set_count": "New words: set 4 of 4 · 10 words",
 "last10": "Your last 10 new words",
 "wp_part": "Words & phrases · part 4 of 4",
 "wp_count": "10 new words & phrases",
 "wp_last": "Last 10 words & phrases",
 "meet": "Meet 10 new words & phrases",
 "vocab": "Vocabulary 4 of 4",
 "learn_say": "Learn 10 new things to say",
}
Q = {"clear": {"type": "score", "instructions": "`step` `where` The title is: `label`. For `who`, how clearly does the title tell them what this step is and what they'll do?",
               "criteria": ["Not clear", "A little", "Mostly", "Completely"]},
     "misread": {"type": "score", "instructions": "`step` `where` The title is: `label`. How likely is `who` to misunderstand it (e.g. think it means only 4 words, or not know what 'set'/'part' means)?",
                 "criteria": ["Not likely", "A little", "Quite", "Very"]},
     "accurate": {"type": "score", "instructions": "`step` The title is: `label`. How accurately does it describe what the step contains?",
                  "criteria": ["Inaccurate", "Partly", "Mostly", "Exactly"]},
     "inviting": {"type": "score", "instructions": "`step` `where` The title is: `label`. How much does it make `who` want to tap Continue?",
                  "criteria": ["Not at all", "A little", "Quite", "Very"]}}
jobs = [(k, w) for k in LABELS for w in WHO]
def run(j):
    k, w = j
    a = ask({"step": STEP, "where": WHERE, "label": LABELS[k], "who": w}, Q)["answers"]
    return j, tuple(a[q]['score'] for q in ("clear", "misread", "accurate", "inviting"))
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(run, jobs))
rows = []
for k in LABELS:
    c, m, a, i = (sum(r[(k, w)][n] for w in WHO) / len(WHO) for n in range(4))
    rows.append((c - m + a + i, c, m, a, i, k))
print("value = clear - misread + accurate + inviting")
for v, c, m, a, i, k in sorted(rows, reverse=True): print(f"{v:5.2f}  clear {c:.2f}  misread {m:.2f}  accurate {a:.2f}  inviting {i:.2f}  {LABELS[k]}")
