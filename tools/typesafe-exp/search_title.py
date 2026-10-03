# Google result for rafiq-arabic.com (#199): which title + description gets the click?
from concurrent.futures import ThreadPoolExecutor
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from videos_v9 import ask, Q, VIEWERS
DESC = "Understand every word of your salah, and learn Arabic in short daily lessons with native audio. Free for 7 days, no card needed."
TITLES = {"now": "Rafiq — your Arabic study companion",
          "salah_first": "Rafiq: understand every word of your salah, learn Arabic",
          "arabic_first": "Rafiq Arabic: learn Arabic and understand your salah",
          "app": "Rafiq — the Arabic app for understanding your salah"}
SEARCHES = ["learn arabic app uk", "understand salah meaning", "rafiq arabic", "learn quran arabic for beginners"]
QS = {"click": Q("Someone (`viewer`) searched Google for '`s`'. One result reads: title `t`, under it `d`. How likely are they to click it?", ["Unlikely", "Maybe", "Likely", "Very likely"])}
if __name__ == "__main__":
    runs = [(k, s, v) for k in TITLES for s in SEARCHES for v in VIEWERS]
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(lambda r: ask({"viewer": VIEWERS[r[2]], "s": r[1], "t": TITLES[r[0]], "d": DESC}, QS)["answers"]["click"]["score"], runs))
    for k in TITLES:
        by = {s: sum(x for (n, ss, _), x in zip(runs, res) if n == k and ss == s) / len(VIEWERS) for s in SEARCHES}
        print(f"{k:<13} all {sum(by.values())/len(by):.2f}  " + "  ".join(f"{s.split()[0]}..{v:.2f}" for s, v in by.items()))

# Results (3 Oct 2026), 5 viewers per search, click likelihood (0-3) — overall / "learn arabic app uk" / "understand salah meaning" / "rafiq arabic" / "learn quran arabic":
#   now "Rafiq — your Arabic study companion"            2.12 / 2.24 / 1.94 / 2.07 / 2.22
#   "Rafiq: understand every word of your salah, ..."     2.14 / 2.29 / 1.96 / 2.09 / 2.23
#   "Rafiq Arabic: learn Arabic and understand your salah" 2.27 / 2.35 / 2.19 / 2.24 / 2.31   <- chosen
#   "Rafiq — the Arabic app for understanding your salah" 2.06
