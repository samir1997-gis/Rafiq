# The owner: posts shouldn't all say "come to the site"; most should earn reach, likes and follows, and the
# follows bring people to the site over time. Does TypeSafe agree, what mix, and which caption for the food quiz?
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/reach_strategy.py
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

CTX = ("Rafiq is a small new web app teaching Arabic to adult beginners, mostly UK Muslims (hook: understand every word of your salah); "
       "7 days free, then from £6.99 a month. Its TikTok and Instagram have a few hundred followers. Posts so far: Arabic quizzes, root-word "
       "carousels, short teaching videos; almost every caption ends 'Learn with Rafiq, link in bio (free for a week)'. Last week about 230 site visits, "
       "4-5 sign-ups. A paid TikTok promotion brought clicks but few sign-ups.")
WHO = {"scroller": "a 22-year-old UK Muslim scrolling TikTok for fun, sees the post with no idea what Rafiq is",
       "learner": "a 34-year-old who has wanted to learn Arabic for years, follows a few Islamic accounts, cautious about apps that sell",
       "follower": "someone who already follows Rafiq and has seen five of its posts"}

# Part 1: the mix
MIX = {"M1_all_cta": "Every post ends with 'link in bio, free for a week'.",
       "M2_80_20":   "About 4 posts in 5 are pure content made for reach: a quiz or a fact, the caption asks for a comment, a share or a follow ('follow for a word a day'), no mention of the app or the link. About 1 in 5 shows the app itself and says 'free week, link in bio'.",
       "M3_none":    "No post ever mentions the app or the link; only the bio does."}
QM = {"grow": {"type": "score", "instructions": "`ctx` Posting plan: `h`. Over the next 3 months, how much will the accounts grow (reach, follows)?", "criteria": ["Barely", "A little", "Well", "Strongly"]},
      "signups": {"type": "score", "instructions": "`ctx` Posting plan: `h`. Over the next 3 months, how many sign-ups will social media bring in total?", "criteria": ["Very few", "Some", "Good", "Many"]},
      "trust": {"type": "score", "instructions": "`ctx` Posting plan: `h`. Person: `who`. After seeing several posts, how much do they like and trust the account (not just an ad)?", "criteria": ["Not at all", "A little", "Fairly", "A lot"]}}

# Part 2: the caption for the food quiz video (three food words: bread, dates, milk; three choices each; 3 seconds; then the answer)
CAP = {"C1_now": "Can you guess these 3 Arabic words? 🍞 Three everyday Arabic words, three choices each, and 3 seconds to answer ⏱️ No pressure 😅 Comment your score 👇 1, 2 or 3 out of 3? Learn the Arabic you'll actually use with Rafiq, link in bio (free for a week). #learnarabic #arabic #arabicquiz",
       "C2_reach": "3 Arabic words, 3 seconds each ⏱️ Comment your score 👇 (be honest 😅) Send it to someone who'd get 0/3 😂 Follow for a new Arabic word quiz every week. #learnarabic #arabic #arabicquiz #quiz",
       "C3_reach_bio": "3 Arabic words, 3 seconds each ⏱️ Comment your score 👇 (be honest 😅) Send it to someone who'd get 0/3 😂 Follow for more, and if you want to learn properly, there's a free week in our bio. #learnarabic #arabic #arabicquiz #quiz",
       "C4_dates": "If you don't get the dates one, we need to talk 🌴😅 3 Arabic food words, 3 seconds each. Comment your score 👇 Follow for a new Arabic quiz every week. #learnarabic #arabic #arabicquiz #ramadan"}
QC = {"comment": {"type": "score", "instructions": "`ctx` Caption on a quiz video: `h`. Person: `who`. How likely are they to comment or share it?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
      "follow": {"type": "score", "instructions": "`ctx` Caption on a quiz video: `h`. Person: `who`. How likely are they to follow the account?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
      "salesy": {"type": "score", "instructions": "`ctx` Caption on a quiz video: `h`. Person: `who`. How much does it feel like content rather than an ad?", "criteria": ["Pure ad", "Mostly ad", "Mostly content", "Pure content"]}}

def table(opts, qs, title):
    jobs = [(k, w) for k in opts for w in WHO]
    with ThreadPoolExecutor(12) as ex:
        r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": opts[j[0]], "who": WHO[j[1]]}, qs)["answers"]), jobs))
    print(f"\n{title}\n{'':14}" + "".join(f"{q:>9}" for q in qs) + "   total")
    rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / len(WHO) for q in qs}) for k in opts]
    for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:14}" + "".join(f"{s[q]:9.2f}" for q in qs) + f"   {sum(s.values()):.2f}")

table(MIX, QM, "Part 1: posting mix (0-3, averaged over three people)")
table(CAP, QC, "Part 2: caption for the food quiz")
