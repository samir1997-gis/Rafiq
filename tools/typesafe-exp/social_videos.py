# Social media and ads (#159): which kinds of video to make for Rafiq, as organic posts and as paid ads.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/social_videos.py
from concurrent.futures import ThreadPoolExecutor
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from videos_v9 import ask, Q

APP = ("Rafiq, a phone app (launching 10 Oct 2026) that teaches Modern Standard Arabic to UK Muslims, with a free section "
       "that teaches the meaning of every word you say in salah (prayer), an AI tutor, Pray along, and short daily lessons. "
       "Paid plan (Complete) about £80 a year after a free week.")
VIEWER = "a UK Muslim aged 18-40 scrolling Instagram Reels, TikTok or YouTube Shorts, who prays but doesn't understand most of the Arabic they say"

FORMATS = {
    "demo":      "a 45-60s vertical video of the real app working on a phone screen, with a warm female voiceover and captions (what we have now)",
    "founder":   "the founder talking straight to camera for 45-60s about why they built Rafiq: praying for years without understanding the words",
    "street":    "street interviews: the founder asks Muslims outside a UK masjid or on the high street 'what does subhana rabbiyal azeem mean?', then shows the answer in the app",
    "lesson":    "the founder teaching one phrase from salah per video to camera, word by word, 30-45s, ending with 'there's more in Rafiq'",
    "challenge": "the founder (or a friend who knows no Arabic) doing a '30 days to understand my salah' challenge on camera, posting progress every few days",
    "reaction":  "a real learner's reaction the first time they pray and understand every word, filmed talking to camera afterwards",
    "split":     "the founder's face in a corner talking over a screen recording of the app, showing one feature (green-screen style), 30-45s",
    "skit":      "a short comedy skit about relatable moments (the imam's long surah, not knowing what you're saying, aunties) that ends on the app",
    "journey":   "behind-the-scenes build-in-public posts: the founder showing what they built this week, the teacher checking the Arabic, launch countdown",
}
QS = {
    "stop":   Q("A video for `app`. The video: `f`. Viewer: `viewer`. How likely are they to stop scrolling and watch the first 3 seconds?", ["Not at all", "A little", "Clearly", "Very"]),
    "trust":  Q("A video for `app`. The video: `f`. Viewer: `viewer`. How much does it make them trust the app and the people behind it?", ["Not at all", "A little", "Clearly", "A lot"]),
    "want":   Q("A video for `app`. The video: `f`. Viewer: `viewer`. How much does it make them want to download the app and try it?", ["Not at all", "A little", "Clearly", "A lot"]),
    "pay":    Q("A video for `app`. The video: `f`. Viewer: `viewer`. How much does it make them willing to pay for the full plan after the free week?", ["Not at all", "A little", "Clearly", "A lot"]),
    "share":  Q("A video for `app`. The video: `f`. Viewer: `viewer`. How likely are they to share it or send it to a friend or family member?", ["Not at all", "A little", "Clearly", "Very"]),
    "ad":     Q("The same video run as a paid ad on Instagram/TikTok: `f`, for `app`, shown to `viewer`. How well does it work as a paid ad (people click through and install)?", ["Badly", "OK", "Well", "Very well"]),
    "risk":   Q("A video for `app`: `f`. Shown to `viewer`. How likely is it to feel disrespectful, embarrassing to someone in it, or to put off religious viewers?", ["Not at all", "A little", "Clearly", "Very"]),
}
HOOKS = {
    "a": "\"I prayed for 15 years without understanding a single word I was saying.\"",
    "b": "\"Do you know what you're actually saying in sujood?\"",
    "c": "\"Why I spent a year building an Arabic app for UK Muslims.\"",
    "d": "\"20 words make up over half of your salah. Here's the first one.\"",
    "e": "\"Struggling to learn Arabic? Meet Rafiq.\"",
}
QH = {"stop": Q("The first line of a short vertical video for `app`: `h`. Viewer: `viewer`. How likely are they to keep watching?", ["Not at all", "A little", "Clearly", "Very"])}

if __name__ == "__main__":
    with ThreadPoolExecutor(8) as ex:
        rf = dict(zip(FORMATS, ex.map(lambda f: ask({"app": APP, "viewer": VIEWER, "f": f}, QS)["answers"], FORMATS.values())))
        rh = dict(zip(HOOKS, ex.map(lambda h: ask({"app": APP, "viewer": VIEWER, "h": h}, QH)["answers"], HOOKS.values())))
    keys = list(QS)
    score = lambda a: sum(a[k]["score"] for k in keys if k != "risk") - a["risk"]["score"]
    print("format     " + "  ".join(f"{k:>5}" for k in keys) + "  total")
    for f, a in sorted(rf.items(), key=lambda x: -score(x[1])):
        print(f"{f:<10} " + "  ".join(f"{a[k]['score']:5.2f}" for k in keys) + f"  {score(a):5.2f}")
    print("\nhook  stop")
    for h, a in sorted(rh.items(), key=lambda x: -x[1]["stop"]["score"]):
        print(f"{h}     {a['stop']['score']:.2f}  {HOOKS[h]}")

# Results (30 Sep 2026), total = stop+trust+want+pay+share+ad-risk:
#   reaction 15.9 · hook+demo 14.5 (founder's face 5s, then the app) · founder 12.7 · lesson 12.0 · street-kind 12.0
#   challenge 11.1 · street 10.8 (risk 1.31) · skit 10.6 · demo 10.4 · beta-reaction (friends) 10.1 · split 8.6 · journey 7.7
# Hooks: "I prayed for 15 years without understanding..." 2.85 · "20 words make up over half..." 2.78
#   · "Do you know what you're saying in sujood?" 2.76 · "Why I spent a year building..." 2.12 · "Meet Rafiq" 1.86
