"""The 20-words salah reel (owner, 12 Oct 2026): the template's config.json, filled in from the transcript.
Silences cut (owner, 13 Oct) except the pause before "your salah"; the times below are the take's own, mapped through the cut.
  python3 config.py /tmp/reel-salah      (after `reel.py <W> plan`; then zoom, masks, layers, mix, then build.py)"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from timemap import loader
W = sys.argv[1]; C = json.load(open(os.path.join(W, "config.json"))); m = loader(W)

C["flicks"] = []                                      # the flicker hook is its own clip, joined in front by build.py
C["titles"] = [                                       # behind the head, one per beat of the script
    [0.0, 3.2, "", "PICTURE THIS", 175], [7.3, 13.5, "", "THE GRAVE", 250], [13.5, 16.0, "", "BARZAKH", 280],
    [19.0, 23.1, "THE DAY OF", "JUDGEMENT", 185], [32.8, 39.7, "THE VERY", "FIRST THING", 175],
    [41.3, 46.4, "", "BE HONEST", 220], [46.9, 51.6, "ARE YOU", "CONTENT?", 250], [51.7, 60.2, "STRUGGLING WITH", "KHUSHU", 280],
    [61.2, 66.6, "TRY TO", "UNDERSTAND", 180], [91.0, 106.4, "HAVE A", "CONVERSATION", 145], [108.1, 111.4, "IS ARABIC", "DIFFICULT?", 190],
    [111.8, 115.9, "IS LEARNING", "20 WORDS?", 220], [116.1, 120.4, "", "NOT AT ALL", 200], [120.6, 124.3, "START WITH", "20 WORDS", 220],
    [124.7, 129.2, "YOU WILL", "FEEL IT", 280], [142.3, 145.6, "DROP A", "COMMENT", 260]]
C["steps"] = [                                        # a zoom step and a hit on every phrase the owner leans on
    [[0.44, 2.38, 5.10], 7.2], [[7.56, 9.96, 12.36], 13.4], [[13.86], 15.9],
    [[19.66], 22.9], [[23.24, 23.92, 24.44], 26.0], [[33.04, 34.48, 34.88], 39.6], [[40.08], 41.2]]
SKIP = [(0, 26.0), (32.8, 41.4), (66.6, 83.8)]        # covered by the steps, the slams, the counter and the carousel
C["titles"] = [[m(a), m(b), *r] for a, b, *r in C["titles"]]
C["steps"] = [[[m(x) for x in ts], m(e)] for ts, e in C["steps"]]
SKIP = [(m(a), m(b)) for a, b in SKIP]
C["punch"] = [p for p in C["punch"] if not any(a <= p[0] < b for a, b in SKIP)][:9]
QUIET = [(23.1, 26.0), (39.7, 41.3), (66.6, 83.8)]   # build.py puts its own words here (the counter, SALAH, the carousel)
QUIET = [(m(a), m(b)) for a, b in QUIET]
C["caps"] = [c for c in C["caps"] if not any(a <= c[0] < b for a, b in QUIET)]
FIX = {"monkar": "Munkar", "nakila": "Nakir", "bharzakh.": "barzakh.", "Khushur": "khushūʿ", "Khushu": "khushūʿ", "swords": "sūrahs", "Salah": "salah", "Salah.": "salah.",
       "Salah,": "salah,", "Salah?": "salah?", "Fatihah.": "al-Fātiḥah."}             # what the transcriber mishears
for c in C["caps"]:
    for w in c[2]: w[0] = FIX.get(w[0], w[0])
C["sections"] = [[t[0], t[1]] for t in C["titles"]]
C["split"] = None
json.dump(C, open(os.path.join(W, "config.json"), "w"), ensure_ascii=False, indent=1)
print(len(C["titles"]), "titles,", len(C["steps"]), "step runs,", len(C["punch"]), "punches,", len(C["caps"]), "caption lines")
