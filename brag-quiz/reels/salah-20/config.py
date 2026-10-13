"""The 20-words salah reel (owner, 12 Oct 2026): the template's config.json, filled in from the transcript.
Silences cut (owner, 13 Oct) except the pause before "your salah"; the times below are the take's own, mapped through the cut.
  python3 config.py /tmp/reel-salah      (after `reel.py <W> plan`; then zoom, masks, layers, mix, then build.py)"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from timemap import loader
W = sys.argv[1]; C = json.load(open(os.path.join(W, "config.json"))); m = loader(W)

C["flicks"] = []                                      # the flicker hook is its own clip, joined in front by build.py
C["title_top"] = 540                                  # at head height, so his head covers part of the word (owner, 13 Oct)
C["titles"] = [                                       # behind the head, one per beat where his face is on screen (the graphics carry the rest)
    [0.0, 7.3, "", "PICTURE THIS", 175], [16.0, 20.8, "THE DAY OF", "JUDGEMENT", 185],
    [46.9, 49.3, "ARE YOU", "CONTENT?", 230], [51.7, 60.2, "IF THE ANSWER IS", "NO", 330],
    [61.2, 66.6, "TRY TO", "UNDERSTAND", 175], [91.0, 101.2, "TO ACTUALLY", "CONNECT", 220], [108.1, 111.7, "IS ARABIC", "DIFFICULT?", 185],
    [111.8, 115.9, "IS LEARNING", "20 WORDS?", 210], [116.1, 118.7, "", "NOT AT ALL", 200], [120.6, 124.3, "START WITH", "20 WORDS", 210],
    [124.7, 129.2, "YOU WILL", "FEEL IT", 260], [142.1, 145.6, "DROP A", "COMMENT", 240]]
C["steps"] = [                                        # a zoom step and a hit where he leans on a word with his face on screen
    [[0.44], 7.2], [[19.66], 20.8], [[40.08], 41.2]]
SKIP = [(0, 41.4), (66.6, 83.8)]                     # covered by the steps, the graphics, SALAH and the carousel
C["titles"] = [[m(a), m(b), *r] for a, b, *r in C["titles"]]
C["steps"] = [[[m(x) for x in ts], m(e)] for ts, e in C["steps"]]
SKIP = [(m(a), m(b)) for a, b in SKIP]
C["punch"] = [p for p in C["punch"] if not any(a <= p[0] < b for a, b in SKIP)][:9]
QUIET = [(39.7, 41.3), (66.6, 74.2)]                # build.py puts its own words here (SALAH, the 20-words wheel)
QUIET = [(m(a), m(b)) for a, b in QUIET]
C["caps"] = [c for c in C["caps"] if not any(a <= c[0] < b for a, b in QUIET)]
FIX = {"monkar": "Munkar", "nakila": "Nakir", "bharzakh.": "barzakh.", "Khushur": "khushūʿ", "Khushu": "khushūʿ", "swords": "sūrahs", "Salah": "salah", "Salah.": "salah.",
       "Salah,": "salah,", "Salah?": "salah?", "Fatihah.": "al-Fātiḥah."}             # what the transcriber mishears
KEY = {"this", "grave", "munkar", "nakir", "barzakh", "judgement", "resurrected", "50,000", "years", "sun", "hot", "sweating", "afraid",
       "first", "salah", "content", "no,", "no", "khushūʿ", "solution", "understand", "20", "words", "half", "actions", "connect", "conversation", "lord",
       "arabic", "difficult", "not", "start", "believe", "feel", "difference", "commitment", "common", "comment", "dm"}
for c in C["caps"]:                                   # the key words land big and gold, the rest are small white words (kinetic captions)
    for w in c[2]: w[0] = FIX.get(w[0], w[0]); w[2] = w[0].strip(",.?!").lower() in KEY
C["sections"] = [[t[0], t[1]] for t in C["titles"]]
C["split"] = None
json.dump(C, open(os.path.join(W, "config.json"), "w"), ensure_ascii=False, indent=1)
print(len(C["titles"]), "titles,", len(C["steps"]), "step runs,", len(C["punch"]), "punches,", len(C["caps"]), "caption lines")
