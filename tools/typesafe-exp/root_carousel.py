# The ʿ-l-m root carousel: the posted version vs a rebuild (brag-quiz/build_root.py). Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/root_carousel.py
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
CTX = "A 7-slide TikTok/Instagram photo carousel from Rafiq, an app teaching Arabic to UK Muslim beginners, about words from one Arabic root."
V = {"posted": "Cover: 'ONE ROOT · FIVE WORDS', 'All of these come from the same three letters', the letters ع · ل · م with dots between, 'What do they share?', "
               "'Swipe to find out'. Then one word per slide (عِلْم ʿilm knowledge, عالِم a scholar, مُعَلِّم a teacher, تَعْلِيم education...) under a header 'SHARED ROOT ع·ل·م 1/5'; "
               "the root letters are not highlighted. No ending slide. Location tag: Al Masjid-e-Nabawi, Medina.",
     "rebuild": "Cover: four Arabic words in cards and 'These four words share three letters. Can you spot them?'. Slide 2: 'The same three letters: ع ل م. Together "
               "they mean knowing', the same four words with those three letters coloured red inside each, plus meanings. Slides 3-6: one big word each (knowledge, "
               "a scholar, a teacher, a learner) with the root letters red and the rest dark. Last slide: 'It's in a duʿāʾ from the Quran: رَبِّ زِدْنِي عِلْمًا, My Lord, "
               "increase me in knowledge (Ta Ha 20:114)' and 'Learn the words you say · rafiq-arabic.com'. No location tag."}
WHO = {"beginner": "a UK Muslim who can't read Arabic yet, scrolling TikTok", "some": "a UK Muslim who can read Quran letters but not understand them", "parent": "a busy Muslim parent on Instagram"}
Q = {"clear": {"type": "score", "instructions": "`ctx` Carousel: `v`. Viewer: `who`. How easy is it to understand what it's showing?", "criteria": ["Confusing", "Somewhat unclear", "Clear", "Very clear"]},
     "swipe": {"type": "score", "instructions": "`ctx` Carousel: `v`. Viewer: `who`. How likely are they to swipe to the end?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "learn": {"type": "score", "instructions": "`ctx` Carousel: `v`. Viewer: `who`. How likely are they to come away understanding the root idea?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "visit": {"type": "score", "instructions": "`ctx` Carousel: `v`. Viewer: `who`. How likely are they to visit the site or follow?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "respect": {"type": "score", "instructions": "`ctx` Carousel: `v`. Viewer: `who`. How respectful and trustworthy does it feel?", "criteria": ["Not at all", "A little", "Fairly", "Very"]}}
jobs = [(k, w) for k in V for w in WHO]
with ThreadPoolExecutor(6) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "v": V[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':9}" + "".join(f"{q:>9}" for q in Q))
for k in V: print(f"{k:9}" + "".join(f"{sum(r[(k, w)][q]['score'] for w in WHO) / 3:9.2f}" for q in Q))
