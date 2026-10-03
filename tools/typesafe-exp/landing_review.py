# Landing page review (4 Oct): which changes would most raise sign-ups from ad visitors? Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/landing_review.py
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

CTX = ("Rafiq teaches Arabic to adult beginners, mostly UK Muslims; every TikTok/Instagram ad is a salah quiz promising 'understand every word of your salah'. "
 "Visitors arrive on a phone. The home page, 8 phone screens long: (1) Arabic calligraphy, heading 'Learn Arabic, and understand every word of your salah', "
 "a 5-line paragraph, 'Start your free week' button, '7 days free, no card. Nothing is charged when it ends.' (2) a one-minute taster: 4 words, pick the "
 "meaning, hear it; it always starts with an everyday word (book, house, water) and has 2 prayer words second or fourth; it ends 'You just learned 4 Arabic "
 "words... including 2 you say in every prayer', 'Keep the momentum going' button. (3) a one-minute video, 4 number tiles. (4) How a day works. "
 "(5) What's inside: 8 tiles. (6) a second video. (7) Pricing: free-week box with a start link, Essentials £6.99 (only a 20-word salah taster), Complete "
 "£11.99 (all of the salah). (8) Coming next (AI tutor, 4 future units). (9) Good to know: two folded notes, one says a teacher checks the Arabic. "
 "There are no reviews or testimonials yet and nothing says who is behind Rafiq. Between the taster and Pricing (about 4 screens) there is no start button.")
FIX = {
 "A_salah_first": "The taster starts with a prayer word (e.g. سُبْحانَ, 'Glory be to', said when bowing), so the first thing an ad visitor does matches the ad.",
 "B_sticky_cta": "On phones, once the top button scrolls away, a slim bar stays at the bottom: 'Start your free week · no card'.",
 "C_same_button": "The taster's last button says 'Start your free week' (like the top one) instead of 'Keep the momentum going'.",
 "D_trust_line": "A short line near the top about who is behind Rafiq and that a teacher checks every word (moved up from the folded note at the bottom).",
 "E_shorter": "Cut the page from 8 to about 6 screens: drop 'Coming next' and the second video, fold 'How a day works' into What's inside.",
 "F_salah_essentials": "Put all of the salah into Essentials £6.99 too (today only a 20-word taster); Complete keeps the conversation partner, scenes, unlimited checks.",
 "G_testimonials": "Add 2–3 short quotes from early learners once there are real ones.",
}
Q = {"signup": {"type": "score", "instructions": "`ctx` Change: `t`. For a UK Muslim on a phone who just tapped a salah quiz ad, how much does this raise the chance they start the free week?", "criteria": ["Not at all", "A little", "Quite a lot", "A lot"]},
     "pay":    {"type": "score", "instructions": "`ctx` Change: `t`. How much does it raise the chance people go on to pay after the free week?", "criteria": ["Lowers it", "No change", "A little", "A lot"]},
     "effort": {"type": "score", "instructions": "`ctx` Change: `t`. For a developer who knows this small static site, how much work?", "criteria": ["Minutes", "An hour or two", "Half a day", "Days"]}}
with ThreadPoolExecutor(7) as ex: r = dict(ex.map(lambda k: (k, ask({"ctx": CTX, "t": FIX[k]}, Q)["answers"]), FIX))
print("change                 sign-up  pay  effort | priority (sign-up + pay/2 - effort/2)")
for k in sorted(FIX, key=lambda k: -(r[k]['signup']['score'] + r[k]['pay']['score'] / 2 - r[k]['effort']['score'] / 2)):
    s, p, e = r[k]['signup']['score'], r[k]['pay']['score'], r[k]['effort']['score']
    print(f"{k:22} {s:6.2f} {p:5.2f} {e:6.2f}  | {s + p / 2 - e / 2:.2f}")
