# Getting learners to put Rafiq on their home screen: the #31 branch vs alternatives.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/install_prompt.py
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
CTX=("Rafiq is a web app (website) teaching Arabic to UK adult beginners, mostly on phones, about 60% iPhone. Daily use is what makes it work "
 "(spaced review, streaks). It can be added to the home screen as an app icon that opens full screen and works offline. On Android Chrome "
 "a button can trigger the browser's own install prompt; on iPhone there is no prompt, the learner must tap Safari's Share button then "
 "'Add to Home Screen' (and it must be Safari). On iPhone, notifications (daily reminders) only work once it's on the home screen.")
O={"A_card_day1":"A card on Home from the very first visit, just under today's lesson: 'Put Rafiq on your home screen'. Android: an Install button. iPhone: one line of text: 'Tap Share, then Add to Home Screen'. 'Not now' hides it for 30 days. Also a row in Settings.",
   "B_after_first_win":"The same card, but only shown after the learner finishes their first lesson, on the lesson-complete screen: 'Nice work. Keep Rafiq one tap away for tomorrow.' Then on Home from day 2 if they haven't installed.",
   "C_ios_visual":"Like A, but on iPhone the button opens a short visual guide: a picture of Safari's toolbar with an arrow at the Share button, then the 'Add to Home Screen' row; if they're in Chrome or another browser on iPhone, it says to open Rafiq in Safari first.",
   "D_reminder_framing":"Tie it to reminders: 'Want a daily reminder at your time? Add Rafiq to your home screen' offered when they set their daily goal and after the first lesson, with Android's Install button and iPhone's visual guide.",
   "E_combined":"Combine B, C and D: nothing on day one; after the first finished lesson a card framed around tomorrow's reminder and streak, with Android's Install button and iPhone's visual step-by-step guide (and 'open in Safari' when needed); 'Not now' hides it for 30 days; a Settings row always.",
   "F_store_apps":"Publish Rafiq in the App Store and Google Play (a native wrapper around the website) and show 'Get the app' store badges instead of an install card.",
   "G_settings_only":"No card at all; only an 'Install the app' row in Settings."}
PEOPLE={"iphone":"a UK beginner on an iPhone who isn't very technical","android":"a UK beginner on an Android phone","keen":"a keen learner who has done 3 lessons and wants to study every day"}
Q={"install":{"type":"score","instructions":"`ctx` Approach: `o`. Person: `who`. How likely are they to end up with Rafiq on their home screen within a week?","criteria":["Very unlikely","Unlikely","Likely","Very likely"]},
   "annoy":{"type":"score","instructions":"`ctx` Approach: `o`. Person: `who`. How annoying or confusing is it for them?","criteria":["Not at all","A little","Quite","Very"]},
   "habit":{"type":"score","instructions":"`ctx` Approach: `o`. Person: `who`. How much does it help them come back every day?","criteria":["Not at all","A little","Quite a lot","A lot"]},
   "effort":{"type":"score","instructions":"`ctx` Approach: `o`. For a small team whose web app already has the basic install card built, how much extra work is it?","criteria":["None","A day or two","A week","A month or more"]}}
jobs=[(k,w) for k in O for w in PEOPLE]
with ThreadPoolExecutor(12) as ex: r=dict(ex.map(lambda j:(j,ask({"ctx":CTX,"o":O[j[0]],"who":PEOPLE[j[1]]},Q)["answers"]),jobs))
rows=[]
for k in O:
    avg=lambda q:sum(r[(k,w)][q]['score'] for w in PEOPLE)/3
    ins,an,hb,ef=avg('install'),avg('annoy'),avg('habit'),r[(k,'iphone')]['effort']['score']
    rows.append((k,ins,r[(k,'iphone')]['install']['score'],an,hb,ef,ins+hb-an-0.5*ef))
print("approach             install(iPhone) annoy habit effort | total")
for k,i,ip,a,h,e,t in sorted(rows,key=lambda x:-x[6]): print(f"{k:20} {i:.2f} ({ip:.2f})     {a:.2f}  {h:.2f}  {e:.2f}  | {t:.2f}")
