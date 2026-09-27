# Other ways to make the first units easier for a complete beginner, beyond rewording the grammar cards.
# Result (27 Sep 2026, value = easier + keeps going - cost, avg over 4 learner types):
#   3.36 one idea per card   3.25 quick check after card   3.16 transliteration fades   3.09 spoken explanation
#   2.77 phrases first       2.72 tap-a-term glossary       2.59 no grammar terms        2.15 3 options
#   2.14 endings later       1.87 function words in a sentence   1.36 grammar after practice
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/simplify_ideas.py
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
APP = ("Rafiq, a web app teaching Arabic (Modern Standard, for Muslims in the UK). Each lesson: meet new words (picture, audio, "
       "then a 4-option meaning quiz), a short 'How it works' grammar card (English heading, an Arabic example with its "
       "translation, a plain-English explanation), then practice (build sentences from tiles, type answers, listen). "
       "Words show Arabic with full vowel marks and a transliteration. Word endings (case endings such as -u/-a/-i) are shown from unit 1.")
WHO = ["an adult complete beginner, no grammar background, can't yet read Arabic script",
       "an adult who can read Quran script slowly but knows no grammar",
       "a busy parent doing 5 minutes a day on their phone",
       "a 16-year-old at a weekend madrasa, impatient"]
IDEAS = {
 "endings_later":  "Hide word endings (case endings) in units 1-3: words and sentences show the pause form (e.g. كِتَاب not كِتَابٌ); endings are introduced as their own lesson in unit 4.",
 "one_idea_card":  "Each grammar card teaches exactly one idea in at most two short sentences, with a 'Tell me more' link for the detail.",
 "grammar_after":  "Show the grammar card after the learner has practised the pattern (notice it first, then the card names it), instead of before.",
 "no_terms":       "Never use grammar terms (noun, definite, case, masculine) in units 1-4; say it in everyday words ('words for things', 'the', 'for a man / for a woman').",
 "glossary":       "Any grammar term that does appear is underlined; tapping it shows a one-line everyday explanation and an example.",
 "audio_explain":  "Each grammar card has a 20-second spoken explanation from a teacher, with the example highlighted as it's said.",
 "fewer_options":  "In the first two units, meaning quizzes offer 3 options instead of 4, and never two options that mean nearly the same.",
 "translit_toggle":"Transliteration is on by default in units 1-3, then fades out; a toggle lets the learner turn it back on any time.",
 "function_words": "Words without a simple translation (like هَلْ, the question word) are taught in a sentence ('هَلْ أَنْتَ طَالِبٌ؟ = Are you a student?') rather than in the word quiz with a label like '(question marker)'.",
 "chunks_first":   "Units 1-2 teach whole useful phrases as chunks (greetings, 'my name is…', 'where is…?') with no grammar at all; grammar cards start in unit 3.",
 "check_in":       "After each grammar card, one quick tap question checks it made sense ('Which one means *the* book?'); if they get it wrong, a simpler second explanation appears.",
}
Q = {"easier": {"type": "score", "instructions": "App: `app`. Change: `idea`. For `who`, how much easier would this make the first two weeks?",
                "criteria": ["No easier or harder", "A little easier", "Clearly easier", "Much easier"]},
     "keep_going": {"type": "score", "instructions": "App: `app`. Change: `idea`. How much more likely is `who` to still be using the app after a month?",
                    "criteria": ["No more likely", "A little", "Clearly", "Much more likely"]},
     "cost": {"type": "score", "instructions": "App: `app`. Change: `idea`. Does it cost `who` anything important later (bad habits, relearning, feeling patronised, slower progress)?",
              "criteria": ["No cost", "Small cost", "Real cost", "Big cost"]}}
jobs = [(k, w) for k in IDEAS for w in WHO]
def run(j):
    k, w = j
    a = ask({"app": APP, "idea": IDEAS[k], "who": w}, Q)["answers"]
    return j, (a['easier']['score'], a['keep_going']['score'], a['cost']['score'])
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(run, jobs))
rows = []
for k in IDEAS:
    e, g, c = (sum(r[(k, w)][i] for w in WHO) / len(WHO) for i in range(3))
    rows.append((e + g - c, e, g, c, k))
print("value = easier + keeps going - cost")
for v, e, g, c, k in sorted(rows, reverse=True): print(f"{v:5.2f}  easier {e:.2f}  keeps going {g:.2f}  cost {c:.2f}  {k}")
