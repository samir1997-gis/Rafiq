# The ruku reel's config (#233): applied after `reel.py plan`. Times are in the cut.
import json, re
C = json.load(open("config.json"))
def rakah(first, sit, last):
    s = [("t",2)] + ([("o",15)] if first else []) + [("f",30),("t",2),("k",9),("r",7),("t",2),("s",9),("t",2),("g",3),("t",2),("s",9)]
    if sit: s += [("t",2),("h",28)]
    if last: s += [("w",34),("x",8)]
    return s
seq = "".join(("g" if k == "r" else ".") * n for k, n in rakah(1,0,0)+rakah(0,1,0)+rakah(0,0,0)+rakah(0,1,1))
assert len(seq) == 425
C["flicks"] = [[0, 2.45, "17 TIMES A DAY", 150], [23.41, 24.85, "YOU ANSWER", 150], [69.9, C["end"], "RAFIQ", 260]]
C["titles"] = [[2.5, 6.0, "YOU'RE HAVING A", "CONVERSATION", 160],
               [48.36, 52.85, "PRAISE RUNS THROUGH IT", "ح م د", 340],
               [52.9, 59.6, "EVEN HIS NAME", "MUHAMMAD", 190]]
C["panels"] = [
  [8.1, 23.41, "words", {"title": "RISING FROM RUKU · YOU SAY",
     "words": [["سَمِعَ", "hears", 11.4], ["اللَّهُ", "Allah", 13.22], ["لِمَنْ", "the one who", 15.86], ["حَمِدَهُ", "praises Him", 17.36]],
     "line": "“Allah hears the one who praises Him.”"}],
  [24.85, 33.1, "chat", {"title": "THE CONVERSATION", "pip": [0.55, 540, 810, 540, 720], "lines": [
     ["rising", "سَمِعَ اللَّهُ لِمَنْ حَمِدَهُ", "Allah hears the one who praises Him.", 25.0],
     ["standing straight", "رَبَّنا وَلَكَ الْحَمْدُ", "Our Lord, and to You belongs all praise.", 26.25]]}],
  [33.2, 42.6, "wall", {"title": "EVERY WORD OF A 4-RAKAH PRAYER", "seq": seq, "pre": "7 WORDS", "pre_t": 35.02, "light": 37.0, "dur": 1.6, "stat": 39.28,
     "big": "1 IN 15", "sub": "of the words you say are these two lines<br><small>425 words · 28 of them · not counting the surah you add</small>"}],
  [42.6, 48.36, "count", {"title": "ONCE EVERY RAKAH", "prayers": [["FAJR",2],["DHUHR",4],["ASR",4],["MAGHRIB",3],["ISHA",4]],
     "fill": 42.7, "dur": 0.6, "big": "17×", "sub": "a day, every day", "big_t": 43.31, "year": "6,205 A YEAR", "year_t": 46.17}]]
C["split"] = [61.2, 65.75]
C["steps"] = []
C["punch"] = [[3.04, 3.6], [50.07, 50.4], [56.79, 57.4], [58.77, 59.17], [66.87, 67.05], [67.95, 68.19]]
C["broll"] = {"split": ["risecut", "me", "parts"], "flick": ["self0", "rise", "self1", "self2", "orbit", "self3", "self4", "self5"]}
# captions: fix what speech recognition got wrong, and the gold pops
FIX = {"court": "ruku", "court,": "ruku,", "forakat": "four-rakah", "everyone": "every one", "rakur,": "ruku,", "rakur": "ruku", "...our": "our", "rafiqarabic": "rafiq-arabic.com", ".com": "", "His": "hears", "fora": "four-", "ka": "rakah", "rakur,": "ruku,", }
EM = {"conversation", "hears", "praises", "answer", "seven", "words.", "fifteen", "seventeen", "thousand", "hamd", "muhammad", "praised", "exactly", "learn"}
for c in C["caps"]:
    for w in c[2]:
        w[0] = FIX.get(w[0], w[0])
        w[2] = w[0].strip(",.?!'").lower() in {e.strip(".") for e in EM} and not (8.1 <= w[1] < 23.41 and w[0].lower() == "praises" and w[1] < 18)
json.dump(C, open("config.json", "w"), ensure_ascii=False, indent=1)
for c in C["caps"]: print(c[0], " ".join(w[0] + ("*" if w[2] else "") for w in c[2]))
