# Captions for the "beautiful" pair (owner, 10 Nov 2026), and a check of the carousel's three explanations (accurate, fair to the tafsir?).
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = {"reel": ("A 70-second Reel from Rafiq, a small account teaching the Arabic Muslims use: jamil (beautiful) and jamal (camel) share the root j-m-l; "
                "camels were beauty and wealth to the Arabs (Quran 16:6); jumla, a sentence; a quiz on 'Allah is beautiful and loves beauty' (Muslim 91); "
                "it ends 'tag someone beautiful, just maybe don't call them a camel'. The caption under it:"),
       "car": ("A 6-slide Instagram carousel from Rafiq: three things the Quran calls beautiful (patience 12:18, leaving 73:10, forgiving 15:85), "
               "then 'Allah is beautiful and loves beauty' (Muslim 91), then 'which one do you need most? comment 1, 2 or 3'. The caption under it:")}
WHO = {"scroller": "a 22-year-old UK Muslim scrolling", "learner": "a 34-year-old learning Arabic", "sister": "a 27-year-old UK Muslim woman"}
CAP = {"reel": {
  "a": "Beautiful and camel. Same three letters in Arabic: ج م ل 🐪\n\nجَمِيل jamīl = beautiful\nجَمَل jamal = camel\nجُمْلَة jumla = a sentence\n\nSo... is al-jamāl in the hadith camels, or beauty? Did you get it before the answer? 👇\n\nTag someone beautiful (maybe don't call them a camel).\n\n#arabic #learnarabic #quran #islam #muslim",
  "b": "Why would the Arabs use the same letters for 'beautiful' and 'camel'? 🐪\n\nBecause a herd of camels was beauty and wealth in one. Allah says it in Surat an-Nahl: 'and for you there is beauty in them.'\n\nOne root, ج م ل, and you start seeing it everywhere in the Qur'an.\n\nComment the answer to the quiz: camels or beauty? 👇\n\n#arabic #learnarabic #quran #islam #muslim"},
 "car": {
  "a": "Three things the Qur'an calls beautiful, and none of them are about looks.\n\n1. Patience with no complaint to people (12:18)\n2. Leaving those who hurt you, without insult (73:10)\n3. Forgiving with no blame after it (15:85)\n\nWhich one do you need most right now? Comment 1, 2 or 3 👇\n\n#quran #islam #muslim #arabic #sabr",
  "b": "Your patience can be beautiful. So can the way you walk away, and the way you forgive.\n\nThe Qur'an uses the word jamīl, beautiful, for how we act. Swipe for three of them.\n\nWhich one do you need most right now? Comment 1, 2 or 3 👇\n\n#quran #islam #muslim #arabic #sabr"}}
Q = {"good": {"type": "score", "instructions": "`ctx` `h` Viewer: `who`. Does this caption make them more likely to comment, share or save?", "criteria": ["No", "A little", "Yes", "Very much"]},
     "fair": {"type": "score", "instructions": "`ctx` `h` Is it accurate and respectful about Islam and the Arabic?", "criteria": ["No", "Partly", "Mostly", "Fully"]}}
jobs = [(v, k, w) for v in CAP for k in CAP[v] for w in WHO for _ in range(2)]
with ThreadPoolExecutor(24) as ex: res = list(ex.map(lambda j: (j, ask({"ctx": CTX[j[0]], "h": CAP[j[0]][j[1]], "who": WHO[j[2]]}, Q)["answers"]), jobs))
for v in CAP:
    for k in CAP[v]:
        s = {q: round(sum(a[q]["score"] for (vv, kk, _), a in res if vv == v and kk == k) / 6, 2) for q in Q}
        print(v, k, s, round(sum(s.values()), 2))
# (round 2: "three things" not "Allah calls three things", which overclaims; 15:85 as the tafsir words it, bila itab)
# the carousel's three explanations, against the tafsir
EX = {"12:18": "Sabr jamil (Quran 12:18, Yaqub when told Yusuf was killed): patience with no complaint to people, only to Allah.",
      "73:10": "Hajr jamil (Quran 73:10): walking away from those who hurt you, without insult and without revenge.",
      "15:85": "Safh jamil (Quran 15:85): forgiveness with no blame or reproach after it."}
QA = {"acc": {"type": "score", "instructions": "A one-line explanation on an Islamic post: `h` Does it match the classical tafsir (e.g. Ibn Kathir, al-Tabari)?", "criteria": ["No", "Partly", "Mostly", "Fully"]}}
with ThreadPoolExecutor(12) as ex: r2 = list(ex.map(lambda k: (k, ask({"h": EX[k]}, QA)["answers"]), [k for k in EX for _ in range(3)]))
for k in EX: print(k, round(sum(a["acc"]["score"] for kk, a in r2 if kk == k) / 3, 2), [a["acc"].get("reason", "")[:160] for kk, a in r2 if kk == k][:1])
