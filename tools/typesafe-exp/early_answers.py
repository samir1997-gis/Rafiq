# Units 1-3: how should "Find the mistake", rewrite exercises and the conversation step be answered,
# now that "Say this in Arabic" uses word tiles there (issue #118)?
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/early_answers.py
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
APP = ("Rafiq, an Arabic learning app on phones. In units 1-3 (the first few weeks) learners answer 'Say this in Arabic' by tapping "
       "word tiles into order; typing Arabic starts around unit 7, as they are ready. Many beginners have never typed Arabic and "
       "have no Arabic keyboard set up; the app has an on-screen Arabic keyboard.")
WHO = ["an adult complete beginner in week 1", "a busy parent on a phone", "an impatient 16-year-old", "a learner who can read Quran script slowly"]
EX = {
 "fix": ("'Find the mistake and correct it': the app shows a sentence with one mistake, e.g. هَذا أُخْتِي (wrong: 'this' should be "
         "feminine), and the answer is هَذِهِ أُخْتِي. A short explanation follows."),
 "transform": ("A rewrite exercise, e.g. 'Change to feminine': هَذا طالِبٌ becomes هَذِهِ طالِبَةٌ."),
 "chat": ("'Have the conversation', the last big step of each unit: the other speaker says a line (audio and text), the learner is told "
          "what to get across (e.g. 'Say your name and ask theirs') and replies; an AI checks the reply and gives feedback. "
          "This step is a highlight of the paid Complete plan."),
}
OPTS = {
 "fix": {
  "type":        "Type the corrected sentence in Arabic (as today).",
  "tiles":       "Build the corrected sentence from word tiles (the right sentence's words, shuffled).",
  "tap_pick":    "Tap the word that's wrong, then pick the right word from 3 options.",
  "tiles_decoy": "Build the corrected sentence from tiles that also include the wrong word as a decoy.",
 },
 "transform": {
  "type":        "Type the rewritten sentence in Arabic (as today).",
  "tiles":       "Build the rewritten sentence from word tiles.",
  "pick3":       "Pick the right rewrite from 3 sentences.",
  "tiles_decoy": "Build it from tiles that include the original word as a decoy (e.g. both هَذا and هَذِهِ).",
 },
 "chat": {
  "type":        "Type a reply in your own words (as today); a 'Show the Arabic' hint is available.",
  "tiles":       "Build the reply from word tiles of a model reply; 'Type it in your own words' is available.",
  "pick3":       "Pick the right reply from 3 options (one right, two that don't fit), then hear it and say it aloud.",
  "pick_then_tiles": "Units 1-2: pick from 3 replies; unit 3: build the reply from tiles; own-words typing from unit 4, always available as an option.",
  "say_aloud":   "See and hear a model reply, say it aloud, then continue (no answer checked).",
 },
}
Q = {"doable": {"type": "score", "instructions": "App: `app`. Exercise: `ex`. How it's answered: `opt`. How comfortably can `who` do this in units 1-3 without getting stuck?",
                "criteria": ["Gets stuck", "Struggles", "Mostly fine", "Comfortable"]},
     "learn": {"type": "score", "instructions": "App: `app`. Exercise: `ex`. How it's answered: `opt`. How much does `who` actually learn from it?",
               "criteria": ["Little", "Some", "Good", "A lot"]},
     "keep": {"type": "score", "instructions": "App: `app`. Exercise: `ex`. How it's answered: `opt`. How likely is `who` to keep going rather than quit or skip?",
              "criteria": ["Unlikely", "Somewhat", "Likely", "Very likely"]}}
jobs = [(e, k, w) for e in OPTS for k in OPTS[e] for w in WHO]
def run(j):
    e, k, w = j
    a = ask({"app": APP, "ex": EX[e], "opt": OPTS[e][k], "who": w}, Q)["answers"]
    return j, (a['doable']['score'], a['learn']['score'], a['keep']['score'])
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(run, jobs))
for e in OPTS:
    print(f"\n{e}  (value = doable + learn + keeps going)")
    rows = []
    for k in OPTS[e]:
        d, l, g = (sum(r[(e, k, w)][i] for w in WHO) / len(WHO) for i in range(3))
        rows.append((d + l + g, d, l, g, k))
    for v, d, l, g, k in sorted(rows, reverse=True): print(f"  {v:5.2f}  doable {d:.2f}  learn {l:.2f}  keeps going {g:.2f}  {k}")
