"""The edit of the Ramadan 100-days video (owner, 22 Oct 2026: "edit it like the ads"), after cut.py and the reel template's
words, cut, base nologo and plan: titles behind the head, the flicker hook and end, punch-ins, gold words, a step zoom on "really,
really, really", the app on a phone (panels of kind "app"), one split frame. Times are in the cut (cutwords.json); the fill-in is the
level-up ads' (reels/ad-level-up/edit.py).
  python3 edit.py WORK"""
import json, re, sys
W = sys.argv[1]
S = dict(
    em=[2.76, 6.46, 7.88, 10.04, 12.24, 21.38, 25.94, 27.18, 29.6, 32.26, 37.38, 38.44, 42.64, 50.84, 54.98, 60.12, 62.4, 66.84, 71.62,
        74.12, 77.78, 79.82, 82.66, 85.02],
    words={20.68: "azza", 20.88: "wa jall"},
    titles=[[4.02, 8.34, "THAT CAME UP", "FAST", 340], [8.38, 13.4, "THE SALAF PREPARED", "6 MONTHS", 260],
            [13.44, 22.3, "6 MONTHS ASKING ALLAH TO", "ACCEPT IT", 230], [22.36, 28.34, "6 MONTHS ASKING ALLAH", "TO REACH IT", 220],
            [28.38, 30.62, "NOW WE HAVE", "100 DAYS", 280], [30.66, 37.62, "THE BEST RAMADAN?", "START NOW", 240],
            [37.66, 39.44, "START READING", "QURAN", 320], [39.48, 45.04, "WAKE UP AT", "NIGHT", 320],
            [45.08, 52.8, "ONE THING THAT HELPS", "ARABIC", 300], [68.78, 72.74, "THE DIFFERENCE TO YOUR", "WORSHIP", 270],
            [72.78, 77.14, "THE BEST RAMADAN", "EVER", 340]],
    panels=[[55.64, 63.4, "prayalong", "EVERY WORD OF YOUR SALAH", 2.9], [79.26, 83.24, "home", "DO YOUR DAILY TASKS", 0]],
    split=[63.44, 68.74],
    flicks=[[0, 3.9, "100 DAYS", 260], [77.18, 79.24, "RAFIQARABIC.COM", 120], [83.28, None, "BEST RAMADAN EVER", 140]],
    steps=[[[47.38, 47.76, 48.06], 48.6]],
    punch=[[6.46, 6.9], [10.04, 10.38], [12.24, 12.6], [21.38, 21.68], [25.94, 26.22], [29.6, 29.88], [37.38, 37.6], [50.84, 51.1],
           [74.12, 74.34]])
FIX = {"din": "deen", "rafah": "Rafiq", "rafik": "Rafiq", "rafih": "Rafiq", "rafeeq": "Rafiq", "rafiq": "Rafiq", "realize": "realise",
       "worshiping": "worshipping", "sauras": "surahs"}

C = json.load(open(f"{W}/config.json")); end = C["end"]
for c in C["caps"]:                                      # the brand and Arabic words spelled right; "RafiqArabic .com" as one word
    ws = c[2]
    for w in ws:
        core = re.sub(r"[^\w']", "", w[0]).lower(); tail = re.sub(r"^[\w' -]+", "", w[0])
        if core.startswith("raf") and "arabic" in core: w[0] = "RafiqArabic.com"
        elif core in FIX: w[0] = FIX[core] + tail
        w[0] = S["words"].get(round(w[1], 2), w[0])
        w[2] = round(w[1], 2) in S["em"]
    c[2] = [w for i, w in enumerate(ws) if w[0] and not (w[0].lower().startswith(".com") and i and ws[i - 1][0] == "RafiqArabic.com")]
C["caps"] = [c for c in C["caps"] if c[2]]
C["title_top"] = 250                                     # he sits higher in this frame (head top ~400): the hair covers the big word's foot
C["titles"] = S["titles"]
C["panels"] = [[a, b, "app", {"clip": c, "title": t, "from": f}] for a, b, c, t, f in S["panels"]]
C["flicks"] = [[a, b if b is not None else end, t, z] for a, b, t, z in S["flicks"]]
C["punch"] = S["punch"]; C["steps"] = S["steps"]; C["split"] = S["split"]
C["broll"]["split"] = ["mostsaid", "listen", "prayalong"]   # the surahs and the salah, not the grammar tiles
cuts = sorted({0, end} | set(C["split"]) | {x[0] for x in C["titles"]} | {x for p in C["panels"] for x in p[:2]} | {x for f in C["flicks"] for x in f[:2]})
C["sections"] = [[a, b] for a, b in zip(cuts, cuts[1:]) if b - a > .3]
json.dump(C, open(f"{W}/config.json", "w"), indent=1, ensure_ascii=False)
print(" | ".join(" ".join(w[0].upper() if w[2] else w[0] for w in c[2]) for c in C["caps"]))
