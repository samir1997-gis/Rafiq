# The owner's three founder hooks (#160), as written and lightly edited.
# Run: TYPE_SAFE_KEY=... python3 tools/typesafe-exp/hook_scripts.py
from concurrent.futures import ThreadPoolExecutor
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from videos_v9 import ask, Q
from social_videos import APP, VIEWER

S = {
 "1 mat":          ("on a prayer mat just after praying", "I prayed for 26 years of my life without understanding a single word in my salah. So I built this. [turns the phone to camera]"),
 "2 car, owner":   ("in a parked car", "Are you tired of reading the Quran every single day and not really understanding what you're reading? If you are, then check out Rafiq. [turns the phone to camera]"),
 "2 car, edit":    ("in a parked car", "Do you read the Quran every day without understanding what you're reading? Start with the words you say most, in your salah. This is Rafiq. [turns the phone to camera]"),
 "3 story, owner": ("on a park bench", "Do you pray every single day but still feel like you're lacking a connection to your salah? It's probably because you don't understand the words that you're saying. Try Rafiq now."),
 "3 story, edit":  ("on a park bench", "Do you pray every day but still feel something's missing? For me, it was that I didn't understand the words I was saying. This changed that. [turns the phone to camera]"),
}
QS = {"stop": Q("The first seconds of a vertical video ad for `app`: a man `where`, looking into the camera, says: `line` Viewer: `viewer`. How likely are they to keep watching?", ["Not at all", "A little", "Clearly", "Very"]),
      "real": Q("An ad for `app` opens with a man `where` saying: `line` Viewer: `viewer`. How genuine does it feel (not salesy or preachy)?", ["Not at all", "A little", "Clearly", "Very"]),
      "want": Q("An ad for `app` opens with a man `where` saying: `line` then 40s of the app. Viewer: `viewer`. How much do they want to try it?", ["Not at all", "A little", "Clearly", "A lot"]),
      "honest": {"type": "noul", "instructions": "An ad for `app` opens with: `line` Does everything it says or implies match what the app actually does?"},
      "judge": Q("An ad for `app` says: `line` Viewer: `viewer`. How likely is it to make a practising Muslim feel judged or guilt-tripped?", ["Not at all", "A little", "Clearly", "Very"])}

if __name__ == "__main__":
    with ThreadPoolExecutor(8) as ex:
        r = dict(zip(S, ex.map(lambda v: ask({"app": APP, "viewer": VIEWER, "where": v[0], "line": v[1]}, QS)["answers"], S.values())))
    print("script           stop  real  want  honest judge  total(stop+real+want-judge)")
    for k, a in r.items():
        print(f"{k:<16} {a['stop']['score']:.2f}  {a['real']['score']:.2f}  {a['want']['score']:.2f}  {a['honest']['noul']:.2f}   {a['judge']['score']:.2f}  {a['stop']['score'] + a['real']['score'] + a['want']['score'] - a['judge']['score']:.2f}")

# Results (30 Sep 2026), stop / real / want / honest / judge / total:
#   1 mat          2.89 2.70 2.87 0.73 1.01  7.45
#   2 car, owner   2.23 1.03 2.40 0.51 0.90  4.76   (feels salesy; "the Quran" oversells: the app covers salah, not the whole Quran)
#   2 car, edit    2.49 1.40 2.55 0.76 1.41  5.03
#   2 car, v3      2.72 2.60 2.75 0.83 0.42  7.65   "I used to read Quran every day and not understand... So I started with the words I say most, in my salah. This is how."
#   2 car, v4      2.79 2.18 2.71 0.78 1.04  6.64   "Twenty words make up over half of everything you say in salah..."
#   3 story, owner 2.32 1.04 2.46 0.75 1.32  4.50   (salesy, a little guilt-tripping)
#   3 story, edit  2.70 2.19 2.63 0.82 0.82  6.70   "For me, it was that I didn't understand the words I was saying. This changed that."
