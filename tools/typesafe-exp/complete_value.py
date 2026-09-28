# Is Complete worth upgrading to, and where should "Your salah" sit? (issue: Complete value)
# Result (28 Sep 2026, 4 learner types, 0-3): today's Complete: choose it 1.48, worth the extra 1.66 (only the 'serious' learner
#   likely: 2.56). Salah placement: Essentials 8.95 > free 8.62 > split by content 8.38 > split by feature 8.20 > Complete only 8.07
#   (Complete-only goodwill 0.79: 'paywalling religion'). Add-ons: Juz 'Amma word by word 2.69, AI tutor 2.56, salah extras 2.55,
#   speaking 2.04, seasonal 2.02, live 1.99, certificates 1.65, family 1.59, offline 1.48. Bundles with the salah track in Essentials:
#   tutor + Pray along/drills 4.91, tutor + Juz 'Amma 4.81, Juz 'Amma 4.59, tutor + seasonal 4.49, tutor 4.29, now 4.14.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/complete_value.py
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
APP = ("Rafiq: an app teaching everyday Arabic (MSA) to UK Muslims, launching soon. Everyone gets a free week, then picks a plan. "
       "ESSENTIALS £6.99/month or £49.99/year: all 12 units and the reading starter, native audio, pictures, daily spaced review, every practice area "
       "(words, sentences, verbs, joining words, spelling bee, everyday essentials), 25 AI 'smart checks' of typed answers a day. "
       "COMPLETE £11.99/month or £79.99/year: everything in Essentials plus unlimited smart checks, a conversation partner (reply in your own "
       "words, AI feedback), real-life scenes (airport, doctor, masjid...), a weak-spots review built from your mistakes, first access to new units.")
SALAH = ("New feature 'Your salah': understand every word you say in the prayer. Most-said words first (20 words are 56% of what you say), then "
         "the prayer part by part (word by word, roots linked to everyday words, checks, rebuild the phrase, follow along), the short surahs, a map "
         "of the prayer with understood words lit up, spaced review, 'Pray along' (the whole prayer with meanings, to use before praying), and "
         "drills (meaning quiz, listening, 'your 50 most-said words' challenge). No competitor connects everyday Arabic with understanding salah.")
WHO = {"prays": "a UK Muslim adult who prays daily, wants to understand it, budget-conscious",
       "parent": "a Muslim parent, 35, busy, would pay for something meaningful",
       "revert": "a new Muslim learning the prayer",
       "serious": "a motivated learner who wants to speak Arabic and doesn't mind paying for the best tools"}
# 1. today's Complete
Q1 = {"upgrade": {"type": "score", "instructions": "`app` After the free week, how likely is `who` to choose Complete over Essentials?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
      "gap": {"type": "score", "instructions": "`app` How clearly worth the extra £5/month (£30/year) is Complete for `who`?", "criteria": ["Not worth it", "Doubtful", "Worth it", "Clearly worth it"]}}
# 2. where the salah track sits
PLACE = {
 "essentials": "Your salah is fully included in Essentials (so every paying member gets it; Complete unchanged).",
 "complete": "Your salah is only in Complete.",
 "split_features": "Split by feature: the salah track, map and review in Essentials; Pray along, the drills and the 50-most-said challenge in Complete.",
 "split_parts": "Split by content: the most-said words and the prayer itself (takbir to salam) in Essentials; the short surahs, Pray along and the drills in Complete.",
 "free": "Your salah is free for everyone forever, even without a plan (as a way in); the Arabic course needs a plan.",
}
Q2 = {"attract": {"type": "score", "instructions": "`app` `salah` Placement: `opt`. How much does this make `who` want to sign up for Rafiq at all?", "criteria": ["Not at all", "A little", "Clearly", "Strongly"]},
      "upgrade": {"type": "score", "instructions": "`app` `salah` Placement: `opt`. How likely is `who` to end up paying for Complete?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
      "goodwill": {"type": "score", "instructions": "`app` `salah` Placement: `opt`. How does `who` feel about how Rafiq charges for learning the prayer?", "criteria": ["Put off (paywalling religion)", "Uneasy", "Fine", "Positive"]},
      "pays": {"type": "score", "instructions": "`app` `salah` Placement: `opt`. How likely is `who` to pay for any plan at all after the free week?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]}}
# 3. what would make Complete worth it
ADD = {
 "salah_extras": "Pray along, salah drills and the 50-most-said challenge (the salah track itself stays in Essentials).",
 "quran_wbw": "Understand the Quran beyond salah: Juz 'Amma (the last 37 surahs) word by word, the same way as the salah track.",
 "speaking": "Speaking feedback: say your answers aloud and get pronunciation feedback on each word.",
 "tutor_chat": "An AI tutor you can ask anything ('why is it هَذِهِ here?'), answering from your own lessons and mistakes.",
 "offline": "Download lessons and audio to use offline.",
 "family": "Family sharing: up to 4 people on one Complete plan, with a parent view.",
 "live": "A monthly live group session with a teacher.",
 "certificates": "Can-do checks and certificates at each level.",
 "ramadan": "Seasonal courses: Ramadan and Hajj/Umrah Arabic.",
}
Q3 = {"worth": {"type": "score", "instructions": "`app` If Complete also had: `opt`, how much more likely is `who` to choose Complete?", "criteria": ["No more likely", "A little", "Clearly", "Much more likely"]}}
jobs = [("1", "-", w) for w in WHO] + [("2", k, w) for k in PLACE for w in WHO] + [("3", k, w) for k in ADD for w in WHO]
def run(j):
    part, k, w = j
    if part == "1": a = ask({"app": APP, "who": WHO[w]}, Q1)["answers"]; return j, {q: a[q]['score'] for q in Q1}
    if part == "2": a = ask({"app": APP, "salah": SALAH, "opt": PLACE[k], "who": WHO[w]}, Q2)["answers"]; return j, {q: a[q]['score'] for q in Q2}
    a = ask({"app": APP + " " + SALAH, "opt": ADD[k], "who": WHO[w]}, Q3)["answers"]; return j, {q: a[q]['score'] for q in Q3}
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(run, jobs))
av = lambda p, k, q, ws=WHO: sum(r[(p, k, w)][q] for w in ws) / len(ws)
print("1. TODAY'S COMPLETE (0-3)")
for w in WHO: print(f"  {w:8} choose Complete {r[('1','-',w)]['upgrade']:.2f}  worth the extra {r[('1','-',w)]['gap']:.2f}")
print(f"  average  choose Complete {av('1','-','upgrade'):.2f}  worth the extra {av('1','-','gap'):.2f}")
print("\n2. WHERE 'YOUR SALAH' SITS (value = attract + pays + upgrade + goodwill)")
for v, k in sorted(((sum(av('2', k, q) for q in Q2), k) for k in PLACE), reverse=True):
    print(f"  {v:5.2f}  attract {av('2',k,'attract'):.2f}  pays at all {av('2',k,'pays'):.2f}  upgrades {av('2',k,'upgrade'):.2f}  goodwill {av('2',k,'goodwill'):.2f}  {k}")
print("\n3. WHAT WOULD MAKE COMPLETE WORTH IT (how much more likely to choose Complete)")
for v, k in sorted(((av('3', k, 'worth'), k) for k in ADD), reverse=True): print(f"  {v:4.2f}  {k}")

# 4. Follow-up: with "Your salah" fully in Essentials, which Complete bundle gets upgrades without souring goodwill?
BUNDLE = {
 "now": "Complete as today (unlimited checks, conversation partner, real-life scenes, weak-spots review, first access to new units).",
 "tutor": "Complete as today + an AI tutor you can ask anything, answering from your own lessons and mistakes.",
 "quran": "Complete as today + understand Juz 'Amma (the last 37 surahs) word by word, like the salah track.",
 "tutor_quran": "Complete as today + the AI tutor + Juz 'Amma word by word.",
 "tutor_speaking": "Complete as today + the AI tutor + speaking feedback on your pronunciation.",
 "tutor_pray": "Complete as today + the AI tutor + Pray along and the salah drills.",
 "tutor_seasonal": "Complete as today + the AI tutor + seasonal courses (Ramadan, Hajj/Umrah Arabic).",
}
Q4 = {"upgrade": {"type": "score", "instructions": "`app` `salah` (Your salah is fully included in Essentials.) Complete now offers: `opt`. How likely is `who` to choose Complete over Essentials?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
      "goodwill": {"type": "score", "instructions": "`app` `salah` (Your salah is fully included in Essentials.) Complete now offers: `opt`. How does `who` feel about what Rafiq puts behind the higher price?", "criteria": ["Put off", "Uneasy", "Fine", "Positive"]}}
with ThreadPoolExecutor(12) as ex:
    r4 = dict(ex.map(lambda j: (j, {q: v['score'] for q, v in ask({"app": APP, "salah": SALAH, "opt": BUNDLE[j[0]], "who": WHO[j[1]]}, Q4)["answers"].items()}),
                     [(k, w) for k in BUNDLE for w in WHO]))
a4 = lambda k, q: sum(r4[(k, w)][q] for w in WHO) / len(WHO)
print("\n4. COMPLETE BUNDLES, salah in Essentials (value = upgrade + goodwill)")
for v, k in sorted(((a4(k, 'upgrade') + a4(k, 'goodwill'), k) for k in BUNDLE), reverse=True):
    print(f"  {v:4.2f}  upgrade {a4(k,'upgrade'):.2f}  goodwill {a4(k,'goodwill'):.2f}  {k}")
