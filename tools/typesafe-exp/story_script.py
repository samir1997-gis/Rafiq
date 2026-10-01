# The owner's founder story video (#160): as written, tightened, and aimed at one audience.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/story_script.py
from concurrent.futures import ThreadPoolExecutor
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from videos_v9 import ask, Q
from social_videos import APP

VIEWERS = {"teacher": "a UK Muslim aged 18-40 who studies Arabic with a teacher or at a class once or twice a week and keeps forgetting earlier lessons",
           "new": "a UK Muslim aged 18-40 who has never studied Arabic, prays daily, and wants to understand their salah",
           "any": "a UK Muslim aged 18-40 scrolling Instagram Reels or YouTube Shorts"}
OWNER = ("Two years ago, I decided that it was about time for me to learn Arabic so that I could connect better with my religion, understand the Quran, "
 "understand what I was saying in my salah, and be able to communicate in the language that Islam was sent down upon the Prophet, sallallahu alayhi wa sallam. "
 "So I started studying Arabic with a teacher. And at first it was going really, really well. But about a year in, I started to realise as I was advancing, "
 "I was forgetting the things I learned in the earlier lessons. Now this is obviously because lessons only happen once or twice a week. But what do you do in "
 "between that time? That's why we built Rafiq. For those of you who are studying Arabic with a teacher and find yourselves forgetting, Rafiq is the perfect tool "
 "to support you because it's excellent as a revision tool. And it brings back words that you've already learned and makes them stick in your mind. Or if you're "
 "someone who's just trying to start out learning Arabic, again, Rafiq can be the perfect tool for you because it starts from the very, very basics in teaching you the letters of the Arabic language.")
TIGHT = ("Two years ago, I decided it was time to learn Arabic. To understand what I say in my salah, to understand the Quran, in the language it was revealed in "
 "to the Prophet, sallallahu alayhi wa sallam. So I started studying with a teacher, and at first it went really well. But about a year in, I noticed something. "
 "The further I got, the more I was forgetting my early lessons. A lesson once or twice a week isn't the problem. It's what happens in between. "
 "That's why we built Rafiq. It brings back the words you've learned just before you'd forget them, so they stick. If you study with a teacher, it's your "
 "revision between lessons. And if you're just starting out, it begins with the letters.")
TEACHER = TIGHT.rsplit(" And if you're just starting out", 1)[0]
NEW = ("Two years ago, I decided it was time to learn Arabic. To understand what I say in my salah, to understand the Quran. I started with a teacher, and it went "
 "really well, until I realised I was forgetting my early lessons. So we built Rafiq: short daily lessons that start from the letters, and bring every word back "
 "just before you'd forget it.")
SCRIPTS = {"owner": OWNER, "tight": TIGHT, "teacher-only": TEACHER, "starter-only": NEW}
QS = {"watch": Q("A founder talks to camera, sitting down, in a short vertical video about `app`. What he says: `s` Viewer: `viewer`. How likely are they to watch to the end?", ["Not at all", "A little", "Clearly", "Very"]),
      "real":  Q("A founder talks to camera about `app`: `s` Viewer: `viewer`. How genuine and relatable does it feel (not salesy)?", ["Not at all", "A little", "Clearly", "Very"]),
      "want":  Q("A founder talks to camera about `app`: `s` Viewer: `viewer`. How much does it make them want to try the app?", ["Not at all", "A little", "Clearly", "A lot"]),
      "honest": {"type": "noul", "instructions": "A founder says about `app`: `s` Does everything he says about the app match what it actually does?"}}

if __name__ == "__main__":
    jobs = [(s, v) for s in SCRIPTS for v in VIEWERS]
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(lambda j: ask({"app": APP, "s": SCRIPTS[j[0]], "viewer": VIEWERS[j[1]]}, QS)["answers"], jobs))
    print("script         words  viewer   watch  real  want  honest  total")
    for (s, v), a in zip(jobs, res):
        print(f"{s:<14} {len(SCRIPTS[s].split()):>4}   {v:<8} {a['watch']['score']:.2f}  {a['real']['score']:.2f}  {a['want']['score']:.2f}  {a['honest']['noul']:.2f}   {a['watch']['score'] + a['real']['score'] + a['want']['score']:.2f}")

# Results (30 Sep 2026), watch + real + want, by viewer (teacher / new / any):
#   owner (207 words)       7.87 / 6.85 / 6.69
#   tight (128 words)       8.35 / 8.25 / 7.47   <- best overall
#   teacher-only (117)      8.32 / 8.13 / 7.54
#   starter-only (64)       8.12 / 8.30 / 7.58
# Claims, with the app fully described: "brings back the words you've learned just before you'd forget them" 0.86,
#   "begins with the letters" 0.95, "it's your revision between lessons" 0.35 (misleading: Rafiq reviews its own course,
#   not what a teacher taught). Honest replacement: "If you study with a teacher, use Rafiq on the days in between, so
#   you're practising Arabic every day, not once a week." 0.85.
