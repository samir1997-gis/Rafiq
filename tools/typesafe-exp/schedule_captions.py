# The collaborator's posting schedule (Drive doc "Rafiq video titles and descriptions", 11 Oct 2026): every caption checked
# before it goes out. Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/schedule_captions.py brag-quiz/schedule-captions.json
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
import sys
from concurrent.futures import ThreadPoolExecutor
CAPS = json.load(open(sys.argv[1]))
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun", "learner": "a 34-year-old who has wanted to learn Arabic for years",
       "careful": "a knowledgeable Muslim who dislikes clickbait and mistakes about the religion or the language"}
Q = {"engage": {"type": "score", "instructions": "A reel from Rafiq, a small Arabic-learning account. Video: `v` Title: `t` Caption: `h`. Viewer: `who`. How likely are they to comment, save or share?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "spoil": {"type": "score", "instructions": "Video: `v` Caption: `h`. Does the caption give away the answer the video asks the viewer to guess?", "criteria": ["Not at all", "A little", "Mostly", "Completely"]},
     "right": {"type": "score", "instructions": "Caption: `h`. Viewer: `who`. Is everything it says about Arabic and Islam accurate and respectfully put?", "criteria": ["No", "Somewhat", "Mostly", "Yes"]}}
jobs = [(k, w) for k in CAPS for w in WHO]
def run(j):
    k, w = j; c = CAPS[k]
    return j, ask({"v": c["video"] + ". " + c["note"], "t": c["title"], "h": c["caption"], "who": WHO[w]}, Q)["answers"]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(run, jobs))
print(f"{'#':>3} {'video':34}{'engage':>8}{'spoil':>7}{'right':>7}  (careful viewer: right)")
for k in CAPS:
    s = {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}
    print(f"{k:>3} {CAPS[k]['video'][:33]:34}{s['engage']:8.2f}{s['spoil']:7.2f}{s['right']:7.2f}  ({r[(k, 'careful')]['right']['score']})")
