# Hooks for the "beautiful" pair (owner, 10 Nov 2026): a reel (jamīl and jamal, camel, share the root ج م ل; "and for you there is beauty in them",
# an-Naḥl 16:6; jumla; "Allah is beautiful and loves beauty", Muslim 91) and a carousel (the Qur'an calls patience, leaving and forgiving
# "beautiful": ṣabr jamīl 12:18, hajr jamīl 73:10, ṣafḥ jamīl 15:85). Which opening line, and which first slide, stop the scroll?
exec(open("tools/typesafe-exp/darasa_caption.py").read().split("CTX =")[0])
CTX = {"reel": ("The first line, spoken and on screen from frame 0, of a 50-second Reel from Rafiq, a small account teaching the Arabic Muslims use. It shows that "
                "jamil (beautiful) and jamal (camel) share the root j-m-l; to the Arabs camels were beauty and wealth (Quran 16:6); the same root gives jumla, "
                "a sentence; then a quiz on the hadith 'Allah is beautiful and loves beauty'."),
       "slide": ("The first slide of a 6-slide Instagram carousel from Rafiq, a small account teaching the Arabic Muslims use. The carousel shows three things "
                 "the Quran calls 'beautiful' (jamil): beautiful patience (12:18, Yaqub losing Yusuf), beautiful leaving (73:10), beautiful forgiveness (15:85), "
                 "each explained, then 'Allah is beautiful and loves beauty' and 'which one do you need today? comment 1, 2 or 3'.")}
WHO = {"scroller": "a 22-year-old UK Muslim scrolling", "learner": "a 34-year-old learning Arabic", "sister": "a 27-year-old UK Muslim woman"}
CAP = {"reel": {"letters": "In Arabic, 'beautiful' and 'camel' are built from the same three letters.", "bride": "Why would an Arab bride be happy to hear the word for camel?",
                "camel2": "The Arabic word for beautiful has a camel hiding inside it 🐪", "why": "Why does the Arabic word for 'beautiful' come from camels?"},
       "slide": {"faces": "The Qur'an calls 3 things 'beautiful'. None of them are faces.", "expect": "3 things Allah calls beautiful that you'd never expect.",
                 "patience": "Allah calls your patience beautiful. And 2 other things."}}
Q = {"stop": {"type": "score", "instructions": "`ctx` Line: `h`. Viewer: `who`. How likely are they to stop scrolling and keep watching (or swipe to slide 2)?", "criteria": ["Very unlikely", "Unlikely", "Likely", "Very likely"]},
     "fair": {"type": "score", "instructions": "`ctx` Line: `h`. Is it accurate and respectful, paid off fairly by the content?", "criteria": ["No", "Partly", "Mostly", "Fully"]}}
jobs = [(v, k, w) for v in ["reel"] for k in CAP[v] for w in WHO for _ in range(2)]
with ThreadPoolExecutor(24) as ex: res = list(ex.map(lambda j: (j, ask({"ctx": CTX[j[0]], "h": CAP[j[0]][j[1]], "who": WHO[j[2]]}, Q)["answers"]), jobs))
for v in ["reel"]:
    rows = [(k, {q: sum(a[q]["score"] for (vv, kk, _), a in res if vv == v and kk == k) / 6 for q in Q}) for k in CAP[v]]
    for k, s in sorted(rows, key=lambda x: -sum(x[1].values())): print(v, f"{k:9}", {q: round(x, 2) for q, x in s.items()}, round(sum(s.values()), 2), CAP[v][k])
