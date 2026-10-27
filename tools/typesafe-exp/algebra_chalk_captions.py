# Captions for the silent algebra reel (27 Oct 2026, #299) and the chalkboard ad (#295).
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/algebra_chalk_captions.py
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
WHO = {"scroller": "a 22-year-old UK Muslim scrolling for fun", "learner": "a 34-year-old who has wanted to learn Arabic for years",
       "parent": "a 41-year-old Muslim parent who prays but doesn't understand the Arabic"}
TAGS = "#learnarabic #arabic #islamichistory #muslim #salah"
REELS = {
 "algebra": ("A silent 60-second Reel from Rafiq, a small account teaching the Arabic Muslims use: no voice, typed text and animated graphics. "
             "'Algebra is an Arabic word': al-jabr means setting a broken bone; al-Khwārizmī wrote the book in Baghdad 1,200 years ago; his "
             "x² + 10x = 39 solved by completing the square; Latin turned al-jabr into algebra, and in Spain a bone-setter was an algebrista; "
             "'Your turn': between the two sajdahs Muslims say wajburnī, 'and mend me' (Tirmidhī 284). Ends: rafiq-arabic.com, 'Did you know? Tell me in the comments.'", {
  "A_story": f"Algebra is an Arabic word 🦴 al-jabr: setting a broken bone. Al-Khwārizmī wrote the book in Baghdad 1,200 years ago, and you still say the word in every salah: wajburnī, “and mend me”. Did you know? 👇 {TAGS}",
  "B_teacher": f"Your maths teacher never told you this 👀 “Algebra” comes from al-jabr, Arabic for setting a broken bone. And between the two sajdahs you ask Allah for the same thing: wajburnī, mend me 🤲 Save it for your next salah 📌 {TAGS}",
  "C_short": f"From a broken bone to algebra to your salah 🦴📐🤲 Did you know this one? 👇 {TAGS}",
  "D_salah": f"The word you dreaded in maths is in your salah 🤲 al-jabr → algebra → wajburnī, “mend me”, between the two sajdahs. Which part did you already know? 👇 {TAGS}"}),
 "chalk": ("A 60-second chalkboard-animation ad from Rafiq, an app for learning the Arabic of salah and the Qur'an (voiceover): '10 minutes a day is all it "
           "takes to start understanding your salah. Most courses start with grammar; Rafiq starts with the words you already say. Week one: the 20 words "
           "you say most in salah, more than half of every four-rakʿah prayer before the surah. Every word with audio and a picture, coming back just "
           "before you'd forget it. Then every word of your salah, ten short surahs, 785 words in 36 conversations. Free for 7 days, no card.' "
           "Ends: 'Which part of your salah do you want to understand first? Tell me in the comments.'", {
  "A_ten": f"10 minutes a day to start understanding your salah 🤲 Rafiq starts with the 20 words you say most: more than half of every 4-rakʿah prayer. Free for 7 days, no card, link in bio. Which part of your salah do you want to understand first? 👇 #learnarabic #arabic #salah #muslim #quranarabic",
  "B_years": f"“Arabic takes years” — only if you start with grammar 📚 Rafiq starts with the words you already say in salah. 10 minutes a day, free for 7 days, no card. Link in bio. What do you want to understand first? 👇 #learnarabic #arabic #salah #muslim #quranarabic",
  "C_week1": f"Week 1: the 20 words you say most in salah ✨ That's more than half of every 4-rakʿah prayer before the surah. 10 minutes a day with Rafiq, free for a week, no card (link in bio). Which part do you want to understand first? 👇 #learnarabic #arabic #salah #muslim #quranarabic",
  "D_short": f"10 minutes a day. That's all it takes to start understanding your salah 🤲 Try Rafiq free for 7 days, no card. Link in bio. Which part do you want to understand first? 👇 #learnarabic #arabic #salah #muslim #quranarabic"}),
}
Q = {"engage": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to save, share or comment?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "follow": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to follow the account?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "try": {"type": "score", "instructions": "`ctx` Caption: `h`. Viewer: `who`. How likely are they to visit the site and try Rafiq?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]}}
for reel, (ctx, caps) in REELS.items():
    jobs = [(k, w) for k in caps for w in WHO]
    with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": ctx, "h": caps[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
    print(f"\n{reel:10}" + "".join(f"{q:>9}" for q in Q) + "   total")
    rows = [(k, {q: sum(r[(k, w)][q]["score"] for w in WHO) / 3 for q in Q}) for k in caps]
    for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(f"{k:10}" + "".join(f"{s[q]:9.2f}" for q in Q) + f"   {sum(s.values()):.2f}")
