# Second cut of the four videos (#155): slower, more features shown working, Sara's voice.
# Checks each line (true / clear / cheesy) and each whole video (hook, purpose, try, pace, features).
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/videos_v13_scripts.py [--alts]
from concurrent.futures import ThreadPoolExecutor
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from videos_v9 import ask, FACTS as F9, VIEWERS, Q, avg

FACTS = F9 + (" ALSO TRUE: in 'Say this in Arabic' you build the sentence from word tiles in units 1-3, tiles plus a wrong piece in 4-6, and type it from unit 7. "
 "The spelling bee plays a word from your lessons; you type it on an Arabic keyboard and it's checked. "
 "Your salah shows, for each of the most-said words, its meaning, how many times you say it in a four-rakah prayer, its root, and the words from your course that share it; "
 "its drills are Pick the meaning and Hear it, pick the word; its parts go from the opening takbir to the closing salam, then the short surahs; "
 "the salah page counts how many of the 238 words of your salah you understand. "
 "Real-life scenes: the other person speaks first, you reply in your own words, and the AI gives feedback on your Arabic. "
 "The weak-spots review builds a session from the mistakes you keep making.")

# how each video is paced: a demo of the feature working, shown live, for about 3-7 seconds after each line
PACE = "Each line is followed by a pause of about a second and a half while the app is shown working live on a phone (tapping, typing, words lighting up)."
SCRIPTS = {
 "v12 Meet Rafiq (about 38s)": ("a vertical ad introducing Rafiq, about 38 seconds", "Stop the scroll, show why Rafiq is different, and get a free-week sign-up.", [
   "Learnt Arabic words, then forgot them a week later?",
   "Meet رَفِيق.",
   "Short daily steps. Every word fully vowelled, and spoken by a native voice.",
   "Learn what every word of your salah means, then pray along.",
   "Stuck on something? Ask your tutor, any time.",
   "And رَفِيق brings each word back just before you'd forget it.",
   "A few minutes a day, and words that stay. Start free at rafiq-arabic.com.",
 ]),
 "v9 Your salah (about 55s)": ("a vertical video about learning the words of the prayer in Rafiq, about 55 seconds", "Make Muslims want to understand their salah with Rafiq and start the free week.", [
   "Imagine understanding every word of your salah.",
   "رَفِيق starts with the words you say most.",
   "Each one shows what it means, how often you say it, and where it comes up in your lessons.",
   "Then quick drills: pick the meaning, or hear a word and find it.",
   "Next, each part of the prayer, word by word, from the opening takbir to the salam.",
   "And you can watch it grow: how many of the 238 words of your salah you understand.",
   "Then Pray along takes you through a whole prayer, lighting up each word as it's said.",
   "Understand your salah with رَفِيق. Start free at rafiq-arabic.com.",
 ]),
 "v10 What's in Complete (about 50s)": ("a vertical video showing what Rafiq Complete adds over Essentials, about 50 seconds", "Make viewers want Complete, not just Essentials.", [
   "Here's what you get with رَفِيق Complete.",
   "Pray along: a whole prayer, word by word, each word lighting up as it's said.",
   "Your own tutor: ask anything about Arabic, and get a clear answer built on your lessons.",
   "Get something wrong? Tap Why, and it explains.",
   "Real-life scenes: reply in your own words at the masjid, the doctor or the airport, and get feedback.",
   "And a weak-spots review, built from the mistakes you keep making.",
   "Try Complete free for a week at rafiq-arabic.com.",
 ]),
 "v11 How Rafiq works (about 65s)": ("a vertical tutorial of how to learn Arabic with Rafiq, about 65 seconds", "A new user knows how to use Rafiq and wants to start.", [
   "Here's how to learn Arabic with رَفِيق, a few minutes a day.",
   "Every day, just press Continue. رَفِيق knows what comes next.",
   "Can't read Arabic yet? Start with the letters, and hear each one.",
   "Then short steps: meet ten words, each one spoken by a native voice.",
   "Hear them in a real conversation, and learn one idea at a time.",
   "Then put sentences together from word tiles, and later type them.",
   "رَفِيق brings each word back just before you'd forget it.",
   "Want more? The spelling bee: hear a word, then spell it.",
   "Or learn the words of your salah, one by one.",
   "A few minutes a day, and words that stay. Start free at rafiq-arabic.com.",
 ]),
}
QL = {"true": {"type": "noul", "instructions": "`facts` Voiceover line from a Rafiq video: `line`. Is everything this line says or implies about Rafiq true according to the facts?"},
      "clear": Q("Voiceover line in a short app video: `line`. How clear is it to a beginner hearing it once?", ["Confusing", "OK", "Clear", "Crystal clear"]),
      "cheesy": {"type": "noul", "instructions": "Voiceover line in a short app video: `line`. Does it sound cheesy, salesy or generic?"}}
QV = {"hook": Q("`facts` Video: `desc` Purpose: `purpose` Script: `script`. Viewer: `viewer`. How strongly do the first two lines make this viewer keep watching?", ["Scroll past", "Maybe", "Keep watching", "Hooked"]),
      "purpose": Q("`facts` Video: `desc` Purpose: `purpose` Script: `script`. `pace` Viewer: `viewer`. How well does it achieve its purpose for this viewer?", ["Poorly", "OK", "Well", "Very well"]),
      "try": Q("`facts` Video: `desc` Script: `script`. `pace` Viewer: `viewer`. How likely is this viewer to try Rafiq afterwards?", ["Unlikely", "Maybe", "Likely", "Very likely"]),
      "pace": Q("Video: `desc` Script: `script`. `pace` Viewer: `viewer`. How does the pace feel?", ["Far too fast", "A bit fast", "About right", "Too slow"]),
      "features": Q("`facts` Video: `desc` Script: `script`. `pace` Viewer: `viewer`. How well does it show what Rafiq actually does, feature by feature?", ["Barely", "Some", "Well", "Very well"]),
      "long": Q("Video: `desc` Script: `script`. `pace` Viewer: `viewer`. How does the length feel?", ["Far too long", "A bit long", "About right", "Could be longer"])}

if __name__ == "__main__" and "--alts" not in sys.argv:
    with ThreadPoolExecutor(8) as ex:
        lines = [(k, l) for k, (_, _, ls) in SCRIPTS.items() for l in ls]
        rl = dict(ex.map(lambda j: (j, ask({"facts": FACTS, "line": j[1]}, QL)["answers"]), lines))
        vj = [(k, v) for k in SCRIPTS for v in VIEWERS]
        rv = dict(ex.map(lambda j: (j, ask({"facts": FACTS, "desc": SCRIPTS[j[0]][0], "purpose": SCRIPTS[j[0]][1], "pace": PACE,
            "script": " ".join(SCRIPTS[j[0]][2]), "viewer": VIEWERS[j[1]]}, QV)["answers"]), vj))
    for k, (_, _, ls) in SCRIPTS.items():
        print(f"\n===== {k}\n true  clear  cheesy  line")
        for l in ls:
            a = rl[(k, l)]; print(f" {a['true']['noul']:.2f}  {a['clear']['score']:.2f}   {a['cheesy']['noul']:.2f}    {l}")
        rs = [rv[(k, v)] for v in VIEWERS]
        print(f" whole: hook {avg(rs,'hook'):.2f}  purpose {avg(rs,'purpose'):.2f}  try {avg(rs,'try'):.2f}  pace {avg(rs,'pace'):.2f} (2 = right)  features {avg(rs,'features'):.2f}  length {avg(rs,'long'):.2f} (2 = right)")

ALTS = {
 "ad tutor": ("the AI tutor line in a Rafiq ad (the tutor is in Complete, 20 questions a day)", [
   "Stuck on something? Ask your tutor, any time.",
   "Stuck? Ask your tutor, and get a clear answer built on your lessons.",
   "Stuck on a word or a rule? Just ask your tutor.",
 ]),
 "salah 2": ("the second line of the Your salah video, over the most-said-words list", [
   "رَفِيق starts with the words you say most.",
   "It starts with the words you say most in every prayer.",
   "First, the words you say most, in every rakah.",
 ]),
 "salah 3": ("the third line of the Your salah video, over one word's card", [
   "Each one shows what it means, how often you say it, and where it comes up in your lessons.",
   "For each word: its meaning, how many times you say it, and the words from your lessons that share its root.",
   "See what each word means, how often you say it, and which words you already know that share its root.",
 ]),
 "tutorial hook": ("the first line of a tutorial video about how Rafiq works", [
   "Here's how to learn Arabic with رَفِيق, a few minutes a day.",
   "From the Arabic letters to your first conversation: here's how رَفِيق works.",
   "Never learnt Arabic before? Here's how رَفِيق takes you from the letters to your first conversation.",
 ]),
 "tutorial continue": ("the line about Home in the tutorial", [
   "Every day, just press Continue. رَفِيق knows what comes next.",
   "Each day, press Continue on Home, and pick up right where you left off.",
   "One button on Home, Continue, takes you to your next step.",
 ]),
 "closer": ("the closing line of a Rafiq video (steps take 5-10 minutes; every account gets a free week)", [
   "A few minutes a day, and words that stay. Start free at rafiq-arabic.com.",
   "A few minutes a day. Start your free week at rafiq-arabic.com.",
   "Start your free week at rafiq-arabic.com.",
 ]),
}
QA = {"good": Q("`facts` This is `slot`. Candidate line: `line`. Viewer: `viewer`. How good is it for this viewer: clear, memorable, persuasive, not cheesy?", ["Weak", "OK", "Good", "Excellent"]),
      "true": QL["true"], "clear": QL["clear"]}
if __name__ == "__main__" and "--alts" in sys.argv:
    with ThreadPoolExecutor(8) as ex:
        jobs = [(s, l, v) for s, (_, ls) in ALTS.items() for l in ls for v in VIEWERS]
        r = dict(ex.map(lambda j: (j, ask({"facts": FACTS, "slot": ALTS[j[0]][0], "line": j[1], "viewer": VIEWERS[j[2]]}, QA)["answers"]), jobs))
    for s, (_, ls) in ALTS.items():
        print("--", s)
        for l in ls:
            rs = [r[(s, l, v)] for v in VIEWERS]
            print(f"   good {avg(rs,'good'):.2f}  true {avg(rs,'true','noul'):.2f}  clear {avg(rs,'clear'):.2f}  {l}")
