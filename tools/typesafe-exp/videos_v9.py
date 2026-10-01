# Which new marketing videos to make (#155): the slate, the format, and the hooks.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/videos_v9.py
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

FACTS = ("TRUE FACTS ABOUT RAFIQ (launching 10 Oct 2026): a web app (rafiq-arabic.com) that installs to the phone's home screen. "
 "Teaches Modern Standard Arabic to adult beginners, mostly UK Muslims. Every account gets a free week of Complete, no card. "
 "Plans: Essentials £6.99/month (the whole course, all practice, audio and review) and Complete £11.99/month. "
 "The course: a reading starter (the 28 letters in 7 shape families, the vowel marks, a listening test), then 12 units (greetings, family, housing, daily life, food, prayer, study, work, shopping, weather, people & places, hobbies), "
 "each in 5-10 minute steps: meet 10 words, hear a conversation, one grammar idea, practise, have the conversation, say it yourself. Everything fully vowelled with a native Arabic voice. "
 "Reviews are scheduled by FSRS, a memory model that learns how well you remember each word and brings it back before you'd forget. "
 "AI checks typed Arabic and names the mistake (e.g. masculine/feminine). "
 "NEW, 'Your salah': learn the words of the prayer. The most-said words of the prayer first (free on every plan), then each part of the prayer word by word (takbir, Al-Fatiha, ruku, sujud, tashahhud, and short surahs), with drills. "
 "'Pray along' (Complete): go through a whole prayer line by line; Quran verses are recited by Sheikh al-Husary (licensed from the Quran Foundation) with each word lighting up as it's said, the official Saheeh International translation, then a pause to repeat. "
 "NEW, the AI tutor (Complete): a Tutor tab where you ask anything about Arabic or your lessons and get a short, clear answer built on the course; and a 'Why?' button after a wrong answer that explains the mistake. It gives no religious rulings. "
 "Complete also has: real-life scenes (airport, doctor, masjid, restaurant, taxi, family visit), the weak-spots review from your repeated mistakes, unlimited AI checking, the conversation partner. "
 "Practise area on every plan: spelling bee, 21 common verbs, joining words, redo a unit. No music anywhere (halal-conscious).")
VIEWERS = {
 "muslim": "a UK Muslim adult who prays in Arabic every day, wants to understand what they're saying, and has quit Arabic apps before",
 "revert": "a new Muslim who can't read Arabic script yet and feels behind",
 "parent": "a busy Muslim parent who wants to learn so they can help their children",
 "student": "someone at an Arabic class or madrasa who wants help revising between lessons",
 "general": "a busy adult curious about learning Arabic, scrolling Reels/TikTok",
}
Q = lambda i, c: {"type": "score", "instructions": i, "criteria": c}

# ---- 1. which videos
CONCEPTS = {
 "hook_ad": "a 20-second vertical ad: 'Struggling to learn Arabic? Meet Rafiq.' The problem, then Rafiq's answer in three quick app shots, then the free week.",
 "understand_salah": "a 25-second vertical short about Your salah: 'You pray five times a day. Do you know what you're saying?' Shows the prayer's words lighting up with meanings, and Pray along.",
 "tutor": "a 20-second vertical short about the AI tutor: someone asks 'Why is it هَذِهِ and not هَذا?' and gets a clear answer; then 'Why?' after a wrong answer.",
 "complete_tour": "a 30-second vertical 'What's in Complete' video: Pray along, the AI tutor, real-life scenes, the weak-spots review, unlimited AI checking, with the price and free week.",
 "section_series": "a series of five 15-second vertical shorts, one per section: reading starter, lessons, Your salah, Practise, AI tutor.",
 "tutorial_start": "a 45-second vertical tutorial: 'How to learn Arabic with Rafiq in 5 minutes a day': open, press Continue, what a step looks like, review, practise.",
 "tutorial_prayalong": "a 40-second vertical tutorial of Pray along: pick a surah, listen, repeat, words light up, meanings.",
 "reading_starter": "a 20-second vertical short for people who can't read Arabic yet: 'Can't read Arabic? Start here.' The letters in 7 families, words with the letter in red, a native voice.",
}
QC = {
 "watch": Q("`facts` Video idea: `video`. Viewer: `viewer`. Seeing this in their feed, how likely are they to watch to the end?", ["Scroll past", "A few seconds", "Most of it", "To the end"]),
 "try": Q("`facts` Video idea: `video`. Viewer: `viewer`. How likely are they to try Rafiq afterwards?", ["Unlikely", "Maybe", "Likely", "Very likely"]),
 "pay": Q("`facts` Video idea: `video`. Viewer: `viewer`. How much does it make them want to pay for Complete rather than stay on the free week or Essentials?", ["Not at all", "A little", "Somewhat", "A lot"]),
 "clear": Q("`facts` Video idea: `video`. Viewer: `viewer`. How clearly would they understand what Rafiq is and does?", ["Confused", "Vague", "Clear", "Crystal clear"]),
 "respect": {"type": "noul", "instructions": "`facts` Video idea: `video`. Would a practising Muslim find anything about it disrespectful or inappropriate?"},
}

# ---- 2. hooks for the problem ad and the salah short
HOOKS = {
 "hook_ad": ("the first line (first 2 seconds) of a 20-second vertical ad for Rafiq", [
   "Struggling to learn Arabic? Meet Rafiq.",
   "Tried to learn Arabic and given up? You're not the only one.",
   "You've started learning Arabic three times. This time, it sticks.",
   "Arabic apps teach you words. Rafiq helps you keep them.",
   "What if learning Arabic took five minutes a day?",
 ]),
 "understand_salah": ("the first line of a 25-second vertical short about learning the words of the prayer", [
   "You pray five times a day. Do you know what you're saying?",
   "Imagine understanding every word of your salah.",
   "Seventeen rakahs a day. How many words do you understand?",
   "Your salah, word by word, finally in your language.",
 ]),
 "tutor": ("the first line of a 20-second vertical short about Rafiq's AI tutor", [
   "Ever wished you could ask your Arabic teacher anything, any time?",
   "Why هَذِهِ and not هَذا? Just ask.",
   "Got it wrong? Rafiq tells you why.",
   "An Arabic tutor in your pocket, built on your lessons.",
 ]),
}
QH = {
 "good": Q("`facts` This is `slot`. Candidate line: `line`. Viewer: `viewer`. How strongly does it make them stop scrolling and keep watching?", ["Scroll past", "Maybe", "Keep watching", "Hooked"]),
 "cheesy": {"type": "noul", "instructions": "Opening line of a short app video: `line`. Does it sound cheesy, salesy or generic?"},
 "true": {"type": "noul", "instructions": "`facts` Line from a Rafiq video: `line`. Is everything it says or implies about Rafiq true according to the facts?"},
}

# ---- 3. format and length
FORMATS = {
 "vertical_20": "vertical 9:16, about 20 seconds, voiceover plus captions",
 "vertical_45": "vertical 9:16, about 45 seconds, voiceover plus captions",
 "landscape_60": "landscape 16:9, about 60 seconds, for YouTube and the website",
}
QF = {"fit": Q("`facts` Rafiq's marketing video to post on Instagram Reels, TikTok and YouTube Shorts. Format: `fmt`. Viewer: `viewer`. How well does this format suit reaching them?", ["Poorly", "OK", "Well", "Very well"])}

def avg(rs, k, key="score"): return sum(r[k][key] for r in rs) / len(rs)

if __name__ == "__main__":
    with ThreadPoolExecutor(8) as ex:
        jobs = [(c, v) for c in CONCEPTS for v in VIEWERS]
        rc = dict(ex.map(lambda j: (j, ask({"facts": FACTS, "video": CONCEPTS[j[0]], "viewer": VIEWERS[j[1]]}, QC)["answers"]), jobs))
        hj = [(s, l, v) for s, (_, ls) in HOOKS.items() for l in ls for v in VIEWERS]
        rh = dict(ex.map(lambda j: (j, ask({"facts": FACTS, "slot": HOOKS[j[0]][0], "line": j[1], "viewer": VIEWERS[j[2]]}, QH)["answers"]), hj))
        fj = [(f, v) for f in FORMATS for v in VIEWERS]
        rf = dict(ex.map(lambda j: (j, ask({"facts": FACTS, "fmt": FORMATS[j[0]], "viewer": VIEWERS[j[1]]}, QF)["answers"]), fj))

    print("=== 1. video ideas (0-3, averaged over viewers; respect = chance it offends)")
    print(f"{'idea':20} watch  try   pay   clear respect   best viewer")
    rows = []
    for c in CONCEPTS:
        rs = [rc[(c, v)] for v in VIEWERS]
        best = max(VIEWERS, key=lambda v: rc[(c, v)]["try"]["score"])
        rows.append((avg(rs, "watch") + avg(rs, "try") + avg(rs, "pay") / 2, c, rs, best))
    for tot, c, rs, best in sorted(rows, reverse=True):
        print(f"{c:20} {avg(rs,'watch'):.2f}  {avg(rs,'try'):.2f}  {avg(rs,'pay'):.2f}  {avg(rs,'clear'):.2f}  {avg(rs,'respect','noul'):.2f}    {best}")
    print("\nper viewer, try:")
    print(f"{'idea':20}" + "".join(f"{v:>9}" for v in VIEWERS))
    for c in CONCEPTS: print(f"{c:20}" + "".join(f"{rc[(c, v)]['try']['score']:9.2f}" for v in VIEWERS))

    print("\n=== 2. hooks (hook strength 0-3; cheesy and true are probabilities)")
    for s, (_, ls) in HOOKS.items():
        print("--", s)
        for l in sorted(ls, key=lambda l: -avg([rh[(s, l, v)] for v in VIEWERS], "good")):
            rs = [rh[(s, l, v)] for v in VIEWERS]
            print(f"   {avg(rs,'good'):.2f}  cheesy {avg(rs,'cheesy','noul'):.2f}  true {avg(rs,'true','noul'):.2f}  {l}")

    print("\n=== 3. format")
    for f in FORMATS:
        print(f"   {avg([rf[(f, v)] for v in VIEWERS],'fit'):.2f}  {FORMATS[f]}")

# ---- round 2: the "Meet Rafiq" ad's opening, in the owner's spirit ("Struggling to learn Arabic? Meet Rafiq")
HOOKS2 = ("the first line (first 2 seconds) of a 20-second vertical ad for Rafiq", [
 "Struggling to learn Arabic? Meet Rafiq.",
 "Struggling to remember the Arabic you learn?",
 "Learnt Arabic words, then forgot them a week later?",
 "Struggling with Arabic? Try five minutes a day.",
 "What if learning Arabic took five minutes a day?",
 "Struggling to learn Arabic on your own? Meet Rafiq, your companion.",
])
if __name__ == "__main__":
    with ThreadPoolExecutor(8) as ex:
        j2 = [(l, v) for l in HOOKS2[1] for v in VIEWERS]
        r2 = dict(ex.map(lambda j: (j, ask({"facts": FACTS, "slot": HOOKS2[0], "line": j[0], "viewer": VIEWERS[j[1]]}, QH)["answers"]), j2))
    print("\n=== round 2: the Meet Rafiq ad's hook")
    for l in sorted(HOOKS2[1], key=lambda l: -avg([r2[(l, v)] for v in VIEWERS], "good")):
        rs = [r2[(l, v)] for v in VIEWERS]
        print(f"   {avg(rs,'good'):.2f}  cheesy {avg(rs,'cheesy','noul'):.2f}  true {avg(rs,'true','noul'):.2f}  {l}")
