"""The edit of the five level-up trial cuts (owner, 21 Oct 2026: "edit them with graphics, with clips of Rafiq, so that it's not
just me talking"; the app footage is the "Imagine understanding every word of your salah" ad's, brag-output-v9-12/clips/).
Each version goes through the reel template (reels/template/README.md); this fills in its config.json after `plan`:
titles behind the head, the flicker hook and end, punch-ins, gold words, and the app on a phone (panels of kind "app")
while the owner keeps talking. Times are in the cut (cutwords.json).
  python3 edit.py WORK N        (WORK has been through words, cut, base nologo and plan; N = 1..5)"""
import json, re, sys
W, N = sys.argv[1], int(sys.argv[2])

V = {   # per version: gold words (their start times), titles, app panels, flicks, punch-ins, sections
    1: dict(
        em=[1.7, 6.68, 11.26, 15.5, 18.32, 21.94, 25.94, 27.72, 30.5, 34.76, 37.2, 39.28, 42.54, 44.1, 49.4, 52.4, 55.26,
            58.32, 60.8, 62.32, 65.14, 67.48, 71.06, 75.74, 77.62, 80.02, 82.74, 84.36, 87.84, 94.54],
        titles=[[3.56, 11.8, "THE ODDS ARE", "STACKED", 280], [11.86, 20.3, "EVERYWHERE YOU TURN", "FITNA", 320],
                [20.4, 28.0, "IT'S NOT ENOUGH TO BE", "PASSIVE", 300], [28.04, 32.4, "WE HAVE TO", "LEVEL UP", 280],
                [37.74, 41.38, "THE EASIEST WAY", "ARABIC", 300], [44.0, 50.1, "THE QURAN CAME DOWN", "IN ARABIC", 250],
                [53.66, 57.35, "MY PROPOSAL", "SIMPLE", 300], [68.54, 71.85, "NO CHANGE?", "FULL REFUND", 190],
                [77.14, 80.0, "ARE YOU", "READY?", 320], [85.74, 90.2, "EVERYONE GETS", "7 DAYS FREE", 190]],
        panels=[[32.44, 37.7, "home", "INVEST IN YOURSELF", 0], [41.42, 43.95, "words", "LEARN THE WORDS", .3],
                [63.0, 68.5, "count", "A CHANGE IN YOUR SALAH", 0], [71.9, 77.1, "plans", "LESS THAN A COFFEE A MONTH", 0],
                [80.0, 83.7, "prayalong", "INVEST IN YOUR DEEN", 2.9]],
        split=[57.4, 62.98],
        flicks=[[0, 3.5, "MUSLIM IN 2026", 150], [83.74, 85.7, "RAFIQARABIC.COM", 120], [93.0, None, "7 DAYS FREE", 170]],
        punch=[[6.68, 7.1], [11.26, 11.8], [18.32, 18.7], [25.94, 26.4], [30.5, 30.88], [39.28, 39.76], [49.4, 49.9],
               [71.06, 71.6], [77.62, 77.9]]),
    2: dict(
        em=[1.42, 4.14, 6.42, 11.4, 15.96, 18.12, 22.12, 23.9, 26.66, 30.94, 33.38, 35.46, 38.72, 41.42, 42.74, 44.1, 47.74,
            53.12, 55.0, 57.42, 60.1, 61.76, 65.24, 71.94],
        words={48.08: "azza", 48.36: "wa jall.", 54.46: ""},
        titles=[[2.44, 4.9, "A BIG STATEMENT", "TRUTH", 320], [4.92, 16.6, "THE ODDS ARE", "STACKED", 280],
                [16.62, 24.4, "IT'S NOT ENOUGH TO BE", "PASSIVE", 300], [24.44, 28.6, "WE HAVE TO", "LEVEL UP", 280],
                [33.86, 37.58, "THE EASIEST WAY", "ARABIC", 300], [45.42, 49.26, "TALKING TO", "ALLAH", 320],
                [54.46, 57.4, "ARE YOU", "READY?", 320], [63.54, 67.6, "EVERYONE GETS", "7 DAYS FREE", 190]],
        panels=[[28.62, 33.8, "home", "INVEST IN YOURSELF", 0], [37.6, 39.84, "words", "LEARN THE WORDS", .3],
                [39.86, 45.4, "mostsaid", "UNDERSTAND YOUR SALAH", 0], [49.28, 54.4, "plans", "LESS THAN A COFFEE A MONTH", 0],
                [57.42, 61.14, "prayalong", "INVEST IN YOUR DEEN", 2.9]],
        flicks=[[0, 2.4, "CHANGE YOUR LIFE", 140], [61.16, 63.5, "RAFIQARABIC.COM", 120], [70.4, None, "7 DAYS FREE", 170]],
        punch=[[4.14, 4.6], [11.4, 11.84], [22.12, 22.6], [26.66, 27.04], [35.46, 36.0], [47.74, 48.08], [55.0, 55.3], [65.24, 65.54]]),
    3: dict(
        em=[2.02, 7.08, 11.2, 12.1, 14.12, 18.88, 22.9, 24.68, 27.44, 31.68, 34.14, 36.22, 39.48, 41.04, 46.34, 51.08, 52.98,
            55.38, 58.08, 59.72],
        titles=[[3.04, 8.78, "CONSPIRING AGAINST", "YOU", 340], [8.8, 13.2, "TO TAKE YOU FROM YOUR", "DEEN", 320],
                [13.24, 17.3, "THE SOONER WE", "REALISE", 280], [17.36, 25.1, "IT'S NOT ENOUGH TO BE", "PASSIVE", 300],
                [25.16, 28.9, "WE HAVE TO", "LEVEL UP", 280], [34.7, 38.34, "THE EASIEST WAY", "ARABIC", 300],
                [40.98, 47.2, "THE QURAN CAME DOWN", "IN ARABIC", 250], [52.54, 55.36, "ARE YOU", "READY?", 320]],
        panels=[[28.92, 34.66, "home", "INVEST IN YOURSELF", 0], [38.36, 40.95, "words", "LEARN THE WORDS", .3],
                [47.26, 52.5, "plans", "LESS THAN A COFFEE A MONTH", 0], [55.38, 58.44, "prayalong", "INVEST IN YOUR DEEN", 2.9]],
        flicks=[[0, 3.0, "FORCES AGAINST YOU", 130], [58.46, None, "RAFIQARABIC.COM", 120]],
        punch=[[7.08, 7.34], [11.2, 11.6], [14.76, 15.2], [22.9, 23.3], [27.44, 27.86], [36.22, 36.7], [46.34, 46.8], [52.98, 53.2]]),
    4: dict(
        em=[0.42, 3.18, 5.44, 8.38, 11.86, 13.18, 16.3, 17.24, 19.26, 22.72, 25.62, 28.66, 31.14, 32.66, 35.48, 37.82, 41.4,
            42.46, 44.86, 47.54, 49.2],
        words={5.44: "du'a", 5.62: ""},
        titles=[[4.06, 6.0, "A DIFFERENCE IN YOUR", "DU'A", 320], [6.04, 14.1, "YOU'VE HEARD IT'S", "DIFFICULT", 250],
                [14.14, 17.5, "PEOPLE START, THEN", "QUIT", 330], [24.0, 27.7, "MY PROPOSAL", "SIMPLE", 300],
                [38.9, 42.0, "NO CHANGE?", "FULL REFUND", 190], [42.04, 44.84, "ARE YOU", "READY?", 320]],
        panels=[[17.52, 20.5, "tutor", "THE SOLUTION", 5.0], [33.78, 38.85, "count", "A CHANGE IN YOUR SALAH", 0],
                [44.86, 48.56, "prayalong", "INVEST IN YOUR DEEN", 2.9]],
        split=[27.72, 33.7],
        flicks=[[0, 3.9, "WITHIN DAYS", 200], [48.58, None, "RAFIQARABIC.COM", 120]],
        punch=[[13.18, 13.6], [17.24, 17.5], [23.36, 23.6], [25.62, 26.0], [41.4, 41.9], [42.46, 42.7]]),
    5: dict(
        em=[1.64, 5.64, 7.46, 10.18, 14.42, 16.88, 18.96, 22.22, 27.34, 29.24, 31.64, 34.3, 35.98],
        titles=[[2.7, 7.74, "IT'S NOT ENOUGH TO BE", "PASSIVE", 300], [7.76, 11.9, "WE HAVE TO", "LEVEL UP", 280],
                [17.18, 21.05, "THE EASIEST WAY", "ARABIC", 300], [28.44, 31.6, "ARE YOU", "READY?", 320]],
        panels=[[11.94, 17.15, "home", "INVEST IN YOURSELF", 0], [21.1, 23.05, "words", "LEARN THE WORDS", .3],
                [23.05, 28.4, "plans", "LESS THAN A COFFEE A MONTH", 0], [31.6, 35.36, "prayalong", "INVEST IN YOUR DEEN", 2.9]],
        flicks=[[0, 2.6, "NOT ENOUGH", 190], [35.36, None, "RAFIQARABIC.COM", 120]],
        punch=[[5.64, 6.0], [6.86, 7.1], [10.18, 10.6], [18.96, 19.5], [29.24, 29.5]]),
}
FIX = {"fitment": "fitna", "din": "deen", "car": "card", "rafah": "Rafiq", "rafik": "Rafiq", "rafih": "Rafiq", "rafeeq": "Rafiq", "rafiq": "Rafiq", "wall": "war", "realize": "realise"}

C = json.load(open(f"{W}/config.json")); S = V[N]; end = C["end"]
for c in C["caps"]:                                      # the brand and Arabic words spelled right; "RafiqArabic .com" as one word
    ws = c[2]
    for i, w in enumerate(ws):
        core = re.sub(r"[^\w']", "", w[0]).lower(); tail = re.sub(r"^[\w' -]+", "", w[0])
        if core.startswith("raf") and "arabic" in core: w[0] = "RafiqArabic.com"
        elif core in FIX: w[0] = FIX[core] + tail
        w[0] = S.get("words", {}).get(round(w[1], 2), w[0])          # words fixed by hand ("" drops a doubled one)
        w[2] = round(w[1], 2) in S["em"]
    c[2] = [w for i, w in enumerate(ws) if w[0] and not (w[0].lower().startswith(".com") and i and ws[i - 1][0] == "RafiqArabic.com")]
C["caps"] = [c for c in C["caps"] if c[2]]
C["title_top"] = 530                                     # the hair covers the bottom of the big word (head top ~680)
C["titles"] = S["titles"]
C["panels"] = [[a, b, "app", {"clip": c, "title": t, "from": f}] for a, b, c, t, f in S["panels"]]
C["flicks"] = [[a, b if b is not None else end, t, z] for a, b, t, z in S["flicks"]]
C["punch"] = S["punch"]; C["steps"] = S.get("steps", []); C["split"] = S.get("split")
cuts = sorted({0, end} | set(C["split"] or []) | {x[0] for x in C["titles"]} | {x for p in C["panels"] for x in p[:2]} | {x for f in C["flicks"] for x in f[:2]})
C["sections"] = [[a, b] for a, b in zip(cuts, cuts[1:]) if b - a > .3]
json.dump(C, open(f"{W}/config.json", "w"), indent=1, ensure_ascii=False)
print(" | ".join(" ".join(w[0].upper() if w[2] else w[0] for w in c[2]) for c in C["caps"]))
