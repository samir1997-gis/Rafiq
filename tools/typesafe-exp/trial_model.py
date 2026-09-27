# How should the free week work before learners pick a plan? Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/trial_model.py
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

CTX=("Rafiq is a web app teaching Modern Standard Arabic to adult beginners (mostly UK Muslims), used mostly on phones, launching soon. "
 "Plans: Essentials £6.99/month or £49.99/year; Complete £11.99/month or £79.99/year (adds the AI conversation partner, unlimited smart answer checks, real-life scenes, weak-spots review). "
 "Payments go through Stripe. Every new account should get one free week, after which the learner picks a plan.")
O={"A_nocard_hardwall":"No card at sign-up. 7 days of everything (Complete). On day 8 the app shows only a 'pick your plan' screen until they pay.",
   "B_card_upfront":"At sign-up the learner picks a plan and enters a card in Stripe Checkout; the 7-day trial is inside Stripe and they're charged automatically on day 8 unless they cancel.",
   "C_nocard_nudges":"No card at sign-up. 7 days of everything (Complete), a banner counting down the days, a reminder email on day 5 and on the last day. On day 8 lessons ask them to pick a plan, but their progress, streak and word list stay visible so nothing feels lost.",
   "D_nocard_freemium":"No card at sign-up. 7 days of everything, then a small free level forever (reading starter and reviews of words already learned); new lessons need a plan.",
   "E_choose_day1_nocard":"At sign-up they choose Essentials or Complete for their free week (no card); on day 8 they pay for that plan to continue."}
PEOPLE={"beginner":"a UK Muslim adult beginner who found Rafiq through their masjid's WhatsApp group, cautious about subscriptions",
        "keen":"a motivated learner who studied every day of the free week",
        "parent":"a busy parent who tried two lessons and then forgot about it"}
Q={"convert":{"type":"score","instructions":"`ctx` Trial design: `o`. Person: `who`. How likely is this person to end up paying?","criteria":["Very unlikely","Unlikely","Likely","Very likely"]},
   "trust":{"type":"score","instructions":"`ctx` Trial design: `o`. Person: `who`. How fair and trustworthy does it feel to them?","criteria":["Not at all","A little","Fair","Very fair"]},
   "friction":{"type":"score","instructions":"`ctx` Trial design: `o`. Person: `who`. How much does it put them off starting at all?","criteria":["Not at all","A little","Quite a lot","A lot"]},
   "complaints":{"type":"score","instructions":"`ctx` Trial design: `o`. How likely are refund requests, chargebacks or angry emails?","criteria":["Very unlikely","Unlikely","Likely","Very likely"]}}
jobs=[(k,w) for k in O for w in PEOPLE]
with ThreadPoolExecutor(12) as ex: r=dict(ex.map(lambda j:(j,ask({"ctx":CTX,"o":O[j[0]],"who":PEOPLE[j[1]]},Q)["answers"]),jobs))
rows=[]
for k in O:
    avg=lambda q:sum(r[(k,w)][q]['score'] for w in PEOPLE)/3
    c,t,f,cp=avg('convert'),avg('trust'),avg('friction'),avg('complaints')
    rows.append((k,c,t,f,cp,2*c+t-f-cp))
print("design                 convert trust friction complaints | total")
for k,c,t,f,cp,tot in sorted(rows,key=lambda x:-x[5]): print(f"{k:22} {c:.2f}    {t:.2f}  {f:.2f}     {cp:.2f}      | {tot:.2f}")
