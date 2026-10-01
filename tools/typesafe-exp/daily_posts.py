# What to post day to day on Instagram and TikTok (#161): post types scored for this audience, and how often.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/daily_posts.py
from concurrent.futures import ThreadPoolExecutor
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from videos_v9 import ask, Q
from social_videos import APP, VIEWER

POSTS = {
 "salah-word":   "one word from salah a day: the Arabic, what it means, how many times you say it in a prayer (a 15-20s animated clip or a carousel, no face)",
 "phrase-face":  "the founder teaching one salah phrase word by word to camera, 30-45s",
 "grammar-bite": "one small Arabic grammar point with a common mistake crossed out (e.g. 'this house' vs 'this is a house'), a carousel",
 "quiz":         "a quick quiz post: an Arabic word or phrase with 3 options, 'answer in the comments', answer revealed the next day",
 "root":         "one Arabic root and the words it makes, linking a salah word to everyday words (e.g. s-b-h: subhan, swimming)",
 "everyday":     "one everyday phrase Muslims already say (insha'Allah, masha'Allah, jazakAllah) and what each word really means",
 "demo-clip":    "a 15s clip of one app feature working (Pray along, the tutor answering, the spelling bee)",
 "progress":     "the founder's own learning progress or a learner's streak and milestone, weekly",
 "behind":       "behind the scenes of building the app: the teacher checking the Arabic, a new feature, launch countdown",
 "reply":        "a video reply to a comment or question from a follower ('someone asked what tashahhud means')",
 "reflection":   "a short reflection on the meaning of a salah line and how knowing it changes your prayer (respectful, no preaching)",
}
QS = {"value":   Q("A regular social media post from `app`: `p`. Viewer: `viewer`. How much value do they get from it on its own, even if they never download the app?", ["None", "A little", "Clearly", "A lot"]),
      "follow":  Q("A regular post from `app`: `p`. Viewer: `viewer`. How likely are they to follow the account to see more of these?", ["Not at all", "A little", "Clearly", "Very"]),
      "share":   Q("A regular post from `app`: `p`. Viewer: `viewer`. How likely are they to share or save it?", ["Not at all", "A little", "Clearly", "Very"]),
      "install": Q("A regular post from `app`: `p`. Viewer: `viewer`. How much does it make them want to try the app?", ["Not at all", "A little", "Clearly", "A lot"]),
      "easy":    Q("A small team (one founder, a part-time Arabic teacher) that already has an app full of teacher-checked content (word lists, grammar cards, the salah word by word) makes this post: `p`. How easy is it to keep making one every week for a year?", ["Very hard", "Hard", "Easy", "Very easy"])}
FREQ = {
 "7/week, mostly templated": "a new post every day, most of them quick templated posts from the app's content, one founder video a week",
 "7/week, all face":         "a new face-to-camera founder video every day",
 "4/week":                   "four good posts a week, one of them a founder video",
 "2/week":                   "two polished posts a week",
}
QF = {"grow": Q("A new Instagram/TikTok account for `app`, run by one founder alongside the app, posts `f`. Over 6 months, how well does the account grow?", ["Badly", "Slowly", "Well", "Very well"]),
      "last": Q("A founder running an app alone posts `f`. How likely are they to keep it up for 6 months without burning out or the quality dropping?", ["Unlikely", "Maybe", "Likely", "Very likely"])}

if __name__ == "__main__":
    with ThreadPoolExecutor(8) as ex:
        rp = dict(zip(POSTS, ex.map(lambda p: ask({"app": APP, "viewer": VIEWER, "p": p}, QS)["answers"], POSTS.values())))
        rf = dict(zip(FREQ, ex.map(lambda f: ask({"app": APP, "f": f}, QF)["answers"], FREQ.values())))
    ks = list(QS)
    print("post           " + "  ".join(f"{k:>7}" for k in ks) + "   total")
    for k, a in sorted(rp.items(), key=lambda x: -sum(x[1][q]["score"] for q in ks)):
        print(f"{k:<14} " + "  ".join(f"{a[q]['score']:7.2f}" for q in ks) + f"   {sum(a[q]['score'] for q in ks):.2f}")
    print("\nhow often                   grow  last")
    for k, a in rf.items():
        print(f"{k:<27} {a['grow']['score']:.2f}  {a['last']['score']:.2f}")

# Results (30 Sep 2026), value + follow + share + install + easy:
#   everyday phrase 11.82 · founder teaches a salah phrase 11.51 · reflection 11.33 · salah word of the day 11.30
#   · reply to a comment 10.96 · root 10.94 · feature clip 9.23 · quiz 9.02 · grammar bite 7.90 · progress 6.65 · behind the scenes 6.41
# How often (6 months: grow / keep it up): 4 a week 1.58/0.81 · daily all face 1.45/0.03 · 2 a week 1.30/0.91 · daily templated 1.09/1.24
