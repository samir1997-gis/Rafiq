# Are the "How it works" cards clear to a complete beginner? Old wording vs the plain rewrite
# (tools/plain-grammar.json). Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/grammar_clarity.py
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
ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
notes = json.load(open(os.path.join(ROOT, 'tools/plain-grammar.json'), encoding='utf8'))['notes']
WHO = "an adult complete beginner in Arabic (a UK Muslim), with no grammar background in any language, a few minutes into the app"
Q = {"clear": {"type": "score", "instructions": "`who` sees this card in a language app: `card`. How well do they understand what it's teaching?",
               "criteria": ["Not at all", "A little", "Mostly", "Fully"]},
     "put_off": {"type": "score", "instructions": "`who` sees this card in a language app: `card`. How likely is it to make them feel Arabic is too hard for them?",
                 "criteria": ["Not at all", "A little", "Quite", "Very"]}}
def card_old(old): return f"A heading in Arabic only, then an Arabic example sentence with no translation, then: \"{old}\""
def card_new(n):  return f"Heading: \"{n['h']}\". Example with its translation: \"{n['tr']}\". Explanation: \"{n['en']}\""
jobs = [(k, v, 'old') for k, v in notes.items()] + [(k, v, 'new') for k, v in notes.items()]
def run(j):
    k, v, kind = j
    a = ask({"who": WHO, "card": card_old(k) if kind == 'old' else card_new(v)}, Q)["answers"]
    return (k, kind), (a['clear']['score'], a['put_off']['score'])
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(run, jobs))
avg = lambda kind, i: sum(r[(k, kind)][i] for k in notes) / len(notes)
print(f"old: clear {avg('old',0):.2f} · puts off {avg('old',1):.2f}")
print(f"new: clear {avg('new',0):.2f} · puts off {avg('new',1):.2f}")
worst = sorted(notes, key=lambda k: r[(k, 'new')][0] - r[(k, 'new')][1])[:6]
print("least clear after the rewrite:")
for k in worst: print(f"  {r[(k,'new')][0]:.2f} / {r[(k,'new')][1]:.2f}  {notes[k]['h']}")
