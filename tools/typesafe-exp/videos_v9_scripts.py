# Check the four new video scripts (#155) line by line (true / clear / cheesy) and as a whole per viewer,
# and pick between alternatives for the weakest slots. Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/videos_v9_scripts.py
from concurrent.futures import ThreadPoolExecutor
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from videos_v9 import ask, FACTS, VIEWERS, Q, avg

SCRIPTS = {
 "v9 Your salah (25s)": ("a 25-second vertical short about learning the words of the prayer in Rafiq", "Make Muslims want to understand their salah with Rafiq and start the free week.", [
   "Imagine understanding every word of your salah.",
   "رَفِيق starts with the words you say most.",
   "Then each part of the prayer, word by word.",
   "And Pray along takes you through a whole prayer, lighting up each word as it's said.",
   "Your salah, in رَفِيق. Try it free for a week at rafiq-arabic.com.",
 ]),
 "v10 What's in Complete (30s)": ("a 30-second vertical video showing what Rafiq Complete adds over Essentials", "Make viewers want Complete, not just Essentials.", [
   "Here's what you get with رَفِيق Complete.",
   "Pray along: a whole prayer, word by word, recited by Sheikh al-Husary.",
   "Your own tutor: ask anything about Arabic, and get a clear answer built on your lessons.",
   "Get something wrong? Tap Why, and it explains.",
   "Real-life scenes: the airport, the doctor, the masjid.",
   "And a weak-spots review, built from the mistakes you keep making.",
   "Try Complete free for a week at rafiq-arabic.com.",
 ]),
 "v11 How Rafiq works (45s)": ("a 45-second vertical tutorial of how to learn Arabic with Rafiq", "A new user knows how to use Rafiq and wants to start.", [
   "Here's how to learn Arabic with رَفِيق, in five minutes a day.",
   "Open the app and press Continue. That's it.",
   "Can't read Arabic yet? You start with the letters.",
   "Then short steps: meet ten words, each one spoken by a native voice.",
   "Hear them in a real conversation, and learn one idea at a time.",
   "Then use them: build sentences, then type them.",
   "رَفِيق brings each word back just before you'd forget it.",
   "Want more? Practise has verbs, a spelling bee, and the words of your salah.",
   "Press Continue each day. Try it free for a week at rafiq-arabic.com.",
 ]),
 "v12 Meet Rafiq ad (20s)": ("a 20-second vertical ad introducing Rafiq", "Stop the scroll, show why Rafiq is different, and get a free-week sign-up.", [
   "Learnt Arabic words, then forgot them a week later?",
   "Meet رَفِيق.",
   "Short daily steps, every word fully vowelled and spoken by a native voice.",
   "And it brings each word back just before you'd forget it.",
   "Five minutes a day. Try it free for a week at rafiq-arabic.com.",
 ]),
}
QL = {"true": {"type": "noul", "instructions": "`facts` Voiceover line from a Rafiq video: `line`. Is everything this line says or implies about Rafiq true according to the facts?"},
      "clear": Q("Voiceover line in a short app video: `line`. How clear is it to a beginner hearing it once?", ["Confusing", "OK", "Clear", "Crystal clear"]),
      "cheesy": {"type": "noul", "instructions": "Voiceover line in a short app video: `line`. Does it sound cheesy, salesy or generic?"}}
QV = {"hook": Q("`facts` Video: `desc` Purpose: `purpose` Script: `script`. Viewer: `viewer`. How strongly do the first two lines make this viewer keep watching?", ["Scroll past", "Maybe", "Keep watching", "Hooked"]),
      "purpose": Q("`facts` Video: `desc` Purpose: `purpose` Script: `script`. Viewer: `viewer`. How well does it achieve its purpose for this viewer?", ["Poorly", "OK", "Well", "Very well"]),
      "try": Q("`facts` Video: `desc` Script: `script`. Viewer: `viewer`. How likely is this viewer to try Rafiq afterwards?", ["Unlikely", "Maybe", "Likely", "Very likely"]),
      "long": Q("Video: `desc` Script: `script`. Viewer: `viewer`. How does the amount of information feel?", ["Far too much", "A bit much", "About right", "Could be longer"])}

if __name__ == "__main__" and "--alts" not in sys.argv:
    with ThreadPoolExecutor(8) as ex:
        lines = [(k, l) for k, (_, _, ls) in SCRIPTS.items() for l in ls]
        rl = dict(ex.map(lambda j: (j, ask({"facts": FACTS, "line": j[1]}, QL)["answers"]), lines))
        vj = [(k, v) for k in SCRIPTS for v in VIEWERS]
        rv = dict(ex.map(lambda j: (j, ask({"facts": FACTS, "desc": SCRIPTS[j[0]][0], "purpose": SCRIPTS[j[0]][1],
            "script": " ".join(SCRIPTS[j[0]][2]), "viewer": VIEWERS[j[1]]}, QV)["answers"]), vj))
    for k, (_, _, ls) in SCRIPTS.items():
        print(f"\n===== {k}\n true  clear  cheesy  line")
        for l in ls:
            a = rl[(k, l)]; print(f" {a['true']['noul']:.2f}  {a['clear']['score']:.2f}   {a['cheesy']['noul']:.2f}    {l}")
        rs = [rv[(k, v)] for v in VIEWERS]
        print(f" whole: hook {avg(rs,'hook'):.2f}  purpose {avg(rs,'purpose'):.2f}  try {avg(rs,'try'):.2f}  length {avg(rs,'long'):.2f} (2 = about right)")

# ---- round 2: rewrites for the weak slots
ALTS = {
 "v9 line 2": ("the second line of the Your salah short, over the most-said-words drill", [
   "رَفِيق starts with the words you say most.",
   "It starts with the words you say most in every prayer.",
   "First, the twenty words you say most, again and again, every prayer.",
 ]),
 "v9 closer": ("the closing line of the Your salah short (the most-said words are free on every plan; every account gets a free week of Complete)", [
   "Your salah, in رَفِيق. Try it free for a week at rafiq-arabic.com.",
   "Start with your salah, free, at rafiq-arabic.com.",
   "Understand your salah with رَفِيق. Start free at rafiq-arabic.com.",
 ]),
 "v10 tutor": ("the AI tutor line of the What's in Complete video", [
   "Your own tutor: ask anything about Arabic, and get a clear answer built on your lessons.",
   "Your own tutor: ask anything, or tap Why after a mistake.",
   "An AI tutor: ask any question about Arabic, or tap Why when you get one wrong.",
 ]),
 "v11 opener": ("the first line of the How Rafiq works tutorial", [
   "Here's how to learn Arabic with رَفِيق, in five minutes a day.",
   "Here's how to learn Arabic with رَفِيق, a few minutes a day.",
   "How to learn Arabic with رَفِيق, one short step a day.",
 ]),
 "v11 continue": ("the line about Home in the How Rafiq works tutorial", [
   "Open the app and press Continue. That's it.",
   "Open the app and press Continue. رَفِيق picks your next step.",
   "Every day, just press Continue. رَفِيق knows what comes next.",
 ]),
 "v11 use them": ("the line about practising in the How Rafiq works tutorial", [
   "Then use them: build sentences, then type them.",
   "Then use them: put sentences together from word tiles, then type them yourself.",
   "Then make your own sentences, first with word tiles, later typing.",
 ]),
 "v11 more": ("the line about the Practise area and Your salah in the How Rafiq works tutorial", [
   "Want more? Practise has verbs, a spelling bee, and the words of your salah.",
   "Want more? Practise verbs, try the spelling bee, or learn the words of your salah.",
   "Off the path, there's a spelling bee, verb practice, and the words of your salah.",
 ]),
 "v11/v12 closer": ("the closing line of a Rafiq video (steps take 5-10 minutes; every account gets a free week)", [
   "Five minutes a day. Try it free for a week at rafiq-arabic.com.",
   "A few minutes a day. Try it free for a week at rafiq-arabic.com.",
   "Start your free week at rafiq-arabic.com.",
   "A few minutes a day, and words that stay. Start free at rafiq-arabic.com.",
 ]),
}
QA = {"good": Q("`facts` This is `slot`. Candidate line: `line`. Viewer: `viewer`. How good is it for this viewer: clear, memorable, persuasive, not cheesy?", ["Weak", "OK", "Good", "Excellent"]),
      "true": QL["true"]}
if __name__ == "__main__" and "--alts" in sys.argv:
    with ThreadPoolExecutor(8) as ex:
        jobs = [(s, l, v) for s, (_, ls) in ALTS.items() for l in ls for v in VIEWERS]
        r = dict(ex.map(lambda j: (j, ask({"facts": FACTS, "slot": ALTS[j[0]][0], "line": j[1], "viewer": VIEWERS[j[2]]}, QA)["answers"]), jobs))
    for s, (_, ls) in ALTS.items():
        print("--", s)
        for l in sorted(ls, key=lambda l: -(avg([r[(s, l, v)] for v in VIEWERS], "good") / 3 + avg([r[(s, l, v)] for v in VIEWERS], "true", "noul"))):
            rs = [r[(s, l, v)] for v in VIEWERS]
            print(f"   good {avg(rs,'good'):.2f}  true {avg(rs,'true','noul'):.2f}  {l}")
