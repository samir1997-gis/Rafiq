# The owner's idea (#230): Rafiq as an animated character that talks to learners in videos, that the owner talks to,
# and that is the AI tutor. Which kind of character? Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/rafiq_character.py
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
CTX = ("Rafiq (Arabic for 'companion') is a calm, carefully made web app that teaches Arabic to adult beginners, mostly UK Muslims; "
       "its hook is understanding every word of your salah. The brand: warm paper background, dark ink, a verdigris green and a deep red, "
       "Karla and IBM Plex Sans Arabic type; the logo is a dark rounded square with the letter ر and a small red dot. "
       "The founder wants an animated character called Rafiq that speaks in short videos (he will sometimes talk to it on camera) "
       "and that is also the app's AI tutor, answering learners' questions.")
WHO = {"tiktok": "a 22-year-old UK Muslim who watches Islamic and language content on TikTok",
       "mum": "a 38-year-old practising Muslim mum who wants to understand her salah, careful about what her children watch",
       "revert": "a 30-year-old revert, keen to learn, a little intimidated by Arabic",
       "strict": "a 45-year-old practising Muslim who avoids pictures of faces and living beings for religious reasons",
       "student": "a 27-year-old already studying Arabic at a weekend class, wants serious, accurate teaching"}
CON = {
 "A_tile_eyes": "The logo itself comes alive: the dark rounded square with ر on it gets two simple dot eyes; it bounces, tilts, squashes and blinks; a small mouth moves when it talks.",
 "B_tile_faceless": "The logo itself comes alive but has NO face at all: the dark rounded square with ر moves with personality (bounces, leans in, nods, wobbles when thinking) and its small red dot glows and pulses in time with its voice when it speaks, like a light.",
 "C_letter_figure": "The letter ر is drawn as a little standing figure, its red dot as a round head with no facial features; it gestures with its curved body.",
 "D_human_teacher": "A friendly cartoon young British Muslim teacher with a short beard and a hoodie, a full face that lip-syncs.",
 "E_camel": "A cartoon camel called Rafiq with big friendly eyes and a smile, who talks.",
 "F_lantern": "A glowing Ramadan lantern (fanous) with two eyes and a little mouth, called Rafiq.",
}
Q = {"like":   {"type": "score", "instructions": "`ctx` The character: `h`. Viewer: `who`. How much would they like and want to see this character?", "criteria": ["Not at all", "A little", "Fairly", "A lot"]},
     "ok":     {"type": "score", "instructions": "`ctx` The character: `h`. Viewer: `who`. How comfortable are they with it religiously (no objection to how it is drawn)?", "criteria": ["Uncomfortable", "Unsure", "Fine", "Completely fine"]},
     "trust":  {"type": "score", "instructions": "`ctx` The character: `h`. Viewer: `who`. As the voice of an AI tutor answering Arabic and salah questions, how much would they trust it?", "criteria": ["Not at all", "A little", "Fairly", "A lot"]},
     "brand":  {"type": "score", "instructions": "`ctx` The character: `h`. How well does it fit this calm, crafted brand?", "criteria": ["Poorly", "OK", "Well", "Perfectly"]},
     "video":  {"type": "score", "instructions": "`ctx` The character: `h`. How well would it work on screen in short videos, including the founder talking to it?", "criteria": ["Poorly", "OK", "Well", "Very well"]}}
jobs = [(k, w) for k in CON for w in WHO]
with ThreadPoolExecutor(12) as ex:
    r = dict(ex.map(lambda j: (j, ask({"ctx": CTX, "h": CON[j[0]], "who": WHO[j[1]]}, Q)["answers"]), jobs))
print(f"{'':17}" + "".join(f"{q:>8}" for q in Q) + "  min-ok   total")
rows = []
for k in CON:
    s = {q: sum(r[(k, w)][q]["score"] for w in WHO) / len(WHO) for q in Q}
    rows.append((k, s, min(r[(k, w)]["ok"]["score"] for w in WHO)))
for k, s, m in sorted(rows, key=lambda x: -sum(x[1].values())):
    print(f"{k:17}" + "".join(f"{s[q]:8.2f}" for q in Q) + f"  {m:6}   {sum(s.values()):.2f}")
print("\nthe strict viewer, ok:", {k: r[(k, 'strict')]['ok']['score'] for k in CON})
