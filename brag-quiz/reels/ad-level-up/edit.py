"""The edit of the five level-up trial cuts (owner, 21 Oct 2026: "edit them with graphics, with clips of Rafiq, so that it's not
just me talking"; the app footage is the "Imagine understanding every word of your salah" ad's, brag-output-v9-12/clips/).
Each version goes through the reel template (reels/template/README.md); this fills in its config.json after `plan`:
titles behind the head, the flicker hook and end, punch-ins, gold words, and the app on a phone (panels of kind "app")
while the owner keeps talking. Times are in the cut (cutwords.json).
  python3 edit.py WORK N        (WORK has been through words, cut, base nologo and plan; N = 1..5)"""
import json, re, sys
W, N = sys.argv[1], int(sys.argv[2])

V = {   # per version: gold words (their start times), titles, app panels, flicks, punch-ins, sections
    5: dict(
        em=[1.64, 5.64, 7.46, 10.18, 14.42, 16.88, 18.96, 22.22, 27.34, 29.24, 31.64, 34.3, 35.98],
        titles=[[2.7, 7.74, "IT'S NOT ENOUGH TO BE", "PASSIVE", 300], [7.76, 11.9, "WE HAVE TO", "LEVEL UP", 280],
                [17.18, 21.05, "THE EASIEST WAY", "ARABIC", 300], [28.44, 31.6, "ARE YOU", "READY?", 320]],
        panels=[[11.94, 17.15, "home", "INVEST IN YOURSELF", 0], [21.1, 23.05, "words", "LEARN THE WORDS", .3],
                [23.05, 28.4, "plans", "LESS THAN A COFFEE A MONTH", 0], [31.6, 35.36, "prayalong", "INVEST IN YOUR DEEN", 2.9]],
        flicks=[[0, 2.6, "NOT ENOUGH", 190], [35.36, None, "RAFIQARABIC.COM", 120]],
        punch=[[5.64, 6.0], [6.86, 7.1], [10.18, 10.6], [18.96, 19.5], [29.24, 29.5]]),
}
FIX = {"fitment": "fitna", "din": "deen", "car": "card", "rafah": "Rafiq", "rafik": "Rafiq", "rafih": "Rafiq", "rafeeq": "Rafiq"}

C = json.load(open(f"{W}/config.json")); S = V[N]; end = C["end"]
for c in C["caps"]:                                      # the brand and Arabic words spelled right; "RafiqArabic .com" as one word
    ws = c[2]
    for i, w in enumerate(ws):
        core = re.sub(r"[^\w']", "", w[0]).lower(); tail = re.sub(r"^[\w' -]+", "", w[0])
        if core.startswith("raf") and "arabic" in core: w[0] = "RafiqArabic.com"
        elif core in FIX: w[0] = FIX[core] + tail
        w[2] = round(w[1], 2) in S["em"]
    c[2] = [w for i, w in enumerate(ws) if not (w[0].lower().startswith(".com") and i and ws[i - 1][0] == "RafiqArabic.com")]
C["title_top"] = 530                                     # the hair covers the bottom of the big word (head top ~680)
C["titles"] = S["titles"]
C["panels"] = [[a, b, "app", {"clip": c, "title": t, "from": f}] for a, b, c, t, f in S["panels"]]
C["flicks"] = [[a, b if b is not None else end, t, z] for a, b, t, z in S["flicks"]]
C["punch"] = S["punch"]; C["steps"] = S.get("steps", []); C["split"] = S.get("split")
cuts = sorted({0, end} | {x[0] for x in C["titles"]} | {x for p in C["panels"] for x in p[:2]} | {x for f in C["flicks"] for x in f[:2]})
C["sections"] = [[a, b] for a, b in zip(cuts, cuts[1:]) if b - a > .3]
json.dump(C, open(f"{W}/config.json", "w"), indent=1, ensure_ascii=False)
print(" | ".join(" ".join(w[0].upper() if w[2] else w[0] for w in c[2]) for c in C["caps"]))
