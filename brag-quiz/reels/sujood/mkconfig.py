# The sujood reel's config (#263): applied after `reel.py plan`, in the ruku reel's style (../samia/mkconfig.py).
# The owner's rules for this one (18 Oct 2026): no cuts, no trims, the voice untouched (`mix keepvoice`); add the captions,
# graphics, titles behind the head, sound effects, and his own B-roll (DJI_20261018181326_0042_D: sujood 10-14 s, sitting 15-20 s),
# laid over the picture while he keeps talking (cut.mov is composited before `zoom`; see README in this folder).
import json
C = json.load(open("config.json"))
C["flicks"] = [[0, 2.6, "AT YOUR LOWEST", 150], [86.9, C["end"], "WHICH PART NEXT?", 120]]
C["titles"] = [[2.8, 6.3, "YOU CALL ALLAH", "THE MOST HIGH", 170],
               [64.96, 70.3, "THE PROPHET SAID", "NEVER CLOSER", 190],
               [74.4, 79.2, "NEXT TIME YOU'RE IN", "SUJOOD", 260]]
C["panels"] = [
  [15.0, 34.3, "words", {"title": "IN SUJOOD · YOU SAY",
     "words": [["سُبْحانَ", "glory be", 16.92], ["رَبِّيَ", "my Lord", 21.44], ["الْأَعْلى", "the Most High", 25.4]],
     "line": "“Glory be to my Lord, the Most High.”"}],
  [39.2, 55.7, "words", {"title": "SITTING BETWEEN THE TWO · YOU SAY",
     "words": [["رَبِّ", "my Lord", 40.84], ["اغْفِرْ لِي", "forgive me", 42.94], ["وَارْحَمْنِي", "have mercy on me", 45.66]],
     "line": "“My Lord, forgive me and have mercy on me.”"}],
  [55.8, 61.0, "count", {"title": "EVERY RAKAH, EVERY DAY", "prayers": [["FAJR", 2], ["DHUHR", 4], ["ASR", 4], ["MAGHRIB", 3], ["ISHA", 4]],
     "fill": 55.9, "dur": 0.8, "big": "100+", "sub": "times a day<br><small>102 in sujood · 17 sitting between</small>", "big_t": 58.96,
     "year": "43,000+ A YEAR", "year_t": 60.0}],
  # the hadith he quotes, with its source (owner, 18 Oct 2026); each part lights as he says it
  [69.0, 74.4, "words", {"title": "THE PROPHET (PBUH) SAID · SAHIH MUSLIM 482", "ar": 54,
     "words": [["أَقْرَبُ مَا يَكُونُ الْعَبْدُ", "the closest a servant is", 71.06], ["مِنْ رَبِّهِ", "to his Lord", 72.1], ["وَهُوَ سَاجِدٌ", "is in sujood", 73.86]],
     "line": "“The closest a servant is to his Lord is when he is in sujood, so make lots of du'a.”"}]]
C["split"] = [79.5, 84.5]
# "the Most High": a zoom step and a hit on each word, a boom under "High" (owner, 18 Oct 2026: not emphasised enough)
C["steps"] = [[[5.58, 5.94], 6.3], [[27.12, 27.46], 27.9], [[33.48, 33.78], 34.3]]
C["punch"] = [[8.62, 9.2], [71.06, 71.8], [75.3, 75.7], [78.56, 79.1], [84.92, 85.5]]
C["sections"] = [[0, 7.66], [7.66, 15.0], [15.0, 34.78], [34.78, 55.8], [55.8, 64.96], [64.96, 74.4], [74.4, 79.5], [79.5, C["end"]]]
C["broll"] = {"split": ["sujoodcut", "prayalong", "sitcut"], "flick": ["self0", "sujood", "self1", "sit", "self2", "self3"]}
# captions: fix what speech recognition got wrong, and the gold pops
FIX = {"Sajud,": "sujood,", "Sajud": "sujood", "Rabbiyal": "rabbiyal", "Atla.": "a'la.", "Atla": "a'la", "-Atla": "a'la", "Rabbiyah": "rabbiya", "Rabi": "rabbiya", "rabbih": "rabbighfir",
       "firli": "li", "ikhfir": "ighfir", "SAW": "(pbuh)", "RafeeqArabic": "rafiq-arabic", ".com.": ".com", "ta": "ta'ala,", "Subhana": "subhana"}
EM = {"lowest", "most", "high", "sujood", "glory", "lord", "forgive", "mercy", "100", "important", "never", "closer", "remember", "learn", "next"}
for c in C["caps"]:
    c[2] = [w for w in c[2] if w[0].strip(",") != "'ala"]   # whisper split ta'ala in two
    for w in c[2]:
        w[0] = "rabbi" if abs(w[1] - 39.22) < .05 else FIX.get(w[0], w[0])   # "Rabbi: my Lord", not the start of rabbighfir
        w[2] = w[0].strip(",.?!'").lower() in EM
json.dump(C, open("config.json", "w"), ensure_ascii=False, indent=1)
for c in C["caps"]: print(round(c[0], 2), " ".join(w[0] + ("*" if w[2] else "") for w in c[2]))
