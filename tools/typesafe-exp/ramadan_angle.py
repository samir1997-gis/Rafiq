# Ramadan countdown content: which framing? Facts: 127 days to 8 Feb 2027 (expected); the salah from takbir to salam incl. al-Fatihah has 93
# different words (salah-data.js), ~240 with the 10 short surahs; Complete monthly from today = 4 payments of £11.99 before Ramadan = £47.96 (~38p/day).
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/ramadan_angle.py
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
CTX = ("A TikTok/Instagram post from Rafiq, a web app that teaches UK Muslims the Arabic of their salah word by word (7 days free, no card; "
       "then £11.99/month or £79.99/year for the full salah). It is October; Ramadan is about 127 days away.")
A = {
 "A_price":  "127 days to Ramadan. Start Rafiq today and it's £47.96 until Ramadan, just 38p a day, and by Ramadan you'll know every word of your salah.",
 "B_words":  "127 days to Ramadan. Your salah has 93 different words. That's less than one a day. Start today, a few minutes a day, and pray this Ramadan understanding every word you say. 7 days free.",
 "C_niyyah": "What if this Ramadan, you understood every word of your salah? 127 days. 93 words. Less than one a day. Make the intention now. Start free at rafiq-arabic.com.",
 "D_both":   "127 days to Ramadan. 93 words in your salah. Less than one word a day, about 38p a day. By Ramadan, understand every word you say. 7 days free, no card.",
}
WHO = {"young": "a UK Muslim in their 20s on TikTok who prays but doesn't understand the Arabic", "parent": "a busy Muslim parent on Instagram",
       "devout": "a practising Muslim wary of businesses using Ramadan to sell things"}
Q = {"want":    {"type": "score", "instructions": "`ctx` Post: `a`. Viewer: `who`. How much does it make them want to start now?", "criteria": ["Not at all", "A little", "Quite a lot", "A lot"]},
     "believe": {"type": "score", "instructions": "`ctx` Post: `a`. Viewer: `who`. How believable and achievable does the promise feel?", "criteria": ["Not at all", "A little", "Fairly", "Very"]},
     "respect": {"type": "score", "instructions": "`ctx` Post: `a`. Viewer: `who`. Does it feel sincere, or like cashing in on Ramadan?", "criteria": ["Cashing in", "A bit salesy", "Mostly sincere", "Sincere"]},
     "share":   {"type": "score", "instructions": "`ctx` Post: `a`. Viewer: `who`. How likely are they to save or share it?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]}}
jobs = [(k, w) for k in A for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "a": A[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total   devout-respect")
for k in sorted(A, key=lambda k: -sum(r[(k, w)][q]['score'] for w in WHO for q in Q)):
    s = [sum(r[(k, w)][q]['score'] for w in WHO) / 3 for q in Q]
    print(f"{k:10}" + "".join(f"{x:9.2f}" for x in s) + f"   {sum(s):.2f}   {r[(k,'devout')]['respect']['score']:.2f}")

# Round 2: give first, sell softly
A2 = {"B_words": A["B_words"],
 "E_series": "127 days to Ramadan. Your salah has 93 different words, less than one a day. So we'll teach you one, here, every day until Ramadan. Day 1: اللَّهُ أَكْبَرُ, “Allah is the Greatest.” Follow so you don't miss one. (Want the whole salah sooner? rafiq-arabic.com)",
 "F_soft":   "127 days to Ramadan. Your salah has 93 different words. Less than one a day. Imagine praying this Ramadan understanding every word you say. We built Rafiq to help with exactly that: a few minutes a day, word by word.",
 "G_dua":    "127 days until Ramadan, in shā’ Allāh. Your salah has 93 different words, fewer than the days left. Learn one a day and you could stand in Ramadan understanding every word. May Allah make it easy. 🤲 rafiq-arabic.com"}
jobs = [(k, w) for k in A2 for w in WHO]
with ThreadPoolExecutor(12) as ex: r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "a": A2[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print("\nRound 2"); print(f"{'':10}" + "".join(f"{q:>9}" for q in Q) + "   total   devout-respect")
for k in sorted(A2, key=lambda k: -sum(r[(k, w)][q]['score'] for w in WHO for q in Q)):
    s = [sum(r[(k, w)][q]['score'] for w in WHO) / 3 for q in Q]
    print(f"{k:10}" + "".join(f"{x:9.2f}" for x in s) + f"   {sum(s):.2f}   {r[(k,'devout')]['respect']['score']:.2f}")
