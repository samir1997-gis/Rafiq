# Trimming the owner's three finished ads (#195): which sections can be cut without losing the ad?
# Each ad = the owner's talking-head hook, then one of our app videos. Sections are the spoken lines with the demo after them.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/ad_trims.py
from concurrent.futures import ThreadPoolExecutor
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from videos_v9 import ask, Q, VIEWERS
ADS = {
 "A_26years": [
  ("A1", "Founder to camera: 'I spent 26 years of my life praying every single day, without understanding a single word I was saying.'"),
  ("A2", "Founder: 'That just didn't sit right with me anymore, so I decided to start learning the Arabic language, and I built this to help.'"),
  ("A3", "App: 'Imagine understanding every word of your salah. It starts with the words you say most in every prayer.' (subhana rabbiyal azim with meanings, then the most-said words list)"),
  ("A4", "App: 'Each one shows what it means, how often you say it and where it comes up in your lessons.' (the same list, scrolling)"),
  ("A5", "App: 'Then quick drills: pick the meaning, or hear a word and find it.' (a quiz being answered)"),
  ("A6", "App: 'Next, each part of the prayer, word by word, from the opening takbir to the salam.' (list of prayer parts, then the tashahhud with its meaning) - 10 seconds"),
  ("A7", "App: 'And you can watch it grow: how many of the 238 words of your salah you understand.' (a counter going up) - 10 seconds"),
  ("A8", "App: 'Then Pray along takes you through a whole prayer, lighting up each word as it's said.' (words lighting up with the recitation) - 10 seconds"),
  ("A9", "End card: 'Understand your salah with Rafiq. Start free at rafiq-arabic.com.' - 7 seconds")],
 "B_builder": [
  ("B1", "Founder to camera: 'As someone who was studying Arabic to understand the Qur'an and understand what they were saying in salah a little bit better,'"),
  ("B2", "Founder: 'I found that there were no real tools that were fit for purpose.'"),
  ("B3", "Founder, holding up his phone: 'So I decided to build this.'"),
  ("B4", "App: 'Never learnt Arabic before? Here's how Rafiq takes you from the letters to your first conversation.' (the home screen) - 7 seconds"),
  ("B5", "App: 'Every day, just press Continue. Rafiq knows what comes next.'"),
  ("B6", "App: 'Can't read Arabic yet? Start with the letters, and hear each one.' (the alphabet grid)"),
  ("B7", "App: 'Then short steps: meet ten words, each one spoken by a native voice.' (a word card, the native voice says it) - 10 seconds"),
  ("B8", "App: 'Hear them in a real conversation, and learn one idea at a time.' (a conversation line plays: as-salamu alaykum) - 10 seconds"),
  ("B9", "App: 'Then put sentences together from word tiles, and later type them.' (tiles being tapped into a sentence)"),
  ("B10", "App: 'Rafiq brings each word back just before you'd forget it.' (review gaps: 1 day, 1 week, 1 month, 4 months)"),
  ("B11", "App: 'Want more? The spelling bee: hear a word, then spell it.' (Arabic keyboard typing)"),
  ("B12", "App: 'Or learn the words of your salah, one by one.' (most-said salah words list)"),
  ("B13", "End card: 'A few minutes a day, and words that stay. Start free at rafiq-arabic.com.' - 9 seconds")],
 "C_given_up": [
  ("C1", "Founder to camera: 'Have you tried to learn the Arabic language before and given up?'"),
  ("C2", "Founder: 'Well, I don't blame you. Studying the Arabic language is very difficult.'"),
  ("C3", "Founder: 'I've been studying the Arabic language for two years now and I was really struggling until I started using this.' (holds up phone)"),
  ("C4", "App: 'Learnt Arabic words, then forgot them a week later?' (word cards blurring away)"),
  ("C5", "App: 'Meet Rafiq.' (logo)"),
  ("C6", "App: 'Short daily steps. Every word fully vowelled, and spoken by a native voice.' (word card, native voice says wa alaykum as-salam) - 9 seconds"),
  ("C7", "App: 'Learn what every word of your salah means, then pray along.' (most-said words, then Pray along reciting a'udhu billah) - 8 seconds"),
  ("C9", "App: 'And Rafiq brings each word back just before you'd forget it.' (review gaps)"),
  ("C10", "End card: 'A few minutes a day, and words that stay. Start free at rafiq-arabic.com.' - 9 seconds")],
}
CTX = "A vertical paid ad on Instagram/TikTok for Rafiq, an Arabic-learning app for UK Muslims (free week, then a plan). The whole ad, in order: "
QS = {"need": Q("Ad: `ad` Viewer: `viewer`. Think about this one part of it: `part` If this part were cut out (everything else kept), how much would the ad lose for this viewer?",
                ["Better without it (slow or repetitive)", "Loses nothing important", "Loses something useful", "Loses something essential"])}
if __name__ == "__main__":
    ex = ThreadPoolExecutor(8)
    for ad, parts in ADS.items():
        whole = CTX + " | ".join(t for _, t in parts)
        runs = [(pid, txt, v) for pid, txt in parts for v in VIEWERS for _ in range(2)]
        res = list(ex.map(lambda r: ask({"ad": whole, "viewer": VIEWERS[r[2]], "part": r[1]}, QS)["answers"]["need"]["score"], runs))
        print(ad)
        for pid, txt in parts:
            sc = [s for (p, _, _), s in zip(runs, res) if p == pid]
            print(f"  {pid:<4} {sum(sc)/len(sc):.2f}  {txt[:90]}")

# ---- whole versions: which trimmed version works best?
CUTS = {"A_26years": {"original (74s)": [], "cut A2 A4 A7 (51s)": ["A2", "A4", "A7"], "cut A2 A4 A5 A7 (43s)": ["A2", "A4", "A5", "A7"]},
        "B_builder": {"original (81s)": [], "cut B3 B8 B9 B11 (56s)": ["B3", "B8", "B9", "B11"], "cut B3 B5 B8 B9 B11 (50s)": ["B3", "B5", "B8", "B9", "B11"]},
        "C_given_up": {"original without the tutor (52s)": [], "cut C2 C5 (45s)": ["C2", "C5"], "cut C2 C3 C5 (38s)": ["C2", "C3", "C5"]}}
WQ = {"watch": Q("Viewer: `viewer`. Ad (with its length): `ad` How likely are they to watch it to the end?", ["Scroll past", "Watch a bit", "Most of it", "To the end"]),
      "try": Q("Viewer: `viewer`. Ad: `ad` How likely are they to visit the website after it?", ["Unlikely", "Maybe", "Likely", "Very likely"]),
      "flow": Q("Ad: `ad` Does it flow as a story, with nothing missing that leaves the viewer confused?", ["Confusing, something's missing", "A bit jumpy", "Flows fine", "Flows well"])}
def whole_versions():
    ex = ThreadPoolExecutor(8)
    for ad, versions in CUTS.items():
        runs = []
        for name, cut in versions.items():
            txt = CTX.replace("The whole ad", f"The whole ad ({name.split('(')[-1].rstrip(')')})") + " | ".join(t for p, t in ADS[ad] if p not in cut)
            runs += [(name, txt, v) for v in VIEWERS for _ in range(2)]
        res = list(ex.map(lambda r: ask({"ad": r[1], "viewer": VIEWERS[r[2]]}, WQ)["answers"], runs))
        print(ad)
        for name in versions:
            rs = [a for (n, _, _), a in zip(runs, res) if n == name]
            print(f"  {name:<34}" + "  ".join(f"{q} {sum(a[q]['score'] for a in rs)/len(rs):.2f}" for q in WQ))
if __name__ == "__main__" and "whole" in sys.argv: whole_versions()

# Results (2 Oct 2026), 5 viewers x 2 runs. Part scores (0 = better without it ... 3 = essential):
#   A: A1 2.05, A2 1.57, A3 2.20, A4 1.50, A5 1.70, A6 1.89, A7 1.65, A8 2.12, A9 2.44
#   B: B1 1.64, B2 1.36, B3 1.22, B4 1.88, B5 1.78, B6 1.88, B7 1.86, B8 1.73, B9 1.63, B10 2.03, B11 1.37, B12 2.10, B13 2.48
#   C: C1 1.63, C2 1.34, C3 1.55, C4 1.85, C5 1.56, C6 2.30, C7 2.57, C9 2.14, C10 2.62 (C8, the AI tutor, cut regardless: not live)
# Whole versions (watch / visit / flow): the shortest was best each time:
#   A 74s 1.99/2.08/2.83 -> 43s 2.29/2.11/2.74;  B 81s 1.79/1.96/2.88 -> 50s 2.08/1.99/2.82;  C 52s 2.17/2.12/2.80 -> 38s 2.34/2.17/2.83
# Cut (seconds in the originals): A 7.70-14.67, 23.06-36.12, 46.10-56.75 -> 43.2s;
#   B 10.85-14.23, 22.70-28.70, 43.74-60.28, 63.94-69.05 -> 49.8s;  C 4.55-15.98, 19.95-21.85, 38.92-46.85 -> 37.8s

# ---- second pass: the owner's intros stay whole; only the app parts are trimmed. And: what raises "visit the site"?
CUTS2 = {"A_26years": {"intro kept, cut A4 A5 A7 (50s)": ["A4", "A5", "A7"], "intro kept, cut A4 A5 A6 A7 (40s)": ["A4", "A5", "A6", "A7"]},
         "B_builder": {"intro kept, cut B5 B8 B9 B11 (53s)": ["B5", "B8", "B9", "B11"], "intro kept, cut B5 B6 B8 B9 B11 (48s)": ["B5", "B6", "B8", "B9", "B11"]},
         "C_given_up": {"intro kept, cut C5 (49s)": ["C5"], "intro kept, cut C4 C5 (45s)": ["C4", "C5"]}}
ENDS = {"now": "End card: 'A few minutes a day, and words that stay. Start free at rafiq-arabic.com.'",
        "offer": "End card: 'Try the full app free for 7 days, no card needed. Link in bio: rafiq-arabic.com.'",
        "founder": "The founder back on camera for 3 seconds: 'I built this for people like me. It's free for a week, link's in my bio.' then the end card with rafiq-arabic.com",
        "first_win": "End card: 'In your first week: read the letters and say your first Arabic sentence. Free, no card. rafiq-arabic.com'"}
def second_pass():
    ex = ThreadPoolExecutor(8)
    for ad, versions in CUTS2.items():
        runs = []
        for name, cut in versions.items():
            txt = CTX + " | ".join(t for p, t in ADS[ad] if p not in cut)
            runs += [(name, txt, v) for v in VIEWERS for _ in range(2)]
        res = list(ex.map(lambda r: ask({"ad": r[1], "viewer": VIEWERS[r[2]]}, WQ)["answers"], runs))
        print(ad)
        for name in versions:
            rs = [a for (n, _, _), a in zip(runs, res) if n == name]
            print(f"  {name:<38}" + "  ".join(f"{q} {sum(a[q]['score'] for a in rs)/len(rs):.2f}" for q in WQ))
    base = " | ".join(t for p, t in ADS["A_26years"] if p not in ("A4", "A5", "A7", "A9"))
    runs = [(k, CTX + base + " | " + e, v) for k, e in ENDS.items() for v in VIEWERS for _ in range(2)]
    res = list(ex.map(lambda r: ask({"ad": r[1], "viewer": VIEWERS[r[2]]}, WQ)["answers"]["try"]["score"], runs))
    print("endings (on the 26-years ad), visit the site:")
    for k in ENDS: print(f"  {k:<10} {sum(s for (n, _, _), s in zip(runs, res) if n == k)/10:.2f}")
if __name__ == "__main__" and "second" in sys.argv: second_pass()
# Second pass (owner: keep my intros whole, trim only the app parts) — watch / visit / flow:
#   A cut A4 A5 A7 (50s) 2.34/2.10/2.81  [+A6 (40s) 2.36/2.07/2.87];  B cut B5 B8 B9 B11 (53s) 2.24/2.02/2.89  [+B6 (48s) 2.25/2.02/2.86]
#   C cut C5 (+tutor) (49s) 2.31/2.13/2.77  [+C4 (45s) 2.28/2.10/2.84].  Intros kept watch as well or better than intros cut.
# Endings don't move "visit the site" (2.07-2.10 for all four): the click comes from the link/button, not the words.
# Final cuts: A 23.06-36.12, 46.10-56.75 -> 50.1s;  B 22.70-28.70, 43.74-60.28, 63.94-69.05 -> 53.2s;  C 19.95-21.85, 38.92-46.85 -> 49.2s
