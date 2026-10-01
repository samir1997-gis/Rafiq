# How long should the free trial be: 7 days (now) or 14? (#170) With 3 and 30 for context.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/trial_length.py
from concurrent.futures import ThreadPoolExecutor
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from videos_v9 import ask, Q
APP = ("Rafiq, a phone app teaching Arabic to UK Muslims. Free forever: the meaning of the words said most in salah. Paid plan "
       "'Complete' about £80 a year (or monthly), with the full course, AI tutor, Pray along and more. No card needed for the trial; "
       "a countdown banner and reminder emails near the end; when it ends, lessons ask for a plan but progress stays visible.")
LEARNER = "a UK Muslim adult who signed up after seeing a social media ad, with 5-15 minutes a day"
DAYS = {
 3:  "a 3-day free trial: at about 2 short lessons a day they finish the reading lessons or half of 'The basics'",
 7:  "a 7-day free trial: at about 2 short lessons a day they finish 'The basics' (saying their first Arabic sentence about themselves) and start unit 1",
 14: "a 14-day free trial: at about 2 short lessons a day they finish 'The basics', all of unit 1 and its unit test, and start unit 2; reviews of their first words have come back a few times",
 30: "a 30-day free trial: at about 2 short lessons a day they finish 'The basics' and units 1-3",
}
QS = {"start": Q("App: `app` Offer: `t`. Viewer: `learner`. How likely are they to start the trial?", ["Unlikely", "Maybe", "Likely", "Very likely"]),
      "use":   Q("App: `app` Trial: `t`. Learner: `learner`. How likely are they to still be opening the app on the trial's last day?", ["Unlikely", "Maybe", "Likely", "Very likely"]),
      "pay":   Q("App: `app` Trial: `t`. Learner: `learner`. Of those who start, how likely is someone to pay when it ends?", ["Unlikely", "Maybe", "Likely", "Very likely"]),
      "keep":  Q("App: `app` Trial: `t`. Learner: `learner`. If they pay, how likely are they to still be paying three months later?", ["Unlikely", "Maybe", "Likely", "Very likely"]),
      "forget": Q("App: `app` Trial: `t`. Learner: `learner`. How likely are they to lose the habit or forget about the app before the trial ends?", ["Unlikely", "Maybe", "Likely", "Very likely"])}
if __name__ == "__main__":
    runs = [(d, t) for d, t in DAYS.items() for _ in range(3)]
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(lambda r: ask({"app": APP, "t": r[1], "learner": LEARNER}, QS)["answers"], runs))
    print("days  start  use   pay   keep  forget")
    for d in DAYS:
        a = {q: sum(x[q]["score"] for (n, _), x in zip(runs, res) if n == d) / 3 for q in QS}
        print(f"{d:>4}  {a['start']:.2f}  {a['use']:.2f}  {a['pay']:.2f}  {a['keep']:.2f}  {a['forget']:.2f}")

# Results (1 Oct 2026), averaged over 3 runs — start / still using on the last day / pay / still paying at 3 months / lose the habit first:
#    3 days            2.74 / 1.99 / 0.95 / 1.10 / 1.05
#    7 days (now)      2.81 / 2.05 / 1.10 / 1.22 / 0.96
#   14 days            2.73 / 2.07 / 1.13 / 1.24 / 0.74
#   30 days            2.72 / 1.92 / 1.07 / 1.15 / 1.17
#    7 + earned week   2.86 / 2.11 / 1.12 / 1.16 / 0.63   (a second free week for using it on 4+ of the first 7 days)
# 7 vs 14 is close to a tie on starting and paying; 14 days mainly means fewer people lose the habit before it ends.
