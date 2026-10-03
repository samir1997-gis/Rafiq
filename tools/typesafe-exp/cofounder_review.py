# The cofounder's two branches (3 Oct): the landing-page taster (#207) and the body explorer (#202). Worth shipping?
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/cofounder_review.py
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

CTX = ("Rafiq is a phone-first web app teaching Arabic to adult beginners, mostly UK Muslims. Its hook, used in every TikTok and Instagram ad, is "
 "'understand every word of your salah'. Plans: Essentials £6.99/month, Complete £11.99/month, after a 7-day free week with no card. "
 "It already has a lot: a reading starter, 12 units, salah word by word, a practice area with words, sentences, verbs, spelling bee and "
 "'everyday essentials' (numbers, days, months, colours, time), real-life scenes and a conversation partner. Right now visitors from ads "
 "land on the home page and leave without signing up.")
F = {
 "taster_now": "On the home page, right under the 'Start your free week' button: a one-minute taster. Four everyday words (water, house, book, door, pen), each with "
   "three meanings to pick from and its audio; a wrong pick just shows the right one. It ends 'You just learned 4 Arabic words in under a minute. Imagine what "
   "you'd know in a month.' and a 'Keep the momentum going' button to the free week.",
 "taster_salah": "The same one-minute taster, but the four words are from the salah, the words the ads promise (e.g. سَمِعَ 'hears', رَبَّنا 'our Lord', "
   "اغْفِرْ 'forgive', الْعَظِيمِ 'the Magnificent'), each with where you say it. It ends 'You now know 4 words you say in every prayer' and "
   "the 'Start your free week' button.",
 "body": "Inside the app, Practise > Everyday essentials > The body: a friendly drawn figure. Tap a region (head, arm, leg, torso) to zoom in, tap a part "
   "to hear its Arabic (46 words, eye, elbow, knee, heart, lungs...). No quiz or review, just explore and listen. The Arabic is not yet checked by a teacher.",
}
WHO = {"ad": "a UK Muslim in their 20s who just arrived from a TikTok salah quiz ad",
       "trial": "a learner on day 3 of the free week, deciding whether to pay",
       "parent": "a busy parent learning to understand their salah"}
Q = {"useful":   {"type": "score", "instructions": "`ctx` Feature: `f`. Person: `who`. How useful is it to them?", "criteria": ["Not at all", "A little", "Quite", "Very"]},
     "simple":   {"type": "score", "instructions": "`ctx` Feature: `f`. Person: `who`. Does it keep the app simple and focused for them, or add clutter?", "criteria": ["Adds clutter", "A little cluttered", "Fits fine", "Makes it simpler"]},
     "value":    {"type": "score", "instructions": "`ctx` Feature: `f`. Person: `who`. How much real value does it add to Rafiq for them?", "criteria": ["None", "A little", "Quite a lot", "A lot"]},
     "subscribe":{"type": "score", "instructions": "`ctx` Feature: `f`. Person: `who`. How much does it raise the chance they start the free week and then pay?", "criteria": ["Not at all", "A little", "Quite a lot", "A lot"]}}
jobs = [(k, w) for k in F for w in WHO]
with ThreadPoolExecutor(9) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "f": F[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':14}" + "".join(f"{q:>10}" for q in Q) + "    (0-3, averaged over 3 people)")
for k in F: print(f"{k:14}" + "".join(f"{sum(r[(k, w)][q]['score'] for w in WHO) / 3:10.2f}" for q in Q))
print("\nby person, subscribe:"); [print(f"  {k:14}" + "  ".join(f"{w} {r[(k, w)]['subscribe']['score']:.2f}" for w in WHO)) for k in F]
