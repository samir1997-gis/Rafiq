# Ad visitors land on the home page and leave (#200). Does saying "no card" by the button help, which words, and which other fixes first?
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/free_week_clarity.py
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

CTX = ("Rafiq is a web app teaching Arabic to adult beginners, mostly UK Muslims; its hook is understanding every word of your salah. "
 "Every new account gets 7 days of everything free with no card; afterwards they choose a plan (from £6.99 a month) or simply stop; the free week never turns into a "
 "payment by itself. Visitors arrive on a phone from a TikTok or Instagram salah quiz video, inside the app's own browser. "
 "What they see first on the home page: Arabic calligraphy 'Your companion in learning Arabic', the heading 'Learn Arabic, and understand every word of your "
 "salah', a five-line paragraph about lessons, then the buttons. Prices (£6.99 and £11.99 a month) are further down the page.")
WHO = {"tiktok": "a 24-year-old UK Muslim who just tapped a TikTok salah quiz ad, has been stung by a free trial that charged them, scrolls fast",
       "parent": "a 38-year-old mum from Instagram who wants to understand her salah, busy, cautious about subscriptions",
       "revert": "a 30-year-old revert who found Rafiq through a friend's Instagram story, keen but unsure Arabic is for them"}

# Part 1: what sits by the button
HERO = {
 "A_now":  "Button 'Start your free week' and a 'Sign in' button beside it. Nothing else near them.",
 "B_line": "Button 'Start your free week'. Right under it, in small text: '7 days free · No card needed · Nothing to cancel'. 'Sign in' stays in the top bar only.",
 "C_btn":  "Button 'Start free, no card needed'. Under it: '7 days of everything. Then choose a plan, or just stop.' 'Sign in' in the top bar only.",
 "D_short":"As B, but the paragraph is cut to one line ('Short daily lessons from the very first letter, with audio.') so the button and the line sit higher on the screen.",
 "E_badge":"As D, plus a small pill above the heading: 'Free for 7 days · No card'.",
}
QH = {"tap":   {"type": "score", "instructions": "`ctx` What they see by the button: `h`. Person: `who`. How likely are they to tap to start?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
      "clear": {"type": "score", "instructions": "`ctx` What they see by the button: `h`. Person: `who`. Before tapping, how sure are they that starting costs nothing and needs no card?", "criteria": ["Thinks it needs a card", "Unsure", "Fairly sure", "Certain"]},
      "trust": {"type": "score", "instructions": "`ctx` What they see by the button: `h`. Person: `who`. How honest and trustworthy does it feel (not salesy)?", "criteria": ["Not at all", "A little", "Fairly", "Very"]}}

# Part 1b: the exact words of the line under the button
LINES = {"L1": "7 days free · No card needed · Nothing to cancel",
         "L2": "Free for 7 days. No card details needed.",
         "L3": "No card needed. After 7 days, you choose whether to pay.",
         "L4": "7 days free, no card. Nothing is charged when it ends.",
         "L5": "Free for 7 days. No card, nothing to cancel."}
QL = {"tap":   QH["tap"], "clear": QH["clear"],
      "plain": {"type": "score", "instructions": "`ctx` The line under the button 'Start your free week': `h`. How quick and easy is it to take in at a glance on a phone?", "criteria": ["Hard", "OK", "Easy", "Instant"]}}

# Part 2: the other leaks found, ranked
FIX = {
 "F1_signup_tab": "'Start your free week' opens the account page on the 'Sign in' tab (email + password + 'Forgot password?'); fix: open it on 'Create account'.",
 "F2_form_note":  "The create-account form never mentions the free week; fix: a line above it 'Your free week starts now. No card needed.'",
 "F3_google_inapp": "In TikTok and Instagram's own browsers Google blocks 'Continue with Google' with an 'Access blocked' error page; fix: hide that button there.",
 "F4_pricing_banner": "On the pricing section put 'Free for 7 days, no card needed' as a clear banner above the prices, not a grey sentence.",
 "F5_drop_confirm": "Today new accounts must open a confirmation email before starting (from TikTok's browser the link opens a different browser); fix: let them start straight away and confirm later.",
 "F6_ad_page": "A separate page for ad visitors that starts with the salah quiz they just saw and one button.",
}
QF = {"harm":   {"type": "score", "instructions": "`ctx` Problem and fix: `t`. If NOT fixed, how much does it stop ad visitors from starting their free week?", "criteria": ["Not at all", "A little", "Quite a lot", "A lot"]},
      "effort": {"type": "score", "instructions": "`ctx` Problem and fix: `t`. For a developer who knows this small static web app, how much work?", "criteria": ["Minutes", "An hour or two", "Half a day", "Days"]}}

def table(opts, qs, title):
    jobs = [(k, w) for k in opts for w in WHO]
    with ThreadPoolExecutor(12) as ex:
        r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": opts[j[0]], "who": WHO[j[1]]}, qs)["answers"]), jobs))
    print(f"\n{title}\n{'':10}" + "".join(f"{q:>8}" for q in qs) + "   total")
    rows = []
    for k in opts:
        s = {q: sum(r[(k, w)][q]["score"] for w in WHO) / len(WHO) for q in qs}
        rows.append((k, s, sum(s.values())))
    for k, s, t in sorted(rows, key=lambda x: -x[2]): print(f"{k:10}" + "".join(f"{s[q]:8.2f}" for q in qs) + f"   {t:.2f}")

table(HERO, QH, "Part 1: by the button (0-3 each, averaged over three visitors)")
table(LINES, QL, "Part 1b: the line under the button")
with ThreadPoolExecutor(6) as ex: rf = dict(ex.map(lambda k: (k, ask({"ctx": CTX, "t": FIX[k]}, QF)["answers"]), FIX))
print("\nPart 2: other leaks           harm  effort | priority")
for k in sorted(FIX, key=lambda k: -(rf[k]["harm"]["score"] - 0.5 * rf[k]["effort"]["score"])):
    print(f"{k:28} {rf[k]['harm']['score']:.2f}  {rf[k]['effort']['score']:.2f}   | {rf[k]['harm']['score'] - 0.5 * rf[k]['effort']['score']:.2f}")

# Round 2: the winning button with the best lines, and the note on the create-account form
FINAL = {"C": HERO["C_btn"],
         "C_L4": "Button 'Start free, no card needed'. Under it: '7 days of everything. Nothing is charged when it ends.' 'Sign in' in the top bar only.",
         "C_L5": "Button 'Start free, no card needed'. Under it: '7 days of everything. Nothing to cancel.' 'Sign in' in the top bar only.",
         "B_L4": "Button 'Start your free week'. Under it: '7 days free, no card. Nothing is charged when it ends.' 'Sign in' in the top bar only."}
table(FINAL, QH, "Round 2: final button and line")
NOTE = {"N1": "Above the create-account form: 'Your free week starts now. No card needed.'",
        "N2": "Above the create-account form: '7 days of everything, free. No card needed.'",
        "N3": "Above the create-account form: 'Free for 7 days. No card, nothing to cancel.'"}
table(NOTE, {"go": {"type": "score", "instructions": "`ctx` They tapped the button and now see the create-account form (name, email, password). `h` Person: `who`. How likely are they to fill it in?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
             "clear": QH["clear"]}, "Round 2: note on the create-account form")
