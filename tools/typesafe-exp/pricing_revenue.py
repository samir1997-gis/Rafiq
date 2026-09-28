# Salah in Essentials or Complete, judged on revenue; and are the prices right? (#125)
# Result (28 Sep 2026; 5 learner types; revenue per 100 people finishing the free week, monthly prices):
#   Salah in Complete £531 (pay 52%, Complete 60%, feel 2.00) · taster in Essentials, rest in Complete £523 (pay 54%, 50%, 1.90)
#   · whole track in Essentials £478 (pay 51%, 43%, 1.52).
#   Prices: pay rate barely moved with price (50-52%) and fairness stayed 2.31-2.43, so revenue simply rose with price
#   (£379 at £4.99/£9.99 ... £636 at £9.99/£14.99). The model isn't sensitive to price here: don't read it as 'charge more'.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/pricing_revenue.py
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
BASE = ("Rafiq, an app teaching everyday Arabic (MSA) to UK Muslims, after a free week. The course: 12 units + reading starter, native audio, "
        "pictures, spaced review, practice areas (words, sentences, verbs, spelling bee, everyday essentials), AI-checked answers. "
        "'Your salah' (unique; no other app does it): understand every word said in the prayer, most-said words first, part by part with roots "
        "linked to everyday words, a map of the prayer, review, 'Pray along' and salah drills. Complete also has: unlimited AI checks, a "
        "conversation partner, real-life scenes, a weak-spots review, an AI tutor you can ask anything, first access to new units.")
PLAN = {
 "salah_ess": "ESSENTIALS £6.99/month: the course + the whole salah track (Pray along and salah drills are Complete). COMPLETE £11.99/month: everything, incl. the AI tutor, Pray along, salah drills.",
 "salah_comp": "ESSENTIALS £6.99/month: the course only. COMPLETE £11.99/month: the course + the whole 'Your salah' + the AI tutor and the rest; marketed as 'Rafiq Complete: learn Arabic and understand your salah'.",
 "salah_taster": "ESSENTIALS £6.99/month: the course + the salah 'most-said words' (20 words, over half of what you say in the prayer). COMPLETE £11.99/month: the rest of 'Your salah' (every part of the prayer, surahs, map, Pray along, drills) + the AI tutor and the rest.",
}
WHO = {"prays": "a UK Muslim adult who prays daily, wants to understand it, budget-conscious",
       "parent": "a Muslim parent, 35, busy, would pay for something meaningful",
       "revert": "a new Muslim learning the prayer",
       "serious": "a motivated learner who wants to speak Arabic, happy to pay for the best",
       "student": "a Muslim university student, 20, tight budget"}
PAY = ["Under 10%", "10-30%", "30-60%", "Over 60%"]; MID = [0.05, 0.2, 0.45, 0.75]
Q = {"pays": {"type": "score", "instructions": "`base` Plans: `plan`. After the free week, how likely is `who` to pay for a plan at all?", "criteria": PAY},
     "complete": {"type": "score", "instructions": "`base` Plans: `plan`. If `who` pays, how likely are they to pick Complete rather than Essentials?", "criteria": PAY},
     "feel": {"type": "score", "instructions": "`base` Plans: `plan`. How does `who` feel about the way the plans are split?", "criteria": ["Put off", "Uneasy", "Fine", "Positive"]}}
def p(score): # 0-3 score -> probability, linear between bucket midpoints
    i = min(2, int(score)); f = score - i; return MID[i] + (MID[i+1] - MID[i]) * f
def revenue(pays, comp, e=6.99, c=11.99): return 100 * pays * (comp * c + (1 - comp) * e)
jobs = [(k, w) for k in PLAN for w in WHO]
with ThreadPoolExecutor(12) as ex:
    r = dict(ex.map(lambda j: (j, {q: v['score'] for q, v in ask({"base": BASE, "plan": PLAN[j[0]], "who": WHO[j[1]]}, Q)["answers"].items()}), jobs))
print("1. WHERE SALAH SITS: per 100 people finishing the free week, per month (average over 5 learner types)")
for k in PLAN:
    pays = sum(p(r[(k, w)]['pays']) for w in WHO) / len(WHO); comp = sum(p(r[(k, w)]['complete']) for w in WHO) / len(WHO)
    feel = sum(r[(k, w)]['feel'] for w in WHO) / len(WHO)
    rev = sum(revenue(p(r[(k, w)]['pays']), p(r[(k, w)]['complete'])) for w in WHO) / len(WHO)
    print(f"  £{rev:6.0f}/month  pay {pays:.0%}  pick Complete {comp:.0%}  feel {feel:.2f}  {k}")

# 2. Price points (salah track in Essentials, tutor + extras in Complete)
PRICES = [(4.99, 9.99), (5.99, 9.99), (6.99, 11.99), (7.99, 12.99), (7.99, 14.99), (9.99, 14.99)]
Q2 = {"pays": {"type": "score", "instructions": "`base` Plans: `plan`. After the free week, how likely is `who` to pay for a plan at all?", "criteria": PAY},
      "complete": {"type": "score", "instructions": "`base` Plans: `plan`. If `who` pays, how likely are they to pick Complete?", "criteria": PAY},
      "fair": {"type": "score", "instructions": "`base` Plans: `plan`. How fair does `who` find these prices for what they get?", "criteria": ["Too expensive", "A bit much", "Fair", "Good value"]}}
def plan2(e, c): return (f"ESSENTIALS £{e}/month (about £{round(e*7.2)}/year paid yearly): the course + the whole salah track. COMPLETE £{c}/month "
                          f"(about £{round(c*6.7)}/year): everything, incl. the AI tutor, Pray along and salah drills.")
jobs2 = [(pr, w) for pr in PRICES for w in WHO]
with ThreadPoolExecutor(12) as ex:
    r2 = dict(ex.map(lambda j: (j, {q: v['score'] for q, v in ask({"base": BASE, "plan": plan2(*j[0]), "who": WHO[j[1]]}, Q2)["answers"].items()}), jobs2))
print("\n2. PRICE POINTS: per 100 people finishing the free week, per month (monthly prices; yearly behaves similarly)")
for pr in PRICES:
    rev = sum(revenue(p(r2[(pr, w)]['pays']), p(r2[(pr, w)]['complete']), *pr) for w in WHO) / len(WHO)
    pays = sum(p(r2[(pr, w)]['pays']) for w in WHO) / len(WHO); comp = sum(p(r2[(pr, w)]['complete']) for w in WHO) / len(WHO)
    fair = sum(r2[(pr, w)]['fair'] for w in WHO) / len(WHO)
    print(f"  £{rev:6.0f}/month  pay {pays:.0%}  pick Complete {comp:.0%}  fair {fair:.2f}  Essentials £{pr[0]} / Complete £{pr[1]}")
