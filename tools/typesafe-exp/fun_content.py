# Lighter, funnier TikTok/Instagram content (5 Oct): the POV carousel's punchline, and which other fun formats to make.
# Facts: the 20 words said most are ~56% of a four-rakah prayer (salah.js); the prayer has 93 different words (salah-data.js).
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/fun_content.py
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
CTX = ("Rafiq is a web app teaching UK Muslims the Arabic of their salah. Its TikTok/Instagram has been serious (quizzes, word lessons); the owner wants "
       "lighter, funnier, meme-style posts that still feel respectful about the prayer.")
WHO = {"young": "a UK Muslim aged 18-28 scrolling TikTok who prays but doesn't understand the Arabic", "parent": "a UK Muslim parent in their 30s on Instagram",
       "devout": "a practising Muslim who dislikes jokes about worship"}
POV = "A POV photo carousel with big emoji: 'POV: you just finished praying' 🤲 / '...and you didn't understand a single word you said' 😶 / then a friend 🙋 says: "
P = {"P1_testimonial": POV + "'I've been using rafiq-arabic.com for two months, I understand 60% now.'",
     "P2_fact":        POV + "'Akhi 😭 start with the 20 words you say most. That's over half of your salah.' / 'Next salah:' سُبْحانَ رَبِّيَ الْعَظِيمِ 'wait... I KNOW what that means 🥹' / rafiq-arabic.com",
     "P3_plan":        POV + "'Your whole salah is 93 words. That's less than 2 a day for 2 months.' / 'Next salah:' 'wait... I understood that 🥹' / rafiq-arabic.com"}
QP = {"funny": {"type": "score", "instructions": "`ctx` Post: `p`. Viewer: `who`. How funny and relatable does it feel?", "criteria": ["Not at all", "A little", "Quite", "Very"]},
      "share": {"type": "score", "instructions": "`ctx` Post: `p`. Viewer: `who`. How likely are they to share it or tag a friend?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
      "believe": {"type": "score", "instructions": "`ctx` Post: `p`. Viewer: `who`. How believable and honest does the promise feel?", "criteria": ["Not at all", "A little", "Fairly", "Very"]},
      "respect": {"type": "score", "instructions": "`ctx` Post: `p`. Viewer: `who`. Is it respectful about the prayer?", "criteria": ["Disrespectful", "Borderline", "Fine", "Very respectful"]}}
I = {
 "I1_pov_salah":     "The POV carousel above: finishing salah without understanding, a friend's tip, next salah you understand a word.",
 "I2_inshallah":     "Meme carousel: 'What Arabic phrases mean vs what your mum means' (in shā' Allāh = 'probably not', yalla = 'leave NOW'), then the real meanings.",
 "I3_emoji_guess":   "Guess the Arabic word from the emoji: 🐪 = جَمَل, 🍞 = خُبْز, 🌙 = قَمَر; comment your score.",
 "I4_khutbah":       "'Me nodding along to the Arabic in the khutbah' 🙂 vs 'me after learning 20 words' 🤯, gentle self-deprecating meme.",
 "I5_imam_surah":    "'POV: the imam recites a surah you actually learned word by word' 🥹 (joy, not mocking).",
 "I6_17_times":      "'You say this 17 times a day and might not know what it means' (al-Fātiḥah in the 17 rakʿahs of the daily prayers), then its meaning.",
 "I7_day1_day60":    "'My Arabic, day 1 vs day 60' split-screen style: confused emoji vs reading a line of salah.",
 "I8_loanwords":     "'You already speak Arabic': sugar, coffee, giraffe, zero came from Arabic.",
 "I9_sibling":       "'When your younger sibling corrects your Arabic' 😤 skit carousel, ending with the word they corrected.",
 "I10_red_flag":     "'Green flags in a spouse: understands what they say in salah' meme carousel.",
}
QI = {"viral": {"type": "score", "instructions": "`ctx` Idea: `p`. Viewer: `who`. How likely are they to watch to the end, comment or share?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
      "respect": QP["respect"],
      "fit": {"type": "score", "instructions": "`ctx` Idea: `p`. How well does it lead viewers toward an app for understanding their salah?", "criteria": ["Not at all", "A little", "Quite", "Very"]}}
def run(opts, qs, title):
    jobs = [(k, w) for k in opts for w in WHO]
    with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "p": opts[j[0]], "who": WHO[j[1]]}, qs)["answers"]), jobs))
    print(f"\n{title}\n{'':16}" + "".join(f"{q:>9}" for q in qs) + "   total")
    for k in sorted(opts, key=lambda k: -sum(r[(k, w)][q]['score'] for w in WHO for q in qs)):
        s = [sum(r[(k, w)][q]['score'] for w in WHO) / 3 for q in qs]; print(f"{k:16}" + "".join(f"{x:9.2f}" for x in s) + f"   {sum(s):.2f}")
run(P, QP, "POV punchline"); run(I, QI, "Fun formats")

# Round 2: captions for the two POV carousels (brag-quiz/build_pov.py)
CAP = {
 "salah_A": ("POV carousel: finishing salah not understanding, friend's tip, next salah you know سُبْحانَ رَبِّيَ الْعَظِيمِ.",
   "Be honest… how many words of your salah do you actually understand? 👀 Tag the friend who needs this 😭\n\nStart with the 20 you say most → link in bio\n\n#salah #muslimtiktok #learnarabic #pov #muslim"),
 "salah_B": ("POV carousel: finishing salah not understanding, friend's tip, next salah you know سُبْحانَ رَبِّيَ الْعَظِيمِ.",
   "That feeling when a word in your salah finally clicks 🥹 It starts with just 20 words.\n\nrafiq-arabic.com (link in bio)\n\n#salah #muslimtiktok #learnarabic #pov"),
 "imam_A": ("POV carousel: the imam recites al-Ikhlas and you understand every word for the first time.",
   "The first time you understand the imam 🥹🤍 Which surah do you want to understand next? 👇\n\nLink in bio\n\n#salah #muslimtiktok #learnarabic #pov #quran"),
 "imam_B": ("POV carousel: the imam recites al-Ikhlas and you understand every word for the first time.",
   "Nothing hits like understanding the recitation 🥹 قُلْ هُوَ اللَّهُ أَحَدٌ, “Say: He is Allah, the One.”\n\nLearn your salah word by word → link in bio\n\n#salah #muslimtiktok #learnarabic #pov"),
}
QC = {"engage": {"type": "score", "instructions": "`ctx` `p` Viewer: `who`. How likely are they to comment, tag or share?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
      "visit": {"type": "score", "instructions": "`ctx` `p` Viewer: `who`. How likely are they to visit the link?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
      "respect": QP["respect"]}
run({k: f"Post: {v[0]} Caption: {v[1]}" for k, v in CAP.items()}, QC, "Captions")
