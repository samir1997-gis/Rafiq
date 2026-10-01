# Is the salah part design the best way to learn, and should Practise get a salah area (e.g. a dictionary)?
# Result (28 Sep 2026): learn 5.91 current + most-said opener + frequency tags + Pray along, 5.35 + Pray along,
#   5.32 most-said first, 5.28 current, 5.07 one line a day, 3.27 by roots. Practise 4.59 drills, 4.40 dictionary + drills,
#   3.88 dictionary, 3.77 link only. See #124.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/salah_learning.py
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
APP = ("Rafiq, an app teaching everyday Arabic (Modern Standard) to UK Muslims. It has a 'Your salah' track: 21 parts (the prayer in order: "
       "takbir, opening supplication, Al-Fatiha, bowing, rising, prostration, tashahhud, salawat, salam; then 10 short surahs), 242 distinct words. "
       "Facts: in a normal 4-rakah prayer you say 105 different words; the 10 most frequent words are 31% of everything you say, the top 50 are 75%; "
       "10 roots cover 49%. Words also link to everyday course words with the same root (e.g. rabb, hamd, rahma).")
WHO = {"prays": "a UK Muslim adult who prays five times a day but understands little of the Arabic",
       "revert": "a new Muslim who learned the prayer by sound and can't read Arabic yet",
       "teen": "a 16-year-old who prays but finds it rote",
       "busy": "a busy parent with 5 minutes a day"}
LEARN = {
 "current": "Current design: parts in prayer order, each ~5 minutes: Listen (phrase + meaning) · Word by word (meaning, root, a course word from the same root) · Check (pick meanings) · Put it together (rebuild the line from tiles) · Follow along (words lit as it's said). Then spaced review.",
 "freq_first": "Start with a short 'Your 20 most-said words' part (45% of everything you say in salah), then the parts in prayer order as in the current design.",
 "current_prayalong": "Current design, plus a 'Pray along' mode: the whole prayer at praying pace, each word lit up with its meaning underneath, to use just before praying.",
 "current_freq_tags": "Current design, but each word shows how often you say it ('you say this 22 times in every 4-rakah prayer'), and review prioritises the most-said words.",
 "roots_first": "Organised by root families instead of prayer order (e.g. all the r-b-b words, all the h-m-d words), each family ~5 minutes.",
 "micro": "One line per day, about 2 minutes: hear it, see each word's meaning, one check. No other steps.",
 "all_three": "Current design + the 'most-said words' opener + frequency tags + a 'Pray along' mode.",
}
QL = {"understand": {"type": "score", "instructions": "`app` Design: `opt`. How well will `who` understand what they say while actually praying, a month from now?", "criteria": ["Poorly", "Somewhat", "Well", "Very well"]},
      "khushu": {"type": "score", "instructions": "`app` Design: `opt`. How much would it deepen `who`'s focus and presence in prayer (khushu')?", "criteria": ["Not at all", "A little", "Clearly", "Greatly"]},
      "keep": {"type": "score", "instructions": "`app` Design: `opt`. How likely is `who` to keep going until they've done all of it?", "criteria": ["Unlikely", "Somewhat", "Likely", "Very likely"]}}
PRAC = {
 "none": "Practise has just a 'Your salah' row that opens the salah overview (as now). No extra practice area.",
 "dictionary": "A 'Salah words' dictionary in Practise: all 242 words, searchable, sortable by how often you say them, each with meaning, root, where it appears in the prayer, audio, and everyday course words with the same root.",
 "drills": "A salah practice area in Practise: quick drills (pick the meaning, hear it and pick the word, 'your 50 most-said words' challenge) and a 'Pray along' mode.",
 "dict_drills": "Both: the 'Salah words' dictionary and the salah drills (meaning quiz, listening, 'your 50 most-said words' challenge, 'Pray along').",
}
QP = {"useful": {"type": "score", "instructions": "`app` Option: `opt`. How useful is it for `who`?", "criteria": ["Not useful", "Somewhat", "Useful", "Very useful"]},
      "return": {"type": "score", "instructions": "`app` Option: `opt`. How often would `who` come back to it?", "criteria": ["Rarely", "Now and then", "Weekly", "Most days"]},
      "clutter": {"type": "score", "instructions": "`app` Option: `opt`. How much does it clutter the app or duplicate the salah track and review?", "criteria": ["Not at all", "A little", "Noticeably", "A lot"]}}
jobs = [("L", k, w) for k in LEARN for w in WHO] + [("P", k, w) for k in PRAC for w in WHO]
def run(j):
    kind, k, w = j
    opt, Q = (LEARN[k], QL) if kind == "L" else (PRAC[k], QP)
    a = ask({"app": APP, "opt": opt, "who": WHO[w]}, Q)["answers"]
    return j, {q: a[q]['score'] for q in Q}
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(run, jobs))
avg = lambda kind, k, q: sum(r[(kind, k, w)][q] for w in WHO) / len(WHO)
print("HOW TO LEARN (value = understand + khushu + keeps going)")
for v, k in sorted(((sum(avg("L", k, q) for q in QL), k) for k in LEARN), reverse=True):
    print(f"  {v:5.2f}  understand {avg('L',k,'understand'):.2f}  khushu {avg('L',k,'khushu'):.2f}  keeps going {avg('L',k,'keep'):.2f}  {k}")
print("\nPRACTISE AREA (value = useful + comes back - clutter)")
for v, k in sorted(((avg("P", k, 'useful') + avg("P", k, 'return') - avg("P", k, 'clutter'), k) for k in PRAC), reverse=True):
    print(f"  {v:5.2f}  useful {avg('P',k,'useful'):.2f}  comes back {avg('P',k,'return'):.2f}  clutter {avg('P',k,'clutter'):.2f}  {k}")
