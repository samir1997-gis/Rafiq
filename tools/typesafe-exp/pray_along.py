# Is Pray along useful? What do people think it's for, and which form and name work best? (#145)
# Result (29 Sep 2026): useful+use+khushu+clear: before_prayer 10.80, current Pray along 10.68, none 10.30,
#   self_paced 10.19, meaning_only 8.19. Differences are small; 'none' is level on usefulness and scores
#   highest on use (2.76) and khushu (2.69), so Pray along isn't seen as clearly valuable. Name: 'Pray along'
#   4.94 = 'Your prayer, word by word' 4.92 > 'Walk through your prayer' 4.49 > 'Read along' 3.94.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/pray_along.py
from concurrent.futures import ThreadPoolExecutor
import json, os, time, urllib.request
KEY = os.environ.get("TYPESAFE_API_KEY") or os.environ["TYPE_SAFE_KEY"]
def ask(state, qs):
    body = json.dumps({"state": state, "model": "jev-latest", "questions": qs}).encode()
    for a in range(5):
        try:
            r = urllib.request.Request("https://api.typesafe.ai/v1/systemone", body, {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
            with urllib.request.urlopen(r, timeout=90) as f: return json.load(f)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504, 529) and a < 4: time.sleep(2 ** a); continue
            raise
APP = ("Rafiq, an app teaching everyday Arabic to UK Muslims. Its 'Your salah' track teaches the words of the prayer part by part "
       "(listen, word by word with meanings, check, rebuild the line, follow along), with spaced review of the words. "
       "The Quran parts play a licensed human recitation; prayer phrases play a recorded voice.")
WHO = {"prays": "a UK Muslim adult who prays five times a day but understands little of the Arabic",
       "revert": "a new Muslim who learned the prayer by sound and can't read Arabic yet",
       "teen": "a 16-year-old who prays but finds it rote",
       "busy": "a busy parent with 5 minutes a day",
       "learner": "a Muslim student who has finished half the salah lessons and wants to feel the meanings while praying"}
OPT = {
 "none": "No extra mode: just the salah lessons and review.",
 "current": "'Pray along': plays the whole prayer in order (takbir to salam, with one short surah) at praying pace, audio for every line, each word lit up as it's said with its English meaning under it; moves on by itself; pause, back and 'slower' buttons.",
 "self_paced": "'Pray along', self-paced: the whole prayer in order, one line per screen in large text with each word's meaning under it; tap to hear a line, swipe for the next; no auto-advance.",
 "before_prayer": "'Before you pray': a 2-minute run through only the lines you say most (takbir, Al-Fatiha, bowing, prostration, tashahhud), meanings lit word by word with audio, meant to be opened just before praying.",
 "meaning_only": "'Meanings to hold': one screen per part of the prayer with its English meaning in large type (no word-by-word, no audio), to read and reflect before praying.",
}
Q = {"useful": {"type": "score", "instructions": "`app` Feature: `opt`. How useful is it for `who`?", "criteria": ["Not useful", "Somewhat", "Useful", "Very useful"]},
     "use": {"type": "score", "instructions": "`app` Feature: `opt`. How often would `who` actually use it?", "criteria": ["Never or once", "Now and then", "Weekly", "Most days"]},
     "khushu": {"type": "score", "instructions": "`app` Feature: `opt`. How much would it help `who` be present and understand while actually praying?", "criteria": ["Not at all", "A little", "Clearly", "Greatly"]},
     "clear": {"type": "score", "instructions": "`app` Feature: `opt`. From its name and a one-line description, how clearly would `who` understand what it's for and when to use it?", "criteria": ["Confused", "Vaguely", "Clearly", "Instantly"]}}
NAMES = {"pray_along": "Pray along", "read_along": "Read along", "walk": "Walk through your prayer",
         "before": "Before you pray", "prayer_meanings": "Your prayer, word by word"}
QN = {"clear": {"type": "score", "instructions": "`app` A mode plays the whole prayer in order with each word lit and its meaning under it. It is called '`opt`'. How clearly does the name tell `who` what it does and when to use it?", "criteria": ["Confusing", "Vague", "Clear", "Instantly clear"]},
      "appeal": {"type": "score", "instructions": "`app` A mode plays the whole prayer in order with each word lit and its meaning under it. It is called '`opt`'. How much does the name make `who` want to open it?", "criteria": ["Not at all", "A little", "Quite", "Very"]}}
jobs = [("F", k, w) for k in OPT for w in WHO] + [("N", k, w) for k in NAMES for w in WHO]
def run(j):
    kind, k, w = j
    opt, qs = (OPT[k], Q) if kind == "F" else (NAMES[k], QN)
    a = ask({"app": APP, "opt": opt, "who": WHO[w]}, qs)["answers"]
    return j, {q: a[q]['score'] for q in qs}
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(run, jobs))
avg = lambda kind, k, q: sum(r[(kind, k, w)][q] for w in WHO) / len(WHO)
print("FEATURE (value = useful + use + khushu + clear)")
for v, k in sorted(((sum(avg("F", k, q) for q in Q), k) for k in OPT), reverse=True):
    print(f"  {v:5.2f}  " + "  ".join(f"{q} {avg('F',k,q):.2f}" for q in Q) + f"  {k}")
print("  by person (useful):")
for k in OPT: print("    %-14s" % k + "  ".join(f"{w} {r[('F',k,w)]['useful']}" for w in WHO))
print("\nNAME (clear + appeal)")
for v, k in sorted(((avg("N", k, 'clear') + avg("N", k, 'appeal'), k) for k in NAMES), reverse=True):
    print(f"  {v:5.2f}  clear {avg('N',k,'clear'):.2f}  appeal {avg('N',k,'appeal'):.2f}  {NAMES[k]}")
