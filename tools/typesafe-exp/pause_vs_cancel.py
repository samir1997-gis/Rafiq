# Monthly subscribers who press Cancel: offer a pause? (#72)
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/pause_vs_cancel.py [1|2]   (round 1 by default)
from concurrent.futures import ThreadPoolExecutor
import json, os, sys, time, urllib.request
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
CTX=("Rafiq is a subscription web app teaching Arabic to UK adult beginners (mostly Muslims): £6.99 or £11.99 a month, or yearly. "
 "In Settings, a monthly subscriber presses 'Cancel subscription'. Today it asks them to confirm, and the plan runs to the end of the month already paid for.")
ROUND1={"cancel_only":"Just confirm the cancellation, as now.",
   "pause_equal":"Show two equal choices side by side: 'Pause for 1 or 2 months' (no charge, progress kept, it restarts automatically with an email 3 days before) or 'Cancel'. One tap either way.",
   "pause_first":"Show the pause offer first; the cancel button appears only after they decline the pause.",
   "discount":"Offer 50% off the next 2 months instead of cancelling, with cancel still one tap away.",
   "pause_plus_reason":"Ask one optional question (why are you leaving?) then show pause and cancel as equal choices, tailored: 'busy/Ramadan/exams' highlights pause, 'too expensive' mentions the yearly plan."}
# Round 1: cancel_only 2.54, pause_equal 2.08, pause_plus_reason 2.00, discount 1.76, pause_first -0.19
ROUND2={"cancel_only":"Just confirm the cancellation, as now.",
   "cancel_with_pause_link":"The confirm screen keeps 'Cancel my plan' as the main button, with a small line under it: 'Just need a break? Pause for a month instead.' Nothing else changes.",
   "pause_no_autocharge":"Show 'Cancel' and 'Pause for 1 month' as equal choices. A pause doesn't charge again by itself: a week before it ends we email asking if they want to restart, and if they don't reply it simply ends, like a cancel.",
   "pause_email_before":"Show 'Cancel' and 'Pause for 1 or 2 months' as equal choices. The plan restarts automatically after the pause, with an email 7 days before that has a one-tap cancel link."}
# Round 2: cancel_only 2.52, pause_email_before 1.80, cancel_with_pause_link 1.64, pause_no_autocharge 1.10
O = ROUND2 if sys.argv[1:] == ['2'] else ROUND1
PEOPLE={"busy":"a learner who is busy for a month (exams, travel, Ramadan) and plans to come back",
        "done":"a learner who has decided Rafiq isn't for them",
        "money":"a learner who is short of money this month"}
Q={"stay":{"type":"score","instructions":"`ctx` Proposal: `o`. Person: `who`. How likely is this person to still be paying in three months?","criteria":["Very unlikely","Unlikely","Likely","Very likely"]},
   "trust":{"type":"score","instructions":"`ctx` Proposal: `o`. Person: `who`. How fair and respectful does it feel to them?","criteria":["Manipulative","Slightly pushy","Fair","Very fair"]},
   "risk":{"type":"score","instructions":"`ctx` Proposal: `o`. How likely is it to draw complaints, bad reviews, or trouble under UK consumer rules that cancelling must be easy?","criteria":["Very unlikely","Unlikely","Likely","Very likely"]}}
jobs=[(k,w) for k in O for w in PEOPLE]
with ThreadPoolExecutor(12) as ex: r=dict(ex.map(lambda j:(j,ask({"ctx":CTX,"o":O[j[0]],"who":PEOPLE[j[1]]},Q)["answers"]),jobs))
rows=[]
for k in O:
    avg=lambda q:sum(r[(k,w)][q]['score'] for w in PEOPLE)/3
    s,t,k2=avg('stay'),avg('trust'),avg('risk'); rows.append((k,s,t,k2,2*s+t-k2))
print("option                 stay  trust risk | total")
for k,s,t,k2,tot in sorted(rows,key=lambda x:-x[4]): print(f"{k:22} {s:.2f}  {t:.2f}  {k2:.2f} | {tot:.2f}")
